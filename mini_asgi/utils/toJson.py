import json

class ToJson:

    @staticmethod
    def convertStringToJson(stringToonvert)->(json):
        if type(stringToonvert) is not str or stringToonvert.strip() == '':
            raise ValueError("Provide a valid string to convert to json.")
        return json.loads(stringToonvert)