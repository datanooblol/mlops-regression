import dtale
from datanooblol.configuration.config_manager import EDAConfig

class FastEDA:
    def __init__(self):
        self.eda_cfg = EDAConfig()
        
    def __call__(self, data):
        return self._display(data)
    
    def _display(self, data):
        return dtale.show(data, host=self.eda_cfg.HOST, port=self.eda_cfg.PORT)