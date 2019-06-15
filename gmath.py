import math
from display import *
from draw import *

  # IMPORANT NOTE

  # Ambient light is represented by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represented as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 8

def get_lighting(normal, view, ambient, symbols, reflect ):
    #light_sources is a list of all the lighting sources in symbols
    light_sources = []
    for symbol in symbols:
        if symbols[symbol][0] == 'light':
            light_sources.append(symbols[symbol][1])   

    n = normal[:]
    normalize(n)
    for l in light_sources:
	normalize(l['location'])
    normalize(view)
    r = symbols[reflect][1]

    a = calculate_ambient(ambient, r)
    d = calculate_diffuse(light_sources, r, n)
    s = calculate_specular(light_sources, r, view, n)

    i = [0, 0, 0]
    i[RED] = int(a[RED] + d[RED] + s[RED])
    i[GREEN] = int(a[GREEN] + d[GREEN] + s[GREEN])
    i[BLUE] = int(a[BLUE] + d[BLUE] + s[BLUE])
    limit_color(i)

    return i

def calculate_ambient(alight, reflect):
    a = [0, 0, 0]
    a[RED] = alight[RED] * reflect['red'][AMBIENT]
    a[GREEN] = alight[GREEN] * reflect['green'][AMBIENT]
    a[BLUE] = alight[BLUE] * reflect['blue'][AMBIENT]
    return a

def calculate_diffuse(light_sources, reflect, normal):
    d = [0, 0, 0]
    dot = 0
    for light in light_sources:
        dot += dot_product( light['location'], normal)

        dot += dot if dot > 0 else 0
        d[RED] += (light['color'][RED] * reflect['red'][DIFFUSE] * dot) / len(light_sources)
        d[GREEN] += (light['color'][GREEN] * reflect['green'][DIFFUSE] * dot) / len(light_sources)
        d[BLUE] += (light['color'][BLUE] * reflect['blue'][DIFFUSE] * dot) / len(light_sources)
    return d

def calculate_specular(light_sources, reflect, view, normal):
    s = [0, 0, 0]
    n = [0, 0, 0]
    for light in light_sources:
        result = 2 * dot_product(light['location'], normal)
        n[0] = (normal[0] * result) - light['location'][0]
        n[1] = (normal[1] * result) - light['location'][1]
        n[2] = (normal[2] * result) - light['location'][2]

        result = dot_product(n, view)
        result = result if result > 0 else 0
        result = pow( result, SPECULAR_EXP )

        s[RED] += (light['color'][RED] * reflect['red'][SPECULAR] * result) / len(light_sources)
        s[GREEN] += (light['color'][GREEN] * reflect['green'][SPECULAR] * result) / len(light_sources)
        s[BLUE] += (light['color'][BLUE] * reflect['blue'][SPECULAR] * result) / len(light_sources)
    return s

#color limited at 245 rather than 255 for aesthetic reasons
def limit_color(color):
    color[RED] = 245 if color[RED] > 245 else color[RED]
    color[GREEN] = 245 if color[GREEN] > 245 else color[GREEN]
    color[BLUE] = 245 if color[BLUE] > 245 else color[BLUE]
    color[RED] = 15 if color[RED] < 15 else color[RED]
    color[GREEN] = 15 if color[GREEN] < 15 else color[GREEN]
    color[BLUE] = 15 if color[BLUE] < 15 else color[BLUE]

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        if magnitude != 0:
            vector[i] = vector[i] / magnitude
        else:
            vector[i] = 0

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
