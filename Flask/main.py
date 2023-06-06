from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Content_file'

# Vérifier si le dossier d'upload existe, sinon le créer
if not os.path.exists('Content_file'):
    os.makedirs('Content_file')


@app.route('/')
def index():
    # Obtenir la liste des fichiers dans le dossier d'upload
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index'))


app.run(host='0.0.0.0')