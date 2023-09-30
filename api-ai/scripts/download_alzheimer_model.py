import os

import requests
import tqdm

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


def download_model_from_s3():
    models_dir = os.path.join(ROOT_DIR, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Check if model already exists
    if os.path.exists(os.path.join(models_dir, "alzheimer.pt")):
        print("Model already exists")
        return

    # Download alzheimer model
    with requests.get('https://ainomy-models.s3.eu-west-3.amazonaws.com/alzheimer/alzheimer.pt', stream=True) as r:
        total_length = int(r.headers.get("Content-Length"))

        with open(os.path.join(ROOT_DIR, 'models', "alzheimer.pt"), 'wb') as file:
            for chunk in tqdm.tqdm(r.iter_content(chunk_size=1024), total=int(total_length / 1024), unit='KB'):
                file.write(chunk)

if __name__ == "__main__":
    download_model_from_s3()
