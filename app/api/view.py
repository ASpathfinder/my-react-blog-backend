from . import api
from .. model import sa, User, Post
from flask import jsonify, request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import Pagination


@api.route('/authorize', methods=['POST'])
def authorize():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    user = sa.session.query(User).filter(User.username == username).first()

    if not user:
        return jsonify(
            {
                'status': 'failed',
                'message': "user doesn't exist"
            }
        )

    token = create_access_token(identity=user.id)

    return jsonify(
        {
            'token': token,
            'permissions': user.role.permissions,
            'role': user.role.name,
        }
    )


@api.route('/get-post-items', methods=['GET'])
@jwt_required()
def get_posts(page):
    page = int(page if page else 1)
    current_user_id = get_jwt_identity()

    pagination = Pagination(User.query.get(current_user_id).posts, page=page, per_page=11, items=None, total=None)

    #result = {
    #    'page': pagination.page,
    #    'total': pagination.total,
    #    'items':
    #}





