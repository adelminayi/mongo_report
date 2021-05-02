import os
from mongoengine import connect
from datetime import datetime


my_client = connect('test')

my_db = my_client["test"]
my_col = my_db["people"]

date_from= '2008/03/28'
date_to= '2008/03/28'
date_from = date_from.replace('/','-')+'T00:00:00.000Z'
date_to = date_to.replace('/','-')+'T23:59:59.000Z'
# print(date_from)
# print(date_to)
# -------------- working in right way ---------------
# date_from = '2008-03-22T00:00:00.000Z'
# date_to = '2008-03-22T23:59:59.000Z'

results = my_col.find(
    {'$and': [{'signup': {'$gte': date_from}}, {'signup': {'$lte': date_to}}]})

try:
    today = datetime.today()
    today = today.strftime("%d%m%y-%H%M")
    output_file = os.path.join(os.getcwd(), 'query-result-' + today + '.csv')
    if results.count() :
        # print(type(results[0]))
        with open(output_file, 'w') as reader:
            for result in results:
                reader.write(str(result)+'\n')
except:
    print(" no result found!")


