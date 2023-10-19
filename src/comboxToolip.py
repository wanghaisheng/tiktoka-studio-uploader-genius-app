import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import OnHoverTooltipBase

class ComboboxTip(OnHoverTooltipBase):
    def __init__(self, combobox_widget, hover_delay=1000):
        super(ComboboxTip, self).__init__(combobox_widget, hover_delay=hover_delay)
        self.tips = {}
        self._current_item = 0

        combobox_widget.tk.eval("""
proc callback {y} {
     event generate %(cb)s <<OnMotion>> -y $y
}

set popdown [ttk::combobox::PopdownWindow %(cb)s]
bind $popdown.f.l <Motion> {callback %%y}
""" % ({"cb": combobox_widget}))

        self._id4 = combobox_widget.bind("<<OnMotion>>", self._on_motion)

    def _on_motion(self, event):
        current_item = int(self.anchor_widget.tk.eval("$popdown.f.l nearest %i" % event.y))
        if current_item != self._current_item:
            self._current_item = current_item
            self.hidetip()
            if current_item in self.tips:
                self.schedule()
            else:
                self.unschedule()

    def __del__(self):
        try:
            self.anchor_widget.unbind("<<OnMotion>>", self._id4)
        except tk.TclError:
            pass
        super(ComboboxTip, self).__del__()

    def add_tooltip(self, index, text):
        self.tips[index] = text

    def get_position(self):
        """choose a screen position for the tooltip"""
        try:
            h = self.anchor_widget.winfo_height()
            bbox = self.anchor_widget._getints(self.anchor_widget.tk.eval("$popdown.f.l bbox %i" % self._current_item))
            return bbox[0] + bbox[2], bbox[1] + bbox[-1] + h
        except Exception:
            return 20, self.anchor_widget.winfo_height() + 1

    def showcontents(self):
        label = tk.Label(self.tipwindow, text=self.tips[self._current_item], justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1)
        label.pack()
