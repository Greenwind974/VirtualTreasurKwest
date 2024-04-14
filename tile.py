import pygame
from entite import Entite

import os
class Tile(Entite):
    
    def __init__(self, x, y, width, height, epoque, image, tile_id, tilesetName):
        super().__init__(x, y, width, height, epoque, image)
        self.id = tile_id
        self.name = tilesetName
        dictBloquant = {
            "Arena_Tileset":[86,77,78],
            "castle":[1,200,203,225,228, 2, 3, 4, 6, 8, 10, 11, 13, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 119, 95, 96, 97, 98, 99, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 135, 137, 138, 139, 142, 144, 145, 146, 147, 148, 149,150,151, 156, 157, 162, 163, 164, 167, 169, 170, 171, 172, 173, 174, 201, 202, 204, 207, 209, 221, 222, 223, 224, 226, 227, 229, 230, 248, 249, 271, 272, 273, 274, 278, 279, 283, 284, 285, 296, 297, 298, 299, 301, 302, 303, 304, 308, 309, 310, 321, 322, 323, 324],
            "City Prop Tileset update 2" : [416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 28, 29, 30, 31, 60, 61, 62, 63, 92, 93, 94, 95, 124, 125, 126, 127, 157, 158, 189, 190, 220, 221, 222, 223, 252, 253, 254, 255, 284, 285, 286, 287, 316, 317, 318, 319, 349, 350, 381, 382],
            "Dungeon_Tileset (test)" : [208,224],
            "Forest_Tileset" : [257, 254, 255, 291, 292, 293, 294 ,80, 114, 115, 116, 133, 135,150, 152, 153, 154, 156, 157, 158, 175, 176, 177, 178, 179, 180, 181, 182, 194, 195, 196, 197, 198, 199, 200, 201,215,218, 232, 233, 234, 235, 236, 237, 238, 239, 248, 249, 251, 252, 254, 255, 257, 258, 267, 268, 273, 274, 285, 286, 287, 288, 291, 292, 293, 294, 304, 305, 306, 307, 310, 311, 312, 313],
            "futurtilseset": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            "galletcityptit" : [1372,1373,1374,1375,1376,1436,1437,1438,1439,1440,1500,1501,1502,1503,1504,1564,1565,1566,1567,1568,1628,1629,1630,1631,1632,1692,1693,1694,1695,1696,1675,1676,1677,1678,1679,1739,1740,1741,1742,1743,1803,1804,1805,1806,1807,1867,1868,1869,1870,1871,1931,1932,1933,1934,1935,1995,1996,1997,1998,1999,2059,2060,2061,2062,2063,2123,2124,2125,2126,2127,2187,2188,2189,2190,2191,1954,1955,1956,1957,1958,2018,2019,2020,2021,2022,2082,2083,2084,2085,2086,2146,2147,2148,2149,2150],
            "spritesheetFuturiste": [46,47,60,61,65,168,169]
            }
        """
        if not tilesetName in os.listdir('id_tiles'):
            os.mkdir("id_tiles/{}".format(tilesetName))
        
        if not "{}.png".format(tile_id) in os.listdir("id_tiles/{}".format(tilesetName)):
            pygame.image.save(image,"id_tiles/{}/{}.png".format(tilesetName,tile_id))
        """
        lstTileBloquant = dictBloquant.get(tilesetName)
        if (lstTileBloquant!=None) and (tile_id in lstTileBloquant):
            self.traversable = False # A changer avec une liste des id des tuiles non traversables
        else:
            self.traversable = True


    