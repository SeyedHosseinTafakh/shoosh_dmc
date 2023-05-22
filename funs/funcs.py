from pydicom import dcmread
import pydicom
dc = dcmread("0002.dcm")
#print(dc.Dataset)
#
#def dicom_dataset_to_dict(dicom_header):
#    dicom_dict = {}
#    repr(dicom_header)
#    for dicom_value in dicom_header.values():
#        if dicom_value.tag == (0x7fe0, 0x0010):
#            # discard pixel data
#            continue
#        if type(dicom_value.value) == dicom.dataset.Dataset:
#            dicom_dict[dicom_value.tag] = dicom_dataset_to_dict(dicom_value.value)
#        else:
#            v = _convert_value(dicom_value.value)
#            dicom_dict[dicom_value.tag] = v
#    return dicom_dict
#
#
#def _sanitise_unicode(s):
#    return s.replace(u"\u0000", "").strip()
#
#
#def _convert_value(v):
#    t = type(v)
#    if t in (list, int, float):
#        cv = v
#    elif t == str:
#        cv = _sanitise_unicode(v)
#    elif t == bytes:
#        s = v.decode('ascii', 'replace')
#        cv = _sanitise_unicode(s)
#    elif t == dicom.valuerep.DSfloat:
#        cv = float(v)
#    elif t == dicom.valuerep.IS:
#        cv = int(v)
#    elif t == dicom.valuerep.PersonName3:
#        cv = str(v)
#    else:
#        cv = repr(v)
#    return cv
#
#dicom_dataset_to_dict(dc)

def dictify(ds: pydicom.dataset.Dataset) -> dict:
    """Turn a pydicom Dataset into a dict with keys derived from the Element names."""
    output = dict()
    for elem in ds:
        if elem.VR != "SQ":
            output[elem.name] = str(elem.value)
        else:
            output[elem.name] = [dictify(item) for item in elem]
    return output

#print(dictify(dc))



import mysql.connector

from mysql.connector import Error


def create_connection(host_name, user_name, user_password, database):

    connection = None

    try:

        connection = mysql.connector.connect(

            host=host_name,

            user=user_name,

            passwd=user_password,
            
            database=database

        )

        print("Connection to MySQL DB successful")

    except Error as e:

        print(f"The error '{e}' occurred")


    return connection


connection = create_connection("localhost", "root", "5260145143", "dmc")



cursor = connection.cursor(dictionary=True)


def get_records(start,finish):
    query = "select * from records ORDER BY created_at DESC LIMIT "+str(start)+","+str(finish)+" "
    cursor.execute(query)
    data = cursor.fetchall()
    return data
    # for each in data:
        # print(each)

#get_records(0,1)

def insert_record(p_name, p_phone_number, more_text, file_dir, user_id, created_atj):
    query = "insert into records (p_name, p_phone_number, more_text, file_dir, user_id, created_atj) values (%s, %s , %s, %s, %s, %s)"
    values = (p_name, p_phone_number, more_text, file_dir, user_id, created_atj)
    try:
        cursor.execute(query,values)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


# from datetime import datetime
# import jdatetime
# print(jdatetime.datetime.now())
# format = '%Y-%m-%d %H:%M:%S'

# recived_time = "2023-05-14 11:19:38"
# datetime_str = datetime.strptime(recived_time, format)
#Asia/Tehran
# print(datetime_str.astimezone(pytz.timezone("Asia/Tehran")))
# print(pytz.all_timezones)



def dblogin(username, password):
    query = "select * from users where name=%s and password=%s"
    values = (username, password)
    try:
        cursor.execute(query, values)
        data = cursor.fetchall()
        return data
    except Error as e:
        print(e)

def get_user_by_id(user_id):
    query = "select * from users where uid = %s "
    values = (user_id,)
    try:
        cursor.execute(query,values)
        data = cursor.fetchall()
        
        return data
    except Error as e:
        print(e)

# import urllib.parse
 
# def url_encoder(query):
    # print(urllib.parse.unquote(query))

# url_encoder("https%3A%2F%2Fraw.githubusercontent.com%2Fivmartel%2Fdwv%2Fmaster%2Ftests%2Fdata%2F%3Ffile%3Dbbmri-53323851.dcm%26file%3Dbbmri-53323707.dcm%26file%3Dbbmri-53323563.dcm%26file%3Dbbmri-53323419.dcm%26file%3Dbbmri-53323275.dcm%26file%3Dbbmri-53323131.dcm")

# from random import randrange
import random
import string
def random_char():
    letters =  ''.join(random.choice(string.ascii_lowercase) for x in range(3))
    numbers = random.randrange(1000,9999)
    x = [random.randrange(10) for p in range(0, 10)]
    return letters+str(numbers)
 
# print(random_char())

def get_code_by_phone_number(p_phone_number):
    query = "select * from  user_codes where p_phone_number = %s"
    values = (p_phone_number,)
    try:
        cursor.execute(query,values)
        data = cursor.fetchall()
        return data
    except Error as e:
        print(e)

def check_user_code_by_code(code):
    query = "select * from user_codes where p_access_code=%s"
    values = (code,)
    try:
        cursor.execute(query,values)
        data = cursor.fetchall()
        
        return data
    except Error as e:
        print(e)


def upload_code(p_phone_number):
    query = "INSERT INTO user_codes (p_phone_number, p_access_code) VALUES (%s ,%s)"
    values = (p_phone_number, random_char())
    try:
        cursor.execute(query, values)
        connection.commit()
    except Error as e:
        print(e)


def count_rows_record():
    query = "select count(*) as counts from records"
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Error as e:
        print(e)

# print(count_rows_record())

def search_in_records_phone_number(p_phone_number, start, finish):
    query = "select * from records where p_phone_number = %s limit " + str(start) + ", "+str(finish)

    values = (p_phone_number, )
    try:
        cursor.execute(query,values)
        data = cursor.fetchall()
        return data
    except Error as e:
        print(e)


def count_search_in_records_phone_number(p_phone_number):
    query = "select count(*) as counts from records where p_phone_number = %s"
    values = (p_phone_number, )
    try:
        cursor.execute(query,values)
        data = cursor.fetchall()
        return data
    except Error as e:
        print(e)
def search_in_records_p_name(p_name, start, finish):
    query = "select * from records where p_name = %s limit " + str(start) + ", "+str(finish)

    values = (p_name, )
    try:
        cursor.execute(query,values)
        data = cursor.fetchall()
        return data
    except Error as e:
        print(e)

def count_search_in_records_p_name(p_name):
    query = "select count(*) as counts from records where p_name = %s"
    values = (p_name, )
    try:
        cursor.execute(query,values)
        data = cursor.fetchall()
        return data
    except Error as e:
        print(e)

# print(search_in_records_phone_number("09398709892", 0,10))
# print(search_in_records_phone_number("09398709892", 0,10))
# print(search_in_records_p_name("shandool", 0,10))

def search_in_code(code):
    query = "select * FROM user_codes where   p_access_code = %s"
    values = (code,)
    try:
        cursor.execute(query,values)
        data = cursor.fetchall()
        return data
    except Error as e:
        print(e)


# print(search_in_code("abc1020"))

# print(69%60)