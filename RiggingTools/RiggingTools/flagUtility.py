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

    def mirrorflag(self, mirrorOrientation = False):
        origflag = pm.ls(sl = True)[0]
        pList = origflag.getCVs(space = 'world')
        for point in pList:
            point.x = point.x * -1
            point.y = point.y 
            point.z = point.z 
        #mirror plane# YZ
        #get object world transformation
        #use locator to determine world transformation
        locator1 = pm.spaceLocator()
        #if attr translate or roate is locked
        if origflag.translateX.isLocked() or origflag.translateY.isLocked() or origflag.translateZ.isLocked():
            origflag.translateX.set(l = False)
            origflag.translateY.set(l = False)
            origflag.translateZ.set(l = False)
        if origflag.rotateX.isLocked() or origflag.rotateY.isLocked() or origflag.rotateZ.isLocked():
            origflag.rotateX.set(l = False)
            origflag.rotateY.set(l = False)
            origflag.rotateZ.set(l = False)

        pm.delete(pm.parentConstraint(origflag, locator1, mo = False))
        #mirror by behaviour
        locator1.translateX.set(-locator1.translateX.get())
        if mirrorOrientation:
            locator1.rotate.set(locator1.rotateX.get(), locator1.rotateY.get() + 180, -locator1.rotateZ.get() + 180)
              
        mirror_flag = pm.duplicate(origflag)[0]
        pm.delete(pm.parentConstraint(locator1, mirror_flag, mo = False))
        mirror_flag.setCVs(pList, space = 'world')
        mirror_flag.updateCurve()
        pm.delete(locator1)

test = flagUtitlty()
test.mirrorflag(mirrorOrientation = True)
