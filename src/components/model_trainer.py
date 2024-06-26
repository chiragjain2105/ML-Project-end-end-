import pandas as pd
import numpy as np
from src.logger.logging import logging
from src.exception.exception import customException
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from src.utils.utils import evaluate_model,save_objects
from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self,train_array,test_array):
        try:
            logging.info("Splitting dependent and indipendent variables from train and test data")
            X_train,y_train,X_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                'LinearRegression':LinearRegression(),
                'Lasso':Lasso(),
                'Ridge':Ridge(),
                'ElasticNet':ElasticNet()
            }

            model_report:dict = evaluate_model(X_train,y_train,X_test,y_test,models)
            print(model_report)

            print("-----------------------------------------------------------")

            logging.info(f'Model report: {model_report}')

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            print(f'Best Model Found, Model Name : {best_model_name}, R2 score : {best_model_score}')
            print("-------------------------------------------------------------")
            logging.info(f'Best Model Found, Model Name : {best_model_name}, R2 score : {best_model_score}')

            save_objects(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )


        except Exception as e:
            logging.info("Exception occured at model training")
            raise customException(e,sys)