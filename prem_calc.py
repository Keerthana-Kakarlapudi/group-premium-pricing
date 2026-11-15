import numpy as np

# Loadings applied on top of the predicted cost
EXPENSE_LOADING = 1.10   # admin and claims-handling expenses
AGE_RATER_UNDER_65 = 1.11
AGE_RATER_65_PLUS = 1.13


class premium_pricing:

    def __init__(self):
        print("premium calculations started")

    # Premium = Predicted annual cost * Expense loading * Age rater
    def prem_calc(self, data, extra_cover=0):
        cost = data['Prediction'] + extra_cover
        age_rater = np.where(data['age'] <= 64, AGE_RATER_UNDER_65, AGE_RATER_65_PLUS)
        data['Member_premium'] = cost * EXPENSE_LOADING * age_rater

        print("premium calculations completed!")
        return round(float(np.sum(data['Member_premium'])), 2)
