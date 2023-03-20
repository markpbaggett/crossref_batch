=================
UTK Crossref DOIs
=================

While there are probably countless ways to find all your current DOIs, I keep a list of them online
`here <https://docs.google.com/spreadsheets/d/19QYrRR5SjOeWxS2H3yGCnm08jTaPEYJJu_Z21JCzYeA/edit#gid=178917582>`_.

To generate this, I write a script like this that just gives me the answer as JSON. Note that this assumes there are less
than 1000.

.. code-block:: python

    import requests
    import json

    headers = {
        'User-Agent': 'Mark Baggett (University of Tennessee)',
        'From': 'mbagget1@utk.edu'
    }

    request_string = "http://api.crossref.org/members/12952/works?rows=1000"

    r = requests.get(request_string, headers=headers)
    results = r.json()

    with open("sample.json", "w") as outfile:
        json.dump(results, outfile)

Then, to get this info into a spreadsheet, I run a script like this that prescribes the shape I want the CSV in:

.. code-block:: python

    import json
    import csv

    all_dois = []
    headers = ('title', 'doi', 'url', 'type', 'referenced-count', 'referenced-by', 'created')

    with open('sample.json', 'r') as sample:
        data = json.load(sample)

    for item in data['message']['items']:
        current = {
            "title": item.get('title', [''])[0],
            "doi": item['DOI'],
            "url": item['URL'],
            "type": item.get('type'),
            "referenced-count": item['reference-count'],
            "referenced-by": item['is-referenced-by-count'],
            "created": item['created']['date-time']
        }
        all_dois.append(current)

    with open('output.csv', mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in all_dois:
            writer.writerow(row)

I then upload the CSV to Google Drive.
