# import our required libraries
import os
import pandas as pd
import numpy as np
import cpi
from src.tools import currency_string_to_float
from pathlib import Path
from warnings import filterwarnings

filterwarnings("ignore")


# create a function to adjust for inflation
def inf_adjust(values, years):
    """Adjusts an array of values for inflation

    :values: array of value in USD
    :years: years of the values

    :return: array of inflation adjusted values"""
    results = []
    for value, year in zip(values, years):
        try:
            result = cpi.inflate(value, year)
            results.append(result)
        except cpi.errors.CPIObjectDoesNotExist:
            if year > cpi.LATEST_YEAR:
                results.append(value)
            else:
                results.append(np.nan)
    return results



def make_dataset():

    project_dir = Path(__file__).resolve().parents[1]
    os.chdir(os.path.join(project_dir, "data"))

    ## tn.movie_budgets.csv.bz2

    # import our dataset, display info and head
    tn_movie_budgets = pd.read_csv("./raw/tn.movie_budgets.csv.bz2")

    # convert release_date to a datetime instance
    tn_movie_budgets.release_date = pd.to_datetime(tn_movie_budgets.release_date)

    # convert our budget and gross columns to float
    cols_to_convert = ['production_budget', 'domestic_gross', 'worldwide_gross']
    result = tn_movie_budgets[cols_to_convert].applymap(currency_string_to_float)
    tn_movie_budgets.loc[:, cols_to_convert] = result

    # finally drop the id column
    tn_movie_budgets.drop(columns="id", errors="ignore", inplace=True)


    ## tmdb.movies.csv.bz2

    # import our dataset, display info and head
    tmdb_movies = pd.read_csv("./raw/tmdb.movies.csv.bz2")

    # keep only original_title and title, and release date
    keep_cols = ['original_title', 'title', 'release_date']
    tmdb_movies = tmdb_movies[keep_cols]

    # convert our datetime column
    tmdb_movies.release_date = pd.to_datetime(tmdb_movies.release_date)

    # combine our two title columns, exlode them
    tmdb_movies["title_tup"] = tmdb_movies.apply(lambda row: (row[0], row[1]), axis=1)
    tmdb_movies = tmdb_movies.explode("title_tup")[["title_tup", "release_date"]]

    # drop duplicates and rename columns
    tmdb_movies.drop_duplicates(inplace=True)
    tmdb_movies.rename(columns={"title_tup": "title"}, inplace=True)


    ## imdb.title.crew.csv.bz2

    # load our dataset
    imdb_title_crew = pd.read_csv("./raw/imdb.title.crew.csv.bz2")

    # drop writers column, convert each directors to list of str
    imdb_title_crew.drop(columns="writers", inplace=True, errors="ignore")
    imdb_title_crew.directors = imdb_title_crew.directors.str.split(",")

    # explode the directors column and drop nan rows
    imdb_title_crew = imdb_title_crew.explode("directors")
    imdb_title_crew.dropna(inplace=True)


    ## imdb.name.basics.csv.bz2

    # load and display our data
    imdb_name_basics = pd.read_csv("./raw/imdb.name.basics.csv.bz2")


    # We'll drop all columns except for nconst and primary_name. We could keep just those who have director in their primary profession, but we will be joining later, so it would be wasteful.

    # keep only nconst and primary name columns
    imdb_name_basics = imdb_name_basics[["nconst", "primary_name"]]


    # ## imdb.title.basics.csv.bz2

    # import and load our data
    imdb_title_basics = pd.read_csv("./raw/imdb.title.basics.csv.bz2")

    # make tuple of title and split genre into a list
    imdb_title_basics["title_tup"] = imdb_title_basics.apply(
        lambda row: (row[1], row[2]), axis=1
    )
    imdb_title_basics.genres = imdb_title_basics.genres.str.split(",")

    # explode title_tup, and genres col
    imdb_title_basics = imdb_title_basics.explode("title_tup")
    imdb_title_basics = imdb_title_basics.explode("genres")

    # drop columns primary_title and original_title and drop duplicates
    imdb_title_basics.drop(
        columns=["primary_title", "original_title"], inplace=True, errors="ignore"
    )
    imdb_title_basics.drop_duplicates(inplace=True)


    ## Merging Our Data

    # We'll first merge title_basics with title_crew on tconst, then the results dataframe with name_basics on directors=nconst.
    # In all cases we'll do a left join to maintain the title_basics data.


    # merge title_basics and title_crew and name_basics
    imdb_crew_title_2 = pd.merge(
        imdb_title_basics, imdb_title_crew, how="left", on="tconst"
    )
    imdb = pd.merge(
        imdb_crew_title_2,
        imdb_name_basics,
        how="left",
        left_on="directors",
        right_on="nconst",
    )

    # drop tconst, nconst, directors, and rename title_tup, and primary_name columns
    imdb.drop(columns=["tconst", "directors", "nconst"], inplace=True, errors="ignore")
    imdb.rename(columns={"primary_name": "director", "title_tup": "title"}, inplace=True)



    # tmdb add release year column, join the two datasets, and drop start_year and release_year cols
    tmdb_movies["release_year"] = tmdb_movies.release_date.dt.year
    imdb_tmdb = pd.merge(
        imdb,
        tmdb_movies,
        how="left",
        left_on=["title", "start_year"],
        right_on=["title", "release_year"],
    )
    imdb_tmdb.drop(columns=["start_year", "release_year"], inplace=True, errors="ignore")


    # try joining on both release_date and movie
    merging_on_title = pd.merge(
        tn_movie_budgets,
        imdb_tmdb,
        how="left",
        left_on=["movie"],
        right_on=["title"],
    )
    
    # inflation adjustment
    
    # combine our domestic and worldwide gross into total_gross
    merging_on_title["total_gross"] = (
        merging_on_title.domestic_gross + merging_on_title.worldwide_gross
    )
    
    # create a year column 
    merging_on_title["release_year"] = merging_on_title.release_date_x.dt.year
    
    # adjust total_gross and production budget
    merging_on_title["adj_total_gross"] = inf_adjust(merging_on_title.total_gross, merging_on_title.release_year)
    merging_on_title["adj_prod_budget"] = inf_adjust(merging_on_title.production_budget, merging_on_title.release_year)


    # create a profit column by subtracting budget from (worldwide gross + domestic_gross)
    merging_on_title["profit"] = merging_on_title.adj_total_gross - merging_on_title.adj_prod_budget
    merging_on_title["profit_margin"] = (
        merging_on_title.profit / merging_on_title.adj_prod_budget
    )

    # finalize our data
    cols_to_keep = [
        "movie",
        "adj_prod_budget",
        "profit",
        "profit_margin",
        "release_date_x",
        "runtime_minutes",
        "genres",
        "director",
    ]
    cleaned_data = merging_on_title[cols_to_keep]
    cleaned_data.rename(columns={"release_date_x": "release_date", "adj_prod_budget": "production_budget"}, inplace=True)

    # export our data
    cleaned_data.to_csv("./interim/cleaned_data.csv", index=False)


if __name__ == "__main__":
    make_dataset()