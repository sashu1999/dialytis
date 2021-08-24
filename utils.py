from itertools import groupby
import cv2
import keras
import numpy as np


def get_values(image):
    'resizing to 28 height pixels'
    w = image.size[0]
    h = image.size[1]
    r = w / h  # aspect ratio
    new_w = int(r * 28)
    new_h = 28
    new_image = image.resize((new_w, new_h))

    'converting to a numpy array'
    new_image_arr = np.array(new_image)

    'inverting the image to make background = 0'
    new_inv_image_arr = 255 - new_image_arr

    'rescaling the image'
    final_image_arr = new_inv_image_arr / 255.0

    'splitting image array into individual element arrays using non zero columns'
    m = final_image_arr.any(0)
    out = [final_image_arr[:, [*g]] for k, g in groupby(np.arange(len(m)), lambda x: m[x] != 0) if k]

    '''
    iterating through the element arrays to resize them to match input 
    criteria of the model = [mini_batch_size, height, width, channels]
    '''
    num_of_elements = len(out)
    elements_list = []
    for x in range(0, num_of_elements):
        img = out[x]

        # adding 0 value columns as fillers
        width = img.shape[1]
        filler = (final_image_arr.shape[0] - width) / 2

        if filler.is_integer() == False:  # odd number of filler columns
            filler_l = int(filler)
            filler_r = int(filler) + 1
        else:  # even number of filler columns
            filler_l = int(filler)
            filler_r = int(filler)

        arr_l = np.zeros((final_image_arr.shape[0], filler_l))  # left fillers
        arr_r = np.zeros((final_image_arr.shape[0], filler_r))  # right fillers

        # concatinating the left and right fillers
        help_ = np.concatenate((arr_l, img), axis=1)
        element_arr = np.concatenate((help_, arr_r), axis=1)

        element_arr.resize(28, 28, 1)  # resize array 2d to 3d
        # storing all elements in a list
        elements_list.append(element_arr)
    elements_array = np.array(elements_list)
    'reshaping to fit model input criteria'
    elements_array = elements_array.reshape(-1, 28, 28, 1)
    'predicting using the created model'
    model = keras.models.load_model("model.h5")
    elements_pred = model.predict(elements_array)
    elements_pred = np.argmax(elements_pred, axis=1)
    return elements_pred


def save_image(image):
    cv2.imwrite("temp.jpg", image)