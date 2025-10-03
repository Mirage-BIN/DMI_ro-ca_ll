import tkinter as tk
from tkinter import font, ttk
import random
import time
import os
import sys
from PIL import Image, ImageTk
import webbrowser

class LotteryNamePicker:
    def __init__(self):
        # 创建主窗口但不显示
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口
        
        # 设置窗口图标
        try:
            icon_path = os.path.join("picture", "logo.png")
            if os.path.exists(icon_path):
                icon_image = Image.open(icon_path)
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(False, icon_photo)
                self.root.tk.call('wm', 'iconphoto', self.root._w, icon_photo)
        except Exception as e:
            print(f"设置图标失败: {e}")
        
        # 创建仅包含按钮的顶级窗口
        self.button_window = tk.Toplevel(self.root)
        self.button_window.overrideredirect(True)  # 移除窗口边框
        self.button_window.attributes('-topmost', True)  # 始终置顶
        self.button_window.attributes('-alpha', 0.5)  # 50%透明度
        
        # 设置窗口大小和位置
        self.button_window.geometry("80x40+50+50")
        
        # 尝试设置图标
        try:
            if os.path.exists(icon_path):
                button_icon = Image.open(icon_path)
                button_icon = button_icon.resize((16, 16), Image.Resampling.LANCZOS)
                self.button_icon_photo = ImageTk.PhotoImage(button_icon)
        except:
            self.button_icon_photo = None
        
        # 尝试设置字体
        self.family = "微软雅黑"
        try:
            test_font = font.Font(family="HarmonyOS Sans SC")
            self.family = "HarmonyOS Sans SC"
        except:
            try:
                test_font = font.Font(family="Harmony Sans SC")
                self.family = "Harmony Sans SC"
            except:
                self.family = "微软雅黑"
        
        # 创建开始按钮
        self.start_button = tk.Button(
            self.button_window, 
            text="点名", 
            command=self.show_selection_window,
            font=(self.family, 10),
            bg="#4CAF50",
            fg="white",
            relief="raised"
        )
        if hasattr(self, 'button_icon_photo'):
            self.start_button.config(image=self.button_icon_photo, compound=tk.LEFT)
        self.start_button.pack(fill=tk.BOTH, expand=True)
        
        # 添加拖拽功能
        self.drag_data = {"x": 0, "y": 0, "dragging": False}
        self.start_button.bind("<ButtonPress-1>", self.start_drag)
        self.start_button.bind("<B1-Motion>", self.on_drag)
        self.start_button.bind("<ButtonRelease-1>", self.stop_drag)
        
        # 添加右键菜单
        self.button_window.bind("<Button-3>", self.show_context_menu)
        
        # 读取名字列表
        self.names = self.load_names()
        
        # 提取所有字符用于动画
        self.all_chars = self.extract_all_chars()
        
        # 选择窗口状态
        self.selection_window_open = False
        
    def show_context_menu(self, event):
        """显示右键菜单"""
        menu = tk.Menu(self.button_window, tearoff=0)
        menu.add_command(label="赞助页面", command=self.show_sponsor_page)
        menu.add_separator()
        menu.add_command(label="退出", command=self.quit_app)
        menu.post(event.x_root, event.y_root)
        
    def show_sponsor_page(self):
        """显示赞助页面"""
        # 创建赞助窗口
        sponsor_window = tk.Toplevel(self.root)
        sponsor_window.title("浮幻点名系统 - 赞助页面")
        sponsor_window.geometry("700x700")  # 增加高度以适应新内容
        sponsor_window.resizable(False, False)
        sponsor_window.configure(bg="#f0f0f0")
        
        # 设置窗口图标
        try:
            if hasattr(self, 'button_icon_photo'):
                sponsor_window.iconphoto(False, self.button_icon_photo)
        except:
            pass
        
        # 创建主框架
        main_frame = tk.Frame(sponsor_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(
            main_frame,
            text="浮幻点名系统 | 赞助页面",
            font=(self.family, 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # 开发者信息框架
        dev_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, bd=1)
        dev_frame.pack(fill=tk.X, pady=10, ipadx=10, ipady=10)
        
        # 开发者头像
        try:
            avatar_path = os.path.join("picture", "touxiang.png")
            if os.path.exists(avatar_path):
                avatar_image = Image.open(avatar_path)
                avatar_image = avatar_image.resize((80, 80), Image.Resampling.LANCZOS)
                self.avatar_photo = ImageTk.PhotoImage(avatar_image)
                avatar_label = tk.Label(dev_frame, image=self.avatar_photo, bg="#ffffff")
                avatar_label.pack(side=tk.LEFT, padx=10, pady=10)
        except Exception as e:
            print(f"加载头像失败: {e}")
        
        # 开发者信息文本
        dev_info_frame = tk.Frame(dev_frame, bg="#ffffff")
        dev_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        dev_name_label = tk.Label(
            dev_info_frame,
            text="开发者: MirageBN",
            font=(self.family, 12, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
            anchor="w"
        )
        dev_name_label.pack(fill=tk.X)
        
        dev_desc_label = tk.Label(
            dev_info_frame,
            font=(self.family, 10),
            bg="#ffffff",
            fg="#7f8c8d",
            anchor="w"
        )
        dev_desc_label.pack(fill=tk.X)
        
        # 添加个人B站关注按钮
        personal_bilibili_button = tk.Button(
            dev_info_frame,
            text="关注我的B站",
            command=lambda: webbrowser.open("https://space.bilibili.com/3546558473702169"),
            font=(self.family, 9),
            bg="#FF69B4",
            fg="white",
            width=12
        )
        personal_bilibili_button.pack(pady=5, anchor="w")
        
        # 开发故事框架
        story_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, bd=1)
        story_frame.pack(fill=tk.X, pady=10, ipadx=10, ipady=10)
        
        story_text = """煮包是一名刚上高一的高中生。平时上课时，老师点名常常不够随机，有时候因为不熟悉全班同学，老师总会下意识地选择那几个眼熟的名字。而作为一班之长，我因为经常帮班里做事，也"顺理成章"成了老师点名的重点对象之一。为了不让点名变成"针对性活动"，我决定自己动手，写一个真正公平、随机的点名程序。之前我们老师也曾买过一个点名程序，听说花了好几百，但实际使用起来体验并不理想。我在网上找了很久，也没发现合适的免费开源方案。于是，我结合老师上课的实际需求，开发了这款量身定制、轻量不占地方、界面简洁不复杂的点名软件。它完全免费、开源，希望能帮助更多老师实现轻松、公正的课堂互动。"""
        
        story_label = tk.Label(
            story_frame,
            text=story_text,
            font=(self.family, 10),
            bg="#ffffff",
            fg="#2c3e50",
            justify=tk.LEFT,
            wraplength=650
        )
        story_label.pack(padx=10, pady=10, anchor="w")
        
        # 赞助信息框架
        sponsor_frame = tk.Frame(main_frame, bg="#e8f4fd", relief=tk.RAISED, bd=1)
        sponsor_frame.pack(fill=tk.X, pady=10, ipadx=10, ipady=10)
        
        sponsor_title = tk.Label(
            sponsor_frame,
            text="支持开发",
            font=(self.family, 14, "bold"),
            bg="#e8f4fd",
            fg="#2980b9"
        )
        sponsor_title.pack(pady=5)
        
        sponsor_text = """如果你觉得这个小程序有帮助，欢迎赞助支持我的开发。你的支持将是我熬夜写代码时最好的动力，比如一杯29块的瑞幸茉莉花香拿铁，就能让我开心一整天！9.9也是no problem，万一我有优惠券呢，一块钱买两包辣条也不错啦~"""
        
        sponsor_label = tk.Label(
            sponsor_frame,
            text=sponsor_text,
            font=(self.family, 10),
            bg="#e8f4fd",
            fg="#2c3e50",
            justify=tk.LEFT,
            wraplength=650
        )
        sponsor_label.pack(padx=10, pady=10, anchor="w")
        
        # 按钮框架
        button_frame = tk.Frame(sponsor_frame, bg="#e8f4fd")
        button_frame.pack(pady=10)
        
        # 添加赞助按钮
        sponsor_button = tk.Button(
            button_frame,
            text="赞助我们",
            command=self.show_payment_qr_codes,
            font=(self.family, 10, "bold"),
            bg="#27ae60",
            fg="white",
            width=15
        )
        sponsor_button.pack(side=tk.LEFT, padx=10)
        
        # 添加关注按钮
        follow_button = tk.Button(
            button_frame,
            text="关注我们",
            command=self.open_bilibili,
            font=(self.family, 10, "bold"),
            bg="#ff6b6b",
            fg="white",
            width=15
        )
        follow_button.pack(side=tk.LEFT, padx=10)
        
        # 感谢信息
        thanks_label = tk.Label(
            main_frame,
            text="感谢大家的支持！",
            font=(self.family, 12, "bold"),
            bg="#f0f0f0",
            fg="#27ae60"
        )
        thanks_label.pack(pady=10)
        
        # 关闭按钮
        close_button = tk.Button(
            main_frame,
            text="关闭",
            command=sponsor_window.destroy,
            font=(self.family, 10),
            bg="#95a5a6",
            fg="white",
            width=15
        )
        close_button.pack(pady=10)
        
    def open_bilibili(self):
        """打开B站关注页面"""
        webbrowser.open("https://space.bilibili.com/3546938154683232?spm_id_from=333.1387.follow.user_card.click")
        
    def show_payment_qr_codes(self):
        """显示支付二维码页面"""
        # 创建支付二维码窗口
        qr_window = tk.Toplevel(self.root)
        qr_window.title("浮幻点名系统 - 赞助方式")
        qr_window.geometry("600x550")  # 增加高度以适应关注按钮
        qr_window.resizable(False, False)
        qr_window.configure(bg="#f0f0f0")
        
        # 设置窗口图标
        try:
            if hasattr(self, 'button_icon_photo'):
                qr_window.iconphoto(False, self.button_icon_photo)
        except:
            pass
        
        # 创建主框架
        main_frame = tk.Frame(qr_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(
            main_frame,
            text="赞助方式",
            font=(self.family, 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # 说明文字
        desc_label = tk.Label(
            main_frame,
            text="扫描下方二维码进行赞助，感谢您的支持！",
            font=(self.family, 12),
            bg="#f0f0f0",
            fg="#7f8c8d"
        )
        desc_label.pack(pady=5)
        
        # 二维码框架
        qr_frame = tk.Frame(main_frame, bg="#f0f0f0")
        qr_frame.pack(pady=20)
        
        # 尝试加载微信支付二维码
        try:
            wechat_path = os.path.join("picture", "wechat.png")
            if os.path.exists(wechat_path):
                wechat_image = Image.open(wechat_path)
                # 调整图片大小
                wechat_image = wechat_image.resize((200, 200), Image.Resampling.LANCZOS)
                self.wechat_photo = ImageTk.PhotoImage(wechat_image)
                
                wechat_frame = tk.Frame(qr_frame, bg="#f0f0f0")
                wechat_frame.pack(side=tk.LEFT, padx=20)
                
                wechat_label = tk.Label(
                    wechat_frame,
                    text="微信支付",
                    font=(self.family, 12, "bold"),
                    bg="#f0f0f0",
                    fg="#2c3e50"
                )
                wechat_label.pack(pady=5)
                
                wechat_qr_label = tk.Label(
                    wechat_frame,
                    image=self.wechat_photo,
                    bg="#f0f0f0"
                )
                wechat_qr_label.pack(pady=5)
        except Exception as e:
            print(f"加载微信二维码失败: {e}")
            # 如果加载失败，显示占位符
            wechat_frame = tk.Frame(qr_frame, bg="#f0f0f0")
            wechat_frame.pack(side=tk.LEFT, padx=20)
            
            wechat_label = tk.Label(
                wechat_frame,
                text="微信支付\n(二维码加载失败)",
                font=(self.family, 12, "bold"),
                bg="#f0f0f0",
                fg="#2c3e50"
            )
            wechat_label.pack(pady=5)
            
            placeholder = tk.Label(
                wechat_frame,
                text="QR Code\n200x200",
                font=(self.family, 10),
                bg="#e0e0e0",
                fg="#7f8c8d",
                width=15,
                height=10
            )
            placeholder.pack(pady=5)
        
        # 尝试加载支付宝二维码
        try:
            alipay_path = os.path.join("picture", "Alipay.png")
            if os.path.exists(alipay_path):
                alipay_image = Image.open(alipay_path)
                # 调整图片大小
                alipay_image = alipay_image.resize((200, 200), Image.Resampling.LANCZOS)
                self.alipay_photo = ImageTk.PhotoImage(alipay_image)
                
                alipay_frame = tk.Frame(qr_frame, bg="#f0f0f0")
                alipay_frame.pack(side=tk.LEFT, padx=20)
                
                alipay_label = tk.Label(
                    alipay_frame,
                    text="支付宝",
                    font=(self.family, 12, "bold"),
                    bg="#f0f0f0",
                    fg="#2c3e50"
                )
                alipay_label.pack(pady=5)
                
                alipay_qr_label = tk.Label(
                    alipay_frame,
                    image=self.alipay_photo,
                    bg="#f0f0f0"
                )
                alipay_qr_label.pack(pady=5)
        except Exception as e:
            print(f"加载支付宝二维码失败: {e}")
            # 如果加载失败，显示占位符
            alipay_frame = tk.Frame(qr_frame, bg="#f0f0f0")
            alipay_frame.pack(side=tk.LEFT, padx=20)
            
            alipay_label = tk.Label(
                alipay_frame,
                text="支付宝\n(二维码加载失败)",
                font=(self.family, 12, "bold"),
                bg="#f0f0f0",
                fg="#2c3e50"
            )
            alipay_label.pack(pady=5)
            
            placeholder = tk.Label(
                alipay_frame,
                text="QR Code\n200x200",
                font=(self.family, 10),
                bg="#e0e0e0",
                fg="#7f8c8d",
                width=15,
                height=10
            )
            placeholder.pack(pady=5)
        
        # 关注按钮框架
        follow_frame = tk.Frame(main_frame, bg="#f0f0f0")
        follow_frame.pack(pady=10)
        
        # 个人B站关注按钮
        personal_bilibili_button = tk.Button(
            follow_frame,
            text="关注我的B站",
            command=lambda: webbrowser.open("https://space.bilibili.com/3546558473702169"),
            font=(self.family, 10, "bold"),
            bg="#FF69B4",
            fg="white",
            width=15
        )
        personal_bilibili_button.pack(side=tk.LEFT, padx=5)
        
        # 团队B站关注按钮
        team_bilibili_button = tk.Button(
            follow_frame,
            text="关注我们的B站",
            command=self.open_bilibili,
            font=(self.family, 10, "bold"),
            bg="#ff6b6b",
            fg="white",
            width=15
        )
        team_bilibili_button.pack(side=tk.LEFT, padx=5)
        
        # 感谢信息
        thanks_label = tk.Label(
            main_frame,
            text="感谢您的支持！每一份赞助都是对我继续开发的鼓励！",
            font=(self.family, 11),
            bg="#f0f0f0",
            fg="#27ae60"
        )
        thanks_label.pack(pady=15)
        
        # 关闭按钮
        close_button = tk.Button(
            main_frame,
            text="关闭",
            command=qr_window.destroy,
            font=(self.family, 10),
            bg="#95a5a6",
            fg="white",
            width=15
        )
        close_button.pack(pady=10)
        
    def quit_app(self):
        """退出应用程序"""
        self.root.quit()
        self.root.destroy()
        
    def start_drag(self, event):
        """开始拖拽"""
        self.drag_data["x"] = event.x_root
        self.drag_data["y"] = event.y_root
        self.drag_data["dragging"] = False
        
    def on_drag(self, event):
        """拖拽中"""
        # 标记为拖拽
        self.drag_data["dragging"] = True
        
        # 计算新位置
        x = self.button_window.winfo_x() + (event.x_root - self.drag_data["x"])
        y = self.button_window.winfo_y() + (event.y_root - self.drag_data["y"])
        
        # 更新窗口位置
        self.button_window.geometry(f"+{x}+{y}")
        
        # 更新拖拽起始位置
        self.drag_data["x"] = event.x_root
        self.drag_data["y"] = event.y_root
        
    def stop_drag(self, event):
        """停止拖拽"""
        # 如果不是拖拽，则执行点击操作
        if not self.drag_data["dragging"] and not self.selection_window_open:
            self.show_selection_window()
        self.drag_data["dragging"] = False
        
    def show_selection_window(self):
        """显示人数选择窗口"""
        # 防止重复打开选择窗口
        if self.selection_window_open:
            return
            
        self.selection_window_open = True
        
        # 创建选择窗口
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.title("浮幻点名系统 - 选择点名人数")
        self.selection_window.geometry("350x200")
        self.selection_window.attributes('-topmost', True)
        self.selection_window.resizable(False, False)
        
        # 设置窗口图标
        try:
            if hasattr(self, 'button_icon_photo'):
                self.selection_window.iconphoto(False, self.button_icon_photo)
        except:
            pass
        
        # 添加窗口关闭事件处理
        self.selection_window.protocol("WM_DELETE_WINDOW", self.on_selection_window_close)
        
        # 添加标签
        label = tk.Label(
            self.selection_window,
            text="请选择要点名的人数:",
            font=(self.family, 12)
        )
        label.pack(pady=15)
        
        # 添加下拉选择框
        self.num_people = tk.IntVar(value=1)
        max_people = min(10, len(self.names))
        people_combobox = ttk.Combobox(
            self.selection_window,
            textvariable=self.num_people,
            values=list(range(1, max_people + 1)),
            state="readonly",
            font=(self.family, 12),
            width=10
        )
        people_combobox.pack(pady=10)
        
        # 按钮框架
        button_frame = tk.Frame(self.selection_window)
        button_frame.pack(pady=10)
        
        # 添加确认按钮
        confirm_button = tk.Button(
            button_frame,
            text="开始点名",
            command=self.start_picking,
            font=(self.family, 10),
            bg="#4CAF50",
            fg="white",
            width=12
        )
        confirm_button.pack(side=tk.LEFT, padx=5)
        
        # 添加赞助页面按钮
        sponsor_button = tk.Button(
            button_frame,
            text="赞助页面",
            command=self.show_sponsor_page,
            font=(self.family, 10),
            bg="#3498db",
            fg="white",
            width=12
        )
        sponsor_button.pack(side=tk.LEFT, padx=5)
        
    def on_selection_window_close(self):
        """处理选择窗口关闭事件"""
        self.selection_window_open = False
        if hasattr(self, 'selection_window'):
            self.selection_window.destroy()
        
    def load_names(self):
        """从names.txt文件中加载名字列表"""
        names = []
        try:
            with open("names.txt", "r", encoding="utf-8") as f:
                for line in f:
                    name = line.strip()
                    if name:
                        names.append(name)
        except FileNotFoundError:
            # 如果文件不存在，创建示例文件
            with open("names.txt", "w", encoding="utf-8") as f:
                sample_names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"]
                for name in sample_names:
                    f.write(name + "\n")
            names = sample_names
        return names
    
    def extract_all_chars(self):
        """从所有名字中提取所有字符"""
        chars = set()
        for name in self.names:
            for char in name:
                chars.add(char)
        return list(chars)
    
    def start_picking(self):
        """开始点名"""
        if not self.names:
            return
            
        # 关闭选择窗口
        if hasattr(self, 'selection_window'):
            self.selection_window.destroy()
            self.selection_window_open = False
            
        # 隐藏按钮窗口
        self.button_window.withdraw()
        
        # 获取选择的人数
        num_to_pick = self.num_people.get()
        
        # 随机选择不重复的名字
        if num_to_pick > len(self.names):
            num_to_pick = len(self.names)
            
        self.selected_names = random.sample(self.names, num_to_pick)
        
        # 创建全屏窗口
        self.lottery_window = tk.Toplevel(self.root)
        self.lottery_window.attributes('-fullscreen', True)
        
        # 设置背景透明，但内容不透明
        self.lottery_window.configure(bg='black')
        self.lottery_window.attributes('-alpha', 0.3)  # 背景30%透明度
        
        # 绑定ESC键退出全屏
        self.lottery_window.bind("<Escape>", lambda e: self.close_lottery())
        
        # 根据选择的人数创建不同的动画
        if num_to_pick == 1:
            self.create_single_animation()
        else:
            self.create_multiple_animation()
    
    def create_single_animation(self):
        """创建单人点名动画 - 老虎机特效"""
        # 创建显示框架 - 设置不透明背景
        self.display_frame = tk.Frame(self.lottery_window, bg='black')
        self.display_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # 创建标签用于显示名字 - 设置不透明背景
        self.name_labels = []
        selected_name = self.selected_names[0]
        
        for i, char in enumerate(selected_name):
            label = tk.Label(
                self.display_frame,
                text=" ",
                font=(self.family, 120, "bold"),
                fg="white",
                bg="black",
                width=2
            )
            label.grid(row=0, column=i, padx=5)
            self.name_labels.append(label)
        
        # 开始动画
        self.animate_index = 0
        self.animate_slots()
    
    def animate_slots(self):
        """执行老虎机动画"""
        if self.animate_index >= len(self.name_labels):
            # 动画完成，3秒后关闭窗口
            self.lottery_window.after(3000, self.close_lottery)
            return
            
        current_label = self.name_labels[self.animate_index]
        
        # 滚动动画
        self.roll_character(current_label, 0)
    
    def roll_character(self, label, count):
        """滚动单个字符的动画"""
        if count < 15:
            # 从所有名字中随机选择一个字符
            random_char = random.choice(self.all_chars)
            label.config(text=random_char, fg="#FFD700")
            
            # 继续滚动
            self.lottery_window.after(30, lambda: self.roll_character(label, count + 1))
        else:
            # 滚动结束，显示正确的字符
            selected_name = self.selected_names[0]
            label.config(text=selected_name[self.animate_index], fg="white")
            
            # 移动到下一个字符
            self.animate_index += 1
            self.lottery_window.after(100, self.animate_slots)
    
    def create_multiple_animation(self):
        """创建多人点名动画 - 简化版卡牌效果"""
        # 创建显示框架 - 设置不透明背景
        self.display_frame = tk.Frame(self.lottery_window, bg='black')
        self.display_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # 创建卡牌容器 - 设置不透明背景
        self.card_frame = tk.Frame(self.display_frame, bg='black')
        self.card_frame.pack()
        
        # 创建卡牌标签 - 设置不透明背景
        self.card_labels = []
        num_cards = len(self.selected_names)
        
        # 直接创建卡牌背面
        for i, name in enumerate(self.selected_names):
            # 创建卡牌背面 - 设置不透明背景
            card = tk.Label(
                self.card_frame,
                text="?",
                font=(self.family, 24, "bold"),
                fg="white",
                bg="#2C3E50",  # 深蓝色背景
                width=4,
                height=8,
                relief="raised",
                bd=3
            )
            card.grid(row=0, column=i, padx=10)
            self.card_labels.append((card, name))
        
        # 开始卡牌翻转动画 - 减少延迟时间
        self.flip_index = 0
        self.lottery_window.after(500, self.flip_cards)  # 减少延迟时间到500ms
    
    def flip_cards(self):
        """执行卡牌翻转动画"""
        if self.flip_index >= len(self.card_labels):
            # 动画完成，3秒后关闭窗口
            self.lottery_window.after(3000, self.close_lottery)
            return
            
        card, name = self.card_labels[self.flip_index]
        
        # 翻转卡牌动画
        self.flip_animation(card, name, 0)
    
    def flip_animation(self, card, name, step):
        """执行单个卡牌翻转动画"""
        if step < 8:  # 减少翻转动画步骤到8步，加快速度
            if step < 4:
                # 缩小宽度效果
                card.config(width=4 - step, height=8)
            else:
                # 改变内容和颜色
                if step == 4:
                    # 创建竖向排列的名字
                    vertical_name = "\n".join(list(name))
                    card.config(
                        text=vertical_name,
                        bg="#E74C3C",  # 红色背景
                        font=(self.family, 16, "bold")
                    )
                # 增加宽度效果
                card.config(width=step - 3, height=8)
            
            # 继续动画 - 减少延迟时间到50ms
            self.lottery_window.after(50, lambda: self.flip_animation(card, name, step + 1))
        else:
            # 动画完成，显示最终状态
            vertical_name = "\n".join(list(name))
            card.config(
                text=vertical_name,
                font=(self.family, 16, "bold"),
                bg="#E74C3C",
                fg="white",
                width=4,
                height=8
            )
            
            # 移动到下一个卡牌 - 减少延迟时间到300ms
            self.flip_index += 1
            self.lottery_window.after(300, self.flip_cards)  # 减少延迟时间到300ms
    
    def close_lottery(self):
        """关闭点名窗口并恢复按钮窗口"""
        if hasattr(self, 'lottery_window'):
            self.lottery_window.destroy()
        self.button_window.deiconify()
    
    def run(self):
        """运行程序"""
        self.root.mainloop()

if __name__ == "__main__":
    # 隐藏控制台窗口（仅适用于Windows）
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
    
    app = LotteryNamePicker()
    app.run()