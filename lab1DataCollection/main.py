import requests
import json
import pandas as pd
from DatabaseConnect import connect
import PathFile


def apiGetData():
    url = "https://de-training-2020-7au6fmnprq-de.a.run.app/currency_gbp/all"

    r = requests.get(url)
    result = r.json()
    conversion_rate = pd.DataFrame.from_dict(result).reset_index().rename(columns={
        "index": "date"})
    # print(conversion_rate.describe())
    return conversion_rate


def findData():
    with connect().cursor() as cursor:
        # Read a single record
        sql = "select * from online_retail"
        cursor.execute(sql)
        result = cursor.fetchall()
        retail = pd.DataFrame(result)
        retail['InvoiceTimestamp'] = retail['InvoiceDate']
        # print(retail.describe())
    return retail


def mergeDate(retail, conversion_rate):

    retail['InvoiceDate'] = pd.to_datetime(retail['InvoiceDate']).dt.date
    conversion_rate['date'] = pd.to_datetime(conversion_rate['date']).dt.date
    final_df = retail.merge(conversion_rate, how='left',
                            left_on="InvoiceDate", right_on="date")
    return final_df


def save_pandas_to_csv(dataframe, name):
    dataframe.to_csv("%s%s.csv" % (PathFile.READFILE_CSV, name), index=False)
    print("file saved!!")


def convert_rate(price, rate):
    return price * rate


def calculatorTHBPrice(final_df, swit_type=1):

    if (swit_type == 1):
        final_df['THBPrice'] = final_df['UnitPrice'] * final_df['Rate']
    if (swit_type == 2):
        final_df['THBPrice'] = final_df.apply(
            lambda x: x["UnitPrice"] * x['Rate'], axis=1)
    if (swit_type == 3):
        final_df['THBPrice'] = final_df.apply(
            lambda x: convert_rate(x["UnitPrice"], x['Rate']), axis=1)
    return final_df


if __name__ == '__main__':
    retail = findData()
    conversion_rate = apiGetData()
    final_df = mergeDate(retail, conversion_rate)
    final_df = calculatorTHBPrice(final_df, 3)
    save_pandas_to_csv(final_df, 'THBPrice')
