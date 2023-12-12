class pseudo_example():

    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(100, 100)


    def app(self,):
        self.start_button = tk.Button(self.root, text="start", command=lambda: self.create_await_funct())
        self.start_button.pack()

        self.testfield = tk.Label(self.root, text="output")
        self.testfield.pack()
        self.root.mainloop()

    def create_await_funct(self):
        threading.Thread(target=lambda loop: loop.run_until_complete(self.await_funct()),
                         args=(asyncio.new_event_loop(),)).start()
        self.start_button["relief"] = "sunken"
        self.start_button["state"] = "disabled"

    async def await_funct(self):
        self.testfield["text"] = "start waiting"
        self.root.update_idletasks()

        await asyncio.sleep(2)

        self.testfield["text"] = "end waiting"
        self.root.update_idletasks()

        await asyncio.sleep(1)

        self.testfield["text"] = "output"
        self.root.update_idletasks()
        self.start_button["relief"] = "raised"
        self.start_button["state"] = "normal"


if __name__ == '__main__':
    pseudo_example().app()