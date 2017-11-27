from PIL import Image, ImageDraw
import random
import math

def generate_base_map(grid_size, img_size):
    offset = math.floor(img_size[0]*0.1)
    step = math.floor((img_size[0]-(offset*2))/grid_size)
    max_random = math.floor(step*0.4)
    nodes = []
    edges = []
    for x in range(grid_size+1):
        nodes_line = []
        for y in range(grid_size+1):
            random_y = random.randint(-max_random, max_random) + offset
            random_x = random.randint(-max_random, max_random) + offset
            node = tuple([((x*step)+random_x), ((y*step) + random_y)])
            nodes_line.append(node)
        nodes.append(nodes_line)

    for l_index, line in enumerate(nodes):
        for n_index, node in enumerate(line):
            if not node == line[-1]:
                edges.append([node, line[n_index+1]])
            if not line == nodes[-1]:
                edges.append([node, nodes[l_index+1][n_index]])
    return tuple(edges)


edges = generate_base_map(5, (800, 800))
img = Image.new('RGB', (800, 800), (65, 152, 10))
draw = ImageDraw.Draw(img)
for edge in edges:
    draw.line(edge, fill=(238, 182, 70), width=5)
hs = 30
rotations = ((-hs, -hs), (hs, -hs), (-hs, hs), (hs, hs))
for i in range(100):
    x = random.randint(80, 720)
    y = random.randint(80, 720)
    pixel = img.getpixel((x, y))
    if not pixel == (238, 182, 70):
        add_x = 10 + random.randint(0, 20)
        add_y = 10 + random.randint(0, 20)
        draw.rectangle([(x, y), (x+add_x, y+add_y)], fill=(91, 70, 17))

img.save("test.bmp")
