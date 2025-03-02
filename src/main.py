# Open tkinter window
# Choose your main deck from a list of cards
# Choose your extra deck from a list of cards
# Choose your side deck from a list of cards
# Search bar
# Display currently selected cards in a list
# Be able to remove cards from deck
# Be able to submit deck
# Sort cards in deck alphabetically
# Track number of cards in deck
# Display card icons in deck list after selection
# Game starts (pygame)
# Cards slide into view
# Cards displayed using pygame
# You control both sides
# Side view switches when ready
# You can select your card
# You have a list of actions to take upon selecting your card

import sys, os
import tkinter as tk
import json
from functools import partial
from tkinter import messagebox
from collections import OrderedDict, Counter
from PIL import Image, ImageTk

open('src/main_deck.json', 'w').close()

def update_json_file(file_path, new_data):
    try:
        with open(file_path, 'r+') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
            data.update(new_data)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    except Exception as e:
        print(f"An error occurred: {e}")

def on_item_click(self, item):
    clear_window(root.main_deck_cards)
    if root.main_deck_card_count == 60:
            messagebox.showinfo("Main deck full", "You have reached the main deck card limit. Please either submit your deck or remove cards.")
    elif self.click_counts[item] == 3:
        messagebox.showinfo("Card limit reached", "You have reached the 3 card limit, already.")
    else:
        self.click_counts[item] += 1
        update_json_file('src/main_deck.json', {item: self.click_counts[item]})
        root.main_deck_card_count += 1
        root.item_dict.update({item: self.click_counts[item]})
        root.listbox.delete(0, tk.END)
        root.listbox.insert(0, 'Cards in deck: ' + str(root.main_deck_card_count))
        for item in sorted(list(root.item_dict)):
            if self.click_counts[item] > 0:
                root.listbox.insert(tk.END, item + ': ' + str(root.item_dict[item]))
        i = 0
        for item in sorted(list(Counter(root.item_dict).elements())):
            try:
                img = Image.open(os.path.join(sys._MEIPASS, '../YGO Card Images/' + str(self.items[item]) + '.jpg') if hasattr(sys, '_MEIPASS') else '../YGO Card Images/' + str(self.items[item]) + '.jpg').resize((110, 159))
                photo = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                print("Error: Image file not found.")
                exit()
            image_label = tk.Label(root.main_deck_cards, image=photo)
            x = i * 110
            y = 0
            if (i + 1) / 12 > 1 and (i + 1) / 12 <= 2:
                x = x - 1320
                y = y + 159
            elif (i + 1)  / 12 > 2 and (i + 1)  / 12 <= 3:
                x = x - 1320*2
                y = y + 159*2
            elif (i + 1)  / 12 > 3 and (i + 1)  / 12 <= 4:
                x = x - 1320*3
                y = y + 159*3
            elif (i + 1)  / 12 > 4 and (i + 1)  / 12 <= 5:
                x = x - 1320*4
                y = y + 159*4
            elif (i + 1)  / 12 > 5:
                x = x - 1320*5
                y = y + 159*5
            image_label.place(x=x, y=y)
            image_label.image = photo
            i = i + 1

def on_item_right_click(self, item):
    clear_window(root.main_deck_cards)
    if self.click_counts[item] == 0:
            messagebox.showinfo("Card not in deck", "This card cannot be removed because it is not in your deck, already.")
    else:
        self.click_counts[item] -= 1
        update_json_file('src/main_deck.json', {item: self.click_counts[item]})
        root.main_deck_card_count -= 1
        root.item_dict.update({item: self.click_counts[item]})
        root.listbox.delete(0, tk.END)
        root.listbox.insert(0, 'Cards in deck: ' + str(root.main_deck_card_count))
        for item in sorted(list(root.item_dict)):
            if self.click_counts[item] > 0:
                root.listbox.insert(tk.END, item + ': ' + str(root.item_dict[item]))
        i = 0
        for item in sorted(list(Counter(root.item_dict).elements())):
            try:
                img = Image.open(os.path.join(sys._MEIPASS, '../YGO Card Images/' + str(self.items[item]) + '.jpg') if hasattr(sys, '_MEIPASS') else '../YGO Card Images/' + str(self.items[item]) + '.jpg').resize((110, 159))
                photo = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                print("Error: Image file not found.")
                exit()
            image_label = tk.Label(root.main_deck_cards, image=photo)
            x = i * 110
            y = 0
            if (i + 1) / 12 > 1 and (i + 1) / 12 <= 2:
                x = x - 1320
                y = y + 159
            elif (i + 1)  / 12 > 2 and (i + 1)  / 12 <= 3:
                x = x - 1320*2
                y = y + 159*2
            elif (i + 1)  / 12 > 3 and (i + 1)  / 12 <= 4:
                x = x - 1320*3
                y = y + 159*3
            elif (i + 1)  / 12 > 4 and (i + 1)  / 12 <= 5:
                x = x - 1320*4
                y = y + 159*4
            elif (i + 1)  / 12 > 5:
                x = x - 1320*5
                y = y + 159*5
            image_label.place(x=x, y=y)
            image_label.image = photo
            i = i + 1

def clear_window(window_):
    for widget in window_.winfo_children():
        widget.pack_forget()
        widget.grid_forget()
        widget.place_forget()
        if isinstance(widget, tk.Label):
            widget.config(image='')

def hide_button(self):
    self.pack_forget()

def on_button_click(self):
    if root.main_deck_card_count < 40:
        messagebox.showinfo("Invalid deck size", "Your deck needs to consist of 40-60 cards.")
    else:
        messagebox.showinfo("Deck submitted", "Your deck is legal! Deck submitted.")

def toggle_toplevel(toplevel):
    if toplevel.winfo_ismapped():
        toplevel.withdraw()  # Hide the window
    else:
        toplevel.deiconify() # Show the window

def onEnter(self, card_image, card_name):
    clear_window(card_image)
    try:
        img = Image.open(os.path.join(sys._MEIPASS, '../YGO Card Images/' + str(self.items[card_name]) + '.jpg') if hasattr(sys, '_MEIPASS') else '../YGO Card Images/' + str(self.items[card_name]) + '.jpg').resize((514, 750))
        photo = ImageTk.PhotoImage(img)
    except FileNotFoundError:
        print("Error: Image file not found.")
        exit()
    image_label = tk.Label(card_image, image=photo)
    image_label.pack()
    image_label.image = photo

def onLeave(self, card_image, card_name):
    clear_window(card_image)
    try:
        img = Image.open(os.path.join(sys._MEIPASS, '../YGO Card Images/' + str(self.items[card_name]) + '.jpg') if hasattr(sys, '_MEIPASS') else '../YGO Card Images/' + str(self.items[card_name]) + '.jpg').resize((514, 750))
        photo = ImageTk.PhotoImage(img)
    except FileNotFoundError:
        print("Error: Image file not found.")
        exit()
    image_label = tk.Label(card_image, image=photo)
    image_label.pack()
    image_label.image = photo

class VirtualListbox(tk.Canvas):
    def __init__(self, master, items, **kwargs):
        super().__init__(master, **kwargs)
        self.items = items
        self.click_counts = {item: 0 for item in items}
        self.num_visible = 30  # Number of items to display at once
        self.item_height = 20
        self.config(width=200, height=self.num_visible * self.item_height)
        self.scroll_y = tk.Scrollbar(master, command=self.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.config(yscrollcommand=self.scroll_y.set)
        self.bind("<MouseWheel>", self.on_mousewheel)
        self.viewable_start = 0
        self.update_list()

    def update_list(self):
        self.delete("all")
        clear_window(self)
        for i, item in enumerate(sorted(list(self.items))[self.viewable_start:self.viewable_start + self.num_visible]):
            y = i * self.item_height
            self.create_text(10, y + self.item_height // 2, text=item, anchor=tk.W, tags=''.join(e for e in item if e.isalnum()))
            self.tag_bind(''.join(e for e in item if e.isalnum()), "<Button-1>", lambda event, itm=item: on_item_click(self, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), "<Button-3>", lambda event, itm=item: on_item_right_click(self, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), '<Enter>', lambda event, itm=item: onEnter(self, root.card_image, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), '<Leave>', lambda event, itm=item: onLeave(self, root.card_image, itm))
        self.config(scrollregion=(0, 0, 0, len(self.items) * self.item_height))

    def yview(self, *args):
        if args:
            if args[0] == "moveto":
                self.viewable_start = int(float(args[1]) * (len(self.items) - self.num_visible))
            elif args[0] == "scroll":
                delta = int(args[1])
                self.viewable_start = max(0, min(self.viewable_start + delta, len(self.items) - self.num_visible))
            self.update_list()
            self.scroll_y.set(self.viewable_start / len(self.items), (self.viewable_start + self.num_visible) / len(self.items))

    def on_mousewheel(self, event):
         self.yview("scroll", -1 if event.delta > 0 else 1, "units")

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Red-Eyes Black Duel Simulator')
    messagebox.showinfo("Main deck", "Construct a main deck consisting of 40-60 cards.")
    root.main_deck_card_count = 0
    button = tk.Button(root, text="Submit main deck", command=partial(on_button_click, root))
    button.pack()
    root.main_deck_cards = tk.Toplevel()
    root.main_deck_cards.title("Cards (main deck)")
    root.main_deck_cards.withdraw()
    button2 = tk.Button(root, text="Show/hide main deck cards", command=partial(toggle_toplevel, root.main_deck_cards))
    button2.pack()
    root.listbox_window = tk.Toplevel()
    root.listbox_window.title("Main deck")
    root.listbox = tk.Listbox(root.listbox_window, width=50, height=35)
    root.listbox.pack()
    button3 = tk.Button(root, text="Show/hide main deck", command=partial(toggle_toplevel, root.listbox_window))
    button3.pack()
    root.listbox_window.withdraw()
    root.card_image = tk.Toplevel()
    root.card_image.title("Card image")
    button4 = tk.Button(root, text="Show/hide card images", command=partial(toggle_toplevel, root.card_image))
    button4.pack()
    root.card_image.withdraw()
    root.item_dict = OrderedDict()
    root.main_deck_card_count = 0
    card_info_data = open('src/YGOProDeck_Card_Info.json')
    card_info_data = json.load(card_info_data)
    items = {}
    for data in card_info_data['data']:
        card_name = data['name']
        card_id = data['id']
        if card_name == '7':
            card_name = 'Seven'
        items.update({card_name: card_id})
    virtual_listbox = VirtualListbox(root, items)
    virtual_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    root.mainloop()