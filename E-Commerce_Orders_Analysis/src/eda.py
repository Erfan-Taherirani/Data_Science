import pandas as pd


def fix_data_types(df: pd.DataFrame) -> str:
	"""This function handles the data types of the dataframe.

    :param df: The dataframe to be fixed.
    :return: A string indicating the data types fixed.
    """
    # handle datetime data types
	df['order_date'] = pd.to_datetime(df['order_date'], format="mixed")
	df['ship_date'] = pd.to_datetime(df['ship_date'], format="mixed")
	df['delivery_date'] = pd.to_datetime(df['delivery_date'], format="mixed")

	# normalizing text data and handling categorical data types
	df['customer_name'] = df['customer_name'].str.strip().str.lower()
	df['customer_segment'] = df['customer_segment'].str.lower().astype("category")
	df['customer_country'] = df['customer_country'].replace(
		{"USA": "United States"}
	).str.lower().astype("category")
	df['customer_city'] = df['customer_city'].str.lower().astype("category")
	df['customer_city'] = df['customer_city'].cat.add_categories(['unknown']) # add unknown category for missing values
	df['customer_region'] = df['customer_region'].str.lower().astype("category")
	df['order_status'] = df['order_status'].str.lower().astype("category")
	df['shipping_method'] = df['shipping_method'].str.lower().astype("category")
	df['delivery_status'] = df['delivery_status'].str.lower().astype("category")
	df['payment_method'] = df['payment_method'].str.lower().astype("category")
	df['payment_status'] = df['payment_status'].str.lower().astype("category")
	df['sales_channel'] = df['sales_channel'].str.lower().astype("category")
	df['customer_acquisition_channel'] = df['customer_acquisition_channel'].str.lower().astype("category")
	df['campaign'] = df['campaign'].str.lower().astype("category")

	return "data types fixed"


def fix_customer_country(df: pd.DataFrame) -> str:
	"""This function handles the missing values in the customer_country column.

    :param df: The dataframe to be fixed.
    :return: A string indicating the missing values fixed.
    """
	north_america_region = []
	europe_region = []
	oceania_region = []
	for sample in enumerate(df.loc[:, ['customer_country', 'customer_region']].values):
		if sample[1][0] in ["united states", "canada"]:
			north_america_region.append(sample[0])
		elif sample[1][0] in ["united kingdom", "germany"]:
			europe_region.append(sample[0])
		else:
			oceania_region.append(sample[0])

	df.loc[north_america_region, 'customer_region'] = "north america"
	df.loc[europe_region, 'customer_region'] = "europe"
	df.loc[oceania_region, 'customer_region'] = "oceania"
	return "customer_country column missing values fixed"


def fix_negative_shipping_costs(df: pd.DataFrame) -> str:
	"""This function handles the negative values in the shipping_cost column.

    :param df: The dataframe to be fixed.
    :return: A string indicating the negative values fixed.
    """
	correct_values = df.loc[df['shipping_cost'] < 0, "shipping_cost"] * -1
	negative_shipping_cost_indicies = df.loc[df['shipping_cost'] < 0, "shipping_cost"].index

	df.loc[negative_shipping_cost_indicies, 'shipping_cost'] = correct_values
	return "shipping_cost negative values fixed"


def fix_missing_discounts(
		df: pd.DataFrame, missing_discount_indicies: pd.Index
) -> str:
    """This function handles the missing values in the discount_amount column.

    :param df: The dataframe to be fixed.
    :param missing_discount_indicies: The indicies of the missing discount values.
    :return: A string indicating the missing values fixed.
    """
    subtotal = df.loc[missing_discount_indicies, 'subtotal']
    shipping = df.loc[missing_discount_indicies, 'shipping_cost']
    tax = df.loc[missing_discount_indicies, 'tax_amount']
    total = df.loc[missing_discount_indicies, 'total_order_value']
    
    discount = subtotal + shipping + tax - total 
    discount = discount.apply(lambda x: 0 if x < 0.01 else x) 
    df.loc[missing_discount_indicies, 'discount_amount'] = discount
    
    return "dicount_amount unambiguous samples fixed"


def fix_missing_shipping_costs(
		df: pd.DataFrame, missing_shipping_cost_indicies: pd.Index
) -> str:
    """_summary_

    :param df: The dataframe to be fixed.
    :param missing_shipping_cost_indicies: The indicies of the missing shipping cost values.
    :return: A string indicating the missing values fixed.
    """
    subtotal = df.loc[missing_shipping_cost_indicies, 'subtotal']
    discount = df.loc[missing_shipping_cost_indicies, 'discount_amount']
    tax = df.loc[missing_shipping_cost_indicies, 'tax_amount']
    total = df.loc[missing_shipping_cost_indicies, 'total_order_value']
    
    shipping = total - subtotal + discount - tax
    shipping = shipping.apply(lambda x: 0 if x < 0.01 else x)
    df.loc[missing_shipping_cost_indicies, 'shipping_cost'] = shipping
    
    return "shipping_cost unambiguous samples fixed"


def validate_columns(df: pd.DataFrame) -> str:
	"""This function validates columns of the dataset.

	:param df: The dataframe to be validated.
	:return: A string indicating the validation status.
	"""
	# check the uniqueness of the order_id
	assert df['order_id'].nunique() == df.shape[0], "duplicate order_ids"

	# check if the dates are not in the future
	assert all(df['order_date'].dt.year.value_counts().index.to_numpy() < 2027) == True, "future order_date"
	assert all(df['ship_date'].dt.year.value_counts().index.to_numpy() < 2027) == True, "future ship_date"
	assert all(df['delivery_date'].dt.year.value_counts().index.to_numpy() < 2027) == True, "future delivery_date"

	# check the validity of numeric columns
	assert (df['total_items'] < 0).sum() == 0, "total_items contains negative values"
	assert (df['unique_products'] < 0).sum() == 0, "unique_products contains negative values"
	assert (df['subtotal'] < 0).sum() == 0, "subtotal contains negative values"
	assert (df['discount_amount'] < 0).sum() == 0, "discount_amount contains negative values"
	assert (df['discount_amount'] > df['subtotal']).sum() == 0, "discount_amount greater than subtotal"
	assert (df['shipping_cost'] < 0).sum() == 0, "shipping_cost contains negative values"
	assert (df['tax_amount'] < 0).sum() == 0, "tax_amount contains negative values"
	assert (df['total_order_value'] < 0).sum() == 0, "total_order_value contains negative values"
	assert (df['profit'] > df['total_order_value']).sum() == 0, "profit contains negative values"

	# check no missing values
	columns_with_no_missing_values = [
		'order_id', 'customer_id', 'order_date', 'customer_name',
		'customer_segment', 'customer_country', 'customer_city',
		'customer_region', 'order_status', 'total_items',
		'unique_products', 'subtotal', 'discount_amount', 'shipping_cost',
		'tax_amount', 'total_order_value', 'profit', 'shipping_method',
		'payment_status', 'sales_channel', 'customer_acquisition_channel',
		'delivery_status', 'payment_method'
	]
	for column in columns_with_no_missing_values:
		assert df[column].isnull().sum() == 0, f"{column} contains missing values"

	return "Columns Validated Successfully"
