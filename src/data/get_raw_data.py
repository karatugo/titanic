
import requests
from requests import session
import os
from dotenv import load_dotenv, find_dotenv
import logging

payload = {
    "action": "login",
    "username": os.environ.get("KAGGLE_USERNAME"),
    "password": os.environ.get("KAGGLE_PASSWORD")
}

login_url = "https://www.kaggle.com/account/login"

def extract_data(file_path, url):

    with session() as s:
        s.post(login_url, data=payload)
        
        with open(file_path, "w") as handle:
            response = s.get(url, stream=True)
            
            for block in response.iter_content(1024):
                handle.write(block)

def main(project_dir):
    logger = logging.getLogger(__name__)
    logger.info("Getting raw data")
    
    training_data_url = "https://www.kaggle.com/c/titanic/download/train.csv"
    test_data_url = "https://www.kaggle.com/c/titanic/download/test.csv"
    
    raw_data_path = os.path.join(project_dir, 'data', 'raw')
    train_data_path = os.path.join(raw_data_path, 'train.csv')
    test_data_path = os.path.join(raw_data_path, 'test.csv')
    
    print train_data_path
    
    extract_data(train_data_path, training_data_url)
    extract_data(test_data_path, test_data_url)
    
    logger.info("Downloaded raw data")
    
    
if __name__ == "__main__":
    project_dir = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    main(project_dir)