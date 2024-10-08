from elasticsearch import Elasticsearch

# Define the Elasticsearch server address and credentials
# Create an Elasticsearch client
es = Elasticsearch(
        [{'host':"atlas-kibana.mwt2.org", 'port': 9200, 'scheme': "https"}],
        basic_auth=("selbor", "13Dirtyghettokids*")
)

# Check if the connection is successful
try:
    response = es.info()
    print("Success", response)
except Exception as e:
    print("ERROR", e)

