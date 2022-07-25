class BaseFitTransform:
    """
    BaseClass for any classes that are needed to use .fit method
    
    """
    def __init__(self):
        self._is_fit = False
        self.features = None

    def _fit(self, X):
        pass

    def _transform(self, X):
        pass
    
    def fit(self, X):
        self._fit(X)
        self._is_fit = True
        return self

    def transform(self, X):
        if self._is_fit == False:
            raise Exception(".fit method must be implemented before .transform")
        return self._transform(X)
    
    def fit_transform(self, X):
        return self.fit(X).transform(X)