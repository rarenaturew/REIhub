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
    #request.form is an ImmutableMultiDict
    StockName = request.form['stock_name'].upper()
    ShowFeatures=[] # which features to show
    # or if request.form.get('close_price',False): ShowFeatures.append('Close')
    if 'close_price' in request.form: ShowFeatures.append('Close')
    if 'adj_close_price' in request.form: ShowFeatures.append('Adj. Close')
    SD=request.form['start_date']
    if len(SD) == 10 : StartDate=str(SD)
    ED=request.form['end_date']
    if len(ED) == 10 : EndDate=str(ED)
    URL='https://www.quandl.com/api/v3/datasets/WIKI/'+StockName+'.json?auth_token=XMD-ta2mEyx3bj_AGW3n&start_date='+StartDate+'&end_date='+EndDate
    r = requests.get(URL).json()
    if 'dataset' in r:
      dataDF = pd.DataFrame(data=r['dataset']['data'],\
                         columns=r['dataset']['column_names'])
      plotDF(dataDF,StockName,ShowFeatures)
      return redirect('plot') 
    else:
      return redirect('/error', error_message=r['quandl_error']['message'] ) 


@app.route('/plot',methods=['GET','POST'])
def plot():
  return render_template('bokeh_embed.html') 


@app.route('/error',methods=['GET','POST'])
def error(error_message):
  return render_template('error.html', end_message=error_message ) 

if __name__ == '__main__':
  app.run()
