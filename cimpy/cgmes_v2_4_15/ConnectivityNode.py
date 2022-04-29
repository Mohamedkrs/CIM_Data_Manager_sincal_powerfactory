from cimpy.cgmes_v2_4_15.IdentifiedObject import IdentifiedObject

class ConnectivityNode(IdentifiedObject):
	'''
	Connectivity nodes are points where terminals of AC conducting equipment are connected together with zero impedance.

	:TopologicalNode: The connectivity nodes combine together to form this topological node.  May depend on the current state of switches in the network. Default: None
		'''

	cgmesProfile = IdentifiedObject.cgmesProfile

	possibleProfileList = {'class': [cgmesProfile.TP.value,cgmesProfile.EQ.value, ],
						'TopologicalNode': [cgmesProfile.TP.value, ],
						'ConnectivityNodeContainer':[cgmesProfile.EQ.value, ], #added by Mohamed
						 }

	serializationProfile = {}

	__doc__ += '\n Documentation of parent class IdentifiedObject: \n' + IdentifiedObject.__doc__ 


	def __init__(self, TopologicalNode = None,ConnectivityNodeContainer = None ,  *args, **kw_args ):
		super().__init__(*args, **kw_args)
		self.TopologicalNode = TopologicalNode
		self.ConnectivityNodeContainer = ConnectivityNodeContainer
		
	def __str__(self):
		str = 'class=ConnectivityNode\n'
		attributes = self.__dict__
		for key in attributes.keys():
			str = str + key + '={}\n'.format(attributes[key])
		return str
