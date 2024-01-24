"""
A module to perform operations on relations.
"""

import pandas as pd
from tabulate import tabulate

def _init_relation_from_df(df : pd.DataFrame) -> 'Relation':
    df = df.drop_duplicates()
    return Relation(list(df), df.values.tolist())

class Relation:

    def __init__(self, columns : list[str], rows : list[list[any]], name=None):
        """
        Initializes a Relation with the given columns, rows, and name.
        
        Examples:
            >>> columns = ['id', 'name', 'email']
            >>> rows = [[1, 'Bob', 'bob@c'], [2, 'Jim', 'j@c']]
            >>> print(Relation(columns, rows, 'students'))
            students                   
            ┌──────┬────────┬─────────┐
            │   id │ name   │ email   │
            ├──────┼────────┼─────────┤
            │    1 │ Bob    │ bob@c   │
            ├──────┼────────┼─────────┤
            │    2 │ Jim    │ j@c     │
            └──────┴────────┴─────────┘
        """
        self._table = pd.DataFrame(rows, columns=columns).drop_duplicates()
        self._name = name

    def __str__(self) -> str:
        """
        Returns the string representation of the Relation.
        """
        table = tabulate(self._table, headers='keys', tablefmt='simple_grid',
            showindex=False)
        width_table = len(table.splitlines()[0])
        if self._name:
            name = self._name + (' ' * (width_table - len(self._name)))
        else:
            name = ' ' * width_table
        return name + '\n' + table

    def get_name(self) -> str:
        """
        Returns the name of the Relation.
        """
        return self._name

    def set_name(self, name : str) -> None:
        """
        Sets the name of the Relation to the given name.
        """
        self._name = name

    def get_columns(self) -> list[str]:
        """
        Returns the columns of the Relation.
        """
        return list(self._table)

    def selection(self, expression : str) -> 'Relation':
        """
        Returns a new Relation representing the selection operation using the
        given expression.
        """
        return _init_relation_from_df(self._table.query(expression))
    
    def projection(self, columns : list[str]) -> 'Relation':
        """
        Returns a new Relation representing the projection operation using the
        given columns.
        """
        return _init_relation_from_df(self._table[columns])

    def inner_join(self, relation : 'Relation', left_on=None,
        right_on=None) -> 'Relation':
        """
        Returns a new Relation representing the inner join operation.

        If left_on and right_on are not provided, the Relations will be joined
        based on all the columns that the two Relations have in common.

        Args:
            left_on (str): A column in the current Relation to join on.
            right_on (str): A column in the provided Relation to join on.
        """
        return self._join(relation, 'inner', left_on, right_on)

    def left_outer_join(self, relation : 'Relation', left_on=None,
        right_on=None) -> 'Relation':
        """
        Returns a new Relation representing the left outer join operation.

        If left_on and right_on are not provided, the Relations will be joined
        based on all the columns that the two Relations have in common.

        Args:
            left_on (str): A column in the current Relation to join on.
            right_on (str): A column in the provided Relation to join on.
        """
        return self._join(relation, 'left', left_on, right_on)
    
    def right_outer_join(self, relation : 'Relation', left_on=None,
        right_on=None) -> 'Relation':
        """
        Returns a new Relation representing the right outer join operation.

        If left_on and right_on are not provided, the Relations will be joined
        based on all the columns that the two Relations have in common.

        Args:
            left_on (str): A column in the current Relation to join on.
            right_on (str): A column in the provided Relation to join on.
        """
        return self._join(relation, 'right', left_on, right_on)
    
    def full_outer_join(self, relation : 'Relation', left_on=None,
        right_on=None) -> 'Relation':
        """
        Returns a new Relation representing the full outer join operation.

        If left_on and right_on are not provided, the Relations will be joined
        based on all the columns that the two Relations have in common.

        Args:
            left_on (str): A column in the current Relation to join on.
            right_on (str): A column in the provided Relation to join on.
        """
        return self._join(relation, 'outer', left_on, right_on)

    def union(self, relation : 'Relation'):
        """
        Returns a new Relation representing the union operation.
        """
        return _init_relation_from_df(pd.concat([self._table,
            relation._table]))

    def intersection(self, relation : 'Relation') -> 'Relation':
        """
        Returns a new Relation representing the intersection operation.
        """
        return _init_relation_from_df(pd.merge(self._table, relation._table,
            on=self._get_common_columns(relation), how='inner'))

    def difference(self, relation: 'Relation') -> 'Relation':
        """
        Returns a new Relation representing the difference operation.
        """
        return _init_relation_from_df(pd.merge(self._table, relation._table,
            how='outer', indicator=True).query('_merge == "left_only"') \
            .drop('_merge', axis=1))
    
    def _get_common_columns(self, relation : 'Relation') -> list[str]:
        """
        Returns the columns that the two relations have in common.
        """
        return list(set(self.get_columns()) & set(relation.get_columns()))
    
    def _join(self, relation : 'Relation', how : str, left_on,
        right_on) -> 'Relation':
        """
        Returns a new Relation representing the specified type of join
        operation.
        """
        if left_on is None and right_on is None:
            df = pd.merge(self._table, relation._table, how=how,
                on=self._get_common_columns(relation))
        else:
            df = pd.merge(self._table, relation._table, how=how,
                left_on=left_on, right_on=right_on)
        return _init_relation_from_df(df)
