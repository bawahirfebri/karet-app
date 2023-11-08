import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from tensorflow.keras.models import load_model
from osgeo import gdal


def prediction(model, image, patch_size=128):

    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    X_test = []
    patch_num = 1

    for i in range(0, image.shape[0], patch_size):
        for j in range(0, image.shape[1], patch_size):
            single_patch = image[i:i+patch_size, j:j+patch_size]
            X_test.append(single_patch)
            patch_num += 1

    X_test = np.array(X_test)
    print(X_test.shape)
    preds_test = model.predict(X_test, verbose=1)
    preds_test_t = (preds_test > 0.5).astype(np.uint8)

    return preds_test_t


def process_image_segmentation(img_path, image, patch_size=128):

    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

    resize_image = ((image.shape[0]//patch_size)*patch_size,
                    (image.shape[1]//patch_size)*patch_size)
    canvas_shape = (resize_image[0]+patch_size, resize_image[1]+patch_size)

    canvas = np.zeros((canvas_shape[0], canvas_shape[1], 4), dtype=np.uint8)
    canvas[:image.shape[0], :image.shape[1], :] = image

    print(image.shape, resize_image, canvas_shape, canvas.shape)

    model = load_model("./assets/ml/model_unet_v2.h5")
    segmented_image = prediction(model, canvas, patch_size=128)

    return image, canvas, segmented_image


def combine_patches(large_image, canvas, segmented_image, patch_size):
    segmented_image = segmented_image.reshape(
        (canvas.shape[0]//patch_size), (canvas.shape[1]//patch_size), patch_size, patch_size, 1)
    label = np.zeros((canvas.shape[0], canvas.shape[1], 1), dtype=np.uint8)

    for i in range((canvas.shape[0]//patch_size)):
        for j in range((canvas.shape[1]//patch_size)):
            label[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)
                  * patch_size, :] = segmented_image[i][j]

    label_output = label[:large_image.shape[0],
                         :large_image.shape[1], :].copy()

    label_gulma = label_output.copy()
    label_non_gulma = cv2.bitwise_not(label_output)-254

    print(large_image.shape, label_output.shape, canvas.shape, label.shape)
    print(np.unique(label_output), np.unique(label_output.copy()),
          np.unique(cv2.bitwise_not(label_output)))

    return label, label_output, label_gulma, label_non_gulma


def segment_image(large_image, label_gulma, label_non_gulma):
    gulma = cv2.bitwise_and(large_image, large_image, mask=label_gulma)
    non_gulma = cv2.bitwise_and(large_image, large_image, mask=label_non_gulma)

    if large_image.dtype == np.float32:
        gulma = np.where(gulma == 0., np.nan, gulma)
        non_gulma = np.where(non_gulma == 0., np.nan, non_gulma)

    return gulma, non_gulma


def save_rgb(img_path, output_gulma, output_non_gulma, output_gulma_path, output_non_gulma_path):
    height, width, num_channels = output_gulma.shape

    dataset = gdal.Open(img_path)
    projection = dataset.GetProjection()
    geo_transform = dataset.GetGeoTransform()

    driver = gdal.GetDriverByName("GTiff")

    output_gulma_dataset = driver.Create(
        output_gulma_path, width, height, num_channels, gdal.GDT_Byte)
    output_non_gulma_dataset = driver.Create(
        output_non_gulma_path, width, height, num_channels, gdal.GDT_Byte)

    for band in range(num_channels):
        output_gulma_band = output_gulma_dataset.GetRasterBand(band + 1)
        output_gulma_band.WriteArray(output_gulma[:, :, band])

        output_non_gulma_band = output_non_gulma_dataset.GetRasterBand(
            band + 1)
        output_non_gulma_band.WriteArray(output_non_gulma[:, :, band])

    output_gulma_dataset.GetRasterBand(
        1).SetColorInterpretation(gdal.GCI_RedBand)
    output_gulma_dataset.GetRasterBand(
        2).SetColorInterpretation(gdal.GCI_GreenBand)
    output_gulma_dataset.GetRasterBand(
        3).SetColorInterpretation(gdal.GCI_BlueBand)
    output_gulma_dataset.GetRasterBand(
        4).SetColorInterpretation(gdal.GCI_AlphaBand)

    output_non_gulma_dataset.GetRasterBand(
        1).SetColorInterpretation(gdal.GCI_RedBand)
    output_non_gulma_dataset.GetRasterBand(
        2).SetColorInterpretation(gdal.GCI_GreenBand)
    output_non_gulma_dataset.GetRasterBand(
        3).SetColorInterpretation(gdal.GCI_BlueBand)
    output_non_gulma_dataset.GetRasterBand(
        4).SetColorInterpretation(gdal.GCI_AlphaBand)

    output_gulma_dataset.SetProjection(projection)
    output_gulma_dataset.SetGeoTransform(geo_transform)

    output_non_gulma_dataset.SetProjection(projection)
    output_non_gulma_dataset.SetGeoTransform(geo_transform)

    dataset = None
    output_gulma_dataset = None
    output_non_gulma_dataset = None


def save_label(label_gulma, label_non_gulma, output_gulma_label_path, output_non_gulma_label_path):
    cv2.imwrite(output_gulma_label_path, label_gulma*255)
    cv2.imwrite(output_non_gulma_label_path, label_non_gulma*255)
