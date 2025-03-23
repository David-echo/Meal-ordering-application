import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# 商品数据 (支持 .jpg/.jpeg/.png)
data = [
    ("../img/a.jpeg", "苹果", "¥5.99"),
    ("../img/b.jpeg", "香蕉", "¥3.49"),
    ("../img/c.jpeg", "樱桃", "¥8.99"),
    ("../img/d.jpeg", "葡萄", "¥6.79"),
]

# style = ttk.Style()
# style.configure("Treeview", rowheight=60)  # 设置行高为 60px
# 图片缓存，防止 Tkinter 回收图片
image_cache = {}


def load_image(img_path, size=(60, 60)):
    """ 加载图片并调整大小，确保所有图片大小一致 """
    try:
        img = Image.open(img_path).convert("RGBA")  # 统一转换格式
        img = img.resize(size, Image.Resampling.LANCZOS)  # 调整大小 (LANCZOS 适用于高质量缩放)
        img_tk = ImageTk.PhotoImage(img)
        image_cache[img_path] = img_tk  # 缓存图片，防止 Tkinter 回收
        return img_tk
    except Exception as e:
        print(f"无法加载图片 {img_path}: {e}")
        return None


def load_data():
    """ 加载商品数据到表格 """
    for item in main_tree.get_children():
        main_tree.delete(item)  # 清空旧数据

    for img_path, name, price in data:
        img = load_image(img_path)  # 读取图片
        if img:
            main_tree.insert("", "end", image=img, values=(name, price))


def on_double_click(event):
    """ 双击商品，将数据添加到购物车 """
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

# 商品表格 (显示图片 + 商品名称 + 价格)
columns = ("Name", "Price")
main_tree = ttk.Treeview(root, columns=columns, show="tree headings", height=6)
main_tree.column("Name", width=150)
main_tree.column("Price", width=100)

# 第一列用于显示图片
main_tree.column("#0", width=60, minwidth=60, stretch=False)
main_tree.heading("#0", text="图片")
main_tree.heading("Name", text="商品名称")
main_tree.heading("Price", text="价格")

# 绑定双击事件
main_tree.bind("<Double-1>", on_double_click)
main_tree.pack(pady=10)

# 加载数据按钮
btn_load = tk.Button(root, text="加载商品", command=load_data)
btn_load.pack()

# 购物车表格
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
