import pymysql
from datamap_config import tableCols
from .sql_interpol import (
    schemasql
)

def get_db_connection(cfg):
    retval = db_connection.cursor(**cfg)
    return retval


def __execute_sql(db_conn, sql_queries, cfg=None):
    cur = db_conn.cursor()
    for query in sql_queries:
        cur.execute(query)
    return


####### Get Column Names from DB function ##########

def get_db_column_names(table_name, db_connection):
    ''' This function will get column names from desired table in its ordinal position by passing sql query.'''

    #sql statement to get column names
    schemasql.format(**table_name)

    # cursor = db_connection.cursor()
    # CALL get_db_connection instead to reduce repetive calling, DRY principle way of writing code.

    #executing sql statement and then fetching data from cursor
    cursor.execute(schemasql)
    dbcolumns = cursor.fetchall()

    #retreiving column name from cursor along with ordinal position
    sql_col_name = []

    for item in dbcolumns:
        # item 3 is where col name is found in data fetch object
        sql_col_name.append(item[3])

    #joining list of columns by comma and converting to string
    stringcolnames = ','.join(sql_col_name)

    print('Column Names in Database for Table {}'.format(table_name))
    print('----------------')

    return stringcolnames

####### Generate Insert Sql String ##########


def generateInsertString(table_name, db_connection, update=True):
    '''This function will generate an insert SQL statement
        The file where the function is being called must be connected to a database for function to execute,
        the connection object must be passed in to this function
    '''

    cols = getDBcolumnNames(table_name, db_connection)

    #initalizing empty string
    valueplaceholders = ''

    #for loop to generate placeholder %s
    #splitting string column names by comma to get number of columns
    for i in range(0, len(getDBcolumnNames(table_name, db_connection).split(','))):
        valueplaceholders += '%s,'
    # taking string minus 1 position to remove extra comma
    valueplaceholders = valueplaceholders[0:len(valueplaceholders)-1]

    #final insert string, placeholders will table name, columns from db, and values from datasource/dataframe
    insert_sql = 'INSERT INTO {}({}) VALUES ({})'.format(
        table_name, cols, valueplaceholders)

    # if update is false, then this code to check for duplicate keys and update will not be added to sql string
    if update:
        updatestring = []
        for col in getDBcolumnNames(table_name, db_connection).split(','):
            updatestring.append('{} = %s'.format(col))

        updatestring = ','.join(updatestring)

        insert_sql = insert_sql + ' ON DUPLICATE KEY UPDATE ' + updatestring

    return insert_sql


def insertUpdateToTable(source, table_name, db_connection):
    '''This function will take source data as a Pandas Dataframe and a table name passed as a string
    The table name will filter the source data set to columns mapped to the database columns in the config dictionary
    The function will also return failed row numbers for troubeshooting post insert
    The function will only work when database connection is established, which must be passed in
    '''

    #creating local instance of cursor to avoid errors from using global cursor in main script
    cursor = db_connection.cursor()

    #empty array to store index number that fails to enter
    failedindexes = []

    sql = generateInsertString(table_name, db_connection)

    for index in range(0, source[tableCols[table_name]].shape[0]):

        #storing values for each row in dataframe as list
        #will pass this list into cursor execute function
        rowvalues = list(source[tableCols[table_name]].iloc[index].values)

        #block of nested for loops with take row values from dataframe and append them to blank list twice.
        #values are appended twice to execute insert statment with on duplicate key clause
        values = []
        for i in range(0, 2):
            for value in rowvalues:
                values.append(value)

        try:
            cursor.execute(sql, values)

            #committing to database every 500 inserts
            if index % 500 == 0:
                print('committing to db - {} records inserted'.format(index))
                db_connection.commit()

        except Exception as e:
            print('error occured at index {}'.format(index))
            print(e)
            source[tableCols[table_name]].iloc[index]
            failedindexes.append(index)
    db_connection.commit()

    #closing cursor after end of the full insert, this is to prevent global cursor object
    cursor.close()
    return failedindexes

    #closing cursor after end of the full insert, this is to prevent global cursor object
    cursor.close()
    return failedindexes


def batchInsert(source, table_name, db_connection):
    '''This function will take source data as a Pandas Dataframe and a table name passed as a string
    The table name will filter the source data set to columns mapped to the database columns in the config dictionary
    The function will bulk insert values, which will only work for initial loading of truncated tables. 
    Updates will not work due to bug in executemany function 
    The function will only work when database connection is established, which must be passed in
    '''

    #creating local instance of cursor to avoid errors from using global cursor in main script
    cursor = db_connection.cursor()

    #empty array to store index number that fails to enter
    failedindexes = []

    sql = generateInsertString(table_name, db_connection, update=False)

    #converting sliced pandas dataframe to list of values with pandas functions values to list
    manyvalues = source[tableCols[table_name]].values.tolist()

    try:
        #execute many will bulk insert values from dataframe
        cursor.executemany(sql, manyvalues)

        #committing to db after bulk insert
        db_connection.commit()

    except Exception as e:
        print(e)

    #closing cursor after end of the full insert, this is to prevent global cursor object
    cursor.close()


