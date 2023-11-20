# Running on a Mac M1 Arm CPU

1. Make sure that the following brew packages are installed
   1. rust
   2. lpenssl
   3. libcffi
   4. msodbcsql17 and mssql-tools
      > HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=Y brew install msodbcsql17 mssql-tools
2. Install requirements normally
3. Pip uninstall:
   1. pyopenssl
   2. cryptography
   3. cffi
4. Reinstall cffi using
   > LDFLAGS=-L$(brew --prefix libffi)/lib CFLAGS=-I$(brew --prefix libffi)/include pip install cffi --no-binary :all:
5. Reinstall pyopenssl using
   > LDFLAGS="-L$(brew --prefix openssl@1.1)/lib" CFLAGS="-I$(brew --prefix openssl@1.1)/include" pip install pyopenssl
6. Reinstall mssql-django using
   > LDFLAGS="-L$(brew --prefix unixodbc)/lib" CFLAGS="-I$(brew --prefix unixodbc)/include" pip install mssql-django==1.1.3 

## Run Project

1. RabbitMQ Starts at boot 
2. Run Celery 
   >celery -A celery_worker worker --loglevel=DEBUG --logfile celery.log --concurrency=8 -n $WORKER_NAME
3. Run Spiders Manually
   > scrapy crawl [spider_name]
4. Run Django Server
   > python3 manage.py runserver 80