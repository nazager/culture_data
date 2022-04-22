import logging
from get_csvs import get_csv, URLs
from data_wrangling import normal_all, data_proc_totals, data_proc_cines, data_proc_cultura
from sqlalchemy import create_engine
from decouple import config

logging.basicConfig(filename='out.log', level=logging.INFO)

if __name__ == "__main__":
    try:
        URI = "postgresql://" + config("DB_USER") + ':' + config("DB_PASS") + '@' + config(
            "DB_HOST") + ':' + config("DB_PORT") + '/' + config("DB_NAME")
    except:
        logging.error("Invalid database configuration")
    path_list = get_csv(URLs)
    full_df = normal_all(path_list)
    df1 = data_proc_cultura(full_df)
    df2 = data_proc_totals(full_df)
    df3 = data_proc_cines(full_df)
    db_engine = create_engine(URI)
    conn = db_engine.connect()
    logging.info("DB connection accepted.")
    try:
        conn.execute(open("db/db_cine_summry_table.sql").read())
        conn.execute(open("db/db_culture_table.sql").read())
        conn.execute(open("db/db_regs_count_table.sql").read())
    except Exception as e:
        logging.error("Error creating tables: {}".format(e))
    logging.info("Tables created successfully.")
    try:
        df1.to_sql("cultura", con=conn, if_exists='replace', index=False)
        df2.to_sql("regs_count", con=conn, if_exists='replace', index=False)
        df3.to_sql("cine_summary", con=conn, if_exists='replace', index=False)
    except Exception as e:
        logging.error("Error uploading tables to the db: {}".format(e))
    logging.info("Tables uploaded to the db.")
    conn.close()
