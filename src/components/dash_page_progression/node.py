from src.regex.syntax_tree import Node, stringfy


class DashNode:

    def __init__(self, node: Node):
        if node:
            self.syntax_tree_node = node
            self.regex_symbol = node.regex_symbol

            self.nullable = node.nullable()
            self.first_pos, self.last_pos = stringfy(node)

            self.reverse_level_creation_id = 0

    def __str__(self):
        return (f"nullable: {self.nullable}<br />"
                f"first_pos: {self.first_pos}<br />"
                f"last_pos: {self.last_pos}<br />") if self else ''
