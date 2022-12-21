import functools
import inspect
import sys
import traceback
from flask import (
    current_app,
    session,
    url_for,
    redirect,
    request,
)


def exception_handler(error_response):
    def factory_exception(func):
        @functools.wraps(func)
        def inner_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print("-" * 60)
                print(f"CALLER: {inspect.stack()[1][2]}-{inspect.stack()[1][3]}()")
                print(e.__class__.__name__)
                traceback.print_exc()
                print("-" * 60)
                if e.__class__.__name__ in [
                    "ValueError",
                    "AssertionError",
                    "KeyError",
                    "TypeError",
                ]:
                    print(str(e))
                return error_response

        return inner_function

    return factory_exception


def wrap_response(func):
    @functools.wraps(func)
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as err:
            print(type(err), file=sys.stderr)
            print(str(err), file=sys.stderr)
            print(err.__class__.__name__, file=sys.stderr)
            traceback.print_exc()
            print("-" * 60)

    return inner_function


def login_required(f):
    @wraps(f)
    def decorated(message):

        try:
            data = jwt.decode(message['token'], globals.current_app.config['SECRET_KEY'])
            try:
                user = User.query.filter_by(id=data['id']).first()
                Globals.current_user = UserSchema().dump(user).data
            except Exception as e:
                return Error.api_response(Error.USER_NOT_FOUND)
        except Exception as e:

            return Error.api_response(Error.INVALID_TOKEN)
        return f(message)

    return decorated