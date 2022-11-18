# gallicaGetter

This tool wraps a few endpoints from the [Gallica API](https://api.bnf.fr/api-gallica-de-recherche).

Current endpoints are:
* 'content' : context for term occurrence and page numbers
* 'sru' : for a term, all the volumes the term appears in 
* 'text' : full text for a volume on Gallica
* 'papers' : paper titles and publishing range data
* 'issues' : years published for a paper (used internally in papers)

I developed this tool into a [graphing app](https://d32d5ops9ui5td.cloudfront.net/) similar to Google's n-gram viewer for books. 

For an exact number of occurrences over a period, use [Pyllicagram](https://github.com/regicid/pyllicagram).

# Installation

```sh
pip install gallicaGetter
```

# Content example

This wrapper pairs best with an SRU fetch since the ark code for an issue is in the SRU response.

Build the content wrapper using ```connect()```, fetch using ```get()```:
```python
import gallicaGetter

contentWrapper = gallicaGetter.connect('content')

data = contentWrapper.get(
    ark='bpt6k270178t',
    term='guerre',
)

for contentRecord in data:
    print(contentRecord.num_results)
    print(contentRecord.get_pages())
```

# SRU examples

Build the wrapper object using the ```connect()``` factory:
```python
import gallicaGetter

sruWrapper = gallicaGetter.connect('sru')
```
Then, retrieve records or counts using ```get()```.

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

Retrieve the number of volumes with >= 1 mention of "Victor Hugo" across the Gallica archive from 1800 to 1900, by year, running 30 requests in parallel.

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
Retrieve 15 issues that mention "Brazza" from 1890 to 1900.

```python
import gallicaGetter

sruWrapper = gallicaGetter.connect('sru')

records = sruWrapper.get(
    terms="Brazza",
    startDate="1890",
    endDate="1900",
    grouping="all",
    numRecords=15
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


Retrieve all issues mentioning "Paris" in the papers "Le Temps" and "Le Figaro" from 1890 to 1900.

```python
import gallicaGetter

sruWrapper = gallicaGetter.connect('sru')

recordGenerator = sruWrapper.get(
    terms="Paris",
    startDate="1890",
    endDate="1900",
    grouping="all",
    codes=["cb34431794k", "cb34355551z"]
)

for record in recordGenerator:
    print(record.getRow())
```

# Full text example

Retrieve a volume's text from its ark code. Pass a list of codes to retrieve multiple sets of text.

```python
import gallicaGetter

textWrapper = gallicaGetter.connect('text')

data = textWrapper.get('bpt6k270178t')

for textRecord in data:
    print(textRecord.get_ocr_quality())
    print(textRecord.get_text())
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
