import maya.cmds as maya 
import pymel.core as pm

#ribbon component
#testlevel
#create new joint 
total_joint = 5
internal_joint = total_joint - 1
flexyjointList = []
jointChain = pm.ls(sl = True)

dup_jointChain = pm.duplicate(jointChain)
pm.parent(dup_jointChain, w = True)
root_joint = dup_jointChain[0]
pm.select(cl = True)
flexyjoint_start = pm.joint(n = 'flexy_joint0')
flexyjoint_start.setRadius(3)
flexyjointList.append(flexyjoint_start)
pm.parent(flexyjoint_start, w = True)
flexyjoint_start.setOrientation(root_joint.getOrientation())
pm.delete(pm.parentConstraint(root_joint, flexyjoint_start, mo = False))
endjoint = pm.listRelatives(root_joint, c = True, typ = 'joint')[0]
#get distance
distanceX = endjoint.tx.get()
print distanceX
steplen = distanceX/4.0
pm.delete(endjoint)
pm.delete(root_joint)


for i in range(internal_joint):  
    new_joint = pm.duplicate(flexyjoint_start)[0]
    flexyjointList.append(new_joint)
    new_joint.setRadius(2.0)
    movelen = steplen * (i + 1)
    pm.move(movelen, new_joint, x = True,r=True, os = True)
    new_joint.rename('flexy_joint' + str(i + 1))
#create nurbsurface

#create locator
pointlist = []
startlocator = pm.spaceLocator()
startlocator.rename('startlocator')
pm.delete(pm.parentConstraint(flexyjoint_start, startlocator, mo = False))
halfstepLen = steplen/2
pm.move(-halfstepLen, startlocator, x = True, r = True, os =True)
pointlist.append(pm.xform(startlocator,t = True, ws = True, q = True))
locator_num = total_joint

for i in range(locator_num):
    new_locator = pm.duplicate(startlocator)
    movelen = steplen * (i + 1)
    pm.move(movelen,new_locator, x = True,r=True, os = True)
    pointlist.append(pm.xform(new_locator,t = True, ws = True, q = True))

#create curve
#move curve along z axis
curve1 = pm.curve(p = pointlist,d = 1.0)
curve2 = pm.duplicate(curve1)
pm.move(2, curve1, x = True, r = True, os = True)
pm.move(-2, curve2, x = True, r = True, os = True)

flexymesh_transform = pm.loft(curve1, curve2, ar = True, d = 3, name = 'flexymesh', po = 0, rsn = True)[0]
#surface need to rebuild
pm.rebuildSurface(flexymesh_transform, du = 3, dv = 1, su = total_joint, sv = 1)
flexymesh = flexymesh_transform.getShape()

foll_grp = pm.group(em = True, w = True, n = 'FollicleNode')
#create follicles
for i in range (5):
    foll_transform = pm.createNode('transform', ss= True, name = 'follicle' + str(i))
    follicle = pm.createNode('follicle', name = 'follicleshape' + str(i), p = foll_transform)
    flexymesh.local.connect(follicle.inputSurface)
    flexymesh.worldMatrix[0].connect(follicle.inputWorldMatrix)
    follicle.outRotate.connect(follicle.getParent().rotate)
    follicle.outTranslate.connect(follicle.getParent().translate)
    follicle.parameterU.set(0.1 + i * 0.2)
    follicle.parameterV.set(0.5)
    follicle.getParent().t.lock()
    follicle.getParent().r.lock()
    pm.parent(flexyjointList[i], foll_transform)
    pm.parent(foll_transform,foll_grp)

extra_flexyNode = pm.group(em = True, w = True, n = 'Extra_FlexyNode')
pm.parent(foll_grp, extra_flexyNode)
pm.parent(flexymesh_transform, extra_flexyNode)

#create Bind Joint

bindjoint_Base = pm.joint(n = 'bindjoint_base')
pm.parent(bindjoint_Base, w = True)
pm.delete(pm.parentConstraint(flexyjointList[0], bindjoint_Base, mo = False))
pm.makeIdentity(bindjoint_Base, a = True,r = True)
bindjoint_Base.setRadius(3)

bindjoint_Tip = pm.joint(n = 'bindjoint_tip')
pm.parent(bindjoint_Tip, w = True)
pm.delete(pm.parentConstraint(flexyjointList[-1], bindjoint_Tip, mo = False))
pm.makeIdentity(bindjoint_Tip, a = True, r = True)
bindjoint_Tip.setRadius(3)

bindjoint_Mid = pm.joint(n = 'bindjoint_Mid')
pm.parent(bindjoint_Mid, w = True)
pm.delete(pm.parentConstraint(bindjoint_Tip, bindjoint_Base, bindjoint_Mid, mo = False))
pm.makeIdentity(bindjoint_Mid, a = True, r = True)
bindjoint_Mid.setRadius(3)

pm.delete(curve1)
pm.delete(curve2)