# Carbon Offset Scraper

This script scrapes carbon offset projects from a variety of offset registries.

Currently, these are:

* [Verra (Verified Carbon Standard)](https://registry.verra.org/app/search/VCS)
* [Gold Standard](https://registry.goldstandard.org/projects?q=&page=1)
* [American Carbon Registry](https://acr2.apx.com/myModule/rpt/myrpt.asp?r=111)

The script will download projects from the registries and then create a relatively normalized CSV file containing the following fields:

* `name:` the project name
* `location:` project location
* `registry_id:` the id of the project as listed in its registry
* `registry_url:` the url of the project in the registry
* `project_url:` external project url if available
* `developer:` project developer
* `project_type:` project type
* `description:` project description
* `methodology:` project methodology
* `total_credits:` total credits issued
* `status:` project status
* `registry:` registry name

Each scraper will download temporary files in the `data` directory. These can be used to extract more specific details from each registry.

If you are interested in adding more registries, feel free to request one in the issues page. Code contributions are also welcome.

## Set up

Install the requirements with:

```
pip install -r requirements.txt
```

## Usage

To run all the scrapers:

```
python run.py

```

This will output a file called `offsets.csv` in the `data` folder.


You can also run the scrapers individually. For example, to just download Verra data:

```
python verra.py
```

## Alternatives

The [Berkeley Carbon Trading Project](https://gspp.berkeley.edu/research-and-impact/centers/cepp/projects/berkeley-carbon-trading-project/offsets-database) allows you to download a database with more complete historical data, but seems to lack project descriptions.
