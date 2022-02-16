import bpy


class ImageSeqConverter(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Image Sequence Converter"
    bl_idname = "IMG_PT_CONVERT"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Convert Image Sequence to Video", icon='IMAGE_DATA')

        row = layout.row()
        row.operator("mesh.primitive_cube_add")


def register():
    bpy.utils.register_class(ImageSeqConverter)


def unregister():
    bpy.utils.unregister_class(ImageSeqConverter)


if __name__ == "__main__":
    register()
