import matplotlib.pyplot as plt
import os
import json
import requests
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
from train_model import find_theta

def get_access_token(UID, SECRET):
	url = "https://api.intra.42.fr/oauth/token"
	data = {
		"grant_type": "client_credentials",
		"client_id": UID,
		"client_secret": SECRET
	}
	response = requests.post(url, data=data)
	response.raise_for_status()
	return response.json()["access_token"]

def fetch_logtime(login, access_token):
	headers = {"Authorization": f"Bearer {access_token}"}
	user_url = f"https://api.intra.42.fr/v2/users/{login}"
	log_url = f"https://api.intra.42.fr/v2/users/{login}/locations"
	total_seconds = 0
	retries = 0
	unique_days = set()

	# Fetch user details to get the cursus start date
	user_response = requests.get(user_url, headers=headers)
	if user_response.status_code == 404:
		print(f"Error: User {login} does not exist.")
		return 0, 0

	user_response.raise_for_status()
	user_data = user_response.json()

	# Extract cursus start date
	common_core_cursus = None
	for cursus in user_data["cursus_users"]:
		if cursus["cursus"]["name"] == "42cursus":
			common_core_cursus = cursus
			break

	if not common_core_cursus:
		print(f"Error: User {login} has no 42cursus data.")
		return 0, 0

	begin_date = datetime.fromisoformat(common_core_cursus["begin_at"].replace("Z", "+00:00")).date()
	completion_date = datetime.now().date()

	if "end_at" in common_core_cursus and common_core_cursus["end_at"]:
		completion_date = datetime.fromisoformat(common_core_cursus["end_at"].replace("Z", "+00:00")).date()

	total_days_in_cursus = (completion_date - begin_date).days + 1

	while log_url:
		response = requests.get(log_url, headers=headers)

		# If we hit rate limiting (HTTP 429)
		if response.status_code == 429:
			retries += 1
			retry_after = response.headers.get("retry-after")
			if retry_after:
				time.sleep(int(retry_after))
			continue

		response.raise_for_status()
		logins = response.json()

		# Calculate logtime for each session within cursus duration
		for log in logins:
			end_at = log.get("end_at")
			begin_at = log.get("begin_at")

			if end_at and begin_at:
				try:
					# Parse ISO 8601 strings to datetime objects
					end_at_dt = datetime.fromisoformat(end_at.replace("Z", "+00:00"))
					begin_at_dt = datetime.fromisoformat(begin_at.replace("Z", "+00:00"))

					# Clamp the session to the cursus duration
					if end_at_dt.date() < begin_date or begin_at_dt.date() > completion_date:
						continue

					begin_dt = datetime.fromisoformat(begin_at.replace("Z", "+00:00")).date()
					unique_days.add(begin_dt)
					end_dt = datetime.fromisoformat(end_at.replace("Z", "+00:00")).date()
					current_dt = begin_dt
					while current_dt <= end_dt:
						unique_days.add(current_dt)
						current_dt += timedelta(days=1)

					# Accumulate session duration in seconds
					session_seconds = (end_at_dt - begin_at_dt).total_seconds()
					total_seconds += session_seconds

				except ValueError as e:
					print(f"Error parsing dates for login: {log}")
					print(f"Begin: {begin_at}, End: {end_at}, Error: {e}")

		# Check for next page
		log_url = response.links.get("next", {}).get("url")

	total_hours = total_seconds / 3600
	return total_hours, len(unique_days), total_days_in_cursus

def main():
	load_dotenv()
	UID = os.getenv("42UID")
	SECRET = os.getenv("42SECRET")

	access_token = get_access_token(UID, SECRET)

	try:
		with open("common_core_completed.json", "r") as file:
			data = json.load(file)

	except FileNotFoundError:
		print("common_core_completed.json not found.")
		return
	except Exception as e:
		print(f"An error occurred: {e}")
		return

	login = input("42 login: ")
	logtime, connected_days, total_days_in_cursus = fetch_logtime(login, access_token)
	print(f"Total logtime: {logtime:.2f} hours in {connected_days} days out of {total_days_in_cursus} days in the cursus.")

if __name__ == "__main__":
	main()
