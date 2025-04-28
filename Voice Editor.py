# -*- coding: utf-8 -*-
from tkinter import *
import os
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import play
from tkinter import filedialog

class MovableRectangle:
    def __init__(self, canvas, x1, y1, x2, y2, grid_size=20):
        self.canvas = canvas
        self.grid_size = grid_size
        x1 = round(x1 / grid_size) * grid_size
        y1 = round(y1 / grid_size) * grid_size
        x2 = round(x2 / grid_size) * grid_size
        y2 = round(y2 / grid_size) * grid_size
        
        self.rect = canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black", width=2)
        self.inputbox = Text(canvas, font=("Arial", 12), height=1, width=4)
        self.inputbox.insert(1.0, "あ")
        self.window = canvas.create_window(x1, y1, window=self.inputbox, anchor=NW)
        self.canvas.tag_bind(self.rect, "<Button-1>", self.select)
        self.canvas.tag_bind(self.rect, "<B1-Motion>", self.move)
        self.canvas.tag_bind(self.rect, "<ButtonRelease-1>", self.deselect)
        self.canvas.tag_bind(self.rect, "<Enter>", self.on_hover)
        self.canvas.tag_bind(self.rect, "<Leave>", self.on_leave)
        
        self.selected = False
        self.offset_x = 0
        self.offset_y = 0
        self.hovering_edge = False
        self.resizing = False  # 是否正在调整宽度
        self.resize_edge = None  # 正在调整哪一侧的边缘
    
    def select(self, event):
        coords = self.canvas.coords(self.rect)
        edge_threshold = 5
        
        # 检查是否碰到左边缘
        if abs(event.x - coords[0]) < edge_threshold:
            self.resizing = True
            self.resize_edge = "left"
            self.canvas.config(cursor="sb_h_double_arrow")
        # 检查是否碰到右边缘
        elif abs(event.x - coords[2]) < edge_threshold:
            self.resizing = True
            self.resize_edge = "right"
            self.canvas.config(cursor="sb_h_double_arrow")
        else:
            self.selected = True
            self.resizing = False
            self.offset_x = event.x - coords[0]
            self.offset_y = event.y - coords[1]
            self.update_text_position()  # 更新文字位置
    
    def move(self, event):
        if self.resizing:
            coords = self.canvas.coords(self.rect)
            new_x = round(event.x / self.grid_size) * self.grid_size
            print("resizing")
            if self.resize_edge == "left":
                # 保持右边缘不变，调整左边缘
                if new_x > coords[0] + 20:  # 确保宽度最小为20（兩格）
                    self.canvas.coords(self.rect, new_x, coords[1], coords[2], coords[3])
                    self.canvas.coords(self.window, new_x, coords[1])
            elif self.resize_edge == "right":
                # 保持左边缘不变，调整右边缘
                if new_x > coords[0] + 20:  # 确保宽度最小为20（兩格）
                    self.canvas.coords(self.rect, coords[0], coords[1], new_x, coords[3])
                    self.canvas.coords(self.window, coords[0], coords[1])
            self.update_text_position()  # 更新文字位置
        elif self.selected:
            new_x = round((event.x - self.offset_x) / self.grid_size) * self.grid_size
            new_y = round((event.y - self.offset_y) / self.grid_size) * self.grid_size
            
            rect_coords = self.canvas.coords(self.rect)
            width = rect_coords[2] - rect_coords[0]
            height = rect_coords[3] - rect_coords[1]
            
            if new_y < 25*10 and new_y > -15 and new_x < 25*800 and new_x > -15:
                self.canvas.coords(self.rect, new_x, new_y, new_x + width, new_y + height)
                self.canvas.coords(self.window, new_x, new_y)
                self.update_text_position()  # 更新文字位置
    
    def deselect(self, event):
        self.selected = False
        self.resizing = False
        self.resize_edge = None
        self.canvas.config(cursor="")
    
    def on_hover(self, event):
        coords = self.canvas.coords(self.rect)
        edge_threshold = 5
        
        if abs(event.x - coords[0]) < edge_threshold or abs(event.x - coords[2]) < edge_threshold:
            self.canvas.config(cursor="sb_h_double_arrow")
            self.hovering_edge = True
            self.canvas.itemconfig(self.rect, outline="red", width=3)
        else:
            self.hovering_edge = False
            self.canvas.itemconfig(self.rect, outline="black", width=2)
    
    def on_leave(self, event):
        self.hovering_edge = False
        if not self.selected:
            self.canvas.itemconfig(self.rect, outline="black", width=2)
        self.canvas.config(cursor="")
    
    def update_text_position(self):  # 更新文字位置
        rect_coords = self.canvas.coords(self.rect)
        x = rect_coords[0]  # 左上角的x坐标
        y = rect_coords[1]  # 左上角的y坐标
        self.canvas.coords(self.window, x, y)

    def update_textbox_size(self, x1, x2):
        # 更新Text组件的宽度
        new_width = max(10, int((x2 - x1) / self.grid_size))  # 确保最小宽度为10
        self.inputbox.config(width=new_width)

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=BOTH, expand=True)
        self.main()
    
    def main(self):
        # 创建主菜单
        self.mainmenu = Menu(self.master)
        self.master.config(menu=self.mainmenu)
        
        # 文件菜单
        self.filemenu = Menu(self.mainmenu, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.filemenu.add_command(label="Save", command=self.save_file)
        self.filemenu.add_command(label="Save As", command=self.save_as_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.master.quit)
        self.mainmenu.add_cascade(label="File", menu=self.filemenu)
        
        # 编辑菜单
        self.editmenu = Menu(self.mainmenu, tearoff=0)
        self.editmenu.add_command(label="Cut", command=self.cut)
        self.editmenu.add_command(label="Copy", command=self.copy)
        self.editmenu.add_command(label="Paste", command=self.paste)
        self.mainmenu.add_cascade(label="Edit", menu=self.editmenu)
        
        # 播放菜单
        self.playmenu = Menu(self.mainmenu, tearoff=0)
        self.playmenu.add_command(label="Start Voice", command=self.start_voice)
        self.mainmenu.add_cascade(label="Play", menu=self.playmenu)
        
        # 帮助菜单
        self.helpmenu = Menu(self.mainmenu, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.about)
        self.mainmenu.add_cascade(label="Help", menu=self.helpmenu)
        
        # 创建列表框
        self.voice = ["默認"]
        self.now_voive = StringVar()
        self.now_voive.set("默認")
        self.voice_list = OptionMenu(self.master, self.now_voive, *self.voice)
        self.voice_list.pack()
        self.voice_list.config(width=10)
        
        # 创建画布和滚动条
        self.canvas = Canvas(self.master, bg="white", scrollregion=(0, 0, 10000, 10000))
        self.canvas.pack( fill=BOTH, expand=True)
        self.hbar = ttk.Scrollbar(self.master, orient=HORIZONTAL)
        self.hbar.pack(fill=X)
        self.hbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.hbar.set)
        
        # 绘制网格
        self.grid_size = 20
        self.draw_grid()

        # 存储可移动矩形的列表
        self.rectangles = []
        
        # 工具菜单 - 新增的网格工具菜单
        self.toolsmenu = Menu(self.mainmenu, tearoff=0)
        self.toolsmenu.add_command(label="Add Voice", command=self.add_voice)
        self.mainmenu.add_cascade(label="Tools", menu=self.toolsmenu)
    
    def draw_grid(self):
        # 绘制网格线
        for x in range(0, 25*800, self.grid_size):
            self.canvas.create_line(x, 0, x, 25*11.2, fill="lightgray")
        for y in range(0, 25*12, self.grid_size):
            self.canvas.create_line(0, y, 25*800, y, fill="lightgray")
    
    def add_voice(self):
        # 在画布中央添加一个默认大小的矩形
        rect = MovableRectangle(self.canvas, 300, 200, 400, 225, self.grid_size)
        self.rectangles.append(rect)
        print(self.rectangles)
    
    def open_file(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("ve files", "*.ve"), ("ve json files", "*.json"), ("All files", "*.*")))
        if filename:
            with open(filename, "r") as file:
                self.text.delete(1.0, END)
                self.text.insert(1.0, file.read())
            # self.statusbar.config(text=f"Opened {filename}")  # 移除未定义的状态栏
    
    def save_file(self):
        if not hasattr(self, 'filename') or not self.filename:
            self.save_as_file()
            return
        
        try:
            with open(self.filename, "w") as file:
                file.write(self.text.get(1.0, END))
            # self.statusbar.config(text=f"Saved {self.filename}")  # 移除未定义的状态栏
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
            
    def save_as_file(self):
        filename = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save as file", filetypes=(("Ve project files", "*.ve"), ("Ve Json files", "*.json"), ("All files", "*.*")))
        if filename:
            with open(filename, "w") as file:
                file.write(self.text.get(1.0, END))
            self.filename = filename
            # self.statusbar.config(text=f"Saved {filename}")  # 移除未定义的状态栏

    def start_voice(self):
        play.play_voice(self.text.get(1.0, END), self.now_voive.get(), 1)

    def cut(self):
        self.text.event_generate("<<Cut>>")
    
    def copy(self):
        self.text.event_generate("<<Copy>>")
    
    def paste(self):
        self.text.event_generate("<<Paste>>")
    
    def about(self):
        messagebox.showinfo("About", "Voice Editor 0.1\n\nCreated by Lifua\n\nhttps://github.com/lifua")

root = Tk()
root.title("Voice Editor 0.13 with Movable Rectangle")
root.geometry("1280x720")
app = Application(root)
root.mainloop()
