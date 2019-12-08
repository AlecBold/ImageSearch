from os import listdir
from os.path import isfile, join, curdir
import numpy as np
import json


path_user_images = f'{curdir}/media/user_images'
path_data_images = f'{curdir}/media/images'
path_to_json_file = f'{curdir}/json/vectors_and_file_names.json'


def get_names_of_images():
    files = [file for file in listdir(path_data_images) if isfile(join(path_data_images, file))]
    return files


def get_binary_user_file():
    # Binary file
    return 0


def get_url_images(file_names):
    url_images = [join(path_data_images, name) for name in file_names]
    return url_images


def jsonify(vector):
    return vector.tolist()


def unjsonify(vector):
    return np.array(vector, np.float32)


def json_file_exist():
    try:
        with open(path_to_json_file):
            return True
    except FileNotFoundError:
        return False

def make_json_file(names, vectors):
    names_and_vectors = {}
    for i in range(len(vectors)):
        names_and_vectors[names[i]] = jsonify(vectors[i])
    with open(path_to_json_file, 'w') as file:
        json.dump(names_and_vectors, file)



def get_predicted_vectors_from_json():
    with open(path_to_json_file) as file:
        names, vectors = zip(*json.load(file).items())
        vectors = [unjsonify(vector) for vector in vectors]
        return names, vectors
      