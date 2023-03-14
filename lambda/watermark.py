from PIL import Image

def resize_and_add_watermark(input_image_path, output_image_path, watermark_image_path, height=500):
    #Resize the file
    base_image = Image.open(input_image_path)
    aspect_ratio = float(base_image.height)/float(base_image.width)
    width = height/aspect_ratio
    base_image.thumbnail((width, height))
    #base_image.save(output_location) # To save the resized image

    #Add Watermark
    TRANSPARENCY = 30
    angle = 30
    w_img, h_img = base_image.size
    basewidth = w_img
    watermark = Image.open(watermark_image_path)
    watermark = watermark.rotate(angle, expand=True)
    wpercent = (basewidth / float(watermark.size[0]))
    hpercent = h_img / float(watermark.size[1])
    if wpercent < hpercent:
        hsize = int((float(watermark.size[1]) * float(wpercent)))
        watermark = watermark.resize((basewidth, hsize), Image.ANTIALIAS)
    else:
        wsize = int((float(watermark.size[0]) * float(hpercent)))
        watermark = watermark.resize((wsize, h_img), Image.ANTIALIAS)
    w_logo, h_logo = watermark.size
    center_y = int(h_img / 2)
    center_x = int(w_img / 2)
    top_y = center_y - int(h_logo / 2)
    left_x = center_x - int(w_logo / 2)
    if watermark.mode != 'RGBA':
        alpha = Image.new('L', (w_img, h_img), 255)
        watermark.putalpha(alpha)
    paste_mask = watermark.split()[3].point(lambda i: i * TRANSPARENCY / 100.)
    base_image.paste(watermark, (left_x, top_y), mask=paste_mask)
    base_image.save(output_image_path)

import time
start_time = time.time()
location = "C:/aravind/serviceapp/imgs_to_test/IMG_3357.JPG"
location_op = "C:/aravind/serviceapp/imgs_to_test/1001.JPG"
watermark = "C:/aravind/serviceapp/Service-App-BackEnd/static/lambda/watermark.png"
resize_and_add_watermark(location, location_op, watermark,1000)
print("Took {} seconds".format(time.time() - start_time))
