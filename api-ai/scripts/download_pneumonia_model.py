import os

import requests
import tqdm

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


def download_model_from_s3():
    # Create pneumonia folder
    pneumonia_dir = os.path.join(ROOT_DIR, "models", "pneumonia")
    os.makedirs(pneumonia_dir, exist_ok=True)
    
    # Check if model already exists
    if os.path.exists(os.path.join(pneumonia_dir, "pytorch_model.bin")):
        print("Model already exists")
        return

    # Download pneumonia model
    with requests.get('https://ainomy-models.s3.eu-west-3.amazonaws.com/pneumonia/pytorch_model.bin', stream=True) as r:
        total_length = int(r.headers.get("Content-Length"))

        with open(os.path.join(ROOT_DIR, 'models', "pneumonia", "pytorch_model.bin"), 'wb') as file:
            for chunk in tqdm.tqdm(r.iter_content(chunk_size=1024), total=int(total_length / 1024), unit='KB'):
                file.write(chunk)

    with requests.get('https://ainomy-models.s3.eu-west-3.amazonaws.com/pneumonia/preprocessor_config.json', stream=True) as r:
        total_length = int(r.headers.get("Content-Length"))

        with open(os.path.join(ROOT_DIR, 'models', "pneumonia", "preprocessor_config.json"), 'wb') as file:
            for chunk in tqdm.tqdm(r.iter_content(chunk_size=1024), total=int(total_length / 1024), unit='KB'):
                file.write(chunk)

    with requests.get('https://ainomy-models.s3.eu-west-3.amazonaws.com/pneumonia/config.json', stream=True) as r:
        total_length = int(r.headers.get("Content-Length"))

        with open(os.path.join(ROOT_DIR, 'models', "pneumonia", "config.json"), 'wb') as file:
            for chunk in tqdm.tqdm(r.iter_content(chunk_size=1024), total=int(total_length / 1024), unit='KB'):
                file.write(chunk)


if __name__ == "__main__":
    download_model_from_s3()
