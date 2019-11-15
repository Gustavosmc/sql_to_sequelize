from flask import Flask, render_template, request
from sql_to_json import get_tables, command_generate
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        f = request.files['file']
        ret = "Arquivo Inválido!"
        if str(f.filename).find('.sql') > -1:
            f.save('files/'+f.filename)
            tables = get_tables('files/{}'.format(f.filename))
            ret = command_generate(tables)
        return render_template("index.html", commands=ret)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)