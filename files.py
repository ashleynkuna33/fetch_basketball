import csv
import os

class FileHandler:
    def __init__(self, path:str, tokens:bool=False, encoding:str="utf-8"):
        self.osdir = path
        self.encoding = encoding

        self.results = self.read_csv("results.csv", True)
        self.fixtures = self.read_csv("fixtures.csv", True)
        if tokens:
            self.keys_results = self.create_event_indicators(self.results)
            self.keys_fixtures = self.create_event_indicators(self.fixtures)


    def create_event_indicators(self, data):
        return None

    def write_to_csv(self, file_name:str, data:list, batch:bool):
        try:
            filename = os.path.join(self.osdir, file_name)
            with open(filename, mode="a", newline="", encoding=self.encoding) as file:
                writer = csv.writer(file)
                if batch:
                    writer.writerows(data)
                else:
                    writer.writerow(data)
        except Exception as e:
            print(f"Error:\n{e}")
        
    def read_csv(self, file_name:str, data:bool):
        try:
            filename = os.path.join(self.osdir, file_name)
            with open(filename, mode="r", newline="", encoding=self.encoding) as file:
                reader = csv.DictReader(file)
                if data:
                    headers = reader.fieldnames
                    data = [tuple(row[col] for col in headers) for row in reader]
                else:
                    data = [row["url"] for row in reader if "url" in row]
            return data
        except FileNotFoundError:
            print(f"File {file_name} not found.")
        except KeyError:
            print(f"'url' column not found in {file_name}.")
        
        return []

# a = FileHandler("C:/Users/ashx4/downloads/Production/fetch_basketball/Data",False)
