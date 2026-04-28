
from xgboost import XGBRegressor

# define the quantiles
quantiles = {"q10": 0.1, "q50": 0.5, "q90": 0.9}

def train_quantile_models(X_train, y_train) -> dict:

    models = {}
    for name, alpha in quantiles.items(): # .items() -- on a dict, returns each key-value pair as a tuple
        model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        objective="reg:quantileerror", # ells XGBoost to use quantile loss instead of mean squared error
        quantile_alpha=alpha, # sets which quantile to target (0.1 = P10, 0.5 = P50, 0.9 = P90)
        )
        model.fit(X_train, y_train)
        models[name] = model
    return models