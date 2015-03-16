__author__ = 'fabienngo'
query_template = {
  "query": {
    "bool": {
      "should": {
        "multi_match": {
          "query": "Belgique",
          "type": "cross_fields",
          "fields": [
            "title^2",
            "textualContent^0.75",
            "keywords",
            "header^1.5"
          ],
          "minimum_should_match": "75%"
        }
      }
    }
  }
}


