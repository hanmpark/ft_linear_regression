import matplotlib.pyplot as plt
import os
import json
import requests
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
from train_model import linear_regression

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

def fetch_cursus_duration(login, access_token):
	headers = {"Authorization": f"Bearer {access_token}"}
	begin_url = f"https://api.intra.42.fr/v2/users/{login}/cursus_users"
	end_url = f"https://api.intra.42.fr/v2/users/{login}/projects_users"
	begin_date = None
	end_date = None
	retries = 0
	required_projects = ("Exam Rank 06", "ft_transcendence")
	projects_done = []

	response = requests.get(begin_url, headers=headers)

	if response.status_code == 404:
		print(f"Error: User {login} not found.")
		return None, None

	response.raise_for_status()

	cursus_users = response.json()

	for cursus in cursus_users:
		cursus_name = cursus.get("cursus", {}).get("name")
		if cursus_name == "42cursus":
			begin_at = cursus.get("begin_at")
			if begin_at:
				begin_date = datetime.fromisoformat(begin_at.replace("Z", "+00:00")).date()

	while end_url:
		response = requests.get(end_url, headers=headers)

		if response.status_code == 429:
			retries += 1
			retry_after = response.headers.get("retry-after")
			if retry_after:
				time.sleep(int(retry_after))
			continue

		response.raise_for_status()
		projects = response.json()

		for project in projects:
			project_name = project.get("project", {}).get("name")
			validated = project.get("validated?")
			if project_name in required_projects and validated:
				project_marked_at = project.get("marked_at")
				projects_done.append(project_marked_at)

		if len(projects_done) == 2:
			break

		end_url = response.links.get("next", {}).get("url")

	if len(projects_done) == 2:
		end_date = datetime.fromisoformat(projects_done[0].replace("Z", "+00:00")).date()

	return begin_date, end_date

def fetch_logtime(login, access_token):
	headers = {"Authorization": f"Bearer {access_token}"}
	log_url = f"https://api.intra.42.fr/v2/users/{login}/locations"
	total_seconds = 0
	retries = 0
	unique_days = set()

	# Get the cursus duration
	begin_date, end_date = fetch_cursus_duration(login, access_token)
	if not begin_date:
		return 0, 0, 0, False

	if end_date:
		completion_date = end_date
	else:
		completion_date = datetime.now().date()

	total_days_in_cursus = (completion_date - begin_date).days + 1

	# Fetch logtime during the common core
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
	return total_hours, len(unique_days), total_days_in_cursus, end_date != None

def visualize_data(data, logtime, connected_days, total_days_in_cursus):
	days_duration = [login_data["dateDuration"] for login_data in data]
	logtime_per_day = [login_data["logtimeHours"] / login_data["dateDuration"] for login_data in data]

	plt.scatter(logtime_per_day, days_duration, color='blue', label='Data Points')

	plt.xlabel("Logtime per Day (hours)")
	plt.ylabel("Days in cursus")
	plt.title("Days in common core vs. Logtime per Day")
	plt.legend()

	plt.grid(True)
	plt.show()
	plt.savefig("./img/common_core_plot.png")

	theta0, theta1 = linear_regression(logtime_per_day, days_duration)

	logtime_per_day_range = [min(logtime_per_day) + i * (max(logtime_per_day) - min(logtime_per_day)) / 100 for i in range(101)]
	predicted_days_duration = [theta0 + theta1 * x for x in logtime_per_day_range]

	plt.scatter(logtime_per_day, days_duration, color='blue', label='Data Points')
	plt.plot(logtime_per_day_range, predicted_days_duration, color='red', label='Regression Line')

	plt.xlabel("Logtime per Day (hours)")
	plt.ylabel("Days in cursus")
	plt.title("Days in common core vs. Logtime per Day with regression line")
	plt.legend()

	plt.grid(True)
	plt.show()
	plt.savefig("./img/common_core_plot_with_linear.png")

	user_logtime_per_day = logtime / total_days_in_cursus

	print(f"User logtime per day: {user_logtime_per_day:.2f} hours")

	predicted_days_for_user = theta0 + theta1 * user_logtime_per_day

	days_left = predicted_days_for_user - total_days_in_cursus

	print(f"Predicted days left in common core: {days_left:.2f}")

def main():
	load_dotenv()
	UID = os.getenv("42UID")
	SECRET = os.getenv("42SECRET")

	os.makedirs("img", exist_ok=True)

	access_token = get_access_token(UID, SECRET)

	try:
		with open("./data/common_core_completed.json", "r") as file:
			data = json.load(file)

	except FileNotFoundError:
		print("common_core_completed.json not found.")
		return
	except Exception as e:
		print(f"An error occurred: {e}")
		return

	login = input("42 login: ")
	logtime, connected_days, total_days_in_cursus, has_finished_common_core = fetch_logtime(login, access_token)
	print(f"\033[1mtotal logtime: {logtime:.2f} hours, connected days: {connected_days}, total days: {total_days_in_cursus}\033[0m")

	if has_finished_common_core:
		print("User has already finished the common core.")
	else:
		visualize_data(data, logtime, connected_days, total_days_in_cursus)

if __name__ == "__main__":
	main()
