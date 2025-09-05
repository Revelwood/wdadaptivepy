# How to Get Data

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
## Step 4: Define the version

```py
version = adaptive.versions.get_all()[0]  # adaptive.versions.Version(code="Actuals")
```
## Step 5: Define the account and the account filter
```py
accounts = adaptive.accounts.get_all()
account_filter = AccountFilter(account=accounts[0].get_descendents())
```
## Step 6: Define the time and time filter
```py
adaptive_time = adaptive.time.get_all()
start_period = [period for period in adaptive_time[0].period if period.code == "01/2020"][0]
end_period = [period for period in adaptive_time[0].period if period.code == "01/2026"][0]
time_filter = TimeFilter(start=start_period, end=end_period)
```

## Step 7: Define the data filter and then get the data
```py
data_filter = ExportDataFilter(accounts=account_filter, time=time_filter)
data = adaptive.data.get_data(version=version, data_filter=data_filter)
```
## Sample Output
```
{'Account Code': '1110_CA_PettyCash',
  'Account Name': '1110 Petty Cash',
  'Amount': 0.0,
  'Level Code': 'BC - 91',
  'Level Name': 'Sales - North',
  'Period Code': '05/2024'}
  ```