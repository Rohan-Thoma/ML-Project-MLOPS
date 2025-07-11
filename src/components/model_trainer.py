import os, sys
from dataclasses import dataclass 


from catboost import CatBoostRegressor
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging 

from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_filepath = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting train and test input data")
            X_train, y_train, X_test, y_test =(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbours Regression": KNeighborsRegressor(),
                "XGBRegression": XGBRegressor(),
                "CatBoosting Regression": CatBoostRegressor(verbose=False),
                "AdaBoost Regression": AdaBoostRegressor()
            }
            params={
            "Decision Tree": {
                'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,64,128,256]
            },
            "K-Neighbours Regression":{
                # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                'n_neighbors':[5,7,9,11]
            },
            "Linear Regression":{},
            "XGBRegression":{
                'learning_rate':[.1,.01,.05,.001],
                'n_estimators': [8,16,32,64,128,256]
            },
            "CatBoosting Regression":{
                'depth': [6,8,10],
                'learning_rate': [0.01, 0.05, 0.1],
                'iterations': [30, 50, 100]
            },
            "AdaBoost Regression":{
                'learning_rate':[.1,.01,0.5,.001],
                # 'loss':['linear','square','exponential'],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }

            model_report: dict = evaluate_models(X_train=X_train, y_train= y_train,
                                                 X_test= X_test, y_test=y_test, 
                                                 models = models,
                                                 param = params)

            #to get the best model score from dict
            best_model_score = max(sorted(model_report.values()))

            #to get the bets model name from the dict
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            if best_model_score< 0.6:
                logging.info("No best model found")
                return "No best model found"
            
            logging.info("Best model found on both training anf test dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_filepath,
                obj=best_model
            )
            
            predicted = best_model.predict(X_test)

            r2 = r2_score(y_test, predicted)
            return r2
        except Exception as e:
            raise CustomException(e, sys) #type: ignore
