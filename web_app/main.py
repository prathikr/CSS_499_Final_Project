import marijuana_ml
import preprocessing

def create_graph(user_data):
    df = preprocessing.preprocess(user_data)
    marijuana_ml.run_model(df) # generates graph in /static/charts named chart.png
