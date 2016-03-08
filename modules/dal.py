# -*- coding: utf-8 -*-

class OMPDAL:
	def __init__(self):
		pass

	"""
	Get all authors associated with the specified submission regardless of exact role.
	"""
	def get_authors(self, submission_id):
		return db((db.authors.submission_id==submission_id)).select(
        	    db.authors.first_name, db.authors.middle_name, db.authors.last_name, orderby=db.authors.seq)

	"""
	Get all authors associated with the specified submission with editor role.
	"""
	def get_editors(self, submission_id):
		try:
			editor_group_id = myconf.take('omp.editor_id')
		except:
			editor_group_id = db.user_group_settings(db.user_group_settings.setting_value=="Volume editor").user_group_id
		return db( (db.authors.submission_id==submission_id) & (db.authors.user_group_id==) ).select(
		    db.authors.first_name, db.authors.middle_name, db.authors.last_name, orderby=db.authors.seq)

	"""
	Get all authors associated with the specified submission with chapter author role
	"""
	def get chapter_authors(self, submission_id):
		try:
			editor_group_id = myconf.take('omp.editor_id')
		except:
			editor_group_id = db.user_group_settings(db.user_group_settings.setting_value=="Chapter author").user_group_id
		return db( (db.authors.submission_id==submission_id) & (db.authors.user_group_id==myconf.take('omp.author_id')) ).select(
		    db.authors.first_name, db.authors.middle_name, db.authors.last_name, orderby=db.authors.seq)
