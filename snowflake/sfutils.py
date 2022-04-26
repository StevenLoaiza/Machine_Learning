import re
import yaml
import snowflake.connector
from snowflake.connector.pandas_tools import pd_writer
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import os
import pandas as pd


def return_connector_engine(**kwags):
    """Returns snowflake connector and creates sqlalchemy engine
    """
    sf_ = snowflake.connector.connect(**kwags)
    eng_ = create_engine(URL(**kwags))
    return sf_, eng_


class SnowflakeSetup:
    """ Class for Interactive queries on SF"""
    def __init__(self, snowflake_config, override_database=None, override_schema=None):
        """
        Args:
            snowflake_config: configuration dictionary
            override_database: Change sf database from the one set in config
            override_schema:  Change sf schema from the one set in config
        """
        # Set OS environments to override config
        if override_schema:
            os.environ['SCHEMA'] = override_schema
        if override_database:
            os.environ['DATABASE'] = override_database

        # Place holder for error handling when authentication fails
        try:
            ctx, engine = return_connector_engine(snowflake_config)
        except snowflake.connector.errors.DatabaseError as sf_err:
            raise sf_err

        self.cur = ctx.cursor()
        self.engine = engine

    @staticmethod
    def prep_query(txt):
        """ Remove comments and split query into list
        Args:
            txt: text of queries
        Returns:
            list of formatted queries
        """
        # Comment removal
        query_no_comments = re.sub(r'(--.*)|((/\*)+?[\w\W]+?(\*/)+)', '', txt)
        # Separate by semi colon
        queries = re.split('\n\\s*;', query_no_comments)
        # Remove Whitespace queries (empty)
        queries = [q for q in queries if re.search('\\w', q)]

        return queries

    @staticmethod
    def check_lowercase(list_):
        """Returns boolean if lowercase element is found in the list"""
        lc = re.compile('[a-z]+')
        new_list = list(filter(lc.match, list_))

        return len(new_list) > 1

    def read_sf_dataframe(self, sql_):
        """ Read SF table as pandas DF
        Args:
            sql_: SF query
        Returns:
            Pandas DF
        """
        self.cur.execute(sql_)

        return self.cur.fetch_pandas_all()

    def run_sf_sql(self, sql_):
        """ Executes SF Query
        Args:
            sql_: sql_: SF query
        """
        self.cur.execute(sql_)

    def run_sf_multi_sql(self, txt):
        """ Iterates through list of queries.
        The semi-colon should be on its own line inorder to split the queries.
        Args:
            txt: text of queries
        """
        queries = self.prep_query(txt)

        for q in queries:
            self.run_sf_sql("""{}""".format(q))

    def write_to_sf(self, df_, table_name, if_exists_='fail'):
        """ Write Pandas df to snowflake

        See pandas to_sql() method for parameter definitions
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        """
        # check for lowercase column name - snowflake is case sensitive
        if self.check_lowercase(list(df_.columns)):
            print('Snowflake is case-sensitive, setting column names uppercase')
            df_.columns = [a.upper() for a in df_.columns]

        df_.to_sql(table_name, self.engine, index=False, method=pd_writer, if_exists=if_exists_)


if __name__ == '__main__':
    # Dummy Data
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

    # Init
    config = yaml.load(open('./config/config.yml', 'rb'), Loader=yaml.FullLoader)
    sf_connect = SnowflakeSetup(**config['snowflake'])

    # Upload
    sf_connect.write_to_sf(df, 'testing', 'replace')

