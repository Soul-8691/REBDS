# Open tkinter window
# Choose your main deck from a list of cards
# Choose your extra deck from a list of cards
# Choose your side deck from a list of cards
# Display currently selected cards in a list
# Be able to remove cards from deck
# Be able to submit deck
# Game starts (pygame)
# Cards slide into view
# Cards displayed using pygame
# You control both sides
# Side view switches when ready
# You can select your card
# You have a list of actions to take upon selecting your card

import tkinter as tk
import json
from functools import partial
from tkinter import messagebox
from collections import OrderedDict

open('src/main_deck.json', 'w').close()

def update_json_file(file_path, new_data):
    try:
        with open(file_path, 'w+') as file:
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
    if self.main_deck_card_count == 60:
            messagebox.showinfo("Main deck full", "You have reached the main deck card limit. Please either submit your deck or remove cards.")
    elif self.click_counts[item] == 3:
        messagebox.showinfo("Card limit reached", "You have reached the 3 card limit, already.")
    else:
        self.click_counts[item] += 1
        update_json_file('main_deck.json', {item: self.click_counts[item]})
        self.main_deck_card_count += 1
        self.item_dict.update({item: self.click_counts[item]})
        self.listbox.delete(0, tk.END)
        for item in self.item_dict:
            if self.click_counts[item] > 0:
                self.listbox.insert(tk.END, item + ': ' + str(self.item_dict[item]))

def on_item_right_click(self, item):
    if self.main_deck_card_count == 0:
            messagebox.showinfo("Card not in deck", "This card cannot be removed because it is not in your deck, already.")
    else:
        self.click_counts[item] -= 1
        update_json_file('main_deck.json', {item: self.click_counts[item]})
        self.main_deck_card_count -= 1
        self.item_dict.update({item: self.click_counts[item]})
        self.listbox.delete(0, tk.END)
        for item in self.item_dict:
            if self.click_counts[item] > 0:
                self.listbox.insert(tk.END, item + ': ' + str(self.item_dict[item]))

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
        self.main_deck_card_count = 0
        self.listbox_window = tk.Toplevel()
        self.listbox_window.title("Main deck")
        self.listbox = tk.Listbox(self.listbox_window, width=100, height=35)
        self.listbox.pack()
        self.item_dict = OrderedDict()
        self.update_list()

    def update_list(self):
        self.delete("all")
        for i, item in enumerate(self.items[self.viewable_start:self.viewable_start + self.num_visible]):
            y = i * self.item_height
            self.create_text(10, y + self.item_height // 2, text=item, anchor=tk.W, tags=''.join(e for e in item if e.isalnum()))
            self.tag_bind(''.join(e for e in item if e.isalnum()), "<Button-1>", lambda event, itm=item: on_item_click(self, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), "<Button-3>", lambda event, itm=item: on_item_right_click(self, itm))
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
    card_info_data = open('src/YGOProDeck_Card_Info.json')
    card_info_data = json.load(card_info_data)
    items = []
    for data in card_info_data['data']:
        card_name = data['name']
        if card_name == '7':
            card_name = 'Seven'
        items.append(card_name)
    virtual_listbox = VirtualListbox(root, items)
    virtual_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    root.mainloop()