from asyncore import read
import pytest
import pandas as pd
import numpy as np
import matplotlib
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from project import main
from project import yearly_spending
from project import all_orders
from project import pdf_merge


#check to make sure correct email format is used

def test_main():
    assert main('tlinnard4790@gmail.com') == True
    assert main('12345@com') == 'Incorrect Email'

#check to make sure all pdfs are being merged into this single file which should be the only output from this function

def test_pdf_merge():
    assert pdf_merge() == 'C:\Users\tanne\OneDrive\Documents\Tek Systems\Capstone Project\all_orders.pdf'


#check to make sure read_csv will only open .csv file and not another file type w/ same name

def test_all_orders():
    assert pd.read_csv('anazon_spending.csv') != read('amazon_spending.pdf')

#According to docs, test will fail first time it is run due to no baselineimage to compare against


@image_comparison(baseline_images=['yearly_spending'])
def test_yearly_spending():
    fig = plt.figure()
    x = np.linspace(0,2*np.pi,100)
    y = 2*np.sin(x)
    ax = fig.add_subplot(1,1,1)
    ax.set_title('How much did I spend each year?')
    ax.plot(x,y)
    ax.yaxis.set_ticks_position('right')
    ax.xaxis.set_ticks_position('top')

    


