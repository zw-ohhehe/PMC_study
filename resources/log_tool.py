import os
import json


class Log:
    def __init__(self, path):
        self.path = path
        os.mkdir(path)

    def write(self, data, file_nmae, indent=2):
        with open(os.path.join(self.path, file_nmae), 'w') as f:
            json.dump(data, f, indent=indent)


