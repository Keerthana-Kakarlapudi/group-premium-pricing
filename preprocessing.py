import pandas as pd
import numpy as np


class PreProcess:
    def __init__(self):
        print("Inside class")

    def default(self, Data):
        # Fill in sensible defaults when a group file leaves a column out
        if 'region' not in Data.columns:
            Data['region'] = 'southeast'
        if 'children' not in Data.columns:
            Data['children'] = 0
        print("Exiting the default class")
        return Data

    def processing(self, Data):
        # Encoding age
        Data['age_en'] = Data['age'] / 100

        # Encoding gender
        Data['sex_en'] = Data['sex'].str.upper().map({'MALE': 0, 'M': 0, 'FEMALE': 1, 'F': 1})

        # Encoding smoker
        Data['smoker_en'] = Data['smoker'].str.upper().map({'YES': 1, 'NO': 0})

        # Encoding BMI
        Data['bmi_en'] = Data['bmi'] / 100

        # Encoding children
        Data['children_en'] = Data['children']

        # Encoding region
        regions = {'NORTHEAST': 0, 'NORTHWEST': 1, 'SOUTHEAST': 2, 'SOUTHWEST': 3}
        Data['region_en'] = Data['region'].str.upper().map(regions)

        print("Exiting the processing class")
        return Data


FEATURES = ['age_en', 'sex_en', 'smoker_en', 'bmi_en', 'children_en', 'region_en']
