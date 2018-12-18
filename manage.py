# encoding: utf-8
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import config
from application import create_app
# 创建app
app = create_app()
# 创建绑定migrate
migrate = Migrate(app, config.db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
