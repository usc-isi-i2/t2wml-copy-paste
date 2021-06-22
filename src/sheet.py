import pandas as pd


class Sheet:

    def __init__(self, dataframe: pd.DataFrame, annotations: dict = None):
        self.dataframe = dataframe
        self.annotations = annotations
