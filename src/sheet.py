import pandas as pd

from src.anchor import Anchor
from src.annotation import Annotation
from src.selection import Selection
from src.table import Table

ANCHOR = 'anchor'

VALID = 'valid'

X = 'x'
Y = 'y'
CONTENT = 'content'


class Sheet:
    tables = {}

    def __init__(self, name: str, dataframe: pd.DataFrame, annotations: dict = None):
        self.name = name
        self.dataframe = dataframe
        if annotations:
            self.annotations = [Annotation(annotation) for annotation in annotations]

    def find_anchors(self, target):
        anchors = {}
        candidates = self._get_anchors_candidates()

        for y, row in target.dataframe.iterrows():
            for x, value in row.items():
                if isinstance(value, str):
                    for candidate in candidates:
                        if value.lower() == candidate[CONTENT].lower():
                            if anchors.get(value):
                                anchors[value][VALID] = False
                                continue

                            anchors[value] = {
                                ANCHOR: Anchor(value, candidate[X], candidate[Y], x + 1, y + 1),
                                VALID: True
                            }

        return [v[ANCHOR] for k, v in anchors.items() if v[VALID]]

    def _get_anchors_candidates(self):
        candidates = []
        for y, row in self.dataframe.iterrows():
            for x, value in row.items():
                is_annotated = any([a.source_selection.contains(Selection(x + 1, x + 1, y + 1, y + 1)) for a in self.annotations])
                if isinstance(value, str) and not is_annotated:
                    candidates.append({
                        CONTENT: value,
                        X: x + 1,
                        Y: y + 1,
                    })

        return candidates

    def extract_tables(self):
        table_count = 0
        self.tables = {}

        rows = self.dataframe.isnull().all(1)
        row_blocks = self._get_blocks(rows)
        for row_block in row_blocks:
            row_df = self.dataframe[row_block['start']:row_block['end'] + 1]
            columns = row_df.isnull().all()
            column_blocks = self._get_blocks(columns)
            for column_block in column_blocks:
                selection = Selection(column_block['start'] + 1, column_block['end'] + 1, row_block['start'] + 1, row_block['end'] + 1)
                self.tables[f'{self.name}_{str(table_count)}'] = Table(self.name, row_df.iloc[:, column_block['start']:column_block['end'] + 1], selection)
                table_count += 1

        return self.tables

    @staticmethod
    def _get_blocks(series):
        last_index = len(series) - 1
        blocks = []
        block = {}
        for index, is_empty in series.iteritems():
            if not block and not is_empty:
                block['start'] = index

            if block and not is_empty:
                block['end'] = index

            if block and (is_empty or index == last_index):
                blocks.append(block)
                block = {}
        return blocks
