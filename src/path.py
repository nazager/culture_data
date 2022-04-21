import os
from datetime import datetime
import logging

logging.basicConfig(filename='out.log', level=logging.INFO)


def mk_path(category):
    """
    Given a category creates the path where the information will be stored,
    in the following format: "category/yyyy-month/category-dd-mm-yyyy.csv"

    Parameters:
        category (str): The category name.

    Returns:
        dir_name, full_path (str, str): Returns dir_name to facilitate 
        directory-related tasks (i.e. checking if the directory exists)
        and full_path is the path where the csv will be saved 
        in the requested format.
    """
    logging.info("Making directory name and filename of {}.".format(category))
    try:
        date = datetime.now()
        file_name = category + '-' + str(date.strftime("%d-%m-%Y")) + '.csv'
        dir_name = category + '/' + str(date.strftime("%Y-%B")) + '/'
        full_path = os.path.join(dir_name, file_name)
    except Exception as e:
        logging.error("Error creating paths: {}".format(e))
    logging.info("Maked successfully.")
    return (dir_name, full_path)
