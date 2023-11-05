from src.components.dash_page_progression.tree import DashTree
from src.components.dash_page_progression.node import DashNode
from src.components.dash_page_progression.figure import figure_from, copy


class DashPage:

    def __init__(self, regex):
        self.finalized_tree = DashTree(regex)
        self.final_figure = figure_from(self.finalized_tree.regex)

    def follow_pos_figure(self):
        follow_pos_figure = copy(self.final_figure)

        follow_pos_figure.update_layout(
            title={
                'text': 'FollowPosTree',
                'xanchor': 'center',  # Without it, the title is created to the left.
            }
        )
        follow_pos_figure.update_traces(marker=dict(opacity=1.0))

        return follow_pos_figure

    def pagination_notes(self):
        pagination_notes = [self.finalized_tree.nodes.copy() for _ in range(self.page_quantity())]

        for active_page, page_note in enumerate(pagination_notes.copy()):
            for index, node in enumerate(page_note.values()):
                node: DashNode

                if node.reverse_level_creation_id > active_page:
                    pagination_notes[active_page][index] = None
                else:
                    pagination_notes[active_page][index] = str(node)

        return pagination_notes

    def opacities(self):
        opacities = self.pagination_notes().copy()

        for active_page, page_note in enumerate(self.pagination_notes()):
            for index, note in enumerate(page_note.values()):

                opacities[active_page][index] = 1 if note else 0.4

        return opacities

    @staticmethod
    def empty_dash_page():
        return DashPage('a#')

    def page_quantity(self):
        """Returns the quantity of tree vertices to be iterated."""
        return len(self.finalized_tree.vertices()) + 1


if __name__ == '__main__':
    for page in DashPage('aaa#').opacities():
        print(page)
