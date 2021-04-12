from Class.Application import Application as app
from Models.Sound import Sound
from flask import jsonify, make_response, url_for
from Class.Interfase.IController import IController
from flask_login import current_user
import pickle


class LoadMusicController(IController):
    def __call__(self, massed, *args, **kwargs):
        req = massed.get_json()
        sounds = app().context.query(Sound).all()[req["start"]:req["end"]]
        sounds = list(map(lambda x: self.__make_dict(x.__dict__), sounds))
        res = make_response(jsonify({"data": sounds}), 200)
        return res

    def __make_dict(self, mas):
        del mas['_sa_instance_state']
        for i in mas:
            if type(mas[i]) == bytes:
                mas[i] = len(pickle.loads(mas[i]))
        mas["created_date"] = mas["created_date"].strftime("%d/%m/%Y")
        mas["img"] = url_for("static", filename=mas["img"].replace('\\', "/"))
        mas["file_name"] = url_for("static", filename=mas["file_name"].replace('\\', "/"))
        return mas


