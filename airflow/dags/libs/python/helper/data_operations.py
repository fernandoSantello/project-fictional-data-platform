import pandas as pd
import numpy as np
from decimal import Decimal, getcontext


def tuple_to_dataframe(data: tuple) -> pd.DataFrame:
    data = pd.DataFrame(list(data))
    return data


def create_multiplied_column(dataframe: pd.DataFrame, new_column: str, multiplied_column: str, value: float) -> pd.DataFrame:
    df = pd.DataFrame()
    df[new_column] = np.round(dataframe[multiplied_column] * value, 2)
    return df


def concatenate_dataframes(dataframes: list) -> pd.DataFrame:
    merged_df = dataframes[0]
    for element in dataframes[1:]: 
        merged_df = pd.concat([merged_df, element], axis=1)
    merged_df = merged_df[['id', 'id_currency', 'rateUSD', 'rateBRL', 'rateEUR', 'timestamp']]
    return merged_df


def filter_specific_rate(data: dict, currency: str):
    currency = currency.upper()
    dict_value = np.round(data[currency], 2)
    return dict_value
