# lab.py


import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm
from pathlib import Path
from sklearn.preprocessing import Binarizer, QuantileTransformer, FunctionTransformer
import itertools

import warnings
warnings.filterwarnings('ignore')


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def best_transformation():
    return 1


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------



def create_ordinal(df):
    r_df = pd.DataFrame()
    cut_encoded = {"Fair": 0, "Good": 1, "Very Good": 2, "Premium": 3, "Ideal": 4}
    color_encoded = {"J": 0, "I": 1, "H": 2, "G": 3, "F": 4, "E": 5, "D": 6}
    clarity_encoded = {"I1": 0, "SI2": 1, "SI1": 2, "VS2": 3, "VS1": 4, "VVS2": 5, "VVS1": 6, "IF": 7}
    r_df["ordinal_cut"] = df["cut"].map(cut_encoded)
    r_df["ordinal_color"] = df["color"].map(color_encoded)
    r_df["ordinal_clarity"] = df["clarity"].map(clarity_encoded)
    return r_df


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------



def create_one_hot(df):
    r_df = pd.DataFrame()
    def one_hot(df, col):
        for val in df[col].unique():
            r_df[f"one_hot_{col}_{val}"] = (df[col] == val).astype(int)

    categorical = ["cut", "color", "clarity"]
    for cat in categorical:
        one_hot(df, cat)
    return r_df


def create_proportions(df):
    r_df = pd.DataFrame()
    categorical = ["cut", "color", "clarity"]
    for cat in categorical:
        prop = dict(df[cat].value_counts() / len(df[cat]))
        r_df[f"proportion_{cat}"] = df[cat].map(prop)
    return r_df


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def create_quadratics(df):
    r_df = pd.DataFrame()
    quantitative = ["carat", "depth", "table", "x", "y", "z"]
    combinations = list(itertools.combinations(quantitative, 2))
    for com in combinations:
        r_df[f"{com[0]} * {com[1]}"] = df[com[0]] * df[com[1]]
    return r_df


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------



def comparing_performance():
    # create a model per variable => (variable, R^2, RMSE) table
    return [0.8493305264354858, 1548.5331930613174, "x", "carat * x", "one_hot_clarity_SI2", 1434.8400089047336]


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


class TransformDiamonds(object):
    
    def __init__(self, diamonds):
        self.data = diamonds
        
    # Question 6.1
    def transform_carat(self, data):
        bi = Binarizer(threshold=1)
        return bi.transform(data[["carat"]])
    
    # Question 6.2
    def transform_to_quantile(self, data):
        qt = QuantileTransformer(n_quantiles=100, output_distribution="uniform")
        qt.fit(self.data[["carat"]])
        return qt.transform(data[["carat"]])
    
    # Question 6.3
    def transform_to_depth_pct(self, data):
        def compute_depth(_arr):
            df = pd.DataFrame(_arr)
            denominator = (df[0] + df[1])
            denominator[denominator == 0] = np.nan
            return ((2*df[2] / denominator) * 100)
        temp = np.array(data[["x", "y", "z"]])
        ft = FunctionTransformer(compute_depth)
        return np.array(ft.transform(temp))
