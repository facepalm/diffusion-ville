from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.image import Image



kv = '''
<MapScreen@Screen>:
    name: 'map name'
    Scatter:
        MapImage:
            id: mapimg
            allow_stretch: False                        
           
'''

Builder.load_string(kv)

class MapScreen(Screen):
    pass

class MapImage(Image):
    pass
    
    def process_map(self,_map):
        self.map = _map
        #relaod map
        print _map
