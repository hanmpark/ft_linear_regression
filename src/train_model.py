import os
import argparse
import matplotlib.pyplot as plt


def linear_regression(mileages, prices, verbose=False):
    """
    Train a linear regression model on the given data.

    Args:
        - mileages: A list of integers representing the car mileages.
        - prices: A list of integers representing the car prices.
        - verbose: A boolean indicating whether to print the cost at each epoch.

    Returns:
        - theta0: The intercept of the regression line.
        - theta1: The slope of the regression line.
    """
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
    """
    Parse the command line arguments.

    Returns:
        - args: An object containing the parsed arguments
    """
    parser = argparse.ArgumentParser(description="Train a linear regression model on car mileage and price data")

    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")

    return parser.parse_args()


def parse_data():
    """
    Parse the data from the data.csv file and return the mileages and prices as lists.

    Returns:
        - mileages: A list of integers representing the car mileages.
        - prices: A list of integers representing the car prices.
    """
    try:
        with open("./data/data.csv", "r") as file:
            data = [data.split(",") for data in [line.strip() for line in file.readlines()]][1:]
            data = [[int(values[0]), int(values[1])] for values in data]

            mileages = [values[0] for values in data]
            prices = [values[1] for values in data]

    except FileNotFoundError:
        print("data.csv file not found.")
        return None, None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

    return mileages, prices


def print_data(mileages, prices, theta0, theta1):
    """
    Print the data points and the regression line.

    Args:
        - mileages: A list of integers representing the car mileages.
        - prices: A list of integers representing the car prices.
        - theta0: The intercept of the regression line.
        - theta1: The slope of the regression line.

    Returns:
        None
    """
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


def main():
    args = parse_args()

    os.makedirs("img", exist_ok=True)

    mileages, prices = parse_data()
    if mileages is None or prices is None:
        return

    theta0, theta1 = linear_regression(mileages, prices, args.verbose == True)
    with open("./data/theta.csv", "w") as theta_file:
        theta_file.write(f"{theta0},{theta1}")

    print_data(mileages, prices, theta0, theta1)


if __name__ == "__main__":
    main()
