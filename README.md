# gallicaGetter

This tool wraps a few endpoints from the Gallica API to allow multi-threaded data retrieval with support
for generators. I'll be adding much more documentation soon -- just wanted to get this out there! Pull requests welcome.

Current endpoints are:
* 'sru' -- word occurrences
* 'content' -- occurrence context and page numbers
* 'papers' -- paper metadata
* 'issues' -- years published for a given paper

The tool's functionality has evolved around my application's needs, but it should be easy to extend.

# Examples

I want to retrieve all issues that mention "Brazza" from 1890 to 1900.

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

I want to retrieve all occurrences of "Brazza" within 10 words of "Congo" in the paper "Le Temps" from 1890 to 1900.

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

Retrieve the number of occurrences of "Victor Hugo", by year, across the Gallica archive from 1800 to 1900, running 30 requests in parallel.

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
    codes=["cb34431794k", "cb3443179k"],
    generate=True
)

for i in range(10):
    print(next(recordGenerator).getRow())
```