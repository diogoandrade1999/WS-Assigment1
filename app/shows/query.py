from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph


sparql = SPARQLWrapper("http://172.17.0.1:7200/repositories/shows")


def count_shows():
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT (COUNT(?title) AS ?nshows)
        WHERE {
            ?show pred:title ?title .
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            results = int(results['results']['bindings'][0]['nshows']['value'])
        return results
    except Exception:
        return 0


def list_shows(page):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename ?release_yearname (GROUP_CONCAT(?countryname;SEPARATOR=",") AS ?countriesname) (GROUP_CONCAT(?listed_inname;SEPARATOR=",") AS ?listedname) 
        WHERE {
            ?show pred:title ?title .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            ?show pred:country ?country .
            ?country pred:country ?countryname .
            ?show pred:listed_in ?listed_in .
            ?listed_in pred:listed_in ?listed_inname .
            ?show pred:release_year ?release_year .
            ?release_year pred:release_year ?release_yearname .
        } GROUP BY ?title ?typename ?release_yearname OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                title = d['title']['value']
                results[title] = {'type': d['typename']['value'],
                                'countries': list(set(d['countriesname']['value'].split(','))),
                                'listed_in': list(set(d['listedname']['value'].split(','))),
                                'release_year': d['release_yearname']['value'],
                                }
        return results
    except Exception:
        return None


def list_shows_type():
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT DISTINCT ?typename
        WHERE {
            ?show pred:type ?type .
            ?type pred:type ?typename .
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = []
            for d in data:
                results += [d['typename']['value']]
        return results
    except Exception:
        return None


def list_shows_countries():
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT DISTINCT ?countryname
        WHERE {
            ?show pred:country ?country .
            ?country pred:country ?countryname .
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = []
            for d in data:
                results += [d['countryname']['value']]
        return results
    except Exception:
        return None


def list_shows_listed_in():
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT DISTINCT ?listed_inname
        WHERE {
            ?show pred:listed_in ?listed_in .
            ?listed_in pred:listed_in ?listed_inname .
        }
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = []
            for d in data:
                results += [d['listed_inname']['value']]
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


def list_actors(page):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?actorname ?title
        WHERE {
            ?show pred:cast ?actor .
            ?actor pred:name ?actorname .
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

        SELECT ?title ?typename
            (GROUP_CONCAT(DISTINCT ?directorname;SEPARATOR=";") AS ?directorsname)
            (GROUP_CONCAT(DISTINCT ?countryname;SEPARATOR=";") AS ?countriesname)
        WHERE {
            ?person pred:name """ + "\"" + name + "\"" + """ .
            OPTIONAL {
                ?show pred:director ?person .
                ?show pred:director ?director .
                ?director pred:name ?directorname .
                ?show pred:title ?title .
                ?show pred:type ?type .
                ?type pred:type ?typename .
                ?show pred:country ?country .
                ?country pred:country ?countryname .
            }
        } GROUP BY ?title ?typename
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results1 = {}
            for d in data:
                if 'title' in d:
                    title = d['title']['value']
                    directors = d['directorsname']['value']
                    if directors != "":
                        directors = directors.split(';')
                        directors.remove(name)
                    results1[title] = {'type': d['typename']['value'],
                                    'countries': d['countriesname']['value'].split(';'),
                                    'directors': directors
                                    }
    except Exception:
        results1 = None

    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename
            (GROUP_CONCAT(DISTINCT ?actorname;SEPARATOR=";") AS ?castname)
            (GROUP_CONCAT(DISTINCT ?countryname;SEPARATOR=";") AS ?countriesname)
        WHERE {
            ?person pred:name """ + "\"" + name + "\"" + """ .
            OPTIONAL {
                ?show pred:cast ?person .
                ?show pred:cast ?actor .
                ?actor pred:name ?actorname .
                ?show pred:title ?title .
                ?show pred:type ?type .
                ?type pred:type ?typename .
                ?show pred:country ?country .
                ?country pred:country ?countryname .
            }
        } GROUP BY ?title ?typename
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results2 = {}
            for d in data:
                if 'title' in d:
                    title = d['title']['value']
                    cast = d['castname']['value']
                    if cast != "":
                        cast = cast.split(';')
                        cast.remove(name)
                    results2[title] = {'type': d['typename']['value'],
                                       'countries': d['countriesname']['value'].split(';'),
                                       'cast': cast
                                       }
    except Exception:
        results2 = None
    return results1, results2


def show_detail(title):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?typename ?description ?date_added ?release_yearname ?durationname
            (GROUP_CONCAT(DISTINCT ?countryname;SEPARATOR=";") AS ?countriesname)
            (GROUP_CONCAT(DISTINCT ?listed_inname;SEPARATOR=";") AS ?listedname)
            (GROUP_CONCAT(DISTINCT ?directorname;SEPARATOR=";") AS ?directorsname)
            (GROUP_CONCAT(DISTINCT ?actorname;SEPARATOR=";") AS ?castname)
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
            OPTIONAL {
                ?show pred:director ?director .
                ?director pred:name ?directorname .
            }
            OPTIONAL {
                ?show pred:cast ?actor .
                ?actor pred:name ?actorname .
            }
        } GROUP BY ?typename ?description ?date_added ?release_yearname ?durationname
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            for d in data:
                directors = d['directorsname']['value']
                if directors != "":
                    directors = directors.split(';')
                cast = d['castname']['value']
                if cast != "":
                    cast = cast.split(';')
                results = {'type': d['typename']['value'],
                            'description': d['description']['value'],
                            'date_added': d['date_added']['value'],
                            'release_year': d['release_yearname']['value'],
                            'duration': d['durationname']['value'],
                            'countries': d['countriesname']['value'].split(';'),
                            'listed_in': d['listedname']['value'].split(';'),
                            'directors': directors,
                            'cast': cast
                            }
        return results
    except Exception:
        return None


def search_shows(page, title, types_list, countries_list, listed_in_list):
    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>

        SELECT ?title ?typename ?release_yearname (GROUP_CONCAT(?countryname;SEPARATOR=",") AS ?countriesname) (GROUP_CONCAT(?listed_inname;SEPARATOR=",") AS ?listedname) 
        WHERE {
            ?show pred:title ?title .
            FILTER regex(str(?title), """ + "\"" + title + "\"" + """, "i") .
            ?show pred:type ?type .
            ?type pred:type ?typename .
            FILTER (?typename in (""" + '"' + '\", \"'.join(types_list) + '"' + """))
            ?show pred:country ?country .
            ?country pred:country ?countryname .
            FILTER (?countryname in (""" + '"' + '\", \"'.join(countries_list) + '"' + """))
            ?show pred:listed_in ?listed_in .
            ?listed_in pred:listed_in ?listed_inname .
            FILTER (?listed_inname in (""" + '"' + '\", \"'.join(listed_in_list) + '"' + """))
            ?show pred:release_year ?release_year .
            ?release_year pred:release_year ?release_yearname .
        } GROUP BY ?title ?typename ?release_yearname OFFSET """ + str(page * 30) + """ LIMIT 30
    """)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        if results:
            data = results['results']['bindings']
            results = {}
            for d in data:
                title = d['title']['value']
                results[title] = {'type': d['typename']['value'],
                                'countries': list(set(d['countriesname']['value'].split(','))),
                                'listed_in': list(set(d['listedname']['value'].split(','))),
                                'release_year': d['release_yearname']['value'],
                                }
        return results
    except Exception as e:
        print(e)
        return None


def insert(subject, predicate, object):

    sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>
        Insert DATA {
        pred:""" + subject + """ pred:""" + predicate + """ '""" + object + """' .
        }
    """)

    return
