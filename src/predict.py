def predict(theta0: float, theta1: float) -> float:
    """
    Predicts the price of a car based on its mileage.

    Args:
        theta0 (float): The intercept of the regression line.
        theta1 (float): The slope of the regression line.

    Returns:
        float: The predicted price of the car.
    """

    input_mileage = int(input("Enter mileage: "))
    if input_mileage < 0:
        print("Error: mileage must be positive")
        return

    predicted_price = theta0 + theta1 * input_mileage
    return predicted_price


def main():
    try:
        with open("./data/theta.csv", "r") as theta_file:
            values = [value.strip() for value in theta_file.read().split(",")]

    except FileNotFoundError:
        print("theta.csv file not found. Please train the model first.")
        return

    except Exception as e:
        print(f"An error occurred: {e}")
        return

    if len(values) != 2 or not all([value.replace(".", "", 1).replace("-", "", 1).isdigit() for value in values]):
        print("Error: theta.csv is not properly formatted")
        return

    theta0, theta1 = [float(value) for value in values]

    print(f"Predicted price: {predict(theta0, theta1)}")


if __name__ == "__main__":
    main()
