from src.utils import db
from src.utils import ini

# load ini file
_APP_ROOT_=ini.getenv('OPENSHIFT_REPO_DIR', '')
if not ini.init_config(_APP_ROOT_+'mapif.ini'):
    logger.mprint("Configuration file is missing. Server can't be started !")
    exit(-1)
# initialize database
db.init_db()

# fix issue #14: safe password storage with salt and blowfish encryption
for u in db.get_all_users():
    print("Updating: ", u, "...", end='')
    db.update_user_password(u.id)
    print("done!")

