import os 
import pandas as pd
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
   filename="logs/ingestion_db.log",
   level=logging.DEBUG,
   format='%(asctime)s %(levelname)s %(message)s',
   filemode="a"
)

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df,table_name,engine):
   '''this function will ingest df into database table '''
   try:
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        logging.info(f'✅ Ingested table: {table_name}')
   except Exception as e:
        logging.error(f'Failed to ingest table: {table_name} | Error: {e}')
        # For SQLite, rollback is automatic, but log it just in case
        engine.dispose()

def load_raw_data():
    '''this function wil load csvs as df n ingest into db'''
    start=time.time()
    for file in os.listdir('data'):
       if '.csv' in file:
          df=pd.read_csv('data/'+file)
          logging.info(f'Ingesting {file} in db')
          ingest_db(df,file[:-4],engine)
    end=time.time()
    total_time=(end - start)/60
    logging.info('-----------Ingestion complete-----------')
    logging.info(f'\nTotal time taken:{total_time} minutes')

if __name__=='__main__':
   load_raw_data()

  

