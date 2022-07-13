import pandas as pd
import matplotlib.pyplot as plt
import datetime
import csv
from math import fsum


# def clean_frame():
#df = pd.read_csv('amazon_spending.csv')

# # #fill empty spaces within grid to appear more appealing when viewed
#     df = df.fillna('------')

# # #remove the "$" from the Total Charged column in order to make it easier for analysis using panda math functions

#df["Total_Charged"] = df["Total_Charged"].str.replace('$','', regex=True).astype(float)
#     df["Tax_Charged"] = df["Tax_Charged"].str.replace('$', '', regex=True).astype(float)

# #print out specific columns to narrow down the data 
#     df[['Order_Date','Subtotal','Shipping_Charge','Tax_Charged','Total_Charged']]

# clean_frame()

# sum = pd.read_csv('amazon_spending.csv')
# df = pd.DataFrame(sum)
# sum.df["Total_Charged"] = df["Total_Charged"].str.replace('$','', regex=True).astype(float)

def total():
    with open('amazon_spending.csv', 'r') as f:
        spending_total = fsum(
        float(d['Total_Charged'].strip("$")) if d['Total_Charged'].strip() else 0
        for d in csv.DictReader(f) if d['Total_Charged'])
    return total

 






# df["Total_Charged"].mean()
# df["Total_Charged"].median()
# df["Total_Charged"].min()
# df["Total_Charged"].max()
# df["Total_Charged"].sum().round(2)
# df["Tax_Charged"].sum().round(2)



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
