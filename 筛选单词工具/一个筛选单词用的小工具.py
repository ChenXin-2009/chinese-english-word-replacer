import json
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

def simple_vocabulary_manager(filename):
    # 读取数据
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df['keep'] = True  # 默认保留

    # 排序规则函数：如果中文释义中有单个汉字的翻译，则排前面
    def has_single_char(definition):
        # 多个释义逗号分隔
        parts = definition.split(',')
        return any(len(part.strip()) == 1 for part in parts)

    # 新增列用于排序
    df['single_char_flag'] = df['definition'].apply(lambda x: 0 if has_single_char(x) else 1)
    df['word_len'] = df['word'].apply(len)

    # 排序：单字释义的优先 -> 英文单词长度最短
    df = df.sort_values(by=['single_char_flag', 'word_len'])

    df['keep_flag'] = '✅'

    # 创建主窗口
    root = tk.Tk()
    root.title("Word 管理器")
    root.geometry("800x600")

    # 设置字体
    large_font_chinese = tkfont.Font(family="思源宋体", size=14)
    large_font_english = tkfont.Font(family="JetBrains Mono", size=14)
    style = ttk.Style(root)
    style.configure("Treeview", rowheight=30, font=large_font_english)
    style.configure("Treeview.Heading", font=large_font_english)

    # 创建Treeview
    tree = ttk.Treeview(root, columns=('word', 'definition', 'keep'), show='headings')
    tree.heading('word', text='Word')
    tree.heading('definition', text='中文释义')
    tree.heading('keep', text='是否保留')

    # 添加数据
    for i, row in df.iterrows():
        tree.insert('', 'end', values=(row['word'], row['definition'], row['keep_flag']))

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 保存函数
    def save_filtered():
        selected_items = []
        for item_id in tree.get_children():
            values = tree.item(item_id)['values']
            if values[2] == '✅':  # 如果保留
                selected_items.append({
                    'word': values[0],
                    'definition': values[1]
                })

        new_filename = filename.replace('.json', '_filtered.json')
        with open(new_filename, 'w', encoding='utf-8') as f:
            json.dump(selected_items, f, ensure_ascii=False, indent=2)

        messagebox.showinfo("完成", f"已保存 {len(selected_items)} 个单词到 {new_filename}")

    # 按钮
    btn = ttk.Button(root, text="生成新JSON", command=save_filtered)
    btn.pack(pady=10)

    # 点击切换 ✅/❌
    def toggle_keep(event):
        item = tree.identify_row(event.y)
        column = tree.identify_column(event.x)
        if item and column == '#3':
            current = tree.set(item, 'keep')
            tree.set(item, 'keep', '❌' if current == '✅' else '✅')

    tree.bind('<Button-1>', toggle_keep)

    # 列排序功能
    def treeview_sort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        if col == 'definition':
            l.sort(key=lambda t: (0 if has_single_char(t[0]) else 1, len(tv.set(t[1], 'word'))), reverse=reverse)
        elif col == 'word':
            l.sort(key=lambda t: len(t[0]), reverse=reverse)
        else:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

    tree.heading('word', command=lambda: treeview_sort_column(tree, 'word', False))
    tree.heading('definition', command=lambda: treeview_sort_column(tree, 'definition', False))
    tree.heading('keep', command=lambda: treeview_sort_column(tree, 'keep', False))

    root.mainloop()

simple_vocabulary_manager("第二版2025年10月1日191915.json")
