# Trains the cost model on the public insurance dataset and saves it.
import pickle
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from preprocessing import PreProcess, FEATURES

data = pd.read_csv('data/insurance.csv')
pp = PreProcess()
data = pp.processing(pp.default(data))

X = data[FEATURES]
y = data['charges']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Baseline: linear regression
lin = LinearRegression().fit(X_train, y_train)
lin_pred = lin.predict(X_test)

# Main model: LightGBM
model = lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, num_leaves=15,
                          min_child_samples=20, random_state=42, verbose=-1)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print(f"Linear regression  MAE: {mean_absolute_error(y_test, lin_pred):,.0f}   R2: {r2_score(y_test, lin_pred):.3f}")
print(f"LightGBM           MAE: {mean_absolute_error(y_test, pred):,.0f}   R2: {r2_score(y_test, pred):.3f}")

# Group-level check: premiums are priced on group totals, so sample 200 groups of 50 members
test = pd.DataFrame({'actual': y_test.values, 'predicted': pred})
errors = []
for i in range(200):
    g = test.sample(50, random_state=i)
    errors.append(abs(g['predicted'].sum() - g['actual'].sum()) / g['actual'].sum())
print(f"Groups of 50: average error on total group cost {sum(errors)/len(errors):.1%} (200 sampled groups)")

pickle.dump(model, open('models/cost_model.pkl', 'wb'))
print("Model saved to models/cost_model.pkl")
