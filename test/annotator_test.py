import json

import pandas as pd
from mip import OptimizationStatus

from src.sheet import Sheet
from src.annotator import Annotator


def test_create_annotations_for_same_sheet():
    source_df = pd.read_excel('../resources/data.xlsx', sheet_name='india_wheat', engine='openpyxl', index_col=None, header=None)
    target_df = pd.read_excel('../resources/data.xlsx', sheet_name='india_wheat', engine='openpyxl', index_col=None, header=None)

    with open('../resources/annotations/india_wheat.json') as f:
        source_annotations = json.load(f)

    with open('../resources/annotations/expected_india_wheat.json') as f:
        expected_target_annotations = json.load(f)

    source = Sheet('source', source_df, source_annotations)
    annotator = Annotator(source)

    target = Sheet('target', target_df)
    annotations, status = annotator.generate_annotations(target)

    assert status == OptimizationStatus.OPTIMAL
    assert annotations == expected_target_annotations


def test_create_annotations_for_shifted_sheet():
    source_df = pd.read_excel('../resources/data.xlsx', sheet_name='india_wheat', engine='openpyxl', index_col=None, header=None)
    target_df = pd.read_excel('../resources/data.xlsx', sheet_name='shifted_india_wheat', engine='openpyxl', index_col=None, header=None)

    with open('../resources/annotations/india_wheat.json') as f:
        source_annotations = json.load(f)

    source = Sheet('source', source_df, source_annotations)
    target = Sheet('target', target_df)

    annotator = Annotator(source)

    with open('../resources/annotations/expected_shifted_india_wheat.json') as f:
        target_annotations = json.load(f)

    annotations, status = annotator.generate_annotations(target)
    assert status == OptimizationStatus.OPTIMAL
    assert annotations == target_annotations


def test_create_annotations_for_shifted_sheet_without_anchors():
    source_df = pd.read_excel('../resources/data.xlsx', sheet_name='india_wheat', engine='openpyxl', index_col=None, header=None)
    target_df = pd.read_excel('../resources/data.xlsx', sheet_name='shifted_india_wheat_wo_anchors', engine='openpyxl', index_col=None, header=None)

    with open('../resources/annotations/india_wheat.json') as f:
        source_annotations = json.load(f)

    source = Sheet('source', source_df, source_annotations)
    target = Sheet('target', target_df)

    annotator = Annotator(source)

    with open('../resources/annotations/expected_shifted_india_wheat.json') as f:
        target_annotations = json.load(f)

    annotations, status = annotator.generate_annotations(target)
    assert status == OptimizationStatus.OPTIMAL
    assert annotations == target_annotations


def test_create_annotations_for_shifted_e1():
    source_df = pd.read_excel('../resources/data.xlsx', sheet_name='e1', engine='openpyxl', index_col=None, header=None)
    target_df = pd.read_excel('../resources/data.xlsx', sheet_name='e1_shifted', engine='openpyxl', index_col=None, header=None)

    with open('../resources/annotations/e1.json') as f:
        source_annotations = json.load(f)

    source = Sheet('source', source_df, source_annotations)
    target = Sheet('target', target_df)

    annotator = Annotator(source)

    with open('../resources/annotations/e1_shifted.json') as f:
        target_annotations = json.load(f)

    annotations, status = annotator.generate_annotations(target)
    assert status == OptimizationStatus.OPTIMAL
    assert annotations == target_annotations


def test_create_annotations_for_shifted_e2():
    source_df = pd.read_excel('../resources/data.xlsx', sheet_name='e2', engine='openpyxl', index_col=None, header=None)
    target_df = pd.read_excel('../resources/data.xlsx', sheet_name='e2_shifted', engine='openpyxl', index_col=None, header=None)

    with open('../resources/annotations/e2.json') as f:
        source_annotations = json.load(f)

    source = Sheet('source', source_df, source_annotations)
    target = Sheet('target', target_df)

    annotator = Annotator(source)

    with open('../resources/annotations/e2_shifted.json') as f:
        target_annotations = json.load(f)

    annotations, status = annotator.generate_annotations(target)
    assert status == OptimizationStatus.OPTIMAL
    assert annotations == target_annotations
