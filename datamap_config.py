
#dictionary holds the parsing information for the source data excel file
srcParse = {
    'sheet_name': 'MASTER',
    'header': 9,
    'cols': 'A:AF'
}

# Dictionary maps the columns in the source data to the associated table in the database.  
# Columns in the list pertaining to the dataframe are in the order of the database columns
tableCols = {

#db table name: dataframe column name
    'details': ['LEASE NO.', 'PLOTTED', 'GRANTEE', 'SALE DATE',
                'EFFECTIVE DATE OF LEASE', 'EXPIRATION DATE', 'ACRES', 'COUNTY', 'ST',
                'STATUS/COMMENTS', 'EXPIRATION YEAR', 'TOWNSHIP', 'RANGE',
                'DESCRIPTION I', 'DESCRIPTION II', 'DESCRIPTION III'],

    'sale_info': ['LEASE NO.', 'PARCEL NO',
                  'DUE AT SALE', 'DUE AFTER SALE (REFUNDED)', 'TOTAL  PAID', 'AMOUNT OF RENTAL'],

    'investment': ['LEASE NO.', 'YEARS RENEWED', ' RENTALS PAID UP TO DATE',
                   'TOTAL INVESTMENT (BONUS + RENTALS)', 'Estimated Bonus $/Acre'],

    'interest': ['LEASE NO.', 'UA %',
                 'RA%', 'KA%'],

    'recording': ['LEASE NO.', 'RECORDED LEASE  ', 'DATE FILED (OVERRIDE)',
                  '% OF OVERRIDES', 'Assignment of ORRI'],
}
