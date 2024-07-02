from codeplay.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Should only be False when running a development server
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Compilers path - points to compilers in the container
PYTHON_PATH = "/usr/local/bin/python3.10"  # not to be confused with PYTHONPATH environment variable
#PYTHON_PATH = "compilers/python.exe"
GCC_PATH = "/usr/bin/gcc"
GPP_PATH = "/usr/bin/g++"