import tkinter as tk
from tkinter import messagebox, simpledialog
import time

from storage.storage_handler import StorageHandler
from models.user import User
from models.message import Message

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("پیام‌رسان سوپر کامل 💎")

        self.storage = StorageHandler()
        self.current_user = None

        self.create_widgets()
        self.load_messages()

    def create_widgets(self):
        self.username_label = tk.Label(self.root, text="نام کاربری:")
        self.username_label.grid(row=0, column=0)

        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1)

        self.login_button = tk.Button(self.root, text="ورود / ثبت نام", command=self.login)
        self.login_button.grid(row=0, column=2, padx=5, pady=5)

        self.message_label = tk.Label(self.root, text="پیام:")
        self.message_label.grid(row=1, column=0, pady=5)

        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.grid(row=1, column=1, columnspan=2, pady=5)

        self.send_button = tk.Button(self.root, text="ارسال پیام", command=self.send_message, state=tk.DISABLED)
        self.send_button.grid(row=1, column=3, padx=5)

        self.search_label = tk.Label(self.root, text="جستجو:")
        self.search_label.grid(row=2, column=0)

        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=2, column=1)

        self.search_button = tk.Button(self.root, text="بگرد", command=self.search_messages)
        self.search_button.grid(row=2, column=2)

        self.refresh_button = tk.Button(self.root, text="بارگذاری مجدد", command=self.load_messages)
        self.refresh_button.grid(row=2, column=3)

        self.messages_list = tk.Text(self.root, height=20, width=80)
        self.messages_list.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
        self.messages_list.config(state=tk.DISABLED)
        self.messages_list.bind("<Double-Button-1>", self.reply_to_message)

        self.status_label = tk.Label(self.root, text="آماده...")
        self.status_label.grid(row=4, column=0, columnspan=4, sticky="w", padx=5)

    def login(self):
        username = self.username_entry.get()
        if not username:
            messagebox.showwarning("خطا", "نام کاربری را وارد کنید.")
            return

        user_data = self.storage.get_user(username)
        if user_data:
            self.current_user = User(user_data["username"], user_data["display_name"])
            self.current_user.messages_sent = user_data["messages_sent"]
            messagebox.showinfo("ورود", f"خوش آمدی دوباره {self.current_user.display_name}!")
        else:
            self.current_user = User(username)
            self.storage.save_user(username, {
                "username": self.current_user.username,
                "display_name": self.current_user.display_name,
                "messages_sent": []
            })
            messagebox.showinfo("ثبت نام", f"کاربر {username} ساخته شد و وارد شدی!")

        self.send_button.config(state=tk.NORMAL)
        self.status_label.config(text=f"وارد شده با: {self.current_user.username}")
        self.load_messages()

    def send_message(self):
        if not self.current_user:
            messagebox.showwarning("خطا", "ابتدا وارد شوید.")
            return

        content = self.message_entry.get()
        if not content:
            messagebox.showwarning("خطا", "پیامی وارد کنید.")
            return

        new_id = self.storage.get_next_message_id()
        msg = Message(new_id, self.current_user.username, content)
        self.storage.save_message(msg)

        self.current_user.add_message(new_id)
        self.storage.save_user(self.current_user.username, {
            "username": self.current_user.username,
            "display_name": self.current_user.display_name,
            "messages_sent": self.current_user.messages_sent
        })

        self.message_entry.delete(0, tk.END)
        self.load_messages()

    def load_messages(self, highlight=None):
        messages = self.storage.get_all_messages()
        sorted_messages = [messages[k] for k in sorted(messages.keys())]

        self.messages_list.config(state=tk.NORMAL)
        self.messages_list.delete(1.0, tk.END)

        for msg in sorted_messages:
            self.insert_message_with_replies(msg, highlight=highlight)

        self.messages_list.tag_config("highlight", background="yellow")
        self.messages_list.tag_config("selfmsg", foreground="blue")
        self.messages_list.tag_config("reply", foreground="gray")
        self.messages_list.config(state=tk.DISABLED)

        num_users = len(self.storage.load_data()["users"])
        num_msgs = len(sorted_messages)
        self.status_label.config(text=f"تعداد کاربران: {num_users} | تعداد پیام‌ها: {num_msgs}")

    def insert_message_with_replies(self, msg, level=0, highlight=None):
        prefix = "    " * level
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg.timestamp))
        line = f"{prefix}[{time_str}] {msg.sender_username}: {msg.content}\n"

        tag = ""
        if highlight and highlight.lower() in msg.content.lower():
            tag = "highlight"
        elif self.current_user and msg.sender_username == self.current_user.username:
            tag = "selfmsg"
        elif level > 0:
            tag = "reply"

        self.messages_list.insert(tk.END, line, tag)

        for reply in msg.get_replies():
            self.insert_message_with_replies(reply, level + 1, highlight)

    def search_messages(self):
        keyword = self.search_entry.get()
        if not keyword:
            self.load_messages()
            return
        self.load_messages(highlight=keyword)

    def reply_to_message(self, event):
        index = self.messages_list.index("@%s,%s" % (event.x, event.y))
        line_content = self.messages_list.get(index + " linestart", index + " lineend")
        if "[" not in line_content:
            return

        timestamp = line_content.split("]")[0][1:]
        target_msg = self.find_message_by_timestamp(timestamp)
        if not target_msg:
            return

        reply_text = simpledialog.askstring("ریپلای", f"پاسخی برای پیام بنویس:")
        if reply_text:
            new_id = self.storage.get_next_message_id()
            reply_msg = Message(new_id, self.current_user.username, reply_text)
            target_msg.add_reply(reply_msg)
            self.storage.save_message(target_msg)
            self.current_user.add_message(new_id)
            self.storage.save_user(self.current_user.username, {
                "username": self.current_user.username,
                "display_name": self.current_user.display_name,
                "messages_sent": self.current_user.messages_sent
            })
            self.load_messages()

    def find_message_by_timestamp(self, ts):
        for msg in self.storage.get_all_messages().values():
            found = self._find_in_message(msg, ts)
            if found:
                return found
        return None

    def _find_in_message(self, msg, ts):
        if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg.timestamp)) == ts:
            return msg
        for reply in msg.get_replies():
            found = self._find_in_message(reply, ts)
            if found:
                return found
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
