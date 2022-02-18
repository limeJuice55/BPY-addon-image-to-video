import bpy

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
        row.operator("object.load_reference_image", text= "Import Images")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("render.render", text= "Render")
        row = layout.row()
        


#Register and unregister class to allow for module to be imported
def register():
    bpy.utils.register_class(ImageSeqConverter)


def unregister():
    bpy.utils.unregister_class(ImageSeqConverter)


if __name__ == "__main__":
    register()