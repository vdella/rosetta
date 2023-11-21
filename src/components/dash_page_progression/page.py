from src.components.dash_page_progression.tree import DashTree
from src.components.dash_page_progression.node import DashNode
from src.components.dash_page_progression.figure import figure_from


class DashPage:

    def __init__(self, regex):
        self.finalized_tree = DashTree(regex)
        self.final_figure = figure_from(self.finalized_tree.regex)

        self._pagination_notes = None
        self._opacities = None
        self._colors = None

    @property
    def pagination_notes(self):
        if not self._pagination_notes:
            self._pagination_notes = self.compute_pagination_notes()
        return self._pagination_notes

    def compute_pagination_notes(self):
        pagination_notes = [self.finalized_tree.nodes.copy() for _ in range(self.page_quantity())]

        for active_page, page_note in enumerate(pagination_notes.copy()):
            for index, node in enumerate(page_note.values()):
                node: DashNode

                if node.reverse_level_creation_id > active_page:
                    pagination_notes[active_page][index] = None
                else:
                    pagination_notes[active_page][index] = str(node)

        return pagination_notes

    @property
    def opacities(self):
        if not self._opacities:
            self._opacities = self.compute_opacities()
        return self._opacities

    def compute_opacities(self):
        opacities = self.compute_pagination_notes().copy()

        for active_page, page_note in enumerate(self.pagination_notes):
            for index, note in enumerate(page_note.values()):

                opacities[active_page][index] = 1 if note else 0.4

        return opacities

    @property
    def colors(self):
        if not self._colors:
            self._colors = self.compute_colors()
        return self._colors

    def compute_colors(self):
        colors = self.compute_pagination_notes().copy()

        for active_page, page_note in enumerate(self.pagination_notes):
            for index, note in enumerate(page_note.values()):

                colors[active_page][index] = 'rgb(255, 255, 255)' if note else 'rgb(119, 52, 235)'

        return colors

    @staticmethod
    def empty_dash_page():
        return DashPage('a#')

    def page_quantity(self):
        """Returns the quantity of tree vertices to be iterated."""
        return len(self.finalized_tree.vertices()) + 1


if __name__ == '__main__':
    for page in DashPage('bbb#').pagination_notes:
        print(page)
