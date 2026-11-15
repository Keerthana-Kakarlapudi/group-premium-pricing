import os
import pickle
from preprocessing import FEATURES


class model_obj:

    def __init__(self):
        pass

    def predict_model(self, data):
        # load and read the model in binary mode
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'cost_model.pkl')
        model = pickle.load(open(model_path, 'rb'))

        # take the features used for training the model
        X = data[FEATURES]
        data['Prediction'] = model.predict(X)

        print("Model Prediction Successful!")
        return data
