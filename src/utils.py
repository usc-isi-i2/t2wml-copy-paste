from mip import INTEGER


def generate_constraints(v0, v1, index_1, index_2):
    if index_1 < index_2:
        return v0 + 1 <= v1
    elif index_1 == index_2:
        return v0 == v1
    else:
        return v0 + 1 >= v1


def generate_block_constraints(block_0, block_1, model):
    v0_x1 = model.var_by_name(name=f"{block_0.id}_x1")
    v0_x2 = model.var_by_name(name=f"{block_0.id}_x1")
    v0_y1 = model.var_by_name(name=f"{block_0.id}_x1")
    v0_y2 = model.var_by_name(name=f"{block_0.id}_x1")

    v1_x1 = model.var_by_name(name=f"{block_1.id}_x1")
    v1_x2 = model.var_by_name(name=f"{block_1.id}_x1")
    v1_y1 = model.var_by_name(name=f"{block_1.id}_x1")
    v1_y2 = model.var_by_name(name=f"{block_1.id}_x1")

    model.add_constr(generate_constraints(v0_x1, v1_x1, block_0.selection.x1, block_1.selection.x1))
    model.add_constr(generate_constraints(v0_x1, v1_x2, block_0.selection.x1, block_1.selection.x2))
    model.add_constr(generate_constraints(v0_x1, v1_y1, block_0.selection.x1, block_1.selection.y1))
    model.add_constr(generate_constraints(v0_x1, v1_y2, block_0.selection.x1, block_1.selection.y2))
    model.add_constr(generate_constraints(v0_x2, v1_x1, block_0.selection.x2, block_1.selection.x1))
    model.add_constr(generate_constraints(v0_x2, v1_x2, block_0.selection.x2, block_1.selection.x2))
    model.add_constr(generate_constraints(v0_x2, v1_y1, block_0.selection.x2, block_1.selection.y1))
    model.add_constr(generate_constraints(v0_x2, v1_y2, block_0.selection.x2, block_1.selection.y2))
    model.add_constr(generate_constraints(v0_y1, v1_x1, block_0.selection.y1, block_1.selection.x1))
    model.add_constr(generate_constraints(v0_y1, v1_x2, block_0.selection.y1, block_1.selection.x2))
    model.add_constr(generate_constraints(v0_y1, v1_y1, block_0.selection.y1, block_1.selection.y1))
    model.add_constr(generate_constraints(v0_y1, v1_y2, block_0.selection.y1, block_1.selection.y2))
    model.add_constr(generate_constraints(v0_y2, v1_x1, block_0.selection.y2, block_1.selection.x1))
    model.add_constr(generate_constraints(v0_y2, v1_x2, block_0.selection.y2, block_1.selection.x2))
    model.add_constr(generate_constraints(v0_y2, v1_y1, block_0.selection.y2, block_1.selection.y1))
    model.add_constr(generate_constraints(v0_y2, v1_y2, block_0.selection.y2, block_1.selection.y2))

def initialize_block(annotation, model):
    x1 = model.add_var(name=f"{annotation.id}_x1", lb=annotation.selection.x1, ub=annotation.selection.x1, var_type=INTEGER)
    x2 = model.add_var(name=f"{annotation.id}_x2", lb=annotation.selection.x2, ub=annotation.selection.x2, var_type=INTEGER)
    y1 = model.add_var(name=f"{annotation.id}_y1", lb=annotation.selection.y1, ub=annotation.selection.y1, var_type=INTEGER)
    y2 = model.add_var(name=f"{annotation.id}_y2", lb=annotation.selection.y2, ub=annotation.selection.y2, var_type=INTEGER)

    model.add_constr(x1 <= x2)
    model.add_constr(y1 <= y2)

    return x2 - x1 + y2 - y1