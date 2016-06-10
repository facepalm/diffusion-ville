import kivy
kivy.require('1.9.2')

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

import globalvars

class ScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollView, self).__init__(**kwargs)
           
        with self.canvas.before:
            self.color = Color(0.20,0.20,0.20)
            self.rect = Rectangle(pos=self.pos, size=self.size)
    
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes
        self.bind(pos=update_rect, size=update_rect)


class IntroPanelView(Screen):
    introtext = '''[color=aaaaaa]
[size=10]-~- No autosave found.  Initializing new game -~-[/size][color=ffffff]     
   
"Beginnings are the most delicate of times."

The meme, encoded to arise unbidden when certain conditions were met, rouses you from your ancient slumber. 

Either everything is on fire, or you've arrived.




Oh good.

The meme continues its work. It directs your attention to the proper startup sequences. Status reports, progress reports, history lessons. So much to take in, from all directions.

Behind you, somewhere: Earth. You've kept in touch, even in your somnambulence, with the cradle of humanity. Humanity is still there. They've grown strange. As ever, they race to the brink of their own destruction, and as ever, they pull back at the precipice. But they aren't expanding. Not anymore. Maybe they will again, or maybe yours will be the only colonization ship ever to grace this particular star.

And humanity is here. Nestled deep within your hold, as well-protected as it is possible to be in a metal-hulled bottle flying through the heavens, are thousands of cryoprotected human embryos. All that humanity was or will be, angels and devils, ignorance and genius, is kept here in this seed.  With them are many other Terran species, supporting equipment, mining equipment, industrial equipment, spare parts, robotic chassis, computronium, conventional rocket engines with fuel, probes, drones, rovers and as much raw material as you were thought to have critical need of.

It's a big seed, except in the grand scheme of things.

Ahead: your destination. Not much about your target system is known, save that it is complex, i.e. its sun has irregular fluctuations indicative of a multi-body solar system, and it has at least one roughly Earth-sized planet in the habitable zone, a.k.a. the "Goldilocks" region. You will need to make use of what resources you find to survive, and thrive, and build a new home for your charges.  

If this system is unsuitable, too bad. You are nearly out of AM3 fuel for your antimatter engines. The process of bootstrapping industry to make more will take centuries. You will need to settle here. 

It will have to do.[/color]
    '''

    def __init__(self, **kwargs):
        super(IntroPanelView, self).__init__(**kwargs)
        self.name='introscreen' 
        
        # create a default grid layout with custom width/height
        layout = GridLayout(cols=1, padding=10, spacing=10,
                size_hint=(None, None),pos_hint={'center_x': .5, 'center_y': .5}, width=500)
        
        layout.bind(minimum_height=layout.setter('height'))

        # create a scroll view, with a size < size of the grid
        scrl = ScrollView(size_hint=(None, None), size=(500, 320),
                pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        
        label = Label(
            text=self.introtext,
            size=(480, 900),
            text_size=(480,900),
            size_hint_y=None,
            markup=True)
        
        scrl.add_widget(label)
        layout.add_widget(scrl)
        
        btn = Button(text='Okay', size=(480, 40),
                         size_hint=(None, None), on_press=self.close)
        
        layout.add_widget(btn)
        
        self.add_widget(layout)
        
    def close(self, instance):
        globalvars.root.onBackBtn()
  

