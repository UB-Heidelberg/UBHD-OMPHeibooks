# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''
import re
if re.compile('\w{2}(\-\w{2})?').match(request.vars.lang or ''):
    session.forced_language = request.vars.lang
if session.forced_language is None:
  session.forced_language = 'de'

locale = session.forced_language
T.force(locale)