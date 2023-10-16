from src.components.dash_page_progression.tree import DashTree
from src.components.dash_page_progression.figure import figure_from


class DashPage:

    def __init__(self, regex):
        self.finalized_tree = DashTree(regex)
        self.final_figure = figure_from(self.finalized_tree.regex)

        self.tree_pages = [self.final_figure for _ in range(self.page_quantity())]

    @staticmethod
    def empty_dash_page():
        return DashPage('a#')

    def page_quantity(self):
        """Returns the quantity of tree vertices to be iterated plus the final and complete figure."""
        return len(self.finalized_tree.vertices()) + 1

    def color_figures_by_actual_node(self):

        for index, tree_figure in enumerate(self.tree_pages):
            pass


if __name__ == '__main__':
    print(DashPage.empty_dash_page())
