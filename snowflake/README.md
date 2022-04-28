# Snowflake Connector

# Example
Navigate to `Machine_Leaning/snowflake` directory, update configuration yaml with appropriate credentials before following along.
```python
import yaml
config = yaml.load(open('./config.yaml', 'rb'), Loader=yaml.FullLoader)
from sfutils import *
sf_connect = SnowflakeSetup(config['snowflake'])
ctx = sf_connect.ctx

# Example from SnowFlake (Will Fail)
from snowflake.connector.pandas_tools import write_pandas
import pandas
df = pandas.DataFrame([('Mark', 10), ('Luke', 20)], columns=['name', 'balance'])
success, nchunks, nrows, _ = write_pandas(ctx, df, 'acustomers')

# Using Snowflake Util will run without errors
sf_connect.write_to_sf(df, 'acustomers')
```
