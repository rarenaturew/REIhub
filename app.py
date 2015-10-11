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
  # 9 combinations of rental income, and appreciation
  srcHH_LC="https://irarenature.cartodb.com/viz/ee95e2ce-6c3a-11e5-bfa6-0ef24382571b/embed_map"
  srcHH_MC="https://irarenature.cartodb.com/viz/8cf20b74-6c44-11e5-96b0-0e98b61680bf/embed_map"
  srcHH_HC="https://irarenature.cartodb.com/viz/2998fec6-6c43-11e5-a81d-0e8c56e2ffdb/embed_map"
  srcCA_LC="https://irarenature.cartodb.com/viz/98409b9c-6c46-11e5-823d-0ef7f98ade21/embed_map"
  srcCA_MC="https://irarenature.cartodb.com/viz/f447a08a-6c45-11e5-a517-0ef7f98ade21/embed_map"
  srcCA_HC="https://irarenature.cartodb.com/viz/33f21a4a-6c45-11e5-94ad-0e3a376473ab/embed_map"
  srcAP_LC="https://irarenature.cartodb.com/viz/76a68206-6c48-11e5-9b67-0e98b61680bf/embed_map"
  srcAP_MC="https://irarenature.cartodb.com/viz/dc597ad2-6c47-11e5-9dd6-0ef24382571b/embed_map"
  srcAP_HC="https://irarenature.cartodb.com/viz/00dccca2-6c47-11e5-9f9f-0e3a376473ab/embed_map"
  Today=datetime.date.today()
  EndDate=Today.strftime("%Y-%m-%d") # default end date is today, string: %Y-%m-%d
  StartDate=getStartDate(Today) # one month before today, a string: %Y-%m-%d
  result_src_http = srcAP_LC
  if request.method == 'GET':
    return render_template('index.html',src_http = result_src_http, jump_flag = 0)
  else:
    form_result = request.form
    if form_result['prefer_return']=='cash' and form_result['crime_level']=='high':
      result_src_http = srcCA_HC 
    if form_result['prefer_return']=='cash' and form_result['crime_level']=='medium':
      result_src_http = srcCA_MC
    if form_result['prefer_return']=='cash' and form_result['crime_level']=='low':
      result_src_http = srcCA_LC
    if form_result['prefer_return']=='cash_appr' and form_result['crime_level']=='high':
      result_src_http = srcHH_HC
    if form_result['prefer_return']=='cash_appr' and form_result['crime_level']=='medium':
      result_src_http = srcHH_MC
    if form_result['prefer_return']=='cash_appr' and form_result['crime_level']=='low':
      result_src_http = srcHH_LC
    if form_result['prefer_return']=='appr' and form_result['crime_level']=='high':
      result_src_http = srcAP_HC
    if form_result['prefer_return']=='appr' and form_result['crime_level']=='medium':
      result_src_http = srcAP_MC
    if form_result['prefer_return']=='appr' and form_result['crime_level']=='low':
      result_src_http = srcAP_LC
    return render_template('index.html', src_http = result_src_http, jump_flag = 1 ) 



if __name__ == '__main__':
  app.run()
