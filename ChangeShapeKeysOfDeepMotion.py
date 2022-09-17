'''
reference:
    https://blender.stackexchange.com/questions/143601/batch-rename-shape-keys
    https://blender.stackexchange.com/questions/149045/blender-api-how-to-set-shapekeys-as-keyframe-in-a-loop
'''

import bpy

# get the selected object
selected_object = bpy.context.object

# get its shapekeys
shape_keys = selected_object.data.shape_keys.key_blocks

# little utility function for searching fcurves
# https://blender.stackexchange.com/questions/3240/how-to-get-a-property-value-not-in-current-frame
def find_fcurve(id_data, path, index=0):
    anim_data = id_data.animation_data
    for fcurve in anim_data.action.fcurves:
        #print(fcurve.data_path)
        if fcurve.data_path == path and fcurve.array_index == index:
            #print("found "+"index"+str(index))
            return fcurve
    #print("not found")

def GetShapeKeyValueByFrame(selected_object, keyName, f):
    re = find_fcurve(selected_object.data.shape_keys,'key_blocks["{0}"].value'.format(keyName)).evaluate(f)
    print("f:{0}, key.name:{1}, Val:{2}".format(f, keyName, re))    
    return re

#修改shapeKey的值，比如没有mouseClose需要从jawOpen里逐帧减去
def ChangeShapeKeyValuesByFrame(shape_keys):
    # get the selected object
    selected_object = bpy.context.object    

    # get frames
    frames = bpy.context.scene.frame_end + 1

    mouthCloseVal = [0.0 for index in range(frames)]
    jawOpenVal = [0.0 for index in range(frames)]
    eyeBlinkLeftVal = [0.0 for index in range(frames)]
    eyeBlinkRightVal = [0.0 for index in range(frames)]   
    browDownLeftVal = [0.0 for index in range(frames)]        
    browDownRightVal = [0.0 for index in range(frames)]       

    ifHaveJawOpen = False
    ifHaveMouthClose = False   
    ifHaveEyeBlinkLeft = False   
    ifHaveEyeBlinkRight = False   
    ifHaveBrowDownLeft = False       
    ifHaveBrowDownRight = False    

    for f in range(frames):     
        for key in shape_keys:
            if key.name == "mouthClose":
                '''
                mouthCloseVal[f] = find_fcurve(selected_object.data.shape_keys,'key_blocks["mouthClose"].value').evaluate(f)
                print("f:{0}, key.name:{1}, mouthCloseVal:{2}".format(f, key.name, mouthCloseVal[f]))
                ifHaveMouthClose = True
                '''
                mouthCloseVal[f] = GetShapeKeyValueByFrame(selected_object, key.name, f)
                ifHaveMouthClose = True                
            if key.name == "jawOpen":
                jawOpenVal[f] = GetShapeKeyValueByFrame(selected_object, key.name, f)
                ifHaveJawOpen = True
                                              
            if key.name == "eyeBlinkLeft":
                eyeBlinkLeftVal[f] = GetShapeKeyValueByFrame(selected_object, key.name, f)
                ifHaveEyeBlinkLeft = True
            if key.name == "eyeBlinkRight":
                eyeBlinkRightVal[f] = GetShapeKeyValueByFrame(selected_object, key.name, f)          
                ifHaveEyeBlinkRight = True                
            if key.name == "browDownLeft":
                browDownLeftVal[f] = GetShapeKeyValueByFrame(selected_object, key.name, f)
                ifHaveBrowDownLeft = True
            if key.name == "browDownRight":
                browDownRightVal[f] = GetShapeKeyValueByFrame(selected_object, key.name, f)          
                ifHaveBrowDownRight = True                 
    
    #larger coefficient, make the expression more exaggerated
    largerC=1.8
                
    if ifHaveJawOpen and ifHaveMouthClose:            
        for f in range(frames):  
            #update open values          
            shape_keys["jawOpen"].value = max(jawOpenVal[f]-mouthCloseVal[f],0)*largerC
            shape_keys["jawOpen"].keyframe_insert("value", frame=f)
            
            #set zero
            shape_keys["mouthClose"].value = 0
            shape_keys["mouthClose"].keyframe_insert("value", frame=f)            
            
    #Blink eyes -> lower down the brows
    if ifHaveEyeBlinkLeft and ifHaveEyeBlinkRight and ifHaveBrowDownLeft and ifHaveBrowDownRight:
        for f in range(frames):          
            shape_keys["browDownLeft"].value = max(browDownLeftVal[f],eyeBlinkLeftVal[f])
            shape_keys["browDownLeft"].keyframe_insert("value", frame=f)        
            
            shape_keys["browDownRight"].value = max(browDownRightVal[f],eyeBlinkRightVal[f])
            shape_keys["browDownRight"].keyframe_insert("value", frame=f)        
            
      

def ChangeShapeKeyNamesToMMD_Format(shape_keys):
    for key in shape_keys:
        oldName = key.name
        newName = oldName
        if oldName == "eyeBlinkLeft":
            newName = "ウィンク２"        
        if oldName == "eyeBlinkRight":
            newName = "ウィンク２右"
        if oldName == "jawOpen":
            newName = "ワ"
        if oldName == "mouthFunnel":
            newName = "お"
        if oldName == "mouthPucker":
            newName = "口横狭め"
        if oldName == "mouthSmileLeft":
            newName = "にやり２"                    
        if oldName == "mouthSmileRight":
            newName = "にやり"      
        if oldName == "mouthFrownRight":
            newName = "ん"       
        if oldName == "mouthStretchRight":
            newName = "口横広げ"                             
    #    if oldName == "mouthShrugUpper":
    #        newName = "あ"     
        if oldName == "browDownLeft":
            newName = "下左"       
        if oldName == "browDownRight":
            newName = "下右"        
        if oldName == "browInnerUp":
            newName = "困る"   
        if oldName == "browInnerUp":
            newName = "困る"        
#        if oldName == "noseSneerLeft":
#            newName = "怒り左"        
#        if oldName == "noseSneerRight":
#            newName = "怒り右"                                
        if oldName == "tongueOut":
            newName = "ぺろっ"                                  
        key.name = newName


ChangeShapeKeyValuesByFrame(shape_keys)
ChangeShapeKeyNamesToMMD_Format(shape_keys)


# loop through shapekeys and replace the names
'''
for key in shape_keys:
    key.name = key.name.replace("Key", "FaceKey")
'''
    
# loop through shapekeys and replace the names
'''
for index, key in enumerate(shape_keys):
    if key.name != "Basis":
        key.name = "MyKey" + str(index) 
'''   