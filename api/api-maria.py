#!/uosr/bin/python3
from flask import Flask, request, json
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


app = Flask(__name__)

@app.route('/get_pessoa', methods=['GET'])
def get_nome():
    request_data = request.get_json()
    nome = request_data['nome']
    indexado = request_data['indexado']

    if indexado:
        select_query = "SELECT * FROM PessoaIndexada WHERE nome = \'"+nome+"\'"
    else:
        select_query = "SELECT * FROM PessoaNaoIndexada WHERE nome = \'"+nome+"\'"

    return run_select_query(select_query)


@app.route('/add_pessoa', methods=['POST'])
def add_people_count():
    print('Request' + str(request.data))
    request_data = request.get_json()
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
        if id is not None:
            res += 'Record with id('+str(id)+') inserted successfully into '+table_name+' table'
        else: 
            res += str(cursor.rowcount) + ' Record inserted successfully into '+table_name+' table'
        print(res)
        cursor.close()
    except mysql.connector.Error as error:
        res += "Failed to insert record into table {}".format(error)
        print(res)
    finally:
        if connection.is_connected():
            connection.close()
    return (res,id)

def run_select_query(query):
    connection = get_database_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        for x in res:
            print(x)
        print(res)
        cursor.close()
    except mysql.connector.Error as error:
        res = "Failed to select from table {}".format(error)
        print(res)
    finally:
        if connection.is_connected():
            connection.close()
    return json.dumps(res)
