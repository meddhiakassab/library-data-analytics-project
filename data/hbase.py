import happybase
import csv
import logging

# #### check for a table
# hbase shell
# list
# scan 'UsersX'

# ##### remove a table
# hbase shell
# disable 'UsersX'
# drop 'UsersX'

csv_file = 'users.csv'
table_name = 'UsersXX'
headers = ["User-ID","Location","Age"]


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


try:
    connection = happybase.Connection('0.0.0.0', port=9090)
    logging.info(f'connexion à HBase à 0.0.0.0:9090/ OK')
    
    connection.create_table(table_name, {'cf1': {}})
    logging.info(f'table "{table_name}" créé')
    
    table = connection.table(table_name)
except Exception as e:
    logging.error(f'erreur')
    exit(1)

logging.info(f'Début/ csv : {csv_file}')

try:
    with open(csv_file, 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            table.put(
                row['User-ID'],
                {f'cf1:{header}': row[header] for header in headers if header != 'User-ID'}
            )
            logging.info(f"nouveau data/ user-id : {row['User-ID']}")
except Exception as e:
    logging.error(f"erreur lors creation nouveau table : {e}")
    exit(1)

connection.close()
logging.info('terminé')