'''
Source code for the Flask app
'''

import datetime
from flask import Flask, jsonify,  render_template, request, redirect
from services.network import NetworkService
from services.scrape import DataScrapingService

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home_page():
    '''
    This function returns the home page
    '''

    if (request.method == 'POST'):
        url = request.form.get('url').strip()
        url_star = url.replace("/", "*")
        return redirect('/api/'+url_star)
    else:
        return render_template('index.html')


@app.route("/api/<string:url>", methods=['GET', 'POST'])
def geturl(url):
    '''
    This function returns the data from the url
    '''

    data = {}

    url = url.replace("*", "/")

    if (url.startswith('http://')):
        url = url[7:]

    elif (url.startswith('https://')):
        url = url[8:]

    url = 'https://'+str(url)

    data_scraping_service = DataScrapingService()
    data = data_scraping_service.get_data(url)

    network_service = NetworkService()
    data["network"] = network_service.get_data(url)

    data["data_scraped_at"] = datetime.datetime.now()

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=False)
