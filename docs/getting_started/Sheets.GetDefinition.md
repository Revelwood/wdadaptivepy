# How to Retrieve a Sheet Definition

`get_modeled_definition` and `get_cube_definition` call Adaptive's
`exportSheetDefinition` method and return the full definition of a single
modeled or cube sheet, including its columns (modeled) or its dimensions,
levels, accounts, time configuration, and users (cube).

## Step 1: Import Adaptivepy and pretty print (to show results)

```py
from wdadaptivepy import AdaptiveConnection
import pprint
```

## Step 2: Set up your connection parameters

```py
username = ""  # Provide your username
password = ""  # Provide your password
```

## Step 3: Connect to your adaptive instance

```py
adaptive = AdaptiveConnection(
    login=username,
    password=password
    )
```

## Step 4: Choose how to identify the sheet

`get_modeled_definition` and `get_cube_definition` each accept the sheet in
three forms:

- **A sheet object** — a `ModeledSheet` (for `get_modeled_definition`) or a
  `CubeSheet` (for `get_cube_definition`), for example one returned by
  [Get All Sheets](Sheets.GetAll.md). Its `id` is used; a `ValueError` is
  raised if the object has no `id`.
- **An `int`** — used directly as the sheet's internal ID.
- **A `str`** — treated as the sheet's `code` and looked up across all sheets
  via `exportSheets`. A `ValueError` is raised if no sheet has that code.

## Modeled sheets

### Step 5: Get the modeled sheet definition

```py
# By object (e.g. from get_all)
personnel = adaptive.sheets.get_all().get_member(name="Personnel")
personnel_definition = adaptive.sheets.get_modeled_definition(personnel)

# By internal id
personnel_definition = adaptive.sheets.get_modeled_definition(11)

# By code
personnel_definition = adaptive.sheets.get_modeled_definition("Personnel")
```

### Step 6: Work with the columns

Columns are also grouped by type on the sheet (`levels_columns`,
`text_columns`, `dimension_columns`, `date_columns`, `number_columns`, and so
on). Use the `columns` property to iterate every column in the sheet's
original left-to-right order:

```py
# In original sheet order
for column in personnel_definition.columns:
    print(column.order, column.code, column.name, column.required)

# Access a specific column group
for dimension_column in personnel_definition.dimension_columns:
    print(dimension_column.name, [v.name for v in dimension_column.values])
```

!!! note
Each column carries its 0-based position within the sheet on `column.order`,
and `columns` returns the columns sorted by it. The order is derived from the
document order of the `exportSheetDefinition` response (it is not a distinct
Adaptive XML attribute), so it is populated only when the sheet is parsed from
that response.

## Cube sheets

### Step 5: Get the cube sheet definition

```py
# By internal id
summary_cube = adaptive.sheets.get_cube_definition(24)

# By code
summary_cube = adaptive.sheets.get_cube_definition("SummaryCube")

# By object (e.g. from get_all)
expense_cube = adaptive.sheets.get_all().get_member(name="Expense Cube")
expense_cube_definition = adaptive.sheets.get_cube_definition(expense_cube)
```

### Step 6: Display Results

```py
pprint.pprint(summary_cube)
```

### Example of output

```py
CubeSheet(id=24,
          name='Summary Cube',
          code='SummaryCube',
          description='',
          is_global=False,
          strata_id=1,
          horizontal_axis=-3,
          vertical_axis=[-2],
          dimensions=[
              CubeSheetDimension(
                  id=3,
                  name='Company',
                  values=[ColumnValue(id=35, name=None)]
              )
          ],
          levels=[CubeSheetLevels(levels=[LevelRef(id=1)])],
          accounts=[
              CubeSheetAccounts(accounts=[CubeSheetAccount(id=455, code='', is_assumption=False)])
          ],
          time=[CubeSheetTime(initial_balance=True, visible_time_stratum_codes='month')],
          users=[CubeSheetUsers(is_excluded_from_workflow=True, users=[CubeSheetUser(id=11)])])
```

!!! note
`get_modeled_definition` and `get_cube_definition` return `None` when the
resolved `id` matches no sheet of that type. They instead raise a `ValueError`
when a sheet object has no `id`, or when a `code` string matches no sheet.
