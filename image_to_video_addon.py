bl_info = {
    "name": "Image to Video Converter",
    "author": "Liam D'Arcy",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "Properties > Output Properties > Image to Video Converter",
    "description": "Converts a list of images to video",
    "warning": "",
    "doc_url": "",
    "category": "Render",
}

#imports main modules
import bpy
import os

#imports extra modules
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, OperatorFileListElement

#clears the sequence editor
def clear_sequence(seq):
    for strip in seq:
        seq.remove(strip)
        
    return {'FINISHED'}

#used to manually adjust resolution. Only used if manual_res == True
def adjust_resolution(scene, x, y):
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    
    return {"FINISHED"}

#sets the video length
def adjust_frames(scene, start, end):
    scene.frame_start = start
    scene.frame_end = end
    
    return {'FINISHED'}

#-----------------------------------------------
# Class of properties to be referenced elsewhere
#-----------------------------------------------

class myProperties(bpy.types.PropertyGroup):
    
    output_directory : StringProperty(name="Output", subtype="FILE_PATH", description="Destination for your Video")
    
    manual_res : BoolProperty(name="Manually Adjust Resolution")
    res_x : IntProperty(name="X Res", default=1920)
    res_y : IntProperty(name="Y Res", default=1080)
    
    manual_frames : BoolProperty(name="Manually Adjust Frames")
    frame_start : IntProperty(name="Frame Start", default=0)
    frame_end : IntProperty(name="Frame End", default=250)
    
#---------------------------------------
# Creates the UI panel
#---------------------------------------

class UIPanel(bpy.types.Panel):
    #panel name, ID's and location
    bl_label = "Image to Video Converter"
    bl_idname = "IMG_PT_CONVERT"
    bl_space_type = 'PROPERTIES'
    bl_region_type = "WINDOW"
    bl_context = "output"
    
        
    #Function which defines the UI
    def draw(self, context):
        layout = self.layout
        mydirectories = context.scene.my_directories
        
        #input and output directories
        layout.prop(mydirectories, "output_directory")
        row = layout.row()
        layout.prop(mydirectories, "manual_res")
        
        row = layout.row()
        sub = row.row()
        sub.enabled = mydirectories.manual_res
        sub.prop(mydirectories, "res_x")
        
        row = layout.row()
        sub = row.row()
        sub.enabled = mydirectories.manual_res
        sub.prop(mydirectories, "res_y")
        
        row = layout.row()
        layout.prop(mydirectories, "manual_frames")
        
        row = layout.row()
        sub = row.row()
        sub.enabled = mydirectories.manual_frames
        sub.prop(mydirectories, "frame_start")
        
        row = layout.row()
        sub = row.row()
        sub.enabled = mydirectories.manual_frames
        sub.prop(mydirectories, "frame_end")


        #text and icon
        row = layout.row()
        row.label(text="Convert Image Sequence to Video", icon='IMAGE_DATA')
        row = layout.row()
        #button that calls the file browser
        row.scale_y = 2.0
        row.operator("import_test.some_data", text= "Import Images and Convert")
        
#------------------------------------------------------------
# Operator Class
# Opens a file browser
# imports the images
# converts to video
# Stores video in designated "Output" directory
#------------------------------------------------------------
    
class ImportSomeData(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Some Data"
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_description = "Import Images and Convert them to Video."

    # ImportHelper mixin class uses this
    filename_ext = ".png"

    filter_glob: StringProperty(
            default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp;*.exr',
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    files: CollectionProperty(
        name="BVH files",
        type=OperatorFileListElement,
        )

    directory: StringProperty(subtype='DIR_PATH', options={'HIDDEN'})

    def execute(self, context):
        
        #common BPY shortcuts
        scene = bpy.context.scene
        seq = scene.sequence_editor.sequences
        
        #formats the file list as taken from the image 
        filesFormatted = self.files
        fileList = []
        
        #adds each file in the file list to a new file with basic array formatting - think of it as dictionary to array code
        for file in filesFormatted:
            filepath = file.name
            print(filepath) #debug
            fileList.append(filepath)
            
        print(fileList) #debug
        
        
        #shorthand for the properties from myProperties
        mydirectories = scene.my_directories
        
        
        clear_sequence(seq)
        
        j = 0
        
        directoryString = self.directory
        
        print(directoryString)
        
        
        #creates each frame in the sequencer and produces the length of the video
        for i in fileList:
            j += 1
            seq.new_image("image" + str(j), directoryString + i, 1, j)
            #debug
            print("imported image: " + str(i))
            
        #merges the frames into a video
        bpy.ops.sequencer.meta_make()
        
        old_start = scene.frame_start
        old_end = scene.frame_end
        
        if mydirectories.manual_frames == True:
            adjust_frames(scene, mydirectories.frame_start, mydirectories.frame_end)
        else:
            adjust_frames(scene, 0, j)
        
        
        old_path = scene.render.filepath
        
        #sets the file output path to be the folder the images came from
        scene.render.filepath = bpy.path.abspath(mydirectories.output_directory)
        
        #caches the old resolution settings
        old_x = scene.render.resolution_x
        old_y = scene.render.resolution_y
        
        #checks whether to use manual resolutions
        if mydirectories.manual_res == True:
            adjust_resolution(scene, mydirectories.res_x, mydirectories.res_y)
        
        #activates render
        bpy.ops.render.render(animation=True, write_still=False, use_viewport=False)
        
        clear_sequence(seq)
        
        #resets resolution
        adjust_resolution(scene, old_x, old_y)
        
        adjust_frames(scene, old_start, old_end)
        
        scene.render.filepath = old_path
        
        return {'FINISHED'}

 
classes = [myProperties, UIPanel, ImportSomeData]

#activates the addon when enabled in preferences
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
        bpy.types.Scene.my_directories = bpy.props.PointerProperty(type=myProperties)

#deactivates the addon when disabled in prefernces
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
        del bpy.types.Scene.my_directories


#Checks if the addon is enabled in the user preferences
if __name__ == "__main__":
    register()
