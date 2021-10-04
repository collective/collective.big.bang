from collective.big.bang.big import bang


def main(app):
    users = app.acl_users.users
    password_hash = users._user_passwords.get('admin')
    bang(None)
    new_password_hash = users._user_passwords.get('admin')

    if password_hash != new_password_hash:
        raise ValueError('Password was updated')

main(app)
