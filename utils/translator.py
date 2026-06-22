import json
import os


class Translator:
    def __init__(self, language_file="lang/en.json"):
        self.language_file = language_file
        self.translations = {}

        self.load()

    def load(self):
        try:
            with open(self.language_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)

        except Exception as e:
            print(f"Language loading error: {e}")
            self.translations = {}

    def get(self, key):
        return self.translations.get(key, key)