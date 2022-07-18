
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from PyPDF2 import PdfFileMerger
from reportlab.platypus import SimpleDocTemplate
from ast import And
from re import L
from this import d
from unittest import skip
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from math import fsum
import seaborn as sns
import emails
import os


# This function will print out a dataframe consisting of only the Order_Date, Subtotal, Shipping_Charge, Tax_Charged,
# and Total_Charged columns. It provides an easier grid to view instead of looking at the 21 columns within Excel.
# The '$' signs have been removed to make it easier to call the float instead of a string

def source_frame():
    import pandas as pd
    import emails

    df = pd.read_csv('amazon_spending.csv').fillna('-------')
    df["Total_Charged"] = df["Total_Charged"].str.replace('$','', regex=True).astype(float)
    df["Tax_Charged"] = df["Tax_Charged"].str.replace('$', '', regex=True).astype(float)
    source = df[['Order_Date','Subtotal','Shipping_Charge','Tax_Charged','Total_Charged']]
     
    # reports.generate("report.pdf", "YoY Amazon Spending", "Report.", source)
    # sender = "tlinnard4790@gmail.com"
    # receiver = "tlinnard4790@gmail.com".format(os.environ.get('USER'))
    # subject = "YoY Amazon Spending"
    # body = "Hi\n\nI'm sending an attachment regarding your Amazon spending."
    # message = emails.generate(sender, receiver, subject, body, "/New.pdf")
    # #emails.send(message)  
    df.loc[df['Total_Charged'] == df['Total_Charged'].max().round(2)]
    df.sort_values(ascending=False, by='Total_Charged').head(5)
    df.loc[df['Total_Charged'] == df['Total_Charged'].min().round(2)]

    return source

source_frame()


#Takes code from previous function source_frame and converts that DataFrame
#into and html file which is then converted to PDF file


def df_pdf(method):  
  
    import pandas as pd 
    import pdfkit

    df = pd.read_csv('amazon_spending.csv').fillna('-------')
    df["Total_Charged"] = df["Total_Charged"].str.replace('$','', regex=True).astype(float)
    df["Tax_Charged"] = df["Tax_Charged"].str.replace('$', '', regex=True).astype(float)
    source = df[['Order_Date','Subtotal','Shipping_Charge','Tax_Charged','Total_Charged']]
   
    if method == "string":

        try:
            options = {'page-size: A4','margins: 1in',}
                
            config = pdfkit.configuration(wkhtmltopdf=bytes(r"C:\Users\tanne\OneDrive\Documents\Tek Systems\Capstone Project\wkhtmltopdf\bin\wkhtmltopdf.exe", 'utf8'))
            f = open('exp.html', 'w')
            a = source.to_html()
            f.write(a)
            f.close()
    
            pdf = pdfkit.from_file('exp.html', 'amazon_spending.pdf', configuration = config)
                
            return pdf
            
        except Exception as e:
            return str(e)

    else:
        return "Failed to convert DataFrame"

df_pdf('string')




# Function provides a print return of the total of all spending starting from the origination of the account
    #This includes:
        #total cost of items before shipping and taxes
        #total cost of shipping charges
        #total cost of taxes charged
        #total amount spent overall


def totals():
    import csv
    from math import fsum


    with open('amazon_spending.csv', 'r') as f:

        reader = [x for x in csv.DictReader(f)]
        item_subtotal = fsum([float(x['Subtotal'].strip("$")) for x in reader])
        shipping_total = fsum([float(x['Shipping_Charge'].strip("$")) for x in reader])
        tax_total = fsum([float(x['Tax_Charged'].strip("$")) for x in reader])
        spending_total = fsum([float(x['Total_Charged'].strip("$")) for x in reader])

    df = pd.read_csv('amazon_spending.csv')
    df["Total_Charged"] = df["Total_Charged"].str.replace('$','', regex=True).astype(float)
    average_spent = df['Total_Charged'].mean().round(2)

    print("----------Subtotal Amount----------")
    print("$",item_subtotal, "spent before shipping costs and taxes")
    print("")
    print("----------Shipping Total Amount----------")
    print("$",shipping_total, "spent on shipping charges")
    print("")
    print("----------Total Amount of Taxes----------")
    print("$",tax_total, "spent on taxes")
    print("")
    print("----------Total Amount Spent on All Orders----------")
    print("Total amount spent: $",spending_total)
    print("")
    print("----------Average Amount Spent on All Orders----------")
    print("The average amount spent on an order was: $",average_spent)


totals()


#This function plots a line graph showcasing the total cost of each order since the creation of my Amazon account


def all_orders():

    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from matplotlib.ticker import LinearLocator
    import seaborn as sns
    import numpy as np
    import pandas as pd

    df = pd.read_csv('amazon_spending.csv')
    df["Total_Charged"] = df["Total_Charged"].str.replace("$", "", regex=True).astype(float)








    fig, ax = plt.subplots(figsize=(16,7))
    g = sns.lineplot(x=df['Order_Date'], y=df["Total_Charged"], palette="Blues")
    g.set_xticklabels(['2018','2019','2020','2021','2022'])

    ax.get_xaxis().set_major_locator(LinearLocator(numticks=5))
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator(20))
    ax.grid(visible=True, which='major', color='w', linewidth=1.0)
    sns.set_context(font_scale=1.5, rc={"lines.linewidth": 1.5})

    plt.ylabel("Total Cost ($)")
    plt.xlabel('Order Date')
    plt.title("Cost of Amazon orders over the years")
    fig.savefig('all_orders.svg')

    all_orders_svg=svg2rlg('all_orders.svg')
    renderPDF.drawToFile(all_orders_svg, "all_orders.pdf")

all_orders()



# This function plots a line graph showcasing my total spending for each year 

def yearly_spending():
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

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
    fig.savefig('yearly_spending.svg')

    yearly_spending_svg=svg2rlg('yearly_spending.svg')
    renderPDF.drawToFile(yearly_spending_svg, "yearly_spending.pdf")

yearly_spending()




# This function plots a bar graph showcasing the total spending for each month over the years, 
# so each year for the month of January, etc

def monthly_spending():
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    df = pd.read_csv('amazon_spending.csv')
    df['Month'] = pd.DatetimeIndex(df['Order_Date']).month
    df["Total_Charged"] = df["Total_Charged"].str.replace("$", "", regex=True).astype(float)
    monthly_cost = df.groupby(["Month"], as_index=False).sum()
    print(monthly_cost)
    

    sns.set()
    fig, ax = plt.subplots(figsize=(16,7))
    sns.set_theme()
    sns.set_style("darkgrid")
    g = sns.barplot(x=monthly_cost["Month"], y=monthly_cost['Total_Charged'], palette="flare")
    g.set_xticklabels(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    plt.ylabel("Total Cost ($)")
    plt.title("How much did I spend each month?")
    fig.savefig('monthly_spending.svg')

    monthly_spending_svg=svg2rlg('monthly_spending.svg')
    renderPDF.drawToFile(monthly_spending_svg, "monthly_spending.pdf")

monthly_spending()


#This function showcases the total amount spent on Amazon orders according to each day of the week


def daily_spending():

    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    df = pd.read_csv('amazon_spending.csv')
    df['Days'] = pd.DatetimeIndex(df['Order_Date']).dayofweek
    df["Total_Charged"] = df["Total_Charged"].str.replace("$", "", regex=True).astype(float)
    daily_cost = df.groupby(["Days"], as_index=False).sum()
    print(daily_cost)
    
    fig, ax = plt.subplots(figsize=(18,7))
    g = sns.barplot(x=daily_cost["Days"], y=daily_cost["Total_Charged"], palette = 'icefire')
    g.set_xticklabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    sns.set_theme()
    sns.set_style("darkgrid")
    plt.ylabel("Total Spent ($)")
    plt.title("Which Days of the Week Do I Spend The Most Money")
    ax.grid(visible=True, which='major', color='w', linewidth=1.0)
    fig.savefig('daily_spending.svg')

    daily_spending_svg=svg2rlg('daily_spending.svg')
    renderPDF.drawToFile(daily_spending_svg, "daily_spending.pdf")

daily_spending()




#This function pulls 2 columns from the "amazon_items.csv" : the Category and Item_Total
    #this function will help determine which category I have spent the most amount of money on and what I spend the most on 

def category_spending():

    import pandas as pd
    from matplotlib import pyplot as plt
    import seaborn as sns
    import textwrap

    columns = ["Category", "Item_Total"]
    df = pd.read_csv("amazon_items.csv", usecols=columns)
    df["Item_Total"] = df["Item_Total"].str.replace('$','', regex=True).astype(float)
    df = df.groupby(['Category']).sum().reset_index()
    categories = df.sort_values(by=['Item_Total'], ascending=False).head(n=12)
    print(categories)

    fig, ax = plt.subplots(figsize=(20,7))

    sns.set_theme()
    sns.set_style("darkgrid")
    sns.barplot(x=categories["Category"], y=categories['Item_Total'], palette="crest")
    labels = [textwrap.fill(label.get_text(), 12) for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, fontsize=10);
    plt.ylabel("Amount Spent per Item Category ($)")
    plt.title("Top Categories")
    fig.savefig('category_spending.svg')

    category_spending_svg=svg2rlg('category_spending.svg')
    renderPDF.drawToFile(category_spending_svg, "category_spending.pdf")

category_spending()




#This function pulls 2 columns from the "amazon_items.csv" : the Category and Item_Total
    #this function will help determine which category I have spent the most amount of money on and what I spend the most on 
    #uses the same data as the previous graph, however, it is displayed as a pie chart to show a better visual breakdown of spending


def category_spending_pie():

    import matplotlib.pyplot as plt 
    import seaborn as sns
    import pandas as pd

    #import data
    columns = ["Category", "Item_Total"] 
    df = pd.read_csv("amazon_items.csv", usecols=columns)
    df["Item_Total"] = df["Item_Total"].str.replace('$','', regex=True).astype(float)
    df = df.groupby(['Category']).sum().reset_index()
    categories = df.sort_values(by=['Item_Total'], ascending=False).head(n=12)

    colors = sns.color_palette("bright")
    plt.pie(categories['Item_Total'], labels = categories['Category'], colors=colors,
    autopct='%.0f%%', rotatelabels='true')
    plt.legend(
        loc='upper left',
        prop={'size': 10},
        bbox_to_anchor=(0.5, 2.1))
    theme = plt.get_cmap('bwr')
    fig = plt.gcf()
    plt.show()
    fig.savefig('category_spending_pie.svg', bbox_inches='tight')

    category_spending_pie_svg=svg2rlg('category_spending_pie.svg')
    renderPDF.drawToFile(category_spending_pie_svg, "category_spending_pie.pdf")

category_spending_pie()




pdf_list = ['amazon_spending.pdf', 'all_orders.pdf', 'yearly_spending.pdf', 'monthly_spending.pdf',
'daily_spending.pdf', 'category_spending.pdf', 'category_spending_pie.pdf']

merger = PdfFileMerger()

for pdf in pdf_list:
    merger.append(pdf)

merger.write("amazon_data.pdf") 
merger.close

