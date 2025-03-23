import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# 测试数据 (图片路径 + 其他数据)
data = [
    ("img/a.jpeg", "Apple", "5.99"),
    ("img/b.jpeg", "Banana", "3.49"),
    ("img/c.jpeg", "Cherry", "8.99"),
    ("img/d.jpg", "Grape", "6.79"),
]

# 预处理图片 (缩略图大小)
image_cache = {}
def load_image(img_path, size=(50, 50)):
    if img_path in image_cache:
        return image_cache[img_path]
    img = Image.open(img_path).resize(size)
    img_tk = ImageTk.PhotoImage(img)
    image_cache[img_path] = img_tk
    return img_tk

def load_data():
    """加载数据到主表格"""
    for item in main_tree.get_children():
        main_tree.delete(item)  # 清空表格
    for img_path, name, price in data:
        img = load_image(img_path)
        main_tree.insert("", "end", values=(name, price), image=img)

def on_double_click(event):
    """双击主表格的某一行，将数据添加到购物车表格"""
    selected_item = main_tree.selection()
    if not selected_item:
        return
    for item in selected_item:
        values = main_tree.item(item, "values")
        cart_tree.insert("", "end", values=values)

# 创建主窗口
root = tk.Tk()
root.title("商品管理系统")
root.geometry("500x400")

# 创建表格1 (主商品表格)
columns = ("Name", "Price")
main_tree = ttk.Treeview(root, columns=columns, show="headings", height=5)
main_tree.heading("Name", text="商品名称")
main_tree.heading("Price", text="价格")
main_tree.column("Name", width=150)
main_tree.column("Price", width=100)

# 图片列
main_tree.column("#0", width=60)
main_tree.heading("#0", text="图片")

main_tree.bind("<Double-1>", on_double_click)  # 绑定双击事件
main_tree.pack(pady=10)

# 加载数据按钮
btn_load = tk.Button(root, text="加载商品", command=load_data)
btn_load.pack()

# 创建表格2 (购物车表格)
cart_label = tk.Label(root, text="购物车")
cart_label.pack()

cart_tree = ttk.Treeview(root, columns=columns, show="headings", height=5)
cart_tree.heading("Name", text="商品名称")
cart_tree.heading("Price", text="价格")
cart_tree.column("Name", width=150)
cart_tree.column("Price", width=100)
cart_tree.pack(pady=10)

# 运行主循环
root.mainloop()
