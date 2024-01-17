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

    def _get_common_columns(self, relation : 'Relation') -> list[str]:
        """
        Returns the columns that the two relations have in common.
        """
        return list(set(self.get_columns()) & set(relation.get_columns()))

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
    
    def projection(self, columns : list[str]):
        """
        Returns a new Relation representing the projection operation using the
        given columns.
        """
        return _init_relation_from_df(self._table[columns])

    # FIXME: can condense this
    def inner_join(self, relation : 'Relation', left_on=None, right_on=None):
        """
        Returns a new Relation representing the inner join operation.

        If left_on and right_on are provided...
        """
        if left_on is None and right_on is None:
            df = pd.merge(self._table, relation._table,
                on=self._get_common_columns(relation), how='inner')
        else:
            df = pd.merge(self._table, relation._table,
                left_on=left_on, right_on=right_on, how='inner')
        return _init_relation_from_df(df)

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
