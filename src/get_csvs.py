import os
import requests
import logging
from path import mk_path

URLs = {"museos": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museo.csv",
        "cines": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv",
        "bibliotecas": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv"}

logging.basicConfig(filename='out.log', level=logging.INFO)


def get_csv(urls):
    """
    Given a dictionary with the categories and their respective urls of 
    the csv's, gets the csv's and stores them, finally return a list with
    the paths to the csv's.

    Parameters:
        urls (dict): Dictionary containing categories and urls ({category : url}).

    Returns:
        path_list (list): List containing paths to saved csv's.
    """

    logging.info("Sending the requests.")
    path_list = []
    for key, value in urls.items():
        try:
            csv = requests.get(value).content
        except Exception as e:
            logging.error("Error getting the csv's : {}".format(e))
        try:
            dir_name, full_path = mk_path(key)
            os.makedirs(dir_name, exist_ok=True)
            open(full_path, 'wb').write(csv)
            path_list.append(full_path)
        except Exception as e:
            logging.error("Error writing the csv's: {}".format(e))
    logging.info("Csv's received and stored successfully.")
    return path_list
