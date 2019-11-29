from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sksurv.util import Surv
from sksurv.linear_model import CoxPHSurvivalAnalysis
import seaborn as sns
import numpy as np
import os
import pandas as pd

sns.set_style("whitegrid")

def run_model(df, user_data, truncate_training_data):
    Xtr, Xte = train_test_split(df, test_size=0.2)

    if not truncate_training_data:
        print('Truncating test set')
        for key in user_data.keys():
            if key != 'truncate_training_data':
                print("filtering by " + key + " with value " + user_data[key][0])
                df = df.loc[df[key] == int(user_data[key][0])]
                # DO NOT DROP COLUMNS OR ELSE MODEL WON'T WORK SINCE TRAINED WITH ALL FEATURES
        print("shape", user_data, df.shape)

    # extract Marujiana_Days predictor
    Ytr = Xtr['Marijuana_Days'].copy()
    Yte = Xte['Marijuana_Days'].copy()
    Xtr.drop(columns=['Marijuana_Days'], inplace=True)
    Xte.drop(columns=['Marijuana_Days'], inplace=True)

    Ytr_censored = Surv.from_arrays(Ytr < 365, Ytr.copy()) # structured array to ensure censoring of 365 value
    model = CoxPHSurvivalAnalysis()
    model.fit(Xtr, Ytr_censored)

    pred_surv = model.predict_survival_function(Xte)
    Yte_censored = Surv.from_arrays(Yte < 365, Yte.copy()) # structured array to ensure censoring of 365 value
    score = model.score(Xte, Yte_censored)
    coefs = pd.concat({'Column_Names':pd.DataFrame(Xtr.columns), 'Coefficients':pd.DataFrame(model.coef_)}, axis=1)
    print(coefs)
    plt.clf()

    plt.plot(np.mean([person.y for person in pred_surv], axis=0))
    # plt.plot(np.mean([person.y for person in Yte], axis=0))
    plt.suptitle('Probability of Relapse Over A Year')
    plt.ylabel("Probability")
    plt.xlabel("Days")
    plt.title('Concordance Index: ' + str(score), fontsize=10)
    plt.xlim(right=365)
    plt.savefig('static/charts/chart.png')

    #return coefs




