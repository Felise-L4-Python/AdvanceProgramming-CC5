import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

class Pokemon:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name'].capitalize()
        self.height = data['height']
        self.weight = data['weight']
        self.types = [t['type']['name'] for t in data['types']]
        self.abilities = [a['ability']['name'] for a in data['abilities']]

class PokemonApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pokémon Information App")
        self.master.geometry("900x800")
        self.master.configure(bg='#FFFACD')  
        self.master.minsize(900, 800)
        self.master.resizable(0, 0)

        # Define font styles
        self.default_font = ("Verdana", 9)
        self.bold_font = ("Verdana", 9, "bold")
        self.button_style = {
            "bg": "#F4A460",           
            "fg": "white",              
            "font": self.bold_font,     
            "relief": tk.FLAT,           
            "activebackground": "#CD853F",  
            "padx": 10,                 
            "pady": 5                   
        }

        self.pokemon1 = None
        self.pokemon2 = None

        self.create_widgets()

    def create_widgets(self):
        # Configure grid layout for master
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(2, weight=1)

        # Logo frame
        logo_frame = tk.Frame(self.master, bg='#FFFACD')
        logo_frame.grid(row=0, column=0, pady=10, sticky="ew")

        try:
            logo_image = Image.open("logo.png")
            logo_image = logo_image.resize((250, 100), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(logo_frame, image=logo_photo, bg='#FFFACD')
            logo_label.image = logo_photo
            logo_label.pack()
        except Exception as e:
            print(f"Could not load logo: {e}")

        # Search frame
        search_frame = tk.Frame(self.master, bg='#FFFACD')
        search_frame.grid(row=1, column=0, pady=5, sticky="ew")
        
        # Configure columns in search frame
        search_frame.grid_columnconfigure(1, weight=1)  

        # Label for search bar
        tk.Label(
            search_frame,
            text="Enter Pokémon name or ID:",
            bg='#FFFACD',
            font=self.bold_font,
            anchor="e"
        ).grid(row=0, column=0, sticky="e", padx=(5, 5))

        # Add search entry box
        self.search_entry = tk.Entry(search_frame, font=self.default_font)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(5, 5))

        # Search button
        tk.Button(
            search_frame,
            text="Search",
            **self.button_style,
            command=self.search_pokemon
        ).grid(row=0, column=2, sticky="w", padx=(5, 5))

        # Pokémon selection
        selection_frame = tk.Frame(search_frame, bg='#FFFACD')
        selection_frame.grid(row=1, column=0, columnspan=3)  
        self.pokemon_var = tk.StringVar(value="1")
        
        tk.Radiobutton(
            selection_frame,
            text="Pokémon 1",
            variable=self.pokemon_var,
            value="1",
            bg='#FFFACD',
            font=self.default_font
        ).pack(side=tk.LEFT, padx=(10))
        
        tk.Radiobutton(
            selection_frame,
            text="Pokémon 2",
            variable=self.pokemon_var,
            value="2",
            bg='#FFFACD',
            font=self.default_font
        ).pack(side=tk.LEFT)

        # Display frames for Pokémon details
        display_frame = tk.Frame(self.master, bg='#F4A460')
        display_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        
        display_frame.grid_columnconfigure(0, weight=1)
        display_frame.grid_columnconfigure(1, weight=1)

        self.pokemon1_frame = tk.Frame(display_frame, bg='white', relief=tk.RIDGE, borderwidth=1)
        self.pokemon1_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.pokemon1_frame.grid_propagate(False)
        self.pokemon1_frame.config(width=400, height=500)

        self.pokemon2_frame = tk.Frame(display_frame, bg='white', relief=tk.RIDGE, borderwidth=1)
        self.pokemon2_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.pokemon2_frame.grid_propagate(False)
        self.pokemon2_frame.config(width=400, height=500)

        self.init_pokemon_frame(self.pokemon1_frame)
        self.init_pokemon_frame(self.pokemon2_frame)

        # Compare and Clear buttons
        button_frame = tk.Frame(self.master, bg='#FFFACD')
        button_frame.grid(row=3, column=0, pady=10)
        tk.Button(button_frame, text="Compare", **self.button_style, command=self.compare_pokemon).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear", **self.button_style, command=self.clear_pokemon).pack(side=tk.LEFT, padx=5)

    def init_pokemon_frame(self, frame):
        for i in range(7): 
            frame.grid_rowconfigure(i, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Placeholder for image
        tk.Label(frame, bg='white', height=15).grid(row=0, column=0, sticky="nsew")
        
        # Placeholders for text
        for i in range(1, 7):
            tk.Label(frame, bg='white', font=self.default_font).grid(row=i, column=0, sticky="w")

    def search_pokemon(self):
        query = self.search_entry.get().lower()
        if not query:
            messagebox.showerror("Error", "Please enter a Pokémon name or ID")
            return

        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{query}")
            response.raise_for_status()
            data = response.json()
            pokemon = Pokemon(data)

            # Assigns the Pokémon to the appropriate attribute
            if self.pokemon_var.get() == "1":
                self.pokemon1 = pokemon
            else:
                self.pokemon2 = pokemon

            self.display_pokemon(pokemon)
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to fetch Pokémon data. Please try again.")

    def display_pokemon(self, pokemon):
        frame = self.pokemon1_frame if self.pokemon_var.get() == "1" else self.pokemon2_frame

        for widget in frame.winfo_children():
            widget.destroy()

        self.init_pokemon_frame(frame)

        # Display Pokémon image
        try:
            image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon.id}.png"
            response = requests.get(image_url)
            image_data = Image.open(io.BytesIO(response.content))
            image_data = image_data.resize((250, 250), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image_data)

            image_label = tk.Label(frame, image=photo, bg='white')
            image_label.image = photo  # Keep a reference
            image_label.grid(row=0, column=0, pady=10)
        except Exception as e:
            print(f"Could not load image: {e}")

        # Display Pokémon information
        info = [
            ("Name", pokemon.name),
            ("ID", pokemon.id),
            ("Height", pokemon.height),
            ("Weight", pokemon.weight),
            ("Types", ", ".join(pokemon.types)),
            ("Abilities", ", ".join(pokemon.abilities))
        ]

        for i, (label, value) in enumerate(info, start=1):
            tk.Label(frame, text=f"{label}:", bg='white', anchor='w', font=self.bold_font, fg='#35678c').grid(row=i, column=0, sticky="w", padx=10, pady=2)
            tk.Label(frame, text=value, bg='white', anchor='w', font=self.default_font, fg='#707070').grid(row=i, column=0, sticky="e", padx=(0, 10), pady=2)

    def compare_pokemon(self):
        if not self.pokemon1 or not self.pokemon2:
            messagebox.showerror("Error", "Please search for two Pokémon to compare")
            return

        comparison = f"Comparison:\n"
        comparison += f"Height: {self.pokemon1.name} is {'taller' if self.pokemon1.height > self.pokemon2.height else 'shorter'} than {self.pokemon2.name}\n"
        comparison += f"Weight: {self.pokemon1.name} is {'heavier' if self.pokemon1.weight > self.pokemon2.weight else 'lighter'} than {self.pokemon2.name}\n"
        comparison += f"Types: {self.pokemon1.name} has {len(self.pokemon1.types)} type(s), {self.pokemon2.name} has {len(self.pokemon2.types)} type(s)\n"
        comparison += f"Abilities: {self.pokemon1.name} has {len(self.pokemon1.abilities)} ability/abilities and {self.pokemon2.name} has {len(self.pokemon2.abilities)} ability/abilities"

        messagebox.showinfo("Pokémon Comparison", comparison)

    def clear_pokemon(self):
        self.pokemon1 = None
        self.pokemon2 = None
        for frame in [self.pokemon1_frame, self.pokemon2_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
            self.init_pokemon_frame(frame)
        self.search_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)
    root.mainloop()
