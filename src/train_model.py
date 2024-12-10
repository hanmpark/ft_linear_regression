import os
import argparse
import matplotlib.pyplot as plt

def linear_regression(mileages, prices, verbose=False):
	max_mileage = max(mileages)
	max_price = max(prices)
	mileages = [mileage / max_mileage for mileage in mileages]
	prices = [price / max_price for price in prices]

	# estimatedPrice = theta0 + theta1 * mileages
	theta0 = 0
	theta1 = 0
	learning_rate = 0.1
	epochs = 1500

	n = len(mileages)
	for epoch in range(epochs):
		prices_pred = [theta0 + theta1 * mileages[i] for i in range(n)]

		# Calculate gradients for theta0 and theta1:
		theta0_gradient = (1/n) * sum([prices_pred[i] - prices[i] for i in range(n)])
		theta1_gradient = (1/n) * sum([(prices_pred[i] - prices[i]) * mileages[i] for i in range(n)])

		# Update theta0 and theta1:
		theta0 -= theta0_gradient * learning_rate
		theta1 -= theta1_gradient * learning_rate

		# Print the cost using the mean squared error:
		if epoch % 100 == 0 and verbose:
			cost = (1/n) * sum([(prices_pred[i] - prices[i]) ** 2 for i in range(n)])
			print(f"Epoch {epoch}: Cost = {cost}, theta0 = {theta0}, theta1 = {theta1}")

	theta0 *= max_price
	theta1 *= max_price / max_mileage

	return theta0, theta1

def parse_args():
	parser = argparse.ArgumentParser(description="Train a linear regression model on car mileage and price data")

	parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")

	return parser.parse_args()

def main():
	args = parse_args()

	os.makedirs("img", exist_ok=True)

	try:
		with open("./data/data.csv", "r") as file:
			data = [data.split(",") for data in [line.strip() for line in file.readlines()]][1:]
			data = [[int(values[0]), int(values[1])] for values in data]

			mileages = [values[0] for values in data]
			prices = [values[1] for values in data]
	except FileNotFoundError:
		print("data.csv file not found.")
		return
	except Exception as e:
		print(f"An error occurred: {e}")
		return

	theta0, theta1 = linear_regression(mileages, prices, args.verbose == True)

	mileage_range = [min(mileages) + i * (max(mileages) - min(mileages)) / 100 for i in range(101)]
	predicted_prices = [theta0 + theta1 * x for x in mileage_range]

	# Plot the data points
	plt.scatter(mileages, prices, color='blue', label='Data Points')

	# Add labels and title
	plt.xlabel('Mileage')
	plt.ylabel('Price')
	plt.title('Car Mileage vs Price with Regression Line')
	plt.legend()

	# Display the scatter plot
	plt.grid(True)
	plt.show()
	plt.savefig("./img/plot.png")

	plt.scatter(mileages, prices, color='blue', label='Data Points')
	plt.plot(mileage_range, predicted_prices, color='red', label='Regression Line')

	# Add labels and title
	plt.xlabel('Mileage')
	plt.ylabel('Price')
	plt.title('Car Mileage vs Price with Regression Line')
	plt.legend()

	# Display the scatter plot with regression line
	plt.grid(True)
	plt.show()
	plt.savefig("./img/plot_with_linear.png")

	with open("./data/theta.csv", "w") as theta_file:
		theta_file.write(f"{theta0},{theta1}")

if __name__ == "__main__":
	main()