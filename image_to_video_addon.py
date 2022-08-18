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
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, OperatorFileListElement

#clears the sequence editor
def clear_sequence(seq):
    for strip in seq:
        seq.remove(strip)
        

#used to manually adjust resolution. Only used if manual_res == True
def adjust_resolution(scene, x, y):
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    

#sets the video length
def adjust_frames(scene, start, end):
    scene.frame_start = start
    scene.frame_end = end
    
    
#converts the imported files to a standard array
def create_file_list(files):
    fileList = []
    for file in files:
        fileList.append(file.name)

    return fileList


#creates each frame in the sequencer and returns the length of the video
def create_frames(seq, fileList, directory):
    j = 0
    for i in fileList:
        j += 1
        seq.new_image("image" + str(j), directory + i, 1, j)
        #debug
        print("imported image: " + str(i))
        
    return j

def set_file_format(scene, formatID):
    if formatID == "MP4":
        scene.render.ffmpeg.format = 'MPEG4'
    elif formatID == "AVI":
        scene.render.ffmpeg.format = 'AVI'
    elif formatID == "QUICK":
        scene.render.ffmpeg.format = "QUICKTIME"
    else:
        scene.render.ffmpeg.format = "MKV"
    print("Set Format Container to: " + formatID)

#-----------------------------------------------
# Class of properties to be referenced elsewhere
#-----------------------------------------------

class MyProperties(bpy.types.PropertyGroup):
    
    outputDirectory : StringProperty(name="Output", subtype="FILE_PATH", description="The location of your final video within your computer's files")
    
    #resolution settings
    manualRes : BoolProperty(name="Manually Adjust Resolution", description="Allows you to change the resolution of your video. Default is 1920 x 1080")
    resX : IntProperty(name="X Res", default=1920, description="x-value for your adjusted resolution. Does not apply if Manually Adjust Input is not checked")
    resY : IntProperty(name="Y Res", default=1080, description="y-value for your adjusted resolution. Does not apply if Manually Adjust Input is not checked")
    
    #frame settings
    manualFrames : BoolProperty(name="Manually Adjust Frames", description="Allows you to change the resolution of your video. Default is the number of files imported")
    frameStart : IntProperty(name="Frame Start", default=0, description="The first frame of your video")
    frameEnd : IntProperty(name="Frame End", default=250, description="The last frame of your video")
    
    #determines the output file type
    fileType : EnumProperty(
        name="File Type", 
        description="The file format to be produced",
        items=[("MP4", "mp4", ""),("AVI", "AVI", ""),("QUICK", "Quicktime", ""), ("MKV", "MKV", "")],
        default="MKV"
        )
    
    
#---------------------------------------
# Creates the UI panel
#---------------------------------------

class UIPanel(bpy.types.Panel):
    bl_label = "Image to Video Converter"
    bl_idname = "IMG_PT_CONVERT"
    bl_space_type = 'PROPERTIES'
    bl_region_type = "WINDOW"
    bl_context = "output"
    
        
    #Creates the UI
    def draw(self, context):
        layout = self.layout
        my_properties = context.scene.my_properties
        
        #Output directory
        layout.prop(my_properties, "outputDirectory")
        row = layout.row()
        #checkbox and values for manual resolution cropping
        layout.prop(my_properties, "manualRes")
        
        row = layout.row()
        sub = row.row()
        sub.enabled = my_properties.manualRes
        sub.prop(my_properties, "resX")
        
        row = layout.row()
        sub = row.row()
        sub.enabled = my_properties.manualRes
        sub.prop(my_properties, "resY")
        
        row = layout.row()
        #checkbox and values for manual frame clipping
        layout.prop(my_properties, "manualFrames")
        
        row = layout.row()
        sub = row.row()
        sub.enabled = my_properties.manualFrames
        sub.prop(my_properties, "frameStart")
        
        row = layout.row()
        sub = row.row()
        sub.enabled = my_properties.manualFrames
        sub.prop(my_properties, "frameEnd")
        
        row = layout.row()
        layout.prop(my_properties, "fileType")
        
        #text description
        row = layout.row()
        row.label(text="Convert Image Sequence to Video", icon='IMAGE_DATA')
        row = layout.row()
        #button to initiate conversion
        row.scale_y = 2.0
        row.operator("convert.image_to_video", text= "Import Images and Convert")
        
        row = layout.row()
        row.operator("test.driver", text="Driver test. Check SysConsole")
        
#------------------------------------------------------------
# Operator class - Collects, organises and converts the image files into video
#------------------------------------------------------------
    
class BeginConversion(Operator, ImportHelper):
    bl_idname = "convert.image_to_video"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Files and Convert"
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_description = "Import Images and Convert them to Video."
    
    #filters out unneeded file types
    filterGlob: StringProperty(
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
        
        #shorthand for the properties from myProperties
        my_properties = scene.my_properties
        
        directory = self.directory
        print(directory)
        
        fileList = create_file_list(self.files)
        
        clear_sequence(seq)
            
        videoLength = create_frames(seq, fileList, directory)
            
        #merges the frames into a video
        bpy.ops.sequencer.meta_make()
        
        #caching blender's default render settings
        oldStart = scene.frame_start
        oldEnd = scene.frame_end
        
        oldX = scene.render.resolution_x
        oldY = scene.render.resolution_y
        
        oldType = scene.render.image_settings.file_format
        
        #changes the frame clipping to user-defined values if allowed
        if my_properties.manualFrames == True:
            adjust_frames(scene, my_properties.frameStart, my_properties.frameEnd)
            
        else:
            adjust_frames(scene, 0, videoLength)
            
        print("Frames set to: " + str(scene.frame_start) + ", " + str(scene.frame_end))
        
        oldPath = scene.render.filepath
        
        #sets blender's output path to the user-defined value
        scene.render.filepath = bpy.path.abspath(my_properties.outputDirectory)
        
        #changes the resolution to user-defined values if allowed
        if my_properties.manualRes == True:
            adjust_resolution(scene, my_properties.resX, my_properties.resY)
        
        
        print("Resolution set to: " + str(scene.render.resolution_x) + ", " + str(scene.render.resolution_y))
        
        
        print("Set File Format to: FFMPEG")
        scene.render.image_settings.file_format = 'FFMPEG'
        
        set_file_format(scene, my_properties.fileType)
        
        #activates render
        print("Rendering...") 
        bpy.ops.render.render(animation=True, write_still=False, use_viewport=False)
        
        clear_sequence(seq)
        
        #resets values to before conversion
        adjust_resolution(scene, oldX, oldY)
        
        adjust_frames(scene, oldStart, oldEnd)
        
        scene.render.filepath = oldPath
        
        scene.render.image_settings.file_format = oldType
        
        return {'FINISHED'}


#------------------------------------------------------------------
# Driver class. Sets up alternate context to test functions
#------------------------------------------------------------------
   
class Driver(Operator):
    bl_idname = "test.driver"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Test functions with test data"
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_description = "Tests functions with predetermined data and produces output"
    
    def execute(self, context):
        scene = bpy.context.scene
        seq = scene.sequence_editor.sequences
        
        #stores default scene values
        oldStart = scene.frame_start
        oldEnd = scene.frame_end
        
        #tests the values for adjust_frames
        def driver(start, end):
            try:
                print("Frame values: " + str(start), str(end))
                adjust_frames(scene, start, end)
            except Exception as e:
                print("error has been detected:")
                print(e)
            else:
                print("No errors detected.")
            finally:
                print("resulting frame clips: " + str(scene.frame_start), str(scene.frame_end))
    
        driver(0, 250) # standard frame clips
        driver(1, 1) # same start and end values
        driver(0, 200000000000000000000) # above 64-bit integer
        driver(-50, 250) # negative start
        driver(50, 25) # smaller end clip than start
        driver("0", "250") # incorrect data type
        
        adjust_frames(scene, oldStart, oldEnd) #resets frames
        
        return {'FINISHED'}
            
 
classes = [MyProperties, UIPanel, BeginConversion, Driver]

#activates the addon when enabled in preferences
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.my_properties = bpy.props.PointerProperty(type=MyProperties)

#deactivates the addon when disabled in prefernces
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.my_properties


#Checks if the addon is enabled in the user preferences
if __name__ == "__main__":
    register()
