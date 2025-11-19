# project.py


import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pd.options.plotting.backend = 'plotly'

from IPython.display import display

# DSC 80 preferred styles
pio.templates["dsc80"] = go.layout.Template(
    layout=dict(
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=True,
        width=600,
        height=400,
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        title=dict(x=0.5, xanchor="center"),
    )
)
pio.templates.default = "simple_white+dsc80"
import warnings
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def clean_loans(loans):
    cleaned = loans.copy()
    cleaned["issue_d"] = cleaned["issue_d"].apply(pd.Timestamp)
    cleaned["term"] = cleaned["term"].str.strip(" months").astype(int)
    cleaned["emp_title"] = cleaned["emp_title"].fillna("").str.lower().str.strip()
    cleaned["emp_title"] = cleaned["emp_title"].apply(lambda x: "registered nurse" if (x == "rn") else x)
    cleaned["term_end"] =  cleaned["issue_d"] + cleaned["term"].apply(lambda x: pd.DateOffset(months=int(x)))
    cleaned["term_end"] = pd.to_datetime(cleaned["term_end"])
    return cleaned


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------



def correlations(df, pairs):
    idxs = []
    cc = []
    for i in range(len(pairs)):
        idxs.append(f"r_{pairs[i][0]}_{pairs[i][1]}")
        cc.append(df[pairs[i][0]].corr(df[pairs[i][1]]))
    return pd.Series(cc, idxs)



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def create_boxplot(loans):
    loans = loans.copy()
    loans["fico_range_low"] = pd.cut(loans["fico_range_low"], bins=[580, 670, 740, 800, 850], labels=["[580, 670)", "[670, 740)", "[740, 800)", "[800, 850)"], right=False, include_lowest=True)
    custom_colors = {36: "#541e6f", 60: "#f7c410"}
    fig = px.box(loans, x="fico_range_low", y="int_rate", color="term", title="Interest Rate vs. Credit Score",labels={"fico_range_low": "Credit Score Range", "int_rate": "Interest Rate (%)", "term": "Loan Length (Months)"}, color_discrete_map=custom_colors, category_orders={"term": [36, 60]})
    fig.update_xaxes(categoryorder='array', 
                 categoryarray=["[580, 670)", "[670, 740)", "[740, 800)", "[800, 850)"])
    fig.update_layout(width=700, height=500)
    return fig


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def ps_test(loans, N):
    import plotly.express as px
    copy = loans.copy()
    observed = loans.assign(has_ps=loans['desc'].notna()).groupby('has_ps')['int_rate'].mean()
    observed = observed.loc[True] - observed.loc[False]

    tvds = []
    for i in range(N):
        shuffled = copy.assign(shuffled = np.random.permutation(loans["desc"].notna()))
        tvd = shuffled.groupby("shuffled")["int_rate"].mean()
        tvds.append(tvd.loc[True] - tvd.loc[False])

    # fig_ = px.histogram(tvds)
    # fig_.add_vline(x=observed, line_width=3, line_color="red")
    # fig_.show()

    return (tvds >= observed).mean()
    
def missingness_mechanism():
    return 2
    
def argument_for_nmar():
    return'''
    Some people may believe that a personal statement may negatively harm 
    their interest rate due to their poor writing.
    '''



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def tax_owed(income, brackets):
    total_tax = 0
    for i in range(len(brackets)):
        if i + 1 < len(brackets):
            upper = brackets[i+1][1]
        else:
            upper = income
        taxable = max(0, min(income, upper) - brackets[i][1])
        total_tax += taxable * brackets[i][0]
    return total_tax


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def clean_state_taxes(df):
    df = df.copy()

    df = df.dropna(subset=["State", "Rate", "Lower Limit"], how="all")

    df["State"] = df["State"].apply(lambda x: np.nan if str(x)[0] == "(" else x)
    df["State"] = df["State"].ffill()

    df["Rate"] = df["Rate"].replace("none", np.nan).str.strip("%").astype(float).fillna(0) / 100
    df["Rate"] = df["Rate"].round(2)

    df["Lower Limit"] = df["Lower Limit"].str.strip("$").str.replace(",", "").fillna(0)
    df["Lower Limit"] = df["Lower Limit"].astype(int)
    return df


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def state_brackets(df):
    df = df.groupby("State").agg(list)
    df["bracket_list"] = list(zip(df["Rate"], df["Lower Limit"]))
    df["bracket_list"] = df["bracket_list"].apply(lambda x: list(zip(x[0], x[1])))
    df["bracket_list"] = df["bracket_list"].apply(lambda x: sorted(x, key=lambda y: y[1]))
    return df.drop(columns=["Rate", "Lower Limit"])
    
def combine_loans_and_state_taxes(loans, state_taxes):
    loans = loans.copy()
    state_taxes = state_taxes.copy()
    # Start by loading in the JSON file.
    # state_mapping is a dictionary; use it!
    import json
    state_mapping_path = Path('data') / 'state_mapping.json'
    with open(state_mapping_path, 'r') as f:
        state_mapping = json.load(f)
        
    # Now it's your turn:
    state_taxes["State"] = state_taxes["State"].apply(lambda x: state_mapping[x])
    state_taxes = state_brackets(state_taxes)

    df = pd.merge(loans, state_taxes, left_on="addr_state", right_on="State")
    df["State"] = df["addr_state"]
    return df.drop(columns=["addr_state"])


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def find_disposable_income(loans_with_state_taxes):

    FEDERAL_BRACKETS = [
     (0.1, 0), 
     (0.12, 11000), 
     (0.22, 44725), 
     (0.24, 95375), 
     (0.32, 182100),
     (0.35, 231251),
     (0.37, 578125)
    ]
    
    df = loans_with_state_taxes.copy()
    df["federal_tax_owed"] = df["annual_inc"].apply(lambda x: tax_owed(x, FEDERAL_BRACKETS))
    df["state_tax_owed"] = df[["annual_inc", "bracket_list"]].apply(lambda x: tax_owed(x[0], x[1]), axis=1)
    df["disposable_income"] = df["annual_inc"] - df["federal_tax_owed"] - df["state_tax_owed"]
    
    return df
    


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def aggregate_and_combine(loans, keywords, quantitative_column, categorical_column):
    loans = loans.copy()
    words = []
    for word in keywords:
        words.append(f'{word}_mean_{quantitative_column}')

    loans = loans[loans["emp_title"].apply(lambda x: any(i in x for i in keywords))]

    categories = sorted(loans[categorical_column].unique())
    df = pd.DataFrame({categorical_column: categories + ["Overall"]})


    for i in range(len(keywords)):
        temp_df = loans[loans["emp_title"].str.contains(keywords[i])]
        mor = list(temp_df.groupby(categorical_column)[quantitative_column].mean())
        mor.append(temp_df[quantitative_column].mean())
        df[words[i]] = pd.Series(mor)

    df = df.set_index(categorical_column)
    return df


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def exists_paradox(loans, keywords, quantitative_column, categorical_column):
    aag = aggregate_and_combine(loans, keywords, quantitative_column, categorical_column)
    out = aag[aag.columns[0]] > aag[aag.columns[1]]
    return all(out[:-1] == (not out.iloc[-1]))
    
def paradox_example(loans):
    return {
        'loans': loans,
        'keywords': ["mechanic", "machine operator"],
        'quantitative_column': "annual_inc",
        'categorical_column': "purpose"
    }