# run pip install -r requirements.txt in terminal
from flask import Flask, jsonify,  render_template, request, redirect # Import Framework
import requests as rq # Import requests module to request any site
import bs4 # Web Scraping module
import json # To read json data
import pandas as pd # To work on dataframe
from datetime import datetime # To get current server time

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def home_page():
    if(request.method=='POST'): #on POST request
        url=request.form.get('url') #url is obtained from form
        url = url.replace("/", "*") # '/' is replaced by * in url
        return redirect('/api/'+url) # redirect to api
    else:
        return render_template('index.html' )


@app.route("/api/<string:url>", methods = ['GET', 'POST'])
def geturl(url):
    urlDict= {} #initialize dictionary
    url = url.replace("*", "/") #replace '*' by '/' in url
    url ='https://'+str(url) #'https://' in concatenated with the url
    try:

        res = rq.get(url) #requesting url

    except:

        return 'Error!'

    if res.status_code == 200:
        # print(type(res))
        urlDict["status"] = "success"
        urlDict["url"]= url
        soup = bs4.BeautifulSoup(res.text, 'lxml') #Parser
        # Advantages of using lxml it's Very fast & Lenient
        # print(type(soup))
        # <class 'bs4.element.Tag'>
        title = soup.select('title') #selcting titile tag
        urlDict["title"] = title[0].getText() #text of title tag is obtained
        a = url
        count = 1
        urlDict["links"] = {} #initialize dictionary of dictionary

        for link in soup.find_all('a', href=True):
            if '#' in link['href']: # case 1 when when link is '#'
                continue  # Even pass can be used
            elif '/' in link['href'][0]: # case 2 where link is without root url
                c = a + link['href']
                variable = 'link-' + str(count)
                count = count + 1
                urlDict["links"][variable] = str(c) + link['href']
            else:
                variable = 'link-' + str(count) # else part
                count = count + 1
                urlDict["links"][variable] = link['href']

        urlDict["seo"] = {} #initialize dictionary of dictionary

        for c1 in soup.find_all('meta', content=True, property="og:locale"): #find all meta tag with property='og:locale'
            urlDict["seo"]["language"] = c1['content']

        for c2 in soup.find_all('meta', content=True, property="og:type"): #find all meta tag with property='og:type'
            urlDict["seo"]["type"] = c2['content']

        for c7 in soup.find_all('meta', content=True, property="og:site_name"): #find all meta tag with property='og:site_name'
            urlDict["seo"]["site_name"] = c7['content']

        for c5 in soup.find_all('meta', content=True, property="og:url"): #find all meta tag with property='og:url'
            urlDict["seo"]["site_url"] = c5['content']

        for c4 in soup.find_all('meta', content=True, property="og:title"):#find all meta tag with property='og:title'
            urlDict["seo"]["site_title"] = c4['content']

        for c3 in soup.find_all('meta', content=True, property="og:description"): #find all meta tag with property='og:description'
            urlDict["seo"]["site_description"] = c3['content']

        for c6 in soup.find_all('meta', content=True, property="article:modified_time"): #find all meta tag with property='article:modified_time'
            urlDict["seo"]["last_modified_time"] = c6['content']

        urlDict["img"] = {} #initialize dictionary of dictionary

        countimg = 1

        for link in soup.find_all('img'):
            if '/' in link['src'][0]:
                if '/' in link['src'][1]:
                    var2 = 'img-' + str(countimg)
                    urlDict["img"][var2] = 'https:'+link['src']
                    countimg = countimg + 1

            if '/' in link['src'][0]:
                if '/' not in link['src'][1]:
                    var2 = 'img-' + str(countimg)
                    urlDict["img"][var2] = str(url) + link['src']
                    countimg = countimg + 1
            else:
                var2 = 'img-' + str(countimg)
                urlDict["img"][var2] = link['src']
                countimg = countimg + 1
        urlDict["para_tag"]={}
        pcount=1

        for i in soup.find_all('p'): #find all para tag
            variable = 'ptag-'+str(pcount)
            urlDict["para_tag"][variable] = i.getText().strip('\n') #data cleaning removal of newline characters

        urlDict["data_recived_at"] = str(datetime.now()) #current datatime of the server is obatined using datatime module

#         try:

#             req = rq.get('https://ipapi.co/43.247.157.20/json' + url) #request to get info on host or domain

#         except:

#             return 'Error!'
#         # print(res.text)
#         if res.status_code == 200:

#             urlDict["hosting_info"] = {}  #initialize dictionary of dictionary

#         else:
#             return 'Error!'
#         return jsonify(urlDict)
#     else:
#         return 'Error!'


if __name__ == '__main__':
    app.run(debug=True)
