from config.default import *

SQLALCHEMY_DATABASE_URI ='sqlite://{}'.format(os.path.join(BASE_DIR, 'homepage.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'Q\xa1|\x8c^\xbf\x84i\xca\x081 \xf4\xd5\xf7\xbf'