from itertools import combinations

from mip import Model, MAXIMIZE, CBC, maximize, OptimizationStatus

from src import conflict
from src.conflict import ConflictFinder
from src.selection import X1, X2, Y1, Y2, Selection
from src.sheet import Sheet
from src.utils import generate_block_constraints, initialize_block, get_source_target_table_maps


class Annotator:
    annotations = []

    def __init__(self, source: Sheet):
        self.source = source

    def generate_annotations(self, target: Sheet):
        model = Model(sense=MAXIMIZE, solver_name=CBC)

        source_tables = self.source.extract_tables()
        target_tables = target.extract_tables()
        source_target_table_maps = get_source_target_table_maps(source_tables, target_tables)

        objective_expressions = []
        for annotation in self.source.annotations:
            bounded_selection = Selection(1, target.dataframe.shape[1], 1, target.dataframe.shape[0])
            for source_target_table_map in source_target_table_maps:
                if source_target_table_map['source_selection'].contains(annotation.source_selection) and  source_target_table_map['target_selection']:
                    bounded_selection = source_target_table_map['target_selection']

            objective_expressions.append(initialize_block(annotation, model, bounded_selection))

        for annotation_pair in list(combinations(self.source.annotations, 2)):
            generate_block_constraints(annotation_pair[0], annotation_pair[1], model)

        anchors = self.source.find_anchors(target)
        for anchor in anchors:
            initialize_block(anchor, model, anchor.target_selection)
            for annotation in self.source.annotations:
                generate_block_constraints(anchor, annotation, model)

        model.objective = maximize(sum(objective_expressions))
        status = model.optimize()
        if not (status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE):
            # To debug infeasible model
            # cf = ConflictFinder(model)
            # iis = cf.find_iis(method=conflict.IISFinderAlgorithm.DELETION_FILTER)
            return None, status

        target_annotations = []
        for annotation in self.source.annotations:
            x1 = int(model.var_by_name(annotation.var_name(X1)).x)
            x2 = int(model.var_by_name(annotation.var_name(X2)).x)
            y1 = int(model.var_by_name(annotation.var_name(Y1)).x)
            y2 = int(model.var_by_name(annotation.var_name(Y2)).x)

            target_annotations.append(annotation.generate_target_annotations(x1, x2, y1, y2))

        return target_annotations, status
