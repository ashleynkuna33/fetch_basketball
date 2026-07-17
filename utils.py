import json

def load_json(path:str):
    data = None
    try:
        with open(path, "r") as file:
            data = json.load(file)
    except Exception as e:
        print(f"An error has occured while trying to open file in path: {path}\n{e}")
    
    return data