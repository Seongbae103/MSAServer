from basic.mlearn.stroke.services import StrokeService
import numpy as np
import pandas as pd
from matplotlib import font_manager, rc
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from imblearn.under_sampling import RandomUnderSampler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt
font_path = "C:/Windows/Fonts/malgunbd.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

class StrokeModel:


    def __init__(self):
        global service
        service = StrokeService()

    def fit(self, flag):

        [X_train, X_test, y_train, y_test] = service.load_data()
        if flag == 'ccee':
            tree = DecisionTreeClassifier(criterion="entropy", random_state=0, max_depth=5)
            tree.fit(X_train, y_train)
            print("Accuracy on training set: {:.5f}".format(tree.score(X_train, y_train)))
            print("Accuracy on test set: {:.5f}".format(tree.score(X_test, y_test)))
        elif flag == 'gini':
            tree = DecisionTreeClassifier(criterion="gini", random_state=0, max_depth=5)
            params = {'criterion': ['gini', 'entropy'], 'max_depth': range(1, 21)}
            # 5회의 교차검증을 2개의 기준마다 20개의 max_depth 값으로 대입 (5 * 2 * 20 = 총 500회) 학습(fit) 됨
            grid_tree = GridSearchCV(
                tree,
                param_grid=params,
                scoring='accuracy',
                cv=5,  # 교차 검증 파라미터 5회실시
                n_jobs=-1,  # 멀티코어 CPU 모두 사용
                verbose=1  # 연산중간 메시지 출력
            )
            grid_tree.fit(X_train, y_train)
            tree.fit(X_train, y_train)
            print("GridSerchCV max accuracy: {:.5f}".format(grid_tree.best_score_))
            print("GridSerchCV best parameter: ", (grid_tree.best_params_))
            best_clf = grid_tree.best_estimator_
            pred = best_clf.predict(X_test)
            print("Accuracy on test set: {:.5f}".format(accuracy_score(y_test, pred)))
            print(f"Feature Importances: {best_clf.feature_importances_}")  # 최적 모델의 변수 중요도
            feature_names = list(self.data.columns)
            dft = pd.DataFrame(np.round(best_clf.feature_importances_, 4),
                               index=feature_names, columns=['Feature_importances'])
            dft1 = dft.sort_values(by="Feature_importances", ascending=False)
            print(dft1)
            ax = sns.barplot(y=dft1.index, x="Feature_importances", data=dft1)
            for p in ax.patches:
                ax.annotate("%.3f" % p.get_width(), (p.get_x() + p.get_width(), p.get_y() + 1),
                            xytext=(5, 10), textcoords='offset points')
            plt.show()