

# lab.py


from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def after_purchase():
    return ["NMAR", "MD", "MAR", "MAR", "MAR"]


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def multiple_choice():
    return ["MAR", "NMAR", "MD", "NMAR", "MCAR"]


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------



def first_round():
    return [0.177, "NR"]


def second_round():
    return [0.018, "R", "D"]


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def verify_child(heights):
    heights = heights.copy()
    lst = []
    for col in heights.columns[2:]:
        lst.append(stats.ks_2samp(heights.loc[heights[col].isna(), "father"], heights.loc[heights[col].notna(), "father"]).pvalue)
    return pd.Series(lst, index=heights.columns[2:])


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def cond_single_imputation(new_heights):
    def mean_impute(s):
        return s.fillna(s.mean())

    df = new_heights.copy()
    df["quartile"] = pd.qcut(df["father"], q=4, labels=["Q1", "Q2", "Q3", "Q4"])
    df["child_filled"] = df.groupby("quartile")["child"].transform(mean_impute).to_frame()
    return df["child_filled"]


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def quantitative_distribution(child, N):
    data = child.dropna()
    counts, bins = np.histogram(data, bins=10)
    probabilities = counts / counts.sum()
    to_fill = []
    for i in range(N):
        to_fill.append(bins[np.random.choice(len(probabilities), p=probabilities)])
    return np.array(to_fill)

def impute_height_quant(child):
    quant = quantitative_distribution(child, len(child))
    for i in range(len(child)):
        if pd.isna(child[i]):
            child[i] = quant[i]
    return child


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def answers():
    return  [1, 2, 2, 1], ["https://campuswire.com/", "https://instagram.com"]
