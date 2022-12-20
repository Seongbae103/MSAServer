from dataclasses import dataclass
import pandas as pd

@dataclass
class ScrapVO:
    html = ''
    parser = ''
    domain = ''
    query_string = ''
    headers = None
    tag_name = ''
    fname = ''
    class_names = []
    titles = []
    diction = {}
    df = None

    def dict_to_dataframe(self):
        print(len(self.diction))
        self.df = pd.DataFrame.from_dict(self.diction, orient='index')

    def dataframe_to_csv(self):
        path = f'./save/navermovie.csv'
        self.df.to_csv(path, na_rep="NaN", header=None)