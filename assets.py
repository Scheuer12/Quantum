import json
import re
import os

def load_user_data():
    with open('data/user_data.json', 'r') as f:
        # Remove possible comments and trailing commas for safety
        content = f.read()
        content = re.sub(r'//.*', '', content)
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)

def save_user_data(data):
    with open('data/user_data.json', 'w') as f:
        json.dump(data, f, indent=4)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_narrative():
    with open('data/narrative.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def load_experiments():
    with open("data/experiments.json", 'r') as exp:
        content = exp.read()
        content = re.sub(r'//.*', '', content)
        content = re.sub(r',\s*([}\]])', r'\1', content)

        return json.loads(content)
    
def load_particles():
    with open("data/particles_data.json", 'r') as exp:
        content = exp.read()
        content = re.sub(r'//.*', '', content)
        content = re.sub(r',\s*([}\]])', r'\1', content)

        return json.loads(content)