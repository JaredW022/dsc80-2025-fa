# lab.py


import pandas as pd
import numpy as np
import io
from pathlib import Path
import os


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def prime_time_logins(login):
    copy = login.copy()
    copy['Time'] = pd.to_datetime(copy['Time'])
    queried = copy[(copy["Time"].dt.hour >= 16) & (copy["Time"].dt.hour < 20)].groupby("Login Id").count()
    all_users = login['Login Id'].unique()
    queried = queried.reindex(all_users, fill_value = 0)
    return queried

# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def count_frequency(logins):
    copy = logins.copy()
    copy["Time"] = pd.to_datetime(copy["Time"])
    total_logins = copy.groupby("Login Id")["Time"].count()
    copy["Date"] = copy["Time"].dt.date
    first_day = copy.groupby("Login Id")["Time"].min()
    current_day = pd.to_datetime("2024-01-31 23:59:00")
    return total_logins / pd.to_timedelta(current_day - first_day).dt.days



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def cookies_null_hypothesis():
    return [2]
                         
def cookies_p_value(N):
    return ((np.random.multinomial(250, [.96, .04], size=N)[:, 1] / 250) == 0.04).mean() 


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def car_null_hypothesis():
    return [1, 4]

def car_alt_hypothesis():
    return [2, 6]

def car_test_statistic():
    return [1, 4]

def car_p_value():
    return 4


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def superheroes_test_statistic():
    return [1, 2]
    
def bhbe_col(heroes):
    return (heroes["Hair color"].str.contains("blond", na=False, case=False)) & (heroes["Eye color"].str.contains("blue", na=False, case=False))

def superheroes_observed_statistic(heroes):
    df = heroes[bhbe_col(heroes)]
    good_df = df[df["Alignment"] == "good"]
    return good_df.shape[0] / df.shape[0]

def simulate_bhbe_null(heroes, N): 
    alignment_shuffled = np.random.multinomial(heroes[bhbe_col(heroes)].shape[0], [(heroes["Alignment"] == "good").mean(), 1 - (heroes["Alignment"] == "good").mean()], N)
    return (alignment_shuffled[:, 0] / heroes[bhbe_col(heroes)].shape[0])

def superheroes_p_value(heroes):
    observed = superheroes_observed_statistic(heroes)
    sims = simulate_bhbe_null(heroes, 100000)
    prop = (sims >= observed).mean()
    if prop >= 0.01:
        return [prop, "Fail to Reject"]
    else:
        return [prop, "Reject"]


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def diff_of_means(data, col='orange'):
    data = data.copy()
    means = data.groupby("Factory")[col].mean()
    return np.abs(means["Yorkville"] - means["Waco"])


def simulate_null(data, col='orange'):
    data = data.copy()
    data["Factory"] = np.random.permutation(data["Factory"])
    return diff_of_means(data, col)


def color_p_value(data, col='orange'):
    data = data.copy()
    observed = diff_of_means(data, col)
    simulated = []
    for i in range(1000):
        simulated.append(simulate_null(data, col))
    return np.mean(simulated >= observed)


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def ordered_colors():
    return [("yellow", 0.0), ("orange", 0.033), ("red", 0.243), ("green", 0.465), ("purple", 0.985)]

# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


    
def same_color_distribution():
    return (0.003, "Reject")

# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def perm_vs_hyp():
    return ["P", "P", "H", "H", "P"]
