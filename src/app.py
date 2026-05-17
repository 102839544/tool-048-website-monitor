#!/usr/bin/env python3
"""
网站监控工具 - 检测网站可用性
"""
import sys, tkinter as tk
from tkinter import messagebox, scrolledtext
import urllib.request
import urllib.error
import time
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        root.title("网站监控工具 v1.0")
        root.geometry("700x550")
        self.monitors = []
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#0288d1", height=50)
        f.pack(fill="x")
        tk.Label(f, text="🔍 网站监控工具", font=("Arial",14,"bold"),
                 fg="white", bg="#0288d1").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        # 添加监控
        af = tk.Frame(main)
        af.pack(fill="x", pady=5)
        tk.Label(af, text="网址：").pack(side="left")
        self.url_entry = tk.Entry(af, width=40)
        self.url_entry.pack(side="left", padx=5)
        self.url_entry.insert(0, "https://github.com")
        tk.Button(af, text="添加监控", command=self.add_monitor,
                  bg="#0288d1", fg="white", padx=10).pack(side="left", padx=5)
        tk.Button(af, text="立即检测", command=self.check_all,
                  bg="#4caf50", fg="white", padx=10).pack(side="left", padx=5)
        
        # 监控列表
        self.lb = tk.Listbox(main, font=("Consolas",10), bg="#e1f5fe", height=10)
        self.lb.pack(fill="both", expand=True, pady=10)
        
        # 日志
        tk.Label(main, text="检测日志：", font=("Arial",10,"bold")).pack(anchor="w")
        self.log_txt = scrolledtext.ScrolledText(main, font=("Consolas",9), height=10)
        self.log_txt.pack(fill="both", expand=True)
        
        self.status = tk.Label(main, text="添加网站进行监控",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def add_monitor(self):
        url = self.url_entry.get().strip()
        if not url:
            return
        if url not in self.monitors:
            self.monitors.append(url)
            self.lb.insert("end", f"⏳ {url}")
            self.status.config(text=f"已添加 {len(self.monitors)} 个监控")
    
    def check_all(self):
        if not self.monitors:
            messagebox.showwarning("提示", "请先添加监控网站")
            return
        
        self.log("开始检测...")
        
        for i, url in enumerate(self.monitors):
            try:
                start = time.time()
                req = urllib.request.Request(url, headers={
                    "User-Agent": "WebsiteMonitor/1.0"
                })
                with urllib.request.urlopen(req, timeout=10) as resp:
                    status = resp.status
                    elapsed = (time.time() - start) * 1000
                
                self.lb.delete(i)
                self.lb.insert(i, f"✅ {url} ({status}) {elapsed:.0f}ms")
                self.log(f"✅ {url} - 状态:{status} 耗时:{elapsed:.0f}ms")
                
            except urllib.error.HTTPError as e:
                self.lb.delete(i)
                self.lb.insert(i, f"❌ {url} ({e.code})")
                self.log(f"❌ {url} - HTTP {e.code}")
            except Exception as e:
                self.lb.delete(i)
                self.lb.insert(i, f"❌ {url} (失败)")
                self.log(f"❌ {url} - {str(e)}")
        
        self.status.config(text=f"检测完成 - {datetime.now().strftime('%H:%M:%S')}")
    
    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_txt.insert("end", f"[{timestamp}] {msg}\n")
        self.log_txt.see("end")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
