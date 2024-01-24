from relation import Relation

def _get_matching_close_bracket(query : str, index_open_bracket : int) -> int:
    num_open_brackets = 1
    for i in range(index_open_bracket + 1, len(query)):
        if query[i] == '(':
            num_open_brackets += 1
        elif query[i] == ')':
            num_open_brackets -= 1
        if num_open_brackets == 0:
            return i

class QueryExecutor:

    def __init__(self, query, relations):
        self._query = query
        self._relations = relations
        self._num_inter_relations = 0
        self._result = self._execute_query(self._query)
    
    def get_result(self) -> Relation:
        return self._result

    def _get_relation(self, name : str) -> Relation:
        for relation in self._relations:
            if name == relation.get_name():
                return relation

    def _execute_query(self, query : str, inter_relation_name=None) -> Relation:
        if not '(' in query:
            return self._execute_single_query(query, inter_relation_name)
        
        index_open_bracket = query.find('(')
        index_close_bracket = _get_matching_close_bracket(query, index_open_bracket)

        self._num_inter_relations += 1
        new_inter_relation_name = f'relation{self._num_inter_relations}'

        simplified_query = query[:index_open_bracket] + new_inter_relation_name + query[index_close_bracket + 1:]

        contents_of_brackets = query[index_open_bracket + 1: index_close_bracket]
        self._execute_query(contents_of_brackets, new_inter_relation_name)
        return self._execute_query(simplified_query, inter_relation_name)
        
    def _execute_single_query(self, query : str, inter_relation_name=None) -> Relation:
        query_split = query.split(' ')
        relation = self._get_relation(query_split[-1])

        if 'σ' in query:
            result = relation.selection(query_split[1])
        elif 'π' in query:
            result = relation.projection(query_split[1].split(','))
        else:
            relation1 = self._get_relation(query_split[0])
            relation2 = relation
            if '⨝' in query:
                if len(query_split) == 4:
                    columns = query_split[2].split('=')
                    result = relation1.inner_join(relation2, columns[0], columns[1])
                else:
                    result = relation1.inner_join(relation2)
            elif '⟕' in query:
                if len(query_split) == 4:
                    columns = query_split[2].split('=')
                    result = relation1.left_outer_join(relation2, columns[0], columns[1])
                else:
                    result = relation1.left_outer_join(relation2)
            elif '⟖' in query:
                if len(query_split) == 4:
                    columns = query_split[2].split('=')
                    result = relation1.right_outer_join(relation2, columns[0], columns[1])
                else:
                    result = relation1.right_outer_join(relation2)
            elif '⟗' in query:
                if len(query_split) == 4:
                    columns = query_split[2].split('=')
                    result = relation1.full_outer_join(relation2, columns[0], columns[1])
                else:
                    result = relation1.full_outer_join(relation2)
            elif '∪' in query:
                result = relation1.union(relation2)
            elif '∩' in query:
                result = relation1.intersection(relation2)
            elif '-' in query:
                result = relation1.difference(relation2)

        result.set_name(inter_relation_name)
        self._relations.append(result)
        return result
