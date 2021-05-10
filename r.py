import os, Metashape
print("Script is running")

#sets doc object
doc = Metashape.app.document #sets doc object
# doc.save(path = "C:\Research\Reconstruction\project.psx")

#adds a chunk
# chunk = doc.addChunk()
# print(type(doc))
# print(type(chunk))

doc.chunk.importVideo("D:/Research/Research Demo/video.mp4", "D:/Research/Research Demo/Images/frame{filenum}.png", custom_frame_step=10)
chunk = doc.chunk
#asks for directory of images
#path_photos = Metashape.app.getExistingDirectory("images folder:")
# path_photos = "C:/Research/Reconstruction/Corner_tests/threefps"
# print(path_photos)
# image_list = os.listdir(path_photos)
# photo_list = list()

#adds photos to chunk
# for photo in image_list:
#     if photo.rsplit(".",1)[1].lower() in  ["jpg", "jpeg", "tif", "tiff", "png"]:
#         	photo_list.append("/".join([path_photos, photo]))
# chunk.addPhotos(photo_list)

#estimates image quality and removes images under 0.5 quality
chunk.analyzePhotos()
for camera in chunk.cameras:
    if float(camera.meta["Image/Quality"]) < 0.5:
        camera.enabled = False

#goes through reconstruction workflow
chunk.matchPhotos(downscale = 1, generic_preselection= True, reference_preselection= False)
chunk.alignCameras()
chunk.buildDepthMaps(downscale=4, filter_mode=Metashape.AggressiveFiltering)
chunk.buildDenseCloud()
chunk.buildModel(surface_type=Metashape.Arbitrary, interpolation=Metashape.Extrapolated)
# chunk.buildUV(mapping_mode=Metashape.GenericMapping)
# chunk.buildTexture(blending_mode=Metashape.MosaicBlending, texture_size=4096)

#decimates model under a certain facecount
i = 1
print("There are " + str(len(chunk.model.faces)) + " faces in the original model")
while i > 0:
    faceCount = len(chunk.model.faces)
    if faceCount > 2000000:
        target = int(.75 * faceCount)
        chunk.decimateModel(face_count = target, apply_to_selection=False)
        print(i)
        i += 1
    else:
        i = 0
        print("Did not decimate/stopped decimating")
print("Now there are " + str(len(chunk.model.faces)) + " faces")

#adds a texture to the model
chunk.buildUV(mapping_mode=Metashape.GenericMapping)
chunk.buildTexture(blending_mode=Metashape.MosaicBlending, texture_size=4096)

#exports the model and saves the project
chunk.exportModel(path = "D:\Research\Research Demo\model.fbx", format = Metashape.ModelFormat.ModelFormatFBX)
doc.save(path = "D:\Research\Research Demo\project.psx")