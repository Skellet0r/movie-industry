# Jupyter Notebooks

Refer to the [Project Charter](../docs/project/charter.md) for a comprehensive overview
of this project's purpose.

## Exploration Guide

As per our Project Charter, our first step will be to develop an exploration guide.  

As a measure to guide our analysis/exploration we will be inspecting the following
features of the film industry:

- Genre
- Runtime
- Budget Allocation
- Release Window
- Director

To inspect the above features we will be working with the following raw datasets: 

- rt.movie_info
- imdb.title.basics
- tn.movie_budgets
- imdb.title.crew
- imdb.name.basics

## Notebooks

1. [Create Raw Dictionaries](./01-eamor-create-raw-data-dictionary.ipynb): Create the raw
   data-dictionary as one wasn't supplied to us.
2. [Data Cleaning](./02-eamor-data-cleaning.ipynb): clean up the datasets we will use for
   exploration.
3. [Data Exploration](./03-eamor-data-exploration.ipynb): exploring our cleaned dataset
   inspecting the features of the film industry defined in our exploration guide.