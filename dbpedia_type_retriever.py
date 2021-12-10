import requests
import urllib.parse
import json

def retrieve(uri):

    query = "select distinct ?c where { <"+uri+"> rdf:type ?c. ?c rdf:type owl:Class. } "

    query = urllib.parse.quote(query)
    api_url = "http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query="+query+"&format=JSON&timeout=0&debug=on&run=+Run+Query+"

    response = requests.get(api_url)

    types = []

    # extract the content
    if response.status_code == 200:
        content = response.content.decode("utf-8")
        json_content = json.loads(content)

        if "results" in json_content:
            if "bindings" in json_content["results"]:
                for b in json_content["results"]["bindings"]:
                    type = b["c"]["value"]
                    types.append(type)

        # Agent is used as a general term to for Person, Location, Org, nothing specific that's why we remove it
        if "http://dbpedia.org/ontology/Agent" in types:
            types.remove("http://dbpedia.org/ontology/Agent")

    return types

# do search
types = retrieve("http://dbpedia.org/resource/Barack_Obama")
print("Found #types: " + str(types))
