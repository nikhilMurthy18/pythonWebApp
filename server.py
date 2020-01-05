from flask import Flask, render_template, request, redirect
import datetime
import csv
from azure.storage.blob import BlobClient

app = Flask(__name__)

def getAzureBlob():  
    blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=nikhilstorage;AccountKey=kfJbTJbHj5DmTy9g9dP3FicAKET8UzHtx67vI9SM2l9KXm1tUP1HTSkq0mwpu1MfifQYuYi+rThxZ5fCGgo9DQ==;EndpointSuffix=core.windows.net", container_name="contactdata", blob_name="database.txt")
    with open("./database.txt", "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)
    
def uploadAzureBlob():
    blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=nikhilstorage;AccountKey=kfJbTJbHj5DmTy9g9dP3FicAKET8UzHtx67vI9SM2l9KXm1tUP1HTSkq0mwpu1MfifQYuYi+rThxZ5fCGgo9DQ==;EndpointSuffix=core.windows.net", container_name="contactdata", blob_name="database.txt")
    with open("./database.txt", "rb") as data:
        blob.delete_blob()
        blob.upload_blob(data)

@app.route('/')
def hello_world():
    getAzureBlob()
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    getAzureBlob()
    return render_template(page_name)   
    
@app.route('/<name>')
def hi(name):
    return render_template('index.html', name = name)

def write_to_file(data):
    with open('database.txt',mode='a') as database:
        database.write(f'\n{data["email"]}, {data["subject"]}, {data["message"]}, {datetime.datetime.now()}')    

def write_to_csv(data):
    with open('database2.csv',mode='a', newline='') as database2:
        csv_writer = csv.writer(database2,delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([data["email"],data["subject"],data["message"],datetime.datetime.now()])            

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    data = request.form.to_dict()
    write_to_file(data)
    write_to_csv(data)
    uploadAzureBlob()
    return redirect('thankyou.html')    