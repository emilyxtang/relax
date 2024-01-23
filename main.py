from query_executor import QueryExecutor
from relation import Relation

OPERATORS = ['σ', 'π', '⨝', '∪', '∩', '-']
RELATIONS_TITLE = 'RELATION(S)'
QUERY_TITLE = 'QUERY'
RESULT_TITLE = 'RESULT'

query = ''
relations = []
len_line = 0

def create_relation(relation : list[str]) -> Relation:
    name = relation[0].split('=')[0].strip()
    if not name[0].isalpha():
        raise ValueError(f'Name \'{name}\' must start with an alphabetical character.')

    columns = [column.strip() for column in relation[1].split(',')]
    for column in columns:
        if not column.isalpha():
            raise ValueError(f'Column \'{column}\' must not contain non-alphabetical characters.')
          
    rows = []
    for i in range(2, len(relation)):
        cells = relation[i].split(',')
        for i, cell in enumerate(cells):
            cells[i] = cell.replace('\'', '').strip()
            if cells[i].isnumeric():
                cells[i] = int(cells[i])
        rows.append(cells)
    return Relation(columns, rows, name)

def read_input_file() -> None:
    global query, relations
    input = open('input.txt', 'r').readlines()

    relation = []
    is_relation = False

    for line in input:
        line = line.strip()

        if any(operator in line for operator in OPERATORS):
            query = line
            num_open_brackets = query.count('(')
            num_closed_brackets = query.count(')')
            if num_open_brackets != num_closed_brackets:
                raise ValueError(f'# of open brackets does not match the # of closed brackets in query \'{query}\'')
        else:
            if '{' in line:
                is_relation = True
            elif '}' in line:
                relation = [line for line in relation if line != '']
                relations.append(create_relation(relation))
                is_relation = False
                relation = []

            if is_relation:
                relation.append(line)

    relation_names = [relation.get_name() for relation in relations]
    if len(relation_names) != len(set(relation_names)):
        raise ValueError('Cannot have two or more relations with the same name.')

def print_title(title : str) -> None:
    print('\n' + title + ' ' + ('-' * (len_line - len(title) - 1)))

def print_relations() -> None:
    global len_line

    # get the string representation of each relation
    str_relations = [str(relation).splitlines() for relation in relations]

    # determine the length of the longest string representation of a relation
    max_str_relation = max([len(relation) for relation in str_relations])

    # fill each string representation with empty lines until it reaches the
    # the length of the longest string representation of a relation
    for i, relation in enumerate(str_relations):
        while len(relation) < max_str_relation:
            str_relations[i].append(' ' * len(relation[0]))

    # join the lines of each string representation and print the result
    str_relations = ['  '.join(lines) for lines in zip(*str_relations)]
    len_line = len(str_relations[0])
    print_title(RELATIONS_TITLE)
    print()
    [print(line) for line in str_relations]

def print_query() -> None:
    print_title(QUERY_TITLE)
    print()
    print(query)

def print_execute_query() -> None:
    print_title(RESULT_TITLE)
    print(QueryExecutor(query, relations).get_result())
    print()

if __name__ == '__main__':
    try:
        read_input_file()
        print_relations()
        print_query()
        print_execute_query()
    except Exception as ex:
        print(ex)
        print()
