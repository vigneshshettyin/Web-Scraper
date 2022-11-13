'''
Source code for the Flask app
'''

import datetime
from flask import Flask, jsonify,  render_template, request, redirect
from services.urls import UrlValidators
from services.scrape import DataScrapingService
from services.network import NetworkService

app = Flask(__name__)

url_validator = UrlValidators()


@app.route('/', methods=['GET', 'POST'])
def home_page():
    '''
    This function returns the home page
    '''

    if (request.method == 'POST'):
        url = url_validator.clean_url(request.form.get('url'))
        if not url_validator.validate_url(url):
            return render_template('index.html', error='Invalid URL!')
        return redirect('/v1/scrape?url=' + url)
    else:
        return render_template('index.html')


@app.route("/v1/scrape", methods=['GET'])
def scrape_data():
    '''
    This function returns the data from the url
    '''
    url = url_validator.clean_url(request.args.get('url'))
    if not (url_validator.validate_url(url)):
        return jsonify({'error': 'Invalid URL!'}), 400

    data_scraping_service = DataScrapingService()
    data = data_scraping_service.get_data(url)

    network_service = NetworkService()
    data["network"] = network_service.get_data(url)

    data["data_scraped_at"] = datetime.datetime.now()

    return jsonify(data), 200


if __name__ == '__main__':
    app.run(debug=True)
