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
