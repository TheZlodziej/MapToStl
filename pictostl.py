from PIL import Image

def get_pixels(img_path): #returns set of image width, height, sets of each individual pixel rgb[a] value
    try:
        img = Image.open(img_path, 'r')
        w,h = img.size
        filename = img.filename
        pixels = list(img.getdata())
        return (filename, w, h, pixels)
    except:
        print("there was an error with your file.")
        return None

def get_idx(x,y, max_x):
    return y*max_x+x

def get_z(color):
    r = color[0]
    g = color[1]
    b = color[2]
    m = 0.04
    return m * r*(1+g) / (b+1)

def gen_mesh(w, h, pixels): #returns array of tuples of tuples of triangle's vertex coords [ ( (x,y,z), (...), (...) ) ]
    scale=100
    width=300
    ret = []
    for y in range(h):
        for x in range(w):
            if x != w-1 and y != h-1:
                c1 = pixels[get_idx(x,y,w)]
                c2 = pixels[get_idx(x+1,y,w)]
                c3 = pixels[get_idx(x,y+1,w)]
                ret.append( ( (x*scale, y*scale, get_z(c1)*scale), ((x+1)*scale, y*scale, get_z(c2)*scale), (x*scale, (y+1)*scale, get_z(c3)*scale) ) )
                ret.append( ( (x*scale, y*scale, get_z(c1)*scale - width), ((x+1)*scale, y*scale, get_z(c2)*scale - width), (x*scale, (y+1)*scale, get_z(c3)*scale - width) ) )
                if x == 0:
                    ret.append( ( (x*scale,y*scale,get_z(c1)*scale), (x*scale,y*scale,get_z(c1)*scale-width), (x*scale, (y+1)*scale, get_z(c3)*scale) ) )
                    ret.append( ( (x*scale,(y+1)*scale,get_z(c3)*scale), (x*scale, y*scale, get_z(c1)*scale-width), (x*scale, (y+1)*scale, get_z(c3)*scale-width) ) )
                if y == 0:
                    ret.append( ( (x*scale,y*scale,get_z(c1)*scale), (x*scale,y*scale,get_z(c1)*scale-width), ((x+1)*scale,y*scale,get_z(c2)*scale) ) )
                    ret.append( ( (x*scale,y*scale, get_z(c1)*scale-width ), ((x+1)*scale, y*scale, get_z(c2)*scale-width), ((x+1)*scale, y*scale, get_z(c2)*scale) ) )

            if x != 0 and y != 0:
                c1 = pixels[get_idx(x,y,w)]
                c2 = pixels[get_idx(x-1,y,w)]
                c3 = pixels[get_idx(x,y-1,w)]
                ret.append( ( (x*scale, y*scale, get_z(c1)*scale), ((x-1)*scale, y*scale, get_z(c2)*scale), (x*scale, (y-1)*scale, get_z(c3)*scale) ) )
                ret.append( ( (x*scale, y*scale, get_z(c1)*scale - width), ((x-1)*scale, y*scale, get_z(c2)*scale - width), (x*scale, (y-1)*scale, get_z(c3)*scale - width) ) )
                if x == w-1:
                    ret.append( ( (x*scale,y*scale,get_z(c1)*scale), (x*scale,y*scale,get_z(c1)*scale-width), (x*scale, (y-1)*scale, get_z(c3)*scale) ) )
                    ret.append( ( (x*scale,(y-1)*scale,get_z(c3)*scale), (x*scale, y*scale, get_z(c1)*scale-width), (x*scale, (y-1)*scale, get_z(c3)*scale-width) ) )
                if y == h-1:
                    ret.append( ( (x*scale,y*scale,get_z(c1)*scale), (x*scale,y*scale,get_z(c1)*scale-width), ((x-1)*scale,y*scale,get_z(c2)*scale) ) )
                    ret.append( ( (x*scale,y*scale, get_z(c1)*scale-width ), ((x-1)*scale, y*scale, get_z(c2)*scale-width), ((x-1)*scale, y*scale, get_z(c2)*scale) ) )
    return ret

def gen_stl_file():
    path = str(input("enter file path: "))
    img = get_pixels(path)
    if not img:
        return
    print("picture successfully loaded.")
    filename = img[0]
    w = img[1]
    h = img[2]
    pixels = img[3]

    mesh = gen_mesh(w, h, pixels)
    stl = open(filename+".stl", 'w')
    stl.write("solid 3dmap\n")
    for facet in mesh:
        stl.write("\tfacet normal 0 0 1\n\t\touter loop\n")
        for vertex in facet:
            x = str(vertex[0])
            y = str(vertex[1])
            z = str(vertex[2])
            stl.write("\t\t\tvertex " + x + " " + y + " " + z + "\n")
        stl.write("\t\tendloop\n\tendfacet\n")

    stl.write("endsolid 3dmap")
    stl.close()
    print("done!")

def main():
    gen_stl_file()

if __name__ == '__main__':
    main()
