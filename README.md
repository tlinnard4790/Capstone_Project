# Capstone_Project

This repository contains the scripts and files required for the Python Capstone Project through TekSystems and Optum
  *The main script being the python.py script with additional scripts and files such as a script to test the functions found within project.py
  and the pip-installable libraries required to run project.py. 
  
For this particular project we were given free reign over the design and implementation of our python program, but still had to meet certain criteria and expectations. As you may know the potential and capabilities with Python are rather endless so the first challenege was actually deciding on which direction I wanted to go with my project and what I wanted it to accomplish. 

Ultimately, I decided on some form of data analytics to analyze large datasets that at first may appear to be nonsensical or overwhelming. The next step on this journey was having to choose what datatset or files I wanted to analyze and how that might be done. While I lived in Arizona, I spent quite a bit of my freetime perusing Amazon for items that I wasn't able to purchase around me. I noticed that Amazon has an option within the account settings that allows the user to download all of their purchase history which includes a .csv file of order history, or if you wanted to dive a bit deeper, a .csv file of the items within those orders.


So, for this project I decided to analyze the datasets of both my orders, and the items within, since the creation of my Amazon account back in 2018. This would pull all the data over the past 4.5 years or so and give me two .csv files full of useful and useless data. My approach was to pull the useful data into a DataFrame so it would be much easier to read, while also providing statistics on the orders and items within, as well as plot this information for data visualization. I'd say this can project was quite useful for me as I had no clue the amount of money I had spent over the years and how quickly things can add up.

I chose this approach becuase this particular script does not just apply to my Amazon spending, but rather can be used for almost any dataset with a little tweaking. The possibilities are pretty endless whether you want to check other spending habits elsewhere, assist with budgeting by setting certain parameters to see if any purchases are over a set limit, or use within other sectors such as inventory management, logistics, or healthcare.

Throughout the process there were plenty of issues I came across since I was dealing with some new concepts and pip libraries:

1 - Converting the DataFrames into a PDF was certainly a challenge and I had tried multiple approaches trying to utilize several PDF pip-installable libraries. The technical difficulty came from the fact that I was attempting to convert a DataFrame that I had manipulated with several lines of code beforehand instead of just a DataFrame straight from the .csv file. After several trials with many errors I was able to find a method of converting the customized DataFrame into an html file and then in turn convert that to PDF file. 

2 - Again, another issue with PDF file conversion but this time it was with my string functions pertaining to the totals and calculations of several categories of the dataset. I had already coded out the calculations for shipping costs, taxes, subtotals, overall totals, etc but when trying to iterate through that code and plug the output into a PDF file, I repeatedly received several errors ranging from NoneType to Argument errors. To get past this I overhauled the entire function and utilized PDFkit to create a blank PDF file and input the data that way. 

3 - The data visualization was a challenge as well as any small tweak could completely shutdown the function and result in an error. The main arguments for the plots of x, y, and color resulted in a rather uninteresting plot to look at, so there was a lot of trial and error of tweaking the plots to make them more visually appealing while also showcasing the data as well not just a visual representation.

4 - The final portion of the script emails all of the data into a single merged PDF file for quick analysis. However, getting the email function to work proved rather troublesome even though it appeared I had everything correct within my code. After a bit of searching I discovered it wasn't my account and password needed for the gmail smtp, but rather the password for the 3rd party access. I was able to locate and generate the password required and once that was plugged into the code I received my first email. 


