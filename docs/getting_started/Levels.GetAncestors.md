# How to Retrieve Level Ancestors

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
## Step 5: Choose the level
```py
level = adaptive.levels[10]
```
## Step 6: Get ancestors
```py
ancestors = level.get_ancestors()
```
## Step 7: Display results
```py
pprint.pprint(ancestors)
```
## Example of output
```
[Level(id=165,
       code='BC - 111',
       name='United States',
       display_name='United States',
       currency='USD',
       publish_currency=None,
       short_name='US',
       available_start=None,
       available_end=None,
       is_importable=None,
       workflow_status=None,
       is_elimination=False,
       is_linked=False,
       has_children=True,
       description=''),
 Level(id=164,
       code='BC - 70',
       name='Operations - company A',
       display_name='Operations - company A',
       currency='USD',
       publish_currency=None,
       short_name='Ops',
       available_start=None,
       available_end=None,
       is_importable=None,
       workflow_status=None,
       is_elimination=True,
       is_linked=False,
       has_children=True,
       description=''),
 Level(id=201,
       code='BC - 52',
       name='Company A (100% owned)',
       display_name='Company A (100% owned)',
       currency='USD',
       publish_currency=None,
       short_name='Co.A',
       available_start=None,
       available_end=None,
       is_importable=None,
       workflow_status=None,
       is_elimination=False,
       is_linked=False,
       has_children=True,
       description=''),
 Level(id=1,
       code='Total Company',
       name='Total Company',
       display_name='Total Company',
       currency='USD',
       publish_currency=None,
       short_name='TotalCo',
       available_start=None,
       available_end=None,
       is_importable=None,
       workflow_status=None,
       is_elimination=True,
       is_linked=False,
       has_children=True,
       description='')]
```