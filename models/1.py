# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''
import re
if re.compile('\w{2}(\-\w{2})?').match(request.vars.lang or ''):
    session.forced_language = request.vars.lang
if not session.forced_language:
    session.forced_language = 'de'
locale = 'de_DE'
if session.forced_language == 'en':
    locale = 'en_US'
elif session.forced_language == 'de':
    locale = 'de_DE'
T.force(locale)
