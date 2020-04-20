from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import hug

from functools import wraps


@hug.response_middleware()
def CORS(request, response, resource):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.set_header(
        'Access-Control-Allow-Headers',
        'Authorization,Keep-Alive,User-Agent,'
        'If-Modified-Since,Cache-Control,Content-Type'
    )
    response.set_header(
        'Access-Control-Expose-Headers',
        'Authorization,Keep-Alive,User-Agent,'
        'If-Modified-Since,Cache-Control,Content-Type'
    )
    if request.method == 'OPTIONS':
        response.set_header('Access-Control-Max-Age', 1728000)
        response.set_header('Content-Type', 'text/plain charset=UTF-8')
        response.set_header('Content-Length', 0)
        response.status_code = hug.HTTP_204


@hug.get('/all')
def all():
    es = Elasticsearch()
    res = es.search(index="my-index", body={
        "query": {
            "match_all": {}
        }})
    # print(res)
    return res

@hug.post('/addDoc')
def addDoc(age, name):
    es = Elasticsearch()
    print(age, name)
    res = es.index(index="my-index", doc_type="_doc", body={"age":age,"name":name,"name1":name})
    print(res['result'])
    # res = es.search(index="my-index", body={
    #     "query": {
    #         "match_all": {}
    #     }})
    # print(res)
    return res


@hug.get('/sayt')
def sayt(q):
    es = Elasticsearch()
    print(q)
    res = es.search(index="my-index", body={
        "query": {
            "multi_match": {
                "query": q,
                "type": "bool_prefix",
                "fields": [
                    "name",
                    "name._2gram",
                    "name._3gram",
                    "name._4gram"
                ]
            }
        }})
    # print(res)
    return res


@hug.get('/comp')
def comp(q):
    es = Elasticsearch()
    print(q)
    res = es.search(index="my-index", body={
        "query": {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": q,
                        "fields": [
                            "name",
                            "name._2gram",
                            "name._3gram"
                        ]
                    }
                },
                "script_score": {
                    "script": {
                        "source": "doc['age'].value + _score"
                    }
                }
            }
        }})
    # print(res)
    return res
