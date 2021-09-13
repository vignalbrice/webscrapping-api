from time import time
from flask import json
import requests
from bs4 import BeautifulSoup
import flask
from flask import request, jsonify
from selenium import webdriver
from flask import Flask
from flask_cors import CORS


#Get url to scrap datas
url = 'https://neko-sama.fr'
#Get request and scrap content
r = requests.get(url)
#Call BeautifulSoup package to get the content of html5page
soup = BeautifulSoup(r.content, 'html5lib')
#Target the div we want to scrap
lastContainer = soup.find('div', attrs={'class': 'js-last-episode-container'})
animeContainer = soup.find('div', attrs={'class': 'anime-listing'})
morePopularContainer = soup.find('div', attrs={'class': 'col'})
#Retrieved last episodes
lastEpisodes = []
animeInProgress = [] 
morePopular = []
for row in lastContainer.find_all('div', attrs={'class', 'ma-thumbnail'}):
  lastEp = {}
  try:
    lastEp['img'] = row.find_all("img")[1]["src"]
    lastEp['caption'] = row.find('div', {'class': 'overlay'}).find('a', {'class': 'cover'}).find('img')['src']
    lastEp['published'] = row.find('div', {'class': 'overlay'}).find('span', {'class': 'time'}).contents[0]
    lastEp['title'] = row.find('div', {'class': 'text'}).find('a', attrs={"class": "title"}).find('div', attrs={'class': 'limit'}).contents[0]
    lastEp['episode'] = row.find('div', {'class': 'text'}).find('a', attrs={"class": "title"}).find('span', attrs={'class': 'episode'}).contents[0]
    lastEpisodes.append(lastEp)
    
  except TypeError: 
    continue
  
for row in animeContainer.find_all('a'):
  animeProg = {}
  try:
    animeProg['img'] = row.find('div', {'class': 'ma-lazy-wrapper'}).find('img', {'class': 'lazy'})['data-src']
    animeProg['title'] = row.find('div', {'class': 'title'}).contents[0]
    animeProg['episode'] = row.find('div', {'class': 'episode'}).contents[0]
    animeInProgress.append(animeProg)
    
  except TypeError: 
    continue
  
for row in morePopularContainer.find_all('a'):
  morePop = {}
  try:
    morePop['img'] = row.find('div', {'class': 'ma-lazy-wrapper'}).find('img', {'class': 'lazy'})['data-src']
    morePop['title'] = row.find('div', {'class': 'title'}).contents[0]
    morePop['episode'] = row.find('div', {'class': 'episode'}).contents[0]
    morePopular.append(morePop)
    
  except TypeError: 
    continue

#Show the data  
app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
  
@app.route('/last-episode', methods=['GET'])
def last_episode ():
  return jsonify(lastEpisodes)

@app.route('/anime-in-progress', methods=['GET'])
def anime_in_progress ():
  return jsonify(animeInProgress)

@app.route('/more-popular', methods=['GET'])
def anime_more_popular ():
  return jsonify(morePopular)

app.run()