import pandas as pd
from datamap_config import srcParse

# Import Source Data & Clean
srcData = pd.read_excel('Source Data - Excel File/Master - BLM Leases.xlsx',
                        header=srcParse['header'], usecols=srcParse['cols'])

# Dropping Nulls from Lease No.
cleanData = srcData.dropna(subset=['LEASE NO.', 'COUNTY', 'ST'], how='all')

# Converting date fields to datetime, then converting to string in yyyy-mm-dd format for sql
cleanData["SALE DATE"].apply(lambda x: x.strftime(
    '%Y/%m/%d') if pd.notnull(x) else '')

#filtering column list with 'date' in name
datecols = list(filter(lambda x: 'date' in x.lower(), cleanData.columns))

for col in datecols:
    try:
        cleanData[col] = pd.to_datetime(cleanData[col])
        cleanData[col] = cleanData[col].apply(
            lambda x: x.strftime('%Y/%m/%d') if pd.notnull(x) else '')
        #cleanData[col] = cleanData[col].apply(lambda x: x.date())
    except:
        print(col + " failed")

### Converting Nan's to None to avoid error inserting into SQL
#where function is find and replace where the condition is false. replacing pandas nulls with nones for sql injection
cleanData = cleanData.where(pd.notnull(cleanData), None)

#running where function again to convert blank strings for dates and other fields to be nones
#noticed after initial runs, dates with blank strings instead of nones would output date of 0000-00-00
cleanData = cleanData.where(cleanData != '', None)
