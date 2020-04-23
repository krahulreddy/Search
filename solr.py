import hug
from urllib.request import urlopen
import pysolr
import json

solr = pysolr.Solr('http://localhost:8983/solr/my-index', always_commit=True)

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

    connection = urlopen('http://localhost:8983/solr/my-index/select?q=*:*')
    res = json.load(connection)
    print(res['response']['docs'])
    return res


@hug.post('/addDoc')
def addDoc(age, name):
    res = solr.add([
        {
            "name": name,
            "age": age,
            "name1": name
        }
    ])
    print(res)
    return res


@hug.get('/search')
def search(q):
    connection = urlopen('http://localhost:8983/solr/my-index/select?q=name:\"' + q + '\"')
    res = json.load(connection)
    print(res)
    return res