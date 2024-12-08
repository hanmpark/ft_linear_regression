def main():
	with open("theta.csv", "r") as theta_file:
		if not theta_file:
			print("Error: train the model first")
			return

		values = theta_file.read().split(",")
		if len(values) != 2 or not all([value.replace(".", "", 1).replace("-", "", 1).isdigit() for value in values]):
			print("Error: theta.csv is not properly formatted")
			return

	theta0, theta1 = [float(value) for value in values]

	input_mileage = int(input("Enter mileage: "))
	if input_mileage < 0:
		print("Error: mileage must be positive")
		return

	# Make the prediction
	predicted_price = theta0 + theta1 * input_mileage

	print(f"Price: {predicted_price}")

if __name__ == "__main__":
	main()
