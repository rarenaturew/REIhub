from flask import Flask, render_template, request, redirect

import requests
import datetime
import pandas as pd

# deal with the plot and embedding into bokeh_embed.html
# also, calculate "today" in the previous month
from MyAux import *



app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
  Today=datetime.date.today()
  EndDate=Today.strftime("%Y-%m-%d") # default end date is today, string: %Y-%m-%d
  StartDate=getStartDate(Today) # one month before today, a string: %Y-%m-%d
  if request.method == 'GET':
    return render_template('index.html',start_date=StartDate)
  else:
    return render_template('result.html') 


if __name__ == '__main__':
  app.run()
