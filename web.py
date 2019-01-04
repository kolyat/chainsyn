# Copyright (c) 2016-2019 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

import os
import web
from web import config


if not os.path.exists(config.FILE_UPLOAD_DIR):
    os.mkdir(config.FILE_UPLOAD_DIR)
web.web_interface.run(port=5555, debug=True)
