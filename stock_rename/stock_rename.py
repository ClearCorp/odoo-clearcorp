from osv import osv, fields
from tools import debug
import time
import pooler
from dateutil import parser
from datetime import date
import calendar
from tools.translate import _

class stock_location(osv.osv):
	_name = "stock.location"
	_inherit = "stock.location"
	
	def name_get(self, cr, uid, ids, context=None):
		if not ids:
			return []
		res = []
		for obj_stock_location in self.browse(cr,uid,ids):
			data = []
			location = obj_stock_location.location.id
			#is_leaf = True
			while location:
			#	if is_leaf:
		#			data.insert(0,location.name)
		#			is_leaf = False
		#		else:
				data.insert(0,(location.shortcut or location.name))
				location = location.location_id
			data.append(obj_stock_location.name)
			data = '/'.join(data)
			res.append((obj_stock_location.id, data))  
		return res
	
	def _complete_name2(self, cr, uid, ids, name, args, context=None):
		""" Forms complete name of location from parent location to child location.
		@return: Dictionary of values
		"""
		res = {}
		name_list = self.name_get(cr,uid,ids,context)
		for name in name_list:
			res[name[0]] = name[1]
		return res
	_columns = {
		'shortcut'  :  fields.char('Shortcut',size=10),
		'complete_name': fields.function(_complete_name2, method=True, type='char', size=100, string="Location Name"),
	}
stock_location()
