import json
import random

class words():
    def __init__(self):
        self.word = None

    def getNewWord(self) -> str:
        with open('words.json') as f:
            data = json.load(f)
            wordlistlen = len(data['words'])
            self.word = data['words'][random.randint(0, wordlistlen) - 1]
            return self.word
    
    def getCurrent(self) -> str:
        return self.word