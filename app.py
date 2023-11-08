from flask_socketio import SocketIO
from flask import request, make_response, jsonify, render_template, session, send_from_directory
from asyncio import sleep
import os
import cv2

from . import create_app
from .images.controllers import *
from .points.controllers import *
from .assets.weed_model import *

# App Initialization
app = create_app(os.getenv("CONFIG_MODE"))
app.config['SECRET_KEY'] = 'secret_key'

socketio = SocketIO(app)


@app.route('/points', methods=['POST', 'GET'])
def points():
    if request.method == 'GET':
        return retrievePoints()
    elif request.method == 'POST':
        return createPoint()
    else:
        return make_response(jsonify({'message': 'Method not allowed'}, 500))


@app.route('/point/<point_id>', methods=['GET', 'PUT', 'DELETE'])
def point(point_id):
    if request.method == 'GET':
        return retrievePoint(point_id)
    elif request.method == 'PUT':
        return updatePoint(point_id)
    elif request.method == 'DELETE':
        return deletePoint(point_id)
    else:
        return make_response(jsonify({'message': 'Method not allowed'}, 500))


@app.route('/progress')
async def progress():
    for x in [25, 50, 75, 100]:
        socketio.emit('update progress', x)
        await sleep(2)

    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    socketio.emit('update progress', 0)

    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        socketio.emit('update progress', 30)

        file.save('./assets/ortho/' + filename)
        session['filename'] = filename
        socketio.emit('update progress', 60)

        image_url = display_ortho_image(filename)
        socketio.emit('update progress', 100)

        return render_template('index.html', image_url=image_url)
    elif request.method == 'GET':
        return render_template('index.html')
    else:
        return make_response(jsonify({'message': 'Method not allowed'}), 500)


@app.route('/severity')
def severity():
    return None


@app.route('/segmentasi')
def segmentasi():
    socketio.emit('update progress', 0)

    filename = session.get('filename', None)
    img_path = './assets/ortho/' + filename

    output_gulma_path = "./assets/result/gulma_rgb.tif"
    output_non_gulma_path = "./assets/result/non_gulma_rgb.tif"

    output_gulma_label_path = "./assets/result/gulma_label.tif"
    output_non_gulma_label_path = "./assets/result/non_gulma_label.tif"

    patch_size = 128
    large_image, canvas, segmented_image = process_image_segmentation(
        img_path, patch_size)

    label, label_output, label_gulma, label_non_gulma = combine_patches(
        large_image, canvas, segmented_image, patch_size)

    gulma, non_gulma = segment_image(
        large_image, label_gulma, label_non_gulma)

    save_rgb(img_path, gulma, non_gulma,
             output_gulma_path, output_non_gulma_path)
    cv2.imwrite(output_gulma_path, gulma)
    cv2.imwrite(output_non_gulma_path, non_gulma)
    save_label(label_gulma, label_non_gulma,
               output_gulma_label_path, output_non_gulma_label_path)

    image_url = display_ortho_image(filename)
    socketio.emit('update progress', 20)

    gulma_url = display_result_image('gulma_rgb.tif')
    socketio.emit('update progress', 40)

    karet_url = display_result_image('non_gulma_rgb.tif', 60)
    socketio.emit('update progress', 60)

    label_gulma_url = display_result_image('gulma_rgb.tif', 'gulma')
    socketio.emit('update progress', 80)

    label_karet_url = display_result_image('non_gulma_rgb.tif', 'karet')
    socketio.emit('update progress', 100)

    return render_template('index.html', image_url=image_url, gulma_url=gulma_url, karet_url=karet_url, label_gulma_url=label_gulma_url, label_karet_url=label_karet_url)


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory('./assets/ortho/', filename)


if __name__ == '__main__':
    socketio.run(app, port=3000, debug=True)
