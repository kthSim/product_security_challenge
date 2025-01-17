from project import app, db
from project.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555)
