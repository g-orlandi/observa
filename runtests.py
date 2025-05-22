import os

command = 'python manage.py test frontend --settings main.settings.test_settings --verbosity 2'

os.system(command)