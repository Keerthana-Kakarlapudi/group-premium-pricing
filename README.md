# Group Health Premium Calculator

A rebuild, on public data, of a group health premium engine I built at Fedo Health Technologies. The original was used to onboard a health insurance company as a paying client; this version keeps the same design but uses a public dataset, since the original data belonged to the client.

## How it works

1. **Upload** a CSV of group members (age, sex, BMI, children, smoker, region).
2. **Predict** each member's expected annual medical cost with a LightGBM model.
3. **Price** the group: predicted cost × expense loading × age rater, summed across members.

The app also prices a variant with extra cover per member, to show how a plan change moves the group premium.

## Results

Trained on 80% of the data, tested on the remaining 20%:

| Model | Mean absolute error | R² |
|---|---|---|
| Linear regression (baseline) | 4,187 | 0.78 |
| LightGBM | 2,474 | 0.87 |

Premiums are set at group level, so the more useful check is error on a group's total cost. Across 200 sampled groups of 50 members, the predicted total was off by **3.9% on average**.

## Run it

```bash
pip install -r requirements.txt
python train_model.py   # trains the model and prints the results above
python app.py           # opens the calculator at http://127.0.0.1:5000
```

Try it with `data/sample_group.csv` (40 members).

## Files

| File | What it does |
|---|---|
| `preprocessing.py` | Fills default values and encodes member features |
| `train_model.py` | Trains and evaluates the cost model, saves it to `models/` |
| `model.py` | Loads the model and predicts cost per member |
| `prem_calc.py` | Applies loadings and returns the group premium |
| `app.py`, `templates/demo.html` | Flask app for uploading a group file |

## Data and limits

- Data: the public *Medical Cost Personal Datasets* (1,338 US individuals, annual charges in USD), originally from *Machine Learning with R* by Brett Lantz. Amounts are in USD, not INR.
- The original engine also used diagnosis codes (ICD) and an age-based incidence rate. This dataset has neither, and each row's charges are already an annual cost, so those steps are left out.
- Loadings in `prem_calc.py` are illustrative, not a real insurer's rates.
