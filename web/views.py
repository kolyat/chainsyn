# Copyright (c) 2016-2017 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

import re
import flask
from web import web_interface, forms
from core import processing


@web_interface.route('/', methods=['GET', 'POST'])
def main():
    editor_form = forms.EditorForm()
    if flask.request.method == 'GET':
        editor_form.mode.data = 'replication'
        output = ''
    else:
        if editor_form.validate_on_submit():
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
            except processing.ProcessingErr as e:
                output = str(e)
        else:
            output = ''
    return flask.render_template('main.html', editor_form=editor_form,
                                 output=output)
