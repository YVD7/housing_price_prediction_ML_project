

from email.mime import base
import imp

from sklearn import preprocessing
from housing.exception import HousingException
import sys
from housing.logger import logging
from typing import List
from housing.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from housing.entity.config_entity import ModelTrainerConfig
from housing.util.util import load_numpy_array_data, save_object, load_object
from housing.entity.model_factory import MetricInfoArtifact, ModelFactory, GridSearchedBestModel
from housing.entity.model_factory import evaluate_regression_model


class HousingEstimationModel:
    def __init__(self, preprocessing_object, trained_model_object):
        """
        TrainedModel contructor
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """

        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, x):

        """
        function accepts raw inputs and then transfromed raw input using preprocessing_object 
        which guarantees that the inputs are in the same format  as the training data
        At last it perform prediction to transformed features 
        """

        transformed_features  = self.preprocessing_object.transform(x)
        return self.trained_model_object.predict(transformed_features)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"


    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):

        try:
            logging.info(f"Loading transformed training dataset")
            transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
            train_array = load_numpy_array_data(file_path=transformed_train_file_path)

            logging.info(f"Loading transfromed testing dataset")
            transformed_train_file_path = self.data_transformation_artifact.transfromed_train_file_path
            test_array = load_numpy_array_data(file_path=transformed_train_file_path)


            logging.info(f"Splitting training and testing input and target feature")
            x_train, y_train, x_test, y_test = train_array[:,:-1], train_array[:,-1], test_array[:,:-1], test_array[:,-1]

            logging.info(f"Extracting model config file path")
            model_config_file_path = self.model_trainer_config.model_config_file_path

            logging.info(f"Initializing model factory class using above model config file: {model_config_file_path}")
            model_factory = ModelFactory(model_config_path=model_config_file_path)

            base_accuracy = self.model_trainer_config.base_accuracy
            logging.info(f"Expected accuracy:{base_accuracy }")

            logging.info(f"Initializing operation model selection")
            best_model = model_factory.get_best_model(X=x_train, y= y_train, base_accuracy=base_accuracy)

            logging.info(f"Best model found on triaining dataset: {best_model}")

            logging.info(f"Extracting trained model list.")
            grid_searched_best_model_list: List[GridSearchedBestModel] = model_factory.gird_searched_best_model_list


            model_list = [model.best_model for model in grid_searched_best_model_list]
            logging.info(f"Evaluation all trained model on training and testing dataset both")
            metric_info: MetricInfoArtifact = evaluate_regression_model(model_list= model_list, x_train = x_train, y_train = y_train, x_test= x_test, y_test = y_test)


            logging.info(f"Best found model on both training  and testing dataset. ")


            preprocessing_obj= load_object(file_path = self.data_transformation_artifact.preprocessed_object_file_path)
            model_object = metric_info(model_object)

            trained_model_file_path = self.model_trainer_config.trained_model_file_path
            housing_model =HousingEstimationModel(preprocessing_object=preprocessing_obj,trained_model_object=model_object)
            logging.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path = trained_model_file_path,obj = housing_model)


            model_trainer_artifact = ModelTrainerArtifact(is_trained = True, message = "Model Trained successfully", 
            trained_model_file_path  = trained_model_file_path,
            train_rmse = metric_info.train_rmse,
            test_rmse = metric_info.test_rmse,
            train_accuracy  = metric_info.train_accuracy,
            test_accuracy = metric_info.test_accuracy,
            model_accuracy = metric_info.model_accuracy
            
            
            )

            logging.info(f"Model Trainer Artifact : {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise HousingException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*30} Model Trainer log completed. {'<<'*30}")