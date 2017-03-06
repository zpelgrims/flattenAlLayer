# select object
# find top level allayer
# find connections to allayer

# create alsurface



import maya.cmds as cmds

objectName = cmds.ls(selection=True)



sl = cmds.ls(sl=1, o=1)

print "Objects selected: "
for s in sl:
    print s
    
cmds.select(sl)


shader = cmds.listConnections(cmds.listHistory(objectName, f=1),type='alLayer')


for sh in shader:
    print sh
    


# create new alsurface    
newShader = cmds.shadingNode("alSurface",asShader=True, n="alSurfaceMerged")
newShadingGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, n="alSurfaceMergedSG")
cmds.connectAttr('%s.outColor' %newShader ,'%s.surfaceShader' %newShadingGroup)

    
# find connections to alLayer
connectionLayer1 = cmds.listConnections('%s.layer1' %shader[0], d=0)
connectionLayer2 = cmds.listConnections('%s.layer2' %shader[0], d=0)
connectionMix = cmds.listConnections('%s.mix' %shader[0], d=0)

# create diffuse layer node
diffuseLayer = cmds.shadingNode("alLayerColor", n="alLayerColor_diffuse", asUtility=True)
cmds.setAttr("%s.layer1a" %diffuseLayer, 1.0)

# check if diffuse is connected to texture
inputConnectionCheck = cmds.listConnections('%s.diffuseColor' %connectionLayer1[0], destination=False)

diffuseList = ["diffuseColor", "diffuseColorR", "diffuseColorG", "diffuseColorG"]



for index, val in enumerate(diffuseList):
    inputConnectionCheck = cmds.listConnections('{0}.{1}'.format(connectionLayer1[0], diffuseList[index]), destination=False)
    
    if inputConnectionCheck != None:
        print "Found a connection, {0}".format(val)



if inputConnectionCheck == None:
    print "Diffuse color attribute does not have a connection"
    
    attributeValue = cmds.getAttr('%s.diffuseColor' %connectionLayer1[0])
    print attributeValue
    
    cmds.setAttr("%s.layer1R" %diffuseLayer, attributeValue[0][0])
    cmds.setAttr("%s.layer1G" %diffuseLayer, attributeValue[0][1])
    cmds.setAttr("%s.layer1B" %diffuseLayer, attributeValue[0][2])
else:
    print "Diffuse color attribute has a connection"
    
    attributeValue = inputConnectionCheck
    fileOutput = str(cmds.listConnections('%s.diffuseColor' %connectionLayer1[0], plugs=True)[0])
    
    cmds.connectAttr(fileOutput, "%s.layer1" %diffuseLayer)
    
    
cmds.listAttr("alSurface2")












alSurfaceAttributeList = ["diffuseStrength", "diffuseColor", "diffuseColorR", "diffuseColorG", "diffuseColorB", "diffuseRoughness"]





def checkInputs(node, alSurfaceAttributeList):
    
    connectionsList = []
    
    for index, val in enumerate(alSurfaceAttributeList):
        inputConnectionCheck = cmds.listConnections('{0}.{1}'.format(node[0], alSurfaceAttributeList[index]), destination=False)
    
        if inputConnectionCheck != None:
            print "Found a connection for {0}".format(val)
            connectionsList.append(val)
    
    return connectionsList



connectionsList = checkInputs(connectionLayer1, alSurfaceAttributeList)







def compareValues(node1, node2, alSurfaceAttributeList, connectionsList):
    
    for index, val in enumerate(alSurfaceAttributeList):
        
        if val in connectionsList:
            value1 = cmds.listConnections('{0}.{1}'.format(node1, alSurfaceAttributeList[index]), destination=False)
            value2 = cmds.listConnections('{0}.{1}'.format(node2, alSurfaceAttributeList[index]), destination=False)
            
        else:
                
            value1 = cmds.getAttr("{0}.{1}".format(node1, alSurfaceAttributeList[index]))
            value2 = cmds.getAttr("{0}.{1}".format(node2, alSurfaceAttributeList[index]))
        
        if value1 == value2:
            print "{0} [SAME]: {1}, {2}".format(val, value1, value2)
        else:
            print "{0} [DIFFERENT]: {1}, {2}".format(val, value1, value2)
        
    
compareValues("alSurface1", "alSurface2", alSurfaceAttributeList, connectionsList)














