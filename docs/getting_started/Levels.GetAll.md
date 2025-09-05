# How to Retrieve All Levels

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
all_levels = adaptive.levels.get_all()
```
## Step 5: Display Results
```py
pprint.pprint(all_levels)
```
## Example of output
```py
 Level(id=207,
       code='BC - 75',
       name='Production',
       display_name='Production',
       currency='INR',
       publish_currency=None,
       short_name='',
       available_start=None,
       available_end=None,
       is_importable=None,
       workflow_status=None,
       is_elimination=False,
       is_linked=False,
       has_children=None,
       description='')
```