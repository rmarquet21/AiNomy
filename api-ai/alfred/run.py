import os

import alfred

AINOMY_PATH = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command('run:web:gunicorn', help="run ainomy with gunicorn")
def run_web_gunicorn():
    gunicorn = alfred.sh('gunicorn')
    os.chdir(AINOMY_PATH)
    args = ['--bind', '0.0.0.0:4000', '-w', '2', "server.app.web.webapp:create_app()",
            '--reload',
            '--timeout', '600',
            '--log-level', 'DEBUG',
            '--access-logfile', "-", "--access-logformat",
            '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s']

    alfred.run(gunicorn, args)
