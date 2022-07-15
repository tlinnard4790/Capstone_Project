

from ast import And
from re import L
from this import d
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from math import fsum
import seaborn as sns
import emails
import reports
import os


# This function will print out a dataframe consisting of only the Order_Date, Subtotal, Shipping_Charge, Tax_Charged,
# and Total_Charged columns. It provides an easier grid to view instead of looking at the 21 columns within Excel.
# The '$' signs have been removed to make it easier to call the float instead of a string

def source_frame():
    import pandas as pd
    import emails
    import reports

    df = pd.read_csv('amazon_spending.csv').fillna('-------')
    df["Total_Charged"] = df["Total_Charged"].str.replace('$','', regex=True).astype(float)
    df["Tax_Charged"] = df["Tax_Charged"].str.replace('$', '', regex=True).astype(float)
    source = df[['Order_Date','Subtotal','Shipping_Charge','Tax_Charged','Total_Charged']]
     
    reports.generate("report.pdf", "YoY Amazon Spending", "Report.", source)
    sender = "tlinnard4790@gmail.com"
    receiver = "tlinnard4790@gmail.com".format(os.environ.get('USER'))
    subject = "YoY Amazon Spending"
    body = "Hi\n\nI'm sending an attachment regarding your Amazon spending."
    message = emails.generate(sender, receiver, subject, body, "/New.pdf")
    #emails.send(message)  

    return source
     
source_frame()


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
print(df.groupby(['Category']).sum())

plt.plot(df.Category.astype(str))
plt.plot(df.Item_Total.astype(str))
plt.show()



# This function plots a ling graph showcasing my total spending for each year 

def yearly_spending():
    import matplotlib.pyplot as plt
    import seaborn as sns

    df = pd.read_csv('amazon_spending.csv')
    df["Total_Charged"] = df["Total_Charged"].str.replace("$", "", regex=True).astype(float)
    df["Year"] = pd.DatetimeIndex(df['Order_Date']).year
    yoy_cost = df.groupby(["Year"], as_index=False).sum()
    print(yoy_cost)
    fig, ax = plt.subplots(figsize=(16,7))

    sns.set_theme()
    sns.lineplot(x=yoy_cost["Year"], y=yoy_cost["Total_Charged"], palette="mako")
    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 5})
    plt.title("How much did I spend each year?")
    plt.ylabel("Total Cost ($)")

yearly_spending()




# This function plots a bar graph showcasing the total spending for each month over the years, so each year for the month of January, etc

def monthly_spending():
    import matplotlib.pyplot as plt
    import seaborn as sns

    df = pd.read_csv('amazon_spending.csv')
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    df['Month'] = pd.DatetimeIndex(df['Order_Date']).month
    df["Total_Charged"] = df["Total_Charged"].str.replace("$", "", regex=True).astype(float)
    monthly_cost = df.groupby(["Month"], as_index=False).sum()
    print(monthly_cost)
    

    sns.set()
    fig, ax = plt.subplots(figsize=(16,7))
    sns.set_theme()
    sns.set_style("darkgrid")
    sns.barplot(x=monthly_cost["Month"], y=monthly_cost['Total_Charged'], palette="flare")
    plt.ylabel("Total Cost ($)")
    plt.title("How much did I spend each month?")

monthly_spending()





#This function plots a line graph showcasing the total cost of each order since the creation of my Amazon account


def all_orders():
    import matplotlib.pyplot as plt
    import seaborn as sns

    df = pd.read_csv('amazon_spending.csv')
    df["Total_Charged"] = df["Total_Charged"].str.replace("$", "", regex=True).astype(float)

    fig, ax = plt.subplots(figsize=(16,7))
    sns.lineplot(x=df['Order_Date'], y=df["Total_Charged"], palette="Blues")
    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
    plt.ylabel("Total Cost ($)")
    plt.xlabel('Order Date')
    plt.xscale('linear')
    plt.title("Cost of Amazon orders over the years")

all_orders()
