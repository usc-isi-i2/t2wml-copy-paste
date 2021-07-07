import json

import pandas as pd
from mip import OptimizationStatus


from src.sheet import Sheet
from src.annotator import Annotator

test_cases = [
    {'source_sheet': 'e1', 'target_sheet': 'e1_shifted', 'source_annotation': 'source_e1.json', 'target_annotation': 'expected_e1_shifted.json'},
    {'source_sheet': 'e2', 'target_sheet': 'e2_shifted', 'source_annotation': 'source_e2.json', 'target_annotation': 'expected_e2_shifted.json'},
    {'source_sheet': 'e3', 'target_sheet': 'e3_shifted', 'source_annotation': 'source_e3.json', 'target_annotation': 'expected_e3_shifted.json'},
    # needs anchor for passing test
    {'source_sheet': 'e4', 'target_sheet': 'e4_shifted', 'source_annotation': 'source_e4.json', 'target_annotation': 'expected_e4_shifted.json'},
    {'source_sheet': 'e4', 'target_sheet': 'e4_misaligned', 'source_annotation': 'source_e4.json', 'target_annotation': 'expected_e4_misaligned.json'},
    {'source_sheet': 'e4', 'target_sheet': 'e4_empty_row', 'source_annotation': 'source_e4.json', 'target_annotation': 'source_e4.json'},
    {'source_sheet': 'india_wheat', 'target_sheet': 'india_wheat', 'source_annotation': 'source_india_wheat.json', 'target_annotation': 'expected_india_wheat.json'},
    {'source_sheet': 'india_wheat', 'target_sheet': 'shifted_india_wheat', 'source_annotation': 'source_india_wheat.json', 'target_annotation': 'expected_shifted_india_wheat.json'},
    # needs minimum number of anchor for passing test
    {'source_sheet': 'india_wheat', 'target_sheet': 'shifted_india_wheat_wo_anchors', 'source_annotation': 'source_india_wheat.json','target_annotation': 'expected_shifted_india_wheat_wo_anchors.json'}
]


def test_all_test_scenarios():
    failed_cases = []
    for test_case in test_cases:
        source_df = pd.read_excel('../resources/data.xlsx', sheet_name=test_case['source_sheet'], engine='openpyxl', index_col=None, header=None)
        target_df = pd.read_excel('../resources/data.xlsx', sheet_name=test_case['target_sheet'], engine='openpyxl', index_col=None, header=None)

        with open(f"../resources/annotations/{test_case['source_annotation']}") as f:
            source_annotations = json.load(f)

        with open(f"../resources/annotations/{test_case['target_annotation']}") as f:
            target_annotations = json.load(f)

        source = Sheet('source', source_df, source_annotations)
        target = Sheet('target', target_df)

        try:
            annotator = Annotator(source)
            annotations, status = annotator.generate_annotations(target)
            assert status == OptimizationStatus.OPTIMAL
            assert annotations == target_annotations
        except AssertionError as e:
            failed_cases.append((test_case, e))

    error_message = f"Unmatched annotations: {[failed_case['target_annotation'] for failed_case, e in failed_cases]}"
    assert len(failed_cases) == 0, error_message


def test_annotator():
    test_case = {'source_sheet': 'e4', 'target_sheet': 'e4_empty_row', 'source_annotation': 'source_e4.json', 'target_annotation': 'source_e4.json'}

    source_df = pd.read_excel('../resources/data.xlsx', sheet_name=test_case['source_sheet'], engine='openpyxl', index_col=None, header=None)
    target_df = pd.read_excel('../resources/data.xlsx', sheet_name=test_case['target_sheet'], engine='openpyxl', index_col=None, header=None)

    with open(f"../resources/annotations/{test_case['source_annotation']}") as f:
        source_annotations = json.load(f)

    with open(f"../resources/annotations/{test_case['target_annotation']}") as f:
        expected_target_annotations = json.load(f)

    source = Sheet('source', source_df, source_annotations)
    annotator = Annotator(source)

    target = Sheet('target', target_df)
    annotations, status = annotator.generate_annotations(target)

    assert status == OptimizationStatus.OPTIMAL
    assert annotations == expected_target_annotations
