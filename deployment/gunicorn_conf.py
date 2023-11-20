bind = "unix:/home/autotrader-admin/autotrader/autotrader.az/deployment/autotrader-main.sock"
workers = 4
loglevel = "debug"
accesslog = "/var/log/gunicorn/autotrader_access.log"
access_log_format = "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog = "/var/log/gunicorn/autotrader_error.log"
reload = True
