import marijuana_ml
import preprocessing

def create_graph(user_data):
    df = preprocessing.preprocess(user_data, int(user_data['truncate_training_data'][0]))
    marijuana_ml.run_model(df, user_data, int(user_data['truncate_training_data'][0])) # generates graph in /static/charts named chart.png
