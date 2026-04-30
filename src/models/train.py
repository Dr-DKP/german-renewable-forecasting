
# Import libraries
import mlflow
import mlflow.xgboost
from sklearn.model_selection import train_test_split
from src.data.training_matrix import build_training_matrix
from src.models.quantile_model import train_quantile_models
from src.models.conformal import fit_conformal
from src.evaluation.metrics import mae, rmse

# Constant
EXPERIMENT_NAME = "solar-residual-quantile"

def train_and_log():
    # Load X and y from training_matrix module from src
    X, y = build_training_matrix()
    # carve off the test set (last 20%)
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    # carve off the calibration (last 12.5% of 80% is 10% of total)
    X_train, X_cal, y_train, y_cal = train_test_split(X_temp, y_temp, test_size=0.125, shuffle=False)
    # shapes of X_train, X_test, and X_cal
    print(f"The sahapes of X_train is {X_train.shape}, X_test is {X_test.shape}, and X_cal is {X_cal.shape}")
    # Create experimental bucket in MLflow
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run():
        # Training: Train the three quantile models (q10, q50, q90)
        models = train_quantile_models(X_train, y_train)
        # --- Calibration (Conformal Prediction) ---
        q_hat_p50 = fit_conformal(models["q50"], X_cal, y_cal, alpha=0.5)
        q_hat_p90 = fit_conformal(models["q90"], X_cal, y_cal, alpha=0.9) # p90 uses the lower/upper bounds
        # --- Evaluation ---
        y_pred = models["q50"].predict(X_test)
        test_mae = mae(y_test, y_pred)
        test_rmse = rmse(y_test, y_pred)
        # --- Logging Hyperparameters ---
        mlflow.log_param("n_estimators", 300)
        mlflow.log_param("learning_rate", 0.05)
        mlflow.log_param("max_depth", 6)
        # --- Log Confromal Buffer ---
        mlflow.log_param("q_hat_p50", q_hat_p50)
        mlflow.log_param("q_hat_p90", q_hat_p90)
        # --- Log Metrices ---
        mlflow.log_metric("mae", test_mae)
        mlflow.log_metric("rmse", test_rmse)
        # --- Saving the models ---
        for name, model in models.items():
            # This saves the model file into the MLflow directory
            mlflow.xgboost.log_model(model, artifact_path=name)
        # --- Print the ID ---
        print(f"Run logged successfully! ID: {mlflow.active_run().info.run_id}")

if __name__ == "__main__":
    train_and_log()
