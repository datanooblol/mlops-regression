from importlib import import_module

class ModelCatalogue:
    """
    A list of models available for experiment
    
    """
    def __init__(self):
        self.model_catalogue = {
            "LinearRegression": f"sklearn.linear_model",
            "Lasso": f"sklearn.linear_model",
            "Ridge": f"sklearn.linear_model",
            "ElasticNet": f"sklearn.linear_model",
            "SVR": f"sklearn.svm",
            "KNeighborsRegressor": f"sklearn.neighbors",
            "DecisionTreeRegressor": f"sklearn.tree",
            "RandomForestRegressor": f"sklearn.ensemble",
            "GradientBoostingRegressor": f"sklearn.ensemble",
        }
    
    
    def get_model(self, model_name):
        model_path = self.model_catalogue[model_name]
        return getattr(import_module(f"{model_path}"), f"{model_name}")