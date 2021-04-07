from flask import jsonify


class UploadMusicModel:
    def __init__(self, json):
        self.__name = self.lable("name")
        self.__img = self.file("img")
        self.__tag = self.lable("tag")
        self.__music = self.file("music")
        self.__json = json


    def lable(self, name):
        return None


    def file(self, name):
        return None
