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

#shorthands for commonly used code
scene = bpy.context.scene
editor = scene.sequence_editor
seq = editor.sequences
win = bpy.context.window_manager

#clears the sequence editor
def clear_sequence():
    for strip in seq:
        seq.remove(strip)
        
    return {'FINISHED'}

#resets the frames & adjusts video length 
def adjust_video_length(length):
    scene.frame_start = 0
    scene.frame_end = length
    
    return {'FINISHED'}

#adds the image strip and determines its length
def add_image_strip(directory, files):
    j = 0
    for i in files:
        j += 1
        seq.new_image("image" + str(j), directory + i, 1, j)
        #debug
        print("imported image: " + str(i))
    bpy.ops.sequencer.meta_make()
    
    return j

def adjust_resolution(x, y):
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    
    return {"FINISHED"}




#-----------------------------------------------
# Class of properties to be referenced elsewhere
#-----------------------------------------------

class myProperties(bpy.types.PropertyGroup):
    
    output_directory : StringProperty(name="Output", subtype="FILE_PATH", description="Destination for your Video")
    
    manual_res : BoolProperty(name="Manually Adjust Resolution")
    res_x : IntProperty(name="X Resolution", default=scene.render.resolution_x)
    res_y : IntProperty(name="Y Resolution", default=scene.render.resolution_y)
    
#---------------------------------------
# Class which defines the User Interface
#---------------------------------------

class UIPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
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
        
        if mydirectories.manual_res == True:
            layout.prop(mydirectories, "res_x")
            layout.prop(mydirectories, "res_y")
        
        #text and icon
        row = layout.row()
        row.label(text="Convert Image Sequence to Video", icon='IMAGE_DATA')
        row = layout.row()
        #button that calls the file browser
        row.scale_y = 2.0
        row.operator("import_test.some_data", text= "Convert Image to Video")
        
#------------------------------------------------------------
# Class which converts the image sequence to video
#------------------------------------------------------------
    
class ImportSomeData(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Some Data"

    # ImportHelper mixin class uses this
    filename_ext = ".png"

    filter_glob: StringProperty(
            default="*.png",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    files: CollectionProperty(
        name="BVH files",
        type=OperatorFileListElement,
        )

    directory: StringProperty(subtype='DIR_PATH', options={'HIDDEN'})

    def execute(self, context):
        
        fileList = []
        
        for file in self.files:
            filepath = file.name
            print(filepath)
            fileList.append(file.name)
            
        print(fileList)
        print(self.directory)
        
        mydirectories = scene.my_directories
        
        clear_sequence()
        
        video_length = add_image_strip(self.directory, fileList)

        adjust_video_length(video_length)
        
        scene.render.filepath = bpy.path.abspath(mydirectories.output_directory)
        
        old_x = scene.render.resolution_x
        old_y = scene.render.resolution_y
        
        if mydirectories.manual_res == True:
            adjust_resolution(mydirectories.res_x, mydirectories.res_y)
        
        #initiates export
        
#        win.progress_update(50)
        
        
        bpy.ops.render.render(animation=True, write_still=False, use_viewport=False)
        
#        win.progress_update(99)
        
        clear_sequence()
        
        adjust_resolution(old_x, old_y)
        
        return {'FINISHED'}

 
classes = [myProperties, UIPanel, ImportSomeData]

#Register and unregister class to allow for module to be imported
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
        bpy.types.Scene.my_directories = bpy.props.PointerProperty(type=myProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
        del bpy.types.Scene.my_directories


#Checks if the addon is enabled in the user preferences
if __name__ == "__main__":
    register()
