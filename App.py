import math
import time
import tkinter as tk
from functools import partial
from ImageGenerator import ImageGenerator
from PIL import Image, ImageTk, ImageGrab
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self, name, image_generator):
        super(App, self).__init__()

        self.name = name
        self.image_generator = image_generator
        self.title(self.name)
        self.geometry('%dx%d+0+0' % (self.winfo_screenwidth(), self.winfo_screenheight()))
        # change size
        self.resizable(False, False)
        self.selected_character = [0] * image_generator.population_size



    def _set_top_menu_bar(self):
        # Top menu bar
        self.menubar = tk.Menu(self)
        self.operation_menu = tk.Menu(self.menubar, tearoff=0)
        # mutiple menu
        self.menubar.add_cascade(label='Program', menu=self.operation_menu)
        # separator for drop-down menu
        self.operation_menu.add_separator()
        self.operation_menu.add_command(label='Exit', command=self.quit)
        self.configure(menu=self.menubar)



    def _set_left_frame(self):
        # Left frame show images
        # Canvas + grid
        self.left_frame = tk.Frame(self)
        self.canvas1 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=300, highlightthickness=0)
        self.canvas1.grid(row=0, column=0, columnspan=2, padx=3, pady=3)
        self.canvas2 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=300, highlightthickness=0)
        self.canvas2.grid(row=0, column=2, columnspan=2, padx=3, pady=3)
        self.canvas3 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=300, highlightthickness=0)
        self.canvas3.grid(row=0, column=4, columnspan=2, padx=3, pady=3)
        self.canvas4 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=300, highlightthickness=0)
        self.canvas4.grid(row=2, column=0, columnspan=2, padx=3, pady=3)
        self.canvas5 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=300, highlightthickness=0)
        self.canvas5.grid(row=2, column=2, columnspan=2, padx=3, pady=3)
        self.canvas6 = tk.Canvas(self.left_frame, bg="lightgrey",
                                 width=300, height=300, highlightthickness=0)
        self.canvas6.grid(row=2, column=4, columnspan=2, padx=3, pady=3)
        self.canvas_index = { 0: self.canvas1, 1: self.canvas2, 2: self.canvas3,
                              3: self.canvas4, 4: self.canvas5, 5: self.canvas6 }

        left_frame_buttons = {
            "Select": { "bg": "#AAF05A", "fg": "#000000" },
            "Save as PNG": { "bg": "#33B5E5", "fg": "#FFFFFF" }
        }
        self.canvas_btns = []
        for i in range(0, 12):
            if i % 2 == 0:
                btn_name = "Select"
            else:
                btn_name = "Save as PNG"
            btn = left_frame_buttons.get(btn_name, "Index Error")
            self.canvas_btns.append(tk.Label(self.left_frame, text=btn_name, bg=btn['bg'],
                                      fg=btn['fg'], width=16, cursor="X_cursor"))
            row = (math.ceil((i + 1) / 6) - 1) * 2 + 1
            self.canvas_btns[-1].grid(row=row, column=i%6)
        self.left_frame.pack_propagate(0)
        self.left_frame.pack(side=tk.LEFT, fill="both")




    def _enable_canvas_btns(self):
        for btn_index, btn in enumerate(self.canvas_btns):
            btn.configure(cursor="right_ptr")
            if btn_index % 2 == 0:
                btn.bind("<Button-1>", lambda e, x=btn_index/2: self._select_character(int(x)))
                btn.bind("<Enter>", lambda e: self._hover_button(e, "#94CA55"))
                btn.bind("<Leave>", lambda e: self._hover_button(e, "#AAF05A"))
            else:
                btn.bind("<Button-1>", lambda e, x=btn_index/2-0.5: self._save_Canvas(int(x)))
                btn.bind("<Enter>", lambda e: self._hover_button(e, "#51A5C3"))
                btn.bind("<Leave>", lambda e: self._hover_button(e, "#33B5E5"))



    def _hover_button(self, event, color):
        event.widget.configure(bg=color)



    def _set_right_frame(self):
        # Right frame show info and operation
        self.right_frame = tk.Frame(self, width=300, height=800)
        self.right_frame.pack_propagate(0)

        title_box = tk.Label(self.right_frame, text=self.name, wraplength=200,
                             bg="black", fg="white", padx=10, pady=10)
        title_box.pack(side=tk.TOP, fill=tk.X, padx=10)

        self.info = tk.StringVar(self.right_frame)
        self.info_box = tk.Label(self.right_frame, textvar=self.info, bg="black",
                                 fg="white", padx=10, pady=20)
        self.info_box.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        menu_title = tk.Label(self.right_frame, text="Menu", background="grey",
                              foreground="white")

        menu_space = tk.Frame(self.right_frame, width=300, height=600)
        menu_space.pack_propagate(0)

        menu_space.pack(side=tk.BOTTOM)
        menu_title.pack(side=tk.BOTTOM, fill=tk.X)

        # Set up the menu buttons
        self.buttons = {
            "Start": { "bg": "#AAF05A", "command": lambda e: self._start() },
            "Exit": { "bg": "#FFFFFF", "command": quit }
        }
        self.menu_btn = []
        for btn_name in self.buttons:
            btn = self.buttons.get(btn_name, "Index Error")
            self.menu_btn.append(tk.Label(menu_space, text=btn_name, width=300,
                                           bg=btn['bg'], height=2, bd=1, cursor="right_ptr"))
            self.menu_btn[-1].pack(side=tk.TOP)
            self.menu_btn[-1].bind("<Button-1>", btn['command'])
        self.menu_btn[0].bind("<Enter>", lambda e: self._hover_button(e, "#94CA55"))
        self.menu_btn[0].bind("<Leave>", lambda e: self._hover_button(e, "#AAF05A"))
        self.menu_btn[1].bind("<Enter>", lambda e: self.menu_btn[1].configure(bg="#B7B7B7"))
        self.menu_btn[1].bind("<Leave>", lambda e: self.menu_btn[1].configure(bg="#FFFFFF"))

        self.right_frame.pack(side=tk.RIGHT)



    def _next_generation_button(self):
        self.menu_btn[0].configure(cursor="right_ptr", text="Next Generation")
        self.menu_btn[0].bind("<Button-1>", lambda e: self._show_next_generation())



    def _show_info(self):
        self.info.set("Population Size: " + str(self.image_generator.population_size) + "\n" +
                      "Generation: " + str(self.image_generator.generation) + "\n" +
                      "Mutation Probability: " + str(self.image_generator.mutation_prob) + "\n" +
                      "Version: v1.0")



    def _show_images(self):
        self.img = []
        x = 22
        y = 22
        for character_id, character in enumerate(self.image_generator.population):
            canvas = self.canvas_index.get(character_id, "Index Error")

            pixels = self.image_generator.decode_pop(character)
            image = Image.fromarray(pixels, mode='RGB')
            self.img.append(ImageTk.PhotoImage(image))
            # the last one
            canvas.create_image(x, y, image=self.img[-1],  anchor='nw')
            print("character_id, x, y", character_id, x, y)


    def _save_Canvas(self, canvas_id):
        cv = self.canvas_index.get(canvas_id, "Index Error")
        path = "image" + str(canvas_id + 1) + "_" + str(int(time.time())) + ".png"
        
        self.img[canvas_id]._PhotoImage__photo.write(path)
        messagebox.showinfo("Export the image", "Saved the image as " + path)



    def _select_character(self, canvas_id):
        '''
        if chosen then turn 1
        when next generation turn 0
        '''
        cv = self.canvas_index.get(canvas_id, "Index Error")
        self.selected_character[canvas_id] = 1 - self.selected_character[canvas_id]
        cv.configure(highlightthickness= 3 - int(cv['highlightthickness']), highlightbackground="black")



    def _start(self):
        self.image_generator.initial_population()
        self._show_info()
        self._show_images()
        self._enable_canvas_btns()
        self._next_generation_button()



    def _show_next_generation(self):
    
        self.image_generator.next_generation(self.selected_character)
        for selected_index, value in enumerate(self.selected_character):
            #toggle the chosen one(1->0)
            if value == 1:
                self._select_character(selected_index)
        self._show_images()
        self._show_info()



if __name__ == "__main__":
    image_generator = ImageGenerator(population_size = 6, mutation_prob = 0.1)
    app = App("IEC Art Design", image_generator)
    app._set_top_menu_bar()
    app._set_left_frame()
    app._set_right_frame()
    app._show_info()

    app.mainloop()
