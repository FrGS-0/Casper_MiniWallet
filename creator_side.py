from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.popup import Popup
from kivy.uix.label import Label

blue = "#00008B"
red = "#FF0000"
conversion_ratio = 10 ** 9

class creator_Side(App):
    def build(self):
        self.layout = FloatLayout()

        self.qr_image = Image(
            source="", size_hint=(0.25, 0.25),
            pos_hint={"center_x": 0.5, "y": 0.65}
            )
        self.qr_image.texture = CoreImage("casper_logo.png").texture

        size_input = (0.8, 0.1)
        self.address_input = TextInput(
            hint_text="Address", multiline=False,
            size_hint=size_input, pos_hint={"x": 0.1, "y": 0.5}
            )
        self.value_input = TextInput(
            hint_text="Value (CSPR)", multiline=False,
            size_hint=size_input, pos_hint={"x": 0.1, "y": 0.35}
            )
        self.message_input = TextInput(
            hint_text="Message (Optional)", multiline=False,
            size_hint=size_input, pos_hint={"x": 0.1, "y": 0.2}
            )

        self.qr_button = Button(
            text="Get QR", size_hint=size_input,
            pos_hint={"x": 0.1, "y": 0.05},
            background_color=red,
            on_press=self.handle_qr_button
            )
        self.sv_button = Button(
            text="Save QR", size_hint=(0.35, 0.1),
            pos_hint={"x": 0.1, "y": 0.05},
            background_color=red,
            on_press=self.handle_sv_button
            )
        self.nw_button = Button(
            text="New QR", size_hint=(0.35, 0.1),
            pos_hint={"x": 0.55, "y": 0.05},
            background_color=red,
            on_press=self.handle_nw_button
            )

        self.layout.add_widget(self.qr_image)
        self.layout.add_widget(self.address_input)
        self.layout.add_widget(self.value_input)
        self.layout.add_widget(self.message_input)
        self.layout.add_widget(self.qr_button)

        return self.layout

    def on_start(self):
        self.title = "Casper MiniWallet"
        popup = self.create_popup(
            "info",
            "Instructions:\nFill in all the necessary fields with the pertinent\ninformation and press \"Get QR\""
            )
        popup.open()

    def create_popup(self, title, text):
        popup = Popup(
            title=title, size_hint=(0.8, 0.8),
            background = 'atlas://data/images/defaulttheme/button_pressed',
            separator_color=red
            )
        pop_button = Button(
            text="OK", on_press=popup.dismiss,
            size_hint=(0.2, 0.1),
            pos_hint={"x": 0.8, "y": 0},
            background_color=red
            )
        pop_label = Label(
            text=text, size_hint=(1, 0.9),
            pos_hint={"x": 0, "y": 0.1},
            color=(0, 0, 0, 1), halign="center",
            font_size="18sp"
            )
        pop_layout = FloatLayout()
        pop_layout.add_widget(pop_label)
        pop_layout.add_widget(pop_button)
        popup.add_widget(pop_layout)
        return popup

    def handle_qr_button(self, instance):
        if (self.address_input.text == "") or (self.value_input.text == ""):
            popup = self.create_popup(
                "warning",
                "Warning:\nPlease fill in all the necessary fields"
                )
            popup.open()
            return
        try:
            # The value in cspr needs to be turned into motes for storage and compatibility
            value_int = int(float(self.value_input.text) * conversion_ratio)
        except:
            popup = self.create_popup(
                "warning",
                "Warning:\nPlease input a valid value"
                )
            popup.open()
            return
        data = {
            "address": self.address_input.text,
            "value": str(value_int),
            "message": self.message_input.text
            }
        self.qr_image_data, self.qr_image_object = qr_creator(data)
        self.qr_image.texture = CoreImage(self.qr_image_data, ext="png").texture
        self.qr_image.reload()

        self.layout.remove_widget(instance)
        self.layout.add_widget(self.sv_button)
        self.layout.add_widget(self.nw_button)

        self.address_input.readonly = True
        self.value_input.readonly = True
        self.message_input.readonly = True

    def handle_sv_button(self, instance):
        self.qr_image_object.save("qr.png")

        import os
        path = os.path.join(os.getcwd(), "qr.png")
        popup = self.create_popup("info",
            "QR Code saved to\n\"" + path + "\""
            )
        popup.open()

    def handle_nw_button(self, instance):
        self.layout.remove_widget(self.sv_button)
        self.layout.remove_widget(instance)
        self.layout.add_widget(self.qr_button)

        self.address_input.text = ""
        self.value_input.text = ""
        self.message_input.text = ""

        self.address_input.readonly = False
        self.value_input.readonly = False
        self.message_input.readonly = False

        self.qr_image.texture = CoreImage("casper_logo.png").texture
        self.qr_image.reload()

def qr_creator(data):
    import qrcode
    import json
    import io

    image = io.BytesIO()
    json_string = ""
    json_string = json.dumps(data)
    qr_image = qrcode.make(json_string)
    qr_image.save(image, ext="png")
    image.seek(0)
    image_data = io.BytesIO(image.read())

    return image_data, qr_image

Window.size = (500, 500)
Window.minimum_height = 500
Window.minimum_width = 500
Window.clearcolor = (0, 0, 255, 1)
creator_Side().run()
