from PIL import Image
import numpy as np
from os.path import realpath
import os
import uuid


def brightness_rep(im_nparray, y_seq=5, x_seg=5):
    height, width, *_ = im_nparray.shape
    new_pic = []
    for y in range(0, height, y_seq):
        row = []
        for x in range(0, width, x_seg):
            seg = im_nparray[y:y + y_seq, x:x + x_seg]
            brightness = get_brightness(seg)
            row.append(brightness)
        else:
            new_pic.append(row)

    return new_pic


def get_brightness(seg):
    y, x, z = seg.shape
    seg = seg.reshape(x * y, z)
    R, G, B = np.mean(seg, axis=0)
    Y = (2 * R + B + 3 * G) / 6
    return Y


def convert(file, grid_size=(4, 3)):
    '''

    :param file:
    :param grid_size: (y, x)
    :return:
    '''

    image = np.array(Image.open(file, 'r'))

    tile_files = reversed(['0.png', '1.png', '2.png', '3.png', '4.png', '5.png'])
    #image_files = reversed(['1.png', '2.png', '3.png', '4.png', '5.png', '6.png'])
    tiles = [Image.open('fingers/' + name) for name in tile_files]

    new_pic = brightness_rep(image, *grid_size)
    new_pic = np.array(new_pic, dtype=np.uint8)  # to int

    min = np.amin(new_pic)
    max = np.amax(new_pic)
    t_range = (max - min) / (len(tiles)-1) - 1
    new_pic = (new_pic - min) // t_range


    i_width, i_height = tiles[0].size
    n_height, n_width = new_pic.shape

    total_width = i_width * n_width
    max_height = i_height * n_height

    new_im = Image.new('RGB', (total_width, max_height))

    y_offset = 0
    for row in new_pic:
        x_offset = 0
        for entry in row:
            new_im.paste(tiles[int(entry)], (x_offset, y_offset))
            x_offset += i_width
        y_offset += i_height

    new_im.thumbnail((2160, 3840), Image.ANTIALIAS)
    if not os.path.exists('static/converted'):
            os.makedirs('static/converted')
    filename = f'static/converted/{str(uuid.uuid4())}.jpg'
    
    new_im.save(realpath(filename))
    # new_im.show()
    return filename


if __name__ == '__main__':
    convert('donut.jpg', (4, 3))


