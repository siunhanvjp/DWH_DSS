import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
from sqlalchemy import create_engine
import os

RETRIEVE = 0
INSERT = 1



def load_dbconfig(section='warehouse'):
    if st.secrets[section]:
        return st.secrets[section]
    else:
        raise Exception('Section {} not found in the secrects.toml file'.format(section))

def execute_sql(dbconfig, sql, method=None, param=None):
    
    try:
        engine = create_engine(dbconfig['service_url'])
        if method == RETRIEVE:
            return pd.read_sql(sql, engine, params=param)
        else:
            with engine.connect() as conn:
                conn.execute(sql, param) if param else conn.execute(sql)
    except Exception as error:
        print(error)
        
def prepare_df():
    dbconfig = load_dbconfig()

    get_state_fact = "SELECT * FROM state_province_fact"
    df_state = execute_sql(dbconfig, get_state_fact, method=RETRIEVE)

    get_date_dim = "SELECT * FROM date_dim"
    df_date = execute_sql(dbconfig, get_date_dim, method=RETRIEVE)

    df = pd.merge(df_state, df_date, on='date_id', how='inner')
    
    # Dynamic filtering using the list of country names
    df_stateonly = df.groupby(['state_province_id', 'state_province_code', 'state_province_name', 'country_region_name', 'province_lat', 'province_long'])[["total_sale", "product_count","order_count","total_discount"]].sum()
    df_stateonly = df_stateonly.reset_index()
    df_stateonly['average_order_sale'] = df_stateonly['total_sale'] / df_stateonly['product_count']
    
    return df_stateonly