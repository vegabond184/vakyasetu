from hcs import speak
import chat_main
import customtkinter as ctk
import requests
from newsapi import NewsApiClient



api = NewsApiClient(api_key='d68381765b2148cdbf983e93b3d611c9') # Replace with your actual key
top_headlines = api.get_top_headlines(language='en',page=1, page_size=50)




# translator = Translator()
# ------------------ Config ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ACCENT = "#3b82f6"
BG_CARD = "#111827"


# ------------------ App ------------------
class News(ctk.CTk):
    def __init__(self,language):
        super().__init__()

        self.attributes("-fullscreen", True)

        # Exit fullscreen
        self.bind("<Escape>", lambda e: self.destroy())

        # Keyboard
        self.bind("<Delete>", self.move_left)

        self.news = top_headlines['articles']
        # print(self.news[0])
        # result = translator.translate(text_to_translate, src='en', dest='hi')
        self.current_index = 0

        self.title = ctk.CTkLabel(
            self,
            text="Top News Headlines",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#f9fafb",
            wraplength=800,
            justify="center"
        )
        self.title.pack(pady=20)

        self.news_title = ctk.CTkLabel(
            self,
            text=self.news[self.current_index]['title'],
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#f9fafb",
            wraplength=800,
            justify="center"
        )
        self.news_title.pack(pady=50)


        self.news_content = ctk.CTkLabel(
            self,
            text=self.news[self.current_index]['description'],
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color="#f9fafb",
            wraplength=800,
            justify="center"

        )
        self.news_content.pack(pady=80)

        # speak(top_headlines['articles'][self.current_index]['title'])
        # speak(top_headlines['articles'][self.current_index]['description'])
     

    # ------------------ Keyboard ------------------
    def move_left(self, event):
        self.current_index = self.current_index + 1
        self.news_title.configure(text=self.news[self.current_index]['title'])
        self.news_content.configure(text=self.news[self.current_index]['description'])





# ------------------ Run ------------------
def main(language="english"):
    app = News(language)
    app.mainloop()

# main()

# NewsFromBBC()