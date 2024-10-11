import pytest
from io import BytesIO
import csv
from api import app 

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test for the GET
def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    response_text = rv.data.decode("utf-8")  
    assert "Flask server is working" in response_text

# Test for the csv upload
def test_upload_csv(client):
    # csv file created to test
    data = BytesIO(b"50,col2\n51,value2\n53,value4")
    data.name = 'test_file.csv'

    rv = client.post('/upload_csv/dim_departments', 
                     data={'file': (data, 'test_file.csv')},
                     content_type='multipart/form-data')

    assert rv.status_code == 201
    assert b"Data inserted correctly!" in rv.data

# Test for the csv upload, table incorrect
def test_upload_csv_2(client):
    # csv file created to test
    data = BytesIO(b"1000,col2\n1001,value2\n1002,value4")
    data.name = 'test_file.csv'

    rv = client.post('/upload_csv/dim_depar', 
                     data={'file': (data, 'test_file.csv')},
                     content_type='multipart/form-data')

    assert rv.status_code == 400
    assert b"Invalid table" in rv.data

# Test for the csv upload, a file with the wrong structure for the table
def test_upload_csv_3(client):
    # csv file created to test
    data = BytesIO(b"1000,col2,col3\n1001,value2,value3\n1002,value4,value5")
    data.name = 'test_file.csv'

    rv = client.post('/upload_csv/dim_departments', 
                     data={'file': (data, 'test_file.csv')},
                     content_type='multipart/form-data')

    assert rv.status_code == 400
    assert b"The csv file should have 2 columns" in rv.data

# Check if the file was already uploaded
def test_upload_duplicate_csv(client):

    #Create the first instance for the file
    data1 = BytesIO(b"100,col2\n101,value2\n102,value4")
    data1.name = 'test_file.csv'

    client.post('/upload_csv/dim_departments', 
                data={'file': (data1, 'test_file.csv')},
                content_type='multipart/form-data')

    # Create a new instance of BytesIO for the second upload
    data2 = BytesIO(b"100,col2\n101,value2\n102,value4")
    data2.name = 'test_file.csv'

    # Upload the same file again
    rv = client.post('/upload_csv/dim_departments', 
                     data={'file': (data2, 'test_file.csv')},
                     content_type='multipart/form-data')

    assert rv.status_code == 400
    assert b"The file has already been uploaded before" in rv.data