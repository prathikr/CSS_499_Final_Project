import marijuana_ml
import preprocessing

def main(user_data):
    df = preprocessing.preprocess(user_data)
    marijuana_ml.run_model(df)
