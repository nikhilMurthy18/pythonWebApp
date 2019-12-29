from flask import Flask, render_template, request, redirect
import datetime
import csv

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
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
    return redirect('thankyou.html')    



#app.add_url_rule('/favicon.ico',
   #              redirect_to=url_for('static', filename='favicon.ico'))
