from keras.applications.vgg19 import preprocess_input
from keras.preprocessing import image
from keras.engine import Model
from keras import backend as K
from .get_files import *


class PredictModel:

    def vgg19_init(self):
        from keras.applications import VGG19
        bm = VGG19(weights='imagenet')
        self.model = Model(inputs=bm.input, outputs=bm.get_layer('fc1').output)

    def knn_init(self):
        from sklearn.neighbors import NearestNeighbors
        self.knn = NearestNeighbors(metric='cosine', algorithm='brute')

    def prep_one_file(self, name_file, user):
        path = join(path_data_images, name_file)
        if user:
            path = join(path_user_images, name_file)
        img = image.load_img(path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        vector = self.model.predict(x).ravel()
        print(f'File {name_file} convert to vector')
        return vector

    def prep_many_files(self, arr_data_names, user):
        vectors = []
        for file in arr_data_names:
            vectors.append(self.prep_one_file(file, user))
        return vectors

    def get_files_names_and_vectors(self, arr_data_names, user):
        if json_file_exist():
            return get_predicted_vectors()
        else:
            vectors = self.prep_many_files(arr_data_names, user)
            make_json_file(arr_data_names, vectors)
            return get_predicted_vectors()

    def search_nearest(self, arr_data_names, user_file_name):
        # Initialize models
        self.vgg19_init()
        self.knn_init()
        # Get vectors of images
        input_vector = self.prep_one_file(user_file_name, user=True)
        files_names, vectors = self.get_files_names_and_vectors(arr_data_names, user=False)
        # Reshape input vector
        input_vector = np.array(input_vector, np.float32).reshape(1, -1)
        # Fitting model
        self.knn.fit(vectors)
        # Find similar images
        dist, indices = self.knn.kneighbors(input_vector, n_neighbors=10)
        names_similar_images = [(files_names[indices[0][i]], dist[0][i]) for i in range(len(indices[0]))]
        print(names_similar_images)
        print(dist)
        K.clear_session()
        return names_similar_images


