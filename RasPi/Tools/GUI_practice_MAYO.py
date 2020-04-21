# -*- coding: utf-8 -*-

import tkinter as tk
# python2の場合は、import Tkinter as tk
import tkinter.ttk as ttk
# python2の場合は、import ttk
import sqlite3

# 登録画面のGUI
def create_gui():
    # ----------------------------------------
    # コールバック関数群
    # ----------------------------------------
    # 表示ボタンが押下されたときのコールバック関数
    def select_button(var):
        root.destroy()
        if var==0:
            Base_Information_gui()
        elif var==1:
            API_Information_gui()
    # ----------------------------------------
    # 終了ボタンが押下されたときのコールバック関数
    def quit_button():
        root.destroy()
    # ----------------------------------------
    # 登録ボタンがクリックされた時にデータをDBに登録するコールバック関数
    def create_sql(item_name):
        print(item_name)
    # ----------------------------------------
    # 内訳テーブル(item)にあるitem_nameのタプルを作成する
    def createitemname():
        print('null')


    # rootフレームの設定
    root = tk.Tk()
    root.title("登録情報の修正画面")
    root.geometry("250x280")

    # メニューの設定
    frame = tk.Frame(root,bd=2,relief="ridge")
    frame.pack(fill="x")
    button0 = tk.Button(frame,text="ホーム")
    button0.pack(side="left")
    button1 = tk.Button(frame,text="入力(基本設定)")
    button1.pack(side="left")
    button2 = tk.Button(frame,text="表示(API設定)",command=select_button)
    button2.pack(side="left")
    button3 = tk.Button(frame,text="終了",command=quit_button)
    button3.pack(side="right")

    # 入力画面ラベルの設定
    label1 = tk.Label(root,text="【入力(基本設定)】",font=("",16),height=2)
    label1.pack(fill="x")

    #ラジオボタンの設定
    var = tk.IntVar()
    var.set(0)

    #基本設定
    frame1 = tk.Frame(root,pady=10)
    frame1.pack()
    rdo1 = tk.Radiobutton(frame1, value=0, variable=var, text='基本設定')
    rdo1.pack(side="left")

    #API設定
    frame3 = tk.Frame(root,pady=10)
    frame3.pack()
    rdo2 = tk.Radiobutton(frame3, value=1, variable=var, text='API設定')
    rdo2.pack(side="left")

    # 登録ボタンの設定
    button4 = tk.Button(root,text="登録(決定)",
                        font=("",16),
                        width=10,bg="gray",
                        command=lambda:select_button(var.get()))
    button4.pack()

    root.mainloop()

# 表示画面のGUI
def Base_Information_gui():
    # ----------------------------------------
    # コールバック関数群
    # ----------------------------------------
    # 登録ボタンが押下されたときのコールバック関数
    def create_button():
        root.destroy()
        create_gui()
    # ----------------------------------------
    # 終了ボタンが押下されたときのコールバック関数
    def quit_button():
        root.destroy()
    # ----------------------------------------
    # 表示ボタンが押下されたときのコールバック関数
    def select_sql(start,end):
        # treeviewのアイテムをすべて削除
        tree.delete(*tree.get_children())
        # 開始日と終了日が空欄だったらデフォルト値の設定
        if start == "":
            start = "1900-01-01"
        if end == "":
            end = "2100-01-01"
        #SELECT文の作成
        sql = """
        SELECT acc_date,item_name,amount
        FROM acc_data as a,item as i
        WHERE a.item_code = i.item_code AND
        acc_date BETWEEN '{}' AND '{}'
        ORDER BY acc_date
        """.format(start,end)
        # ツリービューにアイテムの追加
        i=0
        for r in c.execute(sql):
            # 金額(r[2])を通貨形式に変換
            r = (r[0],r[1],"¥{:,d}".format(r[2]))
            tree.insert("","end",tags=i,values=r)
            if i & 1:
                tree.tag_configure(i,background="#CCFFFF")
            i+=1
    # ----------------------------------------

    # 空のデータベースを作成して接続する
    dbname = "database.db"
    c = sqlite3.connect(dbname)
    c.execute("PRAGMA foreign_keys = 1")

    # rootフレームの設定
    root = tk.Tk()
    root.title("raspiCV_登録情報の修正")
    root.geometry("400x500")

    # メニューの設定
    frame = tk.Frame(root,bd=2,relief="ridge")
    frame.pack(fill="x")
    button1 = tk.Button(frame,text="入力(基本設定)",command=create_button)
    button1.pack(side="left")
    button2 = tk.Button(frame,text="表示(API設定)")
    button2.pack(side="left")
    button3 = tk.Button(frame,text="終了",command=quit_button)
    button3.pack(side="right")

    # 入力画面ラベルの設定
    label1 = tk.Label(root,text="【基本設定】",font=("",16),height=2)
    label1.pack(fill="x")

    '''
    # 期間選択のラベルエントリーの設定
    frame1 = tk.Frame(root,pady=15)
    frame1.pack()
    label2 = tk.Label(frame1,font=("",14),text="期間 ")
    label2.pack(side="left")
    entry1 = tk.Entry(frame1,font=("",14),justify="center",width=12)
    entry1.pack(side="left")
    label3 = tk.Label(frame1,font=("",14),text="　～　")
    label3.pack(side="left")
    entry2 = tk.Entry(frame1,font=("",14),justify="center",width=12)
    entry2.pack(side="left")
    '''

    # 表示ボタンの設定
    button4 = tk.Button(root,text="基本設定",
                        font=("",16),
                        width=10,bg="gray",
                        command=lambda:select_sql(entry1.get(),entry2.get()))
    button4.pack()

    # ツリービューの作成
    tree = ttk.Treeview(root,padding=10)
    tree["columns"] = (1,2,3)
    tree["show"] = "headings"
    tree.column(1,width=100)
    tree.column(2,width=75)
    tree.column(3,width=100)
    tree.heading(1,text="日付")
    tree.heading(2,text="内訳")
    tree.heading(3,text="金額")

    # ツリービューのスタイル変更
    style = ttk.Style()
    # TreeViewの全部に対して、フォントサイズの変更
    style.configure("Treeview",font=("",12))
    # TreeViewのHeading部分に対して、フォントサイズの変更と太字の設定
    style.configure("Treeview.Heading",font=("",14,"bold"))

    # SELECT文の作成
    sql = """
    SELECT acc_date,item_name,amount
    FROM acc_data as a,item as i
    WHERE a.item_code = i.item_code
    ORDER BY acc_date
    """
    # ツリービューにアイテムの追加
    i=0
    for r in c.execute(sql):
        # 金額(r[2])を通貨形式に変換
        r = (r[0],r[1],"¥{:,d}".format(r[2]))
        tree.insert("","end",tags=i,values=r)
        if i & 1:
            tree.tag_configure(i,background="#CCFFFF")
        i+=1
    # ツリービューの配置
    tree.pack(fill="x",padx=20,pady=20)

    # メインループ
    root.mainloop()

def API_Information_gui():
    # ----------------------------------------
    # コールバック関数群
    # ----------------------------------------
    # 登録ボタンが押下されたときのコールバック関数
    def create_button():
        root.destroy()
        create_gui()
    # ----------------------------------------
    # 終了ボタンが押下されたときのコールバック関数
    def quit_button():
        root.destroy()
    # ----------------------------------------
    # 表示ボタンが押下されたときのコールバック関数
    def select_sql(start,end):
        # treeviewのアイテムをすべて削除
        tree.delete(*tree.get_children())
        # 開始日と終了日が空欄だったらデフォルト値の設定
        if start == "":
            start = "1900-01-01"
        if end == "":
            end = "2100-01-01"
        #SELECT文の作成
        sql = """
        SELECT acc_date,item_name,amount
        FROM acc_data as a,item as i
        WHERE a.item_code = i.item_code AND
        acc_date BETWEEN '{}' AND '{}'
        ORDER BY acc_date
        """.format(start,end)
        # ツリービューにアイテムの追加
        i=0
        for r in c.execute(sql):
            # 金額(r[2])を通貨形式に変換
            r = (r[0],r[1],"¥{:,d}".format(r[2]))
            tree.insert("","end",tags=i,values=r)
            if i & 1:
                tree.tag_configure(i,background="#CCFFFF")
            i+=1
    # ----------------------------------------

    # 空のデータベースを作成して接続する
    dbname = "database.db"
    c = sqlite3.connect(dbname)
    c.execute("PRAGMA foreign_keys = 1")

    # rootフレームの設定
    root = tk.Tk()
    root.title("raspiCV_登録情報の修正")
    root.geometry("400x500")

    # メニューの設定
    frame = tk.Frame(root,bd=2,relief="ridge")
    frame.pack(fill="x")
    button1 = tk.Button(frame,text="入力(基本設定)",command=create_button)
    button1.pack(side="left")
    button2 = tk.Button(frame,text="表示(API設定)")
    button2.pack(side="left")
    button3 = tk.Button(frame,text="終了",command=quit_button)
    button3.pack(side="right")

    # 入力画面ラベルの設定
    label1 = tk.Label(root,text="【API設定】",font=("",16),height=2)
    label1.pack(fill="x")

    '''
    # 期間選択のラベルエントリーの設定
    frame1 = tk.Frame(root,pady=15)
    frame1.pack()
    label2 = tk.Label(frame1,font=("",14),text="期間 ")
    label2.pack(side="left")
    entry1 = tk.Entry(frame1,font=("",14),justify="center",width=12)
    entry1.pack(side="left")
    label3 = tk.Label(frame1,font=("",14),text="　～　")
    label3.pack(side="left")
    entry2 = tk.Entry(frame1,font=("",14),justify="center",width=12)
    entry2.pack(side="left")
    '''

    # 表示ボタンの設定
    button4 = tk.Button(root,text="表示(API設定)",
                        font=("",16),
                        width=10,bg="gray",
                        command=lambda:select_sql(entry1.get(),entry2.get()))
    button4.pack()

    # ツリービューの作成
    tree = ttk.Treeview(root,padding=10)
    tree["columns"] = (1,2,3)
    tree["show"] = "headings"
    tree.column(1,width=100)
    tree.column(2,width=75)
    tree.column(3,width=100)
    tree.heading(1,text="日付")
    tree.heading(2,text="内訳")
    tree.heading(3,text="金額")

    # ツリービューのスタイル変更
    style = ttk.Style()
    # TreeViewの全部に対して、フォントサイズの変更
    style.configure("Treeview",font=("",12))
    # TreeViewのHeading部分に対して、フォントサイズの変更と太字の設定
    style.configure("Treeview.Heading",font=("",14,"bold"))

    # SELECT文の作成
    sql = """
    SELECT acc_date,item_name,amount
    FROM acc_data as a,item as i
    WHERE a.item_code = i.item_code
    ORDER BY acc_date
    """
    # ツリービューにアイテムの追加
    i=0
    for r in c.execute(sql):
        # 金額(r[2])を通貨形式に変換
        r = (r[0],r[1],"¥{:,d}".format(r[2]))
        tree.insert("","end",tags=i,values=r)
        if i & 1:
            tree.tag_configure(i,background="#CCFFFF")
        i+=1
    # ツリービューの配置
    tree.pack(fill="x",padx=20,pady=20)

    # メインループ
    root.mainloop()

# GUI画面の表示
create_gui()
