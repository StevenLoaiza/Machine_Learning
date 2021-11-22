# Data Science and Programming in Python

-- TODO Introduction
# <a id="toolkit"> Data Science Toolkit </a>

## <a id="sql"> Introduction to Structure Query Language </a>

### <a id="general"> General Layout </a>
Below we cover a few base components that make up a sql database:

1.	Schema: It is a container that stores collections of tables, procedures and metadata.
2.	Table: Structure data in a tabular form (such as an excel table).
    1.	Primary Key: It is a column that uniquely identifies each row.
    2.	Foreign Key: It is a column that maps a table to another through the relationship between primary key – foreign key.

![image](https://user-images.githubusercontent.com/46308439/131370112-f12d3ced-af70-4918-bbf9-83d44fc944ba.png)

### <a id="join"> Joins </a>

![image](https://user-images.githubusercontent.com/46308439/131388527-df52aa31-3e1b-422a-b4e1-d6598df45a0d.png)

Let assume we have two seperate tables with an (id) column and a (var) column. Our Goal is to Combine
the tables together.

| id|Val|
|---|---|
|  1| L1|
|  2| L2|
|  3| L3|   
|  4| L4|

| id|Val|
|---|---|
|  1| R1|
|  4| R2|
|  5| R3|
|  6| R4|

The left table column (id) is called a Primary Key, while the right column (id) is called the Foreign
Key . We use foreign keys and primary keys to connect rows in two different tables. One table's foreign
key holds the value of another table's primary key. The most common types of joins will be joining a foreign
key from one table with the primary key from another table.

Now we will use the Query INNER JOIN on both tables above. The INNER JOIN function will combine
the tables above, for the (id) values that are an exact match and discard the rest. The results would look
like this:
|id_L| L_Val| R_Val|
|----|------|------|
|1 |L1 |R1 |
|4 |L4 |R2 |

Given our example above, our SQL query would look like:

```sql
SELECT *
FROM 
  Left_Table
INNER JOIN Right.Table
  ON Left_Table.id=Right_Table.id
```

# <a id="simple">A Simple Approach</a>
A Brief Introduction to the world of Machine Learning. In this article we begin with two easy to understand supervised learning concepts [Linear Regressions & K- Nearest Neighborhood Method](https://github.com/StevenLoaiza/Machine_Learning/blob/master/Introduction/Machine%20Learning%20-%20A%20simple%20approach.ipynb)


# <a id="tree" href="https://github.com/StevenLoaiza/Machine_Learning/tree/master/Decision%20Trees"> Decision Trees</a>

This section is part of a larger effort to create a comprehensive compliation of lessons related to Data Science and Programming in Python.

The project "Decision Tree" hold 3 key lessons:
- Entropy and Information Gain
- Gini Impurity Measure
- Making Decisions with Trees

Each of the lessons above helps the reader decipher the inner workings of tree base algorithms. Keep in mind that this section is a introduction and will go over the building blocks of the algorithm.

# <a id="opti"> Optimization Methods </a>

## <a id="grad"> Gradient Descent </a>

![](https://github.com/StevenLoaiza/Machine_Learning/blob/master/optimize/gradient_animation.gif)

# <a id="deploy">Deployment - Modeling Services</a>

## <a id="k8s">Kubernetes</a>
### <a id="zero">How does Azure Kubernetes service perform zero downtime updates?</a>
Machine learning models have a life cycle and a part of that cycle is retraining/redeploying. There are many reasons why a model requires an update (e.g. feature drift, different relationship between covariates and target, improvements, regular refresh, etc). Assuming the model is a real-time application in Azure Kubernetes Services (AKS), how do we update the model without interrupting the service?

Assumptions: Familiar with [Azure Machine Learning](https://docs.microsoft.com/en-us/python/api/overview/azure/ml/?view=azure-ml-py) software development kit (SDK) and [Kubernetes](https://kubernetes.io/).

![image](https://user-images.githubusercontent.com/46308439/142789874-1b1ab34a-09ed-4108-bd5f-7c42a06f3fce.png)

**Kubernetes Update Workflow**

Kubernetes has promoted zero-downtime updates of deployed models. In other words, the modeling service would not be interrupted by the update and it will continue to process requests without error.

Updates are performed in a staged manner to ensure that the application is not impacted. Assume that you have already deployed the first version of your container image (model) on the Azure Kubernetes cluster. You have developed a second version of the model and are now ready to update the existing web service.

1. Create an image and submit the update to the web service (Python example below).
2. Since this is a gradual rollout one new pod is created with version#2 and it is added to the load balancer.
3. A Pod with version#1 of the image will be deleted and the load balancer will stop sending requests to the pod. Although, the pod is deleted it remains active to complete any request it is still processing (the default termination grace period is 30 seconds [[1]](#k8s_ref1)).
4. Repeat, until all pods in the deployment have version#2 of the image.

![](https://github.com/StevenLoaiza/Machine_Learning/blob/master/deployment/images/k8s_update.gif)

**Python Implementation**

Now that you understand the concept of updating an image on AKS, we will discuss how to implement it via python. The code and config files are located on [GitHub](https://github.com/StevenLoaiza/Machine_Learning/tree/master/deployment).

```json
{
    "environment_params": {
        "name": "my-env-name",
        "conda_dependency": ["numpy", "scikit-learn==0.22.2.post1", "scipy"],
        "pip_dependency": ["azureml-defaults", "inference-schema"]
    }  
    "update_params": {
        "inference_config": {
            "entry_script": "score.py",
            "inference_path": "inference"
        },
        "aks_config": {
            "autoscale_enabled": true, 
            "memory_gb": 8
        }
    }    
}
```
Below is the AmlUtility class defined in azure_utils.py. The class has a few functions to load the config file, set the environment, define the inference config, load the new model, and deploy the update.

```python
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
        inference_config = InferenceConfig(**self.update_params['inference_config'], environment=self.myenv)

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
view rawazure_utils.py hosted with ❤ by GitHub
```

The sample script to run on the terminal, from the directory where the utility script is stored, is:
```bash
python azure_util.py --config_path config.json --service_name current_deployment_name --new_model model_name:2
```
As long as there are no bugs, the logs on the terminal will display when the modeling service update is complete.

Pre-requisites
* AML workspace, compute instance, AKS inference cluster
* A deployed AKS service
* A new version of the model
The update method has many parameters that can be changed [4], by default they are set to **None** and will remain unchanged. When updating the modeling service I include the inference config (specify the environment and path to the scoring scripts), the model, autoscale, and memory.

**Conclusion**

This article is intended for educational purposes. Updating a production modeling service will likely fall outside the scope of a Data Scientist's purview. There are costs associated with downtime, therefore updating and minimizing the cost is best left to other specialized teams. But this is still a useful feature to use during the development phase as you iterate through different versions.

**References**

* [1]: <a id="k8s_ref1">https://learnk8s.io/graceful-shutdown</a>
* [2]: <a id="k8s_ref2">https://www.youtube.com/watch?v=mNK14yXIZF4</a>
* [3]: <a id="k8s_ref3">https://kubernetes.io/docs/concepts/workloads/pods/</a>
* [4]: <a id="k8s_ref4">https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.webservice.akswebservice?view=azure-ml-py</a>

**Issues**

Two issues I came across when testing `AksWebservie.update()` [[4]](#k8s_ref4):
* Relating to point #3 you may see an *“Error: Replica closed connection before replying”*. This occurred because the request was not completed before the pod was completely deleted. **Solution**: Configure the termination grace period of the pods, likely beyond the scope of the Data Scientist.[3]
* If the image is dumping logs via the ModelDataCollector you may run into lost logs during deployment. I did not find documentation relating to this issue. **Solution**: Update image during off-peak hours to minimize lost request logs.
