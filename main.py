from PIL import Image
import numpy as np


grid_size = 2

im = Image.open('tom.jpg', 'r')
width, height = im.size
pixel_values = list(im.getdata())


new_pic = []
for y in range(0, height, grid_size):
    row = []
    for x in range(0, width, grid_size):
        tile = []
        for i in range(y, y+grid_size):
            tile.extend(pixel_values[(i*width+x):(i*width+x+grid_size)])

        tile = np.array(tile)
        tile = np.mean(tile, axis=0)
        R, G, B = tile
        Y = (2*R + B + 3*G) / 6
        row.append(Y)

    new_pic.append(row)

new_pic = np.array(new_pic, dtype=np.uint8)

min = np.amin(new_pic)
max = np.amax(new_pic)
range = (max - min) / 5 + 1

new_pic = (new_pic - min) // range

image_files = reversed(['0.png', '2.png', '3.png', '4.png', '5.png'])
images = [Image.open(name) for name in image_files]

i_width, i_height = images[0].size
n_height, n_width = new_pic.shape


total_width = i_width * n_width
max_height = i_height * n_height

new_im = Image.new('RGB', (total_width, max_height))

y_offset = 0
for row in new_pic:
    x_offset = 0
    for entry in row:
        new_im.paste(images[int(entry)], (x_offset, y_offset))
        x_offset += i_width
    y_offset += i_height

new_im.show()



