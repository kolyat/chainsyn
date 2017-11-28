import os
import web
from web import config


if not os.path.exists(config.FILE_UPLOAD_DIR):
    os.mkdir(config.FILE_UPLOAD_DIR)
web.web_interface.run(port=5555, debug=True)
