import os
from werkzeug.security import generate_password_hash

PASSWORD_HASH = generate_password_hash('')
SECRET_KEY = 'super-secret-key'
