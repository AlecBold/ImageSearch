from os import listdir
from os.path import isfile, join, curdir
import numpy as np
import json
from django.conf import settings
from ..models import UserModel

path_user_images = f'{settings.MEDIA_ROOT}/user_images'
path_data_images = f'{settings.MEDIA_ROOT}/images'
path_model = f'{settings.BASE_DIR}/imagesearch/model/vgg19_weights_tf_dim_ordering_tf_kernels.h5'
path_to_json_file = f'{settings.BASE_DIR}/imagesearch/model/vectors_and_file_names.json'


def get_name_of_images():
    files = [file for file in listdir(path_data_images) if isfile(join(path_data_images, file))]
    return files


def get_name_user_image():
    file = UserModel.objects.last().user_image.name.split('/')[1]
    return file


def get_url_images(file_names):
    url_images = []
    path = '/media/images'
    for name in file_names:
        url_images.append(join(path, name))
    return url_images


def jsonify(vector):
    return vector.tolist()


def unjsonify(vector):
    return np.array(vector, np.float32)


def make_json_file(names, vectors):
    names_and_vectors = {}
    for i in range(len(vectors)):
        names_and_vectors[names[i]] = jsonify(vectors[i])
    with open(path_to_json_file, 'w') as file:
        json.dump(names_and_vectors, file)


def get_predicted_vectors():
    with open(path_to_json_file) as file:
        names, vectors = zip(*json.load(file).items())
        vectors = [unjsonify(vector) for vector in vectors]
        return names, vectors


def json_file_exist():
    try:
        with open(path_to_json_file) as file:
            return True
    except FileNotFoundError:
        return False
