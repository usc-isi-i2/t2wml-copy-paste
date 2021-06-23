from itertools import combinations

from mip import Model, MAXIMIZE, CBC, maximize, OptimizationStatus

from src.selection import X1, X2, Y1, Y2
from src.sheet import Sheet
from src.utils import generate_block_constraints, initialize_block


class Annotator:
    annotations = []

    def __init__(self, source: Sheet):
        self.source = source

    def generate_annotations(self, target: Sheet):
        model = Model(sense=MAXIMIZE, solver_name=CBC)

        objective_expressions = []
        for annotation in self.source.annotations:
            objective_expressions.append(initialize_block(annotation, model))

        for annotation_pair in list(combinations(self.source.annotations, 2)):
            generate_block_constraints(annotation_pair[0], annotation_pair[1], model)

        anchors = self.source.find_anchors(target)
        for anchor in anchors:
            initialize_block(anchor, model)
            for annotation in self.source.annotations:
                generate_block_constraints(anchor, annotation, model)

        model.objective = maximize(sum(objective_expressions))
        status = model.optimize()
        assert (status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE)

        target_annotations = []
        for annotation in self.source.annotations:
            x1 = int(model.var_by_name(annotation.var_name(X1)).x)
            x2 = int(model.var_by_name(annotation.var_name(X2)).x)
            y1 = int(model.var_by_name(annotation.var_name(Y1)).x)
            y2 = int(model.var_by_name(annotation.var_name(Y2)).x)

            target_annotations.append(annotation.generate_target_annotations(x1, x2, y1, y2))

        return target_annotations
