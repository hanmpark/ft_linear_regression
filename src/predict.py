from loguru import logger


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
        logger.error("Mileage must be positive")
        return

    predicted_price = theta0 + theta1 * input_mileage
    return predicted_price


def main():
    try:
        with open("./data/theta.csv", "r") as theta_file:
            values = [value.strip() for value in theta_file.read().split(",")]
        if len(values) != 2 or not all([value.replace(".", "", 1).replace("-", "", 1).isdigit() for value in values]):
            logger.error("theta.csv is not properly formatted")
            return

        theta0, theta1 = [float(value) for value in values]

        logger.info(f"Predicted price: {predict(theta0, theta1)}")

    except FileNotFoundError:
        logger.exception("theta.csv file not found. Please train the model first.")
        return

    except Exception as e:
        logger.exception(f"An error occurred")
        return


if __name__ == "__main__":
    main()
