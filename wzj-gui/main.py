import random
import json
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import LabelFrame
from tkinter import StringVar
from PIL import Image, ImageTk


# 方块大小
card_size = 120
# 间隙大小
gap_size = 2
# 绘图起点坐标
start_x = 400
start_y = 100
# 7 * 5 方格
x_grid = 7
y_grid = 5


# 打开文件，载入json文件
def open_file():
    xxx_name = filedialog.askopenfilename(title='打开文件',
                                          filetypes=[('json', '*.json'),
                                                     ('All Files', '*')])
    # 更新Label text变量
    var.set(xxx_name)
    with open(xxx_name, 'r') as load_f:
        global card_dict
        card_dict = json.load(load_f)


# 画圆
def draw_circle(cvs, x, y, r, **kwargs):
    return cvs.create_oval(x-r, y-r, x+r, y+r, **kwargs)


# 绘图
def draw_card():
    # 这个打开文件，用的是回调函数，我暂时也不知道如何不用这个全局变量
    global card_dict
    imgs_list = []
    for i in range(y_grid):
        y1 = start_y + i * card_size
        for j in range(x_grid):
            x1 = start_x + j * card_size
            # 解析json里对应的文件名
            image_num = card_dict[str(i+1)][str(j+1)]
            image_path = "images/{}.png".format(image_num[0].upper())
            # 载入图片
            img = Image.open(image_path)
            # 重定义大小
            img = img.resize((card_size-gap_size, card_size-gap_size), Image.BILINEAR)
            # 重定义旋转
            img = img.rotate(image_num[1])
            imgs = ImageTk.PhotoImage(img)
            # 先形成一个大列表，便于后面打乱了显示或成行成列显示
            card_pos = [x1 + gap_size, y1 + gap_size, imgs]
            imgs_list.append(card_pos)
    # 为了效果好，随机显示
    random.shuffle(imgs_list)
    for item in imgs_list:
        # 以nw左上角为基准点, 先大图出现，提示一下重点，加点透明GIF，就完美了
        # img_big = ImageTk.PhotoImage(item[3])
        # cv.create_image((item[0], item[1]), anchor='nw', image=img_big, tag='tmp_resize')
        cv.create_image((item[0], item[1]), anchor='nw', image=item[2])
        draw_circle(cv, item[0] + card_size / 2, item[1] + card_size / 2, 20, width='4', outline="green",
                    tag='tmp_circle')
        cv.update()
        # 停一下
        time.sleep(0.15)
        # 删除圆圈，只作动画
        cv.delete('tmp_circle')
        # 不调用update，不会更新画布
        cv.update()
    time.sleep(10)


win = tk.Tk()
win.title('tkinter')
w = win.winfo_screenwidth()
h = win.winfo_screenheight()
win.geometry("%dx%d" % (w, h))
cv = tk.Canvas(win, bg='silver', width=w, height=h)

# 要更新label的text，要用var.set方法才行
var = StringVar()
var.set("...")
lab_fra = LabelFrame(win, height=200, width=300, text='选择文件')
lab_fra.pack(side='top', fill='both', expand=True)
btn_open = tk.Button(lab_fra, text='打开文件', command=open_file)
btn_open.grid(row=0, column=0)
btn_render = tk.Button(lab_fra, text='开始渲染', command=draw_card)
btn_render.grid(row=0, column=1)
text_label = tk.Label(lab_fra, textvariable=var)
text_label.grid(row=0, column=2)

# 画格子， 要算好横纵坐标
for i in range(y_grid):
    y1 = start_y + i * card_size
    for j in range(x_grid):
        x1 = start_x + j * card_size
        cv.create_rectangle(x1, y1, x1 + card_size, y1 + card_size)


cv.pack()
win.mainloop()