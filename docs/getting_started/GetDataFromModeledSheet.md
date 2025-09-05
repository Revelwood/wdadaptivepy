# How to Get data from Modeled Sheet

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
## Step 4: Get data from modeled sheet
### (only using required parameters)
```py
modData = adaptive.data.from_modeled_sheet(
    "MyModeledSheet",
    "Workforce Planning")
```
## Step 5: Display results
```py
pprint.pprint(modData)
```
## Sample Output
```
[{'Allocations >': '',
  'Bonus %': 'None',
  'Comments': 'My comments',
[{'Allocations >': '',
  'Bonus %': 'None',
  'Comments': 'My comments',
  'Commission Target': '',
  'End Date': '8/30/2025',
  'Health Benefits': 'Plan 1',
  'Hr/Week': '',
  'InternalID': 'S24704',
  'IsParent': '',
  'Level': 'BC - 91',
  'MA_Pay Rate': '9000.000000000',
  'Name': 'John Doe',
  'ParentID': '',
  'Pay Raise %': '15.000000000',
  'Pension Plan': 'Defined Contribution A',
  'Per': 'Hr',
  'Raise Date': '8/29/2025',
  'Residence for Tax': 'NJ - New Jersey',
  'Start Date': '8/28/2025',
  'Title': 'Account Executive'}]
```