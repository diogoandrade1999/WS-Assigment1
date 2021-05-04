# WS-Assigment1

## Create Repository in GraphDB
* Setup > Repositories > Create new repository > GraphDB Free
    - Repository ID: shows
    - Ruleset: No inference

## Import data in GraphDB
* Import > RDF > Import RDF files
    - data/shows.nt
    - Import

### URL Repository
* http://192.168.59.219:7200/repositories/shows


## USAGE Conversor csv to nt
```bash
$ python3 conversor/conversor.py -f data/shows.csv
```