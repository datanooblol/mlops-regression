import os

def init_doc():
    """
    Initialize doc
    
    """
    path = "/usr/src/datanoob/_docs"
    command = f"cd {path} && make html"
    os.system(command)
    return

def update_doc():
    """
    Update doc
    
    """
    
    path = "/usr/src/datanoob/_docs"
    command = f"cd {path} && make clean html"
    os.system(command)
    return