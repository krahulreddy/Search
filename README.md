# Search
This repository contains code to test search engines like Elasticsearch and Solr.

## Setup
The index.html is a simple html file, and can be run in any browser.

### hug.rest
The search suggestions API for elasticsearch is provided by es.py. It uses hug.rest.

    pip3 install hug -U

Start the file by using

    hug -f filename

### Elasticsearch
Download and run elasticsearch from [here](https://www.elastic.co/downloads/elasticsearch). Version 7.6.2 is used in this project.

To start the elasticsearch server, run

    path/to/elasticsearch-7.6.2/bin/elasticsearch

Create the mapping using the following:

    curl -H "Content-Type: application/json" -X PUT "localhost:9200/my-index" -d '{
        "mappings": {
            "properties": {
                "age": {
                    "type": "float"
                },
                "name": {
                    "type": "search_as_you_type",
                    "max_shingle_size": 3
                },
                "name1": {
                    "type": "completion"
                }
            }
        }
    }'
