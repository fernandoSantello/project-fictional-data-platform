import pandas as pd
import numpy as np
from decimal import Decimal


def tuple_to_dataframe(data: tuple) -> pd.DataFrame:
    data = pd.DataFrame(list(data))
    return data


def create_multiplied_column(dataframe: pd.DataFrame, new_column: str, multiplied_column: str, value: Decimal) -> pd.DataFrame:
    df = pd.DataFrame()
    df[new_column] = dataframe[multiplied_column] * Decimal(str(value))
    return df


def concatenate_dataframes(dataframes: list) -> dict:
    merged_df = dataframes[0]
    for element in dataframes[1:]: 
        merged_df = pd.concat([merged_df, element], axis=1)
    merged_df = merged_df[['id', 'id_currency', 'rateUSD', 'rateBRL', 'rateEUR', 'timestamp']]
    dictionary = merged_df.to_dict('records')
    return dictionary


def filter_specific_rate(data: dict, currency: str) -> float:
    currency = currency.upper()
    dict_value = np.round(data[currency], 2)
    dict_value = Decimal(str(dict_value))
    return dict_value


def create_rate_column(new_column: str, value: int, rate_table_mysql: dict) -> pd.DataFrame:
    rating_table = tuple_to_dataframe(rate_table_mysql)
    rate_column = create_multiplied_column(dataframe=rating_table, new_column=new_column, multiplied_column='rateUSD', value=value)
    return rate_column
