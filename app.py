from flask import Flask, render_template, request, send_from_directory, session, Response, redirect, url_for
from flask_socketio import SocketIO
import pickle

from weed_model import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///karet.db'

socketio = SocketIO(app)

class Project():
    def __init__(self):
        self.image_url = ''
        self.gulma_url = ''
        self.karet_url = ''
        self.label_gulma_url = ''
        self.label_karet_url = ''
        self.data_occurance = set()

    def __str__(self):
        return f"Project(image_url={self.image_url}, gulma_url={self.gulma_url}, karet_url={self.karet_url}, " \
               f"label_gulma_url={self.label_gulma_url}, label_karet_url={self.label_karet_url}, " \
               f"data_occurance={self.data_occurance})"

def display_image(filename, label=None):
    from PIL import Image
    import io
    import base64

    if(filename.split('.')[1] == 'tif'):
        tiff_image = Image.open('./static/temp/' + filename)
        tiff_image = tiff_image.convert('RGBA')

        if(label):
            pixel_array = np.array(tiff_image)
            condition = np.all(pixel_array != [0,0,0,0], axis=2)
            if(label == 'gulma'): pixel_array[condition] = [255,0,0,255]
            if(label == 'karet'): pixel_array[condition] = [0,0,255,255]
            tiff_image = Image.fromarray(pixel_array)

        data = io.BytesIO()
        tiff_image.save(data, 'PNG')

        encode_image = base64.b64encode(data.getvalue())
        decode_image = encode_image.decode('utf-8')

        image_url = f'data:image/png;base64,{decode_image}'

    return image_url

@app.route('/clear_session', methods=['GET'])
def clear_session():
    session.pop('project', None)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    socketio.emit('update progress', 0)

    if 'project' not in session:
        session['project'] = pickle.dumps(Project())

    project = pickle.loads(session['project'])

    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        socketio.emit('update progress', 30)

        file.save('./static/temp/' + filename)
        project.image_url = filename
        session['project'] = pickle.dumps(project)
        socketio.emit('update progress', 60)

        image_url = display_image(project.image_url)
        socketio.emit('update progress', 100)
            
        return render_template('index.html', image_url=image_url)
    else:
        return render_template('index.html')

@app.route('/occurance', methods=['GET', 'POST'])
def occurance():
    if request.method == 'POST':

        serialized_project = session.get('project')
        project = pickle.loads(serialized_project)

        file = request.form['occurance'].split(', ')
        project.data_occurance.add(tuple(file))
        session['project'] = pickle.dumps(project)

        if(project.gulma_url == ''):
            image_url = display_image(project.image_url)

            return render_template('index.html', image_url=image_url, data=project.data_occurance)
        else:
            image_url = display_image(project.image_url)

            gulma_url = display_image(project.gulma_url)
            socketio.emit('update progress', 40)

            karet_url = display_image(project.karet_url)
            socketio.emit('update progress', 60)

            label_gulma_url = display_image(project.label_gulma_url, 'gulma')
            socketio.emit('update progress', 80)

            label_karet_url = display_image(project.label_karet_url, 'karet')
            socketio.emit('update progress', 100)

            return render_template('index.html', image_url=image_url, gulma_url=gulma_url, karet_url=karet_url, label_gulma_url=label_gulma_url, label_karet_url=label_karet_url, data=project.data_occurance)

@app.route('/segmentasi')
def segmentasi():
    socketio.emit('update progress', 0)

    serialized_project = session.get('project')
    project = pickle.loads(serialized_project)
    
    # img_path = './static/temp/' + filename

    # output_gulma_path = "./static/temp/gulma_rgb.tif"
    # output_non_gulma_path = "./static/temp/non_gulma_rgb.tif"

    # output_gulma_label_path = "./static/temp/gulma_label.tif"
    # output_non_gulma_label_path = "./static/temp/non_gulma_label.tif"

    # patch_size = 128
    # large_image, canvas, segmented_image = process_image_segmentation(img_path, patch_size)

    # label, label_output, label_gulma, label_non_gulma = combine_patches(large_image, canvas, segmented_image, patch_size)

    # gulma, non_gulma = segment_image(large_image, label_gulma, label_non_gulma)

    # # save_rgb(img_path, gulma, non_gulma, output_gulma_path, output_non_gulma_path)
    # cv2.imwrite(output_gulma_path, gulma)
    # cv2.imwrite(output_non_gulma_path, non_gulma)
    # save_label(label_gulma, label_non_gulma, output_gulma_label_path, output_non_gulma_label_path)
    
    image_url = display_image(project.image_url)
    socketio.emit('update progress', 20)

    gulma_url = display_image('gulma_rgb.tif')
    project.gulma_url = 'gulma_rgb.tif'
    socketio.emit('update progress', 40)

    karet_url = display_image('non_gulma_rgb.tif')
    project.karet_url = 'non_gulma_rgb.tif'
    socketio.emit('update progress', 60)

    label_gulma_url = display_image('gulma_rgb.tif', 'gulma')
    project.label_gulma_url = 'gulma_rgb.tif'
    socketio.emit('update progress', 80)

    label_karet_url = display_image('non_gulma_rgb.tif', 'karet')
    project.label_karet_url = 'non_gulma_rgb.tif'
    socketio.emit('update progress', 100)

    session['project'] = pickle.dumps(project)
            
    return render_template('index.html', image_url=image_url, gulma_url=gulma_url, karet_url=karet_url, label_gulma_url=label_gulma_url, label_karet_url=label_karet_url, data=project.data_occurance)

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory('./static/temp/', filename)

if __name__ == '__main__':
    socketio.run(app, port=3000, debug=True)