import pandas as pd
import numpy as np

class HealthCheck:
    def __init__(self):
        pass
    
    def summary_tbl(self, data: pd.DataFrame) -> pd.DataFrame:
        result = pd.DataFrame({
            "dtype":data.dtypes.values,
            "cnt_missing":data.isna().sum(),
            "ratio_missing":(data.isna().sum()/data.shape[0])*100,
            "n_unique":data.nunique(),
            "ratio_unique":(data.nunique()/data.shape[0])*100
        }, 
            index=data.columns, 
        )
        return result

    def summary(self, data: pd.DataFrame) -> str:
        """
        Quick summary for data quality  
        
        :param pd.DataFrame data: data needed to be checked
        :returns: a summary table
        :rtype: str
        """
        summary_df = self.summary_tbl(data=data)
        columns = summary_df.index
        for column in columns:
            if data[column].dtypes == "object":
                least = data[column].value_counts().index[-1]
                most = data[column].value_counts().index[0]
            elif data[column].dtypes == "datetime":
                least = data[column].value_counts().index[-1]
                most = data[column].value_counts().index[0]
            elif data[column].dtypes == "category":
                least = data[column].astype("object").value_counts().index[-1]
                most = data[column].astype("object").value_counts().index[0]                
            else:
                least = data[column].min()
                most = data[column].max()
        
            summary_df.loc[column,"least"] = least
            summary_df.loc[column,"most"] = most
        print(summary_df.round(2).to_markdown())
        print("\n")
        print(f"row: {data.shape[0]}, col: {data.shape[1]}")