#imports main modules
import bpy
import os

#returns the joined path the directory and the files
def process_files(context, directory, files):
    import os
    for file in files:
        path = os.path.join(directory, file.name)
        print("process %s" % path)
        #add function here
    return {'FINISHED'}

#imports various functions from modules
from bpy.props import StringProperty, BoolProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, OperatorFileListElement

#-------------------------------------------------------------------------------
# Defines the UI panel
#-------------------------------------------------------------------------------

class ImageSeqConverter(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    #panel properties
    bl_label = "Output"
    bl_idname = "IMG_PT_CONVERT"
    bl_space_type = 'PROPERTIES'
    bl_region_type = "WINDOW"
    bl_context = "output"
        

    #defines UI creating
    def draw(self, context):
        layout = self.layout

        #text and icon
        row = layout.row()
        row.label(text="Convert Image Sequence", icon='IMAGE_DATA')
        row = layout.row()  
        #button (placeholder)
        row.scale_y = 3.0
        row.operator("file.open_filebrowser", text= "Import Images")
        
#-------------------------------------------------------------------------------
# Defines The file browser operator
#-------------------------------------------------------------------------------       
        
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
    files = CollectionProperty(
        name="BVH files",
        type=OperatorFileListElement,
        )

    #string of the path directory
    directory = StringProperty(subtype='DIR_PATH')
    
    #activates function up top to return the full directory
    def execute(self, context):
        return process_files(context, self.directory, self.files)
    
    

"""    def execute(self, context):
        Do something with the selected file(s)
        filename, extension = os.path.splitext(self.filepath)
        
        print('Selected file:', self.filepath)
        print('File name:', filename)
        print('File extension:', extension)
        print('Some Boolean:', self.some_boolean)
        
        return {'FINISHED'}"""
        


#Register and unregister class to allow for module to be imported
def register():
    bpy.utils.register_class(ImageSeqConverter)
    bpy.utils.register_class(OpenFileBrowser)
    #bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImageSeqConverter)
    bpy.utils.unregister_class(OpenFileBrowser)
    #bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
