import os

def get_openai_model_default():
    return os.environ.get('OPENAI_MODEL', 'gpt-4')
