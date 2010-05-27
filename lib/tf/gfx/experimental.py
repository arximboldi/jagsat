#
#  Copyright (C) 2009 TribleFlame Oy
#  
#  This file is part of TF.
#  
#  TF is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  TF is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from PySFML import sf


def blend(c1, c2):
    a1 = (255 - c2.a) / 255.0

    r1 = c1.r * a1
    g1 = c1.g * a1
    b1 = c1.b * a1

    a2 = c2.a / 255.0
    r2 = c2.r * a2
    g2 = c2.g * a2
    b2 = c2.b * a2

    r = r1 + r2
    g = g1 + g2
    b = b1 + b2

    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255

    return sf.Color(r, g, b)


def blit(fromimage, srcx, srcy, width, height,
         toimage, destx, desty):
    """Stupid blit function, because SFML does not support it?"""
    toimageheight = toimage.GetHeight()
    toimagewidth = toimage.GetWidth()
    for y in range(height):
        ty = desty + y
        if ty < 0 or ty >= toimageheight:
            continue
        for x in range(width):
            tx = destx + x
            if tx >= toimagewidth \
                   or tx < 0:
                continue
            c1 = toimage.GetPixel(tx, ty)
            c2 = fromimage.GetPixel(x, y)
            blendcolor = blend(c1, c2)
            toimage.SetPixel(tx, ty, blendcolor)
