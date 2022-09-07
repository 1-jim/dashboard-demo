import pandas as pd
from datetime import datetime
import os
from vega_datasets import data

def testSourceGrouping():
    source = data.birdstrikes()
    df = transformData(source)
    grp = df.groupby(['origin_state'], as_index=False)['cost__total_$'].sum()
    print(grp)

def transformData(df):
    df.columns = df.columns.str.lower()
    df['flight_date'] = pd.to_datetime(df['flight_date'], dayfirst=True)
    df['cost__total_$'] = df['cost__total_$'].astype(float)
    df['speed_ias_in_knots'] = pd.to_numeric(df['speed_ias_in_knots'])
    df['flight_year'] = pd.DatetimeIndex(df['flight_date']).year
    return(df)

if __name__ == '__main__':
    testSourceGrouping()