# lab.py


import pandas as pd
import numpy as np
import os
import re


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def match_1(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_1("abcde]")
    False
    >>> match_1("ab[cde")
    False
    >>> match_1("a[cd]")
    False
    >>> match_1("ab[cd]")
    True
    >>> match_1("1ab[cd]")
    False
    >>> match_1("ab[cd]ef")
    True
    >>> match_1("1b[#d] _")
    True
    """
    pattern = r'^.{2}\[.{2}\]'
    
    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_2(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_2("(123) 456-7890")
    False
    >>> match_2("858-456-7890")
    False
    >>> match_2("(858)45-7890")
    False
    >>> match_2("(858) 456-7890")
    True
    >>> match_2("(858)456-789")
    False
    >>> match_2("(858)456-7890")
    False
    >>> match_2("a(858) 456-7890")
    False
    >>> match_2("(858) 456-7890b")
    False
    """
    pattern = r'^\(858\) \d{3}\-\d{4}$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_3(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_3("qwertsd?")
    True
    >>> match_3("qw?ertsd?")
    True
    >>> match_3("ab c?")
    False
    >>> match_3("ab   c ?")
    True
    >>> match_3(" asdfqwes ?")
    False
    >>> match_3(" adfqwes ?")
    True
    >>> match_3(" adf!qes ?")
    False
    >>> match_3(" adf!qe? ")
    False
    """
    pattern = r'^[a-zA-Z0-9\s?]{5,9}\?'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_4(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_4("$$AaaaaBbbbc")
    True
    >>> match_4("$!@#$aABc")
    True
    >>> match_4("$a$aABc")
    False
    >>> match_4("$iiuABc")
    False
    >>> match_4("123$$$Abc")
    False
    >>> match_4("$$Abc")
    True
    >>> match_4("$qw345t$AAAc")
    False
    >>> match_4("$s$Bca")
    False
    >>> match_4("$!@$")
    False
    """
    pattern = r'^\$[^abc$]*\$[aA]+[bB]+[cC]+$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_5(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_5("dsc80.py")
    True
    >>> match_5("dsc80py")
    False
    >>> match_5("dsc80..py")
    False
    >>> match_5("dsc80+.py")
    False
    """
    pattern = r'^[a-zA-Z0-9_]+\.py$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_6(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_6("aab_cbb_bc")
    False
    >>> match_6("aab_cbbbc")
    True
    >>> match_6("aab_Abbbc")
    False
    >>> match_6("abcdef")
    False
    >>> match_6("ABCDEF_ABCD")
    False
    """
    pattern = r'^[a-z]+_[a-z]+$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_7(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_7("_abc_")
    True
    >>> match_7("abd")
    False
    >>> match_7("bcd")
    False
    >>> match_7("_ncde")
    False
    """
    pattern = r'^_.*_$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_8(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_8("ASJDKLFK10ASDO")
    False
    >>> match_8("ASJDKLFK0ASDo!!!!!!! !!!!!!!!!")
    True
    >>> match_8("JKLSDNM01IDKSL")
    False
    >>> match_8("ASDKJLdsi0SKLl")
    False
    >>> match_8("ASDJKL9380JKAL")
    True
    """
    pattern = r'^[^Oi1]+$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_9(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_9('NY-32-NYC-1232')
    True
    >>> match_9('ca-23-SAN-1231')
    False
    >>> match_9('MA-36-BOS-5465')
    False
    >>> match_9('CA-56-LAX-7895')
    True
    >>> match_9('NY-32-LAX-0000') # If the state is NY, the city can be any 3 letter code, including LAX or SAN!
    True
    >>> match_9('TX-32-SAN-4491')
    False
    '''
    pattern = r'^(CA-\d{2}-(SAN|LAX)-\d{4})|(NY-\d{2}-[A-Z]{3}-\d{4})$'

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_10(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_10('ABCdef')
    ['bcd']
    >>> match_10(' DEFaabc !g ')
    ['def', 'bcg']
    >>> match_10('Come ti chiami?')
    ['com', 'eti', 'chi']
    >>> match_10('and')
    []
    >>> match_10('Ab..DEF')
    ['bde']
    
    '''
    string = string.lower()
    string = re.sub(r'[^\w]|a', "", string)
    string = re.findall(r'.{3}', string)
    return string


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def extract_personal(s):
    # check for 2-4 characters after the . -- (Done)
    email_address = re.findall(r'[\w]+@[\w]+.\w{2,4}', s)

    # need to clean ssns and btc_address: remove ssn: and bitcoin: from the strings -- Done
    ssns = re.findall(r'ssn:\d{3}-\d{2}-\d{4}', s)
    ssns = [i.strip("ssns:") for i in ssns]

    # check why some outputs returning 'ull' -- (Need to do)
    btc_address = re.findall(r'bitcoin:(?!null)[\w]+', s)
    btc_address = [i.strip("bitcoin:") for i in btc_address]


    # clean \xxx at the end of addresses -- (Done)
    street_address = re.findall(r'\d+ [a-zA-Z ]+', s)
    return email_address, ssns, btc_address, street_address


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def tfidf_data(reviews_ser, review):
    def tokenize(string):
        review = re.findall(r'\b\w+\b', string)
        return review
    counts = np.zeros(len(tokenize(review)))
    counts_df = pd.DataFrame().assign(cnt=counts).assign(words=tokenize(review)).groupby("words").count()
    counts_df = counts_df.assign(tf=(counts_df['cnt'] / len(tokenize(review))))
    idf = {}
    for word in counts_df["cnt"].index:
        df = reviews_ser.str.contains(rf'\b{word}\b', case=False).sum()
        idf[word] = np.log(len(reviews_ser) / df)
    counts_df = counts_df.assign(idf=pd.Series(idf))
    counts_df = counts_df.assign(tfidf=counts_df["tf"]*counts_df["idf"])
    return counts_df


def relevant_word(out):
    return out["tfidf"].sort_values(ascending=False).index[0]


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def hashtag_list(tweet_text):
    hashtags = []
    for line in tweet_text:
        hashtags.append(re.findall(r'#[\w]+', line))
    return pd.Series([[elem.strip("#") for elem in list] for list in hashtags])


def most_common_hashtag(tweet_lists):
    all = []
    for lst in tweet_lists:
        all.extend(lst)
    all = pd.Series(all).value_counts()
    to_return = []
    for lst in tweet_lists:
        if len(lst) == 0:
            to_return.append(np.nan)
        elif len(lst) == 1:
            to_return.append(lst[0])
        else:
            dct = {}
            for elem in lst:
                dct.update({elem: pd.Series(all).loc[elem]})
            to_return.append(pd.Series(dct).idxmax())
    return pd.Series(to_return)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def create_features(ira):
    def clean_text(series):
        cleaned = []
        for text in series:
            text = re.sub(r'https?://\S+', ' ', text)
            text = re.sub(r'^RT', ' ', text)
            text = re.sub(r'@[a-zA-Z0-9_]+', ' ', text)
            text = re.sub(r'#[a-zA-Z0-9_]+', ' ', text)
            text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
            text = text.lower()
            text = re.sub(r'\s+', ' ', text).strip()
            cleaned.append(text)
        return pd.Series(cleaned)

    mod = ira.copy()
    count_hashtags = hashtag_list(ira["text"]).apply(len)
    mod = mod.assign(num_hashtags=count_hashtags)
    mod = mod.assign(mc_hashtags=most_common_hashtag(hashtag_list(ira["text"])))

    ats = []
    for i in ira["text"]:
        ats.append(len(re.findall(r'@[a-zA-Z0-9]+', i)))
    mod = mod.assign(num_tags=ats)
    links = []
    for i in ira["text"]:
        links.append(len(re.findall(r'(https://[\w]+)|(http://[\w]+)', i)))
    mod = mod.assign(num_links=links)
    retweet = []
    for i in ira["text"]:
        if len(re.findall(r'(^RT)', i)) >= 1:
            res = True
        if len(re.findall(r'(^RT)', i)) == 0:
            res = False
        retweet.append(res)
    mod = mod.assign(is_retweet=retweet)
    return mod.assign(text=clean_text(ira["text"]))


