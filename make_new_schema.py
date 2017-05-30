import os


msg_exist = 'exist: {}'
msg_ok = 'ok: {}'
dirs_list = [
    'app',
    'app/static',
    'app/static/img',
    'app/static/css',
    'app/static/js',
    'app/templates'
]

files_list = [
    'app/forms.py',
    'app/models.py',
    'app/views.py',
    'app/__init__.py',
    'config.py',
    'run.py',
    'tests.py',
]

for dir_ in dirs_list:
    if not os.path.exists(dir_):
        print msg_ok.format(dir_)
        os.mkdir(dir_)
    else:
        print msg_exist.format(dir_)


for file_ in files_list:
    if not os.path.exists(file_):
        open(file_, 'a').close()
        print msg_ok.format(file_)
    else:
        print msg_exist.format(file_)
