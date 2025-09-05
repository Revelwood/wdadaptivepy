# Connecting to an Adaptive Instance

To connect to your Adaptive instance you will need to call the AdaptiveConnection function in Adpativepy

## Step 1: Import Adaptivepy
```py
from wdadaptivepy import AdaptiveConnection
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
    password=password,
    # instance_code=None,  # Optional
    # locale="en_US",  # Optional
    # caller_name="AdaptivePY",  # Optional
    # xml_api_version=40)  # Optional
```

Note that this simple example will not return anything. It is simply connecting to your instance. See other examples in the documentation to display outputs.