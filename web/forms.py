# Copyright (c) 2016-2023 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

import flask_wtf
from flask_wtf import file
import wtforms


class EditorForm(flask_wtf.FlaskForm):
    mode = wtforms.RadioField(
        'modes',
        choices=[('replication', 'Replication'),
                 ('transcription', 'Transcription'),
                 ('translation', 'Translation')]
    )
    file_upload = file.FileField('Upload file')
    input_area = wtforms.TextAreaField()
    run = wtforms.SubmitField('Run')
