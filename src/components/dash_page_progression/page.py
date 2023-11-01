from src.components.dash_page_progression.tree import DashTree
from src.components.dash_page_progression.figure import figure_from


class DashPage:

    def __init__(self, regex):
        self.finalized_tree = DashTree(regex)
        self.final_figure = figure_from(self.finalized_tree.regex)

    @staticmethod
    def empty_dash_page():
        return DashPage('a#')

    def page_quantity(self):
        """Returns the quantity of tree vertices to be iterated."""
        return len(self.finalized_tree.vertices())


if __name__ == '__main__':
    print(DashPage.empty_dash_page())
