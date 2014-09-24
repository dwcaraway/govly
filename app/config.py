#The name and port of the server. Required for subdomain support.
#SERVER_NAME = '127.0.0.1:8089'

# Statement for enabling the development environment
DEBUG = True

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'