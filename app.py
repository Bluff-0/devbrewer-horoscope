from flask import Flask, request
import json
import string
import datetime
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route("/long/<sign>", methods=["GET"])
def retTodayD(sign):
	try:
		x = datetime.datetime.now()
		ns=sign
		sign= sign.lower()
		r= requests.get('https://www.prokerala.com/astrology/horoscope/?sign='+sign)
		soup = BeautifulSoup(r.text, 'html.parser')
		results = soup.find_all('p')
		m={'Desc': 'Descriptive', 'Date': x.strftime("%x"), ns:{'Icon': 'https://www.horoscope.com/images-US/signs/'+sign+'.png',
			'Daily': results[1].string, 'Health': results[2].string, 'Love': results[3].string, 'Career': results[5].string}}
		return json.dumps(m)
	except:
		return "Internal Server Error: Status 500 || Check URL brfore proceed."

@app.route("/short/<sign>", methods=["GET"])
def retTodayS(sign):
	try:
		x = datetime.datetime.now()
		signs=['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
		'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
		r= requests.get('https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={}'
			.format(signs.index(sign.lower())+1))
		soup = BeautifulSoup(r.text, 'html.parser')
		results = soup.find_all('p')
		d={'Desc': 'Brief', 'Date': x.strftime("%x")}
		d[soup.title.string[:soup.title.string.index(':')].split(" ")[0]]={
		'Icon': 'https://www.horoscope.com/images-US/signs/'+
		soup.title.string[:soup.title.string.index(':')].split(" ")[0].lower()+'.png',
		'Today': results[0].text[results[0].text.index('-')+2:]}
		return json.dumps(d)
	except:
		return "Internal Server Error: Status 500 || Check URL brfore proceed."

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port= os.environ.get('PORT', 48080), threaded=True)