def find_theta(mileages, prices):
	max_mileage = max(mileages)
	mileages = [mileage / max_mileage for mileage in mileages]

	# estimatedPrice = theta0 + theta1 * mileages
	theta0 = 0
	theta1 = 0
	learning_rate = 1
	epochs = 1000

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
			print(f"Epoch {epoch}/{epochs}: cost = {cost:.4f}, theta0 = {theta0:.4f}, theta1 = {theta1:.4f}")

	return theta0, theta1

def main():
	with open("data.csv", "r") as file:
		data = [data.split(",") for data in [line.strip() for line in file.readlines()]][1:]
		data = [[int(values[0]), int(values[1])] for values in data]

		mileages = [values[0] for values in data]
		prices = [values[1] for values in data]
		theta0, theta1 = find_theta(mileages, prices)

		theta_file = open("theta.csv", "w")
		theta_file.write(f"{theta0},{theta1}")
		theta_file.close()

if __name__ == "__main__":
	main()
