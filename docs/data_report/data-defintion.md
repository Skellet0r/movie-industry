# Data and Feature Definitions

This document provides a central hub for the raw data sources, the processed/transformed
data, and feature sets. More details of each dataset is provided in the data summary
report. 

## Raw Data Sources

| Raw Dataset Name | Dataset Size (MB) |
| ---:| ---: |
| bom.movie_gross.csv.bz2 | 1 |
| imdb.name.basics.csv.bz2 | 13 |
| imdb.title.akas.csv.bz2 | 5 |
| imdb.title.basics.csv.bz2 | 3 |
| imdb.title.crew.csv.bz2 | 2 |
| imdb.title.principals.csv.bz2 | 9 |
| imdb.title.ratings.csv.bz2 | 1 |
| rt.movie_info.tsv.bz2 | 1 |
| rt.reviews.tsv.bz2 | 3 |
| tmdb.movies.csv.bz2 | 1 |
| tn.movie_budgets.csv.bz2 | 1 |

## Interim Data
| Interim Dataset Name | Input Dataset(s)   | Data Processing Tools/Scripts |
| ---:| ---: | ---: |
| cleaned_data.csv | [data_directory](../../data)| [make_dataset](../../src/make_dataset.py) | 

* cleaned_data.csv summary: This is the data that will be used during data exploration. Processed the data to a single flat file, for a simpler
  import and analysis.

