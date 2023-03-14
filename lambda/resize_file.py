from PIL import Image

def resize_image(path, output_location, height=500): 
    img = Image.open(path)
    aspect_ratio = float(img.height)/float(img.width)
    width = height/aspect_ratio
    img.thumbnail((width, height))
    img.save(output_location)

output_location = "C:/aravind/serviceapp/imgs_to_test/333.JPG"
img_path = "C:/aravind/serviceapp/imgs_to_test/IMG_3357.JPG"
resize_image(img_path, output_location, 500)
