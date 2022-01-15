import math
import mouse

height = 17
width = 15
middle_start_y = math.floor(height/4)
middle_start_x = math.floor(width/4)
map = []

for i in range(0, height):
    list = []
    for j in range(0, width):
        if ((middle_start_x - 1) < j < (width - middle_start_x)) & ((middle_start_y - 2) < i < (height + 1) - middle_start_y):
            list.append(1)
        else: list.append(0)
    map.append(list)
map[math.floor(height/2)][math.floor(width/2)] = 2
print(math.floor((height)/2))
for line in map:
    print(line)

m = mouse.Mouse(width/2, height/2)
tuple1 = (2,3)
tuple2 = (1,1)
print(tuple1[0] - tuple2[0])
    