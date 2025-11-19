# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def trick_me():
    return 3


def trick_bool():
    return [4, 10, 13]


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def population_stats(df):
    num_non_nulls = df.notna().sum()
    prop_non_nulls = df.notna().sum() / df.isna().count() 
    num_distinct = df.nunique()
    prop_num_distinct = df.nunique() / df.isna().count()
    return pd.DataFrame({"num_nonnull": num_non_nulls, "prop_nonnull": prop_non_nulls, "num_distinct": num_distinct, "prop_distinct": prop_num_distinct})


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_common(df, N):
    new_df = pd.DataFrame()
    for col in df.columns:
        values = df[col].value_counts(ascending=False)
        n_values = values.iloc[:N]
        updated_col_values = list(n_values.index)
        updated_col_counts = list(n_values.values)
        if(len(n_values) < N):
            null_count = N - len(n_values)
            updated_col_values = list(n_values.index) + [np.nan] * null_count
            updated_col_counts = list(n_values.values) + [np.nan] * null_count
        new_df[f'{col}_values'] = updated_col_values
        new_df[f'{col}_counts'] = updated_col_counts
    return new_df

# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def super_hero_powers(df):
    df = pd.DataFrame(df)
    name = df.groupby('hero_names').sum().sum(axis=1).sort_values(ascending=False).index[0]
    most_common_fly = df[df.get("Flight") == True].groupby("hero_names").sum().sum().sort_values(ascending=False).drop('Flight').index[0]
    most_common_one = df[(df.groupby('hero_names').sum().sum(axis=1) == 1).reset_index(drop=True)].groupby("hero_names").sum().sum().sort_values(ascending=False).index[0]
    return [name, most_common_fly, most_common_one]



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def clean_heroes(df):
    df = df.replace(-99, np.nan).replace("-", np.nan).replace("", np.nan)
    return df


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def super_hero_stats():
    return ["Onslaught", "George Lucas", "bad", "Marvel Comics", "NBC - Heroes", "Groot"]

# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def clean_universities(universities):
    universities.get("institution").str.replace("\n", ", ")
    universities['broad_impact'] = universities['broad_impact'].astype(int)
    new_national_rankings = universities.get("national_rank").str.split(", ")
    temp_df = pd.DataFrame(new_national_rankings.tolist(), columns=["national", "national_rankings_cleaned"])
    universities["nation"] = temp_df.get("national")
    universities["national_rank_cleaned"] = temp_df.get("national_rankings_cleaned").astype(int)
    universities = universities.drop(columns=["national_rank"])
    universities["is_r1_public"] = (universities.get("control") == "Public") & (universities.get("control").notna() == True) & (universities.get("city").notna() == True) & (universities.get("state").notna() == True)
    universities["nation"] = universities.get("nation").str.replace("UK", "United Kingdom").str.replace("USA", "United States").str.replace("Czechia", "Czech Republic")
    return universities

def university_info(cdf):
    greater_than_three = cdf["state"].value_counts()
    greater_than_three = greater_than_three[greater_than_three >= 3].index
    new_cdf = cdf[cdf["state"].isin(greater_than_three)]
    first = new_cdf.groupby("state")["score"].mean().sort_values(ascending=True).index[0]

    second = cdf[(cdf['world_rank'] <= 100) & (cdf["quality_of_faculty"] <= 100)].shape[0] / cdf[cdf['world_rank'] <= 100].shape[0]

    private_unis = cdf[cdf["is_r1_public"] == False]["state"].value_counts().sort_index()
    total = cdf["state"].value_counts().sort_index()
    prop = private_unis/total
    count = len(prop[prop >= 0.5])
    
    lowest_rank = cdf[cdf['national_rank_cleaned'] == 1].sort_values("world_rank", ascending=False).iloc[0]["institution"]
    return [first, second, count, lowest_rank]
    

