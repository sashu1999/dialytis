from itertools import groupby
import cv2
import keras
import numpy as np


def get_values(image):
    w = image.size[0]
    h = image.size[1]
    r = w / h
    new_w = int(r * 28)
    new_h = 28
    new_image = image.resize((new_w, new_h))
    new_image_arr = np.array(new_image)
    new_inv_image_arr = 255 - new_image_arr
    final_image_arr = new_inv_image_arr / 255.0
    m = final_image_arr.any(0)
    out = [final_image_arr[:, [*g]] for k, g in groupby(np.arange(len(m)), lambda x: m[x] != 0) if k]
    num_of_elements = len(out)
    elements_list = []
    for x in range(0, num_of_elements):
        img = out[x]
        width = img.shape[1]
        filler = (final_image_arr.shape[0] - width) / 2
        if filler.is_integer() == False:
            filler_l = int(filler)
            filler_r = int(filler) + 1
        else:
            filler_l = int(filler)
            filler_r = int(filler)

        arr_l = np.zeros((final_image_arr.shape[0], filler_l))
        arr_r = np.zeros((final_image_arr.shape[0], filler_r))
        help_ = np.concatenate((arr_l, img), axis=1)
        element_arr = np.concatenate((help_, arr_r), axis=1)

        element_arr.resize(28, 28, 1)
        elements_list.append(element_arr)
    elements_array = np.array(elements_list)
    elements_array = elements_array.reshape(-1, 28, 28, 1)
    model = keras.models.load_model("model.h5")
    elements_pred = model.predict(elements_array)
    elements_pred = np.argmax(elements_pred, axis=1)
    return elements_pred


def save_image(image):
    cv2.imwrite("temp.jpg", image)