## COMP3005 RelaX

A simple text-based relational algebra calculator.

### Setup and Usage

Clone the repository and install the required packages using: `pip install -r requirements.txt`.

Enter your query into `input.txt`. Ensure proper formatting is followed ([example query below](#example-query)).

Run `main.py` using `python3 main.py`.

The program will output the inputted relations and query from `input.txt`, and the result of the query.

### Supported Operations

| Operator | Examples |
| -------- | -------- |
| `σ` selection | `σ name=='Bob' Employee` `σ id>=3 Employee` <br> NOTE: the `==` to check for equivalence |
| `π` projection | `π name Employee` `π id,name Employee` |
| `⨝` inner join | `Employee ⨝ Department` `Student ⨝ id=sid Takes` |
| `⟕` left outer join | `Employee ⟕ Department` `Student ⟕ id=sid Takes` |
| `⟖` right outer join | `Employee ⟖ Department` `Student ⟖ id=sid Takes` |
| `⟗` full outer join | `Employee ⟗ Department` `Student ⟗ id=sid Takes` |
| `∪` union | `Employee ∪ GradStudent` |
| `∩` intersection | `Employee ∩ GradStudent` |
| `-` difference | `Employee - GradStudent` |

### Example Query

```
student = {
id, name, email, city
1, 'alex', 'a@c', 'ottawa'
2, 'john', 'j@c', 'ottawa'
3, 'makaela', 'm@c', 'toronto'
}

takes = {
sid, cid, mark
1, 1, 9
1, 2, 10
1, 3, 8
2, 1, 8
}

course = {
id, title, hours
1, 'math', 1
2, 'physics', 1
3, 'dbms', 1
}

(π name student) - (π name (student ⨝ id=sid takes))
```

#### Output
```
RELATION(S) ------------------------------------------------------------------------------------

student                                 takes                       course                      
┌──────┬─────────┬─────────┬─────────┐  ┌───────┬───────┬────────┐  ┌──────┬─────────┬─────────┐
│   id │ name    │ email   │ city    │  │   sid │   cid │   mark │  │   id │ title   │   hours │
├──────┼─────────┼─────────┼─────────┤  ├───────┼───────┼────────┤  ├──────┼─────────┼─────────┤
│    1 │ alex    │ a@c     │ ottawa  │  │     1 │     1 │      9 │  │    1 │ math    │       1 │
├──────┼─────────┼─────────┼─────────┤  ├───────┼───────┼────────┤  ├──────┼─────────┼─────────┤
│    2 │ john    │ j@c     │ ottawa  │  │     1 │     2 │     10 │  │    2 │ physics │       1 │
├──────┼─────────┼─────────┼─────────┤  ├───────┼───────┼────────┤  ├──────┼─────────┼─────────┤
│    3 │ makaela │ m@c     │ toronto │  │     1 │     3 │      8 │  │    3 │ dbms    │       1 │
└──────┴─────────┴─────────┴─────────┘  ├───────┼───────┼────────┤  └──────┴─────────┴─────────┘
                                        │     2 │     1 │      8 │                              
                                        └───────┴───────┴────────┘                              

QUERY ------------------------------------------------------------------------------------------

(π name student) - (π name (student ⨝ id=sid takes))

RESULT -----------------------------------------------------------------------------------------
           
┌─────────┐
│ name    │
├─────────┤
│ makaela │
└─────────┘
```

NOTE: Use the fewest brackets necessary to write your query.

For example, if you wanted to do a projection of column 'id' your query should look like: `π id relation_name`. It SHOULD NOT look like `(π id relation_name)` or `π id (relation_name)`.
