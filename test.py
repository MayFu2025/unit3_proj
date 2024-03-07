from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
MDScreen:

    MDChip:
        text: "Portland"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.on_release_chip(self)
'''


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_release_chip(self, instance_check):
        print(instance_check)


Test().run()