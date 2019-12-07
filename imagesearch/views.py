from django.shortcuts import render, redirect
from .forms import *
from .model.get_files import *
from .model.model_predict import *


def home(request):

    if request.method == 'POST':
        print(request.FILES)
        print(request.POST)
        form = UserForm(request.POST, request.FILES)
        print(request.FILES)
        print(request.POST)
        form.save()
        return redirect('preprocessed')
    else:
        form = UserForm()

    return render(request, 'imagesearch/home.html', {'form': form})


def preprocessed(request):

    if request.method == "GET":
        names_of_images = get_name_of_images()
        print(names_of_images)
        input_file_name = get_name_user_image()
        model = PredictModel()
        names_of_similar_images, dist = zip(*model.search_nearest(arr_data_names=names_of_images, user_file_name=input_file_name))

        url_images = get_url_images(names_of_similar_images)
        input_image = UserModel.objects.last()
        print(input_image)
        print(url_images)
        return render(request, 'imagesearch/processed.html', {'url_images': url_images, 'input_image': input_image})


