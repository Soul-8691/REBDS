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
open('src/extra_deck.json', 'w').close()
open('src/side_deck.json', 'w').close()

# Update entry box with listbox clicked
def fillout(my_entry, my_list, e):
	# Delete whatever is in the entry box
	my_entry.delete(0, tk.END)

	# Add clicked list item to entry box
	my_entry.insert(0, my_list.get(tk.ANCHOR))

# Create function to check entry vs listbox
def check(my_entry, items, e):
    typed = my_entry.get()
    root.card_var = typed

    if typed == '':
        filtered = list(items.keys())  # Show all items if search bar is empty
    else:
        filtered = [item for item in items.keys() if typed.lower() in item.lower()]

    if filtered:
        root.virtual_listbox.items_to_show = filtered
        root.virtual_listbox.viewable_start = 0
        root.virtual_listbox.update_list()
        root.virtual_listbox.focus_set()  # Keep focus on the listbox
    else:
        root.virtual_listbox.items_to_show = list(items.keys())  # Reset if no match
        root.virtual_listbox.update_list()

    # Give focus back to the entry box
    my_entry.focus_set()


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
    if root.card_count == 60:
            messagebox.showinfo("Main deck full", "You have reached the main deck card limit. Please either submit your deck or remove cards.")
    elif root.click_counts[item] == 3:
        messagebox.showinfo("Card limit reached", "You have reached the 3 card limit, already.")
    else:
        root.click_counts[item] += 1
        update_json_file('src/main_deck.json', {item: root.click_counts[item]})
        root.card_count += 1
        root.item_dict.update({item: root.click_counts[item]})
        root.listbox.delete(0, tk.END)
        root.listbox.insert(0, 'Cards in deck: ' + str(root.card_count))
        for item in sorted(list(root.item_dict)):
            if root.click_counts[item] > 0:
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
    if root.click_counts[item] == 0:
            messagebox.showinfo("Card not in deck", "This card cannot be removed because it is not in your deck, already.")
    else:
        root.click_counts[item] -= 1
        update_json_file('src/main_deck.json', {item: root.click_counts[item]})
        root.card_count -= 1
        root.item_dict.update({item: root.click_counts[item]})
        root.listbox.delete(0, tk.END)
        root.listbox.insert(0, 'Cards in deck: ' + str(root.card_count))
        for item in sorted(list(root.item_dict)):
            if root.click_counts[item] > 0:
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

def on_item_click_side_deck(self, item):
    clear_window(root.side_deck_cards)
    if root.side_deck_card_count == 15:
            messagebox.showinfo("Side deck full", "You have reached the side deck card limit. Please either submit your side deck or remove cards.")
    elif root.click_counts[item] == 3:
        messagebox.showinfo("Card limit reached", "You have reached the 3 card limit, already.")
    else:
        root.click_counts[item] += 1
        root.side_deck_click_counts[item] += 1
        update_json_file('src/side_deck.json', {item: root.click_counts[item]})
        root.side_deck_card_count += 1
        root.item_dict_side_deck.update({item: root.side_deck_click_counts[item]})
        root.listbox_side_deck.delete(0, tk.END)
        root.listbox_side_deck.insert(0, 'Cards in main deck:')
        for item in sorted(list(root.item_dict)):
            if root.click_counts[item] > 0:
                root.listbox_side_deck.insert(tk.END, item + ': ' + str(root.item_dict[item]))
        root.listbox_side_deck.insert(tk.END, 'Cards in extra deck:')
        for item in sorted(list(root.item_dict_extra_deck)):
            if root.extra_deck_click_counts[item] > 0:
                root.listbox_side_deck.insert(tk.END, item + ': ' + str(root.item_dict_extra_deck[item]))
        root.listbox_side_deck.insert(tk.END, 'Cards in side deck: ' + str(root.side_deck_card_count))
        for item in sorted(list(root.item_dict_side_deck)):
            if root.side_deck_click_counts[item] > 0:
                root.listbox_side_deck.insert(tk.END, item + ': ' + str(root.item_dict_side_deck[item]))
    i = 0
    for item in sorted(list(Counter(root.item_dict_side_deck).elements())):
        try:
            img = Image.open(os.path.join(sys._MEIPASS, '../YGO Card Images/' + str(self.items[item]) + '.jpg') if hasattr(sys, '_MEIPASS') else '../YGO Card Images/' + str(self.items[item]) + '.jpg').resize((110, 159))
            photo = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print("Error: Image file not found.")
            exit()
        image_label = tk.Label(root.side_deck_cards, image=photo)
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

def on_item_right_click_side_deck(self, item):
    clear_window(root.side_deck_cards)
    if root.side_deck_click_counts[item] == 0:
            messagebox.showinfo("Card not in deck", "This card cannot be removed because it is not in your side deck, already.")
    else:
        root.click_counts[item] -= 1
        root.side_deck_click_counts[item] -= 1
        update_json_file('src/side_deck.json', {item: root.click_counts[item]})
        root.side_deck_card_count -= 1
        root.item_dict_side_deck.update({item: root.click_counts_side_deck[item]})
        root.listbox_side_deck.delete(0, tk.END)
        root.listbox_side_deck.insert(0, 'Cards in main deck:')
        for item in sorted(list(root.item_dict)):
            if root.click_counts[item] > 0:
                root.listbox_side_deck.insert(tk.END, item + ': ' + str(root.item_dict[item]))
        root.listbox_side_deck.insert(tk.END, 'Cards in extra deck:')
        for item in sorted(list(root.item_dict_extra_deck)):
            if root.extra_deck_click_counts[item] > 0:
                root.listbox_side_deck.insert(tk.END, item + ': ' + str(root.item_dict_extra_deck[item]))
        root.listbox_side_deck.insert(tk.END, 'Cards in side deck: ' + str(root.side_deck_card_count))
        for item in sorted(list(root.item_dict_side_deck)):
            if root.click_counts_side_deck[item] > 0:
                root.listbox_side_deck.insert(tk.END, item + ': ' + str(root.item_dict_side_deck[item]))
        i = 0
        for item in sorted(list(Counter(root.item_dict_side_deck).elements())):
            try:
                img = Image.open(os.path.join(sys._MEIPASS, '../YGO Card Images/' + str(self.items[item]) + '.jpg') if hasattr(sys, '_MEIPASS') else '../YGO Card Images/' + str(self.items[item]) + '.jpg').resize((110, 159))
                photo = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                print("Error: Image file not found.")
                exit()
            image_label = tk.Label(root.side_deck_cards, image=photo)
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

def on_item_click_extra_deck(self, item):
    clear_window(root.extra_deck_cards)
    if root.extra_deck_card_count == 15:
            messagebox.showinfo("Extra deck full", "You have reached the extra deck card limit. Please either submit your extra deck or remove cards.")
    elif root.click_counts[item] == 3:
        messagebox.showinfo("Card limit reached", "You have reached the 3 card limit, already.")
    else:
        root.click_counts[item] += 1
        root.extra_deck_click_counts[item] += 1
        update_json_file('src/extra_deck.json', {item: root.click_counts[item]})
        root.extra_deck_card_count += 1
        root.item_dict_extra_deck.update({item: root.extra_deck_click_counts[item]})
        root.listbox_extra_deck.delete(0, tk.END)
        root.listbox_extra_deck.insert(0, 'Cards in main deck:')
        for item in sorted(list(root.item_dict)):
            if root.click_counts[item] > 0:
                root.listbox_extra_deck.insert(tk.END, item + ': ' + str(root.item_dict[item]))
        root.listbox_extra_deck.insert(tk.END, 'Cards in extra deck: ' + str(root.extra_deck_card_count))
        for item in sorted(list(root.item_dict_extra_deck)):
            if root.extra_deck_click_counts[item] > 0:
                root.listbox_extra_deck.insert(tk.END, item + ': ' + str(root.item_dict_extra_deck[item]))
    i = 0
    for item in sorted(list(Counter(root.item_dict_extra_deck).elements())):
        try:
            img = Image.open(os.path.join(sys._MEIPASS, '../YGO Card Images/' + str(self.items[item]) + '.jpg') if hasattr(sys, '_MEIPASS') else '../YGO Card Images/' + str(self.items[item]) + '.jpg').resize((110, 159))
            photo = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print("Error: Image file not found.")
            exit()
        image_label = tk.Label(root.extra_deck_cards, image=photo)
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

def on_item_right_click_extra_deck(self, item):
    clear_window(root.extra_deck_cards)
    if root.extra_deck_click_counts[item] == 0:
            messagebox.showinfo("Card not in deck", "This card cannot be removed because it is not in your extra deck, already.")
    else:
        root.click_counts[item] -= 1
        root.extra_deck_click_counts[item] -= 1
        update_json_file('src/extra_deck.json', {item: root.click_counts[item]})
        root.extra_deck_card_count -= 1
        root.item_dict_extra_deck.update({item: root.click_counts_extra_deck[item]})
        root.listbox_extra_deck.delete(0, tk.END)
        root.listbox_extra_deck.insert(0, 'Cards in main deck:')
        for item in sorted(list(root.item_dict)):
            if root.click_counts[item] > 0:
                root.listbox_extra_deck.insert(tk.END, item + ': ' + str(root.item_dict[item]))
        root.listbox_extra_deck.insert(tk.END, 'Cards in extra deck: ' + str(root.extra_deck_card_count))
        for item in sorted(list(root.item_dict_extra_deck)):
            if root.click_counts_extra_deck[item] > 0:
                root.listbox_extra_deck.insert(tk.END, item + ': ' + str(root.item_dict_extra_deck[item]))
        i = 0
        for item in sorted(list(Counter(root.item_dict_extra_deck).elements())):
            try:
                img = Image.open(os.path.join(sys._MEIPASS, '../YGO Card Images/' + str(self.items[item]) + '.jpg') if hasattr(sys, '_MEIPASS') else '../YGO Card Images/' + str(self.items[item]) + '.jpg').resize((110, 159))
                photo = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                print("Error: Image file not found.")
                exit()
            image_label = tk.Label(root.extra_deck_cards, image=photo)
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

def clear_top_level(window_):
    for widget in window_.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.withdraw()

def clear_window(window_):
    for widget in window_.winfo_children():
        if not isinstance(widget, tk.Toplevel):
            widget.pack_forget()
            widget.grid_forget()
            widget.place_forget()
        if isinstance(widget, tk.Label):
            widget.config(image='')

def construct_side_deck_menu(self):
    messagebox.showinfo("Side deck", "Construct a side deck consisting of 0-15 cards.")
    root.side_deck_card_count = 0
    button = tk.Button(root, text="Submit side deck", command=on_button_click_side_deck)
    button.pack()
    root.side_deck_cards = tk.Toplevel()
    root.side_deck_cards.title("Cards (side deck)")
    root.side_deck_cards.withdraw()
    button2 = tk.Button(root, text="Show/hide side deck cards", command=lambda: toggle_toplevel(root.side_deck_cards))
    button2.pack()
    root.side_deck_cards.protocol("WM_DELETE_WINDOW", root.side_deck_cards.withdraw)
    root.listbox_side_deck_window = tk.Toplevel()
    root.listbox_side_deck_window.title("Side deck")
    root.listbox_side_deck = tk.Listbox(root.listbox_side_deck_window, width=50, height=35)
    root.listbox_side_deck.pack()
    button3 = tk.Button(root, text="Show/hide side deck", command=lambda: toggle_toplevel(root.listbox_side_deck_window))
    button3.pack()
    root.listbox_side_deck_window.protocol("WM_DELETE_WINDOW", root.listbox_side_deck_window.withdraw)
    root.listbox_side_deck_window.withdraw()
    root.card_image = tk.Toplevel()
    root.card_image.title("Card image")
    button4 = tk.Button(root, text="Show/hide card images", command=lambda: toggle_toplevel(root.card_image))
    button4.pack()
    root.card_image.protocol("WM_DELETE_WINDOW", root.card_image.withdraw)
    button5 = tk.Button(root, text="Show/hide main deck cards", command=lambda: toggle_toplevel(root.main_deck_cards))
    button5.pack()
    button6 = tk.Button(root, text="Show/hide extra deck cards", command=lambda: toggle_toplevel(root.extra_deck_cards))
    button6.pack()
    root.card_var=tk.StringVar()
    root.my_entry = tk.Entry(root, textvariable=root.card_var)
    root.my_entry.pack()
    root.my_entry.bind("<KeyRelease>", lambda e: check(root.my_entry, items, e))
    root.my_entry.focus_force()
    root.card_image.withdraw()
    root.item_dict_side_deck = OrderedDict()
    items = {}
    for data in root.card_info_data['data']:
        card_name = data['name']
        card_id = data['id']
        card_type = data['type']
        if card_type != 'XYZ Monster' and card_type != 'Synchro Monster' and card_type != 'Fusion Monster':
            if card_name == '7':
                card_name = 'Seven'
            items.update({card_name: card_id})
    root.side_deck_click_counts = {item: 0 for item in items}
    root.virtual_listbox = VirtualListboxSideDeck(root, items)
    root.virtual_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

def construct_extra_deck_menu(self):
    messagebox.showinfo("Extra deck", "Construct a extra deck consisting of 0-15 cards.")
    root.extra_deck_card_count = 0
    button = tk.Button(root, text="Submit extra deck", command=on_button_click_extra_deck)
    button.pack()
    root.extra_deck_cards = tk.Toplevel()
    root.extra_deck_cards.title("Cards (extra deck)")
    root.extra_deck_cards.withdraw()
    button2 = tk.Button(root, text="Show/hide extra deck cards", command=lambda: toggle_toplevel(root.extra_deck_cards))
    button2.pack()
    root.extra_deck_cards.protocol("WM_DELETE_WINDOW", root.extra_deck_cards.withdraw)
    root.listbox_extra_deck_window = tk.Toplevel()
    root.listbox_extra_deck_window.title("Extra deck")
    root.listbox_extra_deck = tk.Listbox(root.listbox_extra_deck_window, width=50, height=35)
    root.listbox_extra_deck.pack()
    button3 = tk.Button(root, text="Show/hide extra deck", command=lambda: toggle_toplevel(root.listbox_extra_deck_window))
    button3.pack()
    root.listbox_extra_deck_window.protocol("WM_DELETE_WINDOW", root.listbox_extra_deck_window.withdraw)
    root.listbox_extra_deck_window.withdraw()
    root.card_image = tk.Toplevel()
    root.card_image.title("Card image")
    button4 = tk.Button(root, text="Show/hide card images", command=lambda: toggle_toplevel(root.card_image))
    button4.pack()
    root.card_image.protocol("WM_DELETE_WINDOW", root.card_image.withdraw)
    button5 = tk.Button(root, text="Show/hide main deck cards", command=lambda: toggle_toplevel(root.main_deck_cards))
    button5.pack()
    root.card_var=tk.StringVar()
    root.my_entry = tk.Entry(root, textvariable=root.card_var)
    root.my_entry.pack()
    root.my_entry.bind("<KeyRelease>", lambda e: check(root.my_entry, items, e))
    root.my_entry.focus_force()
    root.card_image.withdraw()
    root.item_dict_extra_deck = OrderedDict()
    items = {}
    for data in root.card_info_data['data']:
        card_name = data['name']
        card_id = data['id']
        card_type = data['type']
        if card_type == 'XYZ Monster' or card_type == 'Synchro Monster' or card_type == 'Fusion Monster':
            items.update({card_name: card_id})
    root.extra_deck_click_counts = {item: 0 for item in items}
    root.virtual_listbox = VirtualListboxExtraDeck(root, items)
    root.virtual_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

def hide_button(self):
    self.pack_forget()

def on_button_click():
    if root.card_count < 1:
        messagebox.showinfo("Invalid deck size", "Your deck needs to consist of 40-60 cards.")
    else:
        messagebox.showinfo("Deck submitted", "Your deck is legal! Deck submitted.")
        clear_window(root)
        clear_top_level(root)
        construct_extra_deck_menu(root)

def on_button_click_extra_deck():
    messagebox.showinfo("Extra deck submitted", "Your extra deck is legal! Deck submitted.")
    clear_window(root)
    clear_top_level(root)
    construct_side_deck_menu(root)

def on_button_click_side_deck():
    messagebox.showinfo("Side deck submitted", "Your deck is legal! Deck submitted.")
    clear_window(root)
    clear_top_level(root)
    export = messagebox.askyesno("Export to YDK?", "Do you want to export to YDK format?")
    if export:
        root.deck_var=tk.StringVar()
        root.ydk = tk.Entry(root, textvariable=root.deck_var)
        root.ydk.pack()
        root.ydk.bind("<Return>", on_enter)
        root.ydk.focus_force()

def on_enter(self):
    open('src/' + root.ydk.get() + '.ydk', 'w').close()
    root.ydk_file = open('src/' + root.ydk.get() + '.ydk', 'r+', encoding='utf8')
    root.ydk_file.write('#main\n')
    for card_name in sorted(list(root.item_dict)):
        root.ydk_file.write(str(root.items[card_name]) + '\n')
    root.ydk_file.write('#extra\n')
    for card_name in sorted(list(root.item_dict_extra_deck)):
        root.ydk_file.write(str(root.items[card_name]) + '\n')
    root.ydk_file.write('!side\n')
    for card_name in sorted(list(root.item_dict_side_deck)):
        root.ydk_file.write(str(root.items[card_name]) + '\n')

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
        self.items_to_show = list(items)
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
        for i, item in enumerate(sorted(self.items_to_show)[self.viewable_start:self.viewable_start + self.num_visible]):
            y = i * self.item_height
            self.create_text(10, y + self.item_height // 2, text=item, anchor=tk.W, tags=''.join(e for e in item if e.isalnum()))
            self.tag_bind(''.join(e for e in item if e.isalnum()), "<Button-1>", lambda event, itm=item: on_item_click(self, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), "<Button-3>", lambda event, itm=item: on_item_right_click(self, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), '<Enter>', lambda event, itm=item: onEnter(self, root.card_image, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), '<Leave>', lambda event, itm=item: onLeave(self, root.card_image, itm))
        self.config(scrollregion=(0, 0, 0, len(self.items_to_show) * self.item_height))

    def yview(self, *args):
        if args:
            if args[0] == "moveto":
                self.viewable_start = int(float(args[1]) * (len(self.items_to_show) - self.num_visible))
            elif args[0] == "scroll":
                delta = int(args[1])
                self.viewable_start = max(0, min(self.viewable_start + delta, len(self.items_to_show) - self.num_visible))
            self.update_list()
            self.scroll_y.set(self.viewable_start / len(self.items_to_show), (self.viewable_start + self.num_visible) / len(self.items_to_show))

    def on_mousewheel(self, event):
         self.yview("scroll", -1 if event.delta > 0 else 1, "units")

class VirtualListboxSideDeck(tk.Canvas):
    def __init__(self, master, items, **kwargs):
        super().__init__(master, **kwargs)
        self.items = items
        self.items_to_show = list(items)
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
        for i, item in enumerate(sorted(self.items_to_show)[self.viewable_start:self.viewable_start + self.num_visible]):
            y = i * self.item_height
            self.create_text(10, y + self.item_height // 2, text=item, anchor=tk.W, tags=''.join(e for e in item if e.isalnum()))
            self.tag_bind(''.join(e for e in item if e.isalnum()), "<Button-1>", lambda event, itm=item: on_item_click_side_deck(self, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), "<Button-3>", lambda event, itm=item: on_item_right_click_side_deck(self, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), '<Enter>', lambda event, itm=item: onEnter(self, root.card_image, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), '<Leave>', lambda event, itm=item: onLeave(self, root.card_image, itm))
        self.config(scrollregion=(0, 0, 0, len(self.items_to_show) * self.item_height))

    def yview(self, *args):
        if args:
            if args[0] == "moveto":
                self.viewable_start = int(float(args[1]) * (len(self.items_to_show) - self.num_visible))
            elif args[0] == "scroll":
                delta = int(args[1])
                self.viewable_start = max(0, min(self.viewable_start + delta, len(self.items_to_show) - self.num_visible))
            self.update_list()
            self.scroll_y.set(self.viewable_start / len(self.items_to_show), (self.viewable_start + self.num_visible) / len(self.items_to_show))

    def on_mousewheel(self, event):
         self.yview("scroll", -1 if event.delta > 0 else 1, "units")

class VirtualListboxExtraDeck(tk.Canvas):
    def __init__(self, master, items, **kwargs):
        super().__init__(master, **kwargs)
        self.items = items
        self.items_to_show = list(items)
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
        for i, item in enumerate(sorted(self.items_to_show)[self.viewable_start:self.viewable_start + self.num_visible]):
            y = i * self.item_height
            self.create_text(10, y + self.item_height // 2, text=item, anchor=tk.W, tags=''.join(e for e in item if e.isalnum()))
            self.tag_bind(''.join(e for e in item if e.isalnum()), "<Button-1>", lambda event, itm=item: on_item_click_extra_deck(self, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), "<Button-3>", lambda event, itm=item: on_item_right_click_extra_deck(self, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), '<Enter>', lambda event, itm=item: onEnter(self, root.card_image, itm))
            self.tag_bind(''.join(e for e in item if e.isalnum()), '<Leave>', lambda event, itm=item: onLeave(self, root.card_image, itm))
        self.config(scrollregion=(0, 0, 0, len(self.items_to_show) * self.item_height))

    def yview(self, *args):
        if args:
            if args[0] == "moveto":
                self.viewable_start = int(float(args[1]) * (len(self.items_to_show) - self.num_visible))
            elif args[0] == "scroll":
                delta = int(args[1])
                self.viewable_start = max(0, min(self.viewable_start + delta, len(self.items_to_show) - self.num_visible))
            self.update_list()
            self.scroll_y.set(self.viewable_start / len(self.items_to_show), (self.viewable_start + self.num_visible) / len(self.items_to_show))

    def on_mousewheel(self, event):
         self.yview("scroll", -1 if event.delta > 0 else 1, "units")

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Red-Eyes Black Duel Simulator')
    messagebox.showinfo("Main deck", "Construct a main deck consisting of 40-60 cards.")
    root.card_count = 0
    button = tk.Button(root, text="Submit main deck", command=on_button_click)
    button.pack()
    root.main_deck_cards = tk.Toplevel()
    root.main_deck_cards.title("Cards (main deck)")
    root.main_deck_cards.withdraw()
    button2 = tk.Button(root, text="Show/hide main deck cards", command=lambda: toggle_toplevel(root.main_deck_cards))
    button2.pack()
    root.main_deck_cards.protocol("WM_DELETE_WINDOW", root.main_deck_cards.withdraw)
    root.listbox_window = tk.Toplevel()
    root.listbox_window.title("Main deck")
    root.listbox = tk.Listbox(root.listbox_window, width=50, height=35)
    root.listbox.pack()
    button3 = tk.Button(root, text="Show/hide main deck", command=lambda: toggle_toplevel(root.listbox_window))
    button3.pack()
    root.listbox_window.protocol("WM_DELETE_WINDOW", root.listbox_window.withdraw)
    root.listbox_window.withdraw()
    root.card_image = tk.Toplevel()
    root.card_image.title("Card image")
    button4 = tk.Button(root, text="Show/hide card images", command=lambda: toggle_toplevel(root.card_image))
    button4.pack()
    root.card_image.protocol("WM_DELETE_WINDOW", root.card_image.withdraw)
    root.card_var=tk.StringVar()
    root.my_entry = tk.Entry(root, textvariable=root.card_var)
    root.my_entry.pack()
    root.card_image.withdraw()
    root.item_dict = OrderedDict()
    card_info_data = open('src/YGOProDeck_Card_Info.json')
    root.card_info_data = json.load(card_info_data)
    root.items = {}
    items_to_display = {}
    for data in root.card_info_data['data']:
        card_name = data['name']
        card_id = data['id']
        card_type = data['type']
        if card_type != 'XYZ Monster' and card_type != 'Synchro Monster' and card_type != 'Fusion Monster':
            if card_name == '7':
                card_name = 'Seven'
            items_to_display.update({card_name: card_id})
        root.items.update({card_name: card_id})
    root.my_entry.bind("<KeyRelease>", lambda e: check(root.my_entry, items_to_display, e))
    root.my_entry.focus_force()
    root.click_counts = {item: 0 for item in root.items}
    root.virtual_listbox = VirtualListbox(root, items_to_display)
    root.virtual_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    root.mainloop()