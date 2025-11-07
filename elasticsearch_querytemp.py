from elasticsearch import Elasticsearch

# Initialize client
es = Elasticsearch("http://your-es-host:9200")

index_name = "your_index"
id_field = "id"
timestamp_field = "your_timestamp_field"
exclude_ids = ["x1", "x2", "x3", "x4"]
start_time = "t1"
end_time = "t2"

query = {
    "query": {
        "bool": {
            "must": [
                {
                    "range": {
                        timestamp_field: {
                            "gte": start_time,
                            "lte": end_time
                        }
                    }
                }
            ],
            "must_not": [
                {
                    "terms": {
                        id_field: exclude_ids
                    }
                }
            ]
        }
    }
}

response = es.search(index=index_name, body=query)
print(response)
