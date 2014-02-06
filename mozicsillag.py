#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import socket
import xbmcplugin
import xbmcaddon
import xbmcgui
import urlresolver
import mechanize
import re
import sys

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

addon = xbmcaddon.Addon()
socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
addonId = addon.getAddonInfo('id')
translation = addon.getLocalizedString
xbox = xbmc.getCondVisibility("System.Platform.xbox")
baseUrl = "http://www.mozicsillag.com"

def index():
  addDir('Filmek', '', 'filmopciok','')
  addDir('Sorozatok','','sorozatopciok','')
  xbmcplugin.endOfDirectory(pluginhandle)

def listopciok(what):
  if what == "film":
    categ = "1"
    addDir('Keresés', '', 'search','','filmek')
  elif what == "sorozat":
    categ = "4"
    addDir('Keresés', '', 'search','','sorozat')

  addDir('Kategóriák', '' , 'categories','')
  addDir('Legfrissebb',  baseUrl + '/movies.php?sort=id&cat=' + categ , 'filmlista', '')
  addDir('Legnézettebb',  baseUrl + '/movies.php?sort=views&cat=' + categ , 'filmlista', '')
  addDir('Legjobbra értékelt',  baseUrl + '/movies.php?sort=imdb_rating&cat=' + categ ,  'filmlista', '')
  addDir('Legvéleményezetteb',  baseUrl + '/movies.php?sort=comments&cat=' + categ , 'filmlista', '')
  addDir('Filmek A-Z', 'azlist', '', '')
  xbmcplugin.endOfDirectory(pluginhandle)

def categories(url):
  addDir('Akció',  baseUrl + '/movies.php?sort=id&cat=1&scat=1' , 'filmlista', '')
  addDir('Animáció',  baseUrl + '/movies.php?sort=id&cat=1&scat=3' , 'filmlista', '')
  addDir('Ázsiai',  baseUrl + '/movies.php?sort=id&cat=1&scat=33' , 'filmlista', '')
  addDir('Családi',  baseUrl + '/movies.php?sort=id&cat=1&scat=9' , 'filmlista', '')
  addDir('Dokumentum',  baseUrl + '/movies.php?sort=id&cat=1&scat=7' , 'filmlista', '')
  addDir('Dráma',  baseUrl + '/movies.php?sort=id&cat=1&scat=8' , 'filmlista', '')
  addDir('Életrajzi',  baseUrl + '/movies.php?sort=id&cat=1&scat=4' , 'filmlista', '')
  addDir('Fantasy',  baseUrl + '/movies.php?sort=id&cat=1&scat=10' , 'filmlista', '')
  addDir('Game Show',  baseUrl + '/movies.php?sort=id&cat=1&scat=12' , 'filmlista', '')
  addDir('Háborús',  baseUrl + '/movies.php?sort=id&cat=1&scat=23' , 'filmlista', '')
  addDir('Horror',  baseUrl + '/movies.php?sort=id&cat=1&scat=14' , 'filmlista', '')
  addDir('Kaland',  baseUrl + '/movies.php?sort=id&cat=1&scat=2' , 'filmlista', '')
  addDir('Krimi',  baseUrl + '/movies.php?sort=id&cat=1&scat=6' , 'filmlista', '')
  addDir('Misztikus',  baseUrl + '/movies.php?sort=id&cat=1&scat=16' , 'filmlista', '')
  addDir('Reality TV',  baseUrl + '/movies.php?sort=id&cat=1&scat=18' , 'filmlista', '')
  addDir('Romantikus',  baseUrl + '/movies.php?sort=id&cat=1&scat=19' , 'filmlista', '')
  addDir('Sci-fi',  baseUrl + '/movies.php?sort=id&cat=1&scat=20' , 'filmlista', '')
  addDir('Sport',  baseUrl + '/movies.php?sort=id&cat=1&scat=21' , 'filmlista', '')
  addDir('Történelmi',  baseUrl + '/movies.php?sort=id&cat=1&scat=13' , 'filmlista', '')
  addDir('Thriller',  baseUrl + '/movies.php?sort=id&cat=1&scat=22' , 'filmlista', '')
  addDir('Vígjáték',  baseUrl + '/movies.php?sort=id&cat=1&scat=5' , 'filmlista', '')
  addDir('Western',  baseUrl + '/movies.php?sort=id&cat=1&scat=24' , 'filmlista', '')
  addDir('Zenés',  baseUrl + '/movies.php?sort=id&cat=1&scat=15' , 'filmlista', '')
  xbmcplugin.endOfDirectory(pluginhandle) 

def getUrl(url):
  req = urllib2.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:19.0) Gecko/20100101 Firefox/19.0')
  response = urllib2.urlopen(req)
  link = response.read()
  response.close()
  return link

def follow_redirect(url):
  req = urllib2.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:19.0) Gecko/20100101 Firefox/19.0')
  link = urllib2.urlopen(req).geturl()
  return link


def listvideos(urlFull):
  content = getUrl(urlFull)
  soup = BeautifulSoup(content,convertEntities=BeautifulSoup.HTML_ENTITIES)
  currentPage = 0
  nextPage = 0
  maxPage = -1
  paging = soup.findAll('div', attrs={'id': 'paging'})
  a = paging[0].findAll('a', href=True)
  maxpage = int(re.search(".*pag=(\d+).*", max(a)['href']).group(1))
  pageregex = re.search("(.*)pag=(\d+)(.*)", urlFull)
  if pageregex is not None:
    currentPage = int(pageregex.group(2))
    nextPage = currentPage + 16
    nextUrl =  pageregex.group(1) + 'pag=' + str(nextPage) + pageregex.group(3)
  else:
    nextPage = 16
    nextUrl =  urlFull + '&pag=' + str(nextPage)
  filmek = soup.findAll('div', attrs={'id': 'movie_list'})
  film_link = filmek[0].findAll('a', href=True)
  for link in film_link:
    url = link['href']
    img = link.findAll('img',src=True)[0]['src']
    title = re.search('<div class="more" id="(.*)">(.*)<br />',str(link.findAll('div',{'class': 'more'})[0])).group(2)
    addDir(title, baseUrl + '/' + url, 'listproviders', baseUrl + '/' + img)
  addDir('Következő -->', nextUrl ,'filmlista','')
  xbmcplugin.endOfDirectory(pluginhandle)

def listproviders(urlFull,title):
  content = getUrl(urlFull)
  soup = BeautifulSoup(content,convertEntities=BeautifulSoup.HTML_ENTITIES)
  providers = soup.findAll('div', attrs={'id': 'lm'})
  for provider in providers:
    share = provider.find('div', attrs={'class': 'link_share'}).text
    flag = provider.find('div', attrs={'class': 'link_flag'}).findAll('img',src=True)[0]['src']
    if flag == "images/flags/HU.png":
      nyelv = "HUN"
    else:
      nyelv = ""
    viewed = re.search('^(\d+).*',provider.find('div', attrs={'class': 'link_views'}).text).group(1)
    quality = provider.findAll('a')[2].text
    if max(provider.findAll('a')).find('div', attrs={'class': 'link_play'}) is not None:
      if max(provider.findAll('a')).find('div', attrs={'class': 'link_play'}).text == 'Lejátszás'.decode('utf-8'):
        runlink = max(provider.findAll('a'))['href']
        if quality:
          addDir('[' + quality + '] ' + share + ' (' + viewed + ') ' + nyelv , baseUrl + '/' + runlink, 'playvideo', '')
        else:
          addDir('[....] ' + share + ' (' + viewed + ') ' + nyelv , baseUrl + '/' + runlink, 'playvideo', '')
  xbmcplugin.endOfDirectory(pluginhandle)


def playvideo(url,title):
  content = getUrl(url)
  soup = BeautifulSoup(content,convertEntities=BeautifulSoup.HTML_ENTITIES)
  link = follow_redirect(url)
  if re.search('^.*watch_embeded.php.*',link):
    runlink = soup.find('iframe')['src']
  else:
    runlink = link

  print "Playvideo followed link: " + runlink
  media_url = urlresolver.resolve(runlink)
  if media_url:
    xbmc.Player().play(media_url)
  else:
    print "urlresolver.resolve(" + runlink + ') failed, try to playing directly)'
    xbmc.Player().play(runlink)

def parameters_string_to_dict(parameters):
  paramDict = {}
  if parameters:
    paramPairs = parameters[1:].split("&")
    for paramsPair in paramPairs:
      paramSplits = paramsPair.split('=')
      if (len(paramSplits)) == 2:
        paramDict[paramSplits[0]] = paramSplits[1]
  return paramDict

def addDir(name, url, mode, iconimage,other=''):
  u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+urllib.quote_plus(mode)+"&fanart="+urllib.quote_plus(iconimage)+"&other="+urllib.quote_plus(other)
  ok = True
  liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
  liz.setInfo(type="Video", infoLabels={"Title": name})
  liz.setProperty("fanart_image", iconimage)
  ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
  return ok

def search(what):
  keyboard = xbmc.Keyboard('', str(translation(30008)))
  keyboard.doModal()
  if keyboard.isConfirmed() and keyboard.getText():
    search_string = keyboard.getText()#.replace(" ", "+")
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0')]
    br.open(baseUrl)
    br.select_form(name='form1')
    br.form['src'] = search_string
    if what == 'filmek':
      br.form['what'] = ['1']
    elif what == 'sorozat':
      br.form['what'] = ['2']
    data = br.submit()
    soup = BeautifulSoup(data.read(),convertEntities=BeautifulSoup.HTML_ENTITIES)
    filmek = soup.find('div', attrs={'id': 'movie_list'})
    film_link = filmek.findAll('a', href=True)
    for link in film_link:
      url = link['href']
      img = link.findAll('img',src=True)[0]['src']
      title = re.search('^(.*)Megoszt.*',link.find('div', attrs={'class': 'more'}).text).group(1)
      addDir(title, baseUrl + '/' + url, 'listproviders', baseUrl + '/' + img)
  xbmcplugin.endOfDirectory(pluginhandle)


params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
name = urllib.unquote_plus(params.get('name', ''))
title = urllib.unquote_plus(params.get('title', ''))
fanart = urllib.unquote_plus(params.get('fanart', ''))
other = urllib.unquote_plus(params.get('other', ''))

if mode == "playvideo":
  playvideo(url,title)
elif mode == "filmlista":
  listvideos(url)
elif mode == "listproviders":
  listproviders(url,title)
elif mode == "categories":
  categories(url)
elif mode == "filmopciok":
  listopciok("film")
elif mode == "sorozatopciok":
  listopciok("sorozat")
elif mode == "search":
  search(other)
else:
  index()
