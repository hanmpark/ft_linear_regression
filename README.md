# ft_linear_regression

## Overview

**ft_linear_regression** is a project aimed at implementing a simple linear regression model from scratch to analyze and predict data. The project is an excellent introduction to machine learning concepts, particularly in understanding linear relationships and how models are trained.

## Features

- **Prediction**: Use the trained model to make predictions based on input data.
- **Training**: Implement gradient descent to train the model and find the optimal linear function.
- **Evaluation**: Evaluate the model's performance by calculating the mean squared error.
- **Visualization**: Optionally plot the dataset and the regression line for better understanding.

## Project Structure
```
.
├── LICENSE
├── README.md
├── data
│   ├── data.csv
│   └── theta.csv
├── requirements.txt
└── src
    ├── bonus.py
    ├── predict.py
    └── train_model.py
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/hanmpark/ft_linear_regression.git && cd ft_linear_regression
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage
### Training the Model

1. Prepare your dataset as a .csv file with two columns: one for features (x) and one for target values (y). Put a title before setting up the data set.
2. Train the model:
```bash
python3 train.py
```
This will output the trained parameters (`theta`) to a file for the predict program.

### Making Predictions
Use the trained model to make predictions:
```bash
python predict.py
```

## File Structure
- `src/train_model.py`: Contains the training logic for the linear regression model.
- `src/predict.py`: Uses the trained parameters to make predictions.
- `data/`: Directory for sample datasets.

## Project Constraints
- This project avoids using external learning libraries like `scikit-learn` to better understand the fundamentals.
- The implementation is written purely in Python for simplicity and flexibility.
