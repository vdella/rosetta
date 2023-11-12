from src.components.dash_page_progression.tree import DashTree
from src.regex.conversion import fa_from


def fa_table_data_from(tree: DashTree):
    regex = tree.regex
    fa = fa_from(regex)
    return [{'(source_state, symbol)': '(' + str(k[0]) + ', ' + k[1] + ')', 'destiny_state': str(v.pop())} for k, v in fa.transitions.items()]


def skin_individual_follow_pos_set(follow_pos_nodes):
    string = [str(node.serial_number) for node in follow_pos_nodes]
    string.sort()

    label = ''.join(string)
    return label


if __name__ == '__main__':
    btree = '(a|b)*abb#'
    fa = fa_from(btree)
    print(fa)

    print(fa_table_data_from(DashTree(btree)))
