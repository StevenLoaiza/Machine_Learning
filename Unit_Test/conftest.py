# content of conftest.py
import pytest
import pandas as pd

#create a fixture for a test module

@pytest.fixture(scope="module")
def sample_data():
  #create a data set
  data ={'key':[1,2,3,4,5,6,6,7,8,9,10]
         'value': ['a','a','a','a','a','a','a','a','a','a']
          }
  df=pd.DataFrame(data,columns=[]
  return(df)
