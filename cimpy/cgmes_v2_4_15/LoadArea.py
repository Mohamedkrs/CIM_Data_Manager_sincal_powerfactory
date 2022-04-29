from cimpy.cgmes_v2_4_15.IdentifiedObject import IdentifiedObject
#all added by Mohamed

class LoadArea(IdentifiedObject):
	'''
	Loads that do not follow a daily and seasonal load variation pattern.
		'''

	cgmesProfile = IdentifiedObject.cgmesProfile

	possibleProfileList = {'class': [cgmesProfile.EQ.value, ],
						}

	serializationProfile = {}

	__doc__ += '\n Documentation of parent class LoadGroup: \n' + IdentifiedObject.__doc__ 

	def __init__(self,   *args, **kw_args):
		super().__init__(*args, **kw_args)

		

		
	def __str__(self):
		str = 'class=LoadArea\n'
		attributes = self.__dict__
		for key in attributes.keys():
			str = str + key + '={}\n'.format(attributes[key])
		return str
