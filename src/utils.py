from mip import INTEGER

from src.selection import X1, X2, Y1, Y2


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


def initialize_block(block, model):
    x_lb, x_ub, y_lb, y_ub = block.get_bounds()

    x1 = model.add_var(name=block.var_name(X1), lb=x_lb, ub=x_ub, var_type=INTEGER)
    x2 = model.add_var(name=block.var_name(X2), lb=x_lb, ub=x_ub, var_type=INTEGER)
    y1 = model.add_var(name=block.var_name(Y1), lb=y_lb, ub=y_ub, var_type=INTEGER)
    y2 = model.add_var(name=block.var_name(Y2), lb=y_lb, ub=y_ub, var_type=INTEGER)

    model.add_constr(x1 <= x2)
    model.add_constr(y1 <= y2)

    return x2 - x1 + y2 - y1
