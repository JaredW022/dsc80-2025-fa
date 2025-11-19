# lab.py


from pathlib import Path
import io
import pandas as pd
import numpy as np
np.set_printoptions(legacy='1.21')


# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    if len(ints) == 0:
        return False

    for k in range(len(ints) - 1):
        diff = abs(ints[k] - ints[k+1])
        if diff == 1:
            return True

    return False


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    nums = sorted(nums)
    nums_median = 0
    if len(nums) % 2 == 0 :
        nums_median = float((nums[len(nums) // 2 - 1] + nums[len(nums) // 2])) / 2
    else :
        nums_median = nums[len(nums) // 2]
    nums_mean = sum(nums) / len(nums)
    if (nums_median <= nums_mean):
        return True
    return False


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    prefixes = ""
    for i in range(n + 1):
        prefixes += s[:n - i]
    return prefixes


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def exploded_numbers(ints, n):
    exploded_list = []
    for i in ints:
        current_num = ""
        for j in range(n, -1, -1):
            current_num = current_num + str(i - j).rjust(len(str(max(ints) + n)), "0") + " "
        for k in range(1, n + 1):
            current_num = current_num +  str(i + k).rjust(len(str(max(ints) + n)), "0") + " "
            current_num = current_num.rjust(len(str(max(ints) + n)), "0")
        exploded_list.append(current_num.strip())
    return exploded_list


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def last_chars(fh):
    chars = ""
    lines = fh.read().strip().split("\n")
    for line in lines:
        try:
            chars += line[-1]
        except IndexError:
            continue
    return chars


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def add_root(A):
    return A + np.sqrt(np.arange(0, len(A)))

def where_square(A):
    return np.sqrt(A) == np.round(np.sqrt(A))


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_loop(matrix, cutoff):
    means = [0] * len(matrix[0])
    for i in matrix:
        for j in range(len(i)):
            means[j] += i[j]
    for i in range(len(means)):   
        means[i] = means[i] / len(matrix)
    cols_bool = [0] * len(matrix[0])
    for z in range(len(means)):
        if means[z] > cutoff:
            cols_bool[z] = True
        else:
            cols_bool[z] = False
    good_cols_idx = []
    for k in range(len(cols_bool)):
        if cols_bool[k] > 0:
            good_cols_idx.append(k)
    kept_cols = []
    for y in range(len(matrix)):
        to_append = []
        for x in range(len(matrix[0])):
            if x in good_cols_idx:
                to_append.append(matrix[y][x])
        kept_cols.append(to_append)
    return np.array(kept_cols)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_np(matrix, cutoff):
    aT = matrix.T
    list_means = np.mean(aT, axis = 1)
    bool_means = list_means > cutoff
    return matrix[:, bool_means]


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def growth_rates(A):
    excluding_last = A[:-1]
    excluding_first = A[1:]
    return np.round((excluding_first - excluding_last) / excluding_last, 2)

def with_leftover(A):
    leftovers = 20 % A
    cumulative_leftovers = np.cumsum(leftovers)
    if np.any(cumulative_leftovers >= A):
        return np.where(cumulative_leftovers >= A)[0][0]
    else:
        return -1


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def salary_stats(salary):
    num_players = salary["Player"].count()
    num_teams = salary.groupby("Team").count().shape[0]
    total_salary = salary["Salary"].sum()
    highest_salary = salary["Player"].iloc[salary["Salary"].sort_values(ascending=False).index[0]]
    # salary.sort_values("Salary", ascending=False)
    avg_los = np.round(salary.groupby("Team").sum().loc["Los Angeles Lakers"]["Salary"] / salary.groupby("Team").count().loc["Los Angeles Lakers"]["Salary"], 2)
    fifth_lowest = salary.loc[salary["Salary"].sort_values().index[4]]["Player"] + ", " + salary.loc[salary["Salary"].sort_values().index[4]]["Team"]
    duplicates = bool
    if(len(salary["Player"].apply(lambda x: x.split()).apply(lambda x: x[1]).unique()) != num_players):
        duplicates = True
    else:
        duplicates = False
    total_highest = salary.groupby("Team").sum().loc[salary["Team"].iloc[salary["Player"][salary["Player"] == highest_salary].index[0]]]["Salary"]

    salary_stats = pd.Series() 
    salary_stats["num_players"] = num_players
    salary_stats["num_teams"] = num_teams
    salary_stats["total_salary"] = total_salary
    salary_stats["highest_salary"] = highest_salary
    salary_stats["avg_los"] = avg_los
    salary_stats["fifth_lowest"] = fifth_lowest
    salary_stats["duplicates"] = duplicates
    salary_stats["total_highest"] = total_highest 
    
    return salary_stats


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def parse_malformed(fp):
    with open(fp) as f:
        lines = f.readlines()
        cleaned_lines = []

        for line in lines:
            line = line.replace('"', " ")
            line = line.replace(",", " ")
            line = line.strip()
            line = line.split()
            cleaned_lines.append(line)

        df = pd.DataFrame(cleaned_lines)
        new_geo = df[4] + ',' + df[5]
        new_geo[0] = 'geo'
        df = df.drop(columns=[4,5])
        df['geo'] = new_geo
        df.columns = df.iloc[0]
        df = df.drop(0)
        df["weight"] = df["weight"].astype(float)
        df["height"] = df["height"].astype(float)
        return df.reset_index(drop=True)
