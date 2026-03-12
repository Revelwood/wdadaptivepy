# How to Get Data

## Sample Script

```py
from wdadaptivepy import AdaptiveConnection


adaptive = AdaptiveConnection(
    login="your.adaptive@user.name",
    password="YourAdaptivePa$$w0rd!",
)

query = (
    adaptive.data.query_data()              # Initializes the query
    .add_account_filter("Assets")           # Adds an Account filter to the query
    .add_level_filter("Total Company")      # Adds a Level filter to the query
    .set_version_filter("Default Version")  # Adds a Version filter to the query
    .set_time_filter("01/2026", "03/2026")  # Adds a Time filter to the query
)

data = query.get_data()
print(data)
```

## Sample Output

```json
[
  {
    "Account Code": "1110_CA_PettyCash",
    "Account Name": "1110 Petty Cash",
    "Amount": 200.0,
    "Level Code": "BC - 91",
    "Level Name": "Sales - North",
    "Period Code": "02/2026"
  },
  {
    "Account Code": "1110_CA_PettyCash",
    "Account Name": "1110 Petty Cash",
    "Amount": 300.0,
    "Level Code": "BC - 91",
    "Level Name": "Sales - North",
    "Period Code": "03/2026"
  }
]
```

