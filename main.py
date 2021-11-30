import importlib

import pymysql
from db_config import mysql_config
from datamap_config import tableCols
import etl
from dataclean import cleanData #importing cleaned dataframe


# Reloads
importlib.reload(etl)

if __name__ == "__main__":
    ## Connect to DB start Sql load
    db = pymysql.connect(host=mysql_config['host'], user=mysql_config['user'],
                        password=mysql_config['password'], database=mysql_config['database'])


    cursor = db.cursor()
    cursor.execute('Show tables')
    cursor.fetchall()

    ##### Load Details Table #####
    for table in tableCols.keys():

        #checking count of table records, if records exist then update, if no records exist, batch insert
        cursor = db.cursor()
        cursor.execute('Select count(1) from {}'.format(table))
        recordsintable = cursor.fetchone()
        recordsintable = recordsintable[0]

        if recordsintable == 0:
            etl.batchInsert(cleanData, table, db)
            db.commit()
        # else:
        #     etl.insertUpdateToTable(cleanData, table, db) #time consuming process to insert one by one when checking for duplicate keys


    db.close()
    




