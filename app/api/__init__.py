import datetime

from flask import Blueprint
from flask_cors import CORS
from .. model import User

api = Blueprint('api', __name__)


@api.after_app_request
def refresh_expiring_token(response):
    try:
        exp_timestamp = get_jwt()['exp']
        print(datetime.datetime.fromtimestamp(exp_timestamp))
        now = datetime.datetime.now()
        target_timestamp = datetime.datetime.timestamp(now + datetime.timedelta(minutes=3))
        print('token checking')
        print(datetime.datetime.fromtimestamp(target_timestamp))
        if target_timestamp > exp_timestamp:
            user = User.query.get(get_jwt_identity())
            access_token = create_access_token(identity=user.id, additional_claims={
                'permissions': user.role.permissions,
                'role': user.role.name,
            })
            set_access_cookies(response, access_token)
            print('token refreshed')
        return response
    except (RuntimeError, KeyError) as e:
        print(e)
        return response


from . view import *
