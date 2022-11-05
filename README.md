# gallicaGetter

This tool wraps a few endpoints from the [Gallica API](https://api.bnf.fr/api-gallica-de-recherche) to allow multi-threaded data retrieval with support
for generators. Go ahead, explore some archived French periodicals, and a few international editions too!

I developed this tool into a [graphing app](https://d32d5ops9ui5td.cloudfront.net/) similar to Google's n-gram viewer for books. 

I owe inspiration for part of the API integration to queries written by the team at [Gallicagram](https://shiny.ens-paris-saclay.fr/app/gallicagram). 



Current endpoints are:
* 'sru' -- for a term, get the number of occurrences over a time range or fetch all the periodical issues the term appears in. 
* 'content' -- occurrence context and page numbers
* 'papers' -- paper titles and publishing range data, from their Gallica codes
* 'issues' -- years published for a given paper (used internally in papers)

# Installation

```sh
pip install gallicaGetter
```
# SRU quickstart

Build the wrapper object using the ```connect()``` factory:
```python
import gallicaGetter

sruWrapper = gallicaGetter.connect('sru')
```
Then, retrieve records or counts using ```get()```. Parameters are built into queries to the Gallica API.

```get(terms, generate=False, **kwargs)```

PARAMETERS:
* **terms**: a string, or list of strings, to search for.
* **startDate**: lower year boundary for the search.
* **endDate**: upper year boundary for the search.
* **codes**: string paper codes to restrict the search. Can be found in the URL of a Gallica periodical's page.
* **grouping**: 'year', 'month', or 'all'
* **generate**: if True, returns a generator object. Otherwise, returns a list of results.
* **linkTerm**: a string that restricts the search to occurrences within its proximity. 
* **linkDistance**: proximity distance in words.

# SRU Examples

Retrieve the number of occurrences of "Victor Hugo" across the Gallica archive from 1800 to 1900, by year, running 30 requests in parallel.

```python
import gallicaGetter

sruWrapper = gallicaGetter.connect('sru', numWorkers=30)

records = sruWrapper.get(
    terms="Victor Hugo",
    startDate="1800",
    endDate="1900",
    grouping="year"
)

for record in records:
    print(record.getRow())
```
Retrieve all issues that mention "Brazza" from 1890 to 1900.

```python
import gallicaGetter

sruWrapper = gallicaGetter.connect('sru')

records = sruWrapper.get(
    terms="Brazza",
    startDate="1890",
    endDate="1900",
    grouping="all"
)

for record in records:
    print(record.getRow())
```

Retrieve all occurrences of "Brazza" within 10 words of "Congo" in the paper "Le Temps" from 1890 to 1900.

```python
import gallicaGetter

sruWrapper = gallicaGetter.connect('sru')

records = sruWrapper.get(
    terms="Brazza",
    startDate="1890",
    endDate="1900",
    linkTerm="Congo",
    linkDistance=10,
    grouping="all",
    codes="cb34431794k"
)

for record in records:
    print(record.getRow())
```


Retrieve all issues mentioning "Paris" in the papers "Le Temps" and "Le Figaro" from 1890 to 1900, using
a generator.

```python
import gallicaGetter

sruWrapper = gallicaGetter.connect('sru')

recordGenerator = sruWrapper.get(
    terms="Paris",
    startDate="1890",
    endDate="1900",
    grouping="all",
    codes=["cb34431794k", "cb34355551z"],
    generate=True
)

for i in range(10):
    print(next(recordGenerator).getRow())
```



# Content example

This wrapper pairs best with an SRU fetch since the ark code for an issue is in the SRU response.

Retrieve text context for all occurrences of "guerre" in an issue of the Figaro.
```python
import gallicaGetter

contentWrapper = gallicaGetter.connect('content')

data = contentWrapper.get(
    ark='bpt6k270178t',
    term='guerre',
)

for numOccurrences, pages in data:
    print(numOccurrences, pages)
```
# Papers example

Retrieve metadata from a Gallica periodical's code. Example for "Le Temps":

```python
import gallicaGetter

papersWrapper = gallicaGetter.connect('papers')

metadata = papersWrapper.get('cb34431794k')

for record in metadata:
    print(record.getRow())
    print(record.isContinuous())
```

# Issues example

The papers wrapper calls this internally, but it might be useful. For a paper code, retrieve all years with at least one issue archived on Gallica. 

```python
import gallicaGetter

issuesWrapper = gallicaGetter.connect('issues')

years = issuesWrapper.get('cb34431794k')
```
