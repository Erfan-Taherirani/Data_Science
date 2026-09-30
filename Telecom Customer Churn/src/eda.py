"""
This module contains the code for exploratory data analysis.

functions:
    load_data: Loads the data from the raw data file.
	validate_data: Validates the data.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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