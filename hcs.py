import customtkinter as ctk
import pyttsx3
from nltk import FreqDist, ngrams, word_tokenize
import re
import pyautogui
import time


# ------------------------- NLP: WORD SUGGESTIONS -------------------------
def get_word_suggestions(text_corpus, current_word, num_suggestions=5):
    # Tokenize the text into lowercase words
    words = word_tokenize(text_corpus.lower())

    # Frequency distribution of all words
    freq = FreqDist(words)

    # Create bigrams (pairs of consecutive words)
    bigrams = list(ngrams(words, 2))

    # Get frequency of words that follow the current word (context-aware)
    next_word_freq = FreqDist([
        next_word for prev_word, next_word in bigrams
        if prev_word == current_word.lower()
    ])

    # If user typed something, find prefix-matching words
    if current_word:
        pattern = re.compile("^" + re.escape(current_word.lower()))
        possible_words = [w for w in freq.keys() if pattern.match(w)]
    else:
        possible_words = []

    # Sort suggestions by frequency of occurrence
    suggestions = [w.upper() for w in sorted(
        possible_words,
        key=lambda w: freq[w],
        reverse=True
    )[:num_suggestions]]

    # Also include bigram-based (contextual) suggestions
    suggestions_for_one = [word.upper() for word, _ in next_word_freq.most_common(num_suggestions)]

    return suggestions + suggestions_for_one



def speak(text):

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)  # Slow down speech rate
    engine.setProperty('volume', 3)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice (if available)
    engine.say(text)
    engine.runAndWait()



class AlphabetLocator:
    def __init__(self, root):
        
        self.root = root
        self.root.title("HAWKING")
        
        root.attributes('-fullscreen', True) 
        self.root.state("zoomed")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        

        # Grid configuration
        self.alphabet_rows = 7
        self.action_rows = 1
        self.rows = self.alphabet_rows + self.action_rows
        self.cols = 4
        self.labels = []

        # Trackers
        self.current_row = 0
        self.current_col = 0
        self.stage = "col"  # Toggle between 'col' and 'row'
        self.selected_history = ""

        # Suggestion system
        self.suggestions = []
        self.suggestion_labels = []
        self.selected_index = -1

       
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Dynamic resizing
        total_rows = self.rows + 4
        for r in range(total_rows):
            self.main_frame.grid_rowconfigure(r, weight=1)
        for c in range(self.cols + 1):
            self.main_frame.grid_columnconfigure(c, weight=1)

       
        self.history_entry = ctk.CTkEntry(
            self.main_frame, font=("Arial", 26, "bold"), justify="left"
        )

        self.history_entry.focus_set()
        
        
        self.history_entry.grid(row=0, column=0, columnspan=self.cols+1, pady=10, padx=10, sticky="nsew")
        # self.history_entry.bind("<KeyRelease>", self.on_key_release_in_entry)
        self.history_entry.bind("<Down>", self.move_suggestion_down)
        # self.history_entry.bind("<Up>", self.move_suggestion_up)
        self.history_entry.bind("<Return>", self.confirm_suggestion_from_entry)
        self.history_entry.bind('<Map>', self.history_entry.focus_set())
        
        self.update_history()
        

       
        self.suggestion_box = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="gray20")
        self.suggestion_box.grid(row=1, column=0, columnspan=self.cols+1, sticky="nsew", padx=10)
        self.suggestion_box.grid_remove()  # Hidden by default

        # COLUMN AND ROW LABELS
        for c in range(self.cols):
            lbl = ctk.CTkLabel(self.main_frame, text=f"{c+1}", font=("Arial", 18, "bold"))
            lbl.grid(row=2, column=c+1, sticky="nsew", padx=5, pady=5)

        for r in range(self.rows):
            text = "Actions" if r == 0 else f"{r}"
            lbl = ctk.CTkLabel(self.main_frame, text=text, font=("Arial", 18, "bold"))
            lbl.grid(row=r+3, column=0, sticky="nsew", padx=5, pady=5)

        # Create main alphabet and action grid
        self.create_grid()
        

        # ------------------ STATUS BAR ------------------
        self.status = ctk.CTkLabel(self.main_frame, text="Select a column (← →)", font=("Arial", 18))
        self.status.grid(row=self.rows+3, column=0, columnspan=self.cols+1, sticky="nsew")

        self.highlight_selection()
        self.root.after(100, self.history_entry.focus_set)

        #KEYBOARD SHORTCUTS
        
        # Delete: Move Right(loop back to the first) and move down(loop back to the first)
        self.root.bind("<Delete>", self.matrix_navigation)
        self.root.bind("<Return>", self.confirm_selection)  # Enter → Confirm
        self.root.bind("<Escape>", lambda e: self.root.destroy())  # Escape → Exit


    #GRID CREATION
    def create_grid(self):
        """Create the grid layout for actions and alphabets."""
        self.labels = []

        # Action row (row 0)
        actions = ["Enter", "Clear", "Back", "Space"]
        action_row = []
        for c in range(self.cols):
            lbl = ctk.CTkLabel(
                self.main_frame, text=actions[c], font=("Arial", 18, "bold"),
                fg_color="gray25", corner_radius=8
            )
            lbl.grid(row=3, column=c+1, sticky="nsew", padx=5, pady=5)
            action_row.append(lbl)
        self.labels.append(action_row)

        # Alphabet grid (A–Z)
        alphabets = [chr(65 + i) for i in range(26)]
        alphabets.append("Escape")
        index = 0
        for r in range(1, self.rows):
            row_labels = []
            for c in range(self.cols):
                letter = alphabets[index] if index < len(alphabets) else ""
                lbl = ctk.CTkLabel(
                    self.main_frame, text=letter, font=("Arial", 24),
                    fg_color="gray15", corner_radius=8
                )
                lbl.grid(row=r+3, column=c+1, sticky="nsew", padx=5, pady=5)
                row_labels.append(lbl)
                index += 1
            self.labels.append(row_labels)
       
          
        

    #VISUAL SELECTION
    def highlight_selection(self):
        # Reset all colors
        for r in range(self.rows):
            for c in range(self.cols):
                if r == 0:
                    self.labels[r][c].configure(fg_color="gray25")
                else:
                    self.labels[r][c].configure(fg_color="gray15")
        
        

        # Highlight based on stage
        if self.stage == "col":
            for r in range(self.rows):
                self.labels[r][self.current_col].configure(fg_color="royalblue4")
            self.status.configure(text=f"Selected column: {self.current_col+1}. Now choose row (↑ ↓).")

        elif self.stage == "row":
            for c in range(self.cols):
                self.labels[self.current_row][c].configure(fg_color="seagreen4")
            if self.current_row == 0:
                self.status.configure(text="Selected Actions row. Press ENTER to perform action.")
            else:
                self.status.configure(text=f"Selected row: {self.current_row}. Press ENTER to confirm.")

    #NAVIGATION CONTROLS

    def matrix_navigation(self, event):
    
        if self.stage == "col":
            self.current_col = (self.current_col + 1) % self.cols
            self.highlight_selection()

        if self.stage == "row":
            self.current_row = (self.current_row + 1) % self.rows
            self.highlight_selection()



    #CONFIRMATION
    def confirm_selection(self, event):
    
        if self.stage == "col":
            self.stage = "row"
            self.highlight_selection()
            return

        # Get selected label text
        text = self.labels[self.current_row][self.current_col].cget("text")

        if text == "Escape":
            self.root.destroy()

        # Action row logic
        if self.current_row == 0:
            if text == "Clear":
                self.selected_history = ""
            elif text == "Back":
                self.selected_history = self.selected_history[:-1]
            elif text == "Space":
                self.selected_history += " "
            elif text == "Enter":
                speak(self.selected_history)
            self.update_history()

        # Alphabet input
        else:
            if text != "":
                self.selected_history += text
                self.update_history()
                print(self.selected_history)
                

        # Reset selection stage
        self.root.after(800, self.reset_selection)
        self.show_autocomplete()
    

    def reset_selection(self):
        """Reset selection back to column stage."""
        self.stage = "col"
        self.current_row = 0
        self.current_col = 0
        self.highlight_selection()
        
        

    #ENTRY FIELD UPDATES
    def update_history(self):
        """Update the entry box text to match current user input."""
        self.history_entry.delete(0, "end")
        self.history_entry.insert(0, self.selected_history)

    #AUTOCOMPLETE 
    def on_key_release_in_entry(self, event):
        """Handle user typing in entry box and trigger autocomplete."""
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return
        self.show_autocomplete()

    def show_autocomplete(self):
        """Display the autocomplete suggestion list."""
        typed = self.history_entry.get().strip()

        # Clear old suggestions
        for lbl in self.suggestion_labels:
            lbl.destroy()
        self.suggestion_labels = []
        self.suggestions = []
        self.selected_index = -1

        if not typed:
            self.suggestion_box.grid_remove()
            return

        # Example corpus for language suggestions (medical/help phrases)
        corpus = """
        I am hungry
        I am thirsty
        I am tired
        I am in pain
        I am cold
        I am hot
        Please adjust my pillow
        Please move my hand
        Please help me sit up
        Please help me lie down
        Call the nurse
        Call the doctor
        I need medicine
        I feel dizzy
        I feel weak
        I cannot breathe properly
        Please check my blood pressure
        Please check my sugar level
        I am happy
        I am sad
        I am scared
        I feel lonely
        I am comfortable
        Thank you for helping me
        I love you
        Please stay with me
        Hello
        Good morning
        Good night
        How are you?
        I am fine
        Yes
        No
        Maybe
        Please
        Thank you
        Sorry
        exit
        I want to watch TV
        I want to listen to music
        I want to read a book
        I want to sleep
        I want to go outside
        Please open the window
        Please turn on the fan
        Please turn off the light
        Call my family
        Call an ambulance
        I cannot move
        I need help immediately
        I am choking
        I am having chest pain
        """

        last_word = typed.split()[-1] if typed.split() else ""
        self.suggestions = get_word_suggestions(corpus, last_word)
    
        if not self.suggestions:
            self.suggestion_box.grid_remove()
            return

        # Show suggestion box
        self.suggestion_box.grid()

        for i, word in enumerate(self.suggestions[:5]):
            lbl = ctk.CTkLabel(
                self.suggestion_box,
                text=word,
                font=("Arial", 18),
                fg_color="gray30",
                corner_radius=6
            )
            lbl.pack(fill="x", pady=2, padx=4)
            lbl.bind("<Button-1>", lambda e, w=word: self.select_suggestion(w))
            self.suggestion_labels.append(lbl)
        self.update_suggestion_highlight()

    #SUGGESTION CONTROL 
    def update_suggestion_highlight(self):
        """Highlight selected suggestion in the dropdown."""
        for i, lbl in enumerate(self.suggestion_labels):
            if i == self.selected_index:
                lbl.configure(fg_color="royalblue4")
            else:
                lbl.configure(fg_color="gray30")

    def move_suggestion_down(self, event):
        """Move suggestion highlight down."""
        if not self.suggestions:
            return None
        self.selected_index = (self.selected_index + 1) % len(self.suggestion_labels)
        self.update_suggestion_highlight()
        return "break"


    def confirm_suggestion_from_entry(self, event):
        """Confirm currently highlighted suggestion (via Tab)."""
        if not self.suggestions:
            return None
        if self.selected_index != -1:
            
            chosen = self.suggestions[self.selected_index]
            self.select_suggestion(chosen)
            self.show_autocomplete()

            return "break"
        
        # self.selected_index = -1

    def select_suggestion(self, word):
        """Insert the selected suggestion into the entry field."""
        current_text = self.history_entry.get()
        tokens = current_text.split()

        # Remove isolated letters (cleanup)
        for token in tokens:
            if len(token) == 1 and token != "I":
                tokens.remove(token)

        self.selected_history = " ".join(tokens)

        # Append chosen word
        if tokens:
            self.selected_history += " " + word + " "
        else:
            self.selected_history = word

        self.update_history()

        # Clear suggestions
        # for lbl in self.suggestion_labels:
        #     lbl.destroy()
        # self.suggestion_labels = []
        # self.suggestions = []
        # self.selected_index = 0
        # self.suggestion_box.grid_remove()
    

if __name__ == "__main__":
    app = ctk.CTk()
    AlphabetLocator(app)
    app.mainloop()
    
