# Copyright (c) 2016-2021 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

import os
import re
import flask
from werkzeug import utils
from . import config
from web import web_interface, forms
from core import processing, tools


@web_interface.route('/', methods=['GET', 'POST'])
def main():
    editor_form = forms.EditorForm()
    if flask.request.method == 'GET':
        editor_form.mode.data = 'replication'
        stats = None
        output = ''
    else:
        if editor_form.validate_on_submit():
            if editor_form.file_upload.data:
                editor_form.input_area.data = ''
                f = editor_form.file_upload.data
                file_name = os.path.join(config.FILE_UPLOAD_DIR,
                                         utils.secure_filename(f.filename))
                f.save(file_name)
                try:
                    data = tools.from_file(file_name)
                    editor_form.input_area.data = list(data.values())[0]
                except tools.RoutineErr as e:
                    output = str(e)
                    return flask.render_template('main.html',
                                                 editor_form=editor_form,
                                                 output=output, stats=None)
            else:
                editor_form.input_area.data = \
                    re.sub('\s+', '', editor_form.input_area.data)
            chain = processing.Chain('', editor_form.input_area.data)
            try:
                if editor_form.mode.data == 'replication':
                    output = chain.replicate()
                elif editor_form.mode.data == 'transcription':
                    output = chain.transcribe()
                elif editor_form.mode.data == 'translation':
                    output = chain.translate()
                else:
                    output = ''
                if output:
                    stats = chain.collect_stats()
                else:
                    stats = None
            except processing.ProcessingErr as e:
                output = str(e)
                stats = None
        else:
            output = ''
            stats = None
    return flask.render_template('main.html', editor_form=editor_form,
                                 output=output, stats=stats)
