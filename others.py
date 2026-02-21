import hcs
import chat_main
import customtkinter as ctk
import news
# ------------------ Config ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ACCENT = "#3b82f6"
BG_CARD = "#111827"

# ------------------ App ------------------
class MainApp(ctk.CTk):
    def __init__(self,language):
        super().__init__()

        # self.title(msg)/
        self.news = "News"
        self.books = "Books"
        self.photos = "Photos"

        if language == "hindi":
            self.news = "समाचार"
            self. books = "किताबें"
            self.photos = "तस्वीरें"

        self.attributes("-fullscreen", True)

        # Exit fullscreen
        self.bind("<Escape>", lambda e: self.destroy())

        # Keyboard
        self.bind("<Delete>", self.move_left)
        # self.bind("<Right>", self.move_right)
        self.bind("<Return>", self.select_option)

        # Root container
        self.root_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.root_frame.pack(expand=True, fill="both")

        # CENTER container (this centers the cards)
        self.center_frame = ctk.CTkFrame(self.root_frame, fg_color="transparent")
        self.center_frame.pack(expand=True)

        # Cards frame
        self.card_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.card_frame.pack()

        # Cards
        self.cards = []
        self.cards.append(self.create_card("📰",self.news))
        self.cards.append(self.create_card("📖", self.books))
        self.cards.append(self.create_card("📷", self.photos))
        

        for card in self.cards:
            card.pack(side="left", padx=20)

        self.current_index = 0
        self.update_focus(animated=False)

    # ------------------ Card ------------------
    def create_card(self, icon, text):
        card = ctk.CTkFrame(
            self.card_frame,
            width=220,
            height=160,
            corner_radius=30,
            fg_color=BG_CARD,
            border_width=2,
            border_color="#1f2937"
        )
        card.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=72)
        )
        icon_label.pack(pady=(40, 10))

        text_label = ctk.CTkLabel(
            card,
            text=text,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#f9fafb"
        )
        text_label.pack()

        # Click support
        for widget in (card, icon_label, text_label):
            widget.bind("<Button-1>", lambda e, c=card: self.card_click(c))

        return card

    # ------------------ Focus ------------------
    def update_focus(self, animated=True):
        for i, card in enumerate(self.cards):
            if i == self.current_index:
                card.configure(
                    border_color=ACCENT,
                    border_width=4,
                    width=460,
                    height=290
                )
            else:
                card.configure(
                    border_color="#1f2937",
                    border_width=2,
                    width=420,
                    height=260
                )

    # ------------------ Keyboard ------------------
    def move_left(self, event):
        # print(self.current_index)
        self.current_index = (self.current_index + 1) % len(self.cards)
        
        self.update_focus()

    def move_right(self, event):
        self.current_index = (self.current_index + 1) % len(self.cards)
        self.update_focus()

    def select_option(self, event):
        self.activate(self.current_index)

    def card_click(self, card):
        self.current_index = self.cards.index(card)
        self.update_focus()
        self.activate(self.current_index)

    # ------------------ Actions ------------------
    def activate(self, index):
        if index == 0:
            news.main()
            
        elif index == 1:
            pass

        elif index == 2:
            pass
            


# ------------------ Run ------------------
def main(language="english"):
    app = MainApp(language)
    app.mainloop()
