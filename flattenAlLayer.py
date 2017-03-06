# select object
# find top level allayer
# find connections to allayer

# create alsurface



import maya.cmds as cmds

objectName = cmds.ls(selection=True)

shader = cmds.listConnections(cmds.listHistory(objectName, f=1),type='alLayer')
if shader == None:
    print "Select a shape with an AlLayer shader assigned"


# create new alsurface    
newShader = cmds.shadingNode("alSurface",asShader=True, n="alSurfaceMerged")
newShadingGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, n="alSurfaceMergedSG")
cmds.connectAttr('%s.outColor' %newShader ,'%s.surfaceShader' %newShadingGroup)

    
# find connections to alLayer
connectionLayer1 = cmds.listConnections('%s.layer1' %shader[0], d=0)
connectionLayer2 = cmds.listConnections('%s.layer2' %shader[0], d=0)
connectionMix = cmds.listConnections('%s.mix' %shader[0], d=0, plugs=True)







    
cmds.listAttr("alLayerColor_diffuseColor")












alSurfaceAttributeList = ["diffuseStrength", "diffuseColor", "diffuseColorR", "diffuseColorG", "diffuseColorB", "diffuseRoughness"]


def createLayer(type, attribute):
    layer = ""
    
    if type == "float":
        layer = cmds.shadingNode("alLayerFloat", n="alLayerFloat_{0}".format(attribute), asUtility=True)
    elif type == "color":
        layer = cmds.shadingNode("alLayerColor", n="alLayerColor_{0}".format(attribute), asUtility=True)
        
    cmds.setAttr("%s.layer1a" %layer, 1.0)
    cmds.setAttr("%s.layer2a" %layer, 1.0)
    
    return layer
    
    


def checkInputs(node, alSurfaceAttributeList):
    
    connectionsList = []
    
    for index, val in enumerate(alSurfaceAttributeList):
        inputConnectionCheck = cmds.listConnections('{0}.{1}'.format(node[0], alSurfaceAttributeList[index]), destination=False)
    
        if inputConnectionCheck != None:
            print "Found a connection for {0}".format(val)
            connectionsList.append(val)
    
    return connectionsList



connectionsList = checkInputs(connectionLayer1, alSurfaceAttributeList)







def compareValues(node1, node2, node3, alSurfaceAttributeList, connectionsList):
    
    for index, val in enumerate(alSurfaceAttributeList):
        
        if val in connectionsList:
            value1 = cmds.listConnections('{0}.{1}'.format(node1, alSurfaceAttributeList[index]), destination=False)
            value2 = cmds.listConnections('{0}.{1}'.format(node2, alSurfaceAttributeList[index]), destination=False)
            
        else:
            value1 = cmds.getAttr("{0}.{1}".format(node1, alSurfaceAttributeList[index]))
            value2 = cmds.getAttr("{0}.{1}".format(node2, alSurfaceAttributeList[index]))
        
            
        if cmds.getAttr("{0}.{1}".format(node1, val), type=1) == "float":
            attributeType = "float"
        elif cmds.getAttr("{0}.{1}".format(node1, val), type=1) == "float3":
            attributeType = "color"
        
        
        if value1 == value2:
            print "{0} [SAME]: {1}, {2}".format(val, value1, value2)
        else:
            print "{0} [DIFFERENT]: {1}, {2}".format(val, value1, value2)
            
            currentLayer = createLayer(attributeType, val)
            
            if attributeType == "float":
                cmds.connectAttr("{0}.{1}".format(node1, val), "{0}.layer1".format(currentLayer))
                cmds.connectAttr("{0}.{1}".format(node2, val), "{0}.layer2".format(currentLayer))
                cmds.connectAttr("{0}".format(node3), "{0}.layer2a".format(currentLayer))
            elif attributeType == "color":
                cmds.connectAttr("{0}.{1}".format(node1, val), "{0}.layer1".format(currentLayer))
                cmds.connectAttr("{0}.{1}".format(node2, val), "{0}.layer2".format(currentLayer))
                cmds.connectAttr("{0}".format(node3), "{0}.layer2a".format(currentLayer))
            
        
    
compareValues(connectionLayer1[0], connectionLayer2[0], connectionMix[0], alSurfaceAttributeList, connectionsList)