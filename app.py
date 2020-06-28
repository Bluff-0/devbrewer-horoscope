from flask import Flask, request
import json
import string
import datetime
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def authRes():
	y={
	'Home': 'https://devbrewer-horoscope.herokuapp.com/',
	'Short Horoscopes': {
	'Today':'https://devbrewer-horoscope.herokuapp.com/today/short/Aries',
	'This Week': 'https://devbrewer-horoscope.herokuapp.com/week/short/Aries',
	'This Month': 'https://devbrewer-horoscope.herokuapp.com/month/short/Aries'},
	'Detailed Horoscope': 'https://devbrewer-horoscope.herokuapp.com/today/long/Aries',
	'Love Match': 'https://devbrewer-horoscope.herokuapp.com/match/Aries/Libra',
	'Collaborator': {'Name':'Saptarshi Mazumdar',
	'@': 'http://bit.ly/saptarshimazumdar'},
	'Ideator': {'Name':'Suryanarayan Rath',
	'@': 'https://surya-trv-13.herokuapp.com/'},
	'Helping Webs': {
	'1': 'https://www.horoscope.com/',
	'2': 'https://www.prokerala.com/',
	'3': 'https://www.astrology.com/'}
	}
	return json.dumps(y), 200

@app.route("/today/long/<sign>", methods=["GET"])
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
		return json.dumps(m), 200
		m['From']= 'https://www.prokerala.com/'
	except:
		return "<h1>Internal Server Error: Status 500 || Check URL brfore proceed.</h1>",500

@app.route("/today/short/<sign>", methods=["GET"])
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
		results = soup.find_all('div', {'class':'inner flex-center-inline'})
		temp= []
		for i in results[0].text.strip().split("\n"):
			if i != '':
				temp.append(i)
		d['Matchs']={
			temp[0]:temp[1], temp[2]:temp[3], temp[4]:temp[5]
		}
		d['From']= 'https://www.horoscope.com/'
		return json.dumps(d), 200
	except:
		return "<h1>Internal Server Error: Status 500 || Check URL brfore proceed.</h1>",500

@app.route("/week/short/<sign>", methods=["GET"])
def retWeekS(sign):
	try:
		x = datetime.datetime.now()
		signs=['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
		'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
		r= requests.get('https://www.horoscope.com/us/horoscopes/general/horoscope-general-weekly.aspx?sign={}'
			.format(signs.index(sign.lower())+1))
		soup = BeautifulSoup(r.text, 'html.parser')
		results = soup.find_all('p')
		d={'Desc': 'Brief', 'Week': x.strftime("%U")}
		d[soup.title.string.split(" ")[0]]={
		'Icon': 'https://www.horoscope.com/images-US/signs/'+
		soup.title.string.split(" ")[0].lower()+'.png',
		'This Week': results[0].text[results[0].text.index('- ')+2:]}
		d['From']= 'https://www.horoscope.com/'
		return json.dumps(d), 200
	except:
		return "<h1>Internal Server Error: Status 500 || Check URL brfore proceed.</h1>",500

@app.route("/month/short/<sign>", methods=["GET"])
def retMonthS(sign):
	try:
		x = datetime.datetime.now()
		signs=['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
		'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
		r= requests.get('https://www.horoscope.com/us/horoscopes/general/horoscope-general-monthly.aspx?sign={}'
			.format(signs.index(sign.lower())+1))
		soup = BeautifulSoup(r.text, 'html.parser')
		results = soup.find_all('p')
		d={'Desc': 'Brief', 'Month': x.strftime("%m")}
		d[soup.title.string.split(" ")[0]]={
		'Icon': 'https://www.horoscope.com/images-US/signs/'+
		soup.title.string.split(" ")[0].lower()+'.png',
		'This Month': results[0].text[results[0].text.index('- ')+2:results[0].text.index('Standout')],
		'Best Days': results[0].text[results[0].text.index('Standout days'):results[0].text.index('Challenging')][15:],
		'Worst Days': results[0].text[results[0].text.index('Challenging days'):][18:]}
		d['From']= 'https://www.horoscope.com/'
		return json.dumps(d), 200
	except:
		return "<h1>Internal Server Error: Status 500 || Check URL brfore proceed.</h1>",500

@app.route("/match/<sign1>/<sign2>", methods=["GET"])
def signMatch(sign1,sign2):
	try:
		r= requests.get('https://www.astrology.com/love/compatibility/{}-{}.html'
			.format(sign1.lower(), sign2.lower()))
		soup= BeautifulSoup(r.text, 'html.parser')
		results= soup.find_all('p')

		txt=''
		for i in range(6):
			try:
				if results[i].string[:24]=='Check the love potential':
					break
				else:
					txt+= results[i].string+' '
			except:
				continue
		d={
		'Sign 1': sign1.lower(),
		'Sign 2': sign2.lower(),
		'Result': txt,
		'From': 'https://www.astrology.com/'
		}
		return json.dumps(d) , 200
	except:
		return "<h1>Internal Server Error: Status 500 || Check URL brfore proceed.</h1>",500		

if __name__ == '__main__':
    app.run(host= "0.0.0.0", debug=True, threaded=True)
