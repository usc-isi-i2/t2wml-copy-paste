from mip import INTEGER

from src.selection import X1, X2, Y1, Y2, Selection
from src.tf_idf import TF_IDF


def generate_constraints(v0, v1, index_0, index_1):
    if index_0 < index_1:
        return v0 + 1 <= v1
    elif index_0 > index_1:
        return v1 + 1 <= v0
    else:
        return v1 == v0


def generate_block_constraints(block_0, block_1, model):
    v0_x1 = model.var_by_name(name=block_0.var_name(X1))
    v0_x2 = model.var_by_name(name=block_0.var_name(X2))
    v0_y1 = model.var_by_name(name=block_0.var_name(Y1))
    v0_y2 = model.var_by_name(name=block_0.var_name(Y2))

    v1_x1 = model.var_by_name(name=block_1.var_name(X1))
    v1_x2 = model.var_by_name(name=block_1.var_name(X2))
    v1_y1 = model.var_by_name(name=block_1.var_name(Y1))
    v1_y2 = model.var_by_name(name=block_1.var_name(Y2))

    model.add_constr(generate_constraints(v0_x1, v1_x1, block_0.source_selection.x1, block_1.source_selection.x1))
    model.add_constr(generate_constraints(v0_x1, v1_x2, block_0.source_selection.x1, block_1.source_selection.x2))
    model.add_constr(generate_constraints(v0_x1, v1_y1, block_0.source_selection.x1, block_1.source_selection.y1))
    model.add_constr(generate_constraints(v0_x1, v1_y2, block_0.source_selection.x1, block_1.source_selection.y2))
    model.add_constr(generate_constraints(v0_x2, v1_x1, block_0.source_selection.x2, block_1.source_selection.x1))
    model.add_constr(generate_constraints(v0_x2, v1_x2, block_0.source_selection.x2, block_1.source_selection.x2))
    model.add_constr(generate_constraints(v0_x2, v1_y1, block_0.source_selection.x2, block_1.source_selection.y1))
    model.add_constr(generate_constraints(v0_x2, v1_y2, block_0.source_selection.x2, block_1.source_selection.y2))
    model.add_constr(generate_constraints(v0_y1, v1_x1, block_0.source_selection.y1, block_1.source_selection.x1))
    model.add_constr(generate_constraints(v0_y1, v1_x2, block_0.source_selection.y1, block_1.source_selection.x2))
    model.add_constr(generate_constraints(v0_y1, v1_y1, block_0.source_selection.y1, block_1.source_selection.y1))
    model.add_constr(generate_constraints(v0_y1, v1_y2, block_0.source_selection.y1, block_1.source_selection.y2))
    model.add_constr(generate_constraints(v0_y2, v1_x1, block_0.source_selection.y2, block_1.source_selection.x1))
    model.add_constr(generate_constraints(v0_y2, v1_x2, block_0.source_selection.y2, block_1.source_selection.x2))
    model.add_constr(generate_constraints(v0_y2, v1_y1, block_0.source_selection.y2, block_1.source_selection.y1))
    model.add_constr(generate_constraints(v0_y2, v1_y2, block_0.source_selection.y2, block_1.source_selection.y2))


def initialize_block(block, model, bound_selection: Selection):
    x1 = model.add_var(name=block.var_name(X1), lb=bound_selection.x1, ub=bound_selection.x2, var_type=INTEGER)
    x2 = model.add_var(name=block.var_name(X2), lb=bound_selection.x1, ub=bound_selection.x2, var_type=INTEGER)
    y1 = model.add_var(name=block.var_name(Y1), lb=bound_selection.y1, ub=bound_selection.y2, var_type=INTEGER)
    y2 = model.add_var(name=block.var_name(Y2), lb=bound_selection.y1, ub=bound_selection.y2, var_type=INTEGER)

    model.add_constr(x1 <= x2)
    model.add_constr(y1 <= y2)

    return x2 - x1 + y2 - y1


def get_tf_idf_classifier(source_tables, target_tables):
    tfidf = TF_IDF()
    for table_name, table in source_tables.items():
        tfidf.add_document(table_name, table.get_strings())
    for table_name, table in target_tables.items():
        tfidf.add_document(table_name, table.get_strings())
    tfidf.pre_compute()

    return tfidf


def get_source_target_table_maps(source_tables, target_tables):
    source_target_table_maps = []
    tf_idf = get_tf_idf_classifier(source_tables, target_tables)
    for s in range(0, len(source_tables)):
        source = f'source_{s}'
        best_similarity = 0
        best_target_selection = None
        for t in range(0, len(target_tables)):
            target = f'target_{t}'
            similarity = tf_idf.similarity(source, target)
            if similarity > best_similarity:
                best_similarity = similarity
                best_target_selection = target_tables[target].selection

        source_target_table_maps.append({
            'source_selection': source_tables[source].selection,
            'target_selection': best_target_selection
        })

    return source_target_table_maps