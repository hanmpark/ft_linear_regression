import matplotlib.pyplot as plt

def find_theta(mileages, prices):
	max_mileage = max(mileages)
	max_price = max(prices)
	mileages = [mileage / max_mileage for mileage in mileages]
	prices = [price / max_price for price in prices]

	# estimatedPrice = theta0 + theta1 * mileages
	theta0 = 0
	theta1 = 0
	learning_rate = 0.1
	epochs = int(input("Enter the number of epochs: "))

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
		if epoch % 100 == 0:  # Optional: Print cost every 100 epochs for better readability
			cost = (1/n) * sum([(prices_pred[i] - prices[i]) ** 2 for i in range(n)])
			print(f"Epoch {epoch}: Cost = {cost}, theta0 = {theta0}, theta1 = {theta1}")

	theta0 *= max_price
	theta1 *= max_price / max_mileage

	return theta0, theta1

def main():
	with open("data.csv", "r") as file:
		data = [data.split(",") for data in [line.strip() for line in file.readlines()]][1:]
		data = [[int(values[0]), int(values[1])] for values in data]

		mileages = [values[0] for values in data]
		prices = [values[1] for values in data]

	theta0, theta1 = find_theta(mileages, prices)

	mileage_range = [min(mileages) + i * (max(mileages) - min(mileages)) / 100 for i in range(101)]
	predicted_prices = [theta0 + theta1 * x for x in mileage_range]

	plt.scatter(mileages, prices, color='blue', label='Data Points')
	plt.plot(mileage_range, predicted_prices, color='red', label='Regression Line')

	# Add labels and title
	plt.xlabel('Mileage')
	plt.ylabel('Price')
	plt.title('Car Mileage vs Price with Regression Line')
	plt.legend()

	# Display the plot
	plt.grid(True)
	plt.savefig("regression_plot.png")

	with open("theta.csv", "w") as theta_file:
		theta_file.write(f"{theta0},{theta1}")

if __name__ == "__main__":
	main()
