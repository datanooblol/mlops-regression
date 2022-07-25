# classification
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import itertools

# regression
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor



class ModelBuilder:
    """
    Pack models into a single list including model name, model object, and tuning parameters
    
    """
    def __init__(self):
        self.seed=555  
    
    def build(self, model_name:str=None, model=None, parameters:dict=None) -> list:
        param_list = []
        param_name = list(parameters.keys())
        if "default" not in param_name:
            param_value = list(parameters.values())
            param_value = list(itertools.product(*param_value))
            for param in param_value:
                param_list.append({k:v for k, v in zip(param_name, param)})
            return [(model_name, model(**param_dict), param_dict) for param_dict in param_list]
        else:
            return [(model_name, model(), parameters)]