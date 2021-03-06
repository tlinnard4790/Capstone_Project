import os
import re
import csv
import fpdf
import pdfkit
import smtplib
import textwrap
import numpy as np
import pass_config
import pandas as pd
import seaborn as sns
from math import fsum
import matplotlib as mpl
from email import encoders
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileMerger
from svglib.svglib import svg2rlg
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from reportlab.graphics import renderPDF
from matplotlib.ticker import LinearLocator
from email.mime.multipart import MIMEMultipart


# main function will take the final output from merge_pdf function and email the merged file to the credentials from pass_config
# utilized a separate file to store Username and Password information to keep data more secure, then call those variables
# into the sender, password, and receiver variables of main

df = pd.read_csv('amazon_spending.csv').fillna('-------')
df["Total_Charged"] = df["Total_Charged"].str.replace(
        '$', '', regex=True).astype(float)
df["Tax_Charged"] = df["Tax_Charged"].astype(str).str.replace(
        '$', '', regex=True).astype(float)


def main():

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    body = 'Amazon spending data, see attachment'
    sender = pass_config.username
    password = pass_config.password
    receiver = pass_config.username

    # regex to check for correct email or correct credentials pulled from pass_config.py
    if(re.fullmatch(regex, sender)):
        print("Valid Email")
    elif sender.startswith(pass_config):

        print("Valid Credentials")
    else:
        print("Invalid Email")

    # Basic Email formatting
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = 'Amazon Spending Data'

    message.attach(MIMEText(body, 'plain'))

    pdfname = 'amazon_data.pdf'
    binary_pdf = open(pdfname, 'rb')

    payload = MIMEBase('application', 'octate-stream', Name=pdfname)
    payload.set_payload((binary_pdf).read())

    # encode the payload which is in binary_pdf
    encoders.encode_base64(payload)
    payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    message.attach(payload)
    # start secure TLS connection
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender, password)

    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()
    print('Mail Sent')


# This function will print out a dataframe consisting of only the Order_Date, Subtotal, Shipping_Charge, Tax_Charged,
# and Total_Charged columns. It provides an easier grid to view instead of looking at the 21 columns within Excel.
# The '$' signs have been removed to make it easier to call the float instead of a string

def source_frame():
 
    max = df.loc[df['Total_Charged'] == df['Total_Charged'].max().round(2)]
    max_5 = df.sort_values(ascending=False, by='Total_Charged').head(5)
    min = df.loc[df['Total_Charged'] == df['Total_Charged'].min().round(2)]

    source = df[['Order_Date', 'Subtotal',
                 'Shipping_Charge', 'Tax_Charged', 'Total_Charged']]

    return source, max, max_5, min


source_frame()


# Takes code from previous function source_frame and converts that DataFrame
# into and html file which is then converted to PDF file


def df_pdf(method):

    source = df[['Order_Date', 'Subtotal',
                 'Shipping_Charge', 'Tax_Charged', 'Total_Charged']]

    if method == "string":

        try:
            # set configuration to path of wkhtmltopdf
            config = pdfkit.configuration(wkhtmltopdf=bytes(
                r"C:\Users\tanne\OneDrive\Documents\Tek Systems\Capstone Project\wkhtmltopdf\bin\wkhtmltopdf.exe", 'utf8'))
            f = open('exp.html', 'w')
            a = source.to_html()
            f.write(a)
            f.close()

            pdf = pdfkit.from_file(
                'exp.html', 'amazon_spending.pdf', configuration=config)

            return pdf

        except Exception as e:
            return str(e)

    else:
        return "Failed to convert DataFrame"


df_pdf('string')


# Function provides a print return of the total of all spending starting from the origination of the account
# This includes:
# total cost of items before shipping and taxes
# total cost of shipping charges
# total cost of taxes charged
# total amount spent overall


def totals():

    with open('amazon_spending.csv', 'r') as f:

        reader = [x for x in csv.DictReader(f)]
        item_subtotal = fsum([float(x['Subtotal'].strip("$")) for x in reader])
        shipping_total = fsum(
            [float(x['Shipping_Charge'].strip("$")) for x in reader])
        tax_total = fsum([float(x['Tax_Charged'].strip("$")) for x in reader])
        spending_total = fsum(
            [float(x['Total_Charged'].strip("$")) for x in reader])

    df = pd.read_csv('amazon_spending.csv')
    df["Total_Charged"] = df["Total_Charged"].str.replace(
        '$', '', regex=True).astype(float)
    average_spent = df['Total_Charged'].mean().round(2)
# create pdf
    pdf = fpdf.FPDF()
# add page to new pdf file
    pdf.add_page()
    pdf.set_font("Arial", "U", size=18)  # font
    pdf.cell(200, 30, txt='Subtotal Amount ($)                                                                    ',
             ln=3, align="L")
# write to pdf which need to be strings and pull variables from above code
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=str(item_subtotal), ln=1, align="L")
    pdf.set_font("Arial", "U", size=18)
    pdf.cell(200, 30, txt="Shipping Total Amount ($)                                                           ", ln=3, align="L")
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=str(shipping_total), ln=1, align="L")
    pdf.set_font("Arial", "U", size=18)
    pdf.cell(200, 30, txt="Total Amount Spent on Taxes ($)                                                ", ln=3, align="L")
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=str(tax_total), ln=1, align="L")
    pdf.set_font("Arial", "U", size=18)
    pdf.cell(200, 30, txt="Total-Amount Spent on All-Orders ($)                                          ", ln=3, align="L")
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=str(spending_total), ln=1, align="L")
    pdf.set_font("Arial", "U", size=18)
    pdf.cell(200, 30, txt="Average Amount Spent on All Orders ($)                                        ", ln=3, align="L")
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=str(average_spent), ln=1, align="L")

    pdf.output("totals.pdf")


totals()


# This function plots a line graph showcasing the total cost of each order since the creation of my Amazon account
# spread out over the years instead of each individual order date


def all_orders():

    fig, ax = plt.subplots(figsize=(16, 7))
    g = sns.lineplot(x=df['Order_Date'],
                     y=df["Total_Charged"], palette="Blues")
# manual xticklabels for each year ranging 2018-2022
    g.set_xticklabels(['2018', '2019', '2020', '2021', '2022'])

    ax.get_xaxis().set_major_locator(LinearLocator(numticks=5))
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator(20))
    ax.grid(visible=True, which='major', color='w', linewidth=1.0)
    sns.set_context(font_scale=1.5, rc={"lines.linewidth": 1})
    sns.set_style("darkgrid")

    plt.ylabel("Total Cost ($)")
    plt.xlabel('Order Date')
    plt.title("Cost of Amazon orders over the years")
# save svg -> rlg -> pdf
    fig.savefig('all_orders.svg')
    all_orders_svg = svg2rlg('all_orders.svg')
    renderPDF.drawToFile(all_orders_svg, "all_orders.pdf")


all_orders()


# This function plots a line graph showcasing my total spending for each year
# dataset point at each yearly interval

def yearly_spending():

    df["Year"] = pd.DatetimeIndex(df['Order_Date']).year
    yoy_cost = df.groupby(["Year"], as_index=False).sum()
    print(yoy_cost)
    fig, ax = plt.subplots(figsize=(16, 7))

    # set up and customize line plot
    sns.set_theme()
    sns.lineplot(x=yoy_cost["Year"], y=yoy_cost["Total_Charged"],
                 err_style='bars', palette="mako")
    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 5})
    sns.set_style("darkgrid")
    plt.title("How much did I spend each year?")
    plt.ylabel("Total Cost ($)")
    ax.grid(visible=True, which='major', color='w', linewidth=1.0)
    for x, y in zip(yoy_cost["Year"], yoy_cost["Total_Charged"]):
        plt.text(x=x, y=y-150, s='{:.0f}'.format(y))
# save svg -> rlg -> pdf
    fig.savefig('yearly_spending.svg')
    yearly_spending_svg = svg2rlg('yearly_spending.svg')
    renderPDF.drawToFile(yearly_spending_svg, "yearly_spending.pdf")


yearly_spending()


# This function plots a bar graph showcasing the total spending for each month over the years,
# so each year for the month of January, etc

def monthly_spending():

    df['Month'] = pd.DatetimeIndex(df['Order_Date']).month
    monthly_cost = df.groupby(["Month"], as_index=False).sum()
    print(monthly_cost)
# set up and customize bar plot
    sns.set()
    fig, ax = plt.subplots(figsize=(16, 7))
    sns.set_theme()
    sns.set_style("darkgrid")
    g = sns.barplot(
        x=monthly_cost["Month"], y=monthly_cost['Total_Charged'], palette="flare")
# manual xticklabels for eachmonth of the year
    g.set_xticklabels(["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"])
    plt.ylabel("Total Cost ($)")
    plt.title("How much did I spend each month?")
    ax.grid(visible=True, which='major', color='w', linewidth=1.0)
    for i in ax.containers:
        ax.bar_label(i,)
# save svg -> rlg -> pdf
    fig.savefig('monthly_spending.svg')
    monthly_spending_svg = svg2rlg('monthly_spending.svg')
    renderPDF.drawToFile(monthly_spending_svg, "monthly_spending.pdf")


monthly_spending()


# This function showcases the total amount spent on Amazon orders according to each day of the week


def daily_spending():

    df['Days'] = pd.DatetimeIndex(df['Order_Date']).dayofweek
    daily_cost = df.groupby(["Days"], as_index=False).sum()
    print(daily_cost)
# set up and customize barplot
    fig, ax = plt.subplots(figsize=(18, 7))
    g = sns.barplot(
        x=daily_cost["Days"], y=daily_cost["Total_Charged"], palette='icefire')
# manual xticklabels for each day of the week
    g.set_xticklabels(["Monday", "Tuesday", "Wednesday",
                      "Thursday", "Friday", "Saturday", "Sunday"])
    sns.set_theme()
    sns.set_style("darkgrid")
    plt.ylabel("Total Spent ($)")
    plt.title("Which Days of the Week Do I Spend The Most Money")
    for i in ax.containers:
        ax.bar_label(i,)
    ax.grid(visible=True, which='major', color='w', linewidth=1.0)
# save svg -> rlg -> pdf
    fig.savefig('daily_spending.svg')
    daily_spending_svg = svg2rlg('daily_spending.svg')
    renderPDF.drawToFile(daily_spending_svg, "daily_spending.pdf")


daily_spending()


# This function pulls 2 columns from the "amazon_items.csv" : the Category and Item_Total
# this function will help determine which category I have spent the most amount of money on and what I spend the most on

def category_spending():

    columns = ["Category", "Item_Total"]
    df = pd.read_csv("amazon_items.csv", usecols=columns)
    df["Item_Total"] = df["Item_Total"].astype(str).str.replace(
         '$', '', regex=True).astype(float)
    df = df.groupby(['Category']).sum().reset_index()
    categories = df.sort_values(by=['Item_Total'], ascending=False).head(n=12)
    print(categories)

    fig, ax = plt.subplots(figsize=(20, 7))

    sns.set_theme()
    sns.set_style("darkgrid")
    sns.barplot(x=categories["Category"],
                y=categories['Item_Total'], palette="crest")
    labels = [textwrap.fill(label.get_text(), 12)
              for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels, fontsize=10)
    ax.grid(visible=True, which='major', color='w', linewidth=1.0)
    plt.ylabel("Amount Spent per Item Category ($)")
    plt.title("Top Categories")
    for i in ax.containers:
        ax.bar_label(i,)
    # save svg -> rlg -> pdf
    fig.savefig('category_spending.svg')
    category_spending_svg = svg2rlg('category_spending.svg')
    renderPDF.drawToFile(category_spending_svg, "category_spending.pdf")


category_spending()


# This function pulls 2 columns from the "amazon_items.csv" : the Category and Item_Total
# this function will help determine which category I have spent the most amount of money on and what I spend the most on
# uses the same data as the previous graph, however, it is displayed as a pie chart to show a better visual breakdown of spending


def cat_spending_pie():

    #import data
    columns = ["Category", "Item_Total"]
    df = pd.read_csv("amazon_items.csv", usecols=columns)
    df["Item_Total"] = df["Item_Total"].astype(str).str.replace(
        '$', '', regex=True).astype(float)
    df = df.groupby(['Category']).sum().reset_index()
    cats = df.sort_values(by=['Item_Total'], ascending=False).head(n=12)

    colors = sns.color_palette("bright")
    plt.pie(cats['Item_Total'], labels=cats['Category'], colors=colors,
            autopct='%.0f%%', rotatelabels='true')
    fig = plt.gcf()
    fig.legend(
        loc='upper left',
        prop={'size': 10},
        bbox_to_anchor=(0.5, 2.1))
    theme = plt.get_cmap('bwr')
    plt.show()
    # save svg -> rlg -> pdf
    fig.savefig('cat_spending_pie.svg', bbox_inches='tight')
    cat_spending_pie_svg = svg2rlg('cat_spending_pie.svg')
    renderPDF.drawToFile(cat_spending_pie_svg, "cat_spending_pie.pdf")


cat_spending_pie()

# after all svg files have been converted to their respective pdf files, this function then pulls each of those pdf files
# from a list and merges them into a single file I named amazon_data.pdf


def pdf_merge(pdf_file):
    pdf_list = ['amazon_spending.pdf', 'totals.pdf', 'all_orders.pdf', 'yearly_spending.pdf', 'monthly_spending.pdf',
                'daily_spending.pdf', 'category_spending.pdf', 'cat_spending_pie.pdf']
    # merge files
    merger = PdfFileMerger(pdf_file)

    for pdf in pdf_list:
        merger.append(pdf)

    merger.write("amazon_data.pdf")
    merger.close


if __name__ == '__main__':
    main()
