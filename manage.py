import os, sys
from application import app
from application import create_app
from flask_script import Manager, Server
from flask_migrate import MigrateCommand

manager = Manager(app)
manager.add_command('db', MigrateCommand)


manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host=os.getenv('IP', '127.0.0.1'),
    port=int(os.getenv('PORT', 5000)))
)

if __name__ == "__main__":
    manager.run()