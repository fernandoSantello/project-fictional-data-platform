import pandas as pd
import numpy as np

def tuple_to_dataframe(data: tuple) -> pd.DataFrame:
    data = pd.DataFrame(list(data))
    return data

def create_multiplied_column(dataframe: pd.DataFrame, new_column: str, multiplied_column: str, value: float) -> pd.DataFrame:
    df = pd.DataFrame()
    df[new_column] = np.round(dataframe[multiplied_column] * value, 2)
    return df

def concatenate_dataframes(dataframes: list) -> pd.DataFrame:
    merged_df = dataframes[0]
    merged_df = pd.concat(dataframes, axis=1)
    return merged_df
