from itertools import combinations

from mip import Model, MAXIMIZE, CBC, maximize

from src.annotation import Annotation
from src.selection import X1, X2, Y1, Y2
from src.utils import generate_block_constraints, initialize_block


class Annotator:
    annotations = []

    def __init__(self, source_df, source_annotations):
        for annotation in source_annotations:
            self.annotations.append(Annotation(annotation))

    def generate_annotations(self, target_df):
        model = Model(sense=MAXIMIZE, solver_name=CBC)

        objective_expressions = []
        for annotation in self.annotations:
            objective_expressions.append(initialize_block(annotation, model))

        for annotation_pair in list(combinations(self.annotations, 2)):
            generate_block_constraints(annotation_pair[0], annotation_pair[1], model)

        model.objective = maximize(sum(objective_expressions))
        status = model.optimize()

        target_annotations = []
        for annotation in self.annotations:
            x1 = model.var_by_name(annotation.var_name(X1))
            x2 = model.var_by_name(annotation.var_name(X2))
            y1 = model.var_by_name(annotation.var_name(Y1))
            y2 = model.var_by_name(annotation.var_name(Y2))

            target_annotations.append(annotation.generate_target_annotations(x1, x2, y1, y2))

        return target_annotations
