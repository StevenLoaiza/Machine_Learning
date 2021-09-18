"""
Azure Utility Class
"""
from azureml.core import Workspace, Environment
from azureml.core.model import InferenceConfig, Model
from azureml.core.compute import AksCompute
from azureml.core.webservice import AksWebservice
from azureml.core.conda_dependencies import CondaDependencies
import os
import json
import logging
import inspect
import argparse

# logger
logging.basicConfig(level=logging.INFO,
                    format="[%(filename)s - %(funcName)s(): %(asctime)s]  %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class AmlUtility:
    """Utility class for aml deployments
  
  Only supports Azure K8s service.
  """
  
    def __init__(self, config_path):
      """Initialize. Load configuration and defines the workspace
      
      Args:
          config_path (str): Path to json configuration
      """
      # Load config
      with open(config_path) as fp:
          config = json.load(fp)
      # Set workspace
      self.ws = Workspace.from_config()

      # Set config
      self.update_params = config['update_params']
      self.environment_params = config['environment_params']
      
    def environment_setup(self):
        """Configure python environment
        """
        # Initiate Env
        self.myenv = Environment(name=self.environment_params['name'])
        conda_dep = CondaDependencies.create(
            conda_packages=self.environment_params['conda_dependency'],
            pip_packages=self.environment_params['pip_dependency']
        )
        self.myenv.python.conda_dependencies = conda_dep   
        
    def update_aks(self, service_name, new_model):
        """Update an active aks web service
        
        Args:
            service_name (str): Name of the aks service
            new_model (str): Name of the new model to deploy in AKS
        """
        
        # aks service
        service = AksWebservice(self.ws, service_name)
    
        # updated model
        model = Model(self.ws,id=new_model)
    
        # Env
        self.environment_setup()
        
        # Specify prediction configuration - scoring script, running environment
        inference_config = InferenceConfig(**self.update_params['inference_config'])

        # Update AKS service
        service.update(
            inference_config=inference_config, 
            models=[model],  
            **self.update_params['aks_config']
        )
        service.wait_for_deployment(show_output = True)        
   
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=str,
                        dest='config_path',
                        help="Path to the configuration file",
                        required=True)
    parser.add_argument("--service_name", type=str,
                        dest='service_name',
                        help="Name of the aks endpoint",
                        required=True)
    parser.add_argument("--new_model", type=str,
                        dest='new_model',
                        help="Name of the registered model",
                        required=True)
    args = parser.parse_args()
    # Initiate Class
    aml = AmlDeployment(args.config_path)
    # Update Model
    aml.update_aks(args.service_name, args.new_model)  
  
