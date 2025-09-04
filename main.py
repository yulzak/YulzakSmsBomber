from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
import threading
import webbrowser
from sms import SendSms

servisler_sms = [attr for attr in dir(SendSms) if callable(getattr(SendSms, attr)) and not attr.startswith('__')]
success_count = 0

INSTAGRAM_URL = "https://www.instagram.com/yulvez/"
GITHUB_URL = "https://github.com/yulzak"
YOUTUBE_URL = "https://www.youtube.com/@Yulzak"

class IconButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (50,50)
        with self.canvas.before:
            Color(0.85,0.85,0.85,1)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(on_press=self.on_hover)
        self.bind(on_release=self.off_hover)

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_hover(self, *args):
        with self.canvas.before:
            Color(0.7,0.7,0.7,0.5)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])

    def off_hover(self, *args):
        with self.canvas.before:
            Color(0.85,0.85,0.85,1)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])

class SmsLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_image = Image(source='arkaplan.png', allow_stretch=True, keep_ratio=False, size_hint=(1,1), pos_hint={'x':0,'y':0})
        self.add_widget(self.bg_image)

        self.logo = Image(source='uyg.png', size_hint=(0.25,0.25), pos_hint={'center_x':0.5,'top':1})
        self.add_widget(self.logo)

        self.fg_layout = BoxLayout(orientation='vertical', spacing=15, padding=20, size_hint=(0.9,0.75), pos_hint={'center_x':0.5,'y':0.1})
        self.add_widget(self.fg_layout)

        self.title = Label(
            text="[b]Yulzak SMS Bomber[/b]",
            markup=True,
            font_size=32,
            color=(30/255,136/255,160/255,1),
            size_hint=(1,0.12)
        )
        self.fg_layout.add_widget(self.title)

        self.tel_input = TextInput(
            hint_text="Telefon numarasını +90 olmadan yazınız",
            multiline=False,
            input_filter='int',
            size_hint=(1,0.1),
            padding_y=(10,10),
            background_color=(0.1,0.1,0.1,0.5),
            foreground_color=(30/255,136/255,160/255,1)
        )
        self.fg_layout.add_widget(self.tel_input)

        self.send_btn = Button(
            text="SMS Gönder",
            size_hint=(1,0.12),
            background_color=(30/255,136/255,160/255,1),
            color=(1,1,1,1)
        )
        self.send_btn.bind(on_press=self.start_sms_threads)
        self.fg_layout.add_widget(self.send_btn)

        self.scrollview = ScrollView(size_hint=(1,0.5))
        self.msg_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=(5,5))
        self.msg_layout.bind(minimum_height=self.msg_layout.setter('height'))
        self.scrollview.add_widget(self.msg_layout)
        self.fg_layout.add_widget(self.scrollview)

        self.count_label = Label(text=f"Toplam Başarılı: {success_count}", size_hint=(1,0.05), color=(30/255,136/255,160/255,1))
        self.fg_layout.add_widget(self.count_label)

        social_layout = BoxLayout(size_hint=(1,0.12), spacing=10, pos_hint={'center_x':0.5})
        self.insta_btn = IconButton(source='instagram_color.png')
        self.insta_btn.bind(on_press=lambda x: webbrowser.open(INSTAGRAM_URL))
        self.github_btn = IconButton(source='github_color.png')
        self.github_btn.bind(on_press=lambda x: webbrowser.open(GITHUB_URL))
        self.youtube_btn = IconButton(source='youtube.png')
        self.youtube_btn.bind(on_press=lambda x: webbrowser.open(YOUTUBE_URL))
        self.stop_btn = Button(
            text="İşlemi Sonlandır",
            size_hint=(None,None),
            size=(150,50),
            background_color=(1,0,0,1),
            color=(1,1,1,1)
        )
        self.stop_btn.bind(on_press=lambda x: App.get_running_app().stop())
        social_layout.add_widget(self.insta_btn)
        social_layout.add_widget(self.github_btn)
        social_layout.add_widget(self.youtube_btn)
        social_layout.add_widget(self.stop_btn)
        self.fg_layout.add_widget(social_layout)

        self.sms_thread = None

    def start_sms_threads(self, instance):
        tel_no = self.tel_input.text.strip()
        if len(tel_no) != 10:
            self.add_message("[HATA] Telefon numarası 10 haneli olmalı!")
            return
        if self.sms_thread and self.sms_thread.is_alive():
            self.add_message("[!] SMS gönderme zaten devam ediyor.")
            return
        self.sms_thread = threading.Thread(target=self.send_sms_all_loop, args=(tel_no,), daemon=True)
        self.sms_thread.start()

    def send_sms_all_loop(self, tel_no):
        send_sms = SendSms(tel_no, mail="")
        while True:
            for fonk in servisler_sms:
                self.make_call_quiet(send_sms, fonk, tel_no)
                threading.Event().wait(0.1)

    def make_call_quiet(self, sms_obj, fonk, tel_no):
        global success_count
        before = getattr(sms_obj, 'adet', 0)
        try:
            getattr(sms_obj, fonk)()
        except Exception as e:
            Clock.schedule_once(lambda dt: self.add_message(f"[DEBUG][!] {fonk} -> {tel_no} HATA: {str(e)}"), 0)
            return
        after = getattr(sms_obj, 'adet', 0)
        if after > before:
            success_count += (after - before)
            msg = f"[✔] {fonk} -> {tel_no}"
            Clock.schedule_once(lambda dt: self.add_message(msg), 0)
            Clock.schedule_once(lambda dt: self.update_count(), 0)
        else:
            Clock.schedule_once(lambda dt: self.add_message(f"[-] Başarısız! {tel_no} -> {fonk}"), 0)

    def add_message(self, msg):
        lbl = Label(text=msg, markup=True, size_hint_y=None, height=30, color=(30/255,136/255,160/255,1))
        self.msg_layout.add_widget(lbl)
        self.scrollview.scroll_to(lbl)

    def update_count(self):
        self.count_label.text = f"Toplam Başarılı: {success_count}"

class SmsApp(App):
    def build(self):
        return SmsLayout()

if __name__ == "__main__":
    SmsApp().run()
