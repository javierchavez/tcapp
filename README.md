#TC Committee

[![Build Status](https://travis-ci.org/javierchavez/tcapp.svg)](https://travis-ci.org/javierchavez/tcapp)


###Initial Configuration
you need to set some env vars for mail.


    export MAIL_USERNAME=''
    export MAIL_PASSWORD=''
    export MAIL_DEFAULT_SENDER='tc committee < >'
    export MAIL_SERVER=''
    export MAIL_PORT='465'
    export MAIL_USE_SSL='1'
    export MAIL_USE_TLS='0'

**You also need to run pip.** Usually with virtualenv activated.

	
	pip install -r requirements.txt


###Running


    python runserver.py
    
    
###Testing


	python tests.py