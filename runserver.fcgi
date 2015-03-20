#!/home2/javierac/virtualenvironments/tc-venv/bin/python 

from flup.server.fcgi import WSGIServer
from runserver import app as application

WSGIServer(application).run()
