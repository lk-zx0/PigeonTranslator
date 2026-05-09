import customtkinter
import requests
from pynput import keyboard
import os
import json
import sys

google_languages_list = [
    "Auto",
    "Afrikaans",
    "Albanian",
    "Amharic",
    "Arabic",
    "Armenian",
    "Azerbaijani",
    "Basque",
    "Belarusian",
    "Bengali",
    "Bosnian",
    "Bulgarian",
    "Burmese",
    "Catalan",
    "Chinese (Simplified)",
    "Chinese (Traditional)",
    "Croatian",
    "Czech",
    "Danish",
    "Dutch",
    "English",
    "Estonian",
    "Filipino",
    "Finnish",
    "French",
    "French (Canada)",
    "Frisian",
    "Galician",
    "Georgian",
    "German",
    "Greek",
    "Guarani",
    "Gujarati",
    "Hausa",
    "Hebrew",
    "Hindi",
    "Hungarian",
    "Icelandic",
    "Igbo",
    "Indonesian",
    "Irish",
    "Italian",
    "Japanese",
    "Kannada",
    "Khmer",
    "Korean",
    "Kyrgyz",
    "Lao",
    "Latvian",
    "Lingala",
    "Lithuanian",
    "Luxembourgish",
    "Macedonian",
    "Malay",
    "Malayalam",
    "Maltese",
    "Marathi",
    "Mongolian",
    "Nepali",
    "Norwegian",
    "Odia",
    "Persian",
    "Polish",
    "Portuguese (Brazil)",
    "Portuguese (Portugal)",
    "Punjabi",
    "Romanian",
    "Russian",
    "Scots Gaelic",
    "Serbian",
    "Slovak",
    "Slovenian",
    "Somali",
    "Spanish",
    "Swahili",
    "Swedish",
    "Tagalog",
    "Tajik",
    "Tamil",
    "Telugu",
    "Thai",
    "Turkish",
    "Ukrainian",
    "Urdu",
    "Uzbek",
    "Vietnamese",
    "Welsh",
    "Zulu",
]


class App(customtkinter.CTk):

    # Screen init
    def __init__(self):
        super().__init__()

        self.text_to_translate = None

        # The window's dimensions and position setting
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.resizable(False, False)
        self.geometry(f"+{int(screen_width * 0.920)}+{int(screen_height * 0.800)}")
        self.attributes("-topmost", True)

        # The window setting
        self.title("PigeonTrans v1.0")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        # Input
        self.input_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.input_container.grid(row=0, column=0, padx=0, pady=10)
        self.source_language = customtkinter.CTkOptionMenu(self.input_container, width=100, height=3, values=google_languages_list, font=("Arial", 10), fg_color="#3D3F42", button_color="#3D3F42", corner_radius=0, command=self.config_func)
        self.source_language.grid(row=0, column=0, sticky="w", padx=20, pady=5)
        self.input = customtkinter.CTkTextbox(self.input_container, width=350, height=45, fg_color="#4F5154", scrollbar_button_color="#4F5154", scrollbar_button_hover_color="#3D3F42")
        self.input.grid(row=1, column=0, padx=20, pady=0)
        self.input.bind("<Return>", self.translation_services_func)
        self.delete_text_btn = customtkinter.CTkButton(self.input, text="X", width=10, height=10, font=("Arial", 8), fg_color="#3D3F42", command=self.delete_text_func)
        self.delete_text_btn.grid(row=0, column=0, sticky="se")
        # Output
        self.output_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.output_container.grid(row=1, column=0, padx=0, pady=5)
        self.target_language = customtkinter.CTkOptionMenu(self.output_container, width=100, height=3, values=google_languages_list[1:], font=("Arial", 10), fg_color="#3D3F42", button_color="#3D3F42", corner_radius=0, command=self.config_func)
        self.target_language.grid(row=0, column=0, sticky="w", padx=20, pady=5)
        self.exchange_language_btn = customtkinter.CTkButton(self.target_language, width=12, height=12, font=("Arial", 4), text="⥮", fg_color="#3D3F42", command=self.exchange_language_func)
        self.exchange_language_btn.grid(row=0, column=1, padx=10, pady=0)
        self.output = customtkinter.CTkTextbox(self.output_container, width=350, height=70, fg_color="#4F5154")
        self.output.grid(row=1, column=0, padx=20, pady=0)
        self.output.insert("0.0", "Press [Return] to translate")
        self.output.configure(state="disabled")
        # Functions
        self.func_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.func_container.grid(row=2, column=0, padx=0, pady=(5, 10))
        self.ts = customtkinter.CTkLabel(self.func_container, width=1, height=1, text="Translation services:", font=("Arial", 10))
        self.ts.grid(row=0, column=0)
        self.ts_menu = customtkinter.CTkOptionMenu(self.func_container, width=1, height=1, values=["Google"], font=("Arial", 10), fg_color="#3D3F42", button_color="#3D3F42", corner_radius=0, command=self.config_func)
        self.ts_menu.grid(row=0, column=1)
        self.exit = customtkinter.CTkButton(self.func_container, width=1, height=1, text="     Exit     ", font=("Arial", 8), fg_color="#3D3F42", command=self.exit_func)
        self.exit.grid(row=0, column=2, padx=80)

        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        self.hotkey = keyboard.GlobalHotKeys({"<Alt>+t": self.show_hide_window_func})
        self.hotkey.start()
        config_path = "src/config.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    self.source_language.set(config_data.get("Source_language", "Auto"))
                    self.target_language.set(config_data.get("Target_language", "English"))
                    self.ts_menu.set(config_data.get("Translate_service", "Google"))
            except Exception:
                self.config_func()
        else:
            self.config_func()

        self.after(100, self.input.focus)
    # _______________________________ Google _______________________________
    def google_translation_func(self):
        try:
            url = "https://deep-translator-api.azurewebsites.net/google/"
            payload = {
                "source": self.source_language.get().lower(),
                "target": self.target_language.get().lower(),
                "text": self.text_to_translate
            }
            response = requests.post(url, json=payload, timeout=3)
            self.output.configure(state="normal")
            self.output.delete("0.0", "end")
            if response.status_code == 200:
                result = response.json()
                trans_result = result["translation"]
                self.output.insert("0.0", trans_result)
                if len(trans_result) > 30:
                    pass
            elif response.status_code == 429:
                self.output.insert("0.0", 'The number of requests exceeded')
            else:
                self.output.insert("0.0", 'Error,please try again later')
        except Exception as e:
            self.output.configure(state="normal")
            self.output.delete("0.0", "end")
            self.output.insert("0.0", str(e))
        self.output.configure(state="disabled")

    def config_func(self, envent=None):
        if not os.path.exists("src"):
            os.makedirs("src")
        config_dict = {"Source_language": self.source_language.get(),
                       "Target_language": self.target_language.get(),
                       "Translate_service": self.ts_menu.get()
                       }
        with open("src/config.json", "w", encoding="utf-8") as f:
            json.dump(config_dict, f, ensure_ascii=False, indent=4)

    def translation_services_func(self, event):
        service = self.ts_menu.get()
        self.text_to_translate = self.input.get("0.0", "end").strip()
        if service == "Google":
            self.google_translation_func()
        self.config_func()
        return "break"

    def exchange_language_func(self):
        if self.source_language.get() != "Auto":
            source_lang = self.source_language.get()
            target_lang = self.target_language.get()
            self.source_language.set(target_lang)
            self.target_language.set(source_lang)
            self.config_func()
    def delete_text_func(self):
        self.input.delete("0.0", "end")
        self.output.configure(state="normal")
        self.output.delete("0.0", "end")
        self.output.insert("0.0", "Press [Return] to translate")
        self.output.configure(state="disabled")

    def show_hide_window_func(self):
        if self.winfo_viewable():
            self.after(0, self.withdraw)
        else:
            self.after(0, self.deiconify)
            self.after(10, self.lift)
            self.after(20, self.focus_force)
            self.after(30, self.input.focus)

    def exit_func(self):
        self.hotkey.stop()
        self.destroy()
        sys.exit()


main = App()
main.mainloop()
