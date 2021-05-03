from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph

sparql = SPARQLWrapper("http://172.17.0.1:7200/repositories/shows")


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


def show_cast(page):
    sparql.setQuery("""
    PREFIX pred: <http://shows.org/pred/>

    select ?show_name ?actor_name (group_concat(?actor_name;separator=" ; ") as ?actor_name) 
    where {
        ?show_id pred:cast ?actor_id .
        ?show_id pred:title ?show_name .
        ?actor_id pred:name ?actor_name .
    }
    group by ?show_name
    OFFSET """ + str(page * 15) + """ LIMIT 15""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results:
        data = results['results']['bindings']
        results = {}
        for d in data:
            show = d['show_name']['value']
            if show not in results:
                results[show] = []
            results[show] += [d['actor_name']['value']]
    return results


def list_actors(page, name=None):
    if name:
        sparql.setQuery("""
            PREFIX pred: <http://shows.org/pred/>

            SELECT ?actor_name ?show_name (group_concat(?show_name;separator=" ; ") as ?show_name){ 
                ?actor_id pred:name ?actor_name .
                ?actor_id pred:name '""" + name + """' .
                ?show_id pred:cast ?actor_id .
                ?show_id pred:title ?show_name .
            } 
            group by ?actor_name
            order by asc(?actor_name)
            OFFSET """ + str(page * 15) + """ LIMIT 15""")
    else:

        sparql.setQuery("""
        PREFIX pred: <http://shows.org/pred/>
    
        SELECT ?actor_name ?show_name (group_concat(?show_name;separator=" ; ") as ?show_name){ 
            ?actor_id pred:name ?actor_name .
            ?show_id pred:cast ?actor_id .
            ?show_id pred:title ?show_name .
        } 
        group by ?actor_name
        order by asc(?actor_name)
        OFFSET """ + str(page * 15) + """ LIMIT 15""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results:
        data = results['results']['bindings']
        results = {}
        for d in data:
            actors = d['actor_name']['value']
            if actors not in results:
                results[actors] = []
            results[actors] += [d['show_name']['value']]

    return results
