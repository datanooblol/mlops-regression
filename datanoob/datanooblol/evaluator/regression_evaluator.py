from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
# from math import sqrt
class _Evaluator:
    def __init__(self):
        pass
    
    def evaluate(self, y_actual=None, y_pred=None):
        # y_actual = y_actual.to_numpy().reshape(-1)
        # y_pred = y_pred.reshape(-1)
        # y_pred = model.predict(X)
        return {
            "mae": mean_absolute_error(y_actual, y_pred),
            "mse": mean_squared_error(y_actual, y_pred),
            "rmse": mean_squared_error(y_actual, y_pred, squared=True),
            "r2": r2_score(y_actual, y_pred),
            "mape": mean_absolute_percentage_error(y_actual, y_pred)
        }

class Evaluator:
    def __init__(self):
        pass
    
    def evaluate(self, model=None, X=None, y_actual=None):
        # y_actual = y_actual.to_numpy().reshape(-1)
        # y_pred = y_pred.reshape(-1)
        y_pred = model.predict(X)
        return {
            "mae": mean_absolute_error(y_actual, y_pred),
            "mse": mean_squared_error(y_actual, y_pred),
            "rmse": mean_squared_error(y_actual, y_pred, squared=True),
            "r2": r2_score(y_actual, y_pred),
            "mape": mean_absolute_percentage_error(y_actual, y_pred)
        }