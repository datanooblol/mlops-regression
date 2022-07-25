# classification

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import itertools

class ModelBuilder:
    """
    Deprecated
    
    """
    def __init__(self):
        self.seed=555

    def build(self) -> list:
        return [
            ("logit", LogisticRegression(), {"default":"default"}),
            ("svc", SVC(probability=True, random_state=self.seed), {"default":"default"}),
            ("dt", DecisionTreeClassifier(random_state=self.seed), {"default":"default"}),
            ("knn", KNeighborsClassifier(), {"default":"default"}),
            ("rf", RandomForestClassifier(random_state=self.seed), {"default":"default"}),
            ("adaboost", AdaBoostClassifier(random_state=self.seed), {"default":"default"}),
        ]