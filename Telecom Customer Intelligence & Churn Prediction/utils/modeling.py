"""
This module contains functions for modeling.

functions:
    save_estimator: Saves the estimator to the specified file path using joblib.
    load_estimator: Loads the estimator from the specified file path using joblib.
"""
from joblib import dump, load


def save_estimator(estimator: object, file_path: str) -> None:
    """Saves the estimator to the specified file path using joblib.

    :param estimator: The estimator to be saved.
    :param file_path: The file path where the estimator will be saved.
    :return: None
    """
    dump(estimator, file_path) # Save the estimator to the specified file path
    print(f"Model saved to {file_path}")


def load_estimator(file_path: str) -> object:
    """Loads the estimator from the specified file path using joblib.

    :param file_path: The file path where the estimator is saved.
    :return: The loaded estimator.
    """
    return load(file_path)
