#!/usr/bin/env python
import pandas as pd
import numpy as np
from sklearn import preprocessing

def preprocess(user_data):
    print("preprocessing data...")
    # read csv from github url
    # return pandas dataframe
    url = '../BISTRA_GROUP_PROJECT_SMALL.csv'
    df = pd.read_csv(url)
    print("read in data", df.shape)
    for key in user_data.keys():
        df = df.loc[df[key] == int(user_data[key][0])]
        df.drop(columns=[key], inplace=True)
    print("shape", user_data, df.shape)

    df = df[df.Marijuana_Days != -999] # removes all rows with Marijuana_Days = -999
    df['zipcode'] = df['zipcode'].str[:5] # trim zip codes down to first 5 digits

    unused_potential_predictors = ['SFS8p_0', 'SFS8p_3', 'SFS8p_6', 'SFS8p_12', 'ada_0','ada_3',
    'ada_6','ada_12','S2c1_0','S2c1_3','S2c1_6','S2c1_12','S2b1_0','S2b1_3','S2b1_6','S2b1_12','S2z1_3','S2z1_6',
    'S2z1_12','S2z2_3','S2z2_6','S2z2_12','S2z3_3','S2z3_6','S2z3_12','S2z4_3','S2z4_6','S2z4_12','S2z5_3','S2z5_6',
    'S2z5_12','Any_Cens','Alcohol_Cens','Binge_Cens','Marijuana_Cens','Illicit_Cens','Any_Days','Binge_Days',
    'Alcohol_Days','Illicit_Days']

    domain_expert_cols_to_drop = ['SPSy_0', 'loc', 'AFSS_0', 'E9a', 'E9b', 'E9c', 'E9d', 'E9e', 'E9e18', 'E9f', 'ID',
    'E9g', 'E9h', 'E9j', 'E9k', 'E9m', 'txtypeg', 'S7e4_0', 'engage42', 'POPIgrp','L5', 'E14a_0', 'E14b_0', 'SDScrY']

    text_columns = ['City', 'agyaddr', 'zipcode', 'State']

    cols_to_drop = text_columns + domain_expert_cols_to_drop + unused_potential_predictors

    # drop columns and isolate to specific substance
    df.drop(columns=cols_to_drop, inplace=True)
    df = df[df.primsev == 3] # leaves only marijuana drug abusers in dataframe
    df.drop(columns=['primsev'], inplace=True)
    print("dropped useless columns")
    # replace all -999 with NaN inplace
    df.replace(to_replace = -999, value = np.nan, inplace=True)
    print("replace all -999s with NaNs")
    # calculate percentage of NaNs in each column
    percent_missing = df.isnull().sum() * 100 / len(df)
    missing_value_df = pd.DataFrame({'column_name': df.columns,'percent_missing': percent_missing})
    # drop columns with > 25% NaNs
    cols = ['noins', 'RFQ33c', 'GSSI_0', 'press', 'PSSI_0', 'RERI13p_0', 'FIS4p_0']
    df.drop(columns=cols, inplace=True)

    # identify boolean columns
    bool_cols = ['female', 'nonwhite', 'unemplmt', 'prsatx', 'tsd_0', 'und15', 'dldiag',
        'suicprbs_0', 'homeless_0', 'S6', 'ncar', 'engage30', 'init']

    # replace boolean column NaNs with mode
    print("bool cols:", bool_cols)
    for i in range(len(bool_cols)):
        if bool_cols[i] in list(df.columns):
            df[bool_cols[i]].fillna(df[bool_cols[i]].mode(), inplace=True)

    # since binary columns are filled we can just replace all other NaNs with mean
    for column in df.columns:
        df[column].fillna(df[column].mean(), inplace=True)
    print("shape", df.shape)
    # maybe find elegant way to just print % NaNs in entire df and if anything but 0% something went wrong
    percent_missing = df.isnull().sum() * 100 / len(df)
    missing_value_df = pd.DataFrame({'column_name': df.columns,'percent_missing': percent_missing})
    all_null = True
    for index, row in missing_value_df.iterrows():
        if row['percent_missing'] > 0:
            all_null = False
            print(row['column_name'], "has null values!!!! rip...")

    if not all_null:
        return -1

    # normalize columns that are continuous

    cols = ['tottxp4', 'CWS_0', 'ADHDs_0', 'CDS_0', 'CJSI_0', 'EPS7p_0', 'LRI7_0', 'SRI7_0',
            'ERS21_0', 'HIVrisk', 'totttld', 'S2x_0', 'SPSm_0']

    scaler = preprocessing.StandardScaler()
    for i in cols:
        if i in list(df.columns):
            print(df.shape)
            df[i] = scaler.fit_transform(df[[i]])

    return df
