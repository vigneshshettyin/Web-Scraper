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
    # ip_address = "43.247.157.20"; # ip initialized for testing
    # TODO: Comment above line when website is live on web
    ip_address = request.environ['HTTP_X_FORWARDED_FOR']  # get's client ip address
    try:

        response = rq.get("http://ip-api.com/json/{}".format(ip_address)) # requests to get user client info

    except:
        return 'Error!'

    if response.status_code == 200:
        if (ip_address == "127.0.0.1"):
            return 'Error!'
        else:
            js = response.json()
            state = js['regionName'] # user clients state is obtained
        # print(state)
    else:
        return 'Error!'
    try:

        res = rq.get("https://api.rootnet.in/covid19-in/stats/latest")# requests to get user covid 19 status info from api in json format

    except:

        return 'Error!'

    if res.status_code == 200:

        covid = res.json() # json data assigned to variable covid

        if(state=='Karnataka'): # match with json data
            status=15
        elif(state=='Kerala'):
            status=16
        elif(state=='Maharashtra'):
            status=20
        elif(state=='Andhra Pradesh'):
            status=1

        loc = covid['data']['regional'][status]['loc'] # state name

        confirmedCasesIndian = covid['data']['regional'][status]['confirmedCasesIndian'] #confirmedCasesIndian

        discharged = covid['data']['regional'][status]['discharged'] #discharged

        deaths = covid['data']['regional'][status]['deaths'] #deaths

        totalConfirmed = covid['data']['regional'][status]['totalConfirmed'] #totalConfirmed

        # print(loc,confirmedCasesIndian, discharged, deaths, totalConfirmed)
        if(request.method=='POST'): #on POST request

            url=request.form.get('url') #url is obtained from form
            # print(url)
            url = url.replace("/", "*") # '/' is replaced by * in url

            return redirect('/api/'+url) # redirect to api
    else:
        return 'Error'
    return render_template('index.html', state=loc,confirmedCasesIndian=confirmedCasesIndian,discharged=discharged, deaths=deaths, totalConfirmed=totalConfirmed )

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

        try:

            req = rq.get('https://check-host.net/ip-info?host=' + url) #request to get info on host or domain

        except:

            return 'Error!'
        # print(res.text)
        if res.status_code == 200:

            soup = bs4.BeautifulSoup(req.text, 'lxml') #soup object is created

            table = soup.find('table', attrs={'class': 'hostinfo result'}) #find all with class='hostinfo result'
            table_rows = table.find_all('tr')

            # for tr in table_rows:
            #     td = tr.find_all('td')
            #     row = [tr.text for tr in td]
            #     print(row)

            l = [] #initialize list
            for tr in table_rows:
                td = tr.find_all('td')
                row = [tr.text for tr in td]
                l.append(row) #appending to list

            # df = pd.DataFrame(l)

            # df = l.replace('\n','', regex=True)

            df = pd.DataFrame(l) #converting list to dataframe

            df = df.replace('\n', '', regex=True) #data cleaning removal of newline characters

            df.drop(df.columns[[0]], axis=1, inplace=True) #droping column 0 of the dataframe df

            # print(df)

            urlDict["hosting_info"] = {}  #initialize dictionary of dictionary

            urlDict["hosting_info"]["host_ip"] = df[1][0]

            urlDict["hosting_info"]["host_dns"] = df[1][1]

            urlDict["hosting_info"]["host_ip_range"] = df[1][2]

            urlDict["hosting_info"]["isp"] = df[1][3]

            urlDict["hosting_info"]["hosting_provider"] = df[1][4]

            urlDict["hosting_info"]["country"] = df[1][5]

            urlDict["hosting_info"]["region"] = df[1][6]

            urlDict["hosting_info"]["city"] = df[1][7]

            urlDict["hosting_info"]["time_zone"] = df[1][8]

            urlDict["hosting_info"]["local_time"] = df[1][9]

            urlDict["hosting_info"]["postal_code"] = df[1][10]
        else:
            return 'Error!'
        return json.dumps(urlDict)
    else:
        return 'Error!'


if __name__ == '__main__':
    app.run(debug=True)
