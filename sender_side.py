from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import pycspr
from pycspr.client import NodeClient
from pycspr.client import NodeConnectionInfo
import random
from pycspr.crypto import KeyAlgorithm

import cv2
import json

red = "#FF0000"
size_input = (0.8, 0.1)
conversion_ratio = 10 ** 9

class sender_Side(App):
    def build(self):
        self.layout = FloatLayout()
        self.logo_image = Image(
            source="", size_hint=(0.25, 0.25),
            pos_hint={"center_x": 0.5, "y": 0.65}
            )
        self.logo_image.texture = CoreImage("casper_logo.png").texture
        self.path_input = TextInput(
            hint_text="Path to QR Code", multiline=False,
            size_hint=size_input, pos_hint={"x": 0.1, "y": 0.5}
            )
        self.load_button = Button(
            text="Load", pos_hint={"x": 0.1, "y": 0.05},
            background_color=red,
            size_hint=size_input,
            on_press=self.handle_load_button
            )

        self.sign_button = Button(
            text="Sign", on_press=self.handle_sign_button,
            pos_hint={"x": 0.1, "y": 0.05},
            background_color=red,
            size_hint=(0.35, 0.1)
            )
        self.nw_button = Button(
            text="Load Another QR", size_hint=(0.35, 0.1),
            pos_hint={"x": 0.55, "y": 0.05},
            background_color=red,
            on_press=self.handle_nw_button
            )

        self.info_label = Label(
            text="", size_hint=(0.8, 0.29),
            pos_hint={"x": 0.1, "y": 0.18},
            color=(0, 0, 0, 1), halign="left",
            font_size="11sp"
            )

        self.layout.add_widget(self.path_input)
        self.layout.add_widget(self.load_button)
        self.layout.add_widget(self.logo_image)

        return self.layout

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

    def handle_load_button(self, instance):
        from os.path import exists
        if self.path_input.text == "":
            popup = self.create_popup(
                "warning",
                "Warning:\nPlease fill in all the necessary fields"
                )
            popup.open()
            return
        if not exists(self.path_input.text):
            popup = self.create_popup(
                "warning",
                "Warning:\nQR Code not found"
                )
            popup.open()
            return
        data, err = load_qr(self.path_input.text)
        t, form_value, data = check_qr(data)
        if (err != None) and (t != None):
            popup = self.create_popup(
                "warning",
                "Warning:\nAn error has occured\nAre you sure this is a valid QR Code?"
                )
            popup.open()
            self.path_input.text = ""
            return
        self.info_label.text = "Address: " + data["address"] + "\n" + "Value: " + form_value + "\n" + "Message: " + data["message"]
        self.layout.add_widget(self.info_label)
        self.data = data

        self.layout.remove_widget(self.load_button)
        self.layout.add_widget(self.sign_button)
        self.layout.add_widget(self.nw_button)
        self.path_input.readonly = True

    def handle_sign_button(self, instance):
        client = create_client()
        t = send_transaction(
            client,
            self.data["address"],
            self.data["value"]
        )
        if t:
            popup = self.create_popup(
                "info",
                "Your transaction was succesfully\nsubmitted to the network\nYou can check the results at\n\"https://testnet.cspr.live/\""
                )
            popup.open()
            self.handle_nw_button(None)


    def handle_nw_button(self, instance):
        self.path_input.text = ""
        self.path_input.readonly = False
        self.info_label.text = ""

        self.layout.remove_widget(self.sign_button)
        self.layout.remove_widget(self.nw_button)
        self.layout.remove_widget(self.info_label)
        self.layout.add_widget(self.load_button)

def load_qr(path):
    try:
        qr_image = cv2.imread(path)
        detector = cv2.QRCodeDetector()
        json_string, _, _ = detector.detectAndDecode(qr_image)
        data = json.loads(json_string)
        return data, None
    except:
        return None, 1

def check_qr(data):
    try:
        if data["message"] == "":
            data["message"] = "None"
        form_value = str(float(data["value"]) / conversion_ratio)
        return None, form_value, data
    except:
        return 1, None, None

def pick_node():
    pass

def create_client():
    f = open("hosts.json", "r")
    host_data = json.load(f)
    f.close()
    connection = NodeConnectionInfo(
        host=host_data["ip"],
        port_rpc=host_data["port"]
    )
    client = NodeClient(connection)
    return client

def send_transaction(client, address, value):
    from platform import system
    if system() == "Windows":
        pvk_path = "pair1\secret_key.pem"
    elif system() == "Linux":
        pvk_path = "pair1/secret_key.pem"
    first_counter_party = pycspr.factory.parse_private_key(
        pvk_path, KeyAlgorithm.ED25519.name
        )

    account_key = bytes.fromhex(address)
    second_counter_party = pycspr.factory.create_public_key_from_account_key(account_key)

    chain_name = "casper-test"
    deploy_params = pycspr.factory.create_deploy_parameters(
        account=first_counter_party,
        chain_name=chain_name
        )
    deploy = pycspr.factory.create_native_transfer(
        params=deploy_params,
        amount=int(value),
        target=second_counter_party.account_hash,
        correlation_id=random.randint(1, 1e6)
        )
    deploy.approve(first_counter_party)
    client.deploys.send(deploy)
    return True

Window.size = (500, 500)
Window.minimum_height = 500
Window.minimum_width = 500
Window.clearcolor = (0, 0, 255, 1)
sender_Side().run()
