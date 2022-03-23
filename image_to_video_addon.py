#info to be displayed at addon settings
bl_info = {
    "name" : "Image Sequence Converter",
    "author" : "Liam D'Arcy",
    "version" : (1, 5),
    "blender" : (3, 00, 1),
    "location" : "Properties > output",
    "category" : "Import-Export"
}

#imports main modules
import bpy
import os

#returns the joined path the directory and the files
def process_files(context, dir, fileList):
    import os
#   placeholder
    return {"FINISHED"}

#imports various functions from modules
from bpy.props import StringProperty, BoolProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, OperatorFileListElement

#----------------------
# Defines the UI panel
#----------------------

class UIPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    #panel properties
    bl_label = "Output"
    bl_idname = "IMG_PT_CONVERT"
    bl_space_type = 'PROPERTIES'
    bl_region_type = "WINDOW"
    bl_context = "output"
        
    #defines UI creation
    def draw(self, context):
        layout = self.layout

        #text and icon
        row = layout.row()
        row.label(text="Convert Image Sequence", icon='IMAGE_DATA')
        row = layout.row()  
        #button
        row.scale_y = 3.0
        row.operator("file.open_filebrowser", text= "Import Images")
        
#-----------------------------------
# Defines The file browser operator
#-----------------------------------
        
class OpenFileBrowser(Operator, ImportHelper):
    #properties
    bl_idname = "file.open_filebrowser"
    bl_label = "Open the file browser"
    
    #filters file types
    filter_glob: StringProperty(
        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp',
        options={'HIDDEN'}
    )
    
    #test boolean property
    some_boolean: BoolProperty(
        name='Some Boolean',
        description='Testing',
        default=True,
    )
    
    #creates an array of the different files
    fileList: CollectionProperty(
        name="BVH files",
        type=OperatorFileListElement,
        )

    #string of the path directory
    dir: StringProperty(subtype='DIR_PATH')
    
    #activates function up top to return the full directory
    def execute(self, context):
        return process_files(context, self.dir, self.fileList)

#Register and unregister class to allow for module to be imported
def register():
    bpy.utils.register_class(UIPanel)
    bpy.utils.register_class(OpenFileBrowser)


def unregister():
    bpy.utils.unregister_class(UIPanel)
    bpy.utils.unregister_class(OpenFileBrowser)


#Checks if the addon is enabled in the user preferences
if __name__ == "__main__":
    register()
