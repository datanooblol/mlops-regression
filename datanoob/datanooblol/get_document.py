import os

# these below functions needed to be revised as a general function for using in other projects

def init_doc() -> None:
    """
    Initialize doc
    
    """
    path = "/usr/src/datanoob/_docs"
    command = f"cd {path} && make html"
    os.system(command)
    copy_to()

def update_doc() -> None:
    """
    Update doc
    
    """
    path = "/usr/src/datanoob"
    module_path = "datanooblol/"
    command = f"cd {path} && sphinx-apidoc -o _docs {module_path}"
    updated = os.system(command)
    if updated == 0:
        print("updated successfully")
    
    path = "/usr/src/datanoob/_docs"
    command = f"cd {path} && make clean html"
    generated = os.system(command)
    if generated == 0:
        copy_to()
        print("generated successfully")

def copy_to() -> None:
    """
    Copy to document
    
    """
    source = "/usr/src/datanoob/_docs/_build/html/*"
    target = "/usr/src/datanoob/document"
    os.system(f"cp -Rf {source} {target}")