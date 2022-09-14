import pandas as pd
from datetime import datetime
import os
from vega_datasets import data

_DATA_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'source'))
_OUTPUT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'output'))


def processSourceData():
    if (not os.path.exists(_OUTPUT_DIR)):
        os.mkdir(_OUTPUT_DIR)
    dte = str(datetime.now().date())
    outputFile = os.path.join(_OUTPUT_DIR, 'export' + dte + '.csv')
    file_exists = os.path.exists(outputFile)
    if (file_exists):
        existingOutput = pd.read_csv(outputFile)
        return (existingOutput)
    sourceData = []
    for s in os.listdir(_DATA_DIR):
        if (s.endswith('.csv')):
            thisFile = os.path.join(_DATA_DIR,s)
            print('PROCESSING ' + thisFile)
            df = getDataFromFile(thisFile)
            sourceData.append(df)
        else:
            continue
    if (len(sourceData) > 1):
        result = pd.concat(sourceData)
        result.to_csv(outputFile)
        return(result)
    else:
        sourceData[0].to_csv(outputFile)
        print(sourceData[0])
        return(sourceData[0])


def getExternalSource():
    if (not os.path.exists(_DATA_DIR)):
        os.mkdir(_DATA_DIR)
    # testing with vega airports
    print('getting external data..')
    myData = data.birdstrikes()
    df = pd.DataFrame(myData)
    dte = str(datetime.now().date())
    source = os.path.join(_DATA_DIR, 'source' + dte + '.csv')
    df.to_csv(source, index=False)
    print('SOURCE FILE CREATED ' + source)
    return (df.dropna())


def getDataFromFile(filewithpath):
    df = pd.read_csv(filewithpath)
    result = transformFile(df)
    return (result)


def transformFile(df):
    df.columns = df.columns.str.lower()
    df['flight_date'] = pd.to_datetime(df['flight_date'], dayfirst=True)
    df['cost__total_$'] = df['cost__total_$'].astype(float)
    df['speed_ias_in_knots'] = pd.to_numeric(df['speed_ias_in_knots'])
    df['flight_year'] = pd.DatetimeIndex(df['flight_date']).year
    return(df)


if __name__ == '__main__':
    getExternalSource()
    test = processSourceData()
    print(test)
