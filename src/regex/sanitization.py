def is_correct(regex):
    return (are_parenthesis_correct_for(regex) and
            are_pipes_correct_for(regex) and
            are_concatenations_correct_for(regex) and
            are_stars_correct_for(regex) and
            not is_using_question_mark_operator(regex))


def are_parenthesis_correct_for(regex):
    parenthesis_count = 0

    sentence = regex.replace(' ', '')

    for letter in sentence:
        if letter == '(':
            parenthesis_count += 1
        elif letter == ')':
            parenthesis_count -= 1

    return parenthesis_count == 0


def are_pipes_correct_for(regex):
    return ('||' not in regex
            and '(|' not in regex
            and '|)' not in regex
            and '.|' not in regex
            and '|.' not in regex
            and '*|' not in regex
            and '|*' not in regex) and regex[0] != '|' and regex[-1] != '|'


def are_concatenations_correct_for(regex):
    return ('..' not in regex
            and '(.' not in regex
            and '.)' not in regex
            and '*.' not in regex
            and '.*' not in regex) and regex[0] != '.' and regex[-1] != '.'


def are_stars_correct_for(regex):
    return ('**' not in regex
            and '(*' not in regex
            and '*)' not in regex) and regex[0] != '*'


def is_using_question_mark_operator(regex):
    return '?' in regex
