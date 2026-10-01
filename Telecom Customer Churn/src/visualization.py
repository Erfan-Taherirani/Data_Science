"""
This module contains the code for visualization.

functions:
    plot_states: Plot the state counts
    plot_call_minutes: Plot the distribution of call minutes for different time of the day.
    plot_call_counts: Plot the distribution of call counts for different time of the day and international calls.
    plot_charge_distributions: Plot the distribution of charge for different time of the day and international calls.
    plot_correlation: Plot the correlation matrix
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.eda import get_divided_data, get_churn_rate


def plot_states(df: pd.DataFrame) -> None:
    """ Plot the state counts

    :param df: DataFrame
    :return: None
    """
    # plot the state counts
    states_sorted = pd.DataFrame(df['state'].value_counts().sort_values(ascending=False)).reset_index()

    _, ax = plt.subplots(figsize=(8, 10))

    sns.barplot(
		data=states_sorted,
		y='state',
		x='count',
		ax=ax
	)
    ax.set_title('State Counts')
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    plt.show()


def plot_call_minutes(df):
	"""
	Plot the distribution of call minutes for different time of the day.
	"""
	_, axes = plt.subplots(2, 2, figsize=(10, 10))

	sns.histplot(
		data=df,
		x="total_day_minutes",
		ax=axes[0, 0],
	)
	sns.histplot(
		data=df,
		x="total_eve_minutes",
		ax=axes[0, 1],
	)
	sns.histplot(
		data=df,
		x="total_night_minutes",
		ax=axes[1, 0],
	)
	sns.histplot(
		data=df,
		x="total_intl_minutes",
		ax=axes[1, 1],
	)

	axes[0, 0].set_title("Daily minutes")
	axes[0, 1].set_title("Evening minutes")
	axes[1, 0].set_title("Night minutes")
	axes[1, 1].set_title("International minutes")
	axes[0, 0].set_xlabel("Minutes")
	axes[0, 1].set_xlabel("Minutes")
	axes[1, 0].set_xlabel("Minutes")
	axes[1, 1].set_xlabel("Minutes")

	plt.tight_layout()
	plt.show()


def plot_call_counts(df):
	"""
	Plot the distribution of call counts for different time of the day and international calls.
	"""
	_, axes = plt.subplots(2, 2, figsize=(10, 10))

	sns.histplot(
		data=df,
		x="total_day_calls",
		ax=axes[0, 0],
	)
	sns.histplot(
		data=df,
		x="total_eve_calls",
		ax=axes[0, 1],
	)
	sns.histplot(
		data=df,
		x="total_night_calls",
		ax=axes[1, 0],
	)
	sns.histplot(
		data=df,
		x="total_intl_calls",
		ax=axes[1, 1],
		bins=20,
	)

	axes[0, 0].set_title("Day calls")
	axes[0, 1].set_title("Evening calls")
	axes[1, 0].set_title("Night calls")
	axes[1, 1].set_title("International calls")
	axes[0, 0].set_xlabel("calls")
	axes[0, 1].set_xlabel("calls")
	axes[1, 0].set_xlabel("calls")
	axes[1, 1].set_xlabel("calls")

	plt.tight_layout()
	plt.show()


def plot_charge_distributions(df):
	"""
	Plot the distribution of charge for different time of the day and international calls.
	"""
	_, axes = plt.subplots(2, 2, figsize=(10, 10))

	sns.histplot(
		data=df,
		x="total_day_charge",
		ax=axes[0, 0],
	)
	sns.histplot(
		data=df,
		x="total_eve_charge",
		ax=axes[0, 1],
	)
	sns.histplot(
		data=df,
		x="total_night_charge",
		ax=axes[1, 0],
	)
	sns.histplot(
		data=df,
		x="total_intl_charge",
		ax=axes[1, 1]
	)

	axes[0, 0].set_title("Day charge")
	axes[0, 1].set_title("Evening charge")
	axes[1, 0].set_title("Night charge")
	axes[1, 1].set_title("International charge")
	axes[0, 0].set_xlabel("charge")
	axes[0, 1].set_xlabel("charge")
	axes[1, 0].set_xlabel("charge")
	axes[1, 1].set_xlabel("charge")

	plt.tight_layout()
	plt.show()


def plot_correlation(df: pd.DataFrame) -> None:
	""" Plot the correlation matrix

	:param df: DataFrame
	:return: None
	"""
	df = df.drop(columns=["state", "area_code"])
	df['international_plan'] = df['international_plan'].cat.codes
	df['voice_mail_plan'] = df['voice_mail_plan'].cat.codes

	_, ax = plt.subplots(figsize=(12, 12))
	sns.heatmap(
		data=abs(df.corr()),
		annot=True,
		fmt=".2f",
		cmap="Blues",
		ax=ax,
	)

	ax.set_title("Correlation Matrix")
	plt.show()


def plot_churn_rate_by_customer_service_calls(df: pd.DataFrame) -> None:
	""" Plot the churn rate by customer service calls

	:param df: DataFrame
	:return: None
	"""
	def get_cutomer_service_calls_churn_rate(df):
		churn_rates = []
		for n_service_calls in range(10):
			df_new = df.loc[df['customer_service_calls'] == n_service_calls, 'churn']
			churn_rate = (df_new.value_counts() / df_new.shape[0] * 100).values
			if len(churn_rate) == 2:
				churn_rate = churn_rate[1]
				churn_rates.append(round(churn_rate, 2))
			elif len(churn_rate) == 1:
					churn_rates.append(churn_rate[0])

		return churn_rates

	churn_rates = get_cutomer_service_calls_churn_rate(df)
	sns.lineplot(
		y=churn_rates,
		x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
		marker='o',
		markersize=8,
		linestyle='-',
		label='Churn Rate'
	)
	plt.title('Churn Rates by Customer Service Calls')
	plt.xlabel('Number of Customer Service Calls')
	plt.ylabel('Churn Rate')
	plt.grid(True, linestyle='-', alpha=0.5)
	plt.legend()
	plt.show()


def plot_state_churn_rates(df: pd.DataFrame) -> None:
	""" Plot the churn rate by state

	:param df: DataFrame
	:return: None
	"""
	def get_state_churn_rate(df):
		state_divided_data = get_divided_data(df, "state")
		state_churn_rates = get_churn_rate(state_divided_data)
		values = []
		churn_rates = []
		
		for value, churn_rate in state_churn_rates.items():
			values.append(value)
			churn_rates.append(churn_rate)
			# print(f"State: {value}, Churn rate: {churn_rate}%")

		return values, churn_rates

	values, churn_rates = get_state_churn_rate(df)

	_, ax = plt.subplots(figsize=(8, 10))

	sns.barplot(y=values, x=churn_rates)

	plt.axvline(x=25, color='red', linestyle='--')
	plt.axvline(x=15, color='red', linestyle='--')
	plt.text(
		x=20, y=18, s="Critical Threshold", ha='center', va="center",
		color='red', fontsize=12
	)
	sns.barplot(
		y=["NJ", "TX"],
		x=[churn_rates[2], churn_rates[14]],
		color="darkorange",
	)

	ax.set_title("State Churn Rates")
	ax.set_xlabel("Churn Rate (%)")
	ax.set_ylabel("State")
	ax.grid(True, axis='x', linestyle='--', color='grey', alpha=0.5)
	plt.show()
