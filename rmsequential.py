import os
from os.path import isfile, join
from wand.image import Image

def rmsequential(image_dir, fuzz):
    """
    Removes sequential duplicates of images in a directory. Sequence is determined by sort()
    performed on the filenames.

    image-dir -- The directory containing the images
    fuzz -- The ImageMagick fuzziness value; the fuzzier, the more it disregards minor differences
    """
    image_names = [file for file in os.listdir(image_dir) if isfile(join(image_dir, file))]
    image_names.sort()
    image_names.reverse() #if the images are numbered, this will put the lower numbers at the end
    all_images = image_names.copy() #we'll use this later when we start deleting files

    unique = [] #this will be full of file names

    #select first image
    filename = image_names.pop()
    key_image = {
        "img": Image(filename=join(image_dir, filename)),
        "name": filename
    }
    key_image["img"].fuzz = key_image["img"].quantum_range * fuzz

    while len(image_names) > 0:
        filename = image_names.pop()
        analyze_me = {
            "img": Image(filename=join(image_dir, filename)),
            "name": filename
        }

        print("Comparing", key_image["name"], "to", analyze_me["name"])
        #corporate wants you to find the difference between this picture and this picture
        if key_image["img"].compare(analyze_me["img"], metric="absolute")[1] > 0.0: 
            #if they're not the same picture
            #put key_image in unique; make analyze_me the new key_image
            unique.append(key_image["name"])
            key_image = analyze_me
            key_image["img"].fuzz = key_image["img"].quantum_range * fuzz
    unique.append(key_image["name"])

    print(">>>Starting deletion of similar files")
    for filename in all_images:
        if filename not in unique:
            print("removing", filename)
            os.remove(join(image_dir, filename))