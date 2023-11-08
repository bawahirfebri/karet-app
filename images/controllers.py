from PIL import Image
import io
import base64
import numpy as np


def display_ortho_image(filename, label=None):
    if (filename.split('.')[1] == 'tif'):
        tiff_image = Image.open('./assets/ortho/' + filename)
        tiff_image = tiff_image.convert('RGBA')

        if (label):
            pixel_array = np.array(tiff_image)
            condition = np.all(pixel_array != [0, 0, 0, 0], axis=2)
            if (label == 'gulma'):
                pixel_array[condition] = [255, 0, 0, 255]
            if (label == 'karet'):
                pixel_array[condition] = [0, 0, 255, 255]
            tiff_image = Image.fromarray(pixel_array)

        data = io.BytesIO()
        tiff_image.save(data, 'PNG')

        encode_image = base64.b64encode(data.getvalue())
        decode_image = encode_image.decode('utf-8')

        image_url = f'data:image/png;base64,{decode_image}'

    return image_url


def display_result_image(filename, label=None):
    if (filename.split('.')[1] == 'tif'):
        tiff_image = Image.open('./assets/result/' + filename)
        tiff_image = tiff_image.convert('RGBA')

        if (label):
            pixel_array = np.array(tiff_image)
            condition = np.all(pixel_array != [0, 0, 0, 0], axis=2)
            if (label == 'gulma'):
                pixel_array[condition] = [255, 0, 0, 255]
            if (label == 'karet'):
                pixel_array[condition] = [0, 0, 255, 255]
            tiff_image = Image.fromarray(pixel_array)

        data = io.BytesIO()
        tiff_image.save(data, 'PNG')

        encode_image = base64.b64encode(data.getvalue())
        decode_image = encode_image.decode('utf-8')

        image_url = f'data:image/png;base64,{decode_image}'

    return image_url
