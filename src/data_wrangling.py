import pandas as pd
import logging
from datetime import datetime
from get_csvs import get_csv, URLs

logging.basicConfig(filename='out.log', level=logging.INFO)

# Subset of columns to be extracted for the table 1
cols = ['Cod_Loc', 'IdProvincia', 'IdDepartamento', 'Categoría', 'Provincia',
        'Localidad', 'Nombre', 'Dirección', 'CP', 'Teléfono', 'Mail', 'Web',
        'Fecha_de_carga']

# Columns data types
dtypes = {'Cod_Loc': float, 'IdProvincia': float, 'IdDepartamento': float,
          'Categoría': str, 'Provincia': str, 'Localidad': str,
          'Nombre': str, 'Dirección': str, 'CP': str, 'Teléfono': str,
          'Mail': str, 'Web': str}


def normal_museos(path):
    """
    Given the path of the museum csv returns a normalized pandas dataframe

    Parameters:
        path (str): Path to the csv.

    Returns:
        df (pd.DataFrame): Normalized dataframe with the csv data.
    """

    df = pd.read_csv(path, sep=',', encoding='UTF-8')
    df.rename(columns={'categoria': 'Categoría', 'provincia': 'Provincia', 'localidad': 'Localidad',
                       'nombre': 'Nombre', 'direccion': 'Dirección', 'telefono': 'Teléfono',
                       'fuente': 'Fuente'}, inplace=True)
    return df.astype(dtype=dtypes)


def normal_cines(path):
    """
    Given the path of the cinema csv returns a normalized pandas dataframe

    Parameters:
        path (str): Path to the csv.

    Returns:
        df (pd.DataFrame): Normalized dataframe with the csv data.
    """

    df = pd.read_csv(path, sep=',', encoding='UTF-8')
    return df.astype(dtype=dtypes)


def normal_biblio(path):
    """
    Given the path of the library csv returns a normalized pandas dataframe

    Parameters:
        path (str): Path to the csv.

    Returns:
        df (pd.DataFrame): Normalized dataframe with the csv data.
    """
    df = pd.read_csv(path, sep=',', encoding='UTF-8')
    df.rename(columns={'Domicilio': 'Dirección'}, inplace=True)
    return df.astype(dtype=dtypes)


def normal_all(path_list):
    """
    Given a list of paths to csv's returns all the normalized data in a pandas
    dataframe.

    Parameters:
        path_list (list): Path list to the csv's to normalize.

    Returns:
        df (pd.DataFrame): Normalized dataframe with all csv's data.
    """
    df_list = []
    categories = {"museos": normal_museos,
                  "cines": normal_cines,
                  "bibliotecas": normal_biblio}
    try:
        for path in path_list:
            cat = path.split("/")[0]
            normal = categories[cat](path)
            df_list.append(normal)
    except Exception as e:
        logging.error("Normalization error: {}".format(e))
    logging.info("Data normalization done.")
    df = pd.concat(df_list, ignore_index=True)
    df["Fecha_de_carga"] = datetime.now().strftime("%d-%m-%Y")
    return df


def data_proc_cultura(df: pd.DataFrame):
    """
    Adds a column with the loading date to the dataframe.

    Parameters:
        df (pd.Dataframe): Dataframe to which is added the column.

    Returns:
        df (pd.DataFrame): Dataframe with the new column.
    """

    logging.info("Creating table 1...")
    try:
        df["Fecha_de_carga"] = datetime.now().strftime("%d-%m-%Y")
    except Exception as e:
        logging.error("Cannot create table 1: {}".format(e))
    logging.info("Table 1 created successfully.")
    return df[cols]


def data_proc_totals(df: pd.DataFrame):
    """
    Given the dataframe with the normalized data returns a new dataframe
    containing the number of records by category, numbers of records
    by source and the number of records by state and category.

    Parameters:
        df (pd.Dataframe): Dataframe to which records are counted in columns.

    Returns:
        t3 (pd.DataFrame): Dataframe with the new data.
    """
    logging.info("Creating table 2...")
    try:
        a = df.groupby("Categoría").size().to_frame(name="Total_categoría")
        b = df.groupby("Fuente", dropna=True).size().to_frame(
            name="Total_fuente")
        c = df.groupby(["Provincia", "Categoría"],).size().to_frame(
            name="Total_provincia_categoría")
        t2 = a.join(c)
        t2.reset_index(inplace=True)
        b.reset_index(inplace=True)
        t3 = t2.join(b)
        t3["Fecha_de_carga"] = datetime.now().strftime("%d-%m-%Y")
    except Exception as e:
        logging.error("Cannot create table 2: {}".format(e))
    logging.info("Table 2 created successfully.")
    return t3


def data_proc_cines(df: pd.DataFrame):
    """
    Given the dataframe with the normalized data returns a new dataframe
    containing the state, number of screens, number of seats and 
    number of INCAA spaces.

    Parameters:
        df (pd.Dataframe): Dataframe to which records are counted in columns.

    Returns:
        t3 (pd.DataFrame): Dataframe with the new data.
    """
    logging.info("Creating table 3...")
    try:
        a = pd.DataFrame(
            df, columns=['Provincia', 'Pantallas', 'Butacas', 'espacio_INCAA'])
        a[['Provincia', 'Pantallas', 'Butacas']] = a[[
            'Provincia', 'Pantallas', 'Butacas']].fillna(0)
        a['espacio_INCAA'] = a['espacio_INCAA'].replace(
            to_replace=["SI", "si"], value=1).fillna(0).astype(int)
        cine = a.groupby('Provincia').agg({'Pantallas': sum,
                                           'Butacas': sum,
                                           'espacio_INCAA': sum})
        cine["Fecha_de_carga"] = datetime.now().strftime("%d-%m-%Y")
    except Exception as e:
        logging.error("Cannot create table 3 : {}".format(e))
    logging.info("Table 3 created successfully.")
    return cine


if __name__ == "__main__":
    path_list = get_csv(URLs)
    df = normal_all(path_list)
    cine = data_proc_cines(df)
    cine.to_csv("cine.csv", sep='\t', encoding='utf-8')
    print(cine.head(n=5))
