import os
from werkzeug.security import generate_password_hash

PASSWORD_HASH = generate_password_hash('pohang')
SECRET_KEY = 'super-secret-key'
