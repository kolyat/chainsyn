# Copyright (c) 2016-2017 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

import flask_wtf
import wtforms


class EditorForm(flask_wtf.FlaskForm):
    mode = wtforms.RadioField(
        'modes',
        choices=[('replication', 'Replication'),
                 ('transcription', 'Transcription'),
                 ('translation', 'Translation')]
    )
    input_area = wtforms.TextAreaField()
    run = wtforms.SubmitField('Run')
