import pandas as pd
from src.selection import Selection


class Table:
    def __init__(self, name: str, df: pd.DataFrame, selection: Selection):
        self.name = name
        self.df = df
        self.selection = selection

    def get_strings(self):
        data = []
        for rowIndex, row in self.df.iterrows():  # iterate over rows
            for columnIndex, value in row.items():
                if isinstance(value, str):
                    data.append(value)

        return data
