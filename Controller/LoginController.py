from forms.LoginForm import LoginForm
from Class.Application import Application as app
from Models.User import User
from flask import redirect, render_template


class LoginController:
    def __init__(self, view, model, login_user=None):
        self.__view = view
        self.__model = model
        self.__login_user = login_user

    def __call__(self, *args, **kwargs):
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = app.context
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                self.__login_user(user, remember=True)
                return redirect("/")
            return render_template('login.html', message="Неправильный логин или пароль", form=form)
        return render_template('login.html', title='Авторизация', form=form)