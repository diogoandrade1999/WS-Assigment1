from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph


sparql = SPARQLWrapper("http://192.168.59.219:7200/repositories/shows")


def list_shows(page):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT DISTINCT ?title ?typename ?directorname
        WHERE {
            ?show pred:title ?title .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            ?show pred:director ?director .
            ?director pred:name ?directorname .
        } OFFSET """ + str(page * 15) + """ LIMIT 15
    """)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()
    if results:
        results = results['results']['bindings']
    return results


def list_directors(page):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?directorname ?title
        WHERE {
            ?show pred:director ?director .
            ?director pred:name ?directorname .
            ?show pred:title ?title .
        } OFFSET """ + str(page * 15) + """ LIMIT 15
    """)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()
    if results:
        data = results['results']['bindings']
        results = {}
        for d in data:
            director = d['directorname']['value']
            if director not in results:
                results[director] = []
            results[director] += [d['title']['value']]
    return results
