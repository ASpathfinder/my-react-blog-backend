from . import api
from .. model import sa, User, Post
from flask import jsonify, request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, \
    get_jwt, set_access_cookies, unset_access_cookies, get_csrf_token
from flask_sqlalchemy import Pagination
import datetime


@api.after_request
def refresh_expiring_token(response):
    try:
        exp_timestamp = get_jwt()['exp']
        now = datetime.datetime.utcnow()
        target_timestamp = datetime.datetime.timestamp(now + datetime.timedelta(minutes=1))
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
        return response


@api.route('/authorize', methods=['POST'])
def authorize():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    user = sa.session.query(User).filter(User.username == username).first()

    if not user:
        return jsonify(
            {
                'state': 'failed',
                'message': "user doesn't exist"
            }
        )

    token = create_access_token(identity=user.id, additional_claims={
        'permissions': user.role.permissions,
        'role': user.role.name,
    })

    response = jsonify(
        {
            'state': 'success',
            'id': user.id,
            'permissions': user.role.permissions,
            'role': user.role.name,
        }
    )

    set_access_cookies(response, token)

    return response


@api.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({
        'state': 'success',
        'message': 'logged out'
    })
    unset_access_cookies(response)

    return response


@api.route('/get-post-items', methods=['GET'])
@jwt_required()
def get_posts():
    current_user_id = get_jwt_identity()

    posts = User.query.get(current_user_id).posts

    return jsonify(
        {
            'state': 'success',
            'posts': [{
                'id': post.id,
                'title': post.title,
                'body': post.body
            } for post in posts]
        }
    )




