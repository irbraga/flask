'''
Module for Gunicorn configuration.
'''
# pylint: disable=invalid-name
# https://docs.gunicorn.org/en/stable/configure.html#configuration-file
# https://docs.gunicorn.org/en/stable/settings.html#settings
import multiprocessing

bind = '127.0.0.1:5000'
workers = multiprocessing.cpu_count() * 2 + 1
reload = False
logLevel = 'info'
errorlog = 'app.log'
