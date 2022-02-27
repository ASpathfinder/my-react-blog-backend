from manage import app
from app.model import sa, Role, User, Post
import click


@app.cli.command('refresh-roles')
def refresh_roles():
    Role.refresh_roles()
    print('roles refreshed')


@app.cli.command('init')
def init():
    admin_role = sa.session.query(Role).filter(Role.name == 'admin').first()
    if not admin_role:
        print('no admin role exists')
        return

    admin_user = sa.session.query(User).filter(User.role_id == admin_role.id).first()

    if admin_user:
        print('there can be only one admin user')
        return

    admin_user = User(
        username='administrator',
        role_id=admin_role.id
    )

    sa.session.add(admin_user)
    sa.session.commit()


@app.cli.command('generate-posts')
@click.option('-n', default=0, help='amount you want')
def generate_posts(n):
    admin_id = sa.session.query(User.id).join(Role).filter(Role.name == 'admin').scalar()
    for i in range(n):
        sa.session.add(Post(title='#{} Post Title'.format(i+1), body='This is a post body', author_id=admin_id))

    sa.session.commit()

    print('{} posts generated'.format(n))
