import json

class UserPreferences:
    def __init__(self, prefs_file='user_preferences.json'):
        self.prefs_file = prefs_file
        self.preferences = self.load_preferences()

    def load_preferences(self):
        try:
            with open(self.prefs_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}  # Ritorna un dizionario vuoto se il file non esiste

    def save_preferences(self):
        with open(self.prefs_file, 'w') as f:
            json.dump(self.preferences, f, indent=4)

    def get_preference(self, key, default=None):
        return self.preferences.get(key, default)

    def set_preference(self, key, value):
        self.preferences[key] = value
        self.save_preferences()
    

