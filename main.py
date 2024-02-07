from kivy.app import App
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable

Config.set('graphics', 'width', '1500')
Config.set('graphics', 'height', '1500')
class Athen_Cesar(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.window = GridLayout()
        self.window.size_hint = (0.9, 0.9)
        self.window.size = (1500, 1500)
        self.m = 26
        self.selected_file = ""

        # A
        self.a_label = Label(text="A")
        self.a_label.pos = (50, 650)
        self.a_label.size = (20,20)
        self.window.add_widget(self.a_label)
        self.a = TextInput()
        self.a.text = "1"
        self.a.multiline = False
        self.a.pos = (150, 650)
        self.a.size = (40, 35)
        self.window.add_widget(self.a)
        # B
        self.b_label = Label(text="B")
        self.b_label.size = (20, 20)
        self.b_label.pos = (50, 600)
        self.window.add_widget(self.b_label)
        self.b = TextInput()
        self.b.text = "1"
        self.b.pos = (150, 600)
        self.b.size = (40, 35)
        self.b.multiline = False
        self.window.add_widget(self.b)


        # input message
        self.input_label = Label(text="Enter message:")
        self.input_label.size = (200, 25)
        self.input_label.pos = (100, 450)
        self.window.add_widget(self.input_label)

        self.input = TextInput()
        self.input.size = (400,400)
        self.input.pos=(0,0)
        self.window.add_widget(self.input)

        # output
        self.output_label = Label(text="Output:")
        self.output_label.size = (200, 25)
        self.output_label.pos = (700, 450)
        self.window.add_widget(self.output_label)

        self.output = TextInput()
        self.output.size = (400, 400)
        self.output.pos = (600,0)
        self.window.add_widget(self.output)

        # Encrypt
        self.encrypt = Button(
            text = "Encrypt"
        )
        self.encrypt.size = (150, 50)
        self.encrypt.pos = (425,300)
        self.encrypt.bind(on_press = self.EcryptByKey)
        self.window.add_widget(self.encrypt)
        # Decrypt
        self.decrypt = Button(
            text="Decrypt"
        )
        self.decrypt.size = (150, 50)
        self.decrypt.pos = (425, 250)
        self.decrypt.bind(on_press=self.DecryptByKey)
        self.window.add_widget(self.decrypt)
        # File_en
        self.File_en = Button(
            text="File_en"
        )
        self.File_en.size = (150, 50)
        self.File_en.pos = (425, 200)
        self.File_en.bind(on_press=self.Choose_en)
        self.window.add_widget(self.File_en)
        # File_de
        self.File_de = Button(
            text="File_de"
        )
        self.File_de.size = (150, 50)
        self.File_de.pos = (425, 150)
        self.File_de.bind(on_press=self.Choose_de)
        self.window.add_widget(self.File_de)
        # grid
        self.alphbet = [chr(ord('A') + i) for i in range(26)]
        self.Num_list = [i for i in range(26)]
        self.Num_list_coded = [(i * int(self.a.text) + int(self.b.text)) % 26 for i in range(26)]
        self.grid = MDDataTable(
            size=(1100,300),
            column_data=[(letter, 8) for letter in self.alphbet],
            row_data=[self.Num_list])
        self.grid.pos = (300,550)
        self.grid.add_row(self.Num_list_coded)
        self.new_alphabet = [chr(ord('A') + i) for i in range(26)]
        buf = self.new_alphabet[0]
        self.new_alphabet.pop(0)
        self.new_alphabet.append(buf)
        self.grid.add_row(self.new_alphabet)
        self.window.add_widget(self.grid)

        return self.window

    def are_coprime(self,a, b):
        if self.find_gcd(a, 26) == 1 and self.find_gcd(b, 26) == 1:
            gcd = self.find_gcd(a, b)
        else:
            gcd = 0
        return gcd == 1

    def find_gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def Choose_en(self,instance):
        self.show_file_chooser(instance)
        if self.selected_file != "":
            file = open(self.selected_file, "r")
            self.input.text = file.read()
            file.close()
    def Choose_de(self,instance):
        self.show_file_chooser(instance)
        if self.selected_file != "":
            file = open(self.selected_file, "r")
            self.output.text = file.read()
            file.close()

    def show_file_chooser(self, instance):
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=self.on_file_submit)

        self.popup = Popup(title="Choose a File", content=file_chooser, size_hint=(0.9, 0.9))
        self.popup.open()

    def on_file_submit(self, instance, value, touch):
        self.selected_file = value and value[0]
        if self.selected_file:
            print("Selected File:", self.selected_file)
        self.popup.dismiss()
    def EcryptByKey(self,instance):
        a = int(self.a.text)
        b = int(self.b.text)
        message = self.input.text.lower()
        encryption = ""
        if self.are_coprime(a,b):
            for l in message:
                code = ord(l)
                if code in range(97, 123):
                    code -= 97
                else:
                    encryption += l
                    continue
                enc = (code*a + b)%26
                out = chr(enc + 97)
                encryption += out
            self.output.text = f"{encryption}"
            new_Num = [(i*a + b) % 26 for i in range(0, 26)]
            self.grid.update_row(self.Num_list_coded, new_Num)
            self.Num_list_coded = new_Num
            new_alphabet = []
            for i in new_Num:
                new_alphabet.append(chr(i+97))
            self.grid.update_row(self.new_alphabet,new_alphabet)
            self.new_alphabet = new_alphabet
            with open('C:\lab2\output.txt', 'w') as file:
                # Perform write operations here
                file.write(self.output.text)
        else:
            self.output.text = f"{a}, {b} and 26 arent coprime encryption not possible"

    def DecryptByKey(self,instance):
        a = int(self.a.text)
        b = int(self.b.text)
        message = self.output.text.lower()
        decryption = ""
        if self.are_coprime(a,b):
            na = 0
            k = 1
            while True:
                na = (1 + k * self.m) / a
                if na % 2 in [0.0, 1.0]:
                    print(na, k)
                    break
                else:
                    k += 1
                    continue
            for l in message:
                code = ord(l)
                if code in range(97, 123):
                    code -= 97
                else:
                    decryption += l
                    continue
                denc = na*(code - b)%self.m
                out = chr(int(denc + 97))
                decryption += out
            self.input.text = f"{decryption}"
            new_Num = [(i * a + b) % 26 for i in range(0, 26)]
            self.grid.update_row(self.Num_list_coded, new_Num)
            self.Num_list_coded = new_Num
            new_alphabet = []
            for i in new_Num:
                new_alphabet.append(chr(i + 97))
            self.grid.update_row(self.new_alphabet, new_alphabet)
            self.new_alphabet = new_alphabet
            with open('C:\lab2\input.txt', 'w') as file:
                file.write(self.input.text)
        else:
            self.output.text = f"{a}, {b} and 26 arent coprime encryption not possible"
            self.root

if __name__ == "__main__":
    Athen_Cesar().run()