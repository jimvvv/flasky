# -*- coding: utf-8 -*-
import os
from app import create_app, DB
from app.models import User, Role
from flask_migrate import Migrate 

app = create_app(os.environ.get('FLAKS_CONFIG', 'default'))
migrate = Migrate(app, DB)

@app.shell_context_processor
def make_shell_context():
    return dict(db=DB, User=User, Role=Role)

@app.cli.command()
def test():
    '''Run the unit tests.'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)