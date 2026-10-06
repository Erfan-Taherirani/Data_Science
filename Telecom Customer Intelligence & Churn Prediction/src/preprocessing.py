"""
This module contains functions for preprocessing the data.

functions:
    save_processed_data: Saves the processed data as a csv file.
    add_aggregate_usage_features: Adds aggregate usage features to the dataframe.
    add_usage_share_features: Adds usage share features to the dataframe.
    add_usage_composition_share_features: Adds usage composition share features to the dataframe.
    add_customer_service_and_interaction_features: Adds customer service and interaction features to the dataframe.
    get_df_engineered: Engineers the dataframe by adding features.
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.eda import load_data


def save_processed_data():
	"""
	This function preprocessed the training dataset and save it 
	as csv file in the data folder.
	"""
	df = load_data()

	# drop non-informative columns
	df = df.drop(columns=["state"])
	df['area_code'] = df['area_code'].cat.codes
	df['international_plan'] = df['international_plan'].cat.codes
	df['voice_mail_plan'] = df['voice_mail_plan'].cat.codes

	df.to_csv("../data/processed/df_processed.csv", index=False)

def save_test_processed_data():
	"""
	This function preprocessed the test dataset and save it 
	as csv file in the data folder.
	"""
	df = load_data("../data/raw/churn-bigml-20.csv")
    
    # drop non-informative columns
	df = df.drop(columns=["state"])
	df['area_code'] = df['area_code'].cat.codes
	df['international_plan'] = df['international_plan'].cat.codes
	df['voice_mail_plan'] = df['voice_mail_plan'].cat.codes

    # save test data
	df.to_csv("../data/processed/df_test_processed.csv", index=False)


def add_aggregate_usage_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function adds aggregate usage features to the dataframe.

    :param df: Dataframe containing the original data.
    :return: Dataframe with aggregate usage features.
    """
    df = df.copy()

    df['total_minutes'] = (
		df['total_day_minutes'] + df['total_eve_minutes']
		+ df['total_night_minutes'] + df['total_intl_minutes']
	)
    df['total_calls'] = (
		df['total_day_calls'] + df['total_eve_calls']
		+ df['total_night_calls'] + df['total_intl_calls']
	)
    df['total_charge'] = (
		df['total_day_charge'] + df['total_eve_charge']
		+ df['total_night_charge'] + df['total_intl_charge']
	)

    return df


def add_usage_share_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function adds usage share features to the dataframe.

    :param df: Dataframe containing the original data.
    :return: Dataframe with usage share features.
    """ 
    df = df.copy()

    df['avg_day_minutes_per_call'] = (
		df['total_day_minutes'] / df['total_day_calls']
	)
    df['avg_day_minutes_per_call'] = df['avg_day_minutes_per_call'].fillna(0)

    df['avg_eve_minutes_per_call'] = (
		df['total_eve_minutes'] / df['total_eve_calls']
	)
    df['avg_eve_minutes_per_call'] = df['avg_eve_minutes_per_call'].fillna(0)

    df['avg_night_minutes_per_call'] = (
		df['total_night_minutes'] / df['total_night_calls']
	)
    df['avg_night_minutes_per_call'] = df['avg_night_minutes_per_call'].fillna(0)

    df['avg_intl_minutes_per_call'] = (
		df['total_intl_minutes'] / df['total_intl_calls']
    )
    df['avg_intl_minutes_per_call'] = df['avg_intl_minutes_per_call'].fillna(0)

    return df


def add_usage_composition_share_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function adds usage composition share features to the dataframe.

    :param df: Dataframe containing the original data.
    :return: Dataframe with usage composition share features.
    """
    df = df.copy()

    df['day_minutes_share'] = (
        df['total_day_minutes'] / df['total_minutes']
	)
    df['eve_minutes_share'] = (
        df['total_eve_minutes'] / df['total_minutes']
	)
    df['night_minutes_share'] = (
        df['total_night_minutes'] / df['total_minutes']
	)
    df['intl_minutes_share'] = (
        df['total_intl_minutes'] / df['total_minutes']
	)

    return df


def add_customer_service_and_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function adds customer service and interaction features to the dataframe.

    :param df: Dataframe containing the original data.
    :return: Dataframe with customer service and interaction features.
    """
    df = df.copy()

    # make binary feature for high service calls
    df['high_service_calls'] = (
        df['customer_service_calls'] > 4
	)

	# interaction features
    df['international_plan_service_risk'] = (
        (df['international_plan'] == 1) &
        (df['customer_service_calls'] > 4)
	)
    df['high_usage_service_risk'] = (
        (df['total_day_minutes'] > df['total_day_minutes'].mean()) &
        (df['customer_service_calls'] > 4)
	)
    df['intl_plan_no_vmail'] = (
        (df['international_plan'] == 1) &
        (df['voice_mail_plan'] == 0)
	)

    return df


def get_df_engineered(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function engineers the dataframe by adding features.

    :param df: Dataframe containing the original data.
    :return: Dataframe with engineered features.
    """
    df = df.copy()

    # aggregate usage features
    df = add_aggregate_usage_features(df)

	# call intensity features
    df = add_usage_share_features(df)

	# usage composition / share features
    df = add_usage_composition_share_features(df)

	# customer service and interaction features
    df = add_customer_service_and_interaction_features(df)

	# charge-efficiency features
    df['day_charge_per_minute'] = (
        df['total_day_charge'] / df['total_day_minutes']
	)
    df['day_charge_per_minute'] = df['day_charge_per_minute'].fillna(0)

    df['eve_charge_per_minute'] = (
        df['total_eve_charge'] / df['total_eve_minutes']
	)
    df['eve_charge_per_minute'] = df['eve_charge_per_minute'].fillna(0)

    df['night_charge_per_minute'] = (
        df['total_night_charge'] / df['total_night_minutes']
	)
    df['night_charge_per_minute'] = df['night_charge_per_minute'].fillna(0)

    df['intl_charge_per_minute'] = (
        df['total_intl_charge'] / df['total_intl_minutes']
	)
    df['intl_charge_per_minute'] = df['intl_charge_per_minute'].fillna(0)

	# voicemail utilization features
    df['has_vmail_usage'] = (
        df['number_vmail_messages'] > 0
	)
    df['vmail_plan_unused '] = (
        (df['voice_mail_plan'] == 0) &
        (df['number_vmail_messages'] == 0)
	)

    # account-length trasformations
    df['new_customer'] = (
        (df['account_length'] < 30)
    )
    df['long_tenure'] = (
        (df['account_length'] >= 30)
	)

    return df


def save_complete_data(
    file_path: str = "../data/processed/complete_data.csv"
) -> str:
    """This function saves the complete data as a csv file.

    :param file_path: The path where the data will be saved.
    :return: A string indicating the success of the operation.
    """
    # Reading the data
    df = load_data("../data/raw/churn-bigml-80.csv")

    df['customer_key'] = [key for key in range(1, len(df)+1)] # Creating a new column with customer keys

    df.to_csv(file_path, index=False) # Saving the dataframe

    return "Data saved successfully"
