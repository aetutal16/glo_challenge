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
    data = BytesIO(b"col1,col2\nvalue1,value2\nvalue3,value4")
    data.name = 'test_file.csv'

    rv = client.post('/upload_csv/test_departments', 
                     data={'file': (data, 'test_file.csv')},
                     content_type='multipart/form-data')

    assert rv.status_code == 201
    assert b"Data inserted correctly" in rv.data

# Check if the file was already uploaded
def test_upload_duplicate_csv(client):
    data = BytesIO(b"col1,col2\nvalue1,value2\nvalue3,value4")
    data.name = 'test_file.csv'

    client.post('/upload_csv/test_departments', 
                data={'file': (data, 'test_file.csv')},
                content_type='multipart/form-data')

    # Upload the same file again
    rv = client.post('/upload_csv/test_departments', 
                     data={'file': (data, 'test_file.csv')},
                     content_type='multipart/form-data')

    assert rv.status_code == 400
    assert b"The file has already been uploaded before" in rv.data