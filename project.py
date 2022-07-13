from ast import And
from re import L
from this import d
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import csv
from math import fsum


# This function will print out a dataframe consisting of only the Order_Date, Subtotal, Shipping_Charge, Tax_Charged,
# and Total_Charged columns. It provides an easier grid to view instead of looking at the 21 columns within Excel.
# The '$' signs have been removed to make it easier to call the float instead of a string

def clean_frame():
    df = pd.read_csv('amazon_spending.csv').fillna('-------')
    df["Total_Charged"] = df["Total_Charged"].str.replace('$','', regex=True).astype(float)
    df["Tax_Charged"] = df["Tax_Charged"].str.replace('$', '', regex=True).astype(float)
    clean = df[['Order_Date','Subtotal','Shipping_Charge','Tax_Charged','Total_Charged']]
    return clean
clean_frame()


# Function provides a print return of the total of all spending starting from the origination of the account
    #This includes:
        #total cost of items before shipping and taxes
        #total cost of shipping charges
        #total cost of taxes charged
        #total amount spent overall


def totals():
    with open('amazon_spending.csv', 'r') as f:
        reader = [x for x in csv.DictReader(f)]

        item_subtotal = fsum([float(x['Subtotal'].strip("$")) for x in reader])
        shipping_total = fsum([float(x['Shipping_Charge'].strip("$")) for x in reader])
        tax_total = fsum([float(x['Tax_Charged'].strip("$")) for x in reader])
        spending_total = fsum([float(x['Total_Charged'].strip("$")) for x in reader])

        print("$",item_subtotal, "spent before shipping costs and taxes")
        print("$",shipping_total, "spent on shipping charges")
        print("$",tax_total, "spent on taxes")
        print("Total amount spent: $",spending_total)
totals()


#This function pulls 2 columns from the "amazon_items.csv" : the Category and Item_Total
    #this function will help determine which category I have spent the most amount of money on and what I spend the most on 

import pandas as pd
from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = [10.00, 5.00]
plt.rcParams["figure.autolayout"] = True
columns = ["Category", "Item_Total"]
df = pd.read_csv("amazon_items.csv", usecols=columns)
print("Contents in csv file:\n", df)
plt.plot(df.Category.astype(str))
plt.plot(df.Item_Total.astype(str))
plt.show()



# df.plot.bar(x='Order Date', y='Total Charged', rot=90, figsize=(30,20))
# plt.gcf().set_facecolor('white')

#--------------------------------------------------------------------------------------------------------#

#file = 'amazon_spending.csv'

# def main():
#     with open(file) as f:
#         reader = csv.reader(f)
#         header_row = next(reader)

#         for index, column_header in enumerate(header_row):
#             if column_header == 'Order_ID':
#                 orderIndex = index
#             if column_header == 'Shipment_Date':
#                 shipIndex = index
#             if column_header == 'Subtotal':
#                 subIndex = index
#             if column_header == 'Tax_Charged':
#                 taxIndex = index
#             if column_header == 'Total_Charged':
#                 totIndex = index
#              Else:
#                  pass


#         dates, order, sub, tax, tot = [], [], [], [], []
#         for row in reader:
#                 current_date = datetime.strptime(row[shipIndex], '%m/%d/%Y')
#                 order = row[orderIndex]
#                 sub = row[subIndex]
#                 tax = row[taxIndex]
#                 tot = row[totIndex]
#                 dates.append(current_date)
#                #order.append(order)
#                 #sub.append(sub)
#                 #tax.append(tax)
#                 #tot.append(tot)

#                 plt.style.use('seaborn')
#                 fig, ax = plt.subplots()
#                 ax.plot(dates, order, c='black', alpha=0.5)
#                 ax.plot(dates, sub, c='blue', alpha=0.5)
#                 ax.plot(dates, tax, c='red', alpha=0.5)
#                 ax.plot(dates, tot, c='red', alpha=0.5)

#                 ax.set_title(file)
#                 ax.set_xlabel('Date')
#                 fig.autofmt_xdate()
#                 ax.set_ylabel('Stock Price ($)')
#                 ax.tick_params(axis='both', which='major')
# if __name__ == "__main__":
#    main()
