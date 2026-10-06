"""
This module contains the functions for training the optimal xgboost model.

functions:
    train_model: Trains the optimal xgboost model on the train data.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from src.preprocessing import add_aggregate_usage_features


def train_model(df: pd.DataFrame, target: str) -> XGBClassifier:
    """Trains the optimal xgboost model on the train data.

    This function loads the train data, adds aggregate usage features,
    defines the model, optimizes the model, and evaluates the model on
    the train data. It returns the best model object.

    :param df: The dataframe containing the train data.
    :param target: The target column name.
    :return: The best model object.
    """
    # load data
    df = add_aggregate_usage_features(df) # add aggregate usage features
    X = df.drop(columns=[target])
    y = df[target]

	# define model
    bst = XGBClassifier(
        n_jobs=-1,
        random_state=42
    )
    pipe = Pipeline(
        steps=[
            ('scaler', StandardScaler()),
            ('bst', bst)
        ]
	)
    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

	# optimize model
    grid = GridSearchCV(
        estimator=pipe,
        param_grid={
            'bst__n_estimators': [10, 50, 100, 300],
            'bst__max_depth': [1, 5, 10],
            'bst__learning_rate': [0.01, 0.1, 0.5],
        },
        scoring='f1',
        cv=kfold,
        n_jobs=-1
	)
    grid.fit(X, y)
    best_params = grid.best_params_
    pipe.set_params(**best_params) # set best parameters

	# evaluate model on train data
    metrics = ["accuracy", "precision", "recall", "f1", "roc_auc"]
    print("Training Scores:\n")
    for metric in metrics:
        cv_scores = cross_val_score(
			estimator=pipe,
			X=X,
			y=y,
			cv=kfold,
			scoring=metric,
			n_jobs=-1
		)
        print(f"{metric}: {cv_scores.mean()} +/- {cv_scores.std()}")

    return pipe.fit(X, y) # return the best model object
