# -*- coding: utf-8 -*-

class OMPDAL:
	def __init__(self, db, conf):
		self.db = db
		self.conf = conf

	def getAuthors(self, submission_id):
        	"""
	       	Get all authors associated with the specified submission regardless of exact role.
        	"""
		return self.db((self.db.authors.submission_id==submission_id)).select(self.db.authors.first_name, self.db.authors.middle_name, self.db.authors.last_name, orderby=self.db.authors.seq)

	def getEditors(self, submission_id):
        	"""
	       	Get all authors associated with the specified submission with editor role.
       		"""
		try:
			editor_group_id = self.conf.take('omp.editor_id')
		except:
			return []
		return self.db((self.db.authors.submission_id==submission_id) & (self.db.authors.user_group_id==editor_group_id)).select(self.db.authors.first_name, self.db.authors.middle_name, self.db.authors.last_name, orderby=self.db.authors.seq)

	def getChapterAuthors(self, submission_id):
       		"""
       		Get all authors associated with the specified submission with chapter author role
       		"""
		try:
			chapter_author_group_id = self.conf.take('omp.author_id')
		except:
			return []
		return self.db((self.db.authors.submission_id==submission_id) & (self.db.authors.user_group_id==chapter_author_group_id)).select(self.db.authors.first_name, self.db.authors.middle_name, self.db.authors.last_name, orderby=self.db.authors.seq)

	def getSubmission(self, submission_id):
		return self.db.submissions[submission_id]

	def getLocalizedSeriesSettings(self, series_id, locale):
		return self.db((self.db.series_settings.series_id==series_id) & (self.db.series_settings.locale == locale)).select(self.db.series_settings.setting_name, self.db.series_settings.setting_value)

	def getSeriesSettings(self, series_id):
		return self.db(self.db.series_settings.series_id==series_id).select(self.db.series_settings.locale, self.db.series_settings.setting_name, self.db.series_settings.setting_value)
