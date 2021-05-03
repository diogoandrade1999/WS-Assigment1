from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph


sparql = SPARQLWrapper("http://192.168.59.219:7200/repositories/shows")


def list_shows(page):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename ?directorname
        WHERE {
            ?show pred:title ?title .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            ?show pred:director ?director .
            ?director pred:name ?directorname .
        } OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                title = d['title']['value']
                if title not in results:
                    results[title] = {'type': d['typename']['value'], 'directors': []}
                results[title]['directors'] += [d['directorname']['value']]
        return results
    except Exception:
        return None


def list_directors(page):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?directorname ?title
        WHERE {
            ?show pred:director ?director .
            ?director pred:name ?directorname .
            ?show pred:title ?title .
        } OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
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
    except Exception:
        return None

def person_detail(name):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename ?directorname ?castname
        WHERE {
            ?director pred:name """ + "\"" + name + "\"" + """ .
            ?show pred:director ?director .
            ?show pred:director ?directors .
            FILTER (?director != ?directors)
            ?directors pred:name ?directorname .
            ?show pred:title ?title .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            ?show pred:cast ?cast .
            ?cast pred:name ?castname .
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results1 = {}
            for d in data:
                title = d['title']['value']
                director = d['directorname']['value']
                cast = d['castname']['value']
                if title not in results1:
                    results1[title] = {'type': d['typename']['value'], 'directors': [] , 'cast': []}
                if director not in results1[title]['directors']:
                    results1[title]['directors'] += [director]
                if cast not in results1[title]['cast']:
                    results1[title]['cast'] += [cast]
    except Exception:
        results1 = None

    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename ?directorname ?castname
        WHERE {
            ?actor pred:name """ + "\"" + name + "\"" + """ .
            ?show pred:cast ?actor .
            ?show pred:cast ?cast .
            FILTER (?actor != ?cast)
            ?cast pred:name ?castname .
            ?show pred:title ?title .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            ?show pred:director ?director .
            ?director pred:name ?directorname .
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results2 = {}
            for d in data:
                title = d['title']['value']
                director = d['directorname']['value']
                cast = d['castname']['value']
                if title not in results2:
                    results2[title] = {'type': d['typename']['value'], 'directors': [] , 'cast': []}
                if director not in results2[title]['directors']:
                    results2[title]['directors'] += [director]
                if cast not in results2[title]['cast']:
                    results2[title]['cast'] += [cast]
    except Exception:
        results2 = None
    return results1, results2


def show_detail(page):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename ?directorname
        WHERE {
            ?show pred:title ?title .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            ?show pred:director ?director .
            ?director pred:name ?directorname .
        } OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = []
            for d in data:
                results += [{'title': d['title']['value'], 'director': d['directorname']['value'], 'type': d['typename']['value']}]
        return results
    except Exception:
        return None
