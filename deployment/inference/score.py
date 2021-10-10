import json 

"""
Simple scoring script that returns the input
"""

def init():
    """Init method

    This method will be run once when the scoring script is deployed.

    """
    print("This is the inti() method")

def run(request):
    """run method
    Begins the entry script pipeline

    Args:
        request: string representation of Python-encoding JSON object.

    """
    print("This is the run() method")
    
    #load str
    payload = json.loads(request)
    
    return f"/n Returning the input for testing: {payload}"
