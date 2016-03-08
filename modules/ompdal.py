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
			pass#editor_group_id = self.db.user_group_settings(self.db.user_group_settings.setting_value=="Volume editor").user_group_id
		return self.db((self.db.authors.submission_id==submission_id) & (self.db.authors.user_group_id==editor_group_id)).select(self.db.authors.first_name, self.db.authors.middle_name, self.db.authors.last_name, orderby=self.db.authors.seq)

	def getChapterAuthors(self, submission_id):
       		"""
       		Get all authors associated with the specified submission with chapter author role
       		"""
		try:
			chapter_author_group_id = self.conf.take('omp.author_id')
		except:
			pass#chapter_author_group_id = self.db.user_group_settings(self.db.user_group_settings.setting_value=="Chapter author").user_group_id
		return self.db((self.db.authors.submission_id==submission_id) & (self.db.authors.user_group_id==chapter_author_group_id)).select(self.db.authors.first_name, self.db.authors.middle_name, self.db.authors.last_name, orderby=self.db.authors.seq)
