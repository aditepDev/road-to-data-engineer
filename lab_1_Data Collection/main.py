import requests
import json
import pandas as pd
from DatabaseConnect import connect


def apiGetData():
    url = "https://de-training-2020-7au6fmnprq-de.a.run.app/currency_gbp/all"

    r = requests.get(url)
    result = r.json()
    conversion_rate = pd.DataFrame.from_dict(result).reset_index().rename(columns={
        "index": "date"})
    print(conversion_rate.describe())
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


if __name__ == '__main__':
    retail = findData()
    conversion_rate = apiGetData()
    print(retail)
    print(conversion_rate)
