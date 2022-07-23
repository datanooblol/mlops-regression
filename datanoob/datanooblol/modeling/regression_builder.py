from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

class ModelBuilder:
    def __init__(self):
        self.seed=555

    def build(self) -> list:
        return [
            ("lr", LinearRegression(), {"default":"default"}),
            ("svm", SVR(), {"default":"default"}),
            ("lasso", Lasso(), {"default":"default"}),
            ("ridge", Ridge(), {"default":"default"}),
            ("elastic", ElasticNet(random_state=self.seed), {"default":"default"}),
            ("knn", KNeighborsRegressor(), {"default":"default"}),
            ("dt", DecisionTreeRegressor(random_state=self.seed), {"default":"default"}),
            ("rf", RandomForestRegressor(random_state=self.seed), {"default":"default"}),
            ("gboost", GradientBoostingRegressor(random_state=self.seed), {"default":"default"}),
        ]