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


connection = create_connection("localhost", "root", "12345678Ho", "dmc")



cursor = connection.cursor(dictionary=True)


def get_records(start,finish):
    query = "select * from records LIMIT "+str(start)+","+str(finish)
    cursor.execute(query)
    data = cursor.fetchall()
    return data
    # for each in data:
        # print(each)

#get_records(0,1)