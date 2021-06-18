import json

import pandas as pd

from src.annotator import Annotator


def test_create_annotations_for_same_sheet():
    source_df = pd.read_excel('../resources/data.xlsx', sheet_name='india_wheat', engine='openpyxl', index_col=None, header=None)
    target_df = pd.read_excel('../resources/data.xlsx', sheet_name='india_wheat', engine='openpyxl', index_col=None, header=None)

    with open('../resources/annotations/india_wheat.json') as f:
        source_annotations = json.load(f)

    annotator = Annotator(source_df, source_annotations)
    annotations = annotator.generate_annotations(target_df)
    assert annotations == source_annotations


def test_create_annotations_for_shifted_sheet():
    source_df = pd.read_excel('../resources/data.xlsx', sheet_name='india_wheat', engine='openpyxl', index_col=None, header=None)
    target_df = pd.read_excel('../resources/data.xlsx', sheet_name='shifted_india_wheat', engine='openpyxl', index_col=None, header=None)

    with open('../resources/annotations/india_wheat.json') as f:
        source_annotations = json.load(f)

    with open('../resources/annotations/shifted_india_wheat.json') as f:
        target_annotations = json.load(f)

    annotator = Annotator(source_df, source_annotations)
    annotations = annotator.generate_annotations(target_df)
    assert annotations == target_annotations