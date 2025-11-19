# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def read_linkedin_survey(path):
    paths = list(Path(path).iterdir())
    txt = []
    for path in paths:
        with open(path) as f:
            temp = pd.read_csv(f)
            temp.columns = temp.columns.str.lower().str.replace("_", " ").str.strip()
            txt.append(temp)
    to_concat = pd.concat(txt, ignore_index=True)
    to_concat.columns = ['first name', 'last name', 'current company',
                            'job title', 'email', 'university']
    return to_concat


def com_stats(df):
    prop_ohio_programmer = df[df["university"].str.contains("Ohio", na=False, case=False) & df["job title"].str.contains("Programmer", na=False, case=False)].shape[0] / df[df["university"].str.contains("Ohio", na=False, case=False)].shape[0]
    num_engineer = len(df[df["job title"].str.endswith("Engineer", na=False)]["job title"].unique())
    longest_title = max(df["job title"].astype(str), key=len)
    with_manager = df[df["job title"].str.contains("manager", na=False, case=False)].shape[0]
    return [prop_ohio_programmer, num_engineer, longest_title, with_manager]



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def read_student_surveys(path):
    paths = list(Path(path).iterdir())
    txt = []
    for path in paths:
        with open(path) as f:
            temp = pd.read_csv(f)
            txt.append(temp)
    df = pd.DataFrame(txt[0]) 

    for i in range(1, len(txt)):
        df = df.merge(txt[i], on="id")
    return df.set_index("id")


def check_credit(df):
    df["genre"] = df["genre"].replace("(no genres listed)", np.nan)
    above_90_ec = min(2, sum((np.array([sum(df["movie"].notna()), sum(df["genre"].notna()), sum(df["animal"].notna()), sum(df["plant"].notna()), sum(df["color"].notna())]) / df.shape[0]) >= 0.9))
    new_df = pd.DataFrame(index=df.index)
    new_df["name"] = df["name"]
    survey = df.copy().drop(columns=["name"])
    new_df["ec"] = 5 * (survey.isna().sum(axis=1) / (len(survey.columns)) < 0.5) + above_90_ec
    return new_df


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_popular_procedure(pets, procedure_history):
    pets = pets.merge(procedure_history, on="PetID", how="inner")
    return pets.groupby("ProcedureType").count()["PetID"].sort_values(ascending=False).index[0]


def pet_name_by_owner(owners, pets):
    df = pd.merge(owners, pets, on="OwnerID", how="left")
    df = df.rename(columns={"Name_x": "Owner"})
    df = df.rename(columns={"Name_y": "Pet"})
    return pd.DataFrame(df.groupby(["OwnerID", "Owner"])["Pet"].agg(lambda x: list(x) if len(x) > 1 else x.iloc[0])).reset_index().drop(columns="OwnerID").set_index("Owner")["Pet"]


def total_cost_per_city(owners, pets, procedure_history, procedure_detail):
    x = pd.merge(owners, pets, on="OwnerID", how="left")
    y = pd.merge(x, procedure_history, on="PetID", how="inner")
    z = pd.merge(y, procedure_detail, on="ProcedureSubCode", how="left")
    return z.groupby("City")["Price"].sum().reindex(owners["City"].unique(), fill_value=0)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def average_seller(df):
    df = pd.DataFrame(df.groupby("Name")["Total"].mean())
    df = df.rename(columns={"Total": "Average Sales"})
    return df

def product_name(df):
    temp = df.pivot_table(index="Name",columns="Product",values="Total", aggfunc="sum")
    return temp

def count_product(df):
    return df.pivot_table(index=["Product", "Name"],columns="Date",values="Total", aggfunc="count").fillna(0).astype(int)

def total_by_month(df):
    return df.pivot_table(index=["Name", "Product"],columns=pd.to_datetime(df["Date"]).dt.month_name(),values="Total", aggfunc="sum").fillna(0).astype(int)
