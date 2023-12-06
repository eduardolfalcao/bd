#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from os import environ
import json

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

def add_people_count(request_data):
    #print('Add people count called!')
    #print('Request' + str(request_data))
    insert_query = """INSERT INTO PeopleCount (value, collector_id, timestamp) VALUES (%s, %s, %s)"""
    val = (request_data['value'],request_data['collector_id'],str(request_data['timestamp']))
    run_insert_query(insert_query, val, 'PeopleCount')   
    return run_insert_query(insert_query, val, 'PeopleCount')   

def add_people_recognized(request_data):
    name_ids = []
    print('Request data (json): '+str(request_data['value']))
    for name in request_data['value']:
        #print(name)          
        name_ids.append(add_people(name))

    recog_id = add_recognized(request_data)   
    res = []
    for name_id in name_ids:
        insert_query = """INSERT IGNORE INTO PeopleRecognized (id_recognized, id_people) VALUES (%s, %s)"""    
        val = (recog_id, name_id)        
        res.append(run_insert_query(insert_query, val, 'PeopleRecognized'))

    return json.dumps(res)

def add_people(name):
    insert_query = """INSERT IGNORE INTO People (name) VALUES (%s)"""    
    val = (name,)
    return run_insert_query(insert_query, val, 'People')[1]   #returns id

def add_recognized(request_data):
    insert_query = """INSERT INTO Recognized (collector_id, timestamp) VALUES (%s, %s)"""
    val = (request_data['collector_id'],str(request_data['timestamp']))
    return run_insert_query(insert_query, val, 'Recognized')[1]   #returns id
    
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
        #print(res)
        cursor.close()
    except mysql.connector.Error as error:
        res += "Failed to insert record into table {}".format(error)
        print(res)
    finally:
        if connection.is_connected():
            connection.close()
    return (res,id)

request_data_pc = dict()
request_data_pr = dict()

for i in range(10000):
    request_data_pc['value'] = i
    request_data_pc['collector_id'] = 'iot_dev_id_'+str(i)
    request_data_pc['timestamp'] = i
    add_people_count(request_data_pc)

    request_data_pr['value'] = ['andrey','eduardo','fabio']
    request_data_pr['collector_id'] = 'iot_dev_id_'+str(i)
    request_data_pr['timestamp'] = i
    add_people_recognized(request_data_pr)
    
    print("Entry "+str(i)+" inserted!")
