from cimpy.cgmes_v2_4_15.ExcitationSystemDynamics import ExcitationSystemDynamics
#Mohamed copied this .py from ExcSEXS and added extra elements


class SEXS(ExcitationSystemDynamics):
	'''
	Simplified Excitation System Model.

	:tatb: Ta/Tb - gain reduction ratio of lag-lead element (TaTb).  Typical Value = 0.1. Default: 0.0
	:tb: Denominator time constant of lag-lead block (Tb).  Typical Value = 10. Default: 0
	:k: Gain (K) (>0).  Typical Value = 100. Default: 0.0
	:te: Time constant of gain block (Te).  Typical Value = 0.05. Default: 0
	:emin: Minimum field voltage output (Emin).  Typical Value = -5. Default: 0.0
	:emax: Maximum field voltage output (Emax).  Typical Value = 5. Default: 0.0
	:kc: PI controller gain (Kc).  Typical Value = 0.08. Default: 0.0
	:tc: PI controller phase lead time constant (Tc).  Typical Value = 0. Default: 0
	:efdmin: Field voltage clipping minimum limit (Efdmin).  Typical Value = -5. Default: 0.0
	:efdmax: Field voltage clipping maximum limit (Efdmax).  Typical Value = 5. Default: 0.0
		'''

	cgmesProfile = ExcitationSystemDynamics.cgmesProfile

	possibleProfileList = {'class': [cgmesProfile.DY.value, ],
						   'tatb': [cgmesProfile.DY.value, ],
						   'tb': [cgmesProfile.DY.value, ],
						   'k': [cgmesProfile.DY.value, ],
						   'te': [cgmesProfile.DY.value, ],
						   'emin': [cgmesProfile.DY.value, ],
						   'emax': [cgmesProfile.DY.value, ],
						   'kc': [cgmesProfile.DY.value, ],
						   'tc': [cgmesProfile.DY.value, ],
						   'efdmin': [cgmesProfile.DY.value, ],
						   'efdmax': [cgmesProfile.DY.value, ],
						   'Sn': [cgmesProfile.DY.value, ],
						   'SN': [cgmesProfile.DY.value, ],
						   'K': [cgmesProfile.DY.value, ],
						   'EMAX': [cgmesProfile.DY.value, ],
						   'EMIN': [cgmesProfile.DY.value, ],
						   'LPFP': [cgmesProfile.DY.value, ],
						   'LPFQ': [cgmesProfile.DY.value, ],
						   'phi': [cgmesProfile.DY.value, ],
						   'phinet': [cgmesProfile.DY.value, ],
						   'Plf': [cgmesProfile.DY.value, ],
						   'Pmax': [cgmesProfile.DY.value, ],
						   'Pmin': [cgmesProfile.DY.value, ],
						   'Qlf': [cgmesProfile.DY.value, ],
						   'Qmax': [cgmesProfile.DY.value, ],
						   'Qmin': [cgmesProfile.DY.value, ],
						   'Rlf': [cgmesProfile.DY.value, ],
						   'Snenn': [cgmesProfile.DY.value, ],
						   'TA_TB': [cgmesProfile.DY.value, ],
						   'TB': [cgmesProfile.DY.value, ],
						   'TE': [cgmesProfile.DY.value, ],
						   'Ulf': [cgmesProfile.DY.value, ],
						   'Ulfpu': [cgmesProfile.DY.value, ],
						   'UNE': [cgmesProfile.DY.value, ],
						   'UNN': [cgmesProfile.DY.value, ],
						   'XLF': [cgmesProfile.DY.value, ],
						   } 

	serializationProfile = {}

	__doc__ += '\n Documentation of parent class ExcitationSystemDynamics: \n' + \
		ExcitationSystemDynamics.__doc__

	def __init__(self, tatb = 0.0, tb = 0, XLF=0.0, k = 0.0, te = 0, emin = 0.0, emax = 0.0, kc = 0.0, tc = 0, efdmin = 0.0, efdmax = 0.0, K =0.0, SN=0.0, Sn=0.0, EMAX=0.0, EMIN=0.0, LPFP=0.0, LPFQ=0.0, phi=0.0, phinet=0.0, Plf=0.0, Pmax=0.0, Pmin=0.0, Qlf=0.0, Qmax=0.0, Qmin=0.0, Rlf=0.0, Snenn=0.0, TA_TB=0.0, TB=0.0, TE=0.0, Ulf=0.0, Ulfpu=0.0, UNE=0.0, UNN=0.0, *args, **kw_args):
		super().__init__(*args, **kw_args)

		self.tatb = tatb
		self.tb = tb
		self.k = k
		self.te = te
		self.emin = emin
		self.emax = emax
		self.kc = kc
		self.tc = tc
		self.efdmin = efdmin
		self.efdmax = efdmax
		self.K =K
		self.SN =SN 
		self.Sn = Sn
		self.EMAX= EMAX
		self.LPFP=LPFP 
		self.EMIN= EMIN
		self.LPFQ= LPFQ
		self.phi= phi
		self.phinet= phinet
		self.Plf= Plf
		self.Pmax= Pmax
		self.Pmin= Pmin
		self.Qlf=Qlf 
		self.Qmax= Qmax
		self.Qmin= Qmin
		self.Rlf= Rlf
		self.Snenn= Snenn
		self.TA_TB= TA_TB
		self.TB= TB
		self.TE= TE
		self.Ulf= Ulf
		self.Ulfpu= Ulfpu
		self.UNE= UNE
		self.UNN= UNN
		self.XLF = XLF
		

	def __str__(self):
		str = 'class=SEXS\n'
		attributes = self.__dict__
		for key in attributes.keys():
			str = str + key + '={}\n'.format(attributes[key])
		return str
