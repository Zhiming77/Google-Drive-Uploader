import os
import json
import requests
from flask import Flask,render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key="banc"
app.config['UPLOAD_EXTENSIONS']=['.mp4','.mkv','.mov','.gif','.jpg','.png']

auth = {}
auth['folder_id']=os.environ.get('FOLDER_ID')
auth['access_token']=os.environ.get('ACCESS_TOKEN')


folder_id = str(auth['folder_id'])
print("folder id is: "+folder_id)
access_token = auth['access_token']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if uploaded_file.name != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)

        metadata = {
            "name": filename,
            "parents": [folder_id]

        }


        files = {
            'data':('metadata', json.dumps(metadata), 'application/json'),
            'file': uploaded_file
        }

        r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers={"Authorization": "Bearer " + access_token},
    files=files

        )

        print(r.text)


    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(threaded=True, port = 5000)
