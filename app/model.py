from . import sa
from sqlalchemy import Integer, Column, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT


permissions_config = [
    'create_post',
    'read_post',
]


class Role(sa.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    permissions = Column(LONGTEXT)
    default = Column(Boolean)

    users = relationship('User', back_populates='role')

    @staticmethod
    def refresh_roles():
        role_permissions = {
            'admin': (':'.join(permissions_config), True),
            'user': (permissions_config[1], False),
        }

        for role_name, permissions in role_permissions.items():
            role = sa.session.query(Role).filter(Role.name == role_name).first()
            if not role:
                sa.session.add(
                    Role(
                        name=role_name,
                        permissions=permissions[0],
                        default=permissions[1]
                    )
                )
            else:
                role.permissions = permissions[0]
                role.default = permissions[1]
                sa.session.add(role)

        sa.session.commit()


class User(sa.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30))

    role_id = Column(ForeignKey('roles.id'))

    role = relationship('Role', back_populates='users', lazy='joined')
    posts = relationship('Post', back_populates='author', lazy='dynamic')


class Post(sa.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(100))
    body = Column(LONGTEXT)

    author_id = Column(ForeignKey('users.id'))

    author = relationship('User', back_populates='posts', lazy='joined')
