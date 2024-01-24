"""
A module to solve queries given a query and a list of relations.
"""

from relation import Relation

def _get_matching_close_bracket(query : str, index_open_bracket : int) -> int:
    """
    Return the index of the matching close bracket of the specified query and
    index of the open bracket.
    """
    num_open_brackets = 1
    for i in range(index_open_bracket + 1, len(query)):
        if query[i] == '(':
            num_open_brackets += 1
        elif query[i] == ')':
            num_open_brackets -= 1
        if num_open_brackets == 0:
            return i

class QueryExecutor:

    def __init__(self, query : str, relations : list[Relation]):
        """
        Initializes a QueryExecutor with the given query and
        list of Relations.
        """
        self._query = query
        self._relations = relations
        self._num_inter_relations = 0
        self._result = self._execute_query(self._query)
    
    def get_result(self) -> Relation:
        """
        Returns the result of the query.
        """
        return self._result

    def _get_relation(self, name : str) -> Relation:
        """
        Returns a Relation with the given name from the list of Relations.
        """
        for relation in self._relations:
            if name == relation.get_name():
                return relation

    def _execute_query(self, query : str,
        inter_relation_name=None) -> Relation:
        """
        Executes the given query.

        Args:
            query (str): The query to execute.
            inter_relation_name (str): The name to save the query as.
        """
        # base case: no brackets in the query, only one operation to perform
        if not '(' in query:
            return self._execute_single_query(query, inter_relation_name)
        
        # determine where the brackets enclosing the next operation to execute
        # are
        index_open_bracket = query.find('(')
        index_close_bracket = _get_matching_close_bracket(query,
            index_open_bracket)

        # create a name for the intermediate relation (relation within the
        # the brackets that we must solve first)
        self._num_inter_relations += 1
        new_inter_relation_name = f'relation{self._num_inter_relations}'

        # rewrite the given query using the name of the intermediate relation
        simplified_query = query[:index_open_bracket] + \
            new_inter_relation_name + query[index_close_bracket + 1:]

        # execute the intermediate query and save it in the list of relations
        inter_query = query[index_open_bracket + 1: index_close_bracket]
        self._execute_query(inter_query, new_inter_relation_name)

        # continue solving the query using the simplified version of the query
        return self._execute_query(simplified_query, inter_relation_name)
        
    def _execute_single_query(self, query : str,
        inter_relation_name=None) -> Relation:
        """
        Executes the given single operation query.

        Args:
            query (str): The query to execute.
            inter_relation_name (str): The name to save the query as.
        """
        query_split = query.split(' ')
        relation = self._get_relation(query_split[-1])

        if 'σ' in query:
            result = relation.selection(query_split[1])
        elif 'π' in query:
            result = relation.projection(query_split[1].split(','))
        else:
            relation1 = self._get_relation(query_split[0])
            relation2 = relation
            # perform join operations
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
            # perform set operations
            elif '∪' in query:
                result = relation1.union(relation2)
            elif '∩' in query:
                result = relation1.intersection(relation2)
            elif '-' in query:
                result = relation1.difference(relation2)

        result.set_name(inter_relation_name)
        self._relations.append(result)
        return result
