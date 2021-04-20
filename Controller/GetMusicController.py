from Class.Application import Application as app
from Models.Sound import Sound
from flask import jsonify, make_response, url_for
from Class.Interfase.IController import IController
from flask_login import current_user
from Class.MakeResponse import MakeResponse
import pickle


class GetMusicController(IController):
    def __call__(self, massed, *args, **kwargs):
        req = massed.get_json()
        sound = app().context.query(Sound).filter(Sound.id == req["id"]).first()
        sound = MakeResponse.make_response_sound(sound.__dict__)
        res = make_response(jsonify({"data": sound}), 200)
        return res
