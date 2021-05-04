from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph

sparql = SPARQLWrapper("http://172.17.0.1:7200/repositories/shows")


def list_shows(page, name=None):

    if name is None:
        name = ""

    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename ?directorname
        WHERE {
            ?show pred:title ?title .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            ?show pred:director ?director .
            ?director pred:name ?directorname .
            FILTER regex(?title, '""" + name + """' , "i") .
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


def list_directors(page, name=None):
    if name is None:
        name = ""

    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?directorname ?title
        WHERE {
            ?show pred:director ?director .
            ?director pred:name ?directorname .
            ?show pred:title ?title .
            FILTER regex(?directorname, '""" + name + """' , "i") .
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


def list_actors(page, name=None):
    if name is None:
        name = ""

    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>
        SELECT ?actorname ?title 
        WHERE {
            ?show pred:cast ?actor .
            ?actor pred:name ?actorname .
            ?show pred:title ?title .
            FILTER regex(?actorname, '""" + name + """' , "i") .
            }   OFFSET """ + str(page * 30) + """ LIMIT 30
        """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                actor = d['actorname']['value']
                if actor not in results:
                    results[actor] = []
                results[actor] += [d['title']['value']]
        return results
    except Exception:
        return None


def person_detail(name):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename ?directorname
        WHERE {
            ?director pred:name """ + "\"" + name + "\"" + """ .
            ?show pred:director ?director .
            ?show pred:director ?other_director .
            ?other_director pred:name ?directorname .
            ?show pred:title ?title .
            ?show pred:type ?type .
            ?type pred:type ?typename .
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
                if title not in results1:
                    results1[title] = {'type': d['typename']['value'], 'directors': []}
                if director not in results1[title]['directors'] and director != name:
                    results1[title]['directors'] += [director]
    except Exception:
        results1 = None

    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename ?castname
        WHERE {
            ?actor pred:name """ + "\"" + name + "\"" + """ .
            ?show pred:cast ?actor .
            ?show pred:cast ?other_actor .
            ?other_actor pred:name ?castname .
            ?show pred:title ?title .
            ?show pred:type ?type .
            ?type pred:type ?typename .
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
                cast = d['castname']['value']
                if title not in results2:
                    results2[title] = {'type': d['typename']['value'], 'cast': []}
                if cast not in results2[title]['cast'] and cast != name:
                    results2[title]['cast'] += [cast]
    except Exception:
        results2 = None
    return results1, results2


def show_detail(title):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?typename ?countryname ?description ?date_added ?release_yearname ?durationname ?listed_inname ?directorname ?castname
        WHERE {
            ?show pred:title """ + "\"" + title + "\"" + """ .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            ?show pred:country ?country .
            ?country pred:country ?countryname .
            ?show pred:description ?description .
            ?show pred:date_added ?date_added .
            ?show pred:release_year ?release_year .
            ?release_year pred:release_year ?release_yearname .
            ?show pred:duration ?duration .
            ?duration pred:duration ?durationname .
            ?show pred:listed_in ?listed_in .
            ?listed_in pred:listed_in ?listed_inname .
            ?show pred:director ?director .
            ?director pred:name ?directorname .
            ?show pred:cast ?cast .
            ?cast pred:name ?castname .
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for i, d in enumerate(data):
                if i == 0:
                    results = {'type': d['typename']['value'],
                               'country': d['countryname']['value'],
                               'description': d['description']['value'],
                               'date_added': d['date_added']['value'],
                               'release_year': d['release_yearname']['value'],
                               'duration': d['durationname']['value'],
                               'listed_in': d['listed_inname']['value'],
                               'directors': [],
                               'cast': []}
                director = d['directorname']['value']
                cast = d['castname']['value']
                if director not in results['directors']:
                    results['directors'] += [director]
                if cast not in results['cast']:
                    results['cast'] += [cast]
        return results
    except Exception:
        return None
