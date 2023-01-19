from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from imblearn.under_sampling import RandomUnderSampler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

class StrokeService():
    def __init__(self):
        pass

    def load_data(self):
        data = self.data
        target = self.target
        undersample = RandomUnderSampler(sampling_strategy=0.333, random_state=2)
        data_under, target_under = undersample.fit_resample(data, target)
        print(target_under.value_counts(dropna=True))
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(data_under, target_under,
                                                                                test_size=0.5, random_state=42,
                                                                                stratify=target_under)
        print("X_train shape:", self.X_train.shape)
        print("X_test shape:", self.X_test.shape)
        print("y_train shape:", self.y_train.shape)
        print("y_test shape:", self.y_test.shape)

        return [self.X_train, self.X_test, self.y_train, self.y_test]