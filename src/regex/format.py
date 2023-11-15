operators = {'*', '.', '|', '+', '?'}
parenthesis = {'(', ')'}
non_terminals = operators | parenthesis


def eat(regex) -> list and set:
    """Eats a non formatted regex and returns its list digested form
    with its terminal symbols."""

    if len(regex) == 1:
        # If a regex is 1 char long, that regex is already digested.
        return [regex], {regex}

    regex = ['('] + list(regex) + [')'] + (['#'] if regex[-1] != '#' else [])
    regex = ''.join(regex)

    digest = regex.replace(' ', '')

    digest = __add_missing_concatenations(digest)
    return list(digest), __terminals_from(digest) | {'&'}


def __add_missing_concatenations(regex):
    stripped = list(regex.replace('.', ''))
    concatenated = '.'.join(stripped)  # Join all strings in a list of strings with periods.

    # As we added '.' between every string, we need to trim the wrong additions.
    return concatenated.replace('(.', '(').replace('.)', ')').replace('.|.', '|').replace('.*', '*').replace('.?', '?')


def __terminals_from(regex) -> set:
    """Scans a regex and gathers its terminals inside a set."""
    terminals = set()

    for symbol in regex:
        if symbol not in operators and symbol not in parenthesis:
            terminals.add(symbol)
    return terminals


def sides_for(operator, regex):
    """:returns the inner regexes of a :param regex
    at the side of a given :param operator"""

    left_tree, right_tree = str(), str()
    parenthesis_count = 0

    for i in range(len(regex) - 1, -1, -1):  # We'll be looking from right to left.
        if regex[i] == operator and parenthesis_count == 0:
            left_tree = regex[:i]
            return left_tree, right_tree[::-1]

        if regex[i] == ')':
            parenthesis_count += 1
        elif regex[i] == '(':
            parenthesis_count -= 1

        right_tree += regex[i]

    return left_tree, right_tree[::-1]


if __name__ == '__main__':
    print(eat('a b c'))
    print(eat('a|b|c'))
