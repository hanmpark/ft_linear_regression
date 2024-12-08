import matplotlib.pyplot as plt
import os
import json
import requests
import time
from dotenv import load_dotenv
from datetime import datetime

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
	url = f"https://api.intra.42.fr/v2/users/{login}/locations"
	total_seconds = 0
	retries = 0

	while url:
		response = requests.get(url, headers=headers)

		# If we hit rate limiting (HTTP 429)
		if response.status_code == 429:
			retries += 1

			retry_after = response.headers.get("retry-after")

			if retry_after:
				# If the 'retry-after' header is present, wait for that many seconds
				wait_time = int(retry_after)
				time.sleep(wait_time)
			else:
				# If no 'retry-after' header, fallback to exponential backoff
				wait_time = 2 ** retries
				print(f"Waiting for {wait_time} seconds (exponential backoff).")
				time.sleep(wait_time)

			continue

		response.raise_for_status()
		logins = response.json()
		print(logins)

		# Calculate logtime for each session
		for log in logins:
			end_at = log.get("end_at")
			begin_at = log.get("begin_at")

			if end_at and begin_at:
				try:
					# Parse ISO 8601 strings to datetime objects
					end_at_dt = datetime.fromisoformat(end_at.replace("Z", "+00:00"))
					begin_at_dt = datetime.fromisoformat(begin_at.replace("Z", "+00:00"))

					# Accumulate session duration in seconds
					session_seconds = (end_at_dt - begin_at_dt).total_seconds()
					total_seconds += session_seconds

				except ValueError as e:
					print(f"Error parsing dates for login: {log}")
					print(f"Begin: {begin_at}, End: {end_at}, Error: {e}")

		# Check for next page
		url = response.links.get("next", {}).get("url")

	total_hours = total_seconds / 3600
	return total_hours

def main():
	load_dotenv()
	UID = os.getenv("42UID")
	SECRET = os.getenv("42SECRET")

	access_token = get_access_token(UID, SECRET)

	try:
		with open("common_core_completed.json", "r") as file:
			data = json.load(file)

	except FileNotFoundError:
		return
	except Exception as e:
		print(f"An error occurred: {e}")
		return

	# input("42 login: ")
	logtime = fetch_logtime("hanmpark", access_token)
	print(f"Total logtime: {logtime:.2f} hours")

if __name__ == "__main__":
	main()
