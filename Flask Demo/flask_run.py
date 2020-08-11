import os
from flask import Flask, request, send_from_directory, render_template, url_for, redirect,jsonify
import json

app = Flask(__name__)

app.config['FILE_PATH'] = os.path.join(app.root_path, 'target')
app.config['JSON_AS_ASCII'] = False
app.config['DEBUG'] = True


# 将文件传送至target目录下
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    if request.method == 'POST':
        response = {}
        try:
            f = request.files['file']
            upload_path = os.path.join(app.config['FILE_PATH'], f.filename)
            f.save(upload_path)
        except Exception as e:
            response['status'] = 'failed'
            response['msg'] = str(e)
            return json.dumps(response)
        else:
            response['status'] = 'success'
            response['msg'] = f.filename
        return jsonify(response)


# 提供文件名下载文件
@app.route('/download', methods=['POST', 'GET'])
def download():
    if request.method == 'GET':
        return render_template('download.html')

    if request.method == 'POST':
        response = {}
        try:
            filename = request.form.get('filename')
            if not os.path.isfile(os.path.join(app.config['FILE_PATH'], filename)):
                response['status'] = 'failed'
                response['msg'] = 'No such file'
                return json.dumps(response)
            return send_from_directory(app.config['FILE_PATH'], filename=filename, as_attachment=True)
        except Exception as e:
            response['status'] = 'failed'
            response['msg'] = str(e)
            return json.dumps(response)


if __name__ == '__main__':
    app.run()
