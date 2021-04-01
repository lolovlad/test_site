from Class.Application import Application as app
from Models.User import User
from flask import redirect, render_template
from Class.Interfase.IController import IController


class MyProfileController(IController):
    def __init__(self, view=None, model=None):
        self.__view = view
        self.__model = model

    def __call__(self, *args, **kwargs):
        return render_template('profile.html', title='Профиль', form=self.__model)
