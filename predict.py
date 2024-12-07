def main():
	theta_file = open("theta.csv", "r")
	if not theta_file:
		print("Error: train the model first")
		return
	if len(theta_file.read().split(",")) != 2 or not theta_file.read().split(",")[0].isnumeric() or not theta_file.read().split(",")[1].isnumeric():
		print("Error: theta.csv is not properly formatted")
		return

	theta0, theta1 = [float(value) for value in theta_file.read().split(",")]

	input_mileage = int(input("Enter mileage: "))
	if input_mileage < 0:
		print("Error: mileage must be positive")
		return

	print(f"Price: {theta0 + theta1 * input_mileage}")

if __name__ == "__main__":
	main()
