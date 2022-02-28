from . import api
from .. model import sa, User, Post
from flask import jsonify, request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, \
    get_jwt, set_access_cookies, unset_access_cookies, get_csrf_token, verify_jwt_in_request
import datetime


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
    page = request.args.get('page', 1, type=int)

    pagination = sa.session.query(Post).paginate(page=page, per_page=9)

    return jsonify(
        {
            'state': 'success',
            'data': {
                'posts': [
                    {
                        'id': post.id,
                        'title': post.title,
                        'description': post.description,
                        'author_id': post.author_id,
                    } for post in pagination.items
                ],
                'page': pagination.page,
                'pages': pagination.pages,
            }
        }
    )




