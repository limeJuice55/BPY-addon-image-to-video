import bpy


class ImageSeqConverter(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Image Sequence Converter"
    bl_idname = "IMG_PT_CONVERT"
    bl_space_type = 'PROPERTIES'
    bl_region_type = "WINDOW"
    bl_context = "render"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Convert Image Sequence to Video", icon='IMAGE_DATA')

        row = layout.row()
    #    row.operator("images.import_sequence")



#class ImportImages(bpy.types.operator):
#    bl_label = "Import Images"
#    bl_idname = "images.import_sequence"
#    
#    def execute(self, context):
#        
#        return("Testing Placeholder")

        row.scale_y = 3.0
        row.operator("object.load_reference_image")



def register():
    bpy.utils.register_class(ImageSeqConverter)
    #bpy.utils.register_class(ImportImages)


def unregister():
    bpy.utils.unregister_class(ImageSeqConverter)
    #bpy.utils.unregister_class(ImportImages)


if __name__ == "__main__":
    register()
