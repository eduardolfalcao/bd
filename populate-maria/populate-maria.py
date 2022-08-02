
#!/uosr/bin/python3
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from os import environ

DB_HOST = environ.get('DB_HOST')
DB_NAME = environ.get('DB_NAME')
DB_USER = environ.get('DB_USER')
DB_PASSWORD = environ.get('DB_PASSWORD')
if DB_PASSWORD is not None:
    print('###################################')
    print('These are the environment variables: DB_HOST='+DB_HOST+', DB_NAME='+DB_NAME+', DB_USER='+DB_USER+', DB_PASSWORD='+DB_PASSWORD)
    print('###################################')
else:
    print('###################################')
    print('No environment variable appeared!')
    print('###################################')


def add_people(request_data):
    indexado = request_data['indexado']
    val = (request_data['nome'],str(request_data['idade']))

    if indexado:
        insert_query = """INSERT INTO PessoaIndexada (nome, idade) VALUES (%s, %s)"""
        return run_insert_query(insert_query, val, 'PessoaIndexada')   
    else:
        insert_query = """INSERT INTO PessoaNaoIndexada (nome, idade) VALUES (%s, %s)"""
        return run_insert_query(insert_query, val, 'PessoaNaoIndexada')   
    
def get_database_connection():
    return mysql.connector.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

def run_insert_query(query, values, table_name):
    connection = get_database_connection()
    res = ''
    id = None
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        id = cursor.lastrowid
        '''if id is not None:
            res += 'Record with id('+str(id)+') inserted successfully into '+table_name+' table'
        else: 
            res += str(cursor.rowcount) + ' Record inserted successfully into '+table_name+' table'
        print(res)'''
        cursor.close()
    except mysql.connector.Error as error:
        res += "Failed to insert record into table {}".format(error)
        print(res)
    finally:
        if connection.is_connected():
            connection.close()
    return (res,id)

request_data_pc = dict()

for i in range(157000,10000000):
    request_data_pc['idade'] = i
    request_data_pc['nome'] = 'pessoa'+str(i)
    request_data_pc['indexado'] = True
    add_people(request_data_pc)

    request_data_pc['indexado'] = False
    add_people(request_data_pc)
    
    if i%1000 == 0:
        print("Entry "+str(i)+" inserted!")
