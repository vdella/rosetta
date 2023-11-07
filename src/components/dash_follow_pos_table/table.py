from src.components.dash_page_progression.tree import DashTree


def follow_pos_data_from(tree: DashTree):
    tree.syntax_tree.root.calculate_follow_pos()

    follow_pos = dict()  # Needs to be a list of dicts.

    root = tree.syntax_tree.root
    queue = [root]

    while queue:
        current = queue.pop(0)
        follow_pos[current] = current.follow_pos

        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)

    for key in follow_pos.copy():
        if key.regex_symbol in {'.', '*', '|'}:
            del follow_pos[key]

    unorganized_follow_pos: dict = follow_pos.copy()
    follow_pos = dict()

    for terminal_node, follow_pos_set in unorganized_follow_pos.items():
        follow_pos[terminal_node.serial_number] = skin_individual_follow_pos_set(follow_pos_set)

    sorted_follow_pos = dict(sorted(follow_pos.items()))
    return [{'Node n': k, 'follow_pos(n)': v} for k, v in sorted_follow_pos.items()]


def skin_individual_follow_pos_set(follow_pos_nodes):
    string = [str(node.serial_number) for node in follow_pos_nodes]
    string.sort()

    label = ''.join(string)
    return label


if __name__ == '__main__':
    btree = '(a|b)*abb#'
    follow_pos_ = follow_pos_data_from(DashTree(btree))

    print(follow_pos_data_from(DashTree(btree)))
