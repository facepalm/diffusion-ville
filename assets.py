from kivy.core.image import Image


forest_tiles = Image('game-assets/tiles_forest.png').texture

TEX_GRASS = forest_tiles.get_region(240, 16, 16, 16)
TEX_TALLGRASS = forest_tiles.get_region(32, 0, 16, 16)
TEX_BUSH = forest_tiles.get_region(240, 0, 16, 16)
TEX_TREE = forest_tiles.get_region(240, 32, 16, 16)

if __name__ == "__main__":
    import cv2
    
    test = Image(TEX_GRASS)
    test2 = Image(TEX_GRASS)
    print test
