# Copyright (c) 2016-2017 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

import flask
from web import web_interface, forms


@web_interface.route('/', methods=['GET', 'POST'])
def main():
    editor_form = forms.EditorForm()
    return flask.render_template('main.html', editor_form=editor_form)
