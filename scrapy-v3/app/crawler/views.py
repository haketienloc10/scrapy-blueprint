import crochet
crochet.setup()
from flask import Blueprint, request, jsonify
from marshmallow import fields, Schema
from flask_apispec import use_kwargs, marshal_with, doc, MethodResource
from app.schemas import CrawlSchema, ErrorSchema
from app.database import mongo
from scrapy.crawler import CrawlerRunner
import json
from app.crawler.spider import ExtractSpider

api_crawl = Blueprint('api_crawl', __name__)

crawl_runner = CrawlerRunner()
quotes_list = {}
scrape_in_progress = False
scrape_complete = False
_urls = []
_data = ''

# @api_v1_bp.route('/pet/<name>', methods=['GET'], provide_automatic_options=False)
# @doc(
#     tags=['pets'],
#     params={'name': {'description': 'pet id', 'maxLength': 24}}
# )
# @marshal_with(UserSchema)
# def get_pets():
#     return {'name': 'ABS', 'age': 25, 'status': 'pending'}

sample_crawl = {
    'x-code-samples': 
    [
        {
            "lang": "curl",
            "source": "curl -i http://localhost:5000/api/crawl"
        }
    ]
    }

@doc(
    tags=['crawl'],
)
class AllResource(MethodResource):
    @doc(
        summary="Get all data", 
        description="Returns list of data", 
        operationId="getAllData",
        produces=[
            'application/json'
        ],
        **sample_crawl,
    )
    @marshal_with(
        CrawlSchema(many=True), 
        code=200
    )
    @marshal_with(ErrorSchema(), code=500)
    def get(self):
        collection = mongo.db.lazada
        cursor = collection.find({})
        output = []
        for document in cursor:
            output.append({'_id': str(document.get('_id')), 'web': document['web'], 'data': document['data']})
        if cursor is None:
            return {'message': "Something went wrong on Server"}, 400
        return output, 200
    
    @doc(
        summary="Add new data", 
        description="Returns a new single pet is added", 
        operationId="postUser",
        produces=[
            'application/json'
        ],
    )
    def post(self):
        global scrape_in_progress
        global scrape_complete
        global _urls
        global _data
        _urls = request.json['urls']
        for i in range(0, len(_urls)):
            x = _urls[i].find('/', 8)
            s = _urls[i][:x+1]
            e = _urls[i][x + 1:]
            _urls[i] = s + e
        _data = request.json['data']
        if not scrape_in_progress:
            print(_urls)
            print(_data)
            scrape_in_progress = True
            global quotes_list
            self.scrape_with_crochet(ExtractSpider,quotes_list)
            return 'SCRAPING'
        elif scrape_complete:
            scrape_in_progress = False
            scrape_complete = False
            res_js = json.loads(json_util.dumps(quotes_list))
            return jsonify(res_js)
        return 'SCRAPE IN PROGRESS'

    @crochet.run_in_reactor
    def scrape_with_crochet(self, _spider, _list):
        global _urls
        if len(_list) > 0:
            _list.clear()
            print('clear')
        eventual = crawl_runner.crawl(_spider, start_urls=_urls, quotes_list=_list, data= _data)
        eventual.addCallback(self.finished_scrape)

    def finished_scrape(self, null):
        global scrape_complete
        scrape_complete = True
        print("crawl end..")
    
api_crawl.add_url_rule('/crawl', view_func=AllResource.as_view('crawl'))

