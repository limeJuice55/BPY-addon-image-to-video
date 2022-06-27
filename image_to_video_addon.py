#imports main modules
import bpy
import os

#returns the joined path the directory and the files

#imports various functions from modules
from bpy.props import StringProperty, BoolProperty, CollectionProperty

# This class contains the two directories to be used:
# the input directory with the individual images,
# and the output directory for the final product.

class myProperties(bpy.types.PropertyGroup):
    
    input_directory : StringProperty(name="", subtype="DIR_PATH")
    output_directory : StringProperty(name="", subtype="FILE_PATH")
    
#----------------------
# This is the class for the UI.
#----------------------

class UIPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    #panel name, ID's and location
    bl_label = "Output"
    bl_idname = "IMG_PT_CONVERT"
    bl_space_type = 'PROPERTIES'
    bl_region_type = "WINDOW"
    bl_context = "output"
    
        
    #Creates the UI
    def draw(self, context):
        layout = self.layout
        mydirectories = context.scene.my_directories
        
        #input and output directory
        layout.prop(mydirectories, "input_directory")
        row = layout.row
        layout.prop(mydirectories, "output_directory")
        #text and icon
        row = layout.row()
        row.label(text="Convert Image Sequence", icon='IMAGE_DATA')
        row = layout.row()
        #button that calls the file browser
        row.scale_y = 2.0
        row.operator("file.open_filebrowser", text= "Begin Conversion")
        
#------------------------------------------------------------
# This is the command called upon pressing "BEGIN CONVERSION"
#------------------------------------------------------------
class OpenFileBrowser(bpy.types.Operator):
    #properties
    bl_idname = "file.open_filebrowser"
    bl_label = "Open the file browser"
    
    #executes the conversion
    def execute(self, context):
        #begins by pulling the files from the input directory
        mydirectories = context.scene.my_directories
        directory = bpy.path.abspath(mydirectories.input_directory)
        files = os.listdir(directory)
        
        #print debugs
        print(directory)        
        print(files)
        
        #this creates the shorthands that are used later in the code
        scenes = bpy.context.scene
        seqs = scenes.sequence_editor.sequences
        
        j = 0
        
        #this loop adds one new image one frame after another
        for i in files:
            j += 1
            seqs.new_image("image" + str(j), directory + i, 1, j)
            #debug
            print(i)
        
        #groups the images together
        bpy.ops.sequencer.meta_make()
        
        #resets the frames    
        scenes.frame_start = 0
        scenes.frame_end = j
        
        scenes.render.filepath = bpy.path.abspath(mydirectories.output_directory)
       
        #activates the render sequence
        bpy.ops.render.render(
            animation=True, 
            write_still=False, 
            use_viewport=False, 
        )
        
        return {'FINISHED'}

        

classes = [myProperties, UIPanel, OpenFileBrowser]


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
