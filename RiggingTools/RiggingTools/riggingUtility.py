import maya.cmds as maya
import pymel.core as pm


def lock_hide_attr(translate = True, rotate = True, scale = True):
    selobj = pm.ls(sl = True)
    for obj in selobj:
        if translate:
            obj.translateX.set(l = True)
            obj.translateY.set(l = True)
            obj.translateZ.set(l = True)
        if rotate:
            obj.rotateX.set(l = True)
            obj.rotateY.set(l = True)
            obj.rotateZ.set(l = True)
        if scale:
            obj.scaleX.set(l = True)
            obj.scaleY.set(l = True)
            obj.scaleZ.set(l = True)

lock_hide_attr()