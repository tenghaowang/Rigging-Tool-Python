import maya.cmds as maya 
import pymel.core as pm


class flagUtitlty(object):

	def circleWire_Y(self):
		circle = pm.circle()

	def circleWire_X(self):
		circle = pm.circle()
		makecirclenode = pm.nodetypes.MakeNurbCircle(circle[1])
		makecirclenode.setNormal([1,0,0])

	def circleWire_Z(self):
		circle = pm.circle()

	def cubeWire(self):
		print ('cube flag generated')

 