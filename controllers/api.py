# -*- coding: utf-8 -*-
'''
Copyright (c) 2015 Heidelberg University Library
Distributed under the GNU GPL v3. For full terms see the file
LICENSE.md
'''

import gluon.contrib.simplejson as sj
from ompdal import OMPDAL
from ompcsl import OMPCSL
from os.path import join


response.headers['Content-Type'] = 'application/json'
response.view = 'generic.json'
url = join(request.env.http_host, request.application, request.controller)

ompdal = OMPDAL(db, myconf)
press = ompdal.getPress(myconf.take('omp.press_id'))

if session.forced_language == 'en':
    locale = 'en_US'
elif session.forced_language == 'de':
    locale = 'de_DE'
else:
    locale = ''


@request.restful()
def index():
    """
    Returns all the rest services
    """

    def GET(*args, **vars):
        l = ['catalog', 'csl', 'oastatistik']

        apis = {}
        for i in l:
            apis[i] = join(url, i)
        return apis

    return locals()


@request.restful()
def catalog():
    """ Returns  press submissions """

    def GET(*args, **vars):
        submissions = ompdal.getSubmissionsByPress(press.press_id, -1).as_list()
        submission_ids = [{s['submission_id']: join(url, 'catalog', str(s['submission_id']))} for s in submissions]
        return dict(submissions=request.vars.sort_by)

    return locals()


def remove_url_prefix(url):
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    urls = [url.split('/')[0] for url in url.split()]
    return ''.join(urls)


def oastatistik():

    ompdal = OMPDAL(db, myconf)
    result = []
    locale = 'de_DE'
    context_id = myconf.take('omp.press_id')
    stats_id = myconf.take('statistik.id')
    db_submissions = db.submissions
    q = ((db_submissions.context_id == context_id) & (db_submissions.status == 3))
    submissions = db(q).select(db_submissions.submission_id, orderby=(db_submissions.submission_id))
    press_path = ompdal.getPress(context_id).get('path')

    series_list = ompdal.getSeriesByPress(context_id)

    for series in series_list:
        if series:
            s = {}
            dbs = db.series_settings
            title = db(
                (dbs.series_id == series.get('series_id')) & (dbs.locale == locale) & (dbs.setting_name == 'title')).select(
                dbs.setting_value)

            series_norm_id = '{}:{}:{}'.format(stats_id, press_path, series.get('path'))
            s['doc_id'] = series_norm_id
            s['type'] = 'collection'
            s['title'] = title.first().get('setting_value') or ''
            s['id'] = 'MD:{}'.format(series_norm_id)

            result.append(s)

    for submission in submissions:

        submission_id = submission.submission_id
        norm_id = '{}:{}'.format(stats_id, submission_id)

        metadata_published_date = ompdal.getMetaDataPublishedDates(submission_id).first()
        date_published = metadata_published_date.date_logged if metadata_published_date else None
        if not date_published:
            date_published = submission.date_status_modified
        year = date_published.year  if date_published else []


        volume = {
            "id"  : 'MD:{}'.format(norm_id),
            "type": "volume",
            }
        if year:
            volume['year'] = year

        volume["doc_id"] = '{}'.format(norm_id)
        # submission
        submission_settings = ompdal.getSubmissionSettings(submission_id).as_list()

        srs = ompdal.getSeriesBySubmissionId(submission_id)
        series_norm_id = '{}:{}:{}'.format(stats_id, press_path, srs.get('path')) if srs else []

        for setting in submission_settings:
            if setting["locale"] == locale and setting["setting_name"] == 'title':
                volume["title"] = setting["setting_value"]
            if setting["setting_name"] == 'pub-id::doi':
                volume["norm_id"] = setting["setting_value"]
            if series_norm_id:
                volume["parent_id"] ='MD:{}'.format(series_norm_id)
        result.append(volume)

        chapters = ompdal.getChaptersBySubmission(submission_id).as_list()

        for chapter in chapters:
            chapter_id = chapter["chapter_id"]

            chapter_norm_id = "{}:{}-c{}".format(stats_id, submission_id, chapter_id)
            chs_ = {
                "id"    : 'MD:{}'.format(chapter_norm_id),
                "type"  : "part",
                "parent": norm_id,
                "doc_id": chapter_norm_id
                }
            chapter_settings = ompdal.getChapterSettings(chapter_id).as_list()
            for chapter_setting in chapter_settings:
                if chapter_setting["locale"] == locale and chapter_setting["setting_name"] == 'title':
                    chs_["title"] = chapter_setting["setting_value"]
                if chapter_setting["setting_name"] == 'pub-id::doi':
                    chs_["norm_id"] = chapter_setting["setting_value"]

            result.append(chs_)

    return sj.dumps(result, separators=(',', ':'))


def get_submission_files(book_id):
    full_files = db(
            (db.submission_files.genre_id == myconf.take('omp.monograph_type_id')) & (
                    db.submission_files.file_stage > 5) & (
                    db.submission_files.submission_id == book_id.submission_id)).select(
            db.submission_files.submission_id,
            db.submission_files.file_id,
            db.submission_files.original_file_name)
    return full_files


def get_publication_format_settings_doi(publication_format_settings, publication_format_settings_doi):
    publication_format_settings_doi = db(
            (db.publication_format_settings.setting_name == 'pub-id::doi') & (
                    db.publication_format_settings.publication_format_id == publication_format_settings.first()[
                'publication_format_id']) & (
                    publication_format_settings.first()['setting_value'] == myconf.take('omp.doi_format_name'))).select(
            db.publication_format_settings.setting_value).first()
    return publication_format_settings_doi


def get_publication_format_settings(book_id):
    publication_format_settings = db(
            (db.publication_format_settings.setting_name == 'name') & (
                    db.publication_formats.submission_id == book_id['submission_id']) & (
                    db.publication_formats.publication_format_id ==
                    db.publication_format_settings.publication_format_id)).select(
            db.publication_format_settings.publication_format_id,
            db.publication_format_settings.setting_value)
    return publication_format_setting


def csl():
    if request.args:
        submission_id = request.args[0]
    else:
        raise HTTP(405, "Missing submission ID and getting of all submissions not supported")
    locale = 'de_DE'
    if session.forced_language == 'en':
        locale = 'en_US'
    ompcsl = OMPCSL(OMPDAL(db, myconf), myconf, locale)
    response.headers['Content-Type'] = 'application/json'
    try:
        cls_data = ompcsl.load_csl_data(submission_id)
    except ValueError as e:
        # Invalid argument
        raise HTTP(400, e.message)

    return sj.dumps(cls_data, separators=(',', ':'), sort_keys=True)
