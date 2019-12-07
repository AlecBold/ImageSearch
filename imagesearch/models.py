from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from django.conf import settings as dj_settings
import os


MEDIA_ROOT = dj_settings.MEDIA_ROOT

# @deconstructible
# class UploadToPathAndRename(object):
#     def __init__(self, path):
#         self.path = path
#
#     def __call__(self, instance, filename):  # Change name of file
#         filename = 'hotdog.jpg'
#         full_path = os.path.join(self.path, filename)
#         self.delete_file_if_exist(full_path)
#         return full_path
#
#     def delete_file_if_exist(self, full_path):
#         full_path = MEDIA_ROOT + os.sep + full_path
#         if os.path.isfile(full_path):
#             os.remove(full_path


class DataModel(models.Model):
    data_image = models.ImageField(upload_to='images/')


class UserModel(models.Model):
    user_image = models.ImageField(upload_to='user_images/')