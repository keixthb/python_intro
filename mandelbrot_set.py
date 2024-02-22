from PIL import Image
import colorsys
import math
import time
from mpi4py import MPI

WIDTH_OF_IMAGE_IN_PIXELS, HEIGHT_OF_IMAGE_IN_PIXELS = 2532, 1170

RZF = 1 / 1000000000000
MAX_NUMBER_OF_IMAGES_TO_GENERATE = 6000
MAX_NUMBER_OF_ITERATIONS = 2500

def mandelbrot(x, y, minx, maxx, miny, maxy, R):
    px, py = -0.7746806106269039, -0.1374168856037867

    zx = 0
    zy = 0

    RX1, RX2, RY1, RY2 = px - (R / 2), px + (R / 2), py - (R / 2), py + (R / 2)

    cx = ((x - minx) / (maxx - minx)) * (RX2 - RX1) + RX1
    cy = ((y - miny) / (maxy - miny)) * (RY2 - RY1) + RY1

    number_of_iterations_to_solution = 2500

    for i in range(MAX_NUMBER_OF_ITERATIONS):
        break_condition = ((zx ** 2) + (zy ** 2)) > 4

        if(break_condition):
            number_of_iterations_to_solution = i
            break

        temp = (zx ** 2) - (zy ** 2)
        zy = (2 * zx * zy) + cy
        zx = temp + cx

    return number_of_iterations_to_solution

def gen_mandelbrot_image(image_number, mfactor, R):

    bitmap = Image.new("RGB", (WIDTH_OF_IMAGE_IN_PIXELS, HEIGHT_OF_IMAGE_IN_PIXELS), "white")
    pix = bitmap.load()

    for x in range(WIDTH_OF_IMAGE_IN_PIXELS):
        for y in range(HEIGHT_OF_IMAGE_IN_PIXELS):

            c = mandelbrot(x, y, 0, WIDTH_OF_IMAGE_IN_PIXELS - 1, 0, HEIGHT_OF_IMAGE_IN_PIXELS - 1, R)

            v = (c ** mfactor) / (MAX_NUMBER_OF_ITERATIONS ** mfactor)

            hv = 0.67 - v

            if(hv < 0):
                hv += 1

            r, g, b = colorsys.hsv_to_rgb(hv, 1, 1 - ((v - 0.1) ** 2) / (0.9 ** 2))

            r = min(255,round(r * 255))
            g = min(255,round(g * 255))
            b = min(255,round(b * 255))

            pix[x, y] = int(r) + (int(g) << 8) + (int(b) << 16)

    bitmap.save(f"{image_number}.png")


def split_list(data):
    return data[MPI.COMM_WORLD.Get_rank():MAX_NUMBER_OF_IMAGES_TO_GENERATE:MPI.COMM_WORLD.Get_size()]



if("__main__" == __name__):

    r_values = [3 * 0.975 ** i for i in range(MAX_NUMBER_OF_IMAGES_TO_GENERATE)]

    m_factors = [0.5 + (1e-12 ** 0.1) / (r_value ** 0.1) for r_value in r_values]

    indicies = [i for i in range(MAX_NUMBER_OF_IMAGES_TO_GENERATE)]


    local_rvalues = split_list(r_values)

    local_mfactors = split_list(m_factors)

    local_indicies = split_list(indicies)

    for index, m_factor, rvalue in zip(local_indicies, local_mfactors, local_rvalues):
        print(f"gen_mandelbrot_image({index}, {m_factor}, {rvalue})")
        gen_mandelbrot_image(index, m_factor, rvalue)
