# project.py


import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_assignment_names(dFrame):
    dct = {'lab': [], 'project': [], 'midterm': [], 'final': [], 'disc': [], 'checkpoint': []}
    labs = []
    projects = []
    midterms = []
    final = []
    discs = []
    checkpoints = []

    for i in dFrame.columns:
        if i.startswith('lab') and i[-1].isnumeric():
            labs.append(i)
        if i.startswith('project') and i[-1].isnumeric() and i.find('checkpoint') == -1:
            projects.append(i)
        if i.startswith('Midterm') and i.find('-') == -1:
            midterms.append(i)
        if i.startswith('Final') and i.find('-') == -1:
            final.append(i)
        if i.startswith('discussion') and i[-1].isnumeric():
            discs.append(i)
        if i.find('checkpoint') != -1 and i.find('-') == -1:
            checkpoints.append(i)
    
    dct.update({'lab': labs})
    dct.update({'project': projects})
    dct.update({'midterm': midterms})
    dct.update({'final': final})
    dct.update({'disc': discs})
    dct.update({'checkpoint': checkpoints})
    return dct


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def projects_total(grades):
    grades = grades.fillna(0)

    project_grades = []
    frq_grades = []
    max_project_grades = []
    max_frq_grades = []
    for i in grades.columns:
        if i.startswith('project') and i[-1].isnumeric() and i.find('checkpoint') == -1:
            project_grades.append(i)
        if i.startswith('project') and i.find('free') != -1 and i.find('-') == -1:
            frq_grades.append(i)
        if i.startswith('project') and i.find('Max') != -1 and i.find('checkpoint') == -1 and i.find('free') == -1:
            max_project_grades.append(i)
        if i.startswith('project') and i.find('Max') != -1 and i.find('checkpoint') == -1 and i.find('free') != -1:
            max_frq_grades.append(i)

    frq_nums = []
    for i in frq_grades:
        frq_nums.append(i[7:9])

    proj_final_grades = pd.Series()

    frq_index = 0
    for i in range(len(project_grades)):
        if project_grades[i][7:9] in frq_nums:
            proj_final_grades[project_grades[i]] = ((grades.get(project_grades[i]) + grades.get(frq_grades[frq_index])) / (grades.get(max_project_grades[i]) + grades.get(max_frq_grades[frq_index])))
            frq_index += 1
        else:
            proj_final_grades[project_grades[i]] = (grades.get(project_grades[i]) / grades.get(max_project_grades[i]))
    
    sums = np.zeros(len(proj_final_grades.iloc[0]))
    for i in proj_final_grades:
        for j in range(len(i)):
            sums[j] += i[j]
    return pd.Series(sums / len(proj_final_grades), index = grades.index)


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def lateness_penalty(series):
    penalties = []
    times_list = []
    times_secs = []
    for i in series:
        times_list.append(i.split(":"))
    for i in times_list:
        times_secs.append(int(i[0]) * 3600 + int(i[1]) * 60 + int(i[2]))
    for i in times_secs:
        if int(i) > 1209600:
            penalties.append(0.4)
        elif int(i) > 604800:
            penalties.append(0.7)
        elif int(i) > 7200:
            penalties.append(0.9) 
        else:
            penalties.append(1.0)
    return pd.Series(penalties, index=series.index)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def process_labs(grades):
    grades = grades.fillna(0)
    idx = grades.index
    lab_df = pd.DataFrame(index=idx, columns=get_assignment_names(grades)["lab"])
    lateness = []
    max_points_cols = []
    max_points = []
    for i in grades.columns:
        if i.startswith('lab') and i.find('Max') != -1:
            max_points_cols.append(i)
    for i in max_points_cols:
        max_points.append(grades[i])
    for i in lab_df.columns + " - Lateness (H:M:S)":
        lateness.append(lateness_penalty(grades[i]))
    scores = []
    for i in lab_df.columns:
        scores.append(grades[i])
    with_lateness = []
    for i in range(len(lab_df.columns)):
        with_lateness.append(lateness[i] * scores[i])
    for i in range(len(with_lateness)):
        lab_df[lab_df.columns[i]] = with_lateness[i] / max_points[i]
    return lab_df


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def lab_total(df):
    lab_grades = []
    for i in range(df.shape[0]):
        lab_grades.append((sum(list(df.iloc[i])) - (min(df.iloc[i]))) / (len(list(df.iloc[i])) - 1))
    return pd.Series(lab_grades, index = df.index)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def total_points(df):
    df = df.fillna(0)
    labs = lab_total(process_labs(df)) * 0.2
    projects = projects_total(df) * 0.3

    checkpoints_names = get_assignment_names(df)["checkpoint"]
    checkpoints_max = []
    for i in df.columns:
        if i.find("Max") != -1 and i.find("checkpoint") != -1:
            checkpoints_max.append(i)
    checkpoints_as_percent = []
    for i in range(len(checkpoints_names)):
        checkpoints_as_percent.append(df[checkpoints_names[i]] / df[checkpoints_max[i]])
    all_checkpoints = np.zeros(len(df))
    for i in checkpoints_as_percent:
        all_checkpoints += i
    checkpoints = all_checkpoints / len(checkpoints_names) * 0.025

    discussion_names = get_assignment_names(df)["disc"]
    disc_max = []
    for i in df.columns:
        if i.find("Max") != -1 and i.find("discussion") != -1:
            disc_max.append(i)
    disc_as_percent = []
    for i in range(len(discussion_names)):
        disc_as_percent.append(df[discussion_names[i]] / df[disc_max[i]])
    all_disc = np.zeros(len(df))
    for i in disc_as_percent:
        all_disc += i
    disc = all_disc / len(discussion_names) * 0.025

    midterms = df.get("Midterm") / df.get("Midterm - Max Points") * 0.15
    finals = df.get("Final") / df.get("Final - Max Points") * 0.3
    return labs + projects + checkpoints + disc + midterms + finals


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def final_grades(series): 
    grades = []
    for grade in series:
        if grade >= 0.9:
            grades.append("A")
        elif 0.8 <= grade < 0.9:
            grades.append("B")
        elif 0.7 <= grade < 0.8:
            grades.append("C")
        elif 0.6 <= grade < 0.7:
            grades.append("D")
        elif grade < 0.6:
            grades.append("F")
    return pd.Series(grades)

def letter_proportions(series):
    letter_grades = {'A': 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for grade in series:
        if grade >= 0.9:
            letter_grades["A"] += 1
        elif 0.8 <= grade < 0.9:
            letter_grades["B"] += 1
        elif 0.7 <= grade < 0.8:
            letter_grades["C"] += 1
        elif 0.6 <= grade < 0.7:
            letter_grades["D"] += 1
        elif grade < 0.6:
            letter_grades["F"] += 1
    letter_grades["A"] /= len(series)
    letter_grades["B"] /= len(series)
    letter_grades["C"] /= len(series)
    letter_grades["D"] /= len(series)
    letter_grades["F"] /= len(series)
    return pd.Series(letter_grades).sort_values(ascending=False)


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def raw_redemption(dFrame, rQuestions):
    dFrame = dFrame.fillna(0)
    each_question = []
    for i in rQuestions:
        each_question.append(dFrame.get(dFrame.columns[i]))
    max_scores = []
    for i in each_question:
        max_scores.append(np.max(i))
    raw_redemption_scores = np.zeros(len(each_question[0]))
    for series in each_question:
        for index in range(len(series)):
            raw_redemption_scores[index] += series[index]
    return_dFrame = dFrame
    return_dFrame["Raw Redemption Score"] = raw_redemption_scores / sum(max_scores)
    return_dFrame = return_dFrame.set_index("PID").get("Raw Redemption Score")
    return pd.DataFrame(return_dFrame).reset_index()
    
def combine_grades(grades, raw_redemption):
    return grades.merge(raw_redemption, on="PID", how="left")

# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def z_score(series):
    series_std = series.std(ddof=0)
    series_mean = np.mean(series)
    return (series - series_mean) / series_std
    
def add_post_redemption(df):
    # Since her redemption z-score, $0.8485$, is greater than her midterm z-score, $0.6286$, her midterm exam score of $\frac{53}{70} \approx 0.7571$ will be replaced with
    #v $$\text{Jasmine's redemption z-score} \cdot \text{class' midterm SD} + \text{class' midterm mean} \approx 0.8485 \cdot 0.25 + 0.6 = \boxed{0.8121}$$
    original_zscore = z_score(df["Midterm"])
    redemption_zscore = z_score(df["Raw Redemption Score"])
    updated_scores = []
    for index in range(len(redemption_zscore)):
        if redemption_zscore[index] > original_zscore[index]:
            updated_scores.append(redemption_zscore.iloc[index] * (df["Midterm"]).std(ddof=0) + np.mean(df["Midterm"]))
        else:
            updated_scores.append(df["Midterm"][index])
    df["Midterm Score Pre-Redemption"] = df["Midterm"] / df["Midterm - Max Points"]
    df["Midterm Score Post-Redemption"] = updated_scores / df["Midterm - Max Points"]
    return df


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def total_points_post_redemption(df):
    df = df.fillna(0)
    return pd.Series(total_points(df) - (df["Midterm Score Pre-Redemption"] * 0.15) + (df["Midterm Score Post-Redemption"] * 0.15))
        
def proportion_improved(df):
    adjusted_scores = total_points_post_redemption(df)
    original_scores = total_points(df)
    count = 0
    adjusted_individual = final_grades(adjusted_scores)
    original_individual = final_grades(original_scores)
    for i in range(len(adjusted_individual)):
        if adjusted_individual[i] < original_individual[i]:
            count += 1
    return count / len(adjusted_individual)


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def section_most_improved(df):
    return df[["Section", "Total Points Post-Redemption"]].groupby("Section")["Total Points Post-Redemption"].mean().sort_values(ascending=False).index[0]
    
def top_sections(df, t, n):
    df = df[df["Final"] >= t]
    valid_sections = (df["Section"].value_counts() >= n) 
    valid_sections = valid_sections[valid_sections == True].index
    return np.sort(valid_sections.to_numpy())


# ---------------------------------------------------------------------
# QUESTION 12
# ---------------------------------------------------------------------


def rank_by_section(df):
    num_rows = df.groupby(["Section"]).count()["PID"].max()
    sections = list(df.groupby("Section").count().reset_index()["Section"])
    new_df = pd.DataFrame(index=range(num_rows), columns=sections)
    for section in sections:
        short_list = list(df.groupby(["Section", "PID"]).sum().loc[section].sort_values("Total Points Post-Redemption", ascending=False).reset_index()["PID"])
        short_list += [None] * (num_rows - len(short_list))
        new_df[section] = short_list
    return new_df.fillna("")








# ---------------------------------------------------------------------
# QUESTION 13
# ---------------------------------------------------------------------


def letter_grade_heat_map(df):
    sections = np.sort(df["Section"].unique())
    props = []
    for section in sections:
        current_section = df[df["Section"] == section]
        props.append(letter_proportions(current_section["Total Points Post-Redemption"]).sort_index())
    props = pd.DataFrame(props).T
    fig = px.imshow(props, labels=dict(x="Section", y="Letter Grades"),
                x=sections,
                y=['A', 'B', 'C', 'D', 'F'],
                color_continuous_scale='turbid')
    fig.update_layout(title="Distribution of Letter Grades by Section", font=dict(size=20))
    fig.update_layout(
    xaxis_title_font=dict(size=20),
    yaxis_title_font=dict(size=20)
    )
    return fig
