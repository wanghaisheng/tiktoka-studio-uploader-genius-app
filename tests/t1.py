# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2017
# For license see LICENSE

from ttkwidgets import CheckboxTreeview
import tkinter as tk
from tkinter import ttk

def on_checkbox_change(proxy_id):
    print(f"Checkbox {proxy_id} changed")

def delete_proxy(proxy_id):
    print(f"Proxy {proxy_id} deleted")

root = tk.Tk()

tree = CheckboxTreeview(root)
tree.pack()

tree.insert("", "end", "1", text="1")
tree.insert("1", "end", "11", text="11")
tree.insert("1", "end", "12",  text="12")
tree.insert("11", "end", "111", text="111")
tree.insert("", "end", "2", text="2")

root.mainloop()



root = tk.Tk()
tree = CheckboxTreeview(root, columns=('host', 'port', 'status', 'city', 'country', 'tags', 'network_type', 'validate_results', 'operation'))
tree.heading('#0', text='proxy No.')
tree.heading('host', text='Host')
# Add other headings similarly

# Inserting a row with checkbox and delete button
proxy_id = '123'
checkbox = ttk.Checkbutton(tree, command=lambda proxy_id=proxy_id: on_checkbox_change(proxy_id))
delete_button = ttk.Button(tree, text='Delete', command=lambda proxy_id=proxy_id: delete_proxy(proxy_id))

tree.insert("", 0, text=proxy_id, values=('example.com', 8080, 'OK', 'City', 'Country', 'tag1, tag2', 'Network', 'Results', ''), tags=('checkbox',))
tree.window_create(tree.identify_row(proxy_id), column='operation', window=delete_button)

tree.pack()
root.mainloop()
