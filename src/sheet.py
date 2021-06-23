import pandas as pd

from src.anchor import Anchor
from src.annotation import Annotation

ANCHOR = 'anchor'

VALID = 'valid'

X = 'x'
Y = 'y'
CONTENT = 'content'


class Sheet:

    def __init__(self, dataframe: pd.DataFrame, annotations: dict = None):
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
                                ANCHOR: Anchor(value, candidate[X], candidate[Y], x, y),
                                VALID: True
                            }

        return [v[ANCHOR] for k, v in anchors.items() if v[VALID]]

    def _get_anchors_candidates(self):
        candidates = []
        for y, row in self.dataframe.iterrows():
            for x, value in row.items():
                is_annotated = any([a.selection.contains(x + 1, y + 1) for a in self.annotations])
                if isinstance(value, str) and not is_annotated:
                    candidates.append({
                        CONTENT: value,
                        X: x + 1,
                        Y: y + 1,
                    })

        return candidates
