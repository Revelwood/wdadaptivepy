# How to Retrieve All Sheets

`get_all` calls Adaptive's `exportSheets` method and returns every sheet defined
in the instance — modeled, standard, and cube sheets — including incomplete and
user-assigned sheets.

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

## Step 4: Use the get_all function

```py
all_sheets = adaptive.sheets.get_all()
```

## Step 5: Display Results

```py
pprint.pprint(all_sheets)
```

## Example of output

Each sheet is returned as its matching type — `ModeledSheet`, `StandardSheet`,
or `CubeSheet` — all sharing the common `id`, `name`, `code`, `description`,
`is_global`, and `recalculate_on_demand` attributes.

```py
[
  ModeledSheet(
    id=1,
    name='Personnel',
    code='Personnel',
    description='Personnel Sheet',
    is_global=False,
    recalculate_on_demand=True
  ),
  StandardSheet(
    id=6,
    name='Model Summary',
    code='',
    description='Configurable Model Summary Sheet',
    is_global=True,
    recalculate_on_demand=False
  ),
  CubeSheet(
    id=17,
    name='Expense Cube',
    code='ExpenseCube',
    description='',
    is_global=True,
    recalculate_on_demand=True
  )
]
```

!!! note
    `is_global` and `recalculate_on_demand` map to Adaptive's `isGlobal` and
    `recalculateOnDemand` XML attributes, which use `"0"`/`"1"` for
    false/true. They are returned by `exportSheets` even though they are not
    listed in Adaptive's published documentation for the method.

## Filtering the results

`get_all` returns a `MetadataList`, so you can narrow the results by sheet type
or by any attribute:

```py
# Only modeled sheets
modeled_sheets = [s for s in all_sheets if isinstance(s, adaptive.sheets.ModeledSheet)]

# Look up a single sheet by name
personnel = all_sheets.get_member(name="Personnel")
```

!!! note
The list endpoint returns only the light attributes above. To retrieve a
sheet's columns (modeled) or dimensions and users (cube), pass its `id` to
[Get Sheet Definition](Sheets.GetDefinition.md).
