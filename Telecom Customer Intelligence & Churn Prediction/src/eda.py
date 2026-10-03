"""
This module contains the code for exploratory data analysis.

functions:
    load_data: Loads the data from the raw data file.
	validate_data: Validates the data.
	get_categorical_and_numerical_features: Get categorical and numerical features from DataFrame
	get_minutes_stats: Get minute stats
	get_call_stats: Get call stats
	get_charge_stats: Get charge stats
	get_divided_data: Divides the data into different groups based on the value of the column specified.
	get_churn_rate: Calculates the churn rate for each group of data based on the number of customer service calls.
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from utils.eda import describe_stats


def load_data(
		file_path: str = "../data/raw/churn-bigml-80.csv"
) -> pd.DataFrame:
	""" Loads the data from the raw data file.
	
	:param file_path: The path to the file containing the data.
	:return: A pandas dataframe containing the data.
	"""
	df = pd.read_csv(file_path)
	df.rename(columns={
		"State": "state",
		"Account length": "account_length",
		"Area code": "area_code",
		"International plan": "international_plan",
		"Voice mail plan": "voice_mail_plan",
		"Number vmail messages": "number_vmail_messages",
		"Total day minutes": "total_day_minutes",
		"Total day calls": "total_day_calls",
		"Total day charge": "total_day_charge",
		"Total eve minutes": "total_eve_minutes",
		"Total eve calls": "total_eve_calls",
		"Total eve charge": "total_eve_charge",
		"Total night minutes": "total_night_minutes",
		"Total night calls": "total_night_calls",
		"Total night charge": "total_night_charge",
		"Total intl minutes": "total_intl_minutes",
		"Total intl calls": "total_intl_calls",
		"Total intl charge": "total_intl_charge",
		"Customer service calls": "customer_service_calls",
		"Churn": "churn"
	},
	inplace=True
	)
	
	# fix data quality issues
	df['state'] = df['state'].str.upper()
	df['international_plan'] = df['international_plan'].str.lower()
	df['voice_mail_plan'] = df['voice_mail_plan'].str.lower()

	# fix data type issues
	df['state'] = df['state'].astype('category')
	df['area_code'] = df['area_code'].astype('category')
	df['international_plan'] = df['international_plan'].astype('category')
	df['voice_mail_plan'] = df['voice_mail_plan'].astype('category')
	
	return df


def validate_data(df: pd.DataFrame) -> str:
	"""	Validates the data.	

	:param df: Dataframe containing the data
	:return: A string containing the validation result
	"""
	# data validation
	assert len(
		df['state'].unique()
	) == len(
		df['state'].str.upper().unique()
	), "State column has duplicate values"

	assert (df['account_length'] < 0).sum() == 0, "Account length column has negative values"

	assert len(df['area_code'].unique()) == 3, "Invalid area code inserted"

	assert len(df['international_plan'].unique()) == 2, "Should be a binary value"
	assert len(df['voice_mail_plan'].unique()) == 2, "Should be a binary value"

	assert sum(df['number_vmail_messages'] < 0) == 0, "Number of vmail messages should be positive"
	assert sum(df['total_day_minutes'] < 0) == 0, "Total day minutes should be positive"
	assert sum(df['total_day_calls'] < 0) == 0, "Total day calls should be positive"
	assert sum(df['total_day_charge'] < 0) == 0, "Total day charge should be positive"
	assert sum(df['total_eve_minutes'] < 0) == 0, "Total eve minutes should be positive"
	assert sum(df['total_eve_calls'] < 0) == 0, "Total eve calls should be positive"
	assert sum(df['total_eve_charge'] < 0) == 0, "Total eve charge should be positive"
	assert sum(df['total_night_minutes'] < 0) == 0, "Total night minutes should be positive"
	assert sum(df['total_night_calls'] < 0) == 0, "Total night calls should be positive"
	assert sum(df['total_night_charge'] < 0) == 0, "Total night charge should be positive"
	assert sum(df['total_intl_minutes'] < 0) == 0, "Total intl minutes should be positive"
	assert sum(df['total_intl_calls'] < 0) == 0, "Total intl calls should be positive"
	assert sum(df['total_intl_charge'] < 0) == 0, "Total intl charge should be positive"
	assert sum(df['customer_service_calls'] < 0) == 0, "Customer service calls should be positive"
	
	return "Data is valid"


def get_categorical_and_numerical_features(df: pd.DataFrame) -> tuple[list[str], list[str]]:
	"""Get categorical and numerical features from DataFrame

	:param df: DataFrame
	:return: categorical_features, numerical_features
	"""
	categorical_features = [
		"state", "area_code", "international_plan", "voice_mail_plan", "churn"
	]

	numerical_features = []
	for feature in df.columns:
		if feature not in categorical_features:
			numerical_features.append(feature)

	return categorical_features, numerical_features


def get_minutes_stats(df: pd.DataFrame) -> pd.DataFrame:
	""" Get minute stats

	:param df: Dataframe containing the data
	:return: A dataframe containing minute stats
	"""
	minutes_df = describe_stats(df, "total_day_minutes").rename(columns={"Value": "total_day_minutes"})
	minutes_df['total_eve_minutes'] = describe_stats(df, "total_eve_minutes")
	minutes_df['total_night_minutes'] = describe_stats(df, "total_night_minutes")
	minutes_df['total_intl_minutes'] = describe_stats(df, "total_intl_minutes")

	return minutes_df


def get_call_stats(df: pd.DataFrame) -> pd.DataFrame:
	""" Get call stats

	:param df: Dataframe containing the data
	:return: A dataframe containing call stats
	"""
	minutes_df = describe_stats(df, "total_day_calls").rename(columns={"Value": "total_day_calls"})
	minutes_df['total_eve_calls'] = describe_stats(df, "total_eve_calls")
	minutes_df['total_night_calls'] = describe_stats(df, "total_night_calls")
	minutes_df['total_intl_calls'] = describe_stats(df, "total_intl_calls")

	return minutes_df


def get_charge_stats(df: pd.DataFrame) -> pd.DataFrame:
	""" Get charge stats

	:param df: Dataframe containing the data
	:return: A dataframe containing charge stats
	"""
	minutes_df = describe_stats(df, "total_day_charge").rename(columns={"Value": "total_day_charge"})
	minutes_df['total_eve_charge'] = describe_stats(df, "total_eve_charge")
	minutes_df['total_night_charge'] = describe_stats(df, "total_night_charge")
	minutes_df['total_intl_charge'] = describe_stats(df, "total_intl_charge")

	return minutes_df


def get_divided_data(df: pd.DataFrame, based_on: str) -> dict:
	"""
	Divides the data into different groups based on the value of the column
	specified in the 'based_on' parameter.

	:param df: The DataFrame to be divided.
	:param based_on: The column name to be used as the basis for the division.
	:return: A dictionary where the keys are the unique values of the
			 column specifiedin the 'based_on' parameter and the values
			 are the DataFrames that correspond to each unique value.
	"""
	divided_data = {}
	unique_values = df[based_on].unique()
	for value in unique_values:
		divided_data[value] = df.loc[df[based_on] == value] # Create a new DataFrame for each unique value

	return divided_data


def get_churn_rate(divided_data: dict) -> dict:
	"""
	Calculates the churn rate for each group of data based on the number of customer service calls.

	:param divided_data: A dictionary where the keys are the unique values of the column specified
						 in the 'based_on' parameter and the values are the DataFrames that correspond
						 to each unique value.
	:return: A dictionary where the keys are the unique values of the column specified
			 in the 'based_on' parameter and the values are the churn rates for each group.
	"""
	churn_rates = {}
	for value, df in divided_data.items():
		if len(df['churn'].value_counts().values) == 2:
			churn_rate = df['churn'].value_counts().values[1] / df.shape[0] * 100 # Get the churn rate for the group
			churn_rates[value] = round(churn_rate, 2)
		else:
			churn_rate = 100
			churn_rates[value] = churn_rate

	return churn_rates


def get_churned_customers(df: pd.DataFrame) -> pd.DataFrame:
	""" Get churned customers

	:param df: Dataframe containing the data
	:return: A dataframe containing churned customers
	"""
	df = df.loc[df['churn'] == True]
	return df


def get_stayed_customers(df: pd.DataFrame) -> pd.DataFrame:
	""" Get stayed customers

	:param df: Dataframe containing the data
	:return: A dataframe containing stayed customers
	"""
	df = df.loc[df['churn'] == False]
	return df


def describe_total_day_minutes(df: pd.DataFrame) -> pd.DataFrame:
	""" Describe total day minutes

	:param df: Dataframe containing the data
	:return: A dataframe containing total day minutes
	"""
	df_stats = describe_stats(get_churned_customers(df), "total_day_minutes").rename(
		columns={"Value": "total_day_minutes_churned"}
	)
	df_stats['total_day_minutes_stayed'] = describe_stats(
		get_stayed_customers(df), "total_day_minutes"
	)

	return df_stats


def describe_international_calls(df: pd.DataFrame) -> pd.DataFrame:
	""" Describe international calls

	:param df: Dataframe containing the data
	:return: A dataframe containing international calls
	"""
	df_intl = describe_stats(get_churned_customers(df), "total_intl_minutes").rename(
		columns={"Value": "Total International Minutes Churned"}
	)
	df_intl['Total International Minutes Not Churned'] = describe_stats(get_stayed_customers(df), "total_intl_minutes")
	return df_intl


def get_account_length_info(df: pd.DataFrame) -> None:
	""" Get account length info by churn status

	:param df: DataFrame
	:return: None
	"""
	df_churned = get_churned_customers(df)['account_length']
	df_not_churned = get_stayed_customers(df)['account_length']

	mean_churned = df_churned.mean()
	std_churned = df_churned.std()
	mean_not_churned = df_not_churned.mean()
	std_not_churned = df_not_churned.std()
	
	print(f"Account length for churned customers: {mean_churned:.2f} +/- {std_churned:.2f}")
	print(f"Account length for stayed customers: {mean_not_churned:.2f} +/- {std_not_churned:.2f}")
