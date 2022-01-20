from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

es.indices.delete(index='test-index', ignore=[400, 404])

print("#### TEST 1 ####")
res = es.index(index="test-index", id=1, document=doc)
print(res['result'])

print("\n\n#### TEST 2 ####")
res = es.get(index="test-index", id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

print("\n\n#### TEST 3 ####")
res = es.search(index="test-index", query={"match_all": {}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


print("\n\n#### TEST 4 ####")
# User makes a request on client side
user_request = "kimchy"

# Take the user's parameters and put them into a
# Python dictionary structured as an Elasticsearch query:
query_body = {
  "query": {
    "bool": {
      "must": {
        "match": {      
          "author": user_request
        }
      }
    }
  }
}

query_body2 = {
  "query": {
    "bool": {
      "must": {
        "match": {      
          "author": 'Paul'
        }
      }
    }
  }
}
# Pass the query dictionary to the 'body' parameter of the
# client's Search() method, and have it return results:
res = es.search(index="test-index", body=query_body)
res2 = es.search(index="test-index", body=query_body2)

print(res)
print(res2)