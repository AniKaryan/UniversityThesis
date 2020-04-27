# Importing necessary libraries and packages
import os
import glob
import sys
import PyQt4
import time
import platform
import tkinter as tk
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import subprocess
from datetime import datetime
from sys import platform as _platform
from pandas import DataFrame
from tkinter import *
from tkinter import ttk
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import seaborn as seabornInstance
from sklearn import metrics
from statsmodels.formula.api import ols
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import shutil
import pathlib
from PIL import Image
from tkinter import Canvas, Frame, BOTH
from tkinter import filedialog
from tkinter.filedialog import askopenfile 
from statsmodels.sandbox.regression.predstd import wls_prediction_std

sns.set()

# Starting the GUI program
window = Tk() # create root window
window.title("Basic GUI Layout") # title of the GUI window
window.maxsize(1000, 800) # specify the max size the window can expand to
#window.config(bg="#9494b8") # specify background color
# matplotlib.use('qt4agg')

# Initilize global variebles
db, status, columns, column_names = '13_03_20.csv', False, [], []

show_association_rules = False
show_cluster_analysis = False
show_jointplot_analysis = False
show_correlation_analysis = False
show_regression_analysis = False
show_ols_analysis = False
show_functions = False

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def openFolder(name):
    if sys.platform == "win32" or sys.platform == "win64":
        os.startfile(name)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, name])

# Finding current plathform
def find_plathform():
    if _platform == "linux" or _platform == "linux2":
        # peint('Linux')
        return False
    elif _platform == "darwin":
        # print('Darwin')
        return False
    elif _platform == "win32":
        # print('Win32')
        return True
    elif _platform == "win64":
        # print('Win64')
        return True

button_arr = []

def showFunctions():
    global button_arr, show_association_rules, show_cluster_analysis, show_correlation_analysis, show_regression_analysis, show_ols_analysis
    print("showFunctions")

    if show_jointplot_analysis == True:

        jnt_frame=Frame(window, width=950, height=650, bg='#026084').grid(row=0,column=0, padx=5, pady=5)
        #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

        lbl=Label(jnt_frame, text="Correlation", width=20, bg='#cccccc',font=("Sans", 12),bd=3,cursor="arrow", padx=13, pady=10, relief=SUNKEN).place(x=10, y=10)

        jnt_inner_frame=Frame(jnt_frame, width=80, height=150, bg='#e6e6e6', bd=5, highlightbackground='#bfbfbf',highlightthickness=3,relief=GROOVE).grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
        #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

        jnt_input_frame=Frame(jnt_inner_frame, width=300, height=380, bg='#ccccff', bd=4, highlightbackground='#b3b3b3',highlightthickness=3, relief=GROOVE).place(x=65, y=85)

        jnt_image_frame=Frame(jnt_frame, width=490, height=500, bg='#ccccff', bd=5, relief=GROOVE).place(x=385, y=85)

        Label(jnt_image_frame, text="Jointplot Image Result", bg='#ccccff').place(x=565, y=95)


    elif show_association_rules == True:

        apr_frame=Frame(window, width=950, height=650, bg='#026084').grid(row=0,column=0, padx=5, pady=5)
        #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

        lbl_apr=Label(apr_frame, text="Apriori", width=20, bg='#cccccc',font=("Sans", 12),bd=3,cursor="arrow", padx=13, pady=10, relief=SUNKEN).place(x=10, y=10)

        apr_inner_frame=Frame(apr_frame, width=80, height=150, bg='#e6e6e6', bd=5, highlightbackground='#bfbfbf',highlightthickness=3,relief=GROOVE).grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
        #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

        apr_input_frame=Frame(apr_inner_frame, width=300, height=500, bg='#ccccff', bd=4, highlightbackground='#b3b3b3',highlightthickness=3, relief=GROOVE).place(x=65, y=85)

        apr_image_frame=Frame(apr_frame, width=490, height=500, bg='#ccccff', bd=5, relief=GROOVE).place(x=385, y=85)

        Label(apr_image_frame, text="Apriori Image Results", bg='#ccccff').place(x=565, y=95)

        apr_txt_frame=Frame(apr_image_frame, width=250, height=195, bg='#ccccff', bd=5, highlightbackground='#ababba',highlightthickness=4,relief=GROOVE).place(x=627,y=388)

        lbl_apr_txt=Label(apr_txt_frame, text="Browsing text file", width=17, bg='#cccccc',font=("Sans", 12),bd=3,cursor="arrow", padx=13, pady=10, relief=SUNKEN).place(x=630, y=392)

    elif show_cluster_analysis == True:

        clust_frame=Frame(window, width=950, height=650, bg='#026084').grid(row=0,column=0, padx=5, pady=5)
        #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

        lbl_clust=Label(clust_frame, text="Clustering", width=20, bg='#cccccc',font=("Sans", 12),bd=3,cursor="arrow", padx=13, pady=10, relief=SUNKEN).place(x=10, y=10)

        clust_inner_frame=Frame(clust_frame, width=80, height=150, bg='#e6e6e6', bd=5, highlightbackground='#bfbfbf',highlightthickness=3,relief=GROOVE).grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
        #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

        clust_input_frame=Frame(clust_inner_frame, width=300, height=380, bg='#ccccff', bd=4, highlightbackground='#b3b3b3',highlightthickness=3, relief=GROOVE).place(x=65, y=85)

        clust_image_frame=Frame(clust_frame, width=490, height=500, bg='#ccccff', bd=5, relief=GROOVE).place(x=385, y=85)

        Label(clust_image_frame, text="Clustering Image Results", bg='#ccccff').place(x=565, y=95)   

    elif show_correlation_analysis==True:

        corr_frame=Frame(window, width=950, height=650, bg='#026084').grid(row=0,column=0, padx=5, pady=5)
        #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

        corr_apr=Label(corr_frame, text="Correlation", width=20, bg='#cccccc',font=("Sans", 12),bd=3,cursor="arrow", padx=13, pady=10, relief=SUNKEN).place(x=10, y=10)

        corr_inner_frame=Frame(corr_frame, width=80, height=150, bg='#e6e6e6', bd=5, highlightbackground='#bfbfbf',highlightthickness=3,relief=GROOVE).grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
        #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

        corr_input_frame=Frame(corr_inner_frame, width=300, height=500, bg='#ccccff', bd=4, highlightbackground='#b3b3b3',highlightthickness=3, relief=GROOVE).place(x=65, y=85)

        corr_image_frame=Frame(corr_frame, width=490, height=500, bg='#ccccff', bd=5, relief=GROOVE).place(x=385, y=85)

        Label(corr_image_frame, text="Correlation Image Result", bg='#ccccff').place(x=565, y=95)

    elif show_regression_analysis == True:

        reg_frame=Frame(window, width=950, height=650, bg='#026084').grid(row=0,column=0, padx=5, pady=5)
        #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

        reg_clust=Label(reg_frame, text="Regression", width=20, bg='#cccccc',font=("Sans", 12),bd=3,cursor="arrow", padx=13, pady=10, relief=SUNKEN).place(x=10, y=10)

        reg_inner_frame=Frame(reg_frame, width=80, height=150, bg='#e6e6e6', bd=5, highlightbackground='#bfbfbf',highlightthickness=3,relief=GROOVE).grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
        #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

        reg_input_frame=Frame(reg_inner_frame, width=300, height=380, bg='#ccccff', bd=4, highlightbackground='#b3b3b3',highlightthickness=3, relief=GROOVE).place(x=65, y=85)

        reg_image_frame=Frame(reg_frame, width=490, height=500, bg='#ccccff', bd=5, relief=GROOVE).place(x=385, y=85)

        Label(reg_image_frame, text="Regression Image Results", bg='#ccccff').place(x=565, y=95)         

        reg_txt_frame=Frame(reg_image_frame, width=250, height=195, bg='#ccccff', bd=5, highlightbackground='#ababba',highlightthickness=4,relief=GROOVE).place(x=627,y=388)

        lbl_reg_txt=Label(reg_txt_frame, text="Browsing text file", width=17, bg='#cccccc',font=("Sans", 12),bd=3,cursor="arrow", padx=13, pady=10, relief=SUNKEN).place(x=630, y=392)  

    elif show_ols_analysis == True:

        ols_frame=Frame(window, width=950, height=650, bg='#026084').grid(row=0,column=0, padx=5, pady=5)
        #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

        ols_clust=Label(ols_frame, text="Regression", width=20, bg='#cccccc',font=("Sans", 12),bd=3,cursor="arrow", padx=13, pady=10, relief=SUNKEN).place(x=10, y=10)

        ols_inner_frame=Frame(ols_frame, width=80, height=150, bg='#e6e6e6', bd=5, highlightbackground='#bfbfbf',highlightthickness=3,relief=GROOVE).grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
        #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

        ols_input_frame=Frame(ols_inner_frame, width=300, height=380, bg='#ccccff', bd=4, highlightbackground='#b3b3b3',highlightthickness=3, relief=GROOVE).place(x=65, y=85)

        ols_image_frame=Frame(ols_frame, width=490, height=500, bg='#ccccff', bd=5, relief=GROOVE).place(x=385, y=85)

        Label(ols_image_frame, text="OLS Image Results", bg='#ccccff').place(x=565, y=95)         

        ols_txt_frame=Frame(ols_image_frame, width=250, height=195, bg='#ccccff', bd=5, highlightbackground='#ababba',highlightthickness=4,relief=GROOVE).place(x=627,y=388)

        lbl_ols_txt=Label(ols_txt_frame, text="Browsing text file", width=17, bg='#cccccc',font=("Sans", 12),bd=3,cursor="arrow", padx=13, pady=10, relief=SUNKEN).place(x=630, y=392)    


    def apriori_func(e1):
        print("Apriori func")
        print(e1.get())

        if (e1.get() == "2" or e1.get() == " 2"):
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    def apr_gen():
                        print("Apr Generation")
                        apriori_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ',
                                                   'Ծննդավայր (երկիր)',
                                                   'Ծննդավայր (քաղաք/գյուղ)', 'Ընդունման տարեթիվ', 'Առարկա',
                                                   'Առաջին միջանկյալ ստուգում', 'Երկրորդ միջանկյալ ստուգում',
                                                   'Ամփոփիչ քննություն']

                        # Intilizing global vaiables
                        transactions = []

                        # DB file name for Apriori algorithm
                        folder_name = ['apriori']
                        txt_file_name = ['apriori.txt']

                        # Getting dynamically path for appropriate DB file and backup directory
                        absolute_path = sys.path[0]
                        file_path = sys.path[0] + '/' + db

#                        dir_name = absolute_path + '/' + folder_name[0]
#                        abs_path = dir_name + '/' + txt_file_name[0]

                        f_path = pathlib.Path(__file__).parent.absolute()
                        f_path = str(f_path)
                        dir_name = f_path + '/' + 'images' + '/' + folder_name[0]
                        abs_path = f_path + '/' + txt_file_name[0]

                        # Setting pandas library options
                        pd.set_option('display.max_columns', None)
                        pd.set_option('display.max_rows', None)

                        if not find_plathform():
                            file_path = file_path.replace("\\", "/")
                        data = pd.read_csv(file_path)

                        if (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ուսանողի անուն') or (
                                column_names[1] == 'Ֆակուլտետ' and column_names[0] == 'Ուսանողի անուն'):
                            # points = 1000
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ուսանողի սեռ') or (
                                column_names[1] == 'Ուսանողի անուն' and column_names[0] == 'Ուսանողի սեռ'):
                            # points = 900
                            start = 1
                            end = 3
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ծննդավայր (երկիր)') or (
                                column_names[1] == 'Ուսանողի սեռ' and column_names[0] == 'Ծննդավայր (երկիր)'):
                            # points = 800
                            start = 2
                            end = 4
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                            1] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                column_names[1] == 'Ծննդավայր (երկիր)' and column_names[
                            0] == 'Ծննդավայր (քաղաք/գյուղ)'):
                            # points = 850
                            start = 3
                            end = 5
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                            1] == 'Ընդունման տարեթիվ') or (
                                column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                            0] == 'Ընդունման տարեթիվ'):
                            # points = 800
                            start = 4
                            end = 6
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա') or (
                                column_names[1] == 'Ընդունման տարեթիվ' and column_names[0] == 'Առարկա'):
                            # points = 800
                            start = 5
                            end = 7
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Առարկա' and column_names[1] == 'Առաջին միջանկյալ ստուգում') or (
                                column_names[1] == 'Առարկա' and column_names[0] == 'Առաջին միջանկյալ ստուգում'):
                            # points = 800
                            start = 6
                            end = 8
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում') or (
                                column_names[1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում'):
                            # points = 800
                            start = 7
                            end = 9
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[1] == 'Ամփոփիչ քննություն') or (
                                column_names[1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[0] == 'Ամփոփիչ քննություն'):
                            # points = 800
                            start = 8
                            end = 10
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ուսանողի սեռ') or (
                                column_names[1] == 'Ֆակուլտետ' and column_names[0] == 'Ուսանողի սեռ'):
                            # data = pd.read_csv("CVS/Fac->/Fac_Sx.csv")
                            data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Ուսանողի սեռ'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ծննդավայր (երկիր)') or (
                                column_names[1] == 'Ֆակուլտետ' and column_names[0] == 'Ծննդավայր (երկիր)'):
                            # data = pd.read_csv("CVS/Fac->/Fac_COB.csv")
                            data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Ծննդավայր (երկիր)'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                column_names[1] == 'Ֆակուլտետ' and column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)'):
                            # data = pd.read_csv("CVS/Fac->/Fac_C_V.csv")
                            data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Ծննդավայր (քաղաք/գյուղ)'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ընդունման տարեթիվ') or (
                                column_names[1] == 'Faculty' and column_names[0] == 'Ընդունման տարեթիվ'):
                            # data = pd.read_csv("CVS/Fac->/Fac_YOE.csv")
                            data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Ընդունման տարեթիվ'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Առարկա') or (
                                column_names[1] == 'Ֆակուլտետ' and column_names[0] == 'Առարկա'):
                            # data = pd.read_csv("CVS/Fac->/Fac_Sbj.csv")
                            data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Առարկա'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ֆակուլտետ' and column_names[
                            1] == 'Առաջին միջանկյալ ստուգում') or (
                                column_names[1] == 'Ֆակուլտետ' and column_names[0] == 'Առաջին միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/Fac->/Fac_Frst_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Առաջին միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ֆակուլտետ' and column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում') or (
                                column_names[1] == 'Ֆակուլտետ' and column_names[0] == 'Երկրորդ միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/Fac->/Fac_Scnd_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Երկրորդ միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ամփոփիչ քննություն') or (
                                column_names[1] == 'Ֆակուլտետ' and column_names[0] == 'Ամփոփիչ քննություն'):
                            # data = pd.read_csv("CVS/Fac->/Fac_Fnl_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Ամփոփիչ քննություն'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ծննդավայր (երկիր)') or (
                                column_names[1] == 'Ուսանողի անուն' and column_names[0] == 'Ծննդավայր (երկիր)'):
                            # data = pd.read_csv("CVS/Nam->/Name_COB.csv")
                            data = pd.read_csv(file_path, usecols=['Ուսանողի անուն', 'Ծննդավայր (երկիր)'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի անուն' and column_names[
                            1] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                column_names[1] == 'Ուսանողի անուն' and column_names[
                            0] == 'Ծննդավայր (քաղաք/գյուղ)'):
                            # data = pd.read_csv("CVS/Nam->/Name_C_V.csv")
                            data = pd.read_csv(file_path, usecols=['Ուսանողի անուն', 'Ծննդավայր (քաղաք/գյուղ)'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ընդունման տարեթիվ') or (
                                column_names[1] == 'Ուսանողի անուն' and column_names[0] == 'Ընդունման տարեթիվ'):
                            # data = pd.read_csv("CVS/Nam->/Name_YOE.csv")
                            data = pd.read_csv(file_path, usecols=['Ուսանողի անուն', 'Ընդունման տարեթիվ'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Առարկա' and column_names[1] == 'Ուսանողի անուն') or (
                                column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Առարկա'):
                            # data = pd.read_csv("CVS/Nam->/NS.csv")
                            data = pd.read_csv(file_path, usecols=['Առարկա', 'Ուսանողի անուն'])
                            start = 0
                            end = 2
                            for i in range(0, 906):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի անուն' and column_names[
                            1] == 'Առաջին միջանկյալ ստուգում') or (
                                column_names[1] == 'Ուսանողի անուն' and column_names[
                            0] == 'Առաջին միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/Nam->/Name_Frst_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Առաջին միջանկյալ ստուգում', 'Ուսանողի անուն'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի անուն' and column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում') or (
                                column_names[1] == 'Ուսանողի անուն' and column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/Nam->/Name_Scnd_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Ուսանողի անուն', 'Երկրորդ միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ամփոփիչ քննություն') or (
                                column_names[1] == 'Ուսանողի անուն' and column_names[0] == 'Ամփոփիչ քննություն'):
                            # data = pd.read_csv("CVS/Nam->/Name_Fnl_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Ուսանողի անուն', 'Ամփոփիչ քննություն'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի սեռ' and column_names[
                            1] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                column_names[1] == 'Ուսանողի սեռ' and column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)'):
                            # data = pd.read_csv("CVS/Sx->/Sx_C_V.csv")
                            data = pd.read_csv(file_path, usecols=['Ուսանողի սեռ', 'Ծննդավայր (քաղաք/գյուղ)'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ընդունման տարեթիվ') or (
                                column_names[1] == 'Ուսանողի սեռ' and column_names[0] == 'Ընդունման տարեթիվ'):
                            # data = pd.read_csv("CVS/Sx->/Sx_YOE.csv")
                            data = pd.read_csv(file_path, usecols=['Ուսանողի սեռ', 'Ընդունման տարեթիվ'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Առարկա') or (
                                column_names[1] == 'Ուսանողի սեռ' and column_names[0] == 'Առարկա'):
                            # data = pd.read_csv("CVS/Sx->/Sx_Sbj.csv")
                            data = pd.read_csv(file_path, usecols=['Ուսանողի սեռ', 'Առարկա'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի սեռ' and column_names[
                            1] == 'Առաջին միջանկյալ ստուգում') or (
                                column_names[1] == 'Ուսանողի սեռ' and column_names[
                            0] == 'Առաջին միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/Sx->/Sx_Frst_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Ուսանողի սեռ', 'Առաջին միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի սեռ' and column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում') or (
                                column_names[1] == 'Ուսանողի սեռ' and column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/Sx->/Sx_Scnd_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Ուսանողի սեռ', 'Երկրորդ միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ամփոփիչ քննություն') or (
                                column_names[1] == 'Ուսանողի սեռ' and column_names[0] == 'Ամփոփիչ քննություն'):
                            # data = pd.read_csv("CVS/Sx->/Sx_Fnl_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Ուսանողի սեռ', 'Ամփոփիչ քննություն'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                            1] == 'Ընդունման տարեթիվ') or (
                                column_names[1] == 'Ծննդավայր (երկիր)' and column_names[0] == 'Ընդունման տարեթիվ'):
                            # data = pd.read_csv("CVS/COB->/COB_YOE.csv")
                            data = pd.read_csv(file_path, usecols=['Ծննդավայր (երկիր)', 'Ընդունման տարեթիվ'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Առարկա') or (
                                column_names[1] == 'Ծննդավայր (երկիր)' and column_names[0] == 'Առարկա'):
                            # data = pd.read_csv("CVS/COB->/COB_Sbj.csv")
                            data = pd.read_csv(file_path, usecols=['Ծննդավայր (երկիր)', 'Առարկա'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                            1] == 'Առաջին միջանկյալ ստուգում') or (
                                column_names[1] == 'Ծննդավայր (երկիր)' and column_names[
                            0] == 'Առաջին միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/COB->/COB_Frst_Exm.csv")
                            data = pd.read_csv(file_path,
                                               usecols=['Ծննդավայր (երկիր)', 'Առաջին միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում') or (
                                column_names[1] == 'Ծննդավայր (երկիր)' and column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/COB->/COB_Scnd_Exm.csv")
                            data = pd.read_csv(file_path,
                                               usecols=['Ծննդավայր (երկիր)', 'Երկրորդ միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                            1] == 'Ամփոփիչ քննություն') or (
                                column_names[1] == 'Ծննդավայր (երկիր)' and column_names[0] == 'Ամփոփիչ քննություն'):
                            # data = pd.read_csv("CVS/COB->/COB_Fnl_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Ծննդավայր (երկիր)', 'Ամփոփիչ քննություն'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[1] == 'Առարկա') or (
                                column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[0] == 'Առարկա'):
                            # data = pd.read_csv("CVS/CV->/CV_Sbj.csv")
                            data = pd.read_csv(file_path, usecols=['Ծննդավայր (քաղաք/գյուղ)', 'Առարկա'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                            1] == 'Առաջին միջանկյալ ստուգում') or (
                                column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                            0] == 'Առաջին միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/CV->/CV_Frst_Exm.csv")
                            data = pd.read_csv(file_path,
                                               usecols=['Ծննդավայր (քաղաք/գյուղ)', 'Առաջին միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում') or (
                                column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/CV->/CV_Scnd_Exm.csv")
                            data = pd.read_csv(file_path,
                                               usecols=['Ծննդավայր (քաղաք/գյուղ)', 'Երկրորդ միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                            1] == 'Ամփոփիչ քննություն') or (
                                column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                            0] == 'Ամփոփիչ քննություն'):
                            # data = pd.read_csv("CVS/CV->/CV_Fnl_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Ծննդավայր (քաղաք/գյուղ)', 'Ամփոփիչ քննություն'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                            1] == 'Առաջին միջանկյալ ստուգում') or (
                                column_names[1] == 'Ընդունման տարեթիվ' and column_names[
                            0] == 'Առաջին միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/YOE->/YOE_Frst_Exm.csv")
                            data = pd.read_csv(file_path,
                                               usecols=['Ընդունման տարեթիվ', 'Առաջին միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում') or (
                                column_names[1] == 'Ընդունման տարեթիվ' and column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/YOE->/YOE_Scnd_Exm.csv")
                            data = pd.read_csv(file_path,
                                               usecols=['Ընդունման տարեթիվ', 'Երկրորդ միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                            1] == 'Ամփոփիչ քննություն') or (
                                column_names[1] == 'Ընդունման տարեթիվ' and column_names[0] == 'Ամփոփիչ քննություն'):
                            # data = pd.read_csv("CVS/YOE->/YOE_Fnl_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Ընդունման տարեթիվ', 'Ամփոփիչ քննություն'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Առարկա' and column_names[1] == 'Երկրորդ միջանկյալ ստուգում') or (
                                column_names[1] == 'Առարկա' and column_names[0] == 'Երկրորդ միջանկյալ ստուգում'):
                            # data = pd.read_csv("CVS/Sbj->/Sbj_Scnd_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Առարկա', 'Երկրորդ միջանկյալ ստուգում'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Առարկա' and column_names[1] == 'Ամփոփիչ քննություն') or (
                                column_names[1] == 'Առարկա' and column_names[0] == 'Ամփոփիչ քննություն'):
                            # data = pd.read_csv("CVS/Sbj->/Sbj_Fnl_Exm.csv")
                            data = pd.read_csv(file_path, usecols=['Առարկա', 'Ամփոփիչ քննություն'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])
                        elif (column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                            1] == 'Ամփոփիչ քննություն') or (
                                column_names[1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                            0] == 'Ամփոփիչ քննություն'):
                            # data = pd.read_csv("CVS/FE->/Frst_Exm_Fnl_Exm.csv")
                            data = pd.read_csv(file_path,
                                               usecols=['Առաջին միջանկյալ ստուգում', 'Ամփոփիչ քննություն'])
                            start = 0
                            end = 2
                            for i in range(0, 1000):
                                transactions.append([str(data.values[i, j]) for j in range(start, end)])

                        def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png','txt')):
                            """
                            Get the latest image file in the given directory
                            """

                            # get filepaths of all files and dirs in the given dir
                            valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                            # filter out directories, no-extension, and wrong extension files
                            valid_files = [f for f in valid_files if '.' in f and \
                                f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                            if not valid_files:
                                raise ValueError("No valid images in %s" % dirpath)

                            return max(valid_files, key=os.path.getmtime)                                 

                        print("------------------------")
                        oht = TransactionEncoder()
                        oht_ary = oht.fit(transactions).transform(transactions)
                        # oht.columns_  # Need to understand is this need or not!!!!
                        df_train = pd.DataFrame(oht_ary, columns=oht.columns_)
                        rules = apriori(df_train, min_support=0.01, use_colnames=True)
                        training_rules = association_rules(rules, metric="confidence", min_threshold=0.01)

                        # Visualization of "Support" VS "Confidence" parameters on graph
                        plt.figure(1)
                        plt.scatter(training_rules['support'], training_rules['confidence'], alpha=0.5)
                        plt.xlabel('Support')
                        plt.ylabel('Confidence')
                        plt.title('Support vs Confidence')
                        mngr = plt.get_current_fig_manager()
                        mngr.window.setGeometry(20, 350, 600, 550)
                        plt.savefig(
                            'images/apriori/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                           "") + '.png')

                        #apr_2_1_path=get_latest_image("images/apriori/",'png')
                        #print(apr_2_1_path)

                        apr_2_1_path=get_latest_image("images/apriori/",'png')          
                        image_apr_2_1 = PhotoImage(file=apr_2_1_path)
                        original_image_apr_2_1 = image_apr_2_1.subsample(3,3) # resize image using subsample

                        apr_2_1_im_label = Label(apr_image_frame,image=original_image_apr_2_1)
                        apr_2_1_im_label.image = original_image_apr_2_1 # keep a reference
                        apr_2_1_im_label.place(x=387, y=118)


                        # Visualization of "Support" VS "Lift" parameters on graph
                        plt.figure(2)
                        plt.scatter(training_rules['support'], training_rules['lift'], alpha=0.5)
                        plt.xlabel('Support')
                        plt.ylabel('Lift')
                        plt.title('Support vs Lift')
                        mngr = plt.get_current_fig_manager()
                        mngr.window.setGeometry(657, 350, 600, 550)
                        plt.savefig(
                            'images/apriori/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                           "") + '.png')

                        apr_2_2_path=get_latest_image("images/apriori/",'png')        
                        image_apr_2_2 = PhotoImage(file=apr_2_2_path)
                        original_image_apr_2_2 = image_apr_2_2.subsample(3,3) # resize image using subsample

                        apr_2_2_im_label = Label(apr_image_frame,image=original_image_apr_2_2)
                        apr_2_2_im_label.image = original_image_apr_2_2 # keep a reference
                        apr_2_2_im_label.place(x=627, y=118)

                        # Visualization of "Support" VS "Confidence" & "Lift" parameters on graph
                        plt.figure(3)
                        fit = np.polyfit(training_rules['lift'], training_rules['confidence'], 1)
                        fit_fn = np.poly1d(fit)
                        plt.plot(training_rules['lift'], training_rules['confidence'], 'yo', training_rules['lift'],
                                 fit_fn(training_rules['lift']))
                        plt.xlabel('lift')
                        plt.ylabel('confidence')
                        plt.title('lift vs confidence')
                        mngr = plt.get_current_fig_manager()
                        mngr.window.setGeometry(1298, 350, 600, 550)
                        plt.savefig(
                            'images/apriori/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                           "") + '.png')

                        apr_2_3_path=get_latest_image("images/apriori/",'png')          
                        image_apr_2_3 = PhotoImage(file=apr_2_3_path)
                        original_image_apr_2_3 = image_apr_2_3.subsample(3,3) # resize image using subsample

                        apr_2_3_im_label = Label(apr_image_frame,image=original_image_apr_2_3)
                        apr_2_3_im_label.image = original_image_apr_2_3 # keep a reference
                        apr_2_3_im_label.place(x=387, y=308)       

                        def mouse_on_apr_2_1(event):
                            image_apr_2_1 = PhotoImage(file=apr_2_1_path)
                            original_image_apr_2_1 = image_apr_2_1.subsample(2,2) # resize image using subsample

                            apr_2_1_im_label = Label(apr_image_frame,image=original_image_apr_2_1)
                            apr_2_1_im_label.image = original_image_apr_2_1 # keep a reference
                            apr_2_1_im_label.place(x=387, y=118) 

                            return          

                        def mouse_on_apr_2_2(event):
                            image_apr_2_2 = PhotoImage(file=apr_2_2_path)
                            original_image_apr_2_2 = image_apr_2_2.subsample(2,2) # resize image using subsample

                            apr_2_2_im_label = Label(apr_image_frame,image=original_image_apr_2_2)
                            apr_2_2_im_label.image = original_image_apr_2_2 # keep a reference
                            apr_2_2_im_label.place(x=627, y=118) 

                            return        

                        def mouse_on_apr_2_3(event):
                            image_apr_2_3 = PhotoImage(file=apr_2_3_path)
                            original_image_apr_2_3 = image_apr_2_3.subsample(2,2) # resize image using subsample

                            apr_2_3_im_label = Label(apr_image_frame,image=original_image_apr_2_3)
                            apr_2_3_im_label.image = original_image_apr_2_3 # keep a reference
                            apr_2_3_im_label.place(x=387, y=308) 

                            return                                                                

                        apr_2_1_im_label.bind('<Enter>',mouse_on_apr_2_1)                    
                        apr_2_2_im_label.bind('<Enter>',mouse_on_apr_2_2)  
                        apr_2_3_im_label.bind('<Enter>',mouse_on_apr_2_3)                         

                        # Taking backup values from above graphs and puting puting appropriate directory
                        try:
                            # Create target Directory
                            os.mkdir(dir_name)
                            print("Directory ", dir_name, " created.")
                        except FileExistsError:
                            print("Directory ", dir_name, " already exists.")
                        file = open(abs_path, 'w', encoding="utf8")
                        file.write(str(training_rules))
                        file.close()

                        now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                        now = str(now)
                        newname = 'apriori_' + now + '.txt'
                        os.rename('apriori.txt', newname)
                        shutil.move(newname,  "images/apriori/")

                        apr_2_txt_path=get_latest_image("images/apriori/",'txt')
                        print(apr_2_txt_path)  

                        def apr_2_btn_click():
                            window.filename =  filedialog.askopenfile(mode='r',initialdir = "images/apriori/",title = apr_2_txt_path,filetypes = (("txt files","*.txt"),("all files","*.*")))

                        apr_txt_entry=Entry(apr_txt_frame, highlightcolor='#ababba',justify=LEFT, relief=SUNKEN, width=18)
                        apr_txt_entry.insert(END,apr_2_txt_path)
                        apr_txt_entry.place(x=637, y=490)

                        apr_txt_btn=Button(apr_txt_frame, text="Browse", bd=2, activebackground='#c7c7d1',relief=SUNKEN,command=apr_2_btn_click).place(x=786, y=486)

                        def rst_apr():
                            print("Reset")
                            cmb.set('')
                            cmb1.set('')
                            number_of_param.set('')
                            new_text = " "
                            e1.delete(0, tk.END)
                            e1.insert(0, new_text)
                            cmb.place_forget()
                            cmb1.place_forget()
                            apr_2_1_im_label.image =''
                            apr_2_2_im_label.image =''
                            apr_2_3_im_label.image =''
                            apr_txt_entry.delete(0, tk.END)      
                            apr_txt_entry.insert(0, new_text)                            
                                                                                                         

                        plt_rst_apr=PhotoImage(file="reset.png")  
                        sub_plt_rst_apr=plt_rst_apr.subsample(4,4)

                        button_apr_rst = Button(apr_input_frame, text="Reset", fg='#026084', command=rst_apr, image=sub_plt_rst_apr, compound=LEFT, width=130)
                        button_apr_rst.image=sub_plt_rst_apr
                        button_apr_rst.place(x=88, y=316)
                        button_arr.append(button_apr_rst)

                        ttk.Separator(apr_input_frame).place(x=75, y=396, relwidth=0.29)

                        def jnt_go_to_menu():

                            print("Coming soon")

                            apr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                            #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                            lbl_apr=Label(apr_frame, width=20, bg='white').place(x=10, y=10)

                            apr_inner_frame=Frame(apr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                            #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                            apr_input_frame=Frame(apr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                            apr_image_frame=Frame(apr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                            Label(apr_image_frame,bg='white').place(x=565, y=95)

                            apr_txt_frame=Frame(apr_image_frame, width=250, height=195, bg='white', highlightbackground='white').place(x=627,y=388)

                            lbl_apr_txt=Label(apr_txt_frame, width=17, bg='white').place(x=630, y=392)                            

                            print("Apriori frame has been destroyed.")      

                        plt_up=PhotoImage(file="up.png")  
                        sub_plt_up=plt_up.subsample(4,4)     

                        button_jnt_go_to_menu=Button(apr_input_frame, text="Go to menu", fg='#026084', command=jnt_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                        button_jnt_go_to_menu.image=sub_plt_up
                        button_jnt_go_to_menu.place(x=88, y=460)
                        button_arr.append(button_jnt_go_to_menu)                                               

                    # Creating a photoimage object to use image 
                    plt_gen_apr = PhotoImage(file = "images.png") 
                    sub_plt_gen_apr = plt_gen_apr.subsample(4, 4)    

                    button_apr_gen = Button(apr_input_frame, text="Generate", fg='#026084', command=apr_gen, image=sub_plt_gen_apr, compound=LEFT)
                    button_apr_gen.image=sub_plt_gen_apr
                    button_apr_gen.place(x=88, y=246)
                    button_arr.append(button_apr_gen)

                    ttk.Separator(apr_input_frame).place(x=75, y=236, relwidth=0.29)

                cmb1 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        elif (e1.get() == "3" or e1.get() == " 3"):
            print("else 3")
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        def apr_gen():
                            print("Apr Generation")
                            apriori_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ',
                                                       'Ծննդավայր (երկիր)', 'Ծննդավայր (քաղաք/գյուղ)',
                                                       'Ընդունման տարեթիվ', 'Առարկա', 'Առաջին միջանկյալ ստուգում',
                                                       'Երկրորդ միջանկյալ ստուգում', 'Ամփոփիչ քննություն']

                            # Intilizing global vaiables
                            transactions = []

                            # DB file name for Apriori algorithm
                            folder_name = ['apriori']
                            txt_file_name = ['apriori.txt']

                            # Getting dynamically path for appropriate DB file and backup directory
                            absolute_path = sys.path[0]
                            file_path = sys.path[0] + '/' + db

                            #dir_name = absolute_path + '\\' + folder_name[0]
                            #abs_path = dir_name + '\\' + txt_file_name[0]

                            f_path = pathlib.Path(__file__).parent.absolute()
                            f_path = str(f_path)
                            dir_name = f_path + '/' + 'images' + '/' + folder_name[0]
                            abs_path = f_path + '/' + txt_file_name[0]                            

                            # Setting pandas library options
                            pd.set_option('display.max_columns', None)
                            pd.set_option('display.max_rows', None)

                            if not find_plathform():
                                file_path = file_path.replace("\\", "/")
                            data = pd.read_csv(file_path)

                            if (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ուսանողի սեռ' and
                                column_names[
                                    2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Ֆակուլտետ'):
                                # points = 1000
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                  column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ուսանողի սեռ'):
                                # points = 1000
                                start = 2
                                end = 5
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                # points = 1000
                                start = 4
                                end = 7
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ուսանողի սեռ' and
                                  column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Ուսանողի անուն'):
                                # points = 1000
                                start = 1
                                end = 4
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ծննդավայր (երկիր)'):
                                # points = 1000
                                start = 3
                                end = 6
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                  column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ընդունման տարեթիվ'):
                                # points = 1000
                                start = 5
                                end = 8
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Առարկա' and column_names[1] == 'Առաջին միջանկյալ ստուգում' and
                                  column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա'):
                                # points = 1000
                                start = 6
                                end = 9
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                        2] == 'Երկրորդ միջանկյալ ստուգում'):
                                # points = 1000
                                start = 7
                                end = 10
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ուսանողի սեռ' and
                                  column_names[
                                      2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Ֆակուլտետ'):
                                # data = pd.read_csv("CVS/Fac->/Fac3_Sx_COB.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ֆակուլտետ', 'Ուսանողի սեռ', 'Ծննդավայր (երկիր)'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                  column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ֆակուլտետ'):
                                # data = pd.read_csv("CVS/Fac->/Fac3_COB_CV .csv")
                                data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Ծննդավայր (քաղաք/գյուղ)',
                                                                       'Ծննդավայր (երկիր)'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and
                                  column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ֆակուլտետ'):
                                # data = pd.read_csv("CVS/Fac->/Fac3_CV_YOE .csv")
                                data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Ծննդավայր (քաղաք/գյուղ)',
                                                                       'Ընդունման տարեթիվ'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ընդունման տարեթիվ' and
                                  column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Առարկա' and column_names[
                                2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ֆակուլտետ' and column_names[
                                2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ֆակուլտետ'):
                                # data = pd.read_csv("CVS/Fac->/Fac3_YOE_Sbj.csv")
                                data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Առարկա', 'Ընդունման տարեթիվ'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Առարկա' and column_names[
                                2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ֆակուլտետ' and column_names[
                                2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ֆակուլտետ' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ֆակուլտետ'):
                                # data = pd.read_csv("CVS/Fac->/Fac3_Sbj_Fr_Ex.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ֆակուլտետ', 'Առարկա', 'Առաջին միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                  column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ֆակուլտետ' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ֆակուլտետ' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ֆակուլտետ'):
                                # data = pd.read_csv("CVS/Fac->/Fac3_Fr_Ex_Sc_Ex.csv")
                                data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Երկրորդ միջանկյալ ստուգում',
                                                                       'Առաջին միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and
                                  column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ամփոփիչ քննություն' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ֆակուլտետ' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Ամփոփիչ քննությունal_Exam' and column_names[
                                1] == 'Ֆակուլտետ' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ֆակուլտետ'):
                                # data = pd.read_csv("CVS/Fac->/Fac3_Sc_Ex_Fl_Ex.csv")
                                data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Երկրորդ միջանկյալ ստուգում',
                                                                       'Ամփոփիչ քննություն'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and
                                  column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ուսանողի սեռ'):
                                # data = pd.read_csv("CVS/Sx->/Sx3_C_V_YOE .csv")
                                data = pd.read_csv(file_path, usecols=['Ուսանողի սեռ', 'Ծննդավայր (քաղաք/գյուղ)',
                                                                       'Ընդունման տարեթիվ'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ընդունման տարեթիվ' and
                                  column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Առարկա' and
                                    column_names[
                                        2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[
                                        2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ուսանողի սեռ'):
                                # data = pd.read_csv("CVS/Sx->/Sx3_YOE_Sbj .csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ուսանողի սեռ', 'Առարկա', 'Ընդունման տարեթիվ'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Առարկա' and
                                  column_names[
                                      2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ուսանողի սեռ'):
                                # data = pd.read_csv("CVS/Sx->/Sx3_Sbj_Fr_Ex.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ուսանողի սեռ', 'Առարկա', 'Առաջին միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                      2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի սեռ'):
                                # data = pd.read_csv("CVS/Sx->/Sx3_Fr_Ex_Sc_Ex .csv")
                                data = pd.read_csv(file_path, usecols=['Ուսանողի սեռ', 'Երկրորդ միջանկյալ ստուգում',
                                                                       'Առաջին միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Ամփոփիչ քննություն' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի սեռ'):
                                # data = pd.read_csv("CVS/Sx->/Sx3_Sc_Ex_Fn_Ex.csv")
                                data = pd.read_csv(file_path, usecols=['Ուսանողի սեռ', 'Երկրորդ միջանկյալ ստուգում',
                                                                       'Ամփոփիչ քննություն'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                  column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ուսանողի անուն'):
                                # data = pd.read_csv("CVS/Nam->/Name3_COB_CV.csv")
                                data = pd.read_csv(file_path, usecols=['Ուսանողի անուն', 'Ծննդավայր (երկիր)',
                                                                       'Ծննդավայր (քաղաք/գյուղ)'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ուսանողի անուն'):
                                # data = pd.read_csv("CVS/Nam->/Name3_CV_YOE.csv")
                                data = pd.read_csv(file_path, usecols=['Ուսանողի անուն', 'Ընդունման տարեթիվ',
                                                                       'Ծննդավայր (քաղաք/գյուղ)'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ընդունման տարեթիվ' and
                                  column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ուսանողի անուն'):
                                # data = pd.read_csv("CVS/Nam->/Name3_YOE_Sbj.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ուսանողի անուն', 'Ընդունման տարեթիվ', 'Առարկա'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Առարկա' and
                                  column_names[
                                      2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ուսանողի անուն'):
                                # data = pd.read_csv("CVS/Nam->/Name3_Sbj_Fr_Ex.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ուսանողի անուն', 'Առաջին միջանկյալ ստուգում',
                                                            'Առարկա'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                      2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի անուն'):
                                # data = pd.read_csv("CVS/Nam->/Name3_Fr_Ex_Sc_Ex.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ուսանողի անուն', 'Առաջին միջանկյալ ստուգում',
                                                            'Երկրորդ միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Ամփոփիչ քննություն' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի անուն'):
                                # data = pd.read_csv("CVS/Nam->/Name3_Sc_Ex_Fnl_Ex.csv")
                                data = pd.read_csv(file_path, usecols=['Ուսանողի անուն', 'Ամփոփիչ քննություն',
                                                                       'Երկրորդ միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and
                                  column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ծննդավայր (երկիր)'):
                                # data = pd.read_csv("CVS/COB->/COB3_YOE_Sbj.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ծննդավայր (երկիր)', 'Ընդունման տարեթիվ', 'Առարկա'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Առարկա' and
                                  column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ծննդավայր (երկիր)'):
                                # data = pd.read_csv("CVS/COB->/COB3_Sbj_Fr_Ex.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ծննդավայր (երկիր)', 'Առաջին միջանկյալ ստուգում',
                                                            'Առարկա'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                      2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ծննդավայր (երկիր)'):
                                # data = pd.read_csv("CVS/COB->/COB3_Fr_Ex_Sc_Ex.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ծննդավայր (երկիր)', 'Առաջին միջանկյալ ստուգում',
                                                            'Երկրորդ միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ծննդավայր (երկիր)'):
                                # data = pd.read_csv("CVS/COB->/COB3_Fr_Ex_Sc_Ex.csv")
                                data = pd.read_csv(file_path, usecols=['Ծննդավայր (երկիր)', 'Ամփոփիչ քննություն',
                                                                       'Երկրորդ միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[1] == 'Առարկա' and
                                  column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                # data = pd.read_csv("CVS/CV->/CV3_Sbj_Fr_Ex.csv")
                                data = pd.read_csv(file_path, usecols=['Ծննդավայր (քաղաք/գյուղ)', 'Առարկա',
                                                                       'Առաջին միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                      2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                        2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                # data = pd.read_csv("CVS/CV->/CV3_Fr_Ex_Sc_Ex.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ծննդավայր (քաղաք/գյուղ)', 'Երկրորդ միջանկյալ ստուգում',
                                                            'Առաջին միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                        2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                # data = pd.read_csv("CVS/CV->/CV3_Sc_Ex_Fnl_Ex.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ծննդավայր (քաղաք/գյուղ)', 'Երկրորդ միջանկյալ ստուգում',
                                                            'Ամփոփիչ քննություն'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                      2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ընդունման տարեթիվ'):
                                # data = pd.read_csv("CVS/YOE->/YOE_Frst_Exm_Sc_Ex.csv")
                                data = pd.read_csv(file_path,
                                                   usecols=['Ընդունման տարեթիվ', 'Առաջին միջանկյալ ստուգում',
                                                            'Երկրորդ միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ընդունման տարեթիվ'):
                                # data = pd.read_csv("CVS/YOE->/YOE_Sc_Ex_Fnl_Ex.csv")
                                data = pd.read_csv(file_path, usecols=['Ընդունման տարեթիվ', 'Ամփոփիչ քննություն',
                                                                       'Երկրորդ միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])
                            elif (column_names[0] == 'Առարկա' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and
                                  column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ամփոփիչ քննություն' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Առարկա'):
                                # data = pd.read_csv("CVS/Sbj->/Sbj_Scnd_Exm_Fnl_Ex.csv")
                                data = pd.read_csv(file_path, usecols=['Առարկա', 'Ամփոփիչ քննություն',
                                                                       'Երկրորդ միջանկյալ ստուգում'])
                                start = 0
                                end = 3
                                for i in range(0, 1000):
                                    transactions.append([str(data.values[i, j]) for j in range(start, end)])


                            def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png','txt')):
                                """
                                Get the latest image file in the given directory
                                """

                                # get filepaths of all files and dirs in the given dir
                                valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                                # filter out directories, no-extension, and wrong extension files
                                valid_files = [f for f in valid_files if '.' in f and \
                                    f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                                if not valid_files:
                                    raise ValueError("No valid images in %s" % dirpath)

                                return max(valid_files, key=os.path.getmtime)                                      

                            print("------------------------")
                            oht = TransactionEncoder()
                            oht_ary = oht.fit(transactions).transform(transactions)
                            # oht.columns_  # Need to understand is this need or not!!!!
                            df_train = pd.DataFrame(oht_ary, columns=oht.columns_)
                            rules = apriori(df_train, min_support=0.01, use_colnames=True)
                            training_rules = association_rules(rules, metric="confidence", min_threshold=0.01)

                            # Visualization of "Support" VS "Confidence" parameters on graph
                            plt.figure(1)
                            plt.scatter(training_rules['support'], training_rules['confidence'], alpha=0.5)
                            plt.xlabel('Support')
                            plt.ylabel('Confidence')
                            plt.title('Support vs Confidence')
                            mngr = plt.get_current_fig_manager()
                            mngr.window.setGeometry(20, 350, 600, 550)
                            plt.savefig(
                                'images/apriori/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                               "") + '.png')

                            apr_3_1_path=get_latest_image("images/apriori/",'png')          
                            image_apr_3_1 = PhotoImage(file=apr_3_1_path)
                            original_image_apr_3_1 = image_apr_3_1.subsample(3,3) # resize image using subsample

                            apr_3_1_im_label = Label(apr_image_frame,image=original_image_apr_3_1)
                            apr_3_1_im_label.image = original_image_apr_3_1 # keep a reference
                            apr_3_1_im_label.place(x=387, y=118)                            

                            # Visualization of "Support" VS "Lift" parameters on graph
                            plt.figure(2)
                            plt.scatter(training_rules['support'], training_rules['lift'], alpha=0.5)
                            plt.xlabel('Support')
                            plt.ylabel('Lift')
                            plt.title('Support vs Lift')
                            mngr = plt.get_current_fig_manager()
                            mngr.window.setGeometry(657, 350, 600, 550)
                            plt.savefig(
                                'images/apriori/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                               "") + '.png')

                            apr_3_2_path=get_latest_image("images/apriori/",'png')        
                            image_apr_3_2 = PhotoImage(file=apr_3_2_path)
                            original_image_apr_3_2 = image_apr_3_2.subsample(3,3) # resize image using subsample

                            apr_3_2_im_label = Label(apr_image_frame,image=original_image_apr_3_2)
                            apr_3_2_im_label.image = original_image_apr_3_2 # keep a reference
                            apr_3_2_im_label.place(x=627, y=118)                            

                            # Visualization of "Support" VS "Confidence" & "Lift" parameters on graph
                            plt.figure(3)
                            fit = np.polyfit(training_rules['lift'], training_rules['confidence'], 1)
                            fit_fn = np.poly1d(fit)
                            plt.plot(training_rules['lift'], training_rules['confidence'], 'yo',
                                     training_rules['lift'],
                                     fit_fn(training_rules['lift']))
                            plt.xlabel('lift')
                            plt.ylabel('confidence')
                            plt.title('lift vs confidence')                            
                            mngr = plt.get_current_fig_manager()
                            mngr.window.setGeometry(1298, 350, 600, 550)
                            plt.savefig(
                                'images/apriori/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                               "") + '.png')

                            apr_3_3_path=get_latest_image("images/apriori/",'png')          
                            image_apr_3_3 = PhotoImage(file=apr_3_3_path)
                            original_image_apr_3_3 = image_apr_3_3.subsample(3,3) # resize image using subsample

                            apr_3_3_im_label = Label(apr_image_frame,image=original_image_apr_3_3)
                            apr_3_3_im_label.image = original_image_apr_3_3 # keep a reference
                            apr_3_3_im_label.place(x=387, y=308) 

                            def mouse_on_apr_3_1(event):
                                image_apr_3_1 = PhotoImage(file=apr_3_1_path)
                                original_image_apr_3_1 = image_apr_3_1.subsample(2,2) # resize image using subsample

                                apr_3_1_im_label = Label(apr_image_frame,image=original_image_apr_3_1)
                                apr_3_1_im_label.image = original_image_apr_3_1 # keep a reference
                                apr_3_1_im_label.place(x=387, y=118) 

                                return          

                            def mouse_on_apr_3_2(event):
                                image_apr_3_2 = PhotoImage(file=apr_3_2_path)
                                original_image_apr_3_2 = image_apr_3_2.subsample(2,2) # resize image using subsample

                                apr_3_2_im_label = Label(apr_image_frame,image=original_image_apr_3_2)
                                apr_3_2_im_label.image = original_image_apr_3_2 # keep a reference
                                apr_3_2_im_label.place(x=627, y=118) 

                                return        

                            def mouse_on_apr_3_3(event):
                                image_apr_3_3 = PhotoImage(file=apr_3_3_path)
                                original_image_apr_3_3 = image_apr_3_3.subsample(2,2) # resize image using subsample

                                apr_3_3_im_label = Label(apr_image_frame,image=original_image_apr_3_3)
                                apr_3_3_im_label.image = original_image_apr_3_3 # keep a reference
                                apr_3_3_im_label.place(x=387, y=308) 

                                return                                                                

                            apr_3_1_im_label.bind('<Enter>',mouse_on_apr_3_1)                    
                            apr_3_2_im_label.bind('<Enter>',mouse_on_apr_3_2)  
                            apr_3_3_im_label.bind('<Enter>',mouse_on_apr_3_3)                                                        

                            # Taking backup values from above graphs and puting puting appropriate directory
                            try:
                                # Create target Directory
                                os.mkdir(dir_name)
                                print("Directory ", dir_name, " created.")
                            except FileExistsError:
                                print("Directory ", dir_name, " already exists.")
                            file = open(abs_path, 'w', encoding="utf8")
                            file.write(str(training_rules))
                            file.close()

                            now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                            now = str(now)
                            newname = 'apriori_' + now + '.txt'
                            os.rename('apriori.txt', newname)
                            shutil.move(newname,  "images/apriori/")

                            apr_3_txt_path=get_latest_image("images/apriori/",'txt')
                            print(apr_3_txt_path)  

                            def apr_3_btn_click():
                                window.filename =  filedialog.askopenfile(mode='r',initialdir = "images/apriori/",title = apr_3_txt_path,filetypes = (("txt files","*.txt"),("all files","*.*")))

                            apr_txt_entry=Entry(apr_txt_frame, highlightcolor='#ababba',justify=LEFT, relief=SUNKEN, width=18)
                            apr_txt_entry.insert(END,apr_3_txt_path)
                            apr_txt_entry.place(x=637, y=490)

                            apr_txt_btn=Button(apr_txt_frame, text="Browse", bd=2, activebackground='#c7c7d1',relief=SUNKEN,command=apr_3_btn_click).place(x=786, y=486)


                            def rst_apr():
                                print("Reset")
                                cmb.set('')
                                cmb1.set('')
                                number_of_param.set('')                                
                                new_text = " "
                                e1.delete(0, tk.END)
                                e1.insert(0, new_text)
                                cmb.place_forget()
                                cmb1.place_forget()
                                cmb2.place_forget()
                                apr_3_1_im_label.image =''
                                apr_3_2_im_label.image =''
                                apr_3_3_im_label.image =''
                                apr_txt_entry.delete(0, tk.END)      
                                apr_txt_entry.insert(0, new_text) 

                            plt_rst_apr=PhotoImage(file="reset.png")  
                            sub_plt_rst_apr=plt_rst_apr.subsample(4,4)

                            button_apr_rst = Button(apr_input_frame, text="Reset", fg='#026084', command=rst_apr, image=sub_plt_rst_apr, compound=LEFT, width=130)
                            button_apr_rst.image=sub_plt_rst_apr
                            button_apr_rst.place(x=88, y=339)
                            button_arr.append(button_apr_rst)

                            ttk.Separator(apr_input_frame).place(x=75, y=419, relwidth=0.29)                            

                            def jnt_go_to_menu():

                                print("Coming soon")
  
                                apr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                lbl_apr=Label(apr_frame, width=20, bg='white').place(x=10, y=10)
   
                                apr_inner_frame=Frame(apr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                apr_input_frame=Frame(apr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                apr_image_frame=Frame(apr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                Label(apr_image_frame,bg='white').place(x=565, y=95)

                                apr_txt_frame=Frame(apr_image_frame, width=250, height=195, bg='white', highlightbackground='white').place(x=627,y=388)

                                lbl_apr_txt=Label(apr_txt_frame, width=17, bg='white').place(x=630, y=392)                            

                                print("Apriori frame has been destroyed.")      

                            plt_up=PhotoImage(file="up.png")  
                            sub_plt_up=plt_up.subsample(4,4)     

                            button_jnt_go_to_menu=Button(apr_input_frame, text="Go to menu", fg='#026084', command=jnt_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                            button_jnt_go_to_menu.image=sub_plt_up
                            button_jnt_go_to_menu.place(x=88, y=483)
                            button_arr.append(button_jnt_go_to_menu)                            

                        # Creating a photoimage object to use image 
                        plt_gen_apr = PhotoImage(file = "images.png") 
                        sub_plt_gen_apr = plt_gen_apr.subsample(4, 4)    

                        button_apr_gen = Button(apr_input_frame, text="Generate", fg='#026084', command=apr_gen, image=sub_plt_gen_apr, compound=LEFT)
                        button_apr_gen.image=sub_plt_gen_apr
                        button_apr_gen.place(x=88, y=269)
                        button_arr.append(button_apr_gen)                        

                        ttk.Separator(apr_input_frame).place(x=75, y=259, relwidth=0.29)

                    cmb2 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        elif (e1.get() == "4" or e1.get() == " 4"):
            print("else 4")
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            def apr_gen():
                                print("Apr Generation")
                                apriori_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ',
                                                           'Ծննդավայր (երկիր)', 'Ծննդավայր (քաղաք/գյուղ)',
                                                           'Ընդունման տարեթիվ', 'Առարկա',
                                                           'Առաջին միջանկյալ ստուգում',
                                                           'Երկրորդ միջանկյալ ստուգում', 'Ամփոփիչ քննություն']
                                # Intilizing global vaiables
                                transactions = []

                                # DB file name for Apriori algorithm
                                folder_name = ['apriori']
                                txt_file_name = ['apriori.txt']

                                # Getting dynamically path for appropriate DB file and backup directory
                                absolute_path = sys.path[0]
                                file_path = sys.path[0] + '/' + db

                                #dir_name = absolute_path + '\\' + folder_name[0]
                                #abs_path = dir_name + '\\' + txt_file_name[0]

                                f_path = pathlib.Path(__file__).parent.absolute()
                                f_path = str(f_path)
                                dir_name = f_path + '/' + 'images' + '/' + folder_name[0]
                                abs_path = f_path + '/' + txt_file_name[0]                                

                                # Setting pandas library options
                                pd.set_option('display.max_columns', None)
                                pd.set_option('display.max_rows', None)

                                if not find_plathform():
                                    file_path = file_path.replace("\\", "/")
                                data = pd.read_csv(file_path)

                                if (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի անուն' or
                                    column_names[0] == 'Ուսանողի սեռ' or column_names[
                                        0] == 'Ծննդավայր (երկիր)') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ուսանողի անուն' or
                                        column_names[1] == 'Ուսանողի սեռ' or column_names[
                                            1] == 'Ծննդավայր (երկիր)') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ուսանողի անուն' or
                                        column_names[2] == 'Ուսանողի սեռ' or column_names[
                                            2] == 'Ծննդավայր (երկիր)') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ուսանողի անուն' or
                                        column_names[3] == 'Ուսանողի սեռ' or column_names[
                                            3] == 'Ծննդավայր (երկիր)'):
                                    # data = pd.read_csv("CVS/Fac->/Fac_Nm_Sx_COB.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ',
                                                                'Ծննդավայր (երկիր)'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                    0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա') and (
                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա') and (
                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա') and (
                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա'):
                                    # data = pd.read_csv("CVS/COB->/COB_CV_YOE_Sbj.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ծննդավայր (քաղաք/գյուղ)', 'Ընդունման տարեթիվ',
                                                                'Առարկա', 'Ծննդավայր (երկիր)'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Առարկա' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or
                                      column_names[0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Առարկա' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or
                                        column_names[1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Առարկա' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or
                                        column_names[2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Առարկա' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or
                                        column_names[3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    # data = pd.read_csv("CVS/Sbj->/Sbj_F_E_S_E_Fl_E_.csv")
                                    data = pd.read_csv(file_path, usecols=['Առաջին միջանկյալ ստուգում',
                                                                           'Երկրորդ միջանկյալ ստուգում', 'Առարկա',
                                                                           'Ամփոփիչ քննություն'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի սեռ' or
                                      column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                          0] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ուսանողի սեռ' or
                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                            1] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ուսանողի սեռ' or
                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                            2] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ուսանողի սեռ' or
                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                            3] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                    # data = pd.read_csv("CVS/Fac->/Fac4_Sx_COB_CV.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ֆակուլտետ', 'Ուսանողի սեռ',
                                                                'Ծննդավայր (քաղաք/գյուղ)',
                                                                'Ծննդավայր (երկիր)'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ծննդավայր (երկիր)' or
                                      column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                          0] == 'Ընդունման տարեթիվ') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ծննդավայր (երկիր)' or
                                        column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            1] == 'Ընդունման տարեթիվ') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ծննդավայր (երկիր)' or
                                        column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            2] == 'Ընդունման տարեթիվ') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ծննդավայր (երկիր)' or
                                        column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            3] == 'Ընդունման տարեթիվ'):
                                    # data = pd.read_csv("CVS/Fac->/Fac4_COB_CV_YOE.csv")
                                    data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Ընդունման տարեթիվ',
                                                                           'Ծննդավայր (քաղաք/գյուղ)',
                                                                           'Ծննդավայր (երկիր)'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                    0] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                      column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[
                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[
                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[
                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա'):
                                    # data = pd.read_csv("CVS/Fac->/Fac4_CV_YOE_Sbj.csv")
                                    data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Ընդունման տարեթիվ',
                                                                           'Ծննդավայր (քաղաք/գյուղ)', 'Առարկա'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա' or column_names[
                                          0] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա' or column_names[
                                            1] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա' or column_names[
                                            2] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա' or column_names[
                                            3] == 'Առաջին միջանկյալ ստուգում'):
                                    # data = pd.read_csv("CVS/Fac->/Fac4_YOE_Sbj_Fr_Ex.csv")
                                    data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Ընդունման տարեթիվ',
                                                                           'Առաջին միջանկյալ ստուգում', 'Առարկա'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Առարկա' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Առարկա' or
                                        column_names[
                                            1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Առարկա' or
                                        column_names[
                                            2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Առարկա' or
                                        column_names[
                                            3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում'):
                                    # data = pd.read_csv("CVS/Fac->/Fac4_Sbj_Fr_Ex_Sc_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ֆակուլտետ', 'Երկրորդ միջանկյալ ստուգում',
                                                                'Առաջին միջանկյալ ստուգում', 'Առարկա'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    # data = pd.read_csv("CVS/Fac->/Fac4_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ֆակուլտետ', 'Երկրորդ միջանկյալ ստուգում',
                                                                'Առաջին միջանկյալ ստուգում',
                                                                'Ամփոփիչ քննություն'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                    0] == 'Ծննդավայր (երկիր)' or
                                      column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                          0] == 'Ընդունման տարեթիվ') and (
                                        column_names[1] == 'Ուսանողի անուն' or column_names[
                                    1] == 'Ծննդավայր (երկիր)' or
                                        column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            1] == 'Ընդունման տարեթիվ') and (
                                        column_names[2] == 'Ուսանողի անուն' or column_names[
                                    2] == 'Ծննդավայր (երկիր)' or
                                        column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            2] == 'Ընդունման տարեթիվ') and (
                                        column_names[3] == 'Ուսանողի անուն' or column_names[
                                    3] == 'Ծննդավայր (երկիր)' or
                                        column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            3] == 'Ընդունման տարեթիվ'):
                                    # data = pd.read_csv("CVS/Nam->/Name4_COB_CV_YOE.csv")
                                    data = pd.read_csv(file_path, usecols=['Ուսանողի անուն', 'Ծննդավայր (երկիր)',
                                                                           'Ծննդավայր (քաղաք/գյուղ)',
                                                                           'Ընդունման տարեթիվ'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                    0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա') and (
                                        column_names[1] == 'Ուսանողի անուն' or column_names[
                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա') and (
                                        column_names[2] == 'Ուսանողի անուն' or column_names[
                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա') and (
                                        column_names[3] == 'Ուսանողի անուն' or column_names[
                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա'):
                                    # data = pd.read_csv("CVS/Nam->/Name4_CV_YOE_Sbj.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ուսանողի անուն', 'Առարկա',
                                                                'Ծննդավայր (քաղաք/գյուղ)',
                                                                'Ընդունման տարեթիվ'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                    0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա' or column_names[
                                          0] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ուսանողի անուն' or column_names[
                                    1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա' or column_names[
                                            1] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ուսանողի անուն' or column_names[
                                    2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա' or column_names[
                                            2] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ուսանողի անուն' or column_names[
                                    3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա' or column_names[
                                            3] == 'Առաջին միջանկյալ ստուգում'):
                                    # data = pd.read_csv("CVS/Nam->/Name4_YOE_Sbj_Fr_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ուսանողի անուն', 'Առարկա',
                                                                'Առաջին միջանկյալ ստուգում',
                                                                'Ընդունման տարեթիվ'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Առարկա' or
                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Առարկա' or
                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ուսանողի անուն' or column_names[2] == 'Առարկա' or
                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ուսանողի անուն' or column_names[3] == 'Առարկա' or
                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում'):
                                    # data = pd.read_csv("CVS/Nam->/Name4_Sbj_Fr_Ex_Sc_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ուսանողի անուն', 'Առարկա',
                                                                'Առաջին միջանկյալ ստուգում',
                                                                'Երկրորդ միջանկյալ ստուգում'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ուսանողի անուն' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ուսանողի անուն' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ուսանողի անուն' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    # data = pd.read_csv("CVS/Nam->/Name4_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                    data = pd.read_csv(file_path, usecols=['Ուսանողի անուն', 'Ամփոփիչ քննություն',
                                                                           'Առաջին միջանկյալ ստուգում',
                                                                           'Երկրորդ միջանկյալ ստուգում'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                    0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա') and (
                                        column_names[1] == 'Ուսանողի սեռ' or column_names[
                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա') and (
                                        column_names[2] == 'Ուսանողի սեռ' or column_names[
                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա') and (
                                        column_names[3] == 'Ուսանողի սեռ' or column_names[
                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա'):
                                    # data = pd.read_csv("CVS/Sx->/Sx4_C_V_YOE_Sbj.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ուսանողի սեռ', 'Ծննդավայր (քաղաք/գյուղ)',
                                                                'Ընդունման տարեթիվ', 'Առարկա'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա' or column_names[
                                          0] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ուսանողի սեռ' or column_names[
                                    1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա' or column_names[
                                            1] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ուսանողի սեռ' or column_names[
                                    2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա' or column_names[
                                            2] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ուսանողի սեռ' or column_names[
                                    3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա' or column_names[
                                            3] == 'Առաջին միջանկյալ ստուգում'):
                                    # data = pd.read_csv("CVS/Sx->/Sx4_YOE_Sbj_Fr_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ուսանողի սեռ', 'Առաջին միջանկյալ ստուգում',
                                                                'Ընդունման տարեթիվ', 'Առարկա'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Առարկա' or
                                      column_names[
                                          0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Առարկա' or
                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ուսանողի սեռ' or column_names[2] == 'Առարկա' or
                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ուսանողի սեռ' or column_names[3] == 'Առարկա' or
                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում'):
                                    # data = pd.read_csv("CVS/Sx->/Sx4_Sbj_Fr_Ex_Sc_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ուսանողի սեռ', 'Առաջին միջանկյալ ստուգում',
                                                                'Երկրորդ միջանկյալ ստուգում', 'Առարկա'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ուսանողի սեռ' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ուսանողի սեռ' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ուսանողի սեռ' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    # data = pd.read_csv("CVS/Sx->/Sx4_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ուսանողի սեռ', 'Առաջին միջանկյալ ստուգում',
                                                                'Երկրորդ միջանկյալ ստուգում',
                                                                'Ամփոփիչ քննություն'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                    0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[
                                          0] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                    1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[
                                            1] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                    2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[
                                            2] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                    3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[
                                            3] == 'Առաջին միջանկյալ ստուգում'):
                                    # data = pd.read_csv("CVS/COB->/COB4_YOE_Sbj_Fr_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ծննդավայր (երկիր)', 'Ընդունման տարեթիվ', 'Առարկա',
                                                                'Առաջին միջանկյալ ստուգում'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Առարկա' or
                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Առարկա' or
                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[2] == 'Առարկա' or
                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[3] == 'Առարկա' or
                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում'):
                                    # data = pd.read_csv("CVS/COB->/COB4_Sbj_Fr_Ex_Sc_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ծննդավայր (երկիր)', 'Երկրորդ միջանկյալ ստուգում',
                                                                'Առարկա', 'Առաջին միջանկյալ ստուգում'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    # data = pd.read_csv("CVS/COB->/COB4_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ծննդավայր (երկիր)', 'Երկրորդ միջանկյալ ստուգում',
                                                                'Ամփոփիչ քննություն', 'Առաջին միջանկյալ ստուգում'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Առարկա' or
                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    1] == 'Առարկա' or
                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    2] == 'Առարկա' or
                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    3] == 'Առարկա' or
                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում'):
                                    # data = pd.read_csv("CVS/CV->/CV4_Sbj_Fr_Ex_Sc_Ex.csv")
                                    data = pd.read_csv(file_path, usecols=['Ծննդավայր (քաղաք/գյուղ)', 'Առարկա',
                                                                           'Առաջին միջանկյալ ստուգում',
                                                                           'Երկրորդ միջանկյալ ստուգում'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    # data = pd.read_csv("CVS/CV->/CV4_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ծննդավայր (քաղաք/գյուղ)', 'Ամփոփիչ քննություն',
                                                                'Առաջին միջանկյալ ստուգում',
                                                                'Երկրորդ միջանկյալ ստուգում'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                elif (column_names[0] == 'Ընդունման տարեթիվ' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ընդունման տարեթիվ' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ընդունման տարեթիվ' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ընդունման տարեթիվ' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    # data = pd.read_csv("CVS/YOE->/YOE4_Fst_Exm_Sc_Ex_Fnl_Ex.csv")
                                    data = pd.read_csv(file_path,
                                                       usecols=['Ընդունման տարեթիվ', 'Ամփոփիչ քննություն',
                                                                'Առաջին միջանկյալ ստուգում',
                                                                'Երկրորդ միջանկյալ ստուգում'])
                                    # points = 1000
                                    start = 0
                                    end = 4
                                    for i in range(0, 1000):
                                        transactions.append([str(data.values[i, j]) for j in range(start, end)])

                                def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png','txt')):
                                    """
                                    Get the latest image file in the given directory
                                    """

                                    # get filepaths of all files and dirs in the given dir
                                    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                                    # filter out directories, no-extension, and wrong extension files
                                    valid_files = [f for f in valid_files if '.' in f and \
                                        f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                                    if not valid_files:
                                        raise ValueError("No valid images in %s" % dirpath)

                                    return max(valid_files, key=os.path.getmtime)                                           

                                print("------------------------")
                                oht = TransactionEncoder()
                                oht_ary = oht.fit(transactions).transform(transactions)
                                # oht.columns_  # Need to understand is this need or not!!!!
                                df_train = pd.DataFrame(oht_ary, columns=oht.columns_)
                                rules = apriori(df_train, min_support=0.01, use_colnames=True)
                                training_rules = association_rules(rules, metric="confidence", min_threshold=0.01)

                                # Visualization of "Support" VS "Confidence" parameters on graph
                                plt.figure(1)
                                plt.scatter(training_rules['support'], training_rules['confidence'], alpha=0.5)
                                plt.xlabel('Support')
                                plt.ylabel('Confidence')
                                plt.title('Support vs Confidence')
                                mngr = plt.get_current_fig_manager()
                                mngr.window.setGeometry(20, 350, 600, 550)
                                plt.savefig(
                                    'images/apriori/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(
                                        " ",
                                        "") + '.png')

                                apr_4_1_path=get_latest_image("images/apriori/",'png')          
                                image_apr_4_1 = PhotoImage(file=apr_4_1_path)
                                original_image_apr_4_1 = image_apr_4_1.subsample(3,3) # resize image using subsample

                                apr_4_1_im_label = Label(apr_image_frame,image=original_image_apr_4_1)
                                apr_4_1_im_label.image = original_image_apr_4_1 # keep a reference
                                apr_4_1_im_label.place(x=387, y=118)                                

                                # Visualization of "Support" VS "Lift" parameters on graph
                                plt.figure(2)
                                plt.scatter(training_rules['support'], training_rules['lift'], alpha=0.5)
                                plt.xlabel('Support')
                                plt.ylabel('Lift')
                                plt.title('Support vs Lift')
                                mngr = plt.get_current_fig_manager()
                                mngr.window.setGeometry(657, 350, 600, 550)
                                plt.savefig(
                                    'images/apriori/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(
                                        " ",
                                        "") + '.png')

                                apr_4_2_path=get_latest_image("images/apriori/",'png')        
                                image_apr_4_2 = PhotoImage(file=apr_4_2_path)
                                original_image_apr_4_2 = image_apr_4_2.subsample(3,3) # resize image using subsample

                                apr_4_2_im_label = Label(apr_image_frame,image=original_image_apr_4_2)
                                apr_4_2_im_label.image = original_image_apr_4_2 # keep a reference
                                apr_4_2_im_label.place(x=627, y=118)                                 

                                # Visualization of "Support" VS "Confidence" & "Lift" parameters on graph
                                plt.figure(3)
                                fit = np.polyfit(training_rules['lift'], training_rules['confidence'], 1)
                                fit_fn = np.poly1d(fit)
                                plt.plot(training_rules['lift'], training_rules['confidence'], 'yo',
                                         training_rules['lift'], fit_fn(training_rules['lift']))
                                plt.xlabel('lift')
                                plt.ylabel('confidence')
                                plt.title('lift vs confidence')                                 
                                mngr = plt.get_current_fig_manager()
                                mngr.window.setGeometry(1298, 350, 600, 550)
                                plt.savefig(
                                    'images/apriori/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(
                                        " ",
                                        "") + '.png')

                                apr_4_3_path=get_latest_image("images/apriori/",'png')          
                                image_apr_4_3 = PhotoImage(file=apr_4_3_path)
                                original_image_apr_4_3 = image_apr_4_3.subsample(3,3) # resize image using subsample

                                apr_4_3_im_label = Label(apr_image_frame,image=original_image_apr_4_3)
                                apr_4_3_im_label.image = original_image_apr_4_3 # keep a reference
                                apr_4_3_im_label.place(x=387, y=308)                           

                                def mouse_on_apr_4_1(event):
                                    image_apr_4_1 = PhotoImage(file=apr_4_1_path)
                                    original_image_apr_4_1 = image_apr_4_1.subsample(2,2) # resize image using subsample

                                    apr_4_1_im_label = Label(apr_image_frame,image=original_image_apr_4_1)
                                    apr_4_1_im_label.image = original_image_apr_4_1 # keep a reference
                                    apr_4_1_im_label.place(x=387, y=118) 

                                    return          

                                def mouse_on_apr_4_2(event):
                                    image_apr_4_2 = PhotoImage(file=apr_4_2_path)
                                    original_image_apr_4_2 = image_apr_4_2.subsample(2,2) # resize image using subsample

                                    apr_4_2_im_label = Label(apr_image_frame,image=original_image_apr_4_2)
                                    apr_4_2_im_label.image = original_image_apr_4_2 # keep a reference
                                    apr_4_2_im_label.place(x=627, y=118) 

                                    return        

                                def mouse_on_apr_4_3(event):
                                    image_apr_4_3 = PhotoImage(file=apr_4_3_path)
                                    original_image_apr_4_3 = image_apr_4_3.subsample(2,2) # resize image using subsample

                                    apr_4_3_im_label = Label(apr_image_frame,image=original_image_apr_4_3)
                                    apr_4_3_im_label.image = original_image_apr_4_3 # keep a reference
                                    apr_4_3_im_label.place(x=387, y=308) 

                                    return                                                                

                                apr_4_1_im_label.bind('<Enter>',mouse_on_apr_4_1)                    
                                apr_4_2_im_label.bind('<Enter>',mouse_on_apr_4_2)  
                                apr_4_3_im_label.bind('<Enter>',mouse_on_apr_4_3)                                                        

                                # Taking backup values from above graphs and puting puting appropriate directory
                                try:
                                    # Create target Directory
                                    os.mkdir(dir_name)
                                    print("Directory ", dir_name, " created.")
                                except FileExistsError:
                                    print("Directory ", dir_name, " already exists.")
                                file = open(abs_path, 'w', encoding="utf8")
                                file.write(str(training_rules))
                                file.close()

                                now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                now = str(now)
                                newname = 'apriori_' + now + '.txt'
                                os.rename('apriori.txt', newname)
                                shutil.move(newname,  "images/apriori/")

                                apr_4_txt_path=get_latest_image("images/apriori/",'txt')
                                print(apr_4_txt_path)  

                                def apr_4_btn_click():
                                    window.filename =  filedialog.askopenfile(mode='r',initialdir = "images/apriori/",title = apr_4_txt_path,filetypes = (("txt files","*.txt"),("all files","*.*")))

                                apr_txt_entry=Entry(apr_txt_frame, highlightcolor='#ababba',justify=LEFT, relief=SUNKEN, width=18)
                                apr_txt_entry.insert(END,apr_4_txt_path)
                                apr_txt_entry.place(x=637, y=490)

                                apr_txt_btn=Button(apr_txt_frame, text="Browse", bd=2, activebackground='#c7c7d1',relief=SUNKEN,command=apr_4_btn_click).place(x=786, y=486)                                

                                def rst_apr():
                                    print("Reset")
                                    cmb.set('')
                                    cmb1.set('')
                                    number_of_param.set('')                                     
                                    new_text = " "
                                    e1.delete(0, tk.END)
                                    e1.insert(0, new_text)
                                    cmb.place_forget()
                                    cmb1.place_forget()
                                    cmb2.place_forget()
                                    cmb3.place_forget()
                                    apr_4_1_im_label.image =''
                                    apr_4_2_im_label.image =''
                                    apr_4_3_im_label.image =''
                                    apr_txt_entry.delete(0, tk.END)      
                                    apr_txt_entry.insert(0, new_text) 

                                plt_rst_apr=PhotoImage(file="reset.png")  
                                sub_plt_rst_apr=plt_rst_apr.subsample(4,4)

                                button_apr_rst = Button(apr_input_frame, text="Reset", fg='#026084', command=rst_apr, image=sub_plt_rst_apr, compound=LEFT, width=130)
                                button_apr_rst.image=sub_plt_rst_apr
                                button_apr_rst.place(x=88, y=362)
                                button_arr.append(button_apr_rst)

                                ttk.Separator(apr_input_frame).place(x=75, y=442, relwidth=0.29)                            

                                def jnt_go_to_menu():

                                    print("Coming soon")
  
                                    apr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                    #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                    lbl_apr=Label(apr_frame, width=20, bg='white').place(x=10, y=10)
   
                                    apr_inner_frame=Frame(apr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                    #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                    apr_input_frame=Frame(apr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                    apr_image_frame=Frame(apr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                    Label(apr_image_frame,bg='white').place(x=565, y=95)

                                    apr_txt_frame=Frame(apr_image_frame, width=250, height=195, bg='white', highlightbackground='white').place(x=627,y=388)

                                    lbl_apr_txt=Label(apr_txt_frame, width=17, bg='white').place(x=630, y=392)                            

                                    print("Apriori frame has been destroyed.")      

                                plt_up=PhotoImage(file="up.png")  
                                sub_plt_up=plt_up.subsample(4,4)     

                                button_jnt_go_to_menu=Button(apr_input_frame, text="Go to menu", fg='#026084', command=jnt_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                button_jnt_go_to_menu.image=sub_plt_up
                                button_jnt_go_to_menu.place(x=88, y=486)
                                button_arr.append(button_jnt_go_to_menu)                            

                            # Creating a photoimage object to use image 
                            plt_gen_apr = PhotoImage(file = "images.png") 
                            sub_plt_gen_apr = plt_gen_apr.subsample(4, 4)    

                            button_apr_gen = Button(apr_input_frame, text="Generate", fg='#026084', command=apr_gen, image=sub_plt_gen_apr, compound=LEFT)
                            button_apr_gen.image=sub_plt_gen_apr
                            button_apr_gen.place(x=88, y=292)
                            button_arr.append(button_apr_gen) 

                            ttk.Separator(apr_input_frame).place(x=75, y=282, relwidth=0.29)

                        cmb3 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)        

        elif (e1.get() == "5" or e1.get() == " 5"):
            print("else 5")
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):
                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                def apr_gen():
                                    print("Apr Generation")
                                    apriori_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ',
                                                               'Ծննդավայր (երկիր)', 'Ծննդավայր (քաղաք/գյուղ)',
                                                               'Ընդունման տարեթիվ', 'Առարկա',
                                                               'Առաջին միջանկյալ ստուգում',
                                                               'Երկրորդ միջանկյալ ստուգում', 'Ամփոփիչ քննություն']

                                    # Intilizing global vaiables
                                    transactions = []

                                    # DB file name for Apriori algorithm
                                    folder_name = ['apriori']
                                    txt_file_name = ['apriori.txt']

                                    # Getting dynamically path for appropriate DB file and backup directory
                                    absolute_path = sys.path[0]
                                    file_path = sys.path[0] + '/' + db

                                    #dir_name = absolute_path + '\\' + folder_name[0]
                                    #abs_path = dir_name + '\\' + txt_file_name[0]

                                    f_path = pathlib.Path(__file__).parent.absolute()
                                    f_path = str(f_path)
                                    dir_name = f_path + '/' + 'images' + '/' + folder_name[0]
                                    abs_path = f_path + '/' + txt_file_name[0]                                     

                                    # Setting pandas library options
                                    pd.set_option('display.max_columns', None)
                                    pd.set_option('display.max_rows', None)

                                    if not find_plathform():
                                        file_path = file_path.replace("\\", "/")
                                    data = pd.read_csv(file_path)

                                    if (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի անուն' or
                                        column_names[0] == 'Ուսանողի սեռ' or column_names[
                                            0] == 'Ծննդավայր (երկիր)' or
                                        column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ուսանողի անուն' or
                                            column_names[1] == 'Ուսանողի սեռ' or column_names[
                                                1] == 'Ծննդավայր (երկիր)' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ուսանողի անուն' or
                                            column_names[2] == 'Ուսանողի սեռ' or column_names[
                                                2] == 'Ծննդավայր (երկիր)' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ուսանողի անուն' or
                                            column_names[3] == 'Ուսանողի սեռ' or column_names[
                                                3] == 'Ծննդավայր (երկիր)' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[4] == 'Ուսանողի անուն' or
                                            column_names[4] == 'Ուսանողի սեռ' or column_names[
                                                4] == 'Ծննդավայր (երկիր)' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                        # data = pd.read_csv("CVS/Fac->/Fac_Nm_Sx_COB.csv")
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում'):
                                        # data = pd.read_csv("CVS/Fac->/Fac_Nm_Sx_COB.csv")
                                        # points = 1000
                                        start = 4
                                        end = 9
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                          column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                            column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                            column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                2] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                            column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                            column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                4] == 'Ամփոփիչ քննություն'):
                                        # data = pd.read_csv("CVS/Fac->/Fac_Nm_Sx_COB.csv")
                                        # points = 1000
                                        start = 5
                                        end = 10
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի սեռ' or
                                          column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                              0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                              0] == 'Ընդունման տարեթիվ') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ուսանողի սեռ' or
                                            column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                1] == 'Ընդունման տարեթիվ') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ուսանողի սեռ' or
                                            column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                2] == 'Ընդունման տարեթիվ') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ուսանողի սեռ' or
                                            column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                3] == 'Ընդունման տարեթիվ') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[4] == 'Ուսանողի սեռ' or
                                            column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                4] == 'Ընդունման տարեթիվ'):
                                        # data = pd.read_csv("CVS/Fac->/Fac5_Sx_COB_CV_YOE.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ֆակուլտետ', 'Ուսանողի սեռ',
                                                                    'Ծննդավայր (երկիր)',
                                                                    'Ծննդավայր (քաղաք/գյուղ)', 'Ընդունման տարեթիվ'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                        0] == 'Ծննդավայր (երկիր)' or
                                          column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                              0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[
                                        1] == 'Ծննդավայր (երկիր)' or
                                            column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[
                                        2] == 'Ծննդավայր (երկիր)' or
                                            column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[
                                        3] == 'Ծննդավայր (երկիր)' or
                                            column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[
                                        4] == 'Ծննդավայր (երկիր)' or
                                            column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա'):
                                        # data = pd.read_csv("CVS/Fac->/Fac5_COB_CV_YOE_Sbj.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ֆակուլտետ', 'Առարկա', 'Ծննդավայր (երկիր)',
                                                                    'Ծննդավայր (քաղաք/գյուղ)', 'Ընդունման տարեթիվ'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                        0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                          column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[
                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                            column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[
                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                            column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[
                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                            column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[
                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or
                                            column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում'):
                                        # data = pd.read_csv("CVS/Fac->/Fac5_CV_YOE_Sbj_Fr_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ֆակուլտետ', 'Առարկա',
                                                                    'Առաջին միջանկյալ ստուգում',
                                                                    'Ծննդավայր (քաղաք/գյուղ)', 'Ընդունման տարեթիվ'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                        0] == 'Ընդունման տարեթիվ' or
                                          column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[
                                        1] == 'Ընդունման տարեթիվ' or
                                            column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[
                                        2] == 'Ընդունման տարեթիվ' or
                                            column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[
                                        3] == 'Ընդունման տարեթիվ' or
                                            column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[
                                        4] == 'Ընդունման տարեթիվ' or
                                            column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում'):
                                        # data = pd.read_csv("CVS/Fac->/Fac5_YOE_Sbj_Fr_Ex_Sc_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ֆակուլտետ', 'Առարկա',
                                                                    'Առաջին միջանկյալ ստուգում',
                                                                    'Երկրորդ միջանկյալ ստուգում',
                                                                    'Ընդունման տարեթիվ'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Առարկա' or
                                          column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Առարկա' or
                                            column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Առարկա' or
                                            column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                2] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Առարկա' or
                                            column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[4] == 'Առարկա' or
                                            column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                4] == 'Ամփոփիչ քննություն'):
                                        # data = pd.read_csv("CVS/Fac->/Fac5_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ֆակուլտետ', 'Առարկա',
                                                                    'Առաջին միջանկյալ ստուգում',
                                                                    'Երկրորդ միջանկյալ ստուգում',
                                                                    'Ամփոփիչ քննություն'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                        0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                          column_names[0] == 'Ընդունման տարեթիվ' or column_names[
                                              0] == 'Առարկա') and (
                                            column_names[1] == 'Ուսանողի անուն' or column_names[
                                        1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                            column_names[1] == 'Ընդունման տարեթիվ' or column_names[
                                                1] == 'Առարկա') and (
                                            column_names[2] == 'Ուսանողի անուն' or column_names[
                                        2] == 'Ծննդավայր (երկիր)' or column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                            column_names[2] == 'Ընդունման տարեթիվ' or column_names[
                                                2] == 'Առարկա') and (
                                            column_names[3] == 'Ուսանողի անուն' or column_names[
                                        3] == 'Ծննդավայր (երկիր)' or column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                            column_names[3] == 'Ընդունման տարեթիվ' or column_names[
                                                3] == 'Առարկա') and (
                                            column_names[4] == 'Ուսանողի անուն' or column_names[
                                        4] == 'Ծննդավայր (երկիր)' or column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                            column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա'):
                                        # data = pd.read_csv("CVS/Nam->/Name5_COB_CV_YOE_Sbj.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ուսանողի անուն', 'Ծննդավայր (երկիր)',
                                                                    'Ծննդավայր (քաղաք/գյուղ)',
                                                                    'Ընդունման տարեթիվ', 'Առարկա'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                        0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                          column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ուսանողի անուն' or column_names[
                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                            column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ուսանողի անուն' or column_names[
                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                            column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ուսանողի անուն' or column_names[
                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                            column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ուսանողի անուն' or column_names[
                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or
                                            column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում'):
                                        # data = pd.read_csv("CVS/Nam->/Name5_CV_YOE_Sbj_Fr_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ուսանողի անուն', 'Առաջին միջանկյալ ստուգում',
                                                                    'Ծննդավայր (քաղաք/գյուղ)', 'Ընդունման տարեթիվ',
                                                                    'Առարկա'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                        0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ուսանողի անուն' or column_names[
                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ուսանողի անուն' or column_names[
                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ուսանողի անուն' or column_names[
                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ուսանողի անուն' or column_names[
                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում'):
                                        # data = pd.read_csv("CVS/Nam->/Name5_YOE_Sbj_Fr_Ex_Sc_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ուսանողի անուն', 'Առաջին միջանկյալ ստուգում',
                                                                    'Երկրորդ միջանկյալ ստուգում',
                                                                    'Ընդունման տարեթիվ',
                                                                    'Առարկա'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Առարկա' or
                                          column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Առարկա' or
                                            column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ուսանողի անուն' or column_names[2] == 'Առարկա' or
                                            column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                2] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ուսանողի անուն' or column_names[3] == 'Առարկա' or
                                            column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ուսանողի անուն' or column_names[4] == 'Առարկա' or
                                            column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                4] == 'Ամփոփիչ քննություն'):
                                        # data = pd.read_csv("CVS/Nam->/Name5_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ուսանողի անուն', 'Առաջին միջանկյալ ստուգում',
                                                                    'Երկրորդ միջանկյալ ստուգում',
                                                                    'Ամփոփիչ քննություն',
                                                                    'Առարկա'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                        0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                          column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ուսանողի սեռ' or column_names[
                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                            column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ուսանողի սեռ' or column_names[
                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                            column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ուսանողի սեռ' or column_names[
                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                            column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ուսանողի սեռ' or column_names[
                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or
                                            column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում'):
                                        # data = pd.read_csv("CVS/Sx->/Sx5_C_V_YOE_Sbj_Fr_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ուսանողի սեռ', 'Ծննդավայր (քաղաք/գյուղ)',
                                                                    'Ընդունման տարեթիվ',
                                                                    'Առաջին միջանկյալ ստուգում',
                                                                    'Առարկա'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                        0] == 'Ընդունման տարեթիվ' or
                                          column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ուսանողի սեռ' or column_names[
                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ուսանողի սեռ' or column_names[
                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ուսանողի սեռ' or column_names[
                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ուսանողի սեռ' or column_names[
                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում'):
                                        # data = pd.read_csv("CVS/Sx->/Sx5_YOE_Sbj_Fr_Ex_Sc_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ուսանողի սեռ', 'Երկրորդ միջանկյալ ստուգում',
                                                                    'Ընդունման տարեթիվ',
                                                                    'Առաջին միջանկյալ ստուգում',
                                                                    'Առարկա'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Առարկա' or
                                          column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Առարկա' or
                                            column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ուսանողի սեռ' or column_names[2] == 'Առարկա' or
                                            column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                2] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ուսանողի սեռ' or column_names[3] == 'Առարկա' or
                                            column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ուսանողի սեռ' or column_names[4] == 'Առարկա' or
                                            column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                4] == 'Ամփոփիչ քննություն'):
                                        # data = pd.read_csv("CVS/Sx->/Sx5_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ուսանողի սեռ', 'Երկրորդ միջանկյալ ստուգում',
                                                                    'Ամփոփիչ քննություն',
                                                                    'Առաջին միջանկյալ ստուգում',
                                                                    'Առարկա'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                        0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում'):
                                        # data = pd.read_csv("CVS/COB->/COB5_YOE_Sbj_Fr_Ex_Sc_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ծննդավայր (երկիր)', 'Ընդունման տարեթիվ',
                                                                    'Առարկա',
                                                                    'Առաջին միջանկյալ ստուգում',
                                                                    'Երկրորդ միջանկյալ ստուգում'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Առարկա' or
                                          column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Առարկա' or
                                            column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ծննդավայր (երկիր)' or column_names[2] == 'Առարկա' or
                                            column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ծննդավայր (երկիր)' or column_names[3] == 'Առարկա' or
                                            column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ծննդավայր (երկիր)' or column_names[4] == 'Առարկա' or
                                            column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                4] == 'Ամփոփիչ քննություն'):
                                        # data = pd.read_csv("CVS/COB->/COB5_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ծննդավայր (երկիր)', 'Ամփոփիչ քննություն',
                                                                    'Առարկա',
                                                                    'Առաջին միջանկյալ ստուգում',
                                                                    'Երկրորդ միջանկյալ ստուգում'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])
                                    elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        0] == 'Առարկա' or
                                          column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում' or
                                            column_names[1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում' or
                                            column_names[2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                2] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում' or
                                            column_names[3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում' or
                                            column_names[4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                4] == 'Ամփոփիչ քննություն'):
                                        # data = pd.read_csv("CVS/CV->/CV5_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                        data = pd.read_csv(file_path,
                                                           usecols=['Ծննդավայր (քաղաք/գյուղ)', 'Ամփոփիչ քննություն',
                                                                    'Առարկա', 'Առաջին միջանկյալ ստուգում',
                                                                    'Երկրորդ միջանկյալ ստուգում'])
                                        # points = 1000
                                        start = 0
                                        end = 5
                                        for i in range(0, 1000):
                                            transactions.append([str(data.values[i, j]) for j in range(start, end)])

                                    def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png','txt')):
                                        """
                                        Get the latest image file in the given directory
                                        """

                                        # get filepaths of all files and dirs in the given dir
                                        valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                                        # filter out directories, no-extension, and wrong extension files
                                        valid_files = [f for f in valid_files if '.' in f and \
                                            f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                                        if not valid_files:
                                            raise ValueError("No valid images in %s" % dirpath)

                                        return max(valid_files, key=os.path.getmtime)                                              

                                    print("------------------------")
                                    oht = TransactionEncoder()
                                    oht_ary = oht.fit(transactions).transform(transactions)
                                    # oht.columns_  # Need to understand is this need or not!!!!
                                    df_train = pd.DataFrame(oht_ary, columns=oht.columns_)
                                    rules = apriori(df_train, min_support=0.01, use_colnames=True)
                                    training_rules = association_rules(rules, metric="confidence",
                                                                       min_threshold=0.01)

                                    # Visualization of "Support" VS "Confidence" parameters on graph
                                    plt.figure(1)
                                    plt.scatter(training_rules['support'], training_rules['confidence'], alpha=0.5)
                                    plt.xlabel('Support')
                                    plt.ylabel('Confidence')
                                    plt.title('Support vs Confidence')
                                    mngr = plt.get_current_fig_manager()
                                    mngr.window.setGeometry(20, 350, 600, 550)
                                    plt.savefig(
                                        'images/apriori/' + datetime.now().strftime(
                                            '%Y-%m-%d-%H:%M:%S.%f').replace(
                                            " ", "") + '.png')

                                    apr_5_1_path=get_latest_image("images/apriori/",'png')          
                                    image_apr_5_1 = PhotoImage(file=apr_5_1_path)
                                    original_image_apr_5_1 = image_apr_5_1.subsample(3,3) # resize image using subsample

                                    apr_5_1_im_label = Label(apr_image_frame,image=original_image_apr_5_1)
                                    apr_5_1_im_label.image = original_image_apr_5_1 # keep a reference
                                    apr_5_1_im_label.place(x=387, y=118)                                     

                                    # Visualization of "Support" VS "Lift" parameters on graph
                                    plt.figure(2)
                                    plt.scatter(training_rules['support'], training_rules['lift'], alpha=0.5)
                                    plt.xlabel('Support')
                                    plt.ylabel('Lift')
                                    plt.title('Support vs Lift')
                                    mngr = plt.get_current_fig_manager()
                                    mngr.window.setGeometry(657, 350, 600, 550)
                                    plt.savefig(
                                        'images/apriori/' + datetime.now().strftime(
                                            '%Y-%m-%d-%H:%M:%S.%f').replace(
                                            " ", "") + '.png')

                                    apr_5_2_path=get_latest_image("images/apriori/",'png')        
                                    image_apr_5_2 = PhotoImage(file=apr_5_2_path)
                                    original_image_apr_5_2 = image_apr_5_2.subsample(3,3) # resize image using subsample

                                    apr_5_2_im_label = Label(apr_image_frame,image=original_image_apr_5_2)
                                    apr_5_2_im_label.image = original_image_apr_5_2 # keep a reference
                                    apr_5_2_im_label.place(x=627, y=118)                                     

                                    # Visualization of "Support" VS "Confidence" & "Lift" parameters on graph
                                    plt.figure(3)
                                    fit = np.polyfit(training_rules['lift'], training_rules['confidence'], 1)
                                    fit_fn = np.poly1d(fit)
                                    plt.plot(training_rules['lift'], training_rules['confidence'], 'yo',
                                             training_rules['lift'], fit_fn(training_rules['lift']))
                                    plt.xlabel('lift')
                                    plt.ylabel('confidence')
                                    plt.title('lift vs confidence')                                 
                                    mngr = plt.get_current_fig_manager()
                                    mngr.window.setGeometry(1298, 350, 600, 550)
                                    plt.savefig(
                                        'images/apriori/' + datetime.now().strftime(
                                            '%Y-%m-%d-%H:%M:%S.%f').replace(
                                            " ", "") + '.png')

                                    apr_5_3_path=get_latest_image("images/apriori/",'png')          
                                    image_apr_5_3 = PhotoImage(file=apr_5_3_path)
                                    original_image_apr_5_3 = image_apr_5_3.subsample(3,3) # resize image using subsample

                                    apr_5_3_im_label = Label(apr_image_frame,image=original_image_apr_5_3)
                                    apr_5_3_im_label.image = original_image_apr_5_3 # keep a reference
                                    apr_5_3_im_label.place(x=387, y=308)                                     

                                    def mouse_on_apr_5_1(event):
                                        image_apr_5_1 = PhotoImage(file=apr_5_1_path)
                                        original_image_apr_5_1 = image_apr_5_1.subsample(2,2) # resize image using subsample

                                        apr_5_1_im_label = Label(apr_image_frame,image=original_image_apr_5_1)
                                        apr_5_1_im_label.image = original_image_apr_5_1 # keep a reference
                                        apr_5_1_im_label.place(x=387, y=118) 

                                        return          

                                    def mouse_on_apr_5_2(event):
                                        image_apr_5_2 = PhotoImage(file=apr_5_2_path)
                                        original_image_apr_5_2 = image_apr_5_2.subsample(2,2) # resize image using subsample

                                        apr_5_2_im_label = Label(apr_image_frame,image=original_image_apr_5_2)
                                        apr_5_2_im_label.image = original_image_apr_5_2 # keep a reference
                                        apr_5_2_im_label.place(x=627, y=118) 

                                        return        

                                    def mouse_on_apr_5_3(event):
                                        image_apr_5_3 = PhotoImage(file=apr_5_3_path)
                                        original_image_apr_5_3 = image_apr_5_3.subsample(2,2) # resize image using subsample

                                        apr_5_3_im_label = Label(apr_image_frame,image=original_image_apr_5_3)
                                        apr_5_3_im_label.image = original_image_apr_5_3 # keep a reference
                                        apr_5_3_im_label.place(x=387, y=308) 

                                        return                                                                

                                    apr_5_1_im_label.bind('<Enter>',mouse_on_apr_5_1)                    
                                    apr_5_2_im_label.bind('<Enter>',mouse_on_apr_5_2)  
                                    apr_5_3_im_label.bind('<Enter>',mouse_on_apr_5_3)                                                        

                                    # Taking backup values from above graphs and puting puting appropriate directory
                                    try:
                                        # Create target Directory
                                        os.mkdir(dir_name)
                                        print("Directory ", dir_name, " created.")
                                    except FileExistsError:
                                        print("Directory ", dir_name, " already exists.")
                                    file = open(abs_path, 'w', encoding="utf8")
                                    file.write(str(training_rules))
                                    file.close()

                                    now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                    now = str(now)
                                    newname = 'apriori_' + now + '.txt'
                                    os.rename('apriori.txt', newname)
                                    shutil.move(newname,  "images/apriori/")

                                    apr_5_txt_path=get_latest_image("images/apriori/",'txt')
                                    print(apr_5_txt_path)  

                                    def apr_5_btn_click():
                                        window.filename =  filedialog.askopenfile(mode='r',initialdir = "images/apriori/",title = apr_5_txt_path,filetypes = (("txt files","*.txt"),("all files","*.*")))

                                    apr_txt_entry=Entry(apr_txt_frame, highlightcolor='#ababba',justify=LEFT, relief=SUNKEN, width=18)
                                    apr_txt_entry.insert(END,apr_5_txt_path)
                                    apr_txt_entry.place(x=637, y=490)

                                    apr_txt_btn=Button(apr_txt_frame, text="Browse", bd=2, activebackground='#c7c7d1',relief=SUNKEN,command=apr_5_btn_click).place(x=786, y=486)                                


                                    def rst_apr():
                                        print("Reset")
                                        cmb.set('')
                                        cmb1.set('')
                                        number_of_param.set('')                                           
                                        new_text = " "
                                        e1.delete(0, tk.END)
                                        e1.insert(0, new_text)
                                        cmb.place_forget()
                                        cmb1.place_forget()
                                        cmb2.place_forget()
                                        cmb3.place_forget()
                                        cmb4.place_forget()
                                        apr_5_1_im_label.image =''
                                        apr_5_2_im_label.image =''
                                        apr_5_3_im_label.image =''
                                        apr_txt_entry.delete(0, tk.END)      
                                        apr_txt_entry.insert(0, new_text)

                                    plt_rst_apr=PhotoImage(file="reset.png")  
                                    sub_plt_rst_apr=plt_rst_apr.subsample(4,4)

                                    button_apr_rst = Button(apr_input_frame, text="Reset", fg='#026084', command=rst_apr, image=sub_plt_rst_apr, compound=LEFT, width=130)
                                    button_apr_rst.image=sub_plt_rst_apr
                                    button_apr_rst.place(x=88, y=384)
                                    button_arr.append(button_apr_rst)

                                    ttk.Separator(apr_input_frame).place(x=75, y=464, relwidth=0.29)                            

                                    def jnt_go_to_menu():

                                        print("Coming soon")
  
                                        apr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                        #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                        lbl_apr=Label(apr_frame, width=20, bg='white').place(x=10, y=10)
   
                                        apr_inner_frame=Frame(apr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                        #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                        apr_input_frame=Frame(apr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                        apr_image_frame=Frame(apr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                        Label(apr_image_frame,bg='white').place(x=565, y=95)

                                        apr_txt_frame=Frame(apr_image_frame, width=250, height=195, bg='white', highlightbackground='white').place(x=627,y=388)

                                        lbl_apr_txt=Label(apr_txt_frame, width=17, bg='white').place(x=630, y=392)                            

                                        print("Apriori frame has been destroyed.")      

                                    plt_up=PhotoImage(file="up.png")  
                                    sub_plt_up=plt_up.subsample(4,4)     

                                    button_jnt_go_to_menu=Button(apr_input_frame, text="Go to menu", fg='#026084', command=jnt_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                    button_jnt_go_to_menu.image=sub_plt_up
                                    button_jnt_go_to_menu.place(x=88, y=498)
                                    button_arr.append(button_jnt_go_to_menu)                            

                                # Creating a photoimage object to use image 
                                plt_gen_apr = PhotoImage(file = "images.png") 
                                sub_plt_gen_apr = plt_gen_apr.subsample(4, 4)    

                                button_apr_gen = Button(apr_input_frame, text="Generate", fg='#026084', command=apr_gen, image=sub_plt_gen_apr, compound=LEFT)
                                button_apr_gen.image=sub_plt_gen_apr
                                button_apr_gen.place(x=88, y=314)
                                button_arr.append(button_apr_gen) 

                                ttk.Separator(apr_input_frame).place(x=75, y=304, relwidth=0.29)

                            cmb4 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        elif (e1.get() == "6" or e1.get() == " 6"):
            print("else 6")

            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):
                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                sixth_data = fifth_data

                                for item in fifth_data:
                                    if item == fifth_curr_val:
                                        sixth_data.remove(item)

                                def on_sixth_select(event=None):
                                    sixth_curr_val = cmb5.get()

                                    if len(column_names) > 5:
                                        column_names.pop(5)

                                    column_names.append(sixth_curr_val)

                                    def apr_gen():
                                        print("Apr Generation")

                                        apriori_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ',
                                                                   'Ծննդավայր (երկիր)', 'Ծննդավայր (քաղաք/գյուղ)',
                                                                   'Ընդունման տարեթիվ', 'Առարկա',
                                                                   'Առաջին միջանկյալ ստուգում',
                                                                   'Երկրորդ միջանկյալ ստուգում',
                                                                   'Ամփոփիչ քննություն']

                                        # Intilizing global vaiables
                                        transactions = []

                                        # DB file name for Apriori algorithm
                                        folder_name = ['apriori']
                                        txt_file_name = ['apriori.txt']

                                        # Getting dynamically path for appropriate DB file and backup directory
                                        absolute_path = sys.path[0]

                                        file_path = sys.path[0] + '/' + db

                                        #dir_name = absolute_path + '\\' + folder_name[0]
                                        #abs_path = dir_name + '\\' + txt_file_name[0]

                                        f_path = pathlib.Path(__file__).parent.absolute()
                                        f_path = str(f_path)
                                        dir_name = f_path + '/' + 'images' + '/' + folder_name[0]
                                        abs_path = f_path + '/' + txt_file_name[0]                                         

                                        # Setting pandas library options
                                        pd.set_option('display.max_columns', None)
                                        pd.set_option('display.max_rows', None)

                                        if not find_plathform():
                                            file_path = file_path.replace("\\", "/")
                                        data = pd.read_csv(file_path)

                                        if (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի անուն' or
                                            column_names[0] == 'Ուսանողի սեռ' or column_names[
                                                0] == 'Ծննդավայր (երկիր)' or column_names[
                                                0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                0] == 'Ընդունման տարեթիվ') and (
                                                column_names[1] == 'Ֆակուլտետ' or column_names[
                                            1] == 'Ուսանողի անուն' or
                                                column_names[1] == 'Ուսանողի սեռ' or column_names[
                                                    1] == 'Ծննդավայր (երկիր)' or column_names[
                                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    1] == 'Ընդունման տարեթիվ') and (
                                                column_names[2] == 'Ֆակուլտետ' or column_names[
                                            2] == 'Ուսանողի անուն' or
                                                column_names[2] == 'Ուսանողի սեռ' or column_names[
                                                    2] == 'Ծննդավայր (երկիր)' or column_names[
                                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    2] == 'Ընդունման տարեթիվ') and (
                                                column_names[3] == 'Ֆակուլտետ' or column_names[
                                            3] == 'Ուսանողի անուն' or
                                                column_names[3] == 'Ուսանողի սեռ' or column_names[
                                                    3] == 'Ծննդավայր (երկիր)' or column_names[
                                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    3] == 'Ընդունման տարեթիվ') and (
                                                column_names[4] == 'Ֆակուլտետ' or column_names[
                                            4] == 'Ուսանողի անուն' or
                                                column_names[4] == 'Ուսանողի սեռ' or column_names[
                                                    4] == 'Ծննդավայր (երկիր)' or column_names[
                                                    4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    4] == 'Ընդունման տարեթիվ') and (
                                                column_names[5] == 'Ֆակուլտետ' or column_names[
                                            5] == 'Ուսանողի անուն' or
                                                column_names[5] == 'Ուսանողի սեռ' or column_names[
                                                    5] == 'Ծննդավայր (երկիր)' or column_names[
                                                    5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    5] == 'Ընդունման տարեթիվ'):
                                            # data = pd.read_csv("CVS/Fac->/Fac_Nm_Sx_COB.csv")
                                            # points = 1000
                                            start = 0
                                            end = 6
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])
                                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                              column_names[
                                                  0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                  0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                  0] == 'Ամփոփիչ քննություն') and (
                                                column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                column_names[
                                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    1] == 'Ամփոփիչ քննություն') and (
                                                column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                column_names[
                                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    2] == 'Ամփոփիչ քննություն') and (
                                                column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                column_names[
                                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    3] == 'Ամփոփիչ քննություն') and (
                                                column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                column_names[
                                                    4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    4] == 'Ամփոփիչ քննություն') and (
                                                column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                column_names[
                                                    5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    5] == 'Ամփոփիչ քննություն'):
                                            # data = pd.read_csv("CVS/Fac->/Fac_Nm_Sx_COB.csv")
                                            # points = 1000
                                            start = 4
                                            end = 10
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])
                                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի սեռ' or
                                              column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                                  0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                  0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա') and (
                                                column_names[1] == 'Ֆակուլտետ' or column_names[
                                            1] == 'Ուսանողի սեռ' or
                                                column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա') and (
                                                column_names[2] == 'Ֆակուլտետ' or column_names[
                                            2] == 'Ուսանողի սեռ' or
                                                column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա') and (
                                                column_names[3] == 'Ֆակուլտետ' or column_names[
                                            3] == 'Ուսանողի սեռ' or
                                                column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա') and (
                                                column_names[4] == 'Ֆակուլտետ' or column_names[
                                            4] == 'Ուսանողի սեռ' or
                                                column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                                    4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա') and (
                                                column_names[5] == 'Ֆակուլտետ' or column_names[
                                            5] == 'Ուսանողի սեռ' or
                                                column_names[5] == 'Ծննդավայր (երկիր)' or column_names[
                                                    5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա'):
                                            # data = pd.read_csv("CVS/Fac->/Fac6_Sx_COB_CV_YOE_Sbj.csv")
                                            data = pd.read_csv(file_path,
                                                               usecols=['Ֆակուլտետ', 'Առարկա', 'Ուսանողի սեռ',
                                                                        'Ծննդավայր (երկիր)',
                                                                        'Ծննդավայր (քաղաք/գյուղ)',
                                                                        'Ընդունման տարեթիվ'])
                                            # points = 1000
                                            start = 0
                                            end = 6
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])
                                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                            0] == 'Ծննդավայր (երկիր)' or column_names[
                                                  0] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                              column_names[0] == 'Ընդունման տարեթիվ' or column_names[
                                                  0] == 'Առարկա' or
                                              column_names[0] == 'Առաջին միջանկյալ ստուգում') and (
                                                column_names[1] == 'Ֆակուլտետ' or column_names[
                                            1] == 'Ծննդավայր (երկիր)' or column_names[
                                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                column_names[1] == 'Ընդունման տարեթիվ' or column_names[
                                                    1] == 'Առարկա' or
                                                column_names[1] == 'Առաջին միջանկյալ ստուգում') and (
                                                column_names[2] == 'Ֆակուլտետ' or column_names[
                                            2] == 'Ծննդավայր (երկիր)' or column_names[
                                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                column_names[2] == 'Ընդունման տարեթիվ' or column_names[
                                                    2] == 'Առարկա' or
                                                column_names[2] == 'Առաջին միջանկյալ ստուգում') and (
                                                column_names[3] == 'Ֆակուլտետ' or column_names[
                                            3] == 'Ծննդավայր (երկիր)' or column_names[
                                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                column_names[3] == 'Ընդունման տարեթիվ' or column_names[
                                                    3] == 'Առարկա' or
                                                column_names[3] == 'Առաջին միջանկյալ ստուգում') and (
                                                column_names[4] == 'Ֆակուլտետ' or column_names[
                                            4] == 'Ծննդավայր (երկիր)' or column_names[
                                                    4] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                column_names[4] == 'Ընդունման տարեթիվ' or column_names[
                                                    4] == 'Առարկա' or
                                                column_names[4] == 'Առաջին միջանկյալ ստուգում') and (
                                                column_names[5] == 'Ֆակուլտետ' or column_names[
                                            5] == 'Ծննդավայր (երկիր)' or column_names[
                                                    5] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                column_names[5] == 'Ընդունման տարեթիվ' or column_names[
                                                    5] == 'Առարկա' or
                                                column_names[5] == 'Առաջին միջանկյալ ստուգում'):
                                            # data = pd.read_csv("CVS/Fac->/Fac6_COB_CV_YOE_Sbj_Fr_Ex.csv")
                                            data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Առարկա',
                                                                                   'Առաջին միջանկյալ ստուգում',
                                                                                   'Ծննդավայր (երկիր)',
                                                                                   'Ծննդավայր (քաղաք/գյուղ)',
                                                                                   'Ընդունման տարեթիվ'])
                                            # points = 1000
                                            start = 0
                                            end = 6
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])
                                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                            0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                  0] == 'Ընդունման տարեթիվ' or
                                              column_names[0] == 'Առարկա' or column_names[
                                                  0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                  0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[1] == 'Ֆակուլտետ' or column_names[
                                            1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    1] == 'Ընդունման տարեթիվ' or
                                                column_names[1] == 'Առարկա' or column_names[
                                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[2] == 'Ֆակուլտետ' or column_names[
                                            2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    2] == 'Ընդունման տարեթիվ' or
                                                column_names[2] == 'Առարկա' or column_names[
                                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[3] == 'Ֆակուլտետ' or column_names[
                                            3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    3] == 'Ընդունման տարեթիվ' or
                                                column_names[3] == 'Առարկա' or column_names[
                                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[4] == 'Ֆակուլտետ' or column_names[
                                            4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    4] == 'Ընդունման տարեթիվ' or
                                                column_names[4] == 'Առարկա' or column_names[
                                                    4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    4] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[5] == 'Ֆակուլտետ' or column_names[
                                            5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    5] == 'Ընդունման տարեթիվ' or
                                                column_names[5] == 'Առարկա' or column_names[
                                                    5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    5] == 'Երկրորդ միջանկյալ ստուգում'):
                                            # data = pd.read_csv("CVS/Fac->/Fac6_CV_YOE_Sbj_Fr_Ex_Sc_Ex.csv")
                                            data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Առարկա',
                                                                                   'Առաջին միջանկյալ ստուգում',
                                                                                   'Երկրորդ միջանկյալ ստուգում',
                                                                                   'Ծննդավայր (քաղաք/գյուղ)',
                                                                                   'Ընդունման տարեթիվ'])
                                            # points = 1000
                                            start = 0
                                            end = 6
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])
                                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                            0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                              column_names[
                                                  0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                  0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                  0] == 'Ամփոփիչ քննություն') and (
                                                column_names[1] == 'Ֆակուլտետ' or column_names[
                                            1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                column_names[
                                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    1] == 'Ամփոփիչ քննություն') and (
                                                column_names[2] == 'Ֆակուլտետ' or column_names[
                                            2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                column_names[
                                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    2] == 'Ամփոփիչ քննություն') and (
                                                column_names[3] == 'Ֆակուլտետ' or column_names[
                                            3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                column_names[
                                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    4] == 'Ամփոփիչ քննություն') and (
                                                column_names[4] == 'Ֆակուլտետ' or column_names[
                                            4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                column_names[
                                                    4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    4] == 'Ամփոփիչ քննություն') and (
                                                column_names[5] == 'Ֆակուլտետ' or column_names[
                                            5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                column_names[
                                                    5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    5] == 'Ամփոփիչ քննություն'):
                                            # data = pd.read_csv("CVS/Fac->/Fac6_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                            data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Առարկա',
                                                                                   'Առաջին միջանկյալ ստուգում',
                                                                                   'Երկրորդ միջանկյալ ստուգում',
                                                                                   'Ամփոփիչ քննություն',
                                                                                   'Ընդունման տարեթիվ'])
                                            # points = 1000
                                            start = 0
                                            end = 6
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])
                                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                            0] == 'Ծննդավայր (երկիր)' or column_names[
                                                  0] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                              column_names[0] == 'Ընդունման տարեթիվ' or column_names[
                                                  0] == 'Առարկա' or
                                              column_names[0] == 'Առաջին միջանկյալ ստուգում') and (
                                                column_names[1] == 'Ուսանողի անուն' or column_names[
                                            1] == 'Ծննդավայր (երկիր)' or column_names[
                                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                column_names[1] == 'Ընդունման տարեթիվ' or column_names[
                                                    1] == 'Առարկա' or
                                                column_names[1] == 'Առաջին միջանկյալ ստուգում') and (
                                                column_names[2] == 'Ուսանողի անուն' or column_names[
                                            2] == 'Ծննդավայր (երկիր)' or column_names[
                                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                column_names[2] == 'Ընդունման տարեթիվ' or column_names[
                                                    2] == 'Առարկա' or
                                                column_names[2] == 'Առաջին միջանկյալ ստուգում') and (
                                                column_names[3] == 'Ուսանողի անուն' or column_names[
                                            3] == 'Ծննդավայր (երկիր)' or column_names[
                                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                column_names[3] == 'Ընդունման տարեթիվ' or column_names[
                                                    3] == 'Առարկա' or
                                                column_names[3] == 'Առաջին միջանկյալ ստուգում') and (
                                                column_names[4] == 'Ուսանողի անուն' or column_names[
                                            4] == 'Ծննդավայր (երկիր)' or column_names[
                                                    4] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                column_names[4] == 'Ընդունման տարեթիվ' or column_names[
                                                    4] == 'Առարկա' or
                                                column_names[4] == 'Առաջին միջանկյալ ստուգում') and (
                                                column_names[5] == 'Ուսանողի անուն' or column_names[
                                            5] == 'Ծննդավայր (երկիր)' or column_names[
                                                    5] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                column_names[5] == 'Ընդունման տարեթիվ' or column_names[
                                                    5] == 'Առարկա' or
                                                column_names[5] == 'Առաջին միջանկյալ ստուգում'):
                                            # data = pd.read_csv("CVS/Nam->/Name6_COB_CV_YOE_Sbj_Fr_Ex.csv")
                                            data = pd.read_csv(file_path,
                                                               usecols=['Ուսանողի անուն', 'Ծննդավայր (երկիր)',
                                                                        'Ծննդավայր (քաղաք/գյուղ)',
                                                                        'Ընդունման տարեթիվ',
                                                                        'Առարկա', 'Առաջին միջանկյալ ստուգում'])
                                            # points = 1000
                                            start = 0
                                            end = 6
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])
                                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                            0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                  0] == 'Ընդունման տարեթիվ' or
                                              column_names[0] == 'Առարկա' or column_names[
                                                  0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                  0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[1] == 'Ուսանողի անուն' or column_names[
                                            1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    1] == 'Ընդունման տարեթիվ' or
                                                column_names[1] == 'Առարկա' or column_names[
                                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[2] == 'Ուսանողի անուն' or column_names[
                                            2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    2] == 'Ընդունման տարեթիվ' or
                                                column_names[2] == 'Առարկա' or column_names[
                                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[3] == 'Ուսանողի անուն' or column_names[
                                            3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    3] == 'Ընդունման տարեթիվ' or
                                                column_names[3] == 'Առարկա' or column_names[
                                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[4] == 'Ուսանողի անուն' or column_names[
                                            4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    4] == 'Ընդունման տարեթիվ' or
                                                column_names[4] == 'Առարկա' or column_names[
                                                    4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    4] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[5] == 'Ուսանողի անուն' or column_names[
                                            5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    5] == 'Ընդունման տարեթիվ' or
                                                column_names[5] == 'Առարկա' or column_names[
                                                    5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    5] == 'Երկրորդ միջանկյալ ստուգում'):
                                            # data = pd.read_csv("CVS/Nam->/Name6_CV_YOE_Sbj_Fr_Ex_Sc_Ex.csv")
                                            data = pd.read_csv(file_path,
                                                               usecols=['Ուսանողի անուն',
                                                                        'Երկրորդ միջանկյալ ստուգում',
                                                                        'Ծննդավայր (քաղաք/գյուղ)',
                                                                        'Ընդունման տարեթիվ',
                                                                        'Առարկա', 'Առաջին միջանկյալ ստուգում'])
                                            # points = 1000
                                            start = 0
                                            end = 6
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])
                                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                            0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                              column_names[
                                                  0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                  0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                  0] == 'Ամփոփիչ քննություն') and (
                                                column_names[1] == 'Ուսանողի անուն' or column_names[
                                            1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                column_names[
                                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    1] == 'Ամփոփիչ քննություն') and (
                                                column_names[2] == 'Ուսանողի անուն' or column_names[
                                            2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                column_names[
                                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    2] == 'Ամփոփիչ քննություն') and (
                                                column_names[3] == 'Ուսանողի անուն' or column_names[
                                            3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                column_names[
                                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    3] == 'Ամփոփիչ քննություն') and (
                                                column_names[4] == 'Ուսանողի անուն' or column_names[
                                            4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                column_names[
                                                    4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    4] == 'Ամփոփիչ քննություն') and (
                                                column_names[5] == 'Ուսանողի անուն' or column_names[
                                            5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                column_names[
                                                    5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    5] == 'Ամփոփիչ քննություն'):
                                            # data = pd.read_csv("CVS/Nam->/Name6_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                            data = pd.read_csv(file_path,
                                                               usecols=['Ուսանողի անուն',
                                                                        'Երկրորդ միջանկյալ ստուգում',
                                                                        'Ամփոփիչ քննություն', 'Ընդունման տարեթիվ',
                                                                        'Առարկա', 'Առաջին միջանկյալ ստուգում'])
                                            # points = 1000
                                            start = 0
                                            end = 6
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])
                                        elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                            0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                  0] == 'Ընդունման տարեթիվ' or
                                              column_names[0] == 'Առարկա' or column_names[
                                                  0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                  0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[1] == 'Ուսանողի սեռ' or column_names[
                                            1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    1] == 'Ընդունման տարեթիվ' or
                                                column_names[1] == 'Առարկա' or column_names[
                                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[2] == 'Ուսանողի սեռ' or column_names[
                                            2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    2] == 'Ընդունման տարեթիվ' or
                                                column_names[2] == 'Առարկա' or column_names[
                                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[3] == 'Ուսանողի սեռ' or column_names[
                                            3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    3] == 'Ընդունման տարեթիվ' or
                                                column_names[3] == 'Առարկա' or column_names[
                                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[4] == 'Ուսանողի սեռ' or column_names[
                                            4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    4] == 'Ընդունման տարեթիվ' or
                                                column_names[4] == 'Առարկա' or column_names[
                                                    4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    4] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                column_names[5] == 'Ուսանողի սեռ' or column_names[
                                            5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    5] == 'Ընդունման տարեթիվ' or
                                                column_names[5] == 'Առարկա' or column_names[
                                                    5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    5] == 'Երկրորդ միջանկյալ ստուգում'):
                                            # data = pd.read_csv("CVS/Sx->/Sx6_C_V_YOE_Sbj_Fr_Ex_Sc_Ex.csv")
                                            data = pd.read_csv(file_path,
                                                               usecols=['Ուսանողի սեռ', 'Ծննդավայր (քաղաք/գյուղ)',
                                                                        'Ընդունման տարեթիվ',
                                                                        'Երկրորդ միջանկյալ ստուգում', 'Առարկա',
                                                                        'Առաջին միջանկյալ ստուգում'])
                                            # points = 1000
                                            start = 0
                                            end = 6
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])
                                        elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                            0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                              column_names[
                                                  0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                  0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                  0] == 'Ամփոփիչ քննություն') and (
                                                column_names[1] == 'Ուսանողի սեռ' or column_names[
                                            1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                column_names[
                                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    1] == 'Ամփոփիչ քննություն') and (
                                                column_names[2] == 'Ուսանողի սեռ' or column_names[
                                            2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                column_names[
                                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    2] == 'Ամփոփիչ քննություն') and (
                                                column_names[3] == 'Ուսանողի սեռ' or column_names[
                                            3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                column_names[
                                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    3] == 'Ամփոփիչ քննություն') and (
                                                column_names[4] == 'Ուսանողի սեռ' or column_names[
                                            4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                column_names[
                                                    4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    4] == 'Ամփոփիչ քննություն') and (
                                                column_names[5] == 'Ուսանողի սեռ' or column_names[
                                            5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                column_names[
                                                    5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    5] == 'Ամփոփիչ քննություն'):
                                            # data = pd.read_csv("CVS/Sx->/Sx6_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                            data = pd.read_csv(file_path,
                                                               usecols=['Ուսանողի սեռ', 'Ամփոփիչ քննություն',
                                                                        'Ընդունման տարեթիվ',
                                                                        'Երկրորդ միջանկյալ ստուգում',
                                                                        'Առարկա',
                                                                        'Առաջին միջանկյալ ստուգում'])
                                            # points = 1000
                                            start = 0
                                            end = 6
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])
                                        elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                            0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                              column_names[
                                                  0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                  0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                  0] == 'Ամփոփիչ քննություն') and (
                                                column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                            1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                column_names[
                                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    1] == 'Ամփոփիչ քննություն') and (
                                                column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                            2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                column_names[
                                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    2] == 'Ամփոփիչ քննություն') and (
                                                column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                            3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                column_names[
                                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    3] == 'Ամփոփիչ քննություն') and (
                                                column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                            4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                column_names[
                                                    4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    4] == 'Ամփոփիչ քննություն') and (
                                                column_names[5] == 'Ծննդավայր (երկիր)' or column_names[
                                            5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                column_names[
                                                    5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                    5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                    5] == 'Ամփոփիչ քննություն'):
                                            # data = pd.read_csv("CVS/COB->/COB5_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                            data = pd.read_csv(file_path,
                                                               usecols=['Ծննդավայր (երկիր)', 'Ընդունման տարեթիվ',
                                                                        'Առարկա', 'Առաջին միջանկյալ ստուգում',
                                                                        'Երկրորդ միջանկյալ ստուգում',
                                                                        'Ամփոփիչ քննություն'])
                                            # points = 1000
                                            start = 0
                                            end = 6
                                            for i in range(0, 1000):
                                                transactions.append(
                                                    [str(data.values[i, j]) for j in range(start, end)])

                                        def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png','txt')):
                                            """
                                            Get the latest image file in the given directory
                                            """

                                            # get filepaths of all files and dirs in the given dir
                                            valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                                            # filter out directories, no-extension, and wrong extension files
                                            valid_files = [f for f in valid_files if '.' in f and \
                                                f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                                            if not valid_files:
                                                raise ValueError("No valid images in %s" % dirpath)

                                            return max(valid_files, key=os.path.getmtime)                                                 

                                        print("------------------------")
                                        oht = TransactionEncoder()
                                        oht_ary = oht.fit(transactions).transform(transactions)
                                        # oht.columns_  # Need to understand is this need or not!!!!
                                        df_train = pd.DataFrame(oht_ary, columns=oht.columns_)
                                        rules = apriori(df_train, min_support=0.01, use_colnames=True)
                                        training_rules = association_rules(rules, metric="confidence",
                                                                           min_threshold=0.01)

                                        # Visualization of "Support" VS "Confidence" parameters on graph
                                        plt.figure(1)
                                        plt.scatter(training_rules['support'], training_rules['confidence'],
                                                    alpha=0.5)
                                        plt.xlabel('Support')
                                        plt.ylabel('Confidence')
                                        plt.title('Support vs Confidence')
                                        mngr = plt.get_current_fig_manager()
                                        mngr.window.setGeometry(20, 350, 600, 550)
                                        plt.savefig('images/apriori/' + datetime.now().strftime(
                                            '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                        apr_6_1_path=get_latest_image("images/apriori/",'png')          
                                        image_apr_6_1 = PhotoImage(file=apr_6_1_path)
                                        original_image_apr_6_1 = image_apr_6_1.subsample(3,3) # resize image using subsample

                                        apr_6_1_im_label = Label(apr_image_frame,image=original_image_apr_6_1)
                                        apr_6_1_im_label.image = original_image_apr_6_1 # keep a reference
                                        apr_6_1_im_label.place(x=387, y=118)                                          

                                        # Visualization of "Support" VS "Lift" parameters on graph
                                        plt.figure(2)
                                        plt.scatter(training_rules['support'], training_rules['lift'], alpha=0.5)
                                        plt.xlabel('Support')
                                        plt.ylabel('Lift')
                                        plt.title('Support vs Lift')
                                        mngr = plt.get_current_fig_manager()
                                        mngr.window.setGeometry(657, 350, 600, 550)
                                        plt.savefig('images/apriori/' + datetime.now().strftime(
                                            '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                        apr_6_2_path=get_latest_image("images/apriori/",'png')        
                                        image_apr_6_2 = PhotoImage(file=apr_6_2_path)
                                        original_image_apr_6_2 = image_apr_6_2.subsample(3,3) # resize image using subsample

                                        apr_6_2_im_label = Label(apr_image_frame,image=original_image_apr_6_2)
                                        apr_6_2_im_label.image = original_image_apr_6_2 # keep a reference
                                        apr_6_2_im_label.place(x=627, y=118)

                                        # Visualization of "Support" VS "Confidence" & "Lift" parameters on graph
                                        plt.figure(3)
                                        fit = np.polyfit(training_rules['lift'], training_rules['confidence'], 1)
                                        fit_fn = np.poly1d(fit)
                                        plt.plot(training_rules['lift'], training_rules['confidence'], 'yo',
                                                 training_rules['lift'], fit_fn(training_rules['lift']))
                                        plt.xlabel('lift')
                                        plt.ylabel('confidence')
                                        plt.title('lift vs confidence') 
                                        mngr = plt.get_current_fig_manager()
                                        mngr.window.setGeometry(1298, 350, 600, 550)
                                        plt.savefig('images/apriori/' + datetime.now().strftime(
                                            '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                        apr_6_3_path=get_latest_image("images/apriori/",'png')          
                                        image_apr_6_3 = PhotoImage(file=apr_6_3_path)
                                        original_image_apr_6_3 = image_apr_6_3.subsample(3,3) # resize image using subsample

                                        apr_6_3_im_label = Label(apr_image_frame,image=original_image_apr_6_3)
                                        apr_6_3_im_label.image = original_image_apr_6_3 # keep a reference
                                        apr_6_3_im_label.place(x=387, y=308)

                                        def mouse_on_apr_6_1(event):
                                            image_apr_6_1 = PhotoImage(file=apr_6_1_path)
                                            original_image_apr_6_1 = image_apr_6_1.subsample(2,2) # resize image using subsample

                                            apr_6_1_im_label = Label(apr_image_frame,image=original_image_apr_6_1)
                                            apr_6_1_im_label.image = original_image_apr_6_1 # keep a reference
                                            apr_6_1_im_label.place(x=387, y=118) 

                                            return          

                                        def mouse_on_apr_6_2(event):
                                            image_apr_6_2 = PhotoImage(file=apr_6_2_path)
                                            original_image_apr_6_2 = image_apr_6_2.subsample(2,2) # resize image using subsample

                                            apr_6_2_im_label = Label(apr_image_frame,image=original_image_apr_6_2)
                                            apr_6_2_im_label.image = original_image_apr_6_2 # keep a reference
                                            apr_6_2_im_label.place(x=627, y=118) 

                                            return        

                                        def mouse_on_apr_6_3(event):
                                            image_apr_6_3 = PhotoImage(file=apr_6_3_path)
                                            original_image_apr_6_3 = image_apr_6_3.subsample(2,2) # resize image using subsample

                                            apr_6_3_im_label = Label(apr_image_frame,image=original_image_apr_6_3)
                                            apr_6_3_im_label.image = original_image_apr_6_3 # keep a reference
                                            apr_6_3_im_label.place(x=387, y=308) 

                                            return                                                                

                                        apr_6_1_im_label.bind('<Enter>',mouse_on_apr_6_1)                    
                                        apr_6_2_im_label.bind('<Enter>',mouse_on_apr_6_2)  
                                        apr_6_3_im_label.bind('<Enter>',mouse_on_apr_6_3)                                                                                    

                                        # Taking backup values from above graphs and puting puting appropriate directory
                                        try:
                                            # Create target Directory
                                            os.mkdir(dir_name)
                                            print("Directory ", dir_name, " created.")
                                        except FileExistsError:
                                            print("Directory ", dir_name, " already exists.")
                                        file = open(abs_path, 'w', encoding="utf8")
                                        file.write(str(training_rules))
                                        file.close()

                                        now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                        now = str(now)
                                        newname = 'apriori_' + now + '.txt'
                                        os.rename('apriori.txt', newname)
                                        shutil.move(newname,  "images/apriori/")

                                        apr_6_txt_path=get_latest_image("images/apriori/",'txt')
                                        print(apr_6_txt_path)  

                                        def apr_6_btn_click():
                                            window.filename =  filedialog.askopenfile(mode='r',initialdir = "images/apriori/",title = apr_6_txt_path,filetypes = (("txt files","*.txt"),("all files","*.*")))

                                        apr_txt_entry=Entry(apr_txt_frame, highlightcolor='#ababba',justify=LEFT, relief=SUNKEN, width=18)
                                        apr_txt_entry.insert(END,apr_6_txt_path)
                                        apr_txt_entry.place(x=637, y=490)

                                        apr_txt_btn=Button(apr_txt_frame, text="Browse", bd=2, activebackground='#c7c7d1',relief=SUNKEN,command=apr_6_btn_click).place(x=786, y=486)                                         

                                        def rst_apr():
                                            print("Reset")
                                            cmb.set('')
                                            cmb1.set('')
                                            number_of_param.set('')                                             
                                            new_text = " "
                                            e1.delete(0, tk.END)
                                            e1.insert(0, new_text)
                                            cmb.place_forget()
                                            cmb1.place_forget()
                                            cmb2.place_forget()
                                            cmb3.place_forget()
                                            cmb4.place_forget()
                                            cmb5.place_forget()
                                            apr_6_1_im_label.image =''
                                            apr_6_2_im_label.image =''
                                            apr_6_3_im_label.image =''
                                            apr_txt_entry.delete(0, tk.END)      
                                            apr_txt_entry.insert(0, new_text)

                                        plt_rst_apr=PhotoImage(file="reset.png")  
                                        sub_plt_rst_apr=plt_rst_apr.subsample(4,4)

                                        button_apr_rst = Button(apr_input_frame, text="Reset", fg='#026084', command=rst_apr, image=sub_plt_rst_apr, compound=LEFT, width=130)
                                        button_apr_rst.image=sub_plt_rst_apr
                                        button_apr_rst.place(x=88, y=407)
                                        button_arr.append(button_apr_rst)

                                        ttk.Separator(apr_input_frame).place(x=75, y=487, relwidth=0.29)                            

                                        def jnt_go_to_menu():

                                            print("Coming soon")
  
                                            apr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                            #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                            lbl_apr=Label(apr_frame, width=20, bg='white').place(x=10, y=10)
   
                                            apr_inner_frame=Frame(apr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                            #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                            apr_input_frame=Frame(apr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                            apr_image_frame=Frame(apr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                            Label(apr_image_frame,bg='white').place(x=565, y=95)

                                            apr_txt_frame=Frame(apr_image_frame, width=250, height=195, bg='white', highlightbackground='white').place(x=627,y=388)

                                            lbl_apr_txt=Label(apr_txt_frame, width=17, bg='white').place(x=630, y=392)                            

                                            print("Apriori frame has been destroyed.")      

                                        plt_up=PhotoImage(file="up.png")  
                                        sub_plt_up=plt_up.subsample(4,4)     

                                        button_jnt_go_to_menu=Button(apr_input_frame, text="Go to menu", fg='#026084', command=jnt_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                        button_jnt_go_to_menu.image=sub_plt_up
                                        button_jnt_go_to_menu.place(x=88, y=501)
                                        button_arr.append(button_jnt_go_to_menu)                            

                                    # Creating a photoimage object to use image 
                                    plt_gen_apr = PhotoImage(file = "images.png") 
                                    sub_plt_gen_apr = plt_gen_apr.subsample(4, 4)    

                                    button_apr_gen = Button(apr_input_frame, text="Generate", fg='#026084', command=apr_gen, image=sub_plt_gen_apr, compound=LEFT)
                                    button_apr_gen.image=sub_plt_gen_apr
                                    button_apr_gen.place(x=88, y=337)
                                    button_arr.append(button_apr_gen)

                                    ttk.Separator(apr_input_frame).place(x=75, y=327, relwidth=0.29)                                    

                                cmb5 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                cmb5.place(x=75, y=296)
                                cmb5.bind('<<ComboboxSelected>>', on_sixth_select)

                            cmb4 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        elif (e1.get() == "7" or e1.get() == " 7"):
            print("else 7")

            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):
                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                sixth_data = fifth_data

                                for item in fifth_data:
                                    if item == fifth_curr_val:
                                        sixth_data.remove(item)

                                def on_sixth_select(event=None):
                                    sixth_curr_val = cmb5.get()

                                    if len(column_names) > 5:
                                        column_names.pop(5)

                                    column_names.append(sixth_curr_val)

                                    seventh_data = sixth_data

                                    for item in sixth_data:
                                        if item == sixth_curr_val:
                                            seventh_data.remove(item)

                                    def on_seventh_select(event=None):
                                        seventh_curr_val = cmb6.get()

                                        if len(column_names) > 6:
                                            column_names.pop(6)

                                        column_names.append(seventh_curr_val)

                                        def apr_gen():

                                            print("Apr Generation")

                                            apriori_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն',
                                                                       'Ուսանողի սեռ',
                                                                       'Ծննդավայր (երկիր)',
                                                                       'Ծննդավայր (քաղաք/գյուղ)',
                                                                       'Ընդունման տարեթիվ', 'Առարկա',
                                                                       'Առաջին միջանկյալ ստուգում',
                                                                       'Երկրորդ միջանկյալ ստուգում',
                                                                       'Ամփոփիչ քննություն']
                                            # Intilizing global vaiables
                                            transactions = []

                                            # DB file name for Apriori algorithm
                                            folder_name = ['apriori']
                                            txt_file_name = ['apriori.txt']

                                            # Getting dynamically path for appropriate DB file and backup directory
                                            absolute_path = sys.path[0]

                                            file_path = sys.path[0] + '/' + db

                                            #dir_name = absolute_path + '\\' + folder_name[0]
                                            #abs_path = dir_name + '\\' + txt_file_name[0]

                                            f_path = pathlib.Path(__file__).parent.absolute()
                                            f_path = str(f_path)
                                            dir_name = f_path + '/' + 'images' + '/' + folder_name[0]
                                            abs_path = f_path + '/' + txt_file_name[0]                                            

                                            # Setting pandas library options
                                            pd.set_option('display.max_columns', None)
                                            pd.set_option('display.max_rows', None)

                                            if not find_plathform():
                                                file_path = file_path.replace("\\", "/")
                                            data = pd.read_csv(file_path)

                                            if (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                0] == 'Ուսանողի անուն' or
                                                column_names[0] == 'Ուսանողի սեռ' or column_names[
                                                    0] == 'Ծննդավայր (երկիր)' or column_names[
                                                    0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա') and (
                                                    column_names[1] == 'Ֆակուլտետ' or column_names[
                                                1] == 'Ուսանողի անուն' or column_names[1] == 'Ուսանողի սեռ' or
                                                    column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[
                                                        1] == 'Առարկա') and (
                                                    column_names[2] == 'Ֆակուլտետ' or column_names[
                                                2] == 'Ուսանողի անուն' or column_names[2] == 'Ուսանողի սեռ' or
                                                    column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[
                                                        2] == 'Առարկա') and (
                                                    column_names[3] == 'Ֆակուլտետ' or column_names[
                                                3] == 'Ուսանողի անուն' or column_names[3] == 'Ուսանողի սեռ' or
                                                    column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[
                                                        3] == 'Առարկա') and (
                                                    column_names[4] == 'Ֆակուլտետ' or column_names[
                                                4] == 'Ուսանողի անուն' or column_names[4] == 'Ուսանողի սեռ' or
                                                    column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[
                                                        4] == 'Առարկա') and (
                                                    column_names[5] == 'Ֆակուլտետ' or column_names[
                                                5] == 'Ուսանողի անուն' or column_names[5] == 'Ուսանողի սեռ' or
                                                    column_names[5] == 'Ծննդավայր (երկիր)' or column_names[
                                                        5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[
                                                        5] == 'Առարկա') and (
                                                    column_names[6] == 'Ֆակուլտետ' or column_names[
                                                6] == 'Ուսանողի անուն' or column_names[6] == 'Ուսանողի սեռ' or
                                                    column_names[6] == 'Ծննդավայր (երկիր)' or column_names[
                                                        6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա'):
                                                # data = pd.read_csv("CVS/Fac->/Fac_Nm_Sx_COB.csv")
                                                # points = 1000
                                                start = 0
                                                end = 7
                                                for i in range(0, 1000):
                                                    transactions.append(
                                                        [str(data.values[i, j]) for j in range(start, end)])
                                            elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                                0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                      0] == 'Ամփոփիչ քննություն') and (
                                                    column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        1] == 'Ամփոփիչ քննություն') and (
                                                    column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        2] == 'Ամփոփիչ քննություն') and (
                                                    column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        3] == 'Ամփոփիչ քննություն') and (
                                                    column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        4] == 'Ամփոփիչ քննություն') and (
                                                    column_names[5] == 'Ծննդավայր (երկիր)' or column_names[
                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        5] == 'Ամփոփիչ քննություն') and (
                                                    column_names[6] == 'Ծննդավայր (երկիր)' or column_names[
                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        6] == 'Ամփոփիչ քննություն'):
                                                # data = pd.read_csv("CVS/Fac->/Fac_Nm_Sx_COB.csv")
                                                # points = 1000
                                                start = 3
                                                end = 10
                                                for i in range(0, 1000):
                                                    transactions.append(
                                                        [str(data.values[i, j]) for j in range(start, end)])
                                            elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                0] == 'Ուսանողի սեռ' or
                                                  column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                                      0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[1] == 'Ֆակուլտետ' or column_names[
                                                1] == 'Ուսանողի սեռ' or column_names[1] == 'Ծննդավայր (երկիր)' or
                                                    column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[2] == 'Ֆակուլտետ' or column_names[
                                                2] == 'Ուսանողի սեռ' or column_names[2] == 'Ծննդավայր (երկիր)' or
                                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[3] == 'Ֆակուլտետ' or column_names[
                                                3] == 'Ուսանողի սեռ' or column_names[3] == 'Ծննդավայր (երկիր)' or
                                                    column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[4] == 'Ֆակուլտետ' or column_names[
                                                4] == 'Ուսանողի սեռ' or column_names[4] == 'Ծննդավայր (երկիր)' or
                                                    column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[5] == 'Ֆակուլտետ' or column_names[
                                                5] == 'Ուսանողի սեռ' or column_names[5] == 'Ծննդավայր (երկիր)' or
                                                    column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[6] == 'Ֆակուլտետ' or column_names[
                                                6] == 'Ուսանողի սեռ' or column_names[6] == 'Ծննդավայր (երկիր)' or
                                                    column_names[6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում'):
                                                # data = pd.read_csv("CVS/Fac->/Fac7_Sx_COB_CV_YOE_Sbj_Fr_Ex.csv")
                                                data = pd.read_csv(file_path, usecols=['Ֆակուլտետ', 'Ուսանողի սեռ',
                                                                                       'Ծննդավայր (երկիր)',
                                                                                       'Ծննդավայր (քաղաք/գյուղ)',
                                                                                       'Ընդունման տարեթիվ',
                                                                                       'Առարկա',
                                                                                       'Առաջին միջանկյալ ստուգում'])
                                                # points = 1000
                                                start = 0
                                                end = 7
                                                for i in range(0, 1000):
                                                    transactions.append(
                                                        [str(data.values[i, j]) for j in range(start, end)])
                                            elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                0] == 'Ծննդավայր (երկիր)' or column_names[
                                                      0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[1] == 'Ֆակուլտետ' or column_names[
                                                1] == 'Ծննդավայր (երկիր)' or column_names[
                                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[2] == 'Ֆակուլտետ' or column_names[
                                                2] == 'Ծննդավայր (երկիր)' or column_names[
                                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[3] == 'Ֆակուլտետ' or column_names[
                                                3] == 'Ծննդավայր (երկիր)' or column_names[
                                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[4] == 'Ֆակուլտետ' or column_names[
                                                4] == 'Ծննդավայր (երկիր)' or column_names[
                                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[5] == 'Ֆակուլտետ' or column_names[
                                                5] == 'Ծննդավայր (երկիր)' or column_names[
                                                        5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[6] == 'Ֆակուլտետ' or column_names[
                                                6] == 'Ծննդավայր (երկիր)' or column_names[
                                                        6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում'):
                                                # data = pd.read_csv("CVS/Fac->/Fac7_COB_CV_YOE_Sbj_Fr_Ex_Sc_Ex.csv")
                                                data = pd.read_csv(file_path,
                                                                   usecols=['Ֆակուլտետ',
                                                                            'Երկրորդ միջանկյալ ստուգում',
                                                                            'Ծննդավայր (երկիր)',
                                                                            'Ծննդավայր (քաղաք/գյուղ)',
                                                                            'Ընդունման տարեթիվ', 'Առարկա',
                                                                            'Առաջին միջանկյալ ստուգում'])
                                                # points = 1000
                                                start = 0
                                                end = 7
                                                for i in range(0, 1000):
                                                    transactions.append(
                                                        [str(data.values[i, j]) for j in range(start, end)])
                                            elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                      0] == 'Ամփոփիչ քննություն') and (
                                                    column_names[1] == 'Ֆակուլտետ' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        1] == 'Ամփոփիչ քննություն') and (
                                                    column_names[2] == 'Ֆակուլտետ' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        2] == 'Ամփոփիչ քննություն') and (
                                                    column_names[3] == 'Ֆակուլտետ' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        3] == 'Ամփոփիչ քննություն') and (
                                                    column_names[4] == 'Ֆակուլտետ' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        4] == 'Ամփոփիչ քննություն') and (
                                                    column_names[5] == 'Ֆակուլտետ' or column_names[
                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        5] == 'Ամփոփիչ քննություն') and (
                                                    column_names[6] == 'Ֆակուլտետ' or column_names[
                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        6] == 'Ամփոփիչ քննություն'):
                                                # data = pd.read_csv("CVS/Fac->/Fac7_CV_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                                data = pd.read_csv(file_path,
                                                                   usecols=['Ֆակուլտետ',
                                                                            'Երկրորդ միջանկյալ ստուգում',
                                                                            'Ամփոփիչ քննություն',
                                                                            'Ծննդավայր (քաղաք/գյուղ)',
                                                                            'Ընդունման տարեթիվ', 'Առարկա',
                                                                            'Առաջին միջանկյալ ստուգում'])
                                                # points = 1000
                                                start = 0
                                                end = 7
                                                for i in range(0, 1000):
                                                    transactions.append(
                                                        [str(data.values[i, j]) for j in range(start, end)])
                                            elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                                0] == 'Ծննդավայր (երկիր)' or column_names[
                                                      0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[1] == 'Ուսանողի անուն' or column_names[
                                                1] == 'Ծննդավայր (երկիր)' or column_names[
                                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[2] == 'Ուսանողի անուն' or column_names[
                                                2] == 'Ծննդավայր (երկիր)' or column_names[
                                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[3] == 'Ուսանողի անուն' or column_names[
                                                3] == 'Ծննդավայր (երկիր)' or column_names[
                                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[4] == 'Ուսանողի անուն' or column_names[
                                                4] == 'Ծննդավայր (երկիր)' or column_names[
                                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[5] == 'Ուսանողի անուն' or column_names[
                                                5] == 'Ծննդավայր (երկիր)' or column_names[
                                                        5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[6] == 'Ուսանողի անուն' or column_names[
                                                6] == 'Ծննդավայր (երկիր)' or column_names[
                                                        6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում'):
                                                # data = pd.read_csv("CVS/Nam->/Name7_COB_CV_YOE_Sbj_Fr_Ex_Sc_Ex.csv")
                                                data = pd.read_csv(file_path, usecols=['Ուսանողի անուն',
                                                                                       'Երկրորդ միջանկյալ ստուգում',
                                                                                       'Ծննդավայր (երկիր)',
                                                                                       'Ծննդավայր (քաղաք/գյուղ)',
                                                                                       'Ընդունման տարեթիվ',
                                                                                       'Առարկա',
                                                                                       'Առաջին միջանկյալ ստուգում'])
                                                # points = 1000
                                                start = 0
                                                end = 7
                                                for i in range(0, 1000):
                                                    transactions.append(
                                                        [str(data.values[i, j]) for j in range(start, end)])
                                            elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                                0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                      0] == 'Ամփոփիչ քննություն') and (
                                                    column_names[1] == 'Ուսանողի անուն' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        1] == 'Ամփոփիչ քննություն') and (
                                                    column_names[2] == 'Ուսանողի անուն' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        2] == 'Ամփոփիչ քննություն') and (
                                                    column_names[3] == 'Ուսանողի անուն' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        3] == 'Ամփոփիչ քննություն') and (
                                                    column_names[4] == 'Ուսանողի անուն' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        4] == 'Ամփոփիչ քննություն') and (
                                                    column_names[5] == 'Ուսանողի անուն' or column_names[
                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        5] == 'Ամփոփիչ քննություն') and (
                                                    column_names[6] == 'Ուսանողի անուն' or column_names[
                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        6] == 'Ամփոփիչ քննություն'):
                                                # data = pd.read_csv("CVS/Nam->/Name7_CV_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                                data = pd.read_csv(file_path, usecols=['Ուսանողի անուն',
                                                                                       'Երկրորդ միջանկյալ ստուգում',
                                                                                       'Ամփոփիչ քննություն',
                                                                                       'Ծննդավայր (քաղաք/գյուղ)',
                                                                                       'Ընդունման տարեթիվ',
                                                                                       'Առարկա',
                                                                                       'Առաջին միջանկյալ ստուգում'])
                                                # points = 1000
                                                start = 0
                                                end = 7
                                                for i in range(0, 1000):
                                                    transactions.append(
                                                        [str(data.values[i, j]) for j in range(start, end)])
                                            elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                                0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                      0] == 'Ամփոփիչ քննություն') and (
                                                    column_names[1] == 'Ուսանողի սեռ' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        1] == 'Ամփոփիչ քննություն') and (
                                                    column_names[2] == 'Ուսանողի սեռ' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        2] == 'Ամփոփիչ քննություն') and (
                                                    column_names[3] == 'Ուսանողի սեռ' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        3] == 'Ամփոփիչ քննություն') and (
                                                    column_names[4] == 'Ուսանողի սեռ' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        4] == 'Ամփոփիչ քննություն') and (
                                                    column_names[5] == 'Ուսանողի սեռ' or column_names[
                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        5] == 'Ամփոփիչ քննություն') and (
                                                    column_names[6] == 'Ուսանողի սեռ' or column_names[
                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        6] == 'Ամփոփիչ քննություն'):
                                                # data = pd.read_csv("CVS/Sx->/Sx7_C_V_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                                data = pd.read_csv(file_path, usecols=['Ուսանողի սեռ',
                                                                                       'Երկրորդ միջանկյալ ստուգում',
                                                                                       'Ամփոփիչ քննություն',
                                                                                       'Ծննդավայր (քաղաք/գյուղ)',
                                                                                       'Ընդունման տարեթիվ',
                                                                                       'Առարկա',
                                                                                       'Առաջին միջանկյալ ստուգում'])
                                                # points = 1000
                                                start = 0
                                                end = 7
                                                for i in range(0, 1000):
                                                    transactions.append(
                                                        [str(data.values[i, j]) for j in range(start, end)])

                                            def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png','txt')):
                                                """
                                                Get the latest image file in the given directory
                                                """

                                                # get filepaths of all files and dirs in the given dir
                                                valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                                                # filter out directories, no-extension, and wrong extension files
                                                valid_files = [f for f in valid_files if '.' in f and \
                                                    f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                                                if not valid_files:
                                                    raise ValueError("No valid images in %s" % dirpath)

                                                return max(valid_files, key=os.path.getmtime)                                                      

                                            print("------------------------")
                                            oht = TransactionEncoder()
                                            oht_ary = oht.fit(transactions).transform(transactions)
                                            # oht.columns_  # Need to understand is this need or not!!!!
                                            df_train = pd.DataFrame(oht_ary, columns=oht.columns_)
                                            rules = apriori(df_train, min_support=0.01, use_colnames=True)
                                            training_rules = association_rules(rules, metric="confidence",
                                                                               min_threshold=0.01)

                                            # Visualization of "Support" VS "Confidence" parameters on graph
                                            plt.figure(1)
                                            plt.scatter(training_rules['support'], training_rules['confidence'],
                                                        alpha=0.5)
                                            plt.xlabel('Support')
                                            plt.ylabel('Confidence')
                                            plt.title('Support vs Confidence')
                                            mngr = plt.get_current_fig_manager()
                                            mngr.window.setGeometry(20, 350, 600, 550)
                                            plt.savefig('images/apriori/' + datetime.now().strftime(
                                                '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                            apr_7_1_path=get_latest_image("images/apriori/",'png')          
                                            image_apr_7_1 = PhotoImage(file=apr_7_1_path)
                                            original_image_apr_7_1 = image_apr_7_1.subsample(3,3) # resize image using subsample

                                            apr_7_1_im_label = Label(apr_image_frame,image=original_image_apr_7_1)
                                            apr_7_1_im_label.image = original_image_apr_7_1 # keep a reference
                                            apr_7_1_im_label.place(x=387, y=118)                                            

                                            # Visualization of "Support" VS "Lift" parameters on graph
                                            plt.figure(2)
                                            plt.scatter(training_rules['support'], training_rules['lift'],
                                                        alpha=0.5)
                                            plt.xlabel('Support')
                                            plt.ylabel('Lift')
                                            plt.title('Support vs Lift')
                                            mngr = plt.get_current_fig_manager()
                                            mngr.window.setGeometry(657, 350, 600, 550)
                                            plt.savefig('images/apriori/' + datetime.now().strftime(
                                                '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                            apr_7_2_path=get_latest_image("images/apriori/",'png')        
                                            image_apr_7_2 = PhotoImage(file=apr_7_2_path)
                                            original_image_apr_7_2 = image_apr_7_2.subsample(3,3) # resize image using subsample

                                            apr_7_2_im_label = Label(apr_image_frame,image=original_image_apr_7_2)
                                            apr_7_2_im_label.image = original_image_apr_7_2 # keep a reference
                                            apr_7_2_im_label.place(x=627, y=118)                                            

                                            # Visualization of "Support" VS "Confidence" & "Lift" parameters on graph
                                            plt.figure(3)
                                            fit = np.polyfit(training_rules['lift'], training_rules['confidence'],
                                                             1)
                                            fit_fn = np.poly1d(fit)
                                            plt.plot(training_rules['lift'], training_rules['confidence'], 'yo',
                                                     training_rules['lift'], fit_fn(training_rules['lift']))
                                            plt.xlabel('lift')
                                            plt.ylabel('confidence')
                                            plt.title('lift vs confidence')                                             
                                            mngr = plt.get_current_fig_manager()
                                            mngr.window.setGeometry(1298, 350, 600, 550)
                                            plt.savefig('images/apriori/' + datetime.now().strftime(
                                                '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                            apr_7_3_path=get_latest_image("images/apriori/",'png')          
                                            image_apr_7_3 = PhotoImage(file=apr_7_3_path)
                                            original_image_apr_7_3 = image_apr_7_3.subsample(3,3) # resize image using subsample

                                            apr_7_3_im_label = Label(apr_image_frame,image=original_image_apr_7_3)
                                            apr_7_3_im_label.image = original_image_apr_7_3 # keep a reference
                                            apr_7_3_im_label.place(x=387, y=308)

                                            def mouse_on_apr_7_1(event):
                                                image_apr_7_1 = PhotoImage(file=apr_7_1_path)
                                                original_image_apr_7_1 = image_apr_7_1.subsample(2,2) # resize image using subsample

                                                apr_7_1_im_label = Label(apr_image_frame,image=original_image_apr_7_1)
                                                apr_7_1_im_label.image = original_image_apr_7_1 # keep a reference
                                                apr_7_1_im_label.place(x=387, y=118) 

                                                return          

                                            def mouse_on_apr_7_2(event):
                                                image_apr_7_2 = PhotoImage(file=apr_7_2_path)
                                                original_image_apr_7_2 = image_apr_7_2.subsample(2,2) # resize image using subsample

                                                apr_7_2_im_label = Label(apr_image_frame,image=original_image_apr_7_2)
                                                apr_7_2_im_label.image = original_image_apr_7_2 # keep a reference
                                                apr_7_2_im_label.place(x=627, y=118) 

                                                return        

                                            def mouse_on_apr_7_3(event):
                                                image_apr_7_3 = PhotoImage(file=apr_7_3_path)
                                                original_image_apr_7_3 = image_apr_7_3.subsample(2,2) # resize image using subsample

                                                apr_7_3_im_label = Label(apr_image_frame,image=original_image_apr_7_3)
                                                apr_7_3_im_label.image = original_image_apr_7_3 # keep a reference
                                                apr_7_3_im_label.place(x=387, y=308) 

                                                return                                                                

                                            apr_7_1_im_label.bind('<Enter>',mouse_on_apr_7_1)                    
                                            apr_7_2_im_label.bind('<Enter>',mouse_on_apr_7_2)  
                                            apr_7_3_im_label.bind('<Enter>',mouse_on_apr_7_3)                                             

                                            # Taking backup values from above graphs and puting puting appropriate directory
                                            try:
                                                # Create target Directory
                                                os.mkdir(dir_name)
                                                print("Directory ", dir_name, " created.")
                                            except FileExistsError:
                                                print("Directory ", dir_name, " already exists.")
                                            file = open(abs_path, 'w', encoding="utf8")
                                            file.write(str(training_rules))
                                            file.close()

                                            now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                            now = str(now)
                                            newname = 'apriori_' + now + '.txt'
                                            os.rename('apriori.txt', newname)
                                            shutil.move(newname,  "images/apriori/")

                                            apr_7_txt_path=get_latest_image("images/apriori/",'txt')
                                            print(apr_7_txt_path)  

                                            def apr_7_btn_click():
                                                window.filename =  filedialog.askopenfile(mode='r',initialdir = "images/apriori/",title = apr_7_txt_path,filetypes = (("txt files","*.txt"),("all files","*.*")))

                                            apr_txt_entry=Entry(apr_txt_frame, highlightcolor='#ababba',justify=LEFT, relief=SUNKEN, width=18)
                                            apr_txt_entry.insert(END,apr_7_txt_path)
                                            apr_txt_entry.place(x=637, y=490)

                                            apr_txt_btn=Button(apr_txt_frame, text="Browse", bd=2, activebackground='#c7c7d1',relief=SUNKEN,command=apr_7_btn_click).place(x=786, y=486)                                             

                                            def rst_apr():
                                                print("Reset")
                                                cmb.set('')
                                                cmb1.set('')
                                                number_of_param.set('')                                                  
                                                new_text = " "
                                                e1.delete(0, tk.END)
                                                e1.insert(0, new_text)
                                                cmb.place_forget()
                                                cmb1.place_forget()
                                                cmb2.place_forget()
                                                cmb3.place_forget()
                                                cmb4.place_forget()
                                                cmb5.place_forget()
                                                cmb6.place_forget()
                                                apr_7_1_im_label.image =''
                                                apr_7_2_im_label.image =''
                                                apr_7_3_im_label.image =''
                                                apr_txt_entry.delete(0, tk.END)      
                                                apr_txt_entry.insert(0, new_text)

                                            plt_rst_apr=PhotoImage(file="reset.png")  
                                            sub_plt_rst_apr=plt_rst_apr.subsample(4,4)

                                            button_apr_rst = Button(apr_input_frame, text="Reset", fg='#026084', command=rst_apr, image=sub_plt_rst_apr, compound=LEFT, width=130)
                                            button_apr_rst.image=sub_plt_rst_apr
                                            button_apr_rst.place(x=88, y=430)
                                            button_arr.append(button_apr_rst)

                                            ttk.Separator(apr_input_frame).place(x=75, y=510, relwidth=0.29)                            

                                            def jnt_go_to_menu():

                                                print("Coming soon")
  
                                                apr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                                #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                                lbl_apr=Label(apr_frame, width=20, bg='white').place(x=10, y=10)
   
                                                apr_inner_frame=Frame(apr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                                #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                                apr_input_frame=Frame(apr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                                apr_image_frame=Frame(apr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                                Label(apr_image_frame,bg='white').place(x=565, y=95)

                                                apr_txt_frame=Frame(apr_image_frame, width=250, height=195, bg='white', highlightbackground='white').place(x=627,y=388)

                                                lbl_apr_txt=Label(apr_txt_frame, width=17, bg='white').place(x=630, y=392)                            

                                                print("Apriori frame has been destroyed.")      

                                            plt_up=PhotoImage(file="up.png")  
                                            sub_plt_up=plt_up.subsample(5,5)     

                                            button_jnt_go_to_menu=Button(apr_input_frame, text="Go to menu", fg='#026084', command=jnt_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                            button_jnt_go_to_menu.image=sub_plt_up
                                            button_jnt_go_to_menu.place(x=88, y=512)
                                            button_arr.append(button_jnt_go_to_menu)  

                                        # Creating a photoimage object to use image 
                                        plt_gen_apr = PhotoImage(file = "images.png") 
                                        sub_plt_gen_apr = plt_gen_apr.subsample(4, 4)    

                                        button_apr_gen = Button(apr_input_frame, text="Generate", fg='#026084', command=apr_gen, image=sub_plt_gen_apr, compound=LEFT)
                                        button_apr_gen.image=sub_plt_gen_apr
                                        button_apr_gen.place(x=88, y=360)
                                        button_arr.append(button_apr_gen)

                                        ttk.Separator(apr_input_frame).place(x=75, y=350, relwidth=0.29)                                                                            

                                    cmb6 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                    cmb6.place(x=75, y=319)
                                    cmb6.bind('<<ComboboxSelected>>', on_seventh_select)

                                cmb5 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                cmb5.place(x=75, y=296)
                                cmb5.bind('<<ComboboxSelected>>', on_sixth_select)

                            cmb4 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        elif (e1.get() == "8" or e1.get() == " 8"):
            print("else 8")

            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):
                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                sixth_data = fifth_data

                                for item in fifth_data:
                                    if item == fifth_curr_val:
                                        sixth_data.remove(item)

                                def on_sixth_select(event=None):
                                    sixth_curr_val = cmb5.get()

                                    if len(column_names) > 5:
                                        column_names.pop(5)

                                    column_names.append(sixth_curr_val)

                                    seventh_data = sixth_data

                                    for item in sixth_data:
                                        if item == sixth_curr_val:
                                            seventh_data.remove(item)

                                    def on_seventh_select(event=None):
                                        seventh_curr_val = cmb6.get()

                                        if len(column_names) > 6:
                                            column_names.pop(6)

                                        column_names.append(seventh_curr_val)

                                        eight_data = seventh_data

                                        for item in seventh_data:
                                            if item == seventh_curr_val:
                                                eight_data.remove(item)

                                        def on_eight_select(event=None):
                                            eight_curr_val = cmb7.get()

                                            if len(column_names) > 7:
                                                column_names.pop(7)

                                            column_names.append(eight_curr_val)

                                            def apr_gen():

                                                print("Apr Generation")

                                                apriori_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն',
                                                                           'Ուսանողի սեռ', 'Ծննդավայր (երկիր)',
                                                                           'Ծննդավայր (քաղաք/գյուղ)',
                                                                           'Ընդունման տարեթիվ', 'Առարկա',
                                                                           'Առաջին միջանկյալ ստուգում',
                                                                           'Երկրորդ միջանկյալ ստուգում',
                                                                           'Ամփոփիչ քննություն']

                                                # Intilizing global vaiables
                                                transactions = []

                                                # DB file name for Apriori algorithm
                                                folder_name = ['apriori']

                                                txt_file_name = ['apriori.txt']

                                                # Getting dynamically path for appropriate DB file and backup directory
                                                absolute_path = sys.path[0]

                                                file_path = sys.path[0] + '/' + db

                                                #dir_name = absolute_path + '\\' + folder_name[0]
                                                #abs_path = dir_name + '\\' + txt_file_name[0]

                                                f_path = pathlib.Path(__file__).parent.absolute()
                                                f_path = str(f_path)
                                                dir_name = f_path + '/' + 'images' + '/' + folder_name[0]
                                                abs_path = f_path + '/' + txt_file_name[0]                                                 

                                                # Setting pandas library options
                                                pd.set_option('display.max_columns', None)
                                                pd.set_option('display.max_rows', None)

                                                if not find_plathform():
                                                    file_path = file_path.replace("\\", "/")
                                                data = pd.read_csv(file_path)

                                                if (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                    0] == 'Ուսանողի անուն' or column_names[0] == 'Ուսանողի սեռ' or
                                                    column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                                        0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                    column_names[0] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[1] == 'Ֆակուլտետ' or column_names[
                                                    1] == 'Ուսանողի անուն' or column_names[1] == 'Ուսանողի սեռ' or
                                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                                            1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            1] == 'Ընդունման տարեթիվ' or column_names[
                                                            1] == 'Առարկա' or
                                                        column_names[1] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[2] == 'Ֆակուլտետ' or column_names[
                                                    2] == 'Ուսանողի անուն' or column_names[2] == 'Ուսանողի սեռ' or
                                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                                            2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            2] == 'Ընդունման տարեթիվ' or column_names[
                                                            2] == 'Առարկա' or
                                                        column_names[2] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[3] == 'Ֆակուլտետ' or column_names[
                                                    3] == 'Ուսանողի անուն' or column_names[3] == 'Ուսանողի սեռ' or
                                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                                            3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            3] == 'Ընդունման տարեթիվ' or column_names[
                                                            3] == 'Առարկա' or
                                                        column_names[3] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[4] == 'Ֆակուլտետ' or column_names[
                                                    4] == 'Ուսանողի անուն' or column_names[4] == 'Ուսանողի սեռ' or
                                                        column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                                            4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            4] == 'Ընդունման տարեթիվ' or column_names[
                                                            4] == 'Առարկա' or
                                                        column_names[4] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[5] == 'Ֆակուլտետ' or column_names[
                                                    5] == 'Ուսանողի անուն' or column_names[5] == 'Ուսանողի սեռ' or
                                                        column_names[5] == 'Ծննդավայր (երկիր)' or column_names[
                                                            5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            5] == 'Ընդունման տարեթիվ' or column_names[
                                                            5] == 'Առարկա' or
                                                        column_names[5] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[6] == 'Ֆակուլտետ' or column_names[
                                                    6] == 'Ուսանողի անուն' or column_names[6] == 'Ուսանողի սեռ' or
                                                        column_names[6] == 'Ծննդավայր (երկիր)' or column_names[
                                                            6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            6] == 'Ընդունման տարեթիվ' or column_names[
                                                            6] == 'Առարկա' or
                                                        column_names[6] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[7] == 'Ֆակուլտետ' or column_names[
                                                    7] == 'Ուսանողի անուն' or column_names[7] == 'Ուսանողի սեռ' or
                                                        column_names[7] == 'Ծննդավայր (երկիր)' or column_names[
                                                            7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            7] == 'Ընդունման տարեթիվ' or column_names[
                                                            7] == 'Առարկա' or
                                                        column_names[7] == 'Առաջին միջանկյալ ստուգում'):
                                                    # data = pd.read_csv("CVS/Sx->/Sx7_C_V_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                                    # points = 1000
                                                    start = 0
                                                    end = 8
                                                    for i in range(0, 1000):
                                                        transactions.append(
                                                            [str(data.values[i, j]) for j in range(start, end)])
                                                elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                                    0] == 'Ծննդավայր (երկիր)' or column_names[
                                                          0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                          0] == 'Ընդունման տարեթիվ' or column_names[
                                                          0] == 'Առարկա' or
                                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or
                                                      column_names[
                                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                          0] == 'Ամփոփիչ քննություն') and (
                                                        column_names[1] == 'Ուսանողի սեռ' or column_names[
                                                    1] == 'Ծննդավայր (երկիր)' or column_names[
                                                            1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            1] == 'Ընդունման տարեթիվ' or column_names[
                                                            1] == 'Առարկա' or
                                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            1] == 'Ամփոփիչ քննություն') and (
                                                        column_names[2] == 'Ուսանողի սեռ' or column_names[
                                                    2] == 'Ծննդավայր (երկիր)' or column_names[
                                                            2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            2] == 'Ընդունման տարեթիվ' or column_names[
                                                            2] == 'Առարկա' or
                                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            2] == 'Ամփոփիչ քննություն') and (
                                                        column_names[3] == 'Ուսանողի սեռ' or column_names[
                                                    3] == 'Ծննդավայր (երկիր)' or column_names[
                                                            3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            3] == 'Ընդունման տարեթիվ' or column_names[
                                                            3] == 'Առարկա' or
                                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            3] == 'Ամփոփիչ քննություն') and (
                                                        column_names[4] == 'Ուսանողի սեռ' or column_names[
                                                    4] == 'Ծննդավայր (երկիր)' or column_names[
                                                            4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            4] == 'Ընդունման տարեթիվ' or column_names[
                                                            4] == 'Առարկա' or
                                                        column_names[4] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            4] == 'Ամփոփիչ քննություն') and (
                                                        column_names[5] == 'Ուսանողի սեռ' or column_names[
                                                    5] == 'Ծննդավայր (երկիր)' or column_names[
                                                            5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            5] == 'Ընդունման տարեթիվ' or column_names[
                                                            5] == 'Առարկա' or
                                                        column_names[5] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            5] == 'Ամփոփիչ քննություն') and (
                                                        column_names[6] == 'Ուսանողի սեռ' or column_names[
                                                    6] == 'Ծննդավայր (երկիր)' or column_names[
                                                            6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            6] == 'Ընդունման տարեթիվ' or column_names[
                                                            6] == 'Առարկա' or
                                                        column_names[6] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            6] == 'Ամփոփիչ քննություն') and (
                                                        column_names[7] == 'Ուսանողի սեռ' or column_names[
                                                    7] == 'Ծննդավայր (երկիր)' or column_names[
                                                            7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            7] == 'Ընդունման տարեթիվ' or column_names[
                                                            7] == 'Առարկա' or
                                                        column_names[7] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            7] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            7] == 'Ամփոփիչ քննություն'):
                                                    # data = pd.read_csv("CVS/Sx->/Sx7_C_V_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                                    # points = 1000
                                                    start = 2
                                                    end = 10
                                                    for i in range(0, 1000):
                                                        transactions.append(
                                                            [str(data.values[i, j]) for j in range(start, end)])
                                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                    0] == 'Ուսանողի սեռ' or column_names[
                                                          0] == 'Ծննդավայր (երկիր)' or
                                                      column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                          0] == 'Ընդունման տարեթիվ' or column_names[
                                                          0] == 'Առարկա' or
                                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or
                                                      column_names[
                                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[1] == 'Ֆակուլտետ' or column_names[
                                                    1] == 'Ուսանողի սեռ' or column_names[
                                                            1] == 'Ծննդավայր (երկիր)' or
                                                        column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            1] == 'Ընդունման տարեթիվ' or column_names[
                                                            1] == 'Առարկա' or
                                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[2] == 'Ֆակուլտետ' or column_names[
                                                    2] == 'Ուսանողի սեռ' or column_names[
                                                            2] == 'Ծննդավայր (երկիր)' or
                                                        column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            2] == 'Ընդունման տարեթիվ' or column_names[
                                                            2] == 'Առարկա' or
                                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[3] == 'Ֆակուլտետ' or column_names[
                                                    3] == 'Ուսանողի սեռ' or column_names[
                                                            3] == 'Ծննդավայր (երկիր)' or
                                                        column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            3] == 'Ընդունման տարեթիվ' or column_names[
                                                            3] == 'Առարկա' or
                                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[4] == 'Ֆակուլտետ' or column_names[
                                                    4] == 'Ուսանողի սեռ' or column_names[
                                                            4] == 'Ծննդավայր (երկիր)' or
                                                        column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            4] == 'Ընդունման տարեթիվ' or column_names[
                                                            4] == 'Առարկա' or
                                                        column_names[4] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            4] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[5] == 'Ֆակուլտետ' or column_names[
                                                    5] == 'Ուսանողի սեռ' or column_names[
                                                            5] == 'Ծննդավայր (երկիր)' or
                                                        column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            5] == 'Ընդունման տարեթիվ' or column_names[
                                                            5] == 'Առարկա' or
                                                        column_names[5] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            5] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[6] == 'Ֆակուլտետ' or column_names[
                                                    6] == 'Ուսանողի սեռ' or column_names[
                                                            6] == 'Ծննդավայր (երկիր)' or
                                                        column_names[6] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            6] == 'Ընդունման տարեթիվ' or column_names[
                                                            6] == 'Առարկա' or
                                                        column_names[6] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            6] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[7] == 'Ֆակուլտետ' or column_names[
                                                    7] == 'Ուսանողի սեռ' or column_names[
                                                            7] == 'Ծննդավայր (երկիր)' or
                                                        column_names[7] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            7] == 'Ընդունման տարեթիվ' or column_names[
                                                            7] == 'Առարկա' or
                                                        column_names[7] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            7] == 'Երկրորդ միջանկյալ ստուգում'):
                                                    # data = pd.read_csv("CVS/Fac->/Fac8_Sx_COB_CV_YOE_Sbj_Fr_Ex _Sc_Ex.csv")
                                                    data = pd.read_csv(file_path,
                                                                       usecols=['Ֆակուլտետ', 'Ուսանողի սեռ',
                                                                                'Ծննդավայր (երկիր)',
                                                                                'Ծննդավայր (քաղաք/գյուղ)',
                                                                                'Ընդունման տարեթիվ',
                                                                                'Առարկա',
                                                                                'Առաջին միջանկյալ ստուգում',
                                                                                'Երկրորդ միջանկյալ ստուգում'])
                                                    # points = 1000
                                                    start = 0
                                                    end = 8
                                                    for i in range(0, 1000):
                                                        transactions.append(
                                                            [str(data.values[i, j]) for j in range(start, end)])
                                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                    0] == 'Ծննդավայր (երկիր)' or column_names[
                                                          0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                          0] == 'Ընդունման տարեթիվ' or column_names[
                                                          0] == 'Առարկա' or
                                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or
                                                      column_names[
                                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                          0] == 'Ամփոփիչ քննություն') and (
                                                        column_names[1] == 'Ֆակուլտետ' or column_names[
                                                    1] == 'Ծննդավայր (երկիր)' or column_names[
                                                            1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            1] == 'Ընդունման տարեթիվ' or column_names[
                                                            1] == 'Առարկա' or
                                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            1] == 'Ամփոփիչ քննություն') and (
                                                        column_names[2] == 'Ֆակուլտետ' or column_names[
                                                    2] == 'Ծննդավայր (երկիր)' or column_names[
                                                            2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            2] == 'Ընդունման տարեթիվ' or column_names[
                                                            2] == 'Առարկա' or
                                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            2] == 'Ամփոփիչ քննություն') and (
                                                        column_names[3] == 'Ֆակուլտետ' or column_names[
                                                    3] == 'Ծննդավայր (երկիր)' or column_names[
                                                            3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            3] == 'Ընդունման տարեթիվ' or column_names[
                                                            3] == 'Առարկա' or
                                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            3] == 'Ամփոփիչ քննություն') and (
                                                        column_names[4] == 'Ֆակուլտետ' or column_names[
                                                    4] == 'Ծննդավայր (երկիր)' or column_names[
                                                            4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            4] == 'Ընդունման տարեթիվ' or column_names[
                                                            4] == 'Առարկա' or
                                                        column_names[4] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            4] == 'Ամփոփիչ քննություն') and (
                                                        column_names[5] == 'Ֆակուլտետ' or column_names[
                                                    5] == 'Ծննդավայր (երկիր)' or column_names[
                                                            5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            5] == 'Ընդունման տարեթիվ' or column_names[
                                                            5] == 'Առարկա' or
                                                        column_names[5] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            5] == 'Ամփոփիչ քննություն') and (
                                                        column_names[6] == 'Ֆակուլտետ' or column_names[
                                                    6] == 'Ծննդավայր (երկիր)' or column_names[
                                                            6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            6] == 'Ընդունման տարեթիվ' or column_names[
                                                            6] == 'Առարկա' or
                                                        column_names[6] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            6] == 'Ամփոփիչ քննություն') and (
                                                        column_names[7] == 'Ֆակուլտետ' or column_names[
                                                    7] == 'Ծննդավայր (երկիր)' or column_names[
                                                            7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            7] == 'Ընդունման տարեթիվ' or column_names[
                                                            7] == 'Առարկա' or
                                                        column_names[7] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            7] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            7] == 'Ամփոփիչ քննություն'):
                                                    # data = pd.read_csv("CVS/Fac->/Fac8_COB_CV_YOE_Sbj_Fr_Ex _Sc_Ex_Fnl_Ex.csv")
                                                    data = pd.read_csv(file_path,
                                                                       usecols=['Ֆակուլտետ', 'Ամփոփիչ քննություն',
                                                                                'Ծննդավայր (երկիր)',
                                                                                'Ծննդավայր (քաղաք/գյուղ)',
                                                                                'Ընդունման տարեթիվ', 'Առարկա',
                                                                                'Առաջին միջանկյալ ստուգում',
                                                                                'Երկրորդ միջանկյալ ստուգում'])
                                                    # points = 1000
                                                    start = 0
                                                    end = 8
                                                    for i in range(0, 1000):
                                                        transactions.append(
                                                            [str(data.values[i, j]) for j in range(start, end)])
                                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                                    0] == 'Ծննդավայր (երկիր)' or column_names[
                                                          0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                          0] == 'Ընդունման տարեթիվ' or column_names[
                                                          0] == 'Առարկա' or
                                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or
                                                      column_names[
                                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                          0] == 'Ամփոփիչ քննություն') and (
                                                        column_names[1] == 'Ուսանողի անուն' or column_names[
                                                    1] == 'Ծննդավայր (երկիր)' or column_names[
                                                            1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            1] == 'Ընդունման տարեթիվ' or column_names[
                                                            1] == 'Առարկա' or
                                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            1] == 'Ամփոփիչ քննություն') and (
                                                        column_names[2] == 'Ուսանողի անուն' or column_names[
                                                    2] == 'Ծննդավայր (երկիր)' or column_names[
                                                            2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            2] == 'Ընդունման տարեթիվ' or column_names[
                                                            2] == 'Առարկա' or
                                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            2] == 'Ամփոփիչ քննություն') and (
                                                        column_names[3] == 'Ուսանողի անուն' or column_names[
                                                    3] == 'Ծննդավայր (երկիր)' or column_names[
                                                            3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            3] == 'Ընդունման տարեթիվ' or column_names[
                                                            3] == 'Առարկա' or
                                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            3] == 'Ամփոփիչ քննություն') and (
                                                        column_names[4] == 'Ուսանողի անուն' or column_names[
                                                    4] == 'Ծննդավայր (երկիր)' or column_names[
                                                            4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            4] == 'Ընդունման տարեթիվ' or column_names[
                                                            4] == 'Առարկա' or
                                                        column_names[4] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            4] == 'Ամփոփիչ քննություն') and (
                                                        column_names[5] == 'Ուսանողի անուն' or column_names[
                                                    5] == 'Ծննդավայր (երկիր)' or column_names[
                                                            5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            5] == 'Ընդունման տարեթիվ' or column_names[
                                                            5] == 'Առարկա' or
                                                        column_names[5] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            5] == 'Ամփոփիչ քննություն') and (
                                                        column_names[6] == 'Ուսանողի անուն' or column_names[
                                                    6] == 'Ծննդավայր (երկիր)' or column_names[
                                                            6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            6] == 'Ընդունման տարեթիվ' or column_names[
                                                            6] == 'Առարկա' or
                                                        column_names[6] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            6] == 'Ամփոփիչ քննություն') and (
                                                        column_names[7] == 'Ուսանողի անուն' or column_names[
                                                    7] == 'Ծննդավայր (երկիր)' or column_names[
                                                            7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            7] == 'Ընդունման տարեթիվ' or column_names[
                                                            7] == 'Առարկա' or
                                                        column_names[7] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            7] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            7] == 'Ամփոփիչ քննություն'):
                                                    # data = pd.read_csv("CVS/Nam->/Name8_COB_CV_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                                    data = pd.read_csv(file_path,
                                                                       usecols=['Ուսանողի անուն',
                                                                                'Ամփոփիչ քննություն',
                                                                                'Ծննդավայր (երկիր)',
                                                                                'Ծննդավայր (քաղաք/գյուղ)',
                                                                                'Ընդունման տարեթիվ', 'Առարկա',
                                                                                'Առաջին միջանկյալ ստուգում',
                                                                                'Երկրորդ միջանկյալ ստուգում'])
                                                    # points = 1000
                                                    start = 0
                                                    end = 8
                                                    for i in range(0, 1000):
                                                        transactions.append(
                                                            [str(data.values[i, j]) for j in range(start, end)])

                                                def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png','txt')):
                                                    """
                                                    Get the latest image file in the given directory
                                                    """

                                                    # get filepaths of all files and dirs in the given dir
                                                    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                                                    # filter out directories, no-extension, and wrong extension files
                                                    valid_files = [f for f in valid_files if '.' in f and \
                                                        f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                                                    if not valid_files:
                                                        raise ValueError("No valid images in %s" % dirpath)

                                                    return max(valid_files, key=os.path.getmtime)                                                      


                                                print("------------------------")
                                                oht = TransactionEncoder()
                                                oht_ary = oht.fit(transactions).transform(transactions)
                                                # oht.columns_  # Need to understand is this need or not!!!!
                                                df_train = pd.DataFrame(oht_ary, columns=oht.columns_)
                                                rules = apriori(df_train, min_support=0.01, use_colnames=True)
                                                training_rules = association_rules(rules, metric="confidence",
                                                                                   min_threshold=0.01)

                                                # Visualization of "Support" VS "Confidence" parameters on graph
                                                plt.figure(1)
                                                plt.scatter(training_rules['support'], training_rules['confidence'],
                                                            alpha=0.5)
                                                plt.xlabel('Support')
                                                plt.ylabel('Confidence')
                                                plt.title('Support vs Confidence')
                                                mngr = plt.get_current_fig_manager()
                                                mngr.window.setGeometry(20, 350, 600, 550)
                                                plt.savefig('images/apriori/' + datetime.now().strftime(
                                                    '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                                apr_8_1_path=get_latest_image("images/apriori/",'png')          
                                                image_apr_8_1 = PhotoImage(file=apr_8_1_path)
                                                original_image_apr_8_1 = image_apr_8_1.subsample(3,3) # resize image using subsample

                                                apr_8_1_im_label = Label(apr_image_frame,image=original_image_apr_8_1)
                                                apr_8_1_im_label.image = original_image_apr_8_1 # keep a reference
                                                apr_8_1_im_label.place(x=387, y=118)                                                

                                                # Visualization of "Support" VS "Lift" parameters on graph
                                                plt.figure(2)
                                                plt.scatter(training_rules['support'], training_rules['lift'],
                                                            alpha=0.5)
                                                plt.xlabel('Support')
                                                plt.ylabel('Lift')
                                                plt.title('Support vs Lift')

                                                mngr = plt.get_current_fig_manager()
                                                mngr.window.setGeometry(657, 350, 600, 550)
                                                plt.savefig('images/apriori/' + datetime.now().strftime(
                                                    '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                                apr_8_2_path=get_latest_image("images/apriori/",'png')        
                                                image_apr_8_2 = PhotoImage(file=apr_8_2_path)
                                                original_image_apr_8_2 = image_apr_8_2.subsample(3,3) # resize image using subsample

                                                apr_8_2_im_label = Label(apr_image_frame,image=original_image_apr_8_2)
                                                apr_8_2_im_label.image = original_image_apr_8_2 # keep a reference
                                                apr_8_2_im_label.place(x=627, y=118)                                                  

                                                # Visualization of "Support" VS "Confidence" & "Lift" parameters on graph
                                                plt.figure(3)
                                                fit = np.polyfit(training_rules['lift'],
                                                                 training_rules['confidence'],
                                                                 1)
                                                fit_fn = np.poly1d(fit)
                                                plt.plot(training_rules['lift'], training_rules['confidence'], 'yo',
                                                         training_rules['lift'], fit_fn(training_rules['lift']))
                                                plt.xlabel('lift')
                                                plt.ylabel('confidence')
                                                plt.title('lift vs confidence')                                                 
                                                mngr = plt.get_current_fig_manager()
                                                mngr.window.setGeometry(1298, 350, 600, 550)
                                                plt.savefig('images/apriori/' + datetime.now().strftime(
                                                    '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                                apr_8_3_path=get_latest_image("images/apriori/",'png')          
                                                image_apr_8_3 = PhotoImage(file=apr_8_3_path)
                                                original_image_apr_8_3 = image_apr_8_3.subsample(3,3) # resize image using subsample

                                                apr_8_3_im_label = Label(apr_image_frame,image=original_image_apr_8_3)
                                                apr_8_3_im_label.image = original_image_apr_8_3 # keep a reference
                                                apr_8_3_im_label.place(x=387, y=308)   

                                                def mouse_on_apr_8_1(event):
                                                    image_apr_8_1 = PhotoImage(file=apr_8_1_path)
                                                    original_image_apr_8_1 = image_apr_8_1.subsample(2,2) # resize image using subsample

                                                    apr_8_1_im_label = Label(apr_image_frame,image=original_image_apr_8_1)
                                                    apr_8_1_im_label.image = original_image_apr_8_1 # keep a reference
                                                    apr_8_1_im_label.place(x=387, y=118) 

                                                    return          

                                                def mouse_on_apr_8_2(event):
                                                    image_apr_8_2 = PhotoImage(file=apr_8_2_path)
                                                    original_image_apr_8_2 = image_apr_8_2.subsample(2,2) # resize image using subsample

                                                    apr_8_2_im_label = Label(apr_image_frame,image=original_image_apr_8_2)
                                                    apr_8_2_im_label.image = original_image_apr_8_2 # keep a reference
                                                    apr_8_2_im_label.place(x=627, y=118) 

                                                    return        

                                                def mouse_on_apr_8_3(event):
                                                    image_apr_8_3 = PhotoImage(file=apr_8_3_path)
                                                    original_image_apr_8_3 = image_apr_8_3.subsample(2,2) # resize image using subsample

                                                    apr_8_3_im_label = Label(apr_image_frame,image=original_image_apr_8_3)
                                                    apr_8_3_im_label.image = original_image_apr_8_3 # keep a reference
                                                    apr_8_3_im_label.place(x=387, y=308) 

                                                    return                                                                

                                                apr_8_1_im_label.bind('<Enter>',mouse_on_apr_8_1)                    
                                                apr_8_2_im_label.bind('<Enter>',mouse_on_apr_8_2)  
                                                apr_8_3_im_label.bind('<Enter>',mouse_on_apr_8_3)                                                                                              

                                                # Taking backup values from above graphs and puting puting appropriate directory
                                                try:
                                                    # Create target Directory
                                                    os.mkdir(dir_name)
                                                    print("Directory ", dir_name, " created.")
                                                except FileExistsError:
                                                    print("Directory ", dir_name, " already exists.")
                                                file = open(abs_path, 'w', encoding="utf8")
                                                file.write(str(training_rules))
                                                file.close()

                                                now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                                now = str(now)
                                                newname = 'apriori_' + now + '.txt'
                                                os.rename('apriori.txt', newname)
                                                shutil.move(newname,  "images/apriori/")

                                                apr_8_txt_path=get_latest_image("images/apriori/",'txt')
                                                print(apr_8_txt_path)  

                                                def apr_8_btn_click():
                                                    window.filename =  filedialog.askopenfile(mode='r',initialdir = "images/apriori/",title = apr_8_txt_path,filetypes = (("txt files","*.txt"),("all files","*.*")))

                                                apr_txt_entry=Entry(apr_txt_frame, highlightcolor='#ababba',justify=LEFT, relief=SUNKEN, width=18)
                                                apr_txt_entry.insert(END,apr_8_txt_path)
                                                apr_txt_entry.place(x=637, y=490)

                                                apr_txt_btn=Button(apr_txt_frame, text="Browse", bd=2, activebackground='#c7c7d1',relief=SUNKEN,command=apr_8_btn_click).place(x=786, y=486)                                                

                                                def rst_apr():
                                                    print("Reset")
                                                    cmb.set('')
                                                    cmb1.set('')
                                                    number_of_param.set('')                                                    
                                                    new_text = " "
                                                    e1.delete(0, tk.END)
                                                    e1.insert(0, new_text)
                                                    cmb.place_forget()
                                                    cmb1.place_forget()
                                                    cmb2.place_forget()
                                                    cmb3.place_forget()
                                                    cmb4.place_forget()
                                                    cmb5.place_forget()
                                                    cmb6.place_forget()
                                                    cmb7.place_forget()
                                                    apr_8_1_im_label.image =''
                                                    apr_8_2_im_label.image =''
                                                    apr_8_3_im_label.image =''
                                                    apr_txt_entry.delete(0, tk.END)      
                                                    apr_txt_entry.insert(0, new_text)

                                                plt_rst_apr=PhotoImage(file="reset.png")  
                                                sub_plt_rst_apr=plt_rst_apr.subsample(4,4)

                                                button_apr_rst = Button(apr_input_frame, text="Reset", fg='#026084', command=rst_apr, image=sub_plt_rst_apr, compound=LEFT, width=130)
                                                button_apr_rst.image=sub_plt_rst_apr
                                                button_apr_rst.place(x=88, y=453)
                                                button_arr.append(button_apr_rst)

                                                ttk.Separator(apr_input_frame).place(x=75, y=533, relwidth=0.29)                            

                                                def jnt_go_to_menu():

                                                    print("Coming soon")
  
                                                    apr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                                    #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                                    lbl_apr=Label(apr_frame, width=20, bg='white').place(x=10, y=10)
   
                                                    apr_inner_frame=Frame(apr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                                    #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                                    apr_input_frame=Frame(apr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                                    apr_image_frame=Frame(apr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                                    Label(apr_image_frame,bg='white').place(x=565, y=95)

                                                    apr_txt_frame=Frame(apr_image_frame, width=250, height=195, bg='white', highlightbackground='white').place(x=627,y=388)

                                                    lbl_apr_txt=Label(apr_txt_frame, width=17, bg='white').place(x=630, y=392)                            

                                                    print("Apriori frame has been destroyed.")      

                                                plt_up=PhotoImage(file="up.png")  
                                                sub_plt_up=plt_up.subsample(9,9)     

                                                button_jnt_go_to_menu=Button(apr_input_frame, text="Go to menu", fg='#026084', command=jnt_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                                button_jnt_go_to_menu.image=sub_plt_up
                                                button_jnt_go_to_menu.place(x=88, y=535)
                                                button_arr.append(button_jnt_go_to_menu) 

                                            # Creating a photoimage object to use image 
                                            plt_gen_apr = PhotoImage(file = "images.png") 
                                            sub_plt_gen_apr = plt_gen_apr.subsample(4, 4)    

                                            button_apr_gen = Button(apr_input_frame, text="Generate", fg='#026084', command=apr_gen, image=sub_plt_gen_apr, compound=LEFT)
                                            button_apr_gen.image=sub_plt_gen_apr
                                            button_apr_gen.place(x=88, y=383)
                                            button_arr.append(button_apr_gen)

                                            ttk.Separator(apr_input_frame).place(x=75, y=373, relwidth=0.29)                                             

                                        cmb7 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                        cmb7.place(x=75, y=342)
                                        cmb7.bind('<<ComboboxSelected>>', on_eight_select)

                                    cmb6 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                    cmb6.place(x=75, y=319)
                                    cmb6.bind('<<ComboboxSelected>>', on_seventh_select)

                                cmb5 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                cmb5.place(x=75, y=296)
                                cmb5.bind('<<ComboboxSelected>>', on_sixth_select)

                            cmb4 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        elif (e1.get() == "9" or e1.get() == " 9"):
            print("else 9")

            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):
                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                sixth_data = fifth_data

                                for item in fifth_data:
                                    if item == fifth_curr_val:
                                        sixth_data.remove(item)

                                def on_sixth_select(event=None):
                                    sixth_curr_val = cmb5.get()

                                    if len(column_names) > 5:
                                        column_names.pop(5)

                                    column_names.append(sixth_curr_val)

                                    seventh_data = sixth_data

                                    for item in sixth_data:
                                        if item == sixth_curr_val:
                                            seventh_data.remove(item)

                                    def on_seventh_select(event=None):
                                        seventh_curr_val = cmb6.get()

                                        if len(column_names) > 6:
                                            column_names.pop(6)

                                        column_names.append(seventh_curr_val)

                                        eight_data = seventh_data

                                        for item in seventh_data:
                                            if item == seventh_curr_val:
                                                eight_data.remove(item)

                                        def on_eight_select(event=None):
                                            eight_curr_val = cmb7.get()

                                            if len(column_names) > 7:
                                                column_names.pop(7)

                                            column_names.append(eight_curr_val)

                                            ninth_data = eight_data

                                            for item in eight_data:
                                                if item == eight_curr_val:
                                                    ninth_data.remove(item)

                                            def on_ninth_select(event=None):
                                                ninth_curr_val = cmb8.get()

                                                if len(column_names) > 8:
                                                    column_names.pop(8)

                                                column_names.append(ninth_curr_val)

                                                def apr_gen():

                                                    print("Apr Generation")

                                                    apriori_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն',
                                                                               'Ուսանողի սեռ', 'Ծննդավայր (երկիր)',
                                                                               'Ծննդավայր (քաղաք/գյուղ)',
                                                                               'Ընդունման տարեթիվ', 'Առարկա',
                                                                               'Առաջին միջանկյալ ստուգում',
                                                                               'Երկրորդ միջանկյալ ստուգում',
                                                                               'Ամփոփիչ քննություն']

                                                    # Intilizing global vaiables
                                                    transactions = []

                                                    # DB file name for Apriori algorithm
                                                    folder_name = ['apriori']
                                                    txt_file_name = ['apriori.txt']

                                                    # Getting dynamically path for appropriate DB file and backup directory
                                                    absolute_path = sys.path[0]

                                                    file_path = sys.path[0] + '/' + db

                                                    #dir_name = absolute_path + '\\' + folder_name[0]
                                                    #abs_path = dir_name + '\\' + txt_file_name[0]

                                                    f_path = pathlib.Path(__file__).parent.absolute()
                                                    f_path = str(f_path)
                                                    dir_name = f_path + '/' + 'images' + '/' + folder_name[0]
                                                    abs_path = f_path + '/' + txt_file_name[0]                                                     

                                                    # Setting pandas library options
                                                    pd.set_option('display.max_columns', None)
                                                    pd.set_option('display.max_rows', None)

                                                    if not find_plathform():
                                                        file_path = file_path.replace("\\", "/")
                                                    data = pd.read_csv(file_path)

                                                    if (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                        0] == 'Ուսանողի անուն' or column_names[
                                                            0] == 'Ուսանողի սեռ' or
                                                        column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                                            0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            0] == 'Ընդունման տարեթիվ' or column_names[
                                                            0] == 'Առարկա' or
                                                        column_names[0] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[1] == 'Ֆակուլտետ' or column_names[
                                                        1] == 'Ուսանողի անուն' or column_names[
                                                                1] == 'Ուսանողի սեռ' or
                                                            column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                1] == 'Ընդունման տարեթիվ' or column_names[
                                                                1] == 'Առարկա' or column_names[
                                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                1] == 'Second_Exam') and (
                                                            column_names[2] == 'Ֆակուլտետ' or column_names[
                                                        2] == 'Ուսանողի անուն' or column_names[
                                                                2] == 'Ուսանողի սեռ' or
                                                            column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                2] == 'Ընդունման տարեթիվ' or column_names[
                                                                2] == 'Առարկա' or column_names[
                                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[3] == 'Ֆակուլտետ' or column_names[
                                                        3] == 'Ուսանողի անուն' or column_names[
                                                                3] == 'Ուսանողի սեռ' or
                                                            column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                3] == 'Ընդունման տարեթիվ' or column_names[
                                                                3] == 'Առարկա' or column_names[
                                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[4] == 'Ֆակուլտետ' or column_names[
                                                        4] == 'Ուսանողի անուն' or column_names[
                                                                4] == 'Ուսանողի սեռ' or
                                                            column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                4] == 'Ընդունման տարեթիվ' or column_names[
                                                                4] == 'Առարկա' or column_names[
                                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                4] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[5] == 'Ֆակուլտետ' or column_names[
                                                        5] == 'Ուսանողի անուն' or column_names[
                                                                5] == 'Ուսանողի սեռ' or
                                                            column_names[5] == 'Ծննդավայր (երկիր)' or column_names[
                                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                5] == 'Ընդունման տարեթիվ' or column_names[
                                                                5] == 'Առարկա' or column_names[
                                                                5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                5] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[6] == 'Ֆակուլտետ' or column_names[
                                                        6] == 'Ուսանողի անուն' or column_names[
                                                                6] == 'Ուսանողի սեռ' or
                                                            column_names[6] == 'Ծննդավայր (երկիր)' or column_names[
                                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                6] == 'Ընդունման տարեթիվ' or column_names[
                                                                6] == 'Առարկա' or column_names[
                                                                6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                6] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[7] == 'Ֆակուլտետ' or column_names[
                                                        7] == 'Ուսանողի անուն' or column_names[
                                                                7] == 'Ուսանողի սեռ' or
                                                            column_names[7] == 'Ծննդավայր (երկիր)' or column_names[
                                                                7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                7] == 'Ընդունման տարեթիվ' or column_names[
                                                                7] == 'Առարկա' or column_names[
                                                                7] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                7] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[8] == 'Ֆակուլտետ' or column_names[
                                                        8] == 'Ուսանողի անուն' or column_names[
                                                                8] == 'Ուսանողի սեռ' or
                                                            column_names[8] == 'Ծննդավայր (երկիր)' or column_names[
                                                                8] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                8] == 'Ընդունման տարեթիվ' or column_names[
                                                                8] == 'Առարկա' or column_names[
                                                                8] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                8] == 'Երկրորդ միջանկյալ ստուգում'):
                                                        # data = pd.read_csv("CVS/Sx->/Sx7_C_V_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                                        # points = 1000
                                                        start = 0
                                                        end = 9
                                                        for i in range(0, 1000):
                                                            transactions.append(
                                                                [str(data.values[i, j]) for j in range(start, end)])
                                                    elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                                        0] == 'Ուսանողի սեռ' or column_names[
                                                              0] == 'Ծննդավայր (երկիր)' or column_names[
                                                              0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                              0] == 'Ընդունման տարեթիվ' or column_names[
                                                              0] == 'Առարկա' or column_names[
                                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                              0] == 'Ամփոփիչ քննություն') and (
                                                            column_names[1] == 'Ուսանողի անուն' or column_names[
                                                        1] == 'Ուսանողի սեռ' or column_names[
                                                                1] == 'Ծննդավայր (երկիր)' or column_names[
                                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                1] == 'Ընդունման տարեթիվ' or column_names[
                                                                1] == 'Առարկա' or column_names[
                                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                1] == 'Ամփոփիչ քննություն') and (
                                                            column_names[2] == 'Ուսանողի անուն' or column_names[
                                                        2] == 'Ուսանողի սեռ' or column_names[
                                                                2] == 'Ծննդավայր (երկիր)' or column_names[
                                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                2] == 'Ընդունման տարեթիվ' or column_names[
                                                                2] == 'Առարկա' or column_names[
                                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                2] == 'Ամփոփիչ քննություն') and (
                                                            column_names[3] == 'Ուսանողի անուն' or column_names[
                                                        3] == 'Ուսանողի սեռ' or column_names[
                                                                3] == 'Ծննդավայր (երկիր)' or column_names[
                                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                3] == 'Ընդունման տարեթիվ' or column_names[
                                                                3] == 'Առարկա' or column_names[
                                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                3] == 'Ամփոփիչ քննություն') and (
                                                            column_names[4] == 'Ուսանողի անուն' or column_names[
                                                        4] == 'Ուսանողի սեռ' or column_names[
                                                                4] == 'Ծննդավայր (երկիր)' or column_names[
                                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                4] == 'Ընդունման տարեթիվ' or column_names[
                                                                4] == 'Առարկա' or column_names[
                                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                4] == 'Ամփոփիչ քննություն') and (
                                                            column_names[5] == 'Ուսանողի անուն' or column_names[
                                                        5] == 'Ուսանողի սեռ' or column_names[
                                                                5] == 'Ծննդավայր (երկիր)' or column_names[
                                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                5] == 'Ընդունման տարեթիվ' or column_names[
                                                                5] == 'Առարկա' or column_names[
                                                                5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                5] == 'Ամփոփիչ քննություն') and (
                                                            column_names[6] == 'Ուսանողի անուն' or column_names[
                                                        6] == 'Ուսանողի սեռ' or column_names[
                                                                6] == 'Ծննդավայր (երկիր)' or column_names[
                                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                6] == 'Ընդունման տարեթիվ' or column_names[
                                                                6] == 'Առարկա' or column_names[
                                                                6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                6] == 'Ամփոփիչ քննություն') and (
                                                            column_names[7] == 'Ուսանողի անուն' or column_names[
                                                        7] == 'Ուսանողի սեռ' or column_names[
                                                                7] == 'Ծննդավայր (երկիր)' or column_names[
                                                                7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                7] == 'Ընդունման տարեթիվ' or column_names[
                                                                7] == 'Առարկա' or column_names[
                                                                7] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                7] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                7] == 'Ամփոփիչ քննություն') and (
                                                            column_names[8] == 'Ուսանողի անուն' or column_names[
                                                        8] == 'Ուսանողի սեռ' or column_names[
                                                                8] == 'Ծննդավայր (երկիր)' or column_names[
                                                                8] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                8] == 'Ընդունման տարեթիվ' or column_names[
                                                                8] == 'Առարկա' or column_names[
                                                                8] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                8] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                8] == 'Ամփոփիչ քննություն'):
                                                        # data = pd.read_csv("CVS/Sx->/Sx7_C_V_YOE_Sbj_Fr_Ex_Sc_Ex_Fnl_Ex.csv")
                                                        # points = 1000
                                                        start = 1
                                                        end = 10
                                                        for i in range(0, 1000):
                                                            transactions.append(
                                                                [str(data.values[i, j]) for j in range(start, end)])
                                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                        0] == 'Ուսանողի սեռ' or column_names[
                                                              0] == 'Ծննդավայր (երկիր)' or column_names[
                                                              0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                              0] == 'Ընդունման տարեթիվ' or column_names[
                                                              0] == 'Առարկա' or column_names[
                                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                              0] == 'Ամփոփիչ քննություն') and (
                                                            column_names[1] == 'Ֆակուլտետ' or column_names[
                                                        1] == 'Ուսանողի սեռ' or column_names[
                                                                1] == 'Ծննդավայր (երկիր)' or column_names[
                                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                1] == 'Ընդունման տարեթիվ' or column_names[
                                                                1] == 'Առարկա' or column_names[
                                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                1] == 'Ամփոփիչ քննություն') and (
                                                            column_names[2] == 'Ֆակուլտետ' or column_names[
                                                        2] == 'Ուսանողի սեռ' or column_names[
                                                                2] == 'Ծննդավայր (երկիր)' or column_names[
                                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                2] == 'Ընդունման տարեթիվ' or column_names[
                                                                2] == 'Առարկա' or column_names[
                                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                2] == 'Ամփոփիչ քննություն') and (
                                                            column_names[3] == 'Ֆակուլտետ' or column_names[
                                                        3] == 'Ուսանողի սեռ' or column_names[
                                                                3] == 'Ծննդավայր (երկիր)' or column_names[
                                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                3] == 'Ընդունման տարեթիվ' or column_names[
                                                                3] == 'Առարկա' or column_names[
                                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                3] == 'Ամփոփիչ քննություն') and (
                                                            column_names[4] == 'Ֆակուլտետ' or column_names[
                                                        4] == 'Ուսանողի սեռ' or column_names[
                                                                4] == 'Ծննդավայր (երկիր)' or column_names[
                                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                4] == 'Ընդունման տարեթիվ' or column_names[
                                                                4] == 'Առարկա' or column_names[
                                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                4] == 'Ամփոփիչ քննություն') and (
                                                            column_names[5] == 'Ֆակուլտետ' or column_names[
                                                        5] == 'Ուսանողի սեռ' or column_names[
                                                                5] == 'Ծննդավայր (երկիր)' or column_names[
                                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                5] == 'Ընդունման տարեթիվ' or column_names[
                                                                5] == 'Առարկա' or column_names[
                                                                5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                5] == 'Ամփոփիչ քննություն') and (
                                                            column_names[6] == 'Ֆակուլտետ' or column_names[
                                                        6] == 'Ուսանողի սեռ' or column_names[
                                                                6] == 'Ծննդավայր (երկիր)' or column_names[
                                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                6] == 'Ընդունման տարեթիվ' or column_names[
                                                                6] == 'Առարկա' or column_names[
                                                                6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                6] == 'Ամփոփիչ քննություն') and (
                                                            column_names[7] == 'Ֆակուլտետ' or column_names[
                                                        7] == 'Ուսանողի սեռ' or column_names[
                                                                7] == 'Ծննդավայր (երկիր)' or column_names[
                                                                7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                7] == 'Ընդունման տարեթիվ' or column_names[
                                                                7] == 'Առարկա' or column_names[
                                                                7] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                7] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                7] == 'Ամփոփիչ քննություն') and (
                                                            column_names[8] == 'Ֆակուլտետ' or column_names[
                                                        8] == 'Ուսանողի սեռ' or column_names[
                                                                8] == 'Ծննդավայր (երկիր)' or column_names[
                                                                8] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                8] == 'Ընդունման տարեթիվ' or column_names[
                                                                8] == 'Առարկա' or column_names[
                                                                8] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                8] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                8] == 'Ամփոփիչ քննություն'):
                                                        # data = pd.read_csv("CVS/Fac->/Fac9_Sx_COB_CV_YOE_Sbj_Fr_Ex _Sc_Ex_Fnl_Ex.csv")
                                                        data = pd.read_csv(file_path,
                                                                           usecols=['Ֆակուլտետ', 'Ուսանողի սեռ',
                                                                                    'Ծննդավայր (երկիր)',
                                                                                    'Ծննդավայր (քաղաք/գյուղ)',
                                                                                    'Ընդունման տարեթիվ', 'Առարկա',
                                                                                    'Առաջին միջանկյալ ստուգում',
                                                                                    'Երկրորդ միջանկյալ ստուգում',
                                                                                    'Ամփոփիչ քննություն'])
                                                        # points = 1000
                                                        start = 0
                                                        end = 9
                                                        for i in range(0, 1000):
                                                            transactions.append(
                                                                [str(data.values[i, j]) for j in range(start, end)])

                                                    def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png','txt')):
                                                        """
                                                        Get the latest image file in the given directory
                                                        """

                                                        # get filepaths of all files and dirs in the given dir
                                                        valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                                                        # filter out directories, no-extension, and wrong extension files
                                                        valid_files = [f for f in valid_files if '.' in f and \
                                                            f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                                                        if not valid_files:
                                                            raise ValueError("No valid images in %s" % dirpath)

                                                        return max(valid_files, key=os.path.getmtime)                                                                   

                                                    print("------------------------")
                                                    oht = TransactionEncoder()
                                                    oht_ary = oht.fit(transactions).transform(transactions)
                                                    # oht.columns_  # Need to understand is this need or not!!!!
                                                    df_train = pd.DataFrame(oht_ary, columns=oht.columns_)
                                                    rules = apriori(df_train, min_support=0.01, use_colnames=True)
                                                    training_rules = association_rules(rules, metric="confidence",
                                                                                       min_threshold=0.01)

                                                    # Visualization of "Support" VS "Confidence" parameters on graph
                                                    plt.figure(1)
                                                    plt.scatter(training_rules['support'],
                                                                training_rules['confidence'],
                                                                alpha=0.5)
                                                    plt.xlabel('Support')
                                                    plt.ylabel('Confidence')
                                                    plt.title('Support vs Confidence')
                                                    mngr = plt.get_current_fig_manager()
                                                    mngr.window.setGeometry(20, 350, 600, 550)
                                                    plt.savefig('images/apriori/' + datetime.now().strftime(
                                                        '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                                    apr_9_1_path=get_latest_image("images/apriori/",'png')          
                                                    image_apr_9_1 = PhotoImage(file=apr_9_1_path)
                                                    original_image_apr_9_1 = image_apr_9_1.subsample(3,3) # resize image using subsample

                                                    apr_9_1_im_label = Label(apr_image_frame,image=original_image_apr_9_1)
                                                    apr_9_1_im_label.image = original_image_apr_9_1 # keep a reference
                                                    apr_9_1_im_label.place(x=387, y=118)                                                       

                                                    # Visualization of "Support" VS "Lift" parameters on graph
                                                    plt.figure(2)
                                                    plt.scatter(training_rules['support'], training_rules['lift'],
                                                                alpha=0.5)
                                                    plt.xlabel('Support')
                                                    plt.ylabel('Lift')
                                                    plt.title('Support vs Lift')
                                                    mngr = plt.get_current_fig_manager()
                                                    mngr.window.setGeometry(657, 350, 600, 550)
                                                    plt.savefig('images/apriori/' + datetime.now().strftime(
                                                        '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                                    apr_9_2_path=get_latest_image("images/apriori/",'png')        
                                                    image_apr_9_2 = PhotoImage(file=apr_9_2_path)
                                                    original_image_apr_9_2 = image_apr_9_2.subsample(3,3) # resize image using subsample

                                                    apr_9_2_im_label = Label(apr_image_frame,image=original_image_apr_9_2)
                                                    apr_9_2_im_label.image = original_image_apr_9_2 # keep a reference
                                                    apr_9_2_im_label.place(x=627, y=118)                                                  


                                                    # Visualization of "Support" VS "Confidence" & "Lift" parameters on graph
                                                    plt.figure(3)
                                                    fit = np.polyfit(training_rules['lift'],
                                                                     training_rules['confidence'], 1)
                                                    fit_fn = np.poly1d(fit)
                                                    plt.plot(training_rules['lift'], training_rules['confidence'],
                                                             'yo',
                                                             training_rules['lift'], fit_fn(training_rules['lift']))
                                                    plt.xlabel('lift')
                                                    plt.ylabel('confidence')
                                                    plt.title('lift vs confidence')                                                     
                                                    mngr = plt.get_current_fig_manager()
                                                    mngr.window.setGeometry(1298, 350, 600, 550)
                                                    plt.savefig('images/apriori/' + datetime.now().strftime(
                                                        '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                                    apr_9_3_path=get_latest_image("images/apriori/",'png')          
                                                    image_apr_9_3 = PhotoImage(file=apr_9_3_path)
                                                    original_image_apr_9_3 = image_apr_9_3.subsample(3,3) # resize image using subsample

                                                    apr_9_3_im_label = Label(apr_image_frame,image=original_image_apr_9_3)
                                                    apr_9_3_im_label.image = original_image_apr_9_3 # keep a reference
                                                    apr_9_3_im_label.place(x=387, y=308)  

                                                    def mouse_on_apr_9_1(event):
                                                        image_apr_9_1 = PhotoImage(file=apr_9_1_path)
                                                        original_image_apr_9_1 = image_apr_9_1.subsample(2,2) # resize image using subsample

                                                        apr_9_1_im_label = Label(apr_image_frame,image=original_image_apr_9_1)
                                                        apr_9_1_im_label.image = original_image_apr_9_1 # keep a reference
                                                        apr_9_1_im_label.place(x=387, y=118) 

                                                        return          

                                                    def mouse_on_apr_9_2(event):
                                                        image_apr_9_2 = PhotoImage(file=apr_9_2_path)
                                                        original_image_apr_9_2 = image_apr_9_2.subsample(2,2) # resize image using subsample

                                                        apr_9_2_im_label = Label(apr_image_frame,image=original_image_apr_9_2)
                                                        apr_9_2_im_label.image = original_image_apr_9_2 # keep a reference
                                                        apr_9_2_im_label.place(x=627, y=118) 

                                                        return        

                                                    def mouse_on_apr_9_3(event):
                                                        image_apr_9_3 = PhotoImage(file=apr_9_3_path)
                                                        original_image_apr_9_3 = image_apr_9_3.subsample(2,2) # resize image using subsample

                                                        apr_9_3_im_label = Label(apr_image_frame,image=original_image_apr_9_3)
                                                        apr_9_3_im_label.image = original_image_apr_9_3 # keep a reference
                                                        apr_9_3_im_label.place(x=387, y=308) 

                                                        return                                                                

                                                    apr_9_1_im_label.bind('<Enter>',mouse_on_apr_9_1)                    
                                                    apr_9_2_im_label.bind('<Enter>',mouse_on_apr_9_2)  
                                                    apr_9_3_im_label.bind('<Enter>',mouse_on_apr_9_3)                                                     

                                                    # Taking backup values from above graphs and puting puting appropriate directory
                                                    try:
                                                        # Create target Directory
                                                        os.mkdir(dir_name)
                                                        print("Directory ", dir_name, " created.")
                                                    except FileExistsError:
                                                        print("Directory ", dir_name, " already exists.")
                                                    file = open(abs_path, 'w', encoding="utf8")
                                                    file.write(str(training_rules))
                                                    file.close()

                                                    now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                                    now = str(now)
                                                    newname = 'apriori_' + now + '.txt'
                                                    os.rename('apriori.txt', newname)
                                                    shutil.move(newname,  "images/apriori/")

                                                    apr_9_txt_path=get_latest_image("images/apriori/",'txt')
                                                    print(apr_9_txt_path)  

                                                    def apr_9_btn_click():
                                                        window.filename =  filedialog.askopenfile(mode='r',initialdir = "images/apriori/",title = apr_9_txt_path,filetypes = (("txt files","*.txt"),("all files","*.*")))

                                                    apr_txt_entry=Entry(apr_txt_frame, highlightcolor='#ababba',justify=LEFT, relief=SUNKEN, width=18)
                                                    apr_txt_entry.insert(END,apr_9_txt_path)
                                                    apr_txt_entry.place(x=637, y=490)

                                                    apr_txt_btn=Button(apr_txt_frame, text="Browse", bd=2, activebackground='#c7c7d1',relief=SUNKEN,command=apr_9_btn_click).place(x=786, y=486)                                                    

                                                    def rst_apr():
                                                        print("Reset")
                                                        cmb.set('')
                                                        cmb1.set('')
                                                        number_of_param.set('')                                                          
                                                        new_text = " "
                                                        e1.delete(0, tk.END)
                                                        e1.insert(0, new_text)
                                                        cmb.place_forget()
                                                        cmb1.place_forget()
                                                        cmb2.place_forget()
                                                        cmb3.place_forget()
                                                        cmb4.place_forget()
                                                        cmb5.place_forget()
                                                        cmb6.place_forget()
                                                        cmb7.place_forget()
                                                        cmb8.place_forget()
                                                        apr_9_1_im_label.image =''
                                                        apr_9_2_im_label.image =''
                                                        apr_9_3_im_label.image =''
                                                        apr_txt_entry.delete(0, tk.END)      
                                                        apr_txt_entry.insert(0, new_text)

                                                    plt_rst_apr=PhotoImage(file="reset.png")  
                                                    sub_plt_rst_apr=plt_rst_apr.subsample(4,4)

                                                    button_apr_rst = Button(apr_input_frame, text="Reset", fg='#026084', command=rst_apr, image=sub_plt_rst_apr, compound=LEFT, width=130)
                                                    button_apr_rst.image=sub_plt_rst_apr
                                                    button_apr_rst.place(x=88, y=466)
                                                    button_arr.append(button_apr_rst)

                                                    ttk.Separator(apr_input_frame).place(x=75, y=536, relwidth=0.29)                            

                                                    def jnt_go_to_menu():

                                                        print("Coming soon")
  
                                                        apr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                                        #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                                        lbl_apr=Label(apr_frame, width=20, bg='white').place(x=10, y=10)
   
                                                        apr_inner_frame=Frame(apr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                                        #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                                        apr_input_frame=Frame(apr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                                        apr_image_frame=Frame(apr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                                        Label(apr_image_frame,bg='white').place(x=565, y=95)

                                                        apr_txt_frame=Frame(apr_image_frame, width=250, height=195, bg='white', highlightbackground='white').place(x=627,y=388)

                                                        lbl_apr_txt=Label(apr_txt_frame, width=17, bg='white').place(x=630, y=392)                            

                                                        print("Apriori frame has been destroyed.")      

                                                    plt_up=PhotoImage(file="up.png")  
                                                    sub_plt_up=plt_up.subsample(10,10)     

                                                    button_jnt_go_to_menu=Button(apr_input_frame, text="Go to menu", fg='#026084', command=jnt_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                                    button_jnt_go_to_menu.image=sub_plt_up
                                                    button_jnt_go_to_menu.place(x=88, y=538)
                                                    button_arr.append(button_jnt_go_to_menu) 

                                                # Creating a photoimage object to use image 
                                                plt_gen_apr = PhotoImage(file = "images.png") 
                                                sub_plt_gen_apr = plt_gen_apr.subsample(4, 4)    

                                                button_apr_gen = Button(apr_input_frame, text="Generate", fg='#026084', command=apr_gen, image=sub_plt_gen_apr, compound=LEFT)
                                                button_apr_gen.image=sub_plt_gen_apr
                                                button_apr_gen.place(x=88, y=401)
                                                button_arr.append(button_apr_gen)

                                                ttk.Separator(apr_input_frame).place(x=75, y=396, relwidth=0.29) 

                                            cmb8 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                            cmb8.place(x=75, y=365)
                                            cmb8.bind('<<ComboboxSelected>>', on_ninth_select)

                                        cmb7 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                        cmb7.place(x=75, y=342)
                                        cmb7.bind('<<ComboboxSelected>>', on_eight_select)

                                    cmb6 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                    cmb6.place(x=75, y=319)
                                    cmb6.bind('<<ComboboxSelected>>', on_seventh_select)

                                cmb5 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                cmb5.place(x=75, y=296)
                                cmb5.bind('<<ComboboxSelected>>', on_sixth_select)

                            cmb4 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        elif (e1.get() == "10" or e1.get() == " 10"):
            print("else 10")

            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):
                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                sixth_data = fifth_data

                                for item in fifth_data:
                                    if item == fifth_curr_val:
                                        sixth_data.remove(item)

                                def on_sixth_select(event=None):
                                    sixth_curr_val = cmb5.get()

                                    if len(column_names) > 5:
                                        column_names.pop(5)

                                    column_names.append(sixth_curr_val)

                                    seventh_data = sixth_data

                                    for item in sixth_data:
                                        if item == sixth_curr_val:
                                            seventh_data.remove(item)

                                    def on_seventh_select(event=None):
                                        seventh_curr_val = cmb6.get()

                                        if len(column_names) > 6:
                                            column_names.pop(6)

                                        column_names.append(seventh_curr_val)

                                        eight_data = seventh_data

                                        for item in seventh_data:
                                            if item == seventh_curr_val:
                                                eight_data.remove(item)

                                        def on_eight_select(event=None):
                                            eight_curr_val = cmb7.get()

                                            if len(column_names) > 7:
                                                column_names.pop(7)

                                            column_names.append(eight_curr_val)

                                            ninth_data = eight_data

                                            for item in eight_data:
                                                if item == eight_curr_val:
                                                    ninth_data.remove(item)

                                            def on_ninth_select(event=None):
                                                ninth_curr_val = cmb8.get()

                                                if len(column_names) > 8:
                                                    column_names.pop(8)

                                                column_names.append(ninth_curr_val)

                                                tenth_data = ninth_data

                                                for item in ninth_data:
                                                    if item == ninth_curr_val:
                                                        tenth_data.remove(item)

                                                def on_tenth_select(event=None):
                                                    tenth_curr_val = cmb9.get()

                                                    if len(column_names) > 9:
                                                        column_names.pop(9)

                                                    column_names.append(tenth_curr_val)

                                                    def apr_gen():

                                                        print("Apr Generation")

                                                        apriori_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն',
                                                                                   'Ուսանողի սեռ',
                                                                                   'Ծննդավայր (երկիր)',
                                                                                   'Ծննդավայր (քաղաք/գյուղ)',
                                                                                   'Ընդունման տարեթիվ', 'Առարկա',
                                                                                   'Առաջին միջանկյալ ստուգում',
                                                                                   'Երկրորդ միջանկյալ ստուգում',
                                                                                   'Ամփոփիչ քննություն']

                                                        # Intilizing global vaiables
                                                        transactions = []

                                                        # DB file name for Apriori algorithm
                                                        folder_name = ['apriori']
                                                        txt_file_name = ['apriori.txt']

                                                        # Getting dynamically path for appropriate DB file and backup directory
                                                        absolute_path = sys.path[0]

                                                        file_path = sys.path[0] + '/' + db

                                                        #dir_name = absolute_path + '\\' + folder_name[0]
                                                        #abs_path = dir_name + '\\' + txt_file_name[0]

                                                        f_path = pathlib.Path(__file__).parent.absolute()
                                                        f_path = str(f_path)
                                                        dir_name = f_path + '/' + 'images' + '/' + folder_name[0]
                                                        abs_path = f_path + '/' + txt_file_name[0]                                                     

                                                        # Setting pandas library options
                                                        pd.set_option('display.max_columns', None)
                                                        pd.set_option('display.max_rows', None)

                                                        if not find_plathform():
                                                            file_path = file_path.replace("\\", "/")
                                                        data = pd.read_csv(file_path)

                                                        start = 0
                                                        end = 10
                                                        for i in range(0, 1000):
                                                            transactions.append(
                                                                [str(data.values[i, j]) for j in range(start, end)])

                                                        def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png','txt')):
                                                            """
                                                            Get the latest image file in the given directory
                                                            """

                                                            # get filepaths of all files and dirs in the given dir
                                                            valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                                                            # filter out directories, no-extension, and wrong extension files
                                                            valid_files = [f for f in valid_files if '.' in f and \
                                                                f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                                                            if not valid_files:
                                                                raise ValueError("No valid images in %s" % dirpath)

                                                            return max(valid_files, key=os.path.getmtime)                                                               

                                                        print("------------------------")
                                                        oht = TransactionEncoder()
                                                        oht_ary = oht.fit(transactions).transform(transactions)
                                                        # oht.columns_  # Need to understand is this need or not!!!!
                                                        df_train = pd.DataFrame(oht_ary, columns=oht.columns_)
                                                        rules = apriori(df_train, min_support=0.01,
                                                                        use_colnames=True)
                                                        training_rules = association_rules(rules,
                                                                                           metric="confidence",
                                                                                           min_threshold=0.01)

                                                        # Visualization of "Support" VS "Confidence" parameters on graph
                                                        plt.figure(1)
                                                        plt.scatter(training_rules['support'],
                                                                    training_rules['confidence'], alpha=0.5)
                                                        plt.xlabel('Support')
                                                        plt.ylabel('Confidence')
                                                        plt.title('Support vs Confidence')
                                                        mngr = plt.get_current_fig_manager()
                                                        mngr.window.setGeometry(20, 350, 600, 550)
                                                        plt.savefig('images/apriori/' + datetime.now().strftime(
                                                            '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                                        apr_10_1_path=get_latest_image("images/apriori/",'png')          
                                                        image_apr_10_1 = PhotoImage(file=apr_10_1_path)
                                                        original_image_apr_10_1 = image_apr_10_1.subsample(3,3) # resize image using subsample

                                                        apr_10_1_im_label = Label(apr_image_frame,image=original_image_apr_10_1)
                                                        apr_10_1_im_label.image = original_image_apr_10_1 # keep a reference
                                                        apr_10_1_im_label.place(x=387, y=118)                                                          

                                                        # Visualization of "Support" VS "Lift" parameters on graph
                                                        plt.figure(2)
                                                        plt.scatter(training_rules['support'],
                                                                    training_rules['lift'],
                                                                    alpha=0.5)
                                                        plt.xlabel('Support')
                                                        plt.ylabel('Lift')
                                                        plt.title('Support vs Lift')
                                                        mngr = plt.get_current_fig_manager()
                                                        mngr.window.setGeometry(657, 350, 600, 550)
                                                        plt.savefig('images/apriori/' + datetime.now().strftime(
                                                            '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                                        apr_10_2_path=get_latest_image("images/apriori/",'png')        
                                                        image_apr_10_2 = PhotoImage(file=apr_10_2_path)
                                                        original_image_apr_10_2 = image_apr_10_2.subsample(3,3) # resize image using subsample

                                                        apr_10_2_im_label = Label(apr_image_frame,image=original_image_apr_10_2)
                                                        apr_10_2_im_label.image = original_image_apr_10_2 # keep a reference
                                                        apr_10_2_im_label.place(x=627, y=118)                                                         

                                                        # Visualization of "Support" VS "Confidence" & "Lift" parameters on graph
                                                        plt.figure(3)
                                                        fit = np.polyfit(training_rules['lift'],
                                                                         training_rules['confidence'], 1)
                                                        fit_fn = np.poly1d(fit)
                                                        plt.plot(training_rules['lift'],
                                                                 training_rules['confidence'],
                                                                 'yo', training_rules['lift'],
                                                                 fit_fn(training_rules['lift']))
                                                        plt.xlabel('lift')
                                                        plt.ylabel('confidence')
                                                        plt.title('lift vs confidence')                                                        
                                                        mngr = plt.get_current_fig_manager()
                                                        mngr.window.setGeometry(1298, 350, 600, 550)
                                                        plt.savefig('images/apriori/' + datetime.now().strftime(
                                                            '%Y-%m-%d-%H:%M:%S.%f').replace(" ", "") + '.png')

                                                        apr_10_3_path=get_latest_image("images/apriori/",'png')          
                                                        image_apr_10_3 = PhotoImage(file=apr_10_3_path)
                                                        original_image_apr_10_3 = image_apr_10_3.subsample(3,3) # resize image using subsample

                                                        apr_10_3_im_label = Label(apr_image_frame,image=original_image_apr_10_3)
                                                        apr_10_3_im_label.image = original_image_apr_10_3 # keep a reference
                                                        apr_10_3_im_label.place(x=387, y=308)                                                         

                                                        def mouse_on_apr_10_1(event):
                                                            image_apr_10_1 = PhotoImage(file=apr_10_1_path)
                                                            original_image_apr_10_1 = image_apr_10_1.subsample(2,2) # resize image using subsample

                                                            apr_10_1_im_label = Label(apr_image_frame,image=original_image_apr_10_1)
                                                            apr_10_1_im_label.image = original_image_apr_10_1 # keep a reference
                                                            apr_10_1_im_label.place(x=387, y=118) 

                                                            return          

                                                        def mouse_on_apr_10_2(event):
                                                            image_apr_10_2 = PhotoImage(file=apr_10_2_path)
                                                            original_image_apr_10_2 = image_apr_10_2.subsample(2,2) # resize image using subsample

                                                            apr_10_2_im_label = Label(apr_image_frame,image=original_image_apr_10_2)
                                                            apr_10_2_im_label.image = original_image_apr_10_2 # keep a reference
                                                            apr_10_2_im_label.place(x=627, y=118) 

                                                            return        

                                                        def mouse_on_apr_10_3(event):
                                                            image_apr_10_3 = PhotoImage(file=apr_10_3_path)
                                                            original_image_apr_10_3 = image_apr_10_3.subsample(2,2) # resize image using subsample

                                                            apr_10_3_im_label = Label(apr_image_frame,image=original_image_apr_10_3)
                                                            apr_10_3_im_label.image = original_image_apr_10_3 # keep a reference
                                                            apr_10_3_im_label.place(x=387, y=308) 

                                                            return                                                                

                                                        apr_10_1_im_label.bind('<Enter>',mouse_on_apr_10_1)                    
                                                        apr_10_2_im_label.bind('<Enter>',mouse_on_apr_10_2)  
                                                        apr_10_3_im_label.bind('<Enter>',mouse_on_apr_10_3) 

                                                        # Taking backup values from above graphs and puting puting appropriate directory
                                                        try:
                                                            # Create target Directory
                                                            os.mkdir(dir_name)
                                                            print("Directory ", dir_name, " created.")
                                                        except FileExistsError:
                                                            print("Directory ", dir_name, " already exists.")
                                                        file = open(abs_path, 'w', encoding="utf8")
                                                        file.write(str(training_rules))
                                                        file.close()

                                                        now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                                                        now = str(now)
                                                        newname = 'apriori_' + now + '.txt'
                                                        os.rename('apriori.txt', newname)
                                                        shutil.move(newname,  "images/apriori/")

                                                        apr_10_txt_path=get_latest_image("images/apriori/",'txt')
                                                        print(apr_10_txt_path)  

                                                        def apr_10_btn_click():
                                                            window.filename =  filedialog.askopenfile(mode='r',initialdir = "images/apriori/",title = apr_10_txt_path,filetypes = (("txt files","*.txt"),("all files","*.*")))

                                                        apr_txt_entry=Entry(apr_txt_frame, highlightcolor='#ababba',justify=LEFT, relief=SUNKEN, width=18)
                                                        apr_txt_entry.insert(END,apr_10_txt_path)
                                                        apr_txt_entry.place(x=637, y=490)

                                                        apr_txt_btn=Button(apr_txt_frame, text="Browse", bd=2, activebackground='#c7c7d1',relief=SUNKEN,command=apr_10_btn_click).place(x=786, y=486)                                                         

                                                        def rst_apr():
                                                            print("Reset")
                                                            cmb.set('')
                                                            cmb1.set('')
                                                            number_of_param.set('')                                                             
                                                            new_text = " "
                                                            e1.delete(0, tk.END)
                                                            e1.insert(0, new_text)
                                                            cmb.place_forget()
                                                            cmb1.place_forget()
                                                            cmb2.place_forget()
                                                            cmb3.place_forget()
                                                            cmb4.place_forget()
                                                            cmb5.place_forget()
                                                            cmb6.place_forget()
                                                            cmb7.place_forget()
                                                            cmb8.place_forget()
                                                            cmb9.place_forget()
                                                            apr_10_1_im_label.image =''
                                                            apr_10_2_im_label.image =''
                                                            apr_10_3_im_label.image =''
                                                            apr_txt_entry.delete(0, tk.END)      
                                                            apr_txt_entry.insert(0, new_text)

                                                        plt_rst_apr=PhotoImage(file="reset.png")  
                                                        sub_plt_rst_apr=plt_rst_apr.subsample(7,7)

                                                        button_apr_rst = Button(apr_input_frame, text="Reset", fg='#026084', command=rst_apr, image=sub_plt_rst_apr, compound=LEFT, width=130)
                                                        button_apr_rst.image=sub_plt_rst_apr
                                                        button_apr_rst.place(x=88, y=484)
                                                        button_arr.append(button_apr_rst)

                                                        ttk.Separator(apr_input_frame).place(x=75, y=530, relwidth=0.29)                            

                                                        def jnt_go_to_menu():

                                                            print("Coming soon")
  
                                                            apr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                                            #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                                            lbl_apr=Label(apr_frame, width=20, bg='white').place(x=10, y=10)
   
                                                            apr_inner_frame=Frame(apr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                                            #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                                            apr_input_frame=Frame(apr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                                            apr_image_frame=Frame(apr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                                            Label(apr_image_frame,bg='white').place(x=565, y=95)

                                                            apr_txt_frame=Frame(apr_image_frame, width=250, height=195, bg='white', highlightbackground='white').place(x=627,y=388)

                                                            lbl_apr_txt=Label(apr_txt_frame, width=17, bg='white').place(x=630, y=392)                            

                                                            print("Apriori frame has been destroyed.")      

                                                        plt_up=PhotoImage(file="up.png")  
                                                        sub_plt_up=plt_up.subsample(10,10)     

                                                        button_jnt_go_to_menu=Button(apr_input_frame, text="Go to menu", fg='#026084', command=jnt_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                                        button_jnt_go_to_menu.image=sub_plt_up
                                                        button_jnt_go_to_menu.place(x=88, y=534)
                                                        button_arr.append(button_jnt_go_to_menu) 
  
                                                    # Creating a photoimage object to use image 
                                                    plt_gen_apr = PhotoImage(file = "images.png") 
                                                    sub_plt_gen_apr = plt_gen_apr.subsample(5, 5)

                                                    button_apr_gen = Button(apr_input_frame, text="Generate", fg='#026084', command=apr_gen, image=sub_plt_gen_apr, compound=LEFT)
                                                    button_apr_gen.image=sub_plt_gen_apr
                                                    button_apr_gen.place(x=88, y=424)
                                                    button_arr.append(button_apr_gen)

                                                    ttk.Separator(apr_input_frame).place(x=75, y=419, relwidth=0.29) 

                                                cmb9 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28,height=5)
                                                cmb9.place(x=75, y=388)
                                                cmb9.bind('<<ComboboxSelected>>', on_tenth_select)

                                            cmb8 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                            cmb8.place(x=75, y=365)
                                            cmb8.bind('<<ComboboxSelected>>', on_ninth_select)

                                        cmb7 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                        cmb7.place(x=75, y=342)
                                        cmb7.bind('<<ComboboxSelected>>', on_eight_select)

                                    cmb6 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                    cmb6.place(x=75, y=319)
                                    cmb6.bind('<<ComboboxSelected>>', on_seventh_select)

                                cmb5 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                                cmb5.place(x=75, y=296)
                                cmb5.bind('<<ComboboxSelected>>', on_sixth_select)

                            cmb4 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(apr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

    if show_association_rules == True:
        Number_Param_Lbl = Label(apr_input_frame, text="Number of Parameters: [2:10]", width=29,height=2,font=("Sans", 10),bd=3, relief=SUNKEN).place(x=75, y=95)
        number_of_param = ttk.Combobox(apr_input_frame, values=[2, 3, 4, 5, 6, 7, 8, 9, 10], state='readonly', width=28, height=5)
        number_of_param.place(x=75, y=136)
        number_of_param.bind('<<ComboboxSelected>>', lambda event: apriori_func(e1=number_of_param))
        labelForMenuApr = tk.Label(apr_input_frame, text="Choose apriori input values", width=29,height=1,font=("Sans", 10),bd=2, relief=SUNKEN)
        labelForMenuApr.place(x=75, y=159)

    def correlation_func(e1):
        print("Correlation func")
        print(e1.get())

        if (e1.get() == "2" or e1.get() == " 2"):
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    def cor_gen():
                        print("Corr Generation")
                        correlation_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ',
                                                       'Ծննդավայր (երկիր)', 'Ծննդավայր (քաղաք/գյուղ)',
                                                       'Ընդունման տարեթիվ', 'Առարկա', 'Առաջին միջանկյալ ստուգում',
                                                       'Երկրորդ միջանկյալ ստուգում', 'Ամփոփիչ քննություն']

                        file_path = sys.path[0] + '\\' + db

                        if not find_plathform():
                            file_path = file_path.replace("\\", "/")
                        df = pd.read_csv(file_path)[correlation_func_parameters]
                        print(column_names)

                        if (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ուսանողի անուն') or (
                                column_names[1] == 'Ֆակուլտետ' and column_names[0] == 'Ուսանողի անուն'):
                            corr_2_path="images/correlation/1/1_Fac_Name.png"

                        elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ուսանողի սեռ') or (
                                column_names[1] == 'Ֆակուլտետ' and column_names[0] == 'Ուսանողի սեռ'):    
                            corr_2_path="images/correlation/1/2_Fac_Sex.png" 

                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ծննդավայր (երկիր)') and (
                                column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ծննդավայր (երկիր)'):
                            corr_2_path="images/correlation/1/3_Fac_COB.png"                         

                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)'):
                            corr_2_path="images/correlation/1/4_Fac_CV.png" 


                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ընդունման տարեթիվ') and (
                                column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ընդունման տարեթիվ'):
                            corr_2_path="images/correlation/1/5_Fac_YOE.png"

                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Առարկա') and (
                                column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Առարկա'):
                            corr_2_path="images/correlation/1/6_Fac_Sub.png"

                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                            0] == 'Առաջին միջանկյալ ստուգում') and (
                                column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Առաջին միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/7_Fac_FrEx.png"

                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Երկրորդ միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/8_Fac_ScEx.png"

                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ամփոփիչ քննություն') and (
                                column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ամփոփիչ քննություն'):
                            corr_2_path="images/correlation/1/9_Fac_FnEx.png"

                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Ուսանողի սեռ') and (
                                column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Ուսանողի սեռ'):
                            corr_2_path="images/correlation/1/10_Name_Sex.png"

                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Ծննդավայր (երկիր)') and (
                                column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Ծննդավայր (երկիր)'):
                            corr_2_path="images/correlation/1/11_Name_COB.png"

                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                            0] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                column_names[1] == 'Ուսանողի անուն' or column_names[
                            1] == 'Ծննդավայր (քաղաք/գյուղ)'):
                            corr_2_path="images/correlation/1/12_Name_CV.png"

                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Ընդունման տարեթիվ') and (
                                column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Ընդունման տարեթիվ'):
                            corr_2_path="images/correlation/1/13_Name_YOE.png"

                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Առարկա') and (
                                column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Առարկա'):
                            corr_2_path="images/correlation/1/14_Name_Sub.png"

                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                            0] == 'Առաջին միջանկյալ ստուգում') and (
                                column_names[1] == 'Ուսանողի անուն' or column_names[
                            1] == 'Առաջին միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/15_Name_FrEx.png"

                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                column_names[1] == 'Ուսանողի անուն' or column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/16_Name_ScEx.png"

                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Ամփոփիչ քննություն') and (
                                column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Ամփոփիչ քննություն'):
                            corr_2_path="images/correlation/1/17_Name_FnEx.png"

                        elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Ծննդավայր (երկիր)') and (
                                column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Ծննդավայր (երկիր)'):
                            corr_2_path="images/correlation/1/18_Sex_COB.png"

                        elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                            0] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)'):
                            corr_2_path="images/correlation/1/18_Sex_CV.png"

                        elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Ընդունման տարեթիվ') and (
                                column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Ընդունման տարեթիվ'):
                            corr_2_path="images/correlation/1/19_Sex_YOE.png"

                        elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Առարկա') and (
                                column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Առարկա'):
                            corr_2_path="images/correlation/1/20_Sex_Sbj.png"

                        elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                            0] == 'Առաջին միջանկյալ ստուգում') and (
                                column_names[1] == 'Ուսանողի սեռ' or column_names[
                            1] == 'Առաջին միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/21_Sex_FrEx.png"

                        elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                column_names[1] == 'Ուսանողի սեռ' or column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/22_Sex_ScEx.png"

                        elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Ամփոփիչ քննություն') and (
                                column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Ամփոփիչ քննություն'):
                            corr_2_path="images/correlation/1/23_Sex_FnEx.png"

                        elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                            0] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                            1] == 'Ծննդավայր (քաղաք/գյուղ)'):
                            corr_2_path="images/correlation/1/24_COB_CV.png"

                        elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                            0] == 'Ընդունման տարեթիվ') and (
                                column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Ընդունման տարեթիվ'):
                            corr_2_path="images/correlation/1/25_COB_YOE.png"

                        elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Առարկա') and (
                                column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Առարկա'):
                            corr_2_path="images/correlation/1/26_COB_Sbj.png"

                        elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                            0] == 'Առաջին միջանկյալ ստուգում') and (
                                column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                            1] == 'Առաջին միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/27_COB_FrEx.png"

                        elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/28_COB_ScEx.png"

                        elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                            0] == 'Ամփոփիչ քննություն') and (
                                column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Ամփոփիչ քննություն'):
                            corr_2_path="images/correlation/1/29_COB_FnEx.png"

                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                            0] == 'Ընդունման տարեթիվ') and (
                                column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                            1] == 'Ընդունման տարեթիվ'):
                            corr_2_path="images/correlation/1/30_CV_YOE.png"

                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Առարկա') and (
                                column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Առարկա'):
                            corr_2_path="images/correlation/1/31_CV_Sbj.png"

                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                            0] == 'Առաջին միջանկյալ ստուգում') and (
                                column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                            1] == 'Առաջին միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/32_CV_FrEx.png"

                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/32_CV_ScEx.png"

                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                            0] == 'Ամփոփիչ քննություն') and (
                                column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                            1] == 'Ամփոփիչ քննություն'):
                            corr_2_path="images/correlation/1/33_CV_FnEx.png"
                        elif (column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա') and (
                                column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա'):
                            corr_2_path="images/correlation/1/34_YOE_Sbj.png"

                        elif (column_names[0] == 'Ընդունման տարեթիվ' or column_names[
                            0] == 'Առաջին միջանկյալ ստուգում') and (
                                column_names[1] == 'Ընդունման տարեթիվ' or column_names[
                            1] == 'Առաջին միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/35_YOE_FrEx.png"

                        elif (column_names[0] == 'Ընդունման տարեթիվ' or column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                column_names[1] == 'Ընդունման տարեթիվ' or column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/36_YOE_ScEx.png"

                        elif (column_names[0] == 'Ընդունման տարեթիվ' or column_names[
                            0] == 'Ամփոփիչ քննություն') and (
                                column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Ամփոփիչ քննություն'):
                            corr_2_path="images/correlation/1/37_YOE_FnEx.png"

                        elif (column_names[0] == 'Առարկա' or column_names[0] == 'Առաջին միջանկյալ ստուգում') and (
                                column_names[1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/38_Sbj_FrEx.png"

                        elif (column_names[0] == 'Առարկա' or column_names[0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                column_names[1] == 'Առարկա' or column_names[1] == 'Երկրորդ միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/39_Sbj_ScEx.png"

                        elif (column_names[0] == 'Առարկա' or column_names[0] == 'Ամփոփիչ քննություն') and (
                                column_names[1] == 'Առարկա' or column_names[1] == 'Ամփոփիչ քննություն'):
                            corr_2_path="images/correlation/1/40_Sbj_FnEx.png"

                        elif (column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                            0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                            1] == 'Երկրորդ միջանկյալ ստուգում'):
                            corr_2_path="images/correlation/1/41_FrEx_ScEx.png"

                        elif (column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                            0] == 'Ամփոփիչ քննություն') and (
                                column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                            1] == 'Ամփոփիչ քննություն'):
                            corr_2_path="images/correlation/1/42_FrEx_FnEx.png"

                        elif (column_names[0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                            0] == 'Ամփոփիչ քննություն') and (
                                column_names[1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                            1] == 'Ամփոփիչ քննություն'):
                            corr_2_path="images/correlation/1/43_ScEx_FnEx.png"                                                                                
      
                        image_corr_2 = PhotoImage(file=corr_2_path)
                        original_image_corr_2 = image_corr_2.subsample(3,3) # resize image using subsample

                        corr_2_im_label = Label(corr_image_frame,image=original_image_corr_2)
                        corr_2_im_label.image = original_image_corr_2 # keep a reference
                        corr_2_im_label.place(x=387, y=118)   

                        def mouse_on_corr_2(event):
                            image_corr_2 = PhotoImage(file=corr_2_path)
                            original_image_corr_2 = image_corr_2.subsample(2,2) # resize image using subsample

                            corr_2_im_label = Label(corr_image_frame,image=original_image_corr_2)
                            corr_2_im_label.image = original_image_corr_2 # keep a reference
                            corr_2_im_label.place(x=387, y=118) 

                            return                                                       

                        corr_2_im_label.bind('<Enter>',mouse_on_corr_2)                              

                        def rst_cor():
                            print("Reset")
                            cmb.set('')
                            cmb1.set('')
                            number_of_param.set('')
                            new_text = " "
                            e1.delete(0, tk.END)
                            e1.insert(0, new_text)
                            cmb.place_forget()
                            cmb1.place_forget()
                            corr_2_im_label.image =''                                                                        

                        plt_rst_corr=PhotoImage(file="reset.png")  
                        sub_plt_rst_corr=plt_rst_corr.subsample(4,4)

                        button_corr_rst = Button(corr_input_frame, text="Reset", fg='#026084', command=rst_cor, image=sub_plt_rst_corr, compound=LEFT, width=130)
                        button_corr_rst.image=sub_plt_rst_corr
                        button_corr_rst.place(x=88, y=316)
                        button_arr.append(button_corr_rst)

                        ttk.Separator(corr_input_frame).place(x=75, y=396, relwidth=0.29)

                        def corr_go_to_menu():

                            print("Coming soon")

                            corr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                            #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                            corr_apr=Label(corr_frame, width=20, bg='white').place(x=10, y=10)

                            corr_inner_frame=Frame(corr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                            #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                            corr_input_frame=Frame(corr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                            corr_image_frame=Frame(corr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                            Label(corr_image_frame, bg='white').place(x=565, y=95)                          

                            print("Correlation frame has been destroyed.")      

                        plt_up=PhotoImage(file="up.png")  
                        sub_plt_up=plt_up.subsample(4,4)     

                        button_corr_go_to_menu=Button(corr_input_frame, text="Go to menu", fg='#026084', command=corr_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                        button_corr_go_to_menu.image=sub_plt_up
                        button_corr_go_to_menu.place(x=88, y=460)
                        button_arr.append(button_corr_go_to_menu)                                               

                    # Creating a photoimage object to use image 
                    plt_gen_corr = PhotoImage(file = "images.png") 
                    sub_plt_gen_corr = plt_gen_corr.subsample(4, 4)    

                    button_corr_gen = Button(corr_input_frame, text="Generate", fg='#026084', command=cor_gen, image=sub_plt_gen_corr, compound=LEFT)
                    button_corr_gen.image=sub_plt_gen_corr
                    button_corr_gen.place(x=88, y=246)
                    button_arr.append(button_corr_gen)

                    ttk.Separator(corr_input_frame).place(x=75, y=236, relwidth=0.29)                    

                cmb1 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)   

        if (e1.get() == "3" or e1.get() == " 3"):
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        def cor_gen():
                            print("Corr Generation")
                            correlation_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ',
                                                           'Ծննդավայր (երկիր)', 'Ծննդավայր (քաղաք/գյուղ)',
                                                           'Ընդունման տարեթիվ', 'Առարկա',
                                                           'Առաջին միջանկյալ ստուգում',
                                                           'Երկրորդ միջանկյալ ստուգում', 'Ամփոփիչ քննություն']

                            file_path = sys.path[0] + '\\' + db

                            if not find_plathform():
                                file_path = file_path.replace("\\", "/")
                            df = pd.read_csv(file_path)[correlation_func_parameters]

                            if (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ուսանողի սեռ' and
                                column_names[
                                    2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Ֆակուլտետ'):
                                corr_3_path="images/correlation/2/1_Fac_Sex_Name.png"  


                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                  column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ուսանողի սեռ'):

                                corr_3_path="images/correlation/2/2_Sex_COB_CV.png"  

                            elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                corr_3_path="images/correlation/2/3_CV_YOE_Sbj.png" 


                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ուսանողի սեռ' and
                                  column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Ուսանողի անուն'):
                                corr_3_path="images/correlation/2/4_Name_Sex_COB.png"

                            elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ծննդավայր (երկիր)'):
                                corr_3_path="images/correlation/2/5_COB_CV_YOE.png"

                            elif (column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                  column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ընդունման տարեթիվ'):
                                corr_3_path="images/correlation/2/6_YOE_Sbj_FrEx.png"

                            elif (column_names[0] == 'Առարկա' and column_names[1] == 'Առաջին միջանկյալ ստուգում' and
                                  column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա'):
                                corr_3_path="images/correlation/2/7_Sbj_FrEx_ScEx.png"

                            elif (column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                        2] == 'Երկրորդ միջանկյալ ստուգում'):
                                corr_3_path="images/correlation/2/8_FrEx_ScEx_FnEx.png"

                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ուսանողի սեռ' and
                                  column_names[
                                      2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Ֆակուլտետ'):
                                corr_3_path="images/correlation/2/9_Fac_Sex_COB.png"


                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                  column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ֆակուլտետ'):
                                corr_3_path="images/correlation/2/10_Fac_COB_CV.png"


                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and
                                  column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ֆակուլտետ'):
                                corr_3_path="images/correlation/2/11_Fac_CV_YOE.png"


                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ընդունման տարեթիվ' and
                                  column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Առարկա' and column_names[
                                2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Ֆակուլտետ' and
                                    column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ֆակուլտետ' and column_names[
                                2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ֆակուլտետ'):
                                corr_3_path="images/correlation/2/12_Fac_YOE_Sbj.png"


                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Առարկա' and column_names[
                                2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ֆակուլտետ' and column_names[
                                2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ֆակուլտետ' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ֆակուլտետ'):
                                corr_3_path="images/correlation/2/13_Fac_Sbj_FrEx.png"

                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                  column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ֆակուլտետ' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ֆակուլտետ' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ֆակուլտետ'):
                                corr_3_path="images/correlation/2/14_Fac_FrEx_ScEx.png"


                            elif (column_names[0] == 'Ֆակուլտետ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and
                                  column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ֆակուլտետ' and column_names[1] == 'Ամփոփիչ քննություն' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ֆակուլտետ' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ֆակուլտետ') or (
                                    column_names[0] == 'Ամփոփիչ քննությունal_Exam' and column_names[
                                1] == 'Ֆակուլտետ' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ֆակուլտետ'):
                                corr_3_path="images/correlation/2/15_Fac_ScEx_FnEx.png"


                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                  column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ուսանողի անուն'):
                                corr_3_path="images/correlation/2/16_Name_COB_CV.png"


                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ուսանողի անուն'):
                                corr_3_path="images/correlation/2/17_Name_CV_YOE.png"


                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Ընդունման տարեթիվ' and
                                  column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ուսանողի անուն'):
                                corr_3_path="images/correlation/2/18_Name_YOE_Sbj.png"


                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[1] == 'Առարկա' and
                                  column_names[
                                      2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ուսանողի անուն'):
                                corr_3_path="images/correlation/2/19_Name_Sbj_FrEx.png"


                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                      2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի անուն'):
                                corr_3_path="images/correlation/2/20_Name_FrEx_ScEx.png"


                            elif (column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ուսանողի անուն' and column_names[
                                1] == 'Ամփոփիչ քննություն' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի անուն' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ուսանողի անուն') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Ուսանողի անուն' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի անուն'):
                                corr_3_path="images/correlation/2/21_Name_ScEx_FnEx.png"


                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and
                                  column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ուսանողի սեռ'):
                                corr_3_path="images/correlation/2/22_Sex_CV_YOE.png"


                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Ընդունման տարեթիվ' and
                                  column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Առարկա' and
                                    column_names[
                                        2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[
                                        2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ուսանողի սեռ'):
                                corr_3_path="images/correlation/2/23_Sex_YOE_Sbj.png"



                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[1] == 'Առարկա' and
                                  column_names[
                                      2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ուսանողի սեռ' and
                                    column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ուսանողի սեռ'):
                                corr_3_path="images/correlation/2/24_Sex_Sbj_FrEx.png"


                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                      2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի սեռ'):
                                corr_3_path="images/correlation/2/25_Sex_FrEx_ScEx.png"



                            elif (column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ուսանողի սեռ' and column_names[
                                1] == 'Ամփոփիչ քննություն' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ուսանողի սեռ' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ուսանողի սեռ') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Ուսանողի սեռ' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ուսանողի սեռ'):
                                corr_3_path="images/correlation/2/26_Sex_ScEx_FnEx.png"


                            elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ընդունման տարեթիվ' and
                                  column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ընդունման տարեթիվ' and
                                    column_names[2] == 'Ծննդավայր (երկիր)'):
                                corr_3_path="images/correlation/2/27_COB_YOE_Sbj.png"


                            elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[1] == 'Առարկա' and
                                  column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ծննդավայր (երկիր)' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ծննդավայր (երկիր)'):
                                corr_3_path="images/correlation/2/28_COB_Sbj_FrEx.png"


                            elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                      2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ծննդավայր (երկիր)'):
                                corr_3_path="images/correlation/2/29_COB_FrEx_ScEx.png"


                            elif (column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ծննդավայր (երկիր)' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ծննդավայր (երկիր)') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Ծննդավայր (երկիր)' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ծննդավայր (երկիր)'):
                                corr_3_path="images/correlation/2/30_COB_ScEx_FnEx.png"


                            elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[1] == 'Առարկա' and
                                  column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' and
                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առարկա' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                corr_3_path="images/correlation/2/31_CV_Sbj_FrEx.png"


                            elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                      2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                        2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                corr_3_path="images/correlation/2/32_CV_FrEx_ScEx.png"

                            elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Ծննդավայր (քաղաք/գյուղ)' and column_names[
                                        2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                corr_3_path="images/correlation/2/33_CV_ScEx_FnEx.png"


                            elif (column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                      2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                        2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Առաջին միջանկյալ ստուգում' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Առաջին միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առաջին միջանկյալ ստուգում' and column_names[2] == 'Ընդունման տարեթիվ'):
                                corr_3_path="images/correlation/2/34_YOE_FrEx_ScEx.png"


                            elif (column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Ընդունման տարեթիվ' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Ընդունման տարեթիվ') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Ընդունման տարեթիվ' and column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Ընդունման տարեթիվ'):
                                corr_3_path="images/correlation/2/35_YOE_ScEx_FnEx.png"


                            elif (column_names[0] == 'Առարկա' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and
                                  column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Առարկա' and column_names[1] == 'Ամփոփիչ քննություն' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Առարկա' and
                                    column_names[2] == 'Ամփոփիչ քննություն') or (
                                    column_names[0] == 'Երկրորդ միջանկյալ ստուգում' and column_names[
                                1] == 'Ամփոփիչ քննություն' and column_names[2] == 'Առարկա') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[1] == 'Առարկա' and
                                    column_names[2] == 'Երկրորդ միջանկյալ ստուգում') or (
                                    column_names[0] == 'Ամփոփիչ քննություն' and column_names[
                                1] == 'Երկրորդ միջանկյալ ստուգում' and column_names[2] == 'Առարկա'):
                                corr_3_path="images/correlation/2/36_Sbj_ScEx_FnEx.png"


                            image_corr_3 = PhotoImage(file=corr_3_path)
                            original_image_corr_3 = image_corr_3.subsample(3,3) # resize image using subsample

                            corr_3_im_label = Label(corr_image_frame,image=original_image_corr_3)
                            corr_3_im_label.image = original_image_corr_3 # keep a reference
                            corr_3_im_label.place(x=387, y=118)   

                            def mouse_on_corr_3(event):
                                image_corr_3 = PhotoImage(file=corr_3_path)
                                original_image_corr_3 = image_corr_3.subsample(2,2) # resize image using subsample

                                corr_3_im_label = Label(corr_image_frame,image=original_image_corr_3)
                                corr_3_im_label.image = original_image_corr_3 # keep a reference
                                corr_3_im_label.place(x=387, y=118) 

                                return                                                       

                            corr_3_im_label.bind('<Enter>',mouse_on_corr_3)                              

                            def rst_cor():
                                print("Reset")
                                cmb.set('')
                                cmb1.set('')
                                cmb2.set('')                                
                                number_of_param.set('')
                                new_text = " "
                                e1.delete(0, tk.END)
                                e1.insert(0, new_text)
                                cmb.place_forget()
                                cmb1.place_forget()
                                cmb2.place_forget()                                
                                corr_3_im_label.image =''                                                                        

                            plt_rst_corr=PhotoImage(file="reset.png")  
                            sub_plt_rst_corr=plt_rst_corr.subsample(4,4)

                            button_corr_rst = Button(corr_input_frame, text="Reset", fg='#026084', command=rst_cor, image=sub_plt_rst_corr, compound=LEFT, width=130)
                            button_corr_rst.image=sub_plt_rst_corr
                            button_corr_rst.place(x=88, y=339)
                            button_arr.append(button_corr_rst)

                            ttk.Separator(corr_input_frame).place(x=75, y=419, relwidth=0.29)

                            def corr_go_to_menu():

                                print("Coming soon")

                                corr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                corr_apr=Label(corr_frame, width=20, bg='white').place(x=10, y=10)

                                corr_inner_frame=Frame(corr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                corr_input_frame=Frame(corr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                corr_image_frame=Frame(corr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                Label(corr_image_frame, bg='white').place(x=565, y=95)                          

                                print("Correlation frame has been destroyed.")      

                            plt_up=PhotoImage(file="up.png")  
                            sub_plt_up=plt_up.subsample(4,4)     

                            button_corr_go_to_menu=Button(corr_input_frame, text="Go to menu", fg='#026084', command=corr_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                            button_corr_go_to_menu.image=sub_plt_up
                            button_corr_go_to_menu.place(x=88, y=483)
                            button_arr.append(button_corr_go_to_menu) 

                        # Creating a photoimage object to use image 
                        plt_gen_corr = PhotoImage(file = "images.png") 
                        sub_plt_gen_corr = plt_gen_corr.subsample(4, 4)    

                        button_corr_gen = Button(corr_input_frame, text="Generate", fg='#026084', command=cor_gen, image=sub_plt_gen_corr, compound=LEFT)
                        button_corr_gen.image=sub_plt_gen_corr
                        button_corr_gen.place(x=88, y=269)
                        button_arr.append(button_corr_gen)                        

                        ttk.Separator(corr_input_frame).place(x=75, y=259, relwidth=0.29)

                    cmb2 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        if (e1.get() == "4" or e1.get() == " 4"):
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            def cor_gen():
                                print("Corr Generation")
                                correlation_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ',
                                                               'Ծննդավայր (երկիր)', 'Ծննդավայր (քաղաք/գյուղ)',
                                                               'Ընդունման տարեթիվ', 'Առարկա',
                                                               'Առաջին միջանկյալ ստուգում',
                                                               'Երկրորդ միջանկյալ ստուգում', 'Ամփոփիչ քննություն']

                                file_path = sys.path[0] + '\\' + db

                                if not find_plathform():
                                    file_path = file_path.replace("\\", "/")
                                df = pd.read_csv(file_path)[correlation_func_parameters]
                                print(column_names)

                                if (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի անուն' or
                                    column_names[0] == 'Ուսանողի սեռ' or column_names[
                                        0] == 'Ծննդավայր (երկիր)') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ուսանողի անուն' or
                                        column_names[1] == 'Ուսանողի սեռ' or column_names[
                                            1] == 'Ծննդավայր (երկիր)') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ուսանողի անուն' or
                                        column_names[2] == 'Ուսանողի սեռ' or column_names[
                                            2] == 'Ծննդավայր (երկիր)') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ուսանողի անուն' or
                                        column_names[3] == 'Ուսանողի սեռ' or column_names[
                                            3] == 'Ծննդավայր (երկիր)'):
                                    corr_4_path="images/correlation/3/1_Fac_Name_Sex_COB.png"


                                elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                    0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա') and (
                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա') and (
                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա') and (
                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա'):
                                    corr_4_path="images/correlation/3/2_COB_CV_YOE_Sbj.png"

                                elif (column_names[0] == 'Առարկա' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or
                                      column_names[0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Առարկա' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or
                                        column_names[1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Առարկա' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or
                                        column_names[2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Առարկա' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or
                                        column_names[3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    corr_4_path="images/correlation/3/3_Sbj_FrEx_ScEx_FnEx.png"


                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի սեռ' or
                                      column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                          0] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ուսանողի սեռ' or
                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                            1] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ուսանողի սեռ' or
                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                            2] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ուսանողի սեռ' or
                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                            3] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                    corr_4_path="images/correlation/3/4_Fac_Sex_COB_CV.png"

                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ծննդավայր (երկիր)' or
                                      column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                          0] == 'Ընդունման տարեթիվ') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ծննդավայր (երկիր)' or
                                        column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            1] == 'Ընդունման տարեթիվ') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ծննդավայր (երկիր)' or
                                        column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            2] == 'Ընդունման տարեթիվ') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ծննդավայր (երկիր)' or
                                        column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            3] == 'Ընդունման տարեթիվ'):
                                    corr_4_path="images/correlation/3/5_Fac_COB_CV_YOE.png"


                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                    0] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                      column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[
                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[
                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[
                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա'):
                                    corr_4_path="images/correlation/3/6_Fac_CV_YOE_Sbj.png"


                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա' or column_names[
                                          0] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա' or column_names[
                                            1] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա' or column_names[
                                            2] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա' or column_names[
                                            3] == 'Առաջին միջանկյալ ստուգում'):
                                    corr_4_path="images/correlation/3/7_Fac_YOE_Sbj_FrEx.png"


                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Առարկա' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Առարկա' or
                                        column_names[
                                            1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Առարկա' or
                                        column_names[
                                            2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Առարկա' or
                                        column_names[
                                            3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում'):
                                    corr_4_path="images/correlation/3/8_Fac_Sbj_FrEx_ScEx.png"

                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ֆակուլտետ' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ֆակուլտետ' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ֆակուլտետ' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    corr_4_path="images/correlation/3/9_Fac_FrEx_ScEx_FnEx.png"


                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                    0] == 'Ծննդավայր (երկիր)' or
                                      column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                          0] == 'Ընդունման տարեթիվ') and (
                                        column_names[1] == 'Ուսանողի անուն' or column_names[
                                    1] == 'Ծննդավայր (երկիր)' or
                                        column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            1] == 'Ընդունման տարեթիվ') and (
                                        column_names[2] == 'Ուսանողի անուն' or column_names[
                                    2] == 'Ծննդավայր (երկիր)' or
                                        column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            2] == 'Ընդունման տարեթիվ') and (
                                        column_names[3] == 'Ուսանողի անուն' or column_names[
                                    3] == 'Ծննդավայր (երկիր)' or
                                        column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                            3] == 'Ընդունման տարեթիվ'):
                                    corr_4_path="images/correlation/3/10_Name_COB_CV_YOE.png"


                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                    0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա') and (
                                        column_names[1] == 'Ուսանողի անուն' or column_names[
                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա') and (
                                        column_names[2] == 'Ուսանողի անուն' or column_names[
                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա') and (
                                        column_names[3] == 'Ուսանողի անուն' or column_names[
                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա'):
                                    corr_4_path="images/correlation/3/11_Name_CV_YOE_Sbj.png"


                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                    0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա' or column_names[
                                          0] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ուսանողի անուն' or column_names[
                                    1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա' or column_names[
                                            1] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ուսանողի անուն' or column_names[
                                    2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա' or column_names[
                                            2] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ուսանողի անուն' or column_names[
                                    3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա' or column_names[
                                            3] == 'Առաջին միջանկյալ ստուգում'):
                                    corr_4_path="images/correlation/3/12_Name_YOE_Sbj_FrEx.png"


                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Առարկա' or
                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Առարկա' or
                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ուսանողի անուն' or column_names[2] == 'Առարկա' or
                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ուսանողի անուն' or column_names[3] == 'Առարկա' or
                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում'):
                                    corr_4_path="images/correlation/3/13_Name_Sbj_FrEx_ScEx.png"

                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ուսանողի անուն' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ուսանողի անուն' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ուսանողի անուն' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    corr_4_path="images/correlation/3/14_Name_FrEx_ScEx_FnEx.png"


                                elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                    0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա') and (
                                        column_names[1] == 'Ուսանողի սեռ' or column_names[
                                    1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա') and (
                                        column_names[2] == 'Ուսանողի սեռ' or column_names[
                                    2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա') and (
                                        column_names[3] == 'Ուսանողի սեռ' or column_names[
                                    3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա'):
                                    corr_4_path="images/correlation/3/15_Sex_CV_YOE_Sbj.png"

                                elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Ընդունման տարեթիվ' or
                                      column_names[0] == 'Առարկա' or column_names[
                                          0] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ուսանողի սեռ' or column_names[
                                    1] == 'Ընդունման տարեթիվ' or
                                        column_names[1] == 'Առարկա' or column_names[
                                            1] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ուսանողի սեռ' or column_names[
                                    2] == 'Ընդունման տարեթիվ' or
                                        column_names[2] == 'Առարկա' or column_names[
                                            2] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ուսանողի սեռ' or column_names[
                                    3] == 'Ընդունման տարեթիվ' or
                                        column_names[3] == 'Առարկա' or column_names[
                                            3] == 'Առաջին միջանկյալ ստուգում'):
                                    corr_4_path="images/correlation/3/16_Sex_YOE_Sbj_FrEx.png"


                                elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Առարկա' or
                                      column_names[
                                          0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Առարկա' or
                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ուսանողի սեռ' or column_names[2] == 'Առարկա' or
                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ուսանողի սեռ' or column_names[3] == 'Առարկա' or
                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում'):
                                    corr_4_path="images/correlation/3/17_Sex_Sbj_FrEx_ScEx.png"


                                elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ուսանողի սեռ' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ուսանողի սեռ' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ուսանողի սեռ' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    corr_4_path="images/correlation/3/18_Sex_FrEx_ScEx_FnEx.png"


                                elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                    0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[
                                          0] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                    1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[
                                            1] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                    2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[
                                            2] == 'Առաջին միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                    3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[
                                            3] == 'Առաջին միջանկյալ ստուգում'):
                                    corr_4_path="images/correlation/3/19_COB_YOE_Sbj_FrEx.png"


                                elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Առարկա' or
                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Առարկա' or
                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[2] == 'Առարկա' or
                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[3] == 'Առարկա' or
                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում'):
                                    corr_4_path="images/correlation/3/20_COB_Sbj_FrEx_ScEx.png"


                                elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    corr_4_path="images/correlation/3/21_COB_FrEx_ScEx_FnEx.png"


                                elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Առարկա' or
                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    1] == 'Առարկա' or
                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    2] == 'Առարկա' or
                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                        column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    3] == 'Առարկա' or
                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում'):
                                    corr_4_path="images/correlation/3/22_CV_Sbj_FrEx_ScEx.png"


                                elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    corr_4_path="images/correlation/3/23_CV_FrEx_ScEx_FnEx.png"


                                elif (column_names[0] == 'Ընդունման տարեթիվ' or column_names[
                                    0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                          0] == 'Ամփոփիչ քննություն') and (
                                        column_names[1] == 'Ընդունման տարեթիվ' or column_names[
                                    1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            1] == 'Ամփոփիչ քննություն') and (
                                        column_names[2] == 'Ընդունման տարեթիվ' or column_names[
                                    2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            2] == 'Ամփոփիչ քննություն') and (
                                        column_names[3] == 'Ընդունման տարեթիվ' or column_names[
                                    3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                            3] == 'Ամփոփիչ քննություն'):
                                    corr_4_path="images/correlation/3/24_YOE_FrEx_ScEx_FnEx.png"

                                image_corr_4 = PhotoImage(file=corr_4_path)
                                original_image_corr_4 = image_corr_4.subsample(3,3) # resize image using subsample

                                corr_4_im_label = Label(corr_image_frame,image=original_image_corr_4)
                                corr_4_im_label.image = original_image_corr_4 # keep a reference
                                corr_4_im_label.place(x=387, y=118)   

                                def mouse_on_corr_4(event):
                                    image_corr_4 = PhotoImage(file=corr_4_path)
                                    original_image_corr_4 = image_corr_4.subsample(2,2) # resize image using subsample

                                    corr_4_im_label = Label(corr_image_frame,image=original_image_corr_4)
                                    corr_4_im_label.image = original_image_corr_4 # keep a reference
                                    corr_4_im_label.place(x=387, y=118) 

                                    return                                                       

                                corr_4_im_label.bind('<Enter>',mouse_on_corr_4)                              

                                def rst_cor():
                                    print("Reset")
                                    cmb.set('')
                                    cmb1.set('')
                                    cmb2.set('')        
                                    cmb3.set('')                                                             
                                    number_of_param.set('')
                                    new_text = " "
                                    e1.delete(0, tk.END)
                                    e1.insert(0, new_text)
                                    cmb.place_forget()
                                    cmb1.place_forget()
                                    cmb2.place_forget()       
                                    cmb3.place_forget()                                                               
                                    corr_4_im_label.image =''                                                                        

                                plt_rst_corr=PhotoImage(file="reset.png")  
                                sub_plt_rst_corr=plt_rst_corr.subsample(4,4)

                                button_corr_rst = Button(corr_input_frame, text="Reset", fg='#026084', command=rst_cor, image=sub_plt_rst_corr, compound=LEFT, width=130)
                                button_corr_rst.image=sub_plt_rst_corr
                                button_corr_rst.place(x=88, y=362)
                                button_arr.append(button_corr_rst)

                                ttk.Separator(corr_input_frame).place(x=75, y=442, relwidth=0.29)

                                def corr_go_to_menu():

                                    print("Coming soon")

                                    corr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                    #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                    corr_apr=Label(corr_frame, width=20, bg='white').place(x=10, y=10)

                                    corr_inner_frame=Frame(corr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                    #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                    corr_input_frame=Frame(corr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                    corr_image_frame=Frame(corr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                    Label(corr_image_frame, bg='white').place(x=565, y=95)                          

                                    print("Correlation frame has been destroyed.")      

                                plt_up=PhotoImage(file="up.png")  
                                sub_plt_up=plt_up.subsample(4,4)     

                                button_corr_go_to_menu=Button(corr_input_frame, text="Go to menu", fg='#026084', command=corr_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                button_corr_go_to_menu.image=sub_plt_up
                                button_corr_go_to_menu.place(x=88, y=486)
                                button_arr.append(button_corr_go_to_menu)                                             

                            # Creating a photoimage object to use image 
                            plt_gen_corr = PhotoImage(file = "images.png") 
                            sub_plt_gen_corr = plt_gen_corr.subsample(4, 4)    

                            button_corr_gen = Button(corr_input_frame, text="Generate", fg='#026084', command=cor_gen, image=sub_plt_gen_corr, compound=LEFT)
                            button_corr_gen.image=sub_plt_gen_corr
                            button_corr_gen.place(x=88, y=292)
                            button_arr.append(button_corr_gen) 

                            ttk.Separator(corr_input_frame).place(x=75, y=282, relwidth=0.29)

                        cmb3 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)   

        if (e1.get() == "5" or e1.get() == " 5"):
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):
                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                def cor_gen():
                                    print("Corr Generation")
                                    correlation_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ',
                                                                   'Ծննդավայր (երկիր)', 'Ծննդավայր (քաղաք/գյուղ)',
                                                                   'Ընդունման տարեթիվ', 'Առարկա',
                                                                   'Առաջին միջանկյալ ստուգում',
                                                                   'Երկրորդ միջանկյալ ստուգում',
                                                                   'Ամփոփիչ քննություն']

                                    file_path = sys.path[0] + '\\' + db

                                    if not find_plathform():
                                        file_path = file_path.replace("\\", "/")
                                    df = pd.read_csv(file_path)[correlation_func_parameters]
                                    print(column_names)

                                    if (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի անուն' or
                                        column_names[0] == 'Ուսանողի սեռ' or column_names[
                                            0] == 'Ծննդավայր (երկիր)' or
                                        column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ուսանողի անուն' or
                                            column_names[1] == 'Ուսանողի սեռ' or column_names[
                                                1] == 'Ծննդավայր (երկիր)' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ուսանողի անուն' or
                                            column_names[2] == 'Ուսանողի սեռ' or column_names[
                                                2] == 'Ծննդավայր (երկիր)' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ուսանողի անուն' or
                                            column_names[3] == 'Ուսանողի սեռ' or column_names[
                                                3] == 'Ծննդավայր (երկիր)' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[4] == 'Ուսանողի անուն' or
                                            column_names[4] == 'Ուսանողի սեռ' or column_names[
                                                4] == 'Ծննդավայր (երկիր)' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)'):
                                        corr_5_path="images/correlation/4/1_Fac_Name_Sex_COB_CV.png" 


                                    elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում'):
                                        corr_5_path="images/correlation/4/2_CV_YOE_Sbj_FrEx_ScEx.png" 


                                    elif (column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                          column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                            column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                            column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                2] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                            column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                            column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                4] == 'Ամփոփիչ քննություն'):
                                        corr_5_path="images/correlation/4/3_YOE_Sbj_FrEx_ScEx_FnEx.png"


                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի սեռ' or
                                          column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                              0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                              0] == 'Ընդունման տարեթիվ') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ուսանողի սեռ' or
                                            column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                1] == 'Ընդունման տարեթիվ') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ուսանողի սեռ' or
                                            column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                2] == 'Ընդունման տարեթիվ') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ուսանողի սեռ' or
                                            column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                3] == 'Ընդունման տարեթիվ') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[4] == 'Ուսանողի սեռ' or
                                            column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                4] == 'Ընդունման տարեթիվ'):
                                        corr_5_path="images/correlation/4/4_Fac_Sex_COB_CV_YOE.png"


                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                        0] == 'Ծննդավայր (երկիր)' or
                                          column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                              0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[
                                        1] == 'Ծննդավայր (երկիր)' or
                                            column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[
                                        2] == 'Ծննդավայր (երկիր)' or
                                            column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[
                                        3] == 'Ծննդավայր (երկիր)' or
                                            column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[
                                        4] == 'Ծննդավայր (երկիր)' or
                                            column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա'):
                                        corr_5_path="images/correlation/4/5_Fac_COB_CV_YOE_Sbj.png"


                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                        0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                          column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[
                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                            column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[
                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                            column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[
                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                            column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[
                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or
                                            column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում'):
                                        corr_5_path="images/correlation/4/6_Fac_CV_YOE_Sbj_FrEx.png"


                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                        0] == 'Ընդունման տարեթիվ' or
                                          column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[
                                        1] == 'Ընդունման տարեթիվ' or
                                            column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[
                                        2] == 'Ընդունման տարեթիվ' or
                                            column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[
                                        3] == 'Ընդունման տարեթիվ' or
                                            column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[
                                        4] == 'Ընդունման տարեթիվ' or
                                            column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում'):
                                        corr_5_path="images/correlation/4/7_Fac_YOE_Sbj_FrEx_ScEx.png"


                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Առարկա' or
                                          column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Առարկա' or
                                            column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Առարկա' or
                                            column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                2] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Առարկա' or
                                            column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ֆակուլտետ' or column_names[4] == 'Առարկա' or
                                            column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                4] == 'Ամփոփիչ քննություն'):
                                        corr_5_path="images/correlation/4/8_Fac_Sbj_FrEx_ScEx_FnEx.png"


                                    elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                        0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                          column_names[0] == 'Ընդունման տարեթիվ' or column_names[
                                              0] == 'Առարկա') and (
                                            column_names[1] == 'Ուսանողի անուն' or column_names[
                                        1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                            column_names[1] == 'Ընդունման տարեթիվ' or column_names[
                                                1] == 'Առարկա') and (
                                            column_names[2] == 'Ուսանողի անուն' or column_names[
                                        2] == 'Ծննդավայր (երկիր)' or column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                            column_names[2] == 'Ընդունման տարեթիվ' or column_names[
                                                2] == 'Առարկա') and (
                                            column_names[3] == 'Ուսանողի անուն' or column_names[
                                        3] == 'Ծննդավայր (երկիր)' or column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                            column_names[3] == 'Ընդունման տարեթիվ' or column_names[
                                                3] == 'Առարկա') and (
                                            column_names[4] == 'Ուսանողի անուն' or column_names[
                                        4] == 'Ծննդավայր (երկիր)' or column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                            column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա'):
                                        corr_5_path="images/correlation/4/9_Name_COB_CV_YOE_Sbj.png"


                                    elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                        0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                          column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ուսանողի անուն' or column_names[
                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                            column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ուսանողի անուն' or column_names[
                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                            column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ուսանողի անուն' or column_names[
                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                            column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ուսանողի անուն' or column_names[
                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or
                                            column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում'):
                                        corr_5_path="images/correlation/4/10_Name_CV_YOE_Sbj_FrEx.png"


                                    elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                        0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ուսանողի անուն' or column_names[
                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ուսանողի անուն' or column_names[
                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ուսանողի անուն' or column_names[
                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ուսանողի անուն' or column_names[
                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում'):
                                        corr_5_path="images/correlation/4/11_Name_YOE_Sbj_FrEx_ScEx.png"


                                    elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Առարկա' or
                                          column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Առարկա' or
                                            column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ուսանողի անուն' or column_names[2] == 'Առարկա' or
                                            column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                2] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ուսանողի անուն' or column_names[3] == 'Առարկա' or
                                            column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ուսանողի անուն' or column_names[4] == 'Առարկա' or
                                            column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                             4] == 'Ամփոփիչ քննություն'):
                                        corr_5_path="images/correlation/4/12_Name_Sbj_FrEx_ScEx_FnEx.png"                                                  



                                    elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                        0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or
                                          column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ուսանողի սեռ' or column_names[
                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or
                                            column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ուսանողի սեռ' or column_names[
                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or
                                            column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ուսանողի սեռ' or column_names[
                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or
                                            column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ուսանողի սեռ' or column_names[
                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or
                                            column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում'):
                                        corr_5_path="images/correlation/4/13_Sex_CV_YOE_Sbj_FrEx.png" 


                                    elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                        0] == 'Ընդունման տարեթիվ' or
                                          column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ուսանողի սեռ' or column_names[
                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ուսանողի սեռ' or column_names[
                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ուսանողի սեռ' or column_names[
                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ուսանողի սեռ' or column_names[
                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում'):

                                        corr_5_path="images/correlation/4/14_Sex_YOE_Sbj_FrEx_ScEx.png" 

                                    elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Առարկա' or
                                          column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Առարկա' or
                                            column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ուսանողի սեռ' or column_names[2] == 'Առարկա' or
                                            column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                2] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ուսանողի սեռ' or column_names[3] == 'Առարկա' or
                                            column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ուսանողի սեռ' or column_names[4] == 'Առարկա' or
                                            column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                4] == 'Ամփոփիչ քննություն'):

                                        corr_5_path="images/correlation/4/15_Sex_Sbj_FrEx_ScEx_FnEx.png" 


                                    elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                        0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[
                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[
                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[
                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[
                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                            column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[
                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում'):
                                        corr_5_path="images/correlation/4/16_COB_YOE_Sbj_FrEx_ScEx.png" 



                                    elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Առարկա' or
                                          column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Առարկա' or
                                            column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ծննդավայր (երկիր)' or column_names[2] == 'Առարկա' or
                                            column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ծննդավայր (երկիր)' or column_names[3] == 'Առարկա' or
                                            column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ծննդավայր (երկիր)' or column_names[4] == 'Առարկա' or
                                            column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                4] == 'Ամփոփիչ քննություն'):
                                        corr_5_path="images/correlation/4/17_COB_Sbj_FrEx_ScEx_FnEx.png"



                                    elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        0] == 'Առարկա' or
                                          column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                              0] == 'Ամփոփիչ քննություն') and (
                                            column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում' or
                                            column_names[1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                1] == 'Ամփոփիչ քննություն') and (
                                            column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում' or
                                            column_names[2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                2] == 'Ամփոփիչ քննություն') and (
                                            column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում' or
                                            column_names[3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                3] == 'Ամփոփիչ քննություն') and (
                                            column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                        4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում' or
                                            column_names[4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                4] == 'Ամփոփիչ քննություն'):
                                               
                                        corr_5_path="images/correlation/4/18_CV_Sbj_FrEx_ScEx_FnEx.png"


                                    image_corr_5 = PhotoImage(file=corr_5_path)
                                    original_image_corr_5 = image_corr_5.subsample(3,3) # resize image using subsample

                                    corr_5_im_label = Label(corr_image_frame,image=original_image_corr_5)
                                    corr_5_im_label.image = original_image_corr_5 # keep a reference
                                    corr_5_im_label.place(x=387, y=118)   

                                    def mouse_on_corr_5(event):
                                        image_corr_5 = PhotoImage(file=corr_5_path)
                                        original_image_corr_5 = image_corr_5.subsample(2,2) # resize image using subsample

                                        corr_5_im_label = Label(corr_image_frame,image=original_image_corr_5)
                                        corr_5_im_label.image = original_image_corr_5 # keep a reference
                                        corr_5_im_label.place(x=387, y=118) 

                                        return                                                       

                                    corr_5_im_label.bind('<Enter>',mouse_on_corr_5)                              

                                    def rst_cor():
                                        print("Reset")
                                        cmb.set('')
                                        cmb1.set('')
                                        cmb2.set('')        
                                        cmb3.set('')        
                                        cmb4.set('')                                                                                               
                                        number_of_param.set('')
                                        new_text = " "
                                        e1.delete(0, tk.END)
                                        e1.insert(0, new_text)
                                        cmb.place_forget()
                                        cmb1.place_forget()
                                        cmb2.place_forget()       
                                        cmb3.place_forget() 
                                        cmb4.place_forget()                                                                                                       
                                        corr_5_im_label.image =''                                                                        

                                    plt_rst_corr=PhotoImage(file="reset.png")  
                                    sub_plt_rst_corr=plt_rst_corr.subsample(4,4)

                                    button_corr_rst = Button(corr_input_frame, text="Reset", fg='#026084', command=rst_cor, image=sub_plt_rst_corr, compound=LEFT, width=130)
                                    button_corr_rst.image=sub_plt_rst_corr
                                    button_corr_rst.place(x=88, y=384)
                                    button_arr.append(button_corr_rst)

                                    ttk.Separator(corr_input_frame).place(x=75, y=464, relwidth=0.29)

                                    def corr_go_to_menu():

                                        print("Coming soon")

                                        corr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                        #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                        corr_apr=Label(corr_frame, width=20, bg='white').place(x=10, y=10)

                                        corr_inner_frame=Frame(corr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                        #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                        corr_input_frame=Frame(corr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                        corr_image_frame=Frame(corr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                        Label(corr_image_frame, bg='white').place(x=565, y=95)                          

                                        print("Correlation frame has been destroyed.")      

                                    plt_up=PhotoImage(file="up.png")  
                                    sub_plt_up=plt_up.subsample(4,4)     

                                    button_corr_go_to_menu=Button(corr_input_frame, text="Go to menu", fg='#026084', command=corr_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                    button_corr_go_to_menu.image=sub_plt_up
                                    button_corr_go_to_menu.place(x=88, y=498)
                                    button_arr.append(button_corr_go_to_menu)  

                                # Creating a photoimage object to use image 
                                plt_gen_corr = PhotoImage(file = "images.png") 
                                sub_plt_gen_corr = plt_gen_corr.subsample(4, 4)    

                                button_corr_gen = Button(corr_input_frame, text="Generate", fg='#026084', command=cor_gen, image=sub_plt_gen_corr, compound=LEFT)
                                button_corr_gen.image=sub_plt_gen_corr
                                button_corr_gen.place(x=88, y=314)
                                button_arr.append(button_corr_gen) 

                                ttk.Separator(corr_input_frame).place(x=75, y=304, relwidth=0.29)

                            cmb4 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        if(e1.get()=="6" or e1.get()==" 6"):
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val) 

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)
                
                def on_second_select(event=None):
                    second_curr_val = cmb1.get()
                
                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)
                    
                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                
                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)
      
                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()
                
                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):
                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                sixth_data = fifth_data

                                for item in fifth_data:
                                    if item == fifth_curr_val:
                                        sixth_data.remove(item)

                                def on_sixth_select(event=None):
                                    sixth_curr_val = cmb5.get()

                                    if len(column_names) > 5:
                                        column_names.pop(5)

                                    column_names.append(sixth_curr_val)

                                    def cor_gen():
                                        print("Corr Generation")
                                        correlation_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ', 'Ծննդավայր (երկիր)', 'Ծննդավայր (քաղաք/գյուղ)', 'Ընդունման տարեթիվ', 'Առարկա', 'Առաջին միջանկյալ ստուգում', 'Երկրորդ միջանկյալ ստուգում', 'Ամփոփիչ քննություն']

                                        file_path = sys.path[0] + '\\' + db

                                        if not find_plathform():
                                            file_path = file_path.replace("\\", "/")
                                        df = pd.read_csv(file_path)[correlation_func_parameters]
                                        print(column_names)
                                        
                                        if (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ') and (column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ') and (column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ուսանողի անուն' or column_names[2] == 'Ուսանողի սեռ' or column_names[2] == 'Ծննդավայր (երկիր)' or column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ') and (column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ուսանողի անուն' or column_names[3] == 'Ուսանողի սեռ' or column_names[3] == 'Ծննդավայր (երկիր)' or column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ') and (column_names[4] == 'Ֆակուլտետ' or column_names[4] == 'Ուսանողի անուն' or column_names[4] == 'Ուսանողի սեռ' or column_names[4] == 'Ծննդավայր (երկիր)' or column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ') and (column_names[5] == 'Ֆակուլտետ' or column_names[5] == 'Ուսանողի անուն' or column_names[5] == 'Ուսանողի սեռ' or column_names[5] == 'Ծննդավայր (երկիր)' or column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[5] == 'Ընդունման տարեթիվ'):
                                            corr_6_path="images/correlation/5/1_Fac_Name_Sex_COB_CV_YOE.png"

                                        elif (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[0] == 'Ամփոփիչ քննություն') and (column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[1] == 'Ամփոփիչ քննություն') and (column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[2] == 'Ամփոփիչ քննություն') and (column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[3] == 'Ամփոփիչ քննություն') and (column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[4] == 'Ամփոփիչ քննություն') and (column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[5] == 'Ամփոփիչ քննություն'):
                                            corr_6_path="images/correlation/5/2_CV_YOE_Sbj_FrEx_ScEx_FnEx.png"

                                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա') and (column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա') and (column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ուսանողի սեռ' or column_names[2] == 'Ծննդավայր (երկիր)' or column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա') and (column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ուսանողի սեռ' or column_names[3] == 'Ծննդավայր (երկիր)' or column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա') and (column_names[4] == 'Ֆակուլտետ' or column_names[4] == 'Ուսանողի սեռ' or column_names[4] == 'Ծննդավայր (երկիր)' or column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա') and (column_names[5] == 'Ֆակուլտետ' or column_names[5] == 'Ուսանողի սեռ' or column_names[5] == 'Ծննդավայր (երկիր)' or column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա'):
                                            corr_6_path="images/correlation/5/3_Fac_Sex_COB_CV_YOE_Sbj.png"

                                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[0] == 'Առաջին միջանկյալ ստուգում') and (column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում') and (column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ծննդավայր (երկիր)' or column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում') and (column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ծննդավայր (երկիր)' or column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում') and (column_names[4] == 'Ֆակուլտետ' or column_names[4] == 'Ծննդավայր (երկիր)' or column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում') and (column_names[5] == 'Ֆակուլտետ' or column_names[5] == 'Ծննդավայր (երկիր)' or column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or column_names[5] == 'Առաջին միջանկյալ ստուգում'):
                                            corr_6_path="images/correlation/5/4_Fac_COB_CV_YOE_Sbj_FrEx.png"

                                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[0] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[1] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[2] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[3] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[4] == 'Ֆակուլտետ' or column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[4] == 'Երկրորդ միջանկյալ ստուգում') and  (column_names[5] == 'Ֆակուլտետ' or column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[5] == 'Երկրորդ միջանկյալ ստուգում'):
                                            corr_6_path="images/correlation/5/5_Fac_CV_YOE_Sbj_FrEx_ScEx.png"

                                        elif (column_names[0] == 'Ֆակուլտետ' or column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[0] == 'Ամփոփիչ քննություն') and (column_names[1] == 'Ֆակուլտետ' or column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[1] == 'Ամփոփիչ քննություն') and (column_names[2] == 'Ֆակուլտետ' or column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[2] == 'Ամփոփիչ քննություն') and (column_names[3] == 'Ֆակուլտետ' or column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[4] == 'Ամփոփիչ քննություն') and (column_names[4] == 'Ֆակուլտետ' or column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[4] == 'Ամփոփիչ քննություն') and (column_names[5] == 'Ֆակուլտետ' or column_names[5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[5] == 'Ամփոփիչ քննություն'):
                                            corr_6_path="images/correlation/5/6_Fac_YOE_Sbj_FrEx_ScEx_FnEx.png"

                                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[0] == 'Առաջին միջանկյալ ստուգում') and (column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում') and (column_names[2] == 'Ուսանողի անուն' or column_names[2] == 'Ծննդավայր (երկիր)' or column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում') and (column_names[3] == 'Ուսանողի անուն' or column_names[3] == 'Ծննդավայր (երկիր)' or column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում') and (column_names[4] == 'Ուսանողի անուն' or column_names[4] == 'Ծննդավայր (երկիր)' or column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում') and (column_names[5] == 'Ուսանողի անուն' or column_names[5] == 'Ծննդավայր (երկիր)' or column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or column_names[5] == 'Առաջին միջանկյալ ստուգում'):
                                            corr_6_path="images/correlation/5/7_Name_COB_CV_YOE_Sbj_FrEx.png"

                                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[0] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[1] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[2] == 'Ուսանողի անուն' or column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[2] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[3] == 'Ուսանողի անուն' or column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[3] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[4] == 'Ուսանողի անուն' or column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[4] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[5] == 'Ուսանողի անուն' or column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[5] == 'Երկրորդ միջանկյալ ստուգում'):
                                            corr_6_path="images/correlation/5/8_Name_CV_YOE_Sbj_FrEx_ScEx.png"

                                        elif (column_names[0] == 'Ուսանողի անուն' or column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[0] == 'Ամփոփիչ քննություն') and (column_names[1] == 'Ուսանողի անուն' or column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[1] == 'Ամփոփիչ քննություն') and (column_names[2] == 'Ուսանողի անուն' or column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[2] == 'Ամփոփիչ քննություն') and (column_names[3] == 'Ուսանողի անուն' or column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[3] == 'Ամփոփիչ քննություն') and (column_names[4] == 'Ուսանողի անուն' or column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[4] == 'Ամփոփիչ քննություն') and (column_names[5] == 'Ուսանողի անուն' or column_names[5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[5] == 'Ամփոփիչ քննություն'):
                                            corr_6_path="images/correlation/5/9_Name_YOE_Sbj_FrEx_ScEx_FnEx.png"

                                        elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[0] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[1] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[2] == 'Ուսանողի սեռ' or column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[2] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[3] == 'Ուսանողի սեռ' or column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[3] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[4] == 'Ուսանողի սեռ' or column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[4] == 'Երկրորդ միջանկյալ ստուգում') and (column_names[5] == 'Ուսանողի սեռ' or column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[5] == 'Երկրորդ միջանկյալ ստուգում'):
                                            corr_6_path="images/correlation/5/10_Sex_CV_YOE_Sbj_FrEx_ScEx.png"

                                        elif (column_names[0] == 'Ուսանողի սեռ' or column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[0] == 'Ամփոփիչ քննություն') and (column_names[1] == 'Ուսանողի սեռ' or column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[1] == 'Ամփոփիչ քննություն') and (column_names[2] == 'Ուսանողի սեռ' or column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[2] == 'Ամփոփիչ քննություն') and (column_names[3] == 'Ուսանողի սեռ' or column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[3] == 'Ամփոփիչ քննություն') and (column_names[4] == 'Ուսանողի սեռ' or column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[4] == 'Ամփոփիչ քննություն') and (column_names[5] == 'Ուսանողի սեռ' or column_names[5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[5] == 'Ամփոփիչ քննություն'):
                                            corr_6_path="images/correlation/5/11_Sex_YOE_Sbj_FrEx_ScEx_FnEx.png"

                                        elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[0] == 'Ամփոփիչ քննություն') and (column_names[1] == 'Ծննդավայր (երկիր)' or column_names[1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[1] == 'Ամփոփիչ քննություն') and (column_names[2] == 'Ծննդավայր (երկիր)' or column_names[2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[2] == 'Ամփոփիչ քննություն') and (column_names[3] == 'Ծննդավայր (երկիր)' or column_names[3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[3] == 'Ամփոփիչ քննություն') and (column_names[4] == 'Ծննդավայր (երկիր)' or column_names[4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[4] == 'Ամփոփիչ քննություն') and (column_names[5] == 'Ծննդավայր (երկիր)' or column_names[5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[5] == 'Ամփոփիչ քննություն'):
                                            corr_6_path="images/correlation/5/12_COB_YOE_Sbj_FrEx_ScEx_FnEx.png"


                                        image_corr_6 = PhotoImage(file=corr_6_path)
                                        original_image_corr_6 = image_corr_6.subsample(3,3) # resize image using subsample

                                        corr_6_im_label = Label(corr_image_frame,image=original_image_corr_6)
                                        corr_6_im_label.image = original_image_corr_6 # keep a reference
                                        corr_6_im_label.place(x=387, y=118)   

                                        def mouse_on_corr_6(event):
                                            image_corr_6 = PhotoImage(file=corr_6_path)
                                            original_image_corr_6 = image_corr_6.subsample(2,2) # resize image using subsample

                                            corr_6_im_label = Label(corr_image_frame,image=original_image_corr_6)
                                            corr_6_im_label.image = original_image_corr_6 # keep a reference
                                            corr_6_im_label.place(x=387, y=118) 

                                            return                                                       

                                        corr_6_im_label.bind('<Enter>',mouse_on_corr_6)                              

                                        def rst_cor():
                                            print("Reset")
                                            cmb.set('')
                                            cmb1.set('')
                                            cmb2.set('')        
                                            cmb3.set('')        
                                            cmb4.set('')       
                                            cmb5.set('')                                                                                                                                       
                                            number_of_param.set('')
                                            new_text = " "
                                            e1.delete(0, tk.END)
                                            e1.insert(0, new_text)
                                            cmb.place_forget()
                                            cmb1.place_forget()
                                            cmb2.place_forget()       
                                            cmb3.place_forget() 
                                            cmb4.place_forget()    
                                            cmb5.place_forget()                                                                                                                                                
                                            corr_6_im_label.image =''                                                                        

                                        plt_rst_corr=PhotoImage(file="reset.png")  
                                        sub_plt_rst_corr=plt_rst_corr.subsample(4,4)

                                        button_corr_rst = Button(corr_input_frame, text="Reset", fg='#026084', command=rst_cor, image=sub_plt_rst_corr, compound=LEFT, width=130)
                                        button_corr_rst.image=sub_plt_rst_corr
                                        button_corr_rst.place(x=88, y=407)
                                        button_arr.append(button_corr_rst)

                                        ttk.Separator(corr_input_frame).place(x=75, y=487, relwidth=0.29)

                                        def corr_go_to_menu():

                                            print("Coming soon")

                                            corr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                            #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                            corr_apr=Label(corr_frame, width=20, bg='white').place(x=10, y=10)

                                            corr_inner_frame=Frame(corr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                            #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                            corr_input_frame=Frame(corr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                            corr_image_frame=Frame(corr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                            Label(corr_image_frame, bg='white').place(x=565, y=95)                          

                                            print("Correlation frame has been destroyed.")      

                                        plt_up=PhotoImage(file="up.png")  
                                        sub_plt_up=plt_up.subsample(4,4)     

                                        button_corr_go_to_menu=Button(corr_input_frame, text="Go to menu", fg='#026084', command=corr_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                        button_corr_go_to_menu.image=sub_plt_up
                                        button_corr_go_to_menu.place(x=88, y=501)
                                        button_arr.append(button_corr_go_to_menu)  

                                    # Creating a photoimage object to use image 
                                    plt_gen_corr = PhotoImage(file = "images.png") 
                                    sub_plt_gen_corr = plt_gen_corr.subsample(4, 4)    

                                    button_corr_gen = Button(corr_input_frame, text="Generate", fg='#026084', command=cor_gen, image=sub_plt_gen_corr, compound=LEFT)
                                    button_corr_gen.image=sub_plt_gen_corr
                                    button_corr_gen.place(x=88, y=337)
                                    button_arr.append(button_corr_gen)

                                    ttk.Separator(corr_input_frame).place(x=75, y=327, relwidth=0.29)                                    

                                cmb5 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                cmb5.place(x=75, y=296)
                                cmb5.bind('<<ComboboxSelected>>', on_sixth_select)

                            cmb4 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        if (e1.get() == "7" or e1.get() == " 7"):
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):
                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                sixth_data = fifth_data

                                for item in fifth_data:
                                    if item == fifth_curr_val:
                                        sixth_data.remove(item)

                                def on_sixth_select(event=None):
                                    sixth_curr_val = cmb5.get()

                                    if len(column_names) > 5:
                                        column_names.pop(5)

                                    column_names.append(sixth_curr_val)

                                    seventh_data = sixth_data

                                    for item in sixth_data:
                                        if item == sixth_curr_val:
                                            seventh_data.remove(item)

                                    def on_seventh_select(event=None):
                                        seventh_curr_val = cmb6.get()

                                        if len(column_names) > 6:
                                            column_names.pop(6)

                                        column_names.append(seventh_curr_val)                                            

                                        def cor_gen():
                                            print("Corr Generation")
                                            correlation_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն',
                                                                           'Ուսանողի սեռ', 'Ծննդավայր (երկիր)',
                                                                           'Ծննդավայր (քաղաք/գյուղ)',
                                                                           'Ընդունման տարեթիվ', 'Առարկա',
                                                                           'Առաջին միջանկյալ ստուգում',
                                                                           'Երկրորդ միջանկյալ ստուգում',
                                                                           'Ամփոփիչ քննություն']

                                            file_path = sys.path[0] + '\\' + db

                                            if not find_plathform():
                                                file_path = file_path.replace("\\", "/")
                                            df = pd.read_csv(file_path)[correlation_func_parameters]
                                            print(column_names)


                                            print(column_names[0])
                                            print(column_names[1])
                                            print(column_names[2])
                                            print(column_names[3])
                                            print(column_names[4])                                                                                                                                                                                     
                                            print(column_names[5])                                            

                                            if (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                0] == 'Ուսանողի անուն' or
                                                column_names[0] == 'Ուսանողի սեռ' or column_names[
                                                    0] == 'Ծննդավայր (երկիր)' or column_names[
                                                    0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                    0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա') and (
                                                    column_names[1] == 'Ֆակուլտետ' or column_names[
                                                1] == 'Ուսանողի անուն' or column_names[1] == 'Ուսանողի սեռ' or
                                                    column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[
                                                        1] == 'Առարկա') and (
                                                    column_names[2] == 'Ֆակուլտետ' or column_names[
                                                2] == 'Ուսանողի անուն' or column_names[2] == 'Ուսանողի սեռ' or
                                                    column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[
                                                        2] == 'Առարկա') and (
                                                    column_names[3] == 'Ֆակուլտետ' or column_names[
                                                3] == 'Ուսանողի անուն' or column_names[3] == 'Ուսանողի սեռ' or
                                                    column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[
                                                        3] == 'Առարկա') and (
                                                    column_names[4] == 'Ֆակուլտետ' or column_names[
                                                4] == 'Ուսանողի անուն' or column_names[4] == 'Ուսանողի սեռ' or
                                                    column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[
                                                        4] == 'Առարկա') and (
                                                    column_names[5] == 'Ֆակուլտետ' or column_names[
                                                5] == 'Ուսանողի անուն' or column_names[5] == 'Ուսանողի սեռ' or
                                                    column_names[5] == 'Ծննդավայր (երկիր)' or column_names[
                                                        5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[
                                                        5] == 'Առարկա') and (
                                                    column_names[6] == 'Ֆակուլտետ' or column_names[
                                                6] == 'Ուսանողի անուն' or column_names[6] == 'Ուսանողի սեռ' or
                                                    column_names[6] == 'Ծննդավայր (երկիր)' or column_names[
                                                        6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա'):
                                                corr_7_path="images/correlation/6/1_Fac_Name_Sex_COB_CV_YOE_Sbj.png"


                                            elif (column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                                0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                      0] == 'Ամփոփիչ քննություն') and (
                                                    column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        1] == 'Ամփոփիչ քննություն') and (
                                                    column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        2] == 'Ամփոփիչ քննություն') and (
                                                    column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        3] == 'Ամփոփիչ քննություն') and (
                                                    column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        4] == 'Ամփոփիչ քննություն') and (
                                                    column_names[5] == 'Ծննդավայր (երկիր)' or column_names[
                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        5] == 'Ամփոփիչ քննություն') and (
                                                    column_names[6] == 'Ծննդավայր (երկիր)' or column_names[
                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        6] == 'Ամփոփիչ քննություն'):
                                                corr_7_path="images/correlation/6/2_COB_CV_YOE_Sbj_FrEx_ScEx_FnEx.png"



                                            elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                0] == 'Ուսանողի սեռ' or
                                                  column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                                      0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[1] == 'Ֆակուլտետ' or column_names[
                                                1] == 'Ուսանողի սեռ' or column_names[1] == 'Ծննդավայր (երկիր)' or
                                                    column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[2] == 'Ֆակուլտետ' or column_names[
                                                2] == 'Ուսանողի սեռ' or column_names[2] == 'Ծննդավայր (երկիր)' or
                                                    column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[3] == 'Ֆակուլտետ' or column_names[
                                                3] == 'Ուսանողի սեռ' or column_names[3] == 'Ծննդավայր (երկիր)' or
                                                    column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[4] == 'Ֆակուլտետ' or column_names[
                                                4] == 'Ուսանողի սեռ' or column_names[4] == 'Ծննդավայր (երկիր)' or
                                                    column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[5] == 'Ֆակուլտետ' or column_names[
                                                5] == 'Ուսանողի սեռ' or column_names[5] == 'Ծննդավայր (երկիր)' or
                                                    column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում') and (
                                                    column_names[6] == 'Ֆակուլտետ' or column_names[
                                                6] == 'Ուսանողի սեռ' or column_names[6] == 'Ծննդավայր (երկիր)' or
                                                    column_names[6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում'):
                                                corr_7_path="images/correlation/6/3_Fac_Sex_COB_CV_YOE_Sbj_FrEx.png"



                                            elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                0] == 'Ծննդավայր (երկիր)' or column_names[
                                                      0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[1] == 'Ֆակուլտետ' or column_names[
                                                1] == 'Ծննդավայր (երկիր)' or column_names[
                                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[2] == 'Ֆակուլտետ' or column_names[
                                                2] == 'Ծննդավայր (երկիր)' or column_names[
                                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[3] == 'Ֆակուլտետ' or column_names[
                                                3] == 'Ծննդավայր (երկիր)' or column_names[
                                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[4] == 'Ֆակուլտետ' or column_names[
                                                4] == 'Ծննդավայր (երկիր)' or column_names[
                                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[5] == 'Ֆակուլտետ' or column_names[
                                                5] == 'Ծննդավայր (երկիր)' or column_names[
                                                        5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[6] == 'Ֆակուլտետ' or column_names[
                                                6] == 'Ծննդավայր (երկիր)' or column_names[
                                                        6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում'):
                                                corr_7_path="images/correlation/6/4_Fac_COB_CV_YOE_Sbj_FrEx_ScEx.png"


                                            elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                      0] == 'Ամփոփիչ քննություն') and (
                                                    column_names[1] == 'Ֆակուլտետ' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        1] == 'Ամփոփիչ քննություն') and (
                                                    column_names[2] == 'Ֆակուլտետ' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        2] == 'Ամփոփիչ քննություն') and (
                                                    column_names[3] == 'Ֆակուլտետ' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        3] == 'Ամփոփիչ քննություն') and (
                                                    column_names[4] == 'Ֆակուլտետ' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        4] == 'Ամփոփիչ քննություն') and (
                                                    column_names[5] == 'Ֆակուլտետ' or column_names[
                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        5] == 'Ամփոփիչ քննություն') and (
                                                    column_names[6] == 'Ֆակուլտետ' or column_names[
                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        6] == 'Ամփոփիչ քննություն'):
                                                corr_7_path="images/correlation/6/5_Fac_CV_YOE_Sbj_FrEx_ScEx_FnEx.png"



                                            elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                                0] == 'Ծննդավայր (երկիր)' or column_names[
                                                      0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[1] == 'Ուսանողի անուն' or column_names[
                                                1] == 'Ծննդավայր (երկիր)' or column_names[
                                                        1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[2] == 'Ուսանողի անուն' or column_names[
                                                2] == 'Ծննդավայր (երկիր)' or column_names[
                                                        2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[3] == 'Ուսանողի անուն' or column_names[
                                                3] == 'Ծննդավայր (երկիր)' or column_names[
                                                        3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[4] == 'Ուսանողի անուն' or column_names[
                                                4] == 'Ծննդավայր (երկիր)' or column_names[
                                                        4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[5] == 'Ուսանողի անուն' or column_names[
                                                5] == 'Ծննդավայր (երկիր)' or column_names[
                                                        5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                    column_names[6] == 'Ուսանողի անուն' or column_names[
                                                6] == 'Ծննդավայր (երկիր)' or column_names[
                                                        6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում'):
                                                corr_7_path="images/correlation/6/6_Name_COB_CV_YOE_Sbj_FrEx_ScEx.png"


                                            elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                                0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                      0] == 'Ամփոփիչ քննություն') and (
                                                    column_names[1] == 'Ուսանողի անուն' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        1] == 'Ամփոփիչ քննություն') and (
                                                    column_names[2] == 'Ուսանողի անուն' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        2] == 'Ամփոփիչ քննություն') and (
                                                    column_names[3] == 'Ուսանողի անուն' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        3] == 'Ամփոփիչ քննություն') and (
                                                    column_names[4] == 'Ուսանողի անուն' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        4] == 'Ամփոփիչ քննություն') and (
                                                    column_names[5] == 'Ուսանողի անուն' or column_names[
                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        5] == 'Ամփոփիչ քննություն') and (
                                                    column_names[6] == 'Ուսանողի անուն' or column_names[
                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        6] == 'Ամփոփիչ քննություն'):
                                                corr_7_path="images/correlation/6/7_Name_CV_YOE_Sbj_FrEx_ScEx_FnEx.png"


                                            elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                                0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                      0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                  column_names[0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                      0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                      0] == 'Ամփոփիչ քննություն') and (
                                                    column_names[1] == 'Ուսանողի սեռ' or column_names[
                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        1] == 'Ընդունման տարեթիվ' or column_names[1] == 'Առարկա' or
                                                    column_names[1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        1] == 'Ամփոփիչ քննություն') and (
                                                    column_names[2] == 'Ուսանողի սեռ' or column_names[
                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        2] == 'Ընդունման տարեթիվ' or column_names[2] == 'Առարկա' or
                                                    column_names[2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        2] == 'Ամփոփիչ քննություն') and (
                                                    column_names[3] == 'Ուսանողի սեռ' or column_names[
                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        3] == 'Ընդունման տարեթիվ' or column_names[3] == 'Առարկա' or
                                                    column_names[3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        3] == 'Ամփոփիչ քննություն') and (
                                                    column_names[4] == 'Ուսանողի սեռ' or column_names[
                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        4] == 'Ընդունման տարեթիվ' or column_names[4] == 'Առարկա' or
                                                    column_names[4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        4] == 'Ամփոփիչ քննություն') and (
                                                    column_names[5] == 'Ուսանողի սեռ' or column_names[
                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        5] == 'Ընդունման տարեթիվ' or column_names[5] == 'Առարկա' or
                                                    column_names[5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        5] == 'Ամփոփիչ քննություն') and (
                                                    column_names[6] == 'Ուսանողի սեռ' or column_names[
                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        6] == 'Ընդունման տարեթիվ' or column_names[6] == 'Առարկա' or
                                                    column_names[6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                        6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                        6] == 'Ամփոփիչ քննություն'):
                                                corr_7_path="images/correlation/6/8_Sex_CV_YOE_Sbj_FrEx_ScEx_FnEx.png"

                                            image_corr_7 = PhotoImage(file=corr_7_path)
                                            original_image_corr_7 = image_corr_7.subsample(3,3) # resize image using subsample

                                            corr_7_im_label = Label(corr_image_frame,image=original_image_corr_7)
                                            corr_7_im_label.image = original_image_corr_7 # keep a reference
                                            corr_7_im_label.place(x=387, y=118)   

                                            def mouse_on_corr_7(event):
                                                image_corr_7 = PhotoImage(file=corr_7_path)
                                                original_image_corr_7 = image_corr_7.subsample(2,2) # resize image using subsample

                                                corr_7_im_label = Label(corr_image_frame,image=original_image_corr_7)
                                                corr_7_im_label.image = original_image_corr_7 # keep a reference
                                                corr_7_im_label.place(x=387, y=118) 

                                                return                                                       

                                            corr_7_im_label.bind('<Enter>',mouse_on_corr_7)                              

                                            def rst_cor():
                                                print("Reset")
                                                cmb.set('')
                                                cmb1.set('')
                                                cmb2.set('')        
                                                cmb3.set('')        
                                                cmb4.set('')       
                                                cmb5.set('')     
                                                cmb6.set('')                                                                                                                                                                                   
                                                number_of_param.set('')
                                                new_text = " "
                                                e1.delete(0, tk.END)
                                                e1.insert(0, new_text)
                                                cmb.place_forget()
                                                cmb1.place_forget()
                                                cmb2.place_forget()       
                                                cmb3.place_forget() 
                                                cmb4.place_forget()    
                                                cmb5.place_forget()       
                                                cmb6.place_forget()                                                                                                                                                                                           
                                                corr_7_im_label.image =''                                                                        

                                            plt_rst_corr=PhotoImage(file="reset.png")  
                                            sub_plt_rst_corr=plt_rst_corr.subsample(4,4)

                                            button_corr_rst = Button(corr_input_frame, text="Reset", fg='#026084', command=rst_cor, image=sub_plt_rst_corr, compound=LEFT, width=130)
                                            button_corr_rst.image=sub_plt_rst_corr
                                            button_corr_rst.place(x=88, y=430)
                                            button_arr.append(button_corr_rst)

                                            ttk.Separator(corr_input_frame).place(x=75, y=510, relwidth=0.29)

                                            def corr_go_to_menu():

                                                print("Coming soon")

                                                corr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                                #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                                corr_apr=Label(corr_frame, width=20, bg='white').place(x=10, y=10)

                                                corr_inner_frame=Frame(corr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                                #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                                corr_input_frame=Frame(corr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                                corr_image_frame=Frame(corr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                                Label(corr_image_frame, bg='white').place(x=565, y=95)                          

                                                print("Correlation frame has been destroyed.")      

                                            plt_up=PhotoImage(file="up.png")  
                                            sub_plt_up=plt_up.subsample(5,5)     

                                            button_corr_go_to_menu=Button(corr_input_frame, text="Go to menu", fg='#026084', command=corr_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                            button_corr_go_to_menu.image=sub_plt_up
                                            button_corr_go_to_menu.place(x=88, y=512)
                                            button_arr.append(button_corr_go_to_menu)  

                                        # Creating a photoimage object to use image 
                                        plt_gen_corr = PhotoImage(file = "images.png") 
                                        sub_plt_gen_corr = plt_gen_corr.subsample(4, 4)    

                                        button_corr_gen = Button(corr_input_frame, text="Generate", fg='#026084', command=cor_gen, image=sub_plt_gen_corr, compound=LEFT)
                                        button_corr_gen.image=sub_plt_gen_corr
                                        button_corr_gen.place(x=88, y=360)
                                        button_arr.append(button_corr_gen)

                                        ttk.Separator(corr_input_frame).place(x=75, y=350, relwidth=0.29)                                                                            

                                    cmb6 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                    cmb6.place(x=75, y=319)
                                    cmb6.bind('<<ComboboxSelected>>', on_seventh_select)

                                cmb5 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                cmb5.place(x=75, y=296)
                                cmb5.bind('<<ComboboxSelected>>', on_sixth_select)

                            cmb4 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        if (e1.get() == "8" or e1.get() == " 8"):
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):

                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                sixth_data = fifth_data

                                for item in fifth_data:
                                    if item == fifth_curr_val:
                                        sixth_data.remove(item)

                                def on_sixth_select(event=None):
                                    sixth_curr_val = cmb5.get()

                                    if len(column_names) > 5:
                                        column_names.pop(5)

                                    column_names.append(sixth_curr_val)

                                    seventh_data = sixth_data

                                    for item in sixth_data:
                                        if item == sixth_curr_val:
                                            seventh_data.remove(item)

                                    def on_seventh_select(event=None):
                                        seventh_curr_val = cmb6.get()

                                        if len(column_names) > 6:
                                            column_names.pop(6)

                                        column_names.append(seventh_curr_val)

                                        eight_data = seventh_data

                                        for item in seventh_data:
                                            if item == seventh_curr_val:
                                                eight_data.remove(item)

                                        def on_eight_select(event=None):
                                            eight_curr_val = cmb7.get()

                                            if len(column_names) > 7:
                                                column_names.pop(7)

                                            column_names.append(eight_curr_val)

                                            def cor_gen():
                                                print("Corr Generation")
                                                correlation_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն',
                                                                               'Ուսանողի սեռ', 'Ծննդավայր (երկիր)',
                                                                               'Ծննդավայր (քաղաք/գյուղ)',
                                                                               'Ընդունման տարեթիվ', 'Առարկա',
                                                                               'Առաջին միջանկյալ ստուգում',
                                                                               'Երկրորդ միջանկյալ ստուգում',
                                                                               'Ամփոփիչ քննություն']

                                                file_path = sys.path[0] + '\\' + db

                                                if not find_plathform():
                                                    file_path = file_path.replace("\\", "/")
                                                df = pd.read_csv(file_path)[correlation_func_parameters]
                                                print(column_names)

                                                if (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                    0] == 'Ուսանողի անուն' or column_names[0] == 'Ուսանողի սեռ' or
                                                    column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                                        0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                        0] == 'Ընդունման տարեթիվ' or column_names[0] == 'Առարկա' or
                                                    column_names[0] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[1] == 'Ֆակուլտետ' or column_names[
                                                    1] == 'Ուսանողի անուն' or column_names[1] == 'Ուսանողի սեռ' or
                                                        column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                                            1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            1] == 'Ընդունման տարեթիվ' or column_names[
                                                            1] == 'Առարկա' or
                                                        column_names[1] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[2] == 'Ֆակուլտետ' or column_names[
                                                    2] == 'Ուսանողի անուն' or column_names[2] == 'Ուսանողի սեռ' or
                                                        column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                                            2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            2] == 'Ընդունման տարեթիվ' or column_names[
                                                            2] == 'Առարկա' or
                                                        column_names[2] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[3] == 'Ֆակուլտետ' or column_names[
                                                    3] == 'Ուսանողի անուն' or column_names[3] == 'Ուսանողի սեռ' or
                                                        column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                                            3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            3] == 'Ընդունման տարեթիվ' or column_names[
                                                            3] == 'Առարկա' or
                                                        column_names[3] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[4] == 'Ֆակուլտետ' or column_names[
                                                    4] == 'Ուսանողի անուն' or column_names[4] == 'Ուսանողի սեռ' or
                                                        column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                                            4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            4] == 'Ընդունման տարեթիվ' or column_names[
                                                            4] == 'Առարկա' or
                                                        column_names[4] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[5] == 'Ֆակուլտետ' or column_names[
                                                    5] == 'Ուսանողի անուն' or column_names[5] == 'Ուսանողի սեռ' or
                                                        column_names[5] == 'Ծննդավայր (երկիր)' or column_names[
                                                            5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            5] == 'Ընդունման տարեթիվ' or column_names[
                                                            5] == 'Առարկա' or
                                                        column_names[5] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[6] == 'Ֆակուլտետ' or column_names[
                                                    6] == 'Ուսանողի անուն' or column_names[6] == 'Ուսանողի սեռ' or
                                                        column_names[6] == 'Ծննդավայր (երկիր)' or column_names[
                                                            6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            6] == 'Ընդունման տարեթիվ' or column_names[
                                                            6] == 'Առարկա' or
                                                        column_names[6] == 'Առաջին միջանկյալ ստուգում') and (
                                                        column_names[7] == 'Ֆակուլտետ' or column_names[
                                                    7] == 'Ուսանողի անուն' or column_names[7] == 'Ուսանողի սեռ' or
                                                        column_names[7] == 'Ծննդավայր (երկիր)' or column_names[
                                                            7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            7] == 'Ընդունման տարեթիվ' or column_names[
                                                            7] == 'Առարկա' or
                                                        column_names[7] == 'Առաջին միջանկյալ ստուգում'):
                                                    corr_8_path="images/correlation/7/1_Fac_Name_Sex_COB_CV_YOE_Sbj_Fr_Ex.png"


                                                elif (column_names[0] == 'Ուսանողի սեռ' or column_names[
                                                    0] == 'Ծննդավայր (երկիր)' or column_names[
                                                          0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                          0] == 'Ընդունման տարեթիվ' or column_names[
                                                          0] == 'Առարկա' or
                                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or
                                                      column_names[
                                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                          0] == 'Ամփոփիչ քննություն') and (
                                                        column_names[1] == 'Ուսանողի սեռ' or column_names[
                                                    1] == 'Ծննդավայր (երկիր)' or column_names[
                                                            1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            1] == 'Ընդունման տարեթիվ' or column_names[
                                                            1] == 'Առարկա' or
                                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            1] == 'Ամփոփիչ քննություն') and (
                                                        column_names[2] == 'Ուսանողի սեռ' or column_names[
                                                    2] == 'Ծննդավայր (երկիր)' or column_names[
                                                            2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            2] == 'Ընդունման տարեթիվ' or column_names[
                                                            2] == 'Առարկա' or
                                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            2] == 'Ամփոփիչ քննություն') and (
                                                        column_names[3] == 'Ուսանողի սեռ' or column_names[
                                                    3] == 'Ծննդավայր (երկիր)' or column_names[
                                                            3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            3] == 'Ընդունման տարեթիվ' or column_names[
                                                            3] == 'Առարկա' or
                                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            3] == 'Ամփոփիչ քննություն') and (
                                                        column_names[4] == 'Ուսանողի սեռ' or column_names[
                                                    4] == 'Ծննդավայր (երկիր)' or column_names[
                                                            4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            4] == 'Ընդունման տարեթիվ' or column_names[
                                                            4] == 'Առարկա' or
                                                        column_names[4] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            4] == 'Ամփոփիչ քննություն') and (
                                                        column_names[5] == 'Ուսանողի սեռ' or column_names[
                                                    5] == 'Ծննդավայր (երկիր)' or column_names[
                                                            5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            5] == 'Ընդունման տարեթիվ' or column_names[
                                                            5] == 'Առարկա' or
                                                        column_names[5] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            5] == 'Ամփոփիչ քննություն') and (
                                                        column_names[6] == 'Ուսանողի սեռ' or column_names[
                                                    6] == 'Ծննդավայր (երկիր)' or column_names[
                                                            6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            6] == 'Ընդունման տարեթիվ' or column_names[
                                                            6] == 'Առարկա' or
                                                        column_names[6] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            6] == 'Ամփոփիչ քննություն') and (
                                                        column_names[7] == 'Ուսանողի սեռ' or column_names[
                                                    7] == 'Ծննդավայր (երկիր)' or column_names[
                                                            7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            7] == 'Ընդունման տարեթիվ' or column_names[
                                                            7] == 'Առարկա' or
                                                        column_names[7] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            7] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            7] == 'Ամփոփիչ քննություն'):

                                                    corr_8_path="images/correlation/7/2_Sex_COB_CV_YOE_Sbj_FrEx_ScEx_FnEx.png"

                                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                    0] == 'Ուսանողի սեռ' or column_names[
                                                          0] == 'Ծննդավայր (երկիր)' or
                                                      column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                          0] == 'Ընդունման տարեթիվ' or column_names[
                                                          0] == 'Առարկա' or
                                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or
                                                      column_names[
                                                          0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[1] == 'Ֆակուլտետ' or column_names[
                                                    1] == 'Ուսանողի սեռ' or column_names[
                                                            1] == 'Ծննդավայր (երկիր)' or
                                                        column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            1] == 'Ընդունման տարեթիվ' or column_names[
                                                            1] == 'Առարկա' or
                                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            1] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[2] == 'Ֆակուլտետ' or column_names[
                                                    2] == 'Ուսանողի սեռ' or column_names[
                                                            2] == 'Ծննդավայր (երկիր)' or
                                                        column_names[2] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            2] == 'Ընդունման տարեթիվ' or column_names[
                                                            2] == 'Առարկա' or
                                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[3] == 'Ֆակուլտետ' or column_names[
                                                    3] == 'Ուսանողի սեռ' or column_names[
                                                            3] == 'Ծննդավայր (երկիր)' or
                                                        column_names[3] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            3] == 'Ընդունման տարեթիվ' or column_names[
                                                            3] == 'Առարկա' or
                                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[4] == 'Ֆակուլտետ' or column_names[
                                                    4] == 'Ուսանողի սեռ' or column_names[
                                                            4] == 'Ծննդավայր (երկիր)' or
                                                        column_names[4] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            4] == 'Ընդունման տարեթիվ' or column_names[
                                                            4] == 'Առարկա' or
                                                        column_names[4] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            4] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[5] == 'Ֆակուլտետ' or column_names[
                                                    5] == 'Ուսանողի սեռ' or column_names[
                                                            5] == 'Ծննդավայր (երկիր)' or
                                                        column_names[5] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            5] == 'Ընդունման տարեթիվ' or column_names[
                                                            5] == 'Առարկա' or
                                                        column_names[5] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            5] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[6] == 'Ֆակուլտետ' or column_names[
                                                    6] == 'Ուսանողի սեռ' or column_names[
                                                            6] == 'Ծննդավայր (երկիր)' or
                                                        column_names[6] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            6] == 'Ընդունման տարեթիվ' or column_names[
                                                            6] == 'Առարկա' or
                                                        column_names[6] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            6] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                        column_names[7] == 'Ֆակուլտետ' or column_names[
                                                    7] == 'Ուսանողի սեռ' or column_names[
                                                            7] == 'Ծննդավայր (երկիր)' or
                                                        column_names[7] == 'Ծննդավայր (քաղաք/գյուղ)' or
                                                        column_names[
                                                            7] == 'Ընդունման տարեթիվ' or column_names[
                                                            7] == 'Առարկա' or
                                                        column_names[7] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            7] == 'Երկրորդ միջանկյալ ստուգում'):
                                                    corr_8_path="images/correlation/7/3_Fac_Sex_COB_CV_YOE_Sbj_FrEx_ScEx.png"


                                                elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                    0] == 'Ծննդավայր (երկիր)' or column_names[
                                                          0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                          0] == 'Ընդունման տարեթիվ' or column_names[
                                                          0] == 'Առարկա' or
                                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or
                                                      column_names[
                                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                          0] == 'Ամփոփիչ քննություն') and (
                                                        column_names[1] == 'Ֆակուլտետ' or column_names[
                                                    1] == 'Ծննդավայր (երկիր)' or column_names[
                                                            1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            1] == 'Ընդունման տարեթիվ' or column_names[
                                                            1] == 'Առարկա' or
                                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            1] == 'Ամփոփիչ քննություն') and (
                                                        column_names[2] == 'Ֆակուլտետ' or column_names[
                                                    2] == 'Ծննդավայր (երկիր)' or column_names[
                                                            2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            2] == 'Ընդունման տարեթիվ' or column_names[
                                                            2] == 'Առարկա' or
                                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            2] == 'Ամփոփիչ քննություն') and (
                                                        column_names[3] == 'Ֆակուլտետ' or column_names[
                                                    3] == 'Ծննդավայր (երկիր)' or column_names[
                                                            3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            3] == 'Ընդունման տարեթիվ' or column_names[
                                                            3] == 'Առարկա' or
                                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            3] == 'Ամփոփիչ քննություն') and (
                                                        column_names[4] == 'Ֆակուլտետ' or column_names[
                                                    4] == 'Ծննդավայր (երկիր)' or column_names[
                                                            4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            4] == 'Ընդունման տարեթիվ' or column_names[
                                                            4] == 'Առարկա' or
                                                        column_names[4] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            4] == 'Ամփոփիչ քննություն') and (
                                                        column_names[5] == 'Ֆակուլտետ' or column_names[
                                                    5] == 'Ծննդավայր (երկիր)' or column_names[
                                                            5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            5] == 'Ընդունման տարեթիվ' or column_names[
                                                            5] == 'Առարկա' or
                                                        column_names[5] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            5] == 'Ամփոփիչ քննություն') and (
                                                        column_names[6] == 'Ֆակուլտետ' or column_names[
                                                    6] == 'Ծննդավայր (երկիր)' or column_names[
                                                            6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            6] == 'Ընդունման տարեթիվ' or column_names[
                                                            6] == 'Առարկա' or
                                                        column_names[6] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            6] == 'Ամփոփիչ քննություն') and (
                                                        column_names[7] == 'Ֆակուլտետ' or column_names[
                                                    7] == 'Ծննդավայր (երկիր)' or column_names[
                                                            7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            7] == 'Ընդունման տարեթիվ' or column_names[
                                                            7] == 'Առարկա' or
                                                        column_names[7] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            7] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            7] == 'Ամփոփիչ քննություն'):
                                                    corr_8_path="images/correlation/7/4_Fac_COB_CV_YOE_Sbj_FrEx_ScEx_FnEx.png"

                                                elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                                    0] == 'Ծննդավայր (երկիր)' or column_names[
                                                          0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                          0] == 'Ընդունման տարեթիվ' or column_names[
                                                          0] == 'Առարկա' or
                                                      column_names[0] == 'Առաջին միջանկյալ ստուգում' or
                                                      column_names[
                                                          0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                          0] == 'Ամփոփիչ քննություն') and (
                                                        column_names[1] == 'Ուսանողի անուն' or column_names[
                                                    1] == 'Ծննդավայր (երկիր)' or column_names[
                                                            1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            1] == 'Ընդունման տարեթիվ' or column_names[
                                                            1] == 'Առարկա' or
                                                        column_names[1] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            1] == 'Ամփոփիչ քննություն') and (
                                                        column_names[2] == 'Ուսանողի անուն' or column_names[
                                                    2] == 'Ծննդավայր (երկիր)' or column_names[
                                                            2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            2] == 'Ընդունման տարեթիվ' or column_names[
                                                            2] == 'Առարկա' or
                                                        column_names[2] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            2] == 'Ամփոփիչ քննություն') and (
                                                        column_names[3] == 'Ուսանողի անուն' or column_names[
                                                    3] == 'Ծննդավայր (երկիր)' or column_names[
                                                            3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            3] == 'Ընդունման տարեթիվ' or column_names[
                                                            3] == 'Առարկա' or
                                                        column_names[3] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            3] == 'Ամփոփիչ քննություն') and (
                                                        column_names[4] == 'Ուսանողի անուն' or column_names[
                                                    4] == 'Ծննդավայր (երկիր)' or column_names[
                                                            4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            4] == 'Ընդունման տարեթիվ' or column_names[
                                                            4] == 'Առարկա' or
                                                        column_names[4] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            4] == 'Ամփոփիչ քննություն') and (
                                                        column_names[5] == 'Ուսանողի անուն' or column_names[
                                                    5] == 'Ծննդավայր (երկիր)' or column_names[
                                                            5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            5] == 'Ընդունման տարեթիվ' or column_names[
                                                            5] == 'Առարկա' or
                                                        column_names[5] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            5] == 'Ամփոփիչ քննություն') and (
                                                        column_names[6] == 'Ուսանողի անուն' or column_names[
                                                    6] == 'Ծննդավայր (երկիր)' or column_names[
                                                            6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            6] == 'Ընդունման տարեթիվ' or column_names[
                                                            6] == 'Առարկա' or
                                                        column_names[6] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            6] == 'Ամփոփիչ քննություն') and (
                                                        column_names[7] == 'Ուսանողի անուն' or column_names[
                                                    7] == 'Ծննդավայր (երկիր)' or column_names[
                                                            7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            7] == 'Ընդունման տարեթիվ' or column_names[
                                                            7] == 'Առարկա' or
                                                        column_names[7] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            7] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                            7] == 'Ամփոփիչ քննություն'):

                                                    corr_8_path="images/correlation/7/5_Name_COB_CV_YOE_Sbj_FrEx_ScEx_FnEx.png"

                                                image_corr_8 = PhotoImage(file=corr_8_path)
                                                original_image_corr_8 = image_corr_8.subsample(3,3) # resize image using subsample

                                                corr_8_im_label = Label(corr_image_frame,image=original_image_corr_8)
                                                corr_8_im_label.image = original_image_corr_8 # keep a reference
                                                corr_8_im_label.place(x=387, y=118)   

                                                def mouse_on_corr_8(event):
                                                    image_corr_8 = PhotoImage(file=corr_8_path)
                                                    original_image_corr_8 = image_corr_8.subsample(2,2) # resize image using subsample

                                                    corr_8_im_label = Label(corr_image_frame,image=original_image_corr_8)
                                                    corr_8_im_label.image = original_image_corr_8 # keep a reference
                                                    corr_8_im_label.place(x=387, y=118) 

                                                    return                                                       

                                                corr_8_im_label.bind('<Enter>',mouse_on_corr_8)                              

                                                def rst_cor():
                                                    print("Reset")
                                                    cmb.set('')
                                                    cmb1.set('')
                                                    cmb2.set('')        
                                                    cmb3.set('')        
                                                    cmb4.set('')       
                                                    cmb5.set('')     
                                                    cmb6.set('')         
                                                    cmb7.set('')                                                                                                                                                                                                                                
                                                    number_of_param.set('')
                                                    new_text = " "
                                                    e1.delete(0, tk.END)
                                                    e1.insert(0, new_text)
                                                    cmb.place_forget()
                                                    cmb1.place_forget()
                                                    cmb2.place_forget()       
                                                    cmb3.place_forget() 
                                                    cmb4.place_forget()    
                                                    cmb5.place_forget()       
                                                    cmb6.place_forget()   
                                                    cmb7.place_forget()                                                                                                                                                                                                                                              
                                                    corr_8_im_label.image =''                                                                        

                                                plt_rst_corr=PhotoImage(file="reset.png")  
                                                sub_plt_rst_corr=plt_rst_corr.subsample(4,4)

                                                button_corr_rst = Button(corr_input_frame, text="Reset", fg='#026084', command=rst_cor, image=sub_plt_rst_corr, compound=LEFT, width=130)
                                                button_corr_rst.image=sub_plt_rst_corr
                                                button_corr_rst.place(x=88, y=453)
                                                button_arr.append(button_corr_rst)

                                                ttk.Separator(corr_input_frame).place(x=75, y=533, relwidth=0.29)

                                                def corr_go_to_menu():

                                                    print("Coming soon")

                                                    corr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                                    #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                                    corr_apr=Label(corr_frame, width=20, bg='white').place(x=10, y=10)

                                                    corr_inner_frame=Frame(corr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                                    #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                                    corr_input_frame=Frame(corr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                                    corr_image_frame=Frame(corr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                                    Label(corr_image_frame, bg='white').place(x=565, y=95)                          

                                                    print("Correlation frame has been destroyed.")      

                                                plt_up=PhotoImage(file="up.png")  
                                                sub_plt_up=plt_up.subsample(9,9)     

                                                button_corr_go_to_menu=Button(corr_input_frame, text="Go to menu", fg='#026084', command=corr_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                                button_corr_go_to_menu.image=sub_plt_up
                                                button_corr_go_to_menu.place(x=88, y=535)
                                                button_arr.append(button_corr_go_to_menu)

                                            # Creating a photoimage object to use image 
                                            plt_gen_corr = PhotoImage(file = "images.png") 
                                            sub_plt_gen_corr = plt_gen_corr.subsample(4, 4)    

                                            button_corr_gen = Button(corr_input_frame, text="Generate", fg='#026084', command=cor_gen, image=sub_plt_gen_corr, compound=LEFT)
                                            button_corr_gen.image=sub_plt_gen_corr
                                            button_corr_gen.place(x=88, y=383)
                                            button_arr.append(button_corr_gen)

                                            ttk.Separator(corr_input_frame).place(x=75, y=373, relwidth=0.29)                                             

                                        cmb7 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                        cmb7.place(x=75, y=342)
                                        cmb7.bind('<<ComboboxSelected>>', on_eight_select)

                                    cmb6 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                    cmb6.place(x=75, y=319)
                                    cmb6.bind('<<ComboboxSelected>>', on_seventh_select)

                                cmb5 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                cmb5.place(x=75, y=296)
                                cmb5.bind('<<ComboboxSelected>>', on_sixth_select)

                            cmb4 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        if (e1.get() == "9" or e1.get() == " 9"):
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):
                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                sixth_data = fifth_data

                                for item in fifth_data:
                                    if item == fifth_curr_val:
                                        sixth_data.remove(item)

                                def on_sixth_select(event=None):
                                    sixth_curr_val = cmb5.get()

                                    if len(column_names) > 5:
                                        column_names.pop(5)

                                    column_names.append(sixth_curr_val)

                                    seventh_data = sixth_data

                                    for item in sixth_data:
                                        if item == sixth_curr_val:
                                            seventh_data.remove(item)

                                    def on_seventh_select(event=None):
                                        seventh_curr_val = cmb6.get()

                                        if len(column_names) > 6:
                                            column_names.pop(6)

                                        column_names.append(seventh_curr_val)

                                        eight_data = seventh_data

                                        for item in seventh_data:
                                            if item == seventh_curr_val:
                                                eight_data.remove(item)

                                        def on_eight_select(event=None):
                                            eight_curr_val = cmb7.get()

                                            if len(column_names) > 7:
                                                column_names.pop(7)

                                            column_names.append(eight_curr_val)

                                            ninth_data = eight_data

                                            for item in eight_data:
                                                if item == eight_curr_val:
                                                    ninth_data.remove(item)

                                            def on_ninth_select(event=None):
                                                ninth_curr_val = cmb8.get()

                                                if len(column_names) > 8:
                                                    column_names.pop(8)

                                                column_names.append(ninth_curr_val)

                                                def cor_gen():
                                                    print("Corr Generation")
                                                    correlation_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն',
                                                                                   'Ուսանողի սեռ',
                                                                                   'Ծննդավայր (երկիր)',
                                                                                   'Ծննդավայր (քաղաք/գյուղ)',
                                                                                   'Ընդունման տարեթիվ', 'Առարկա',
                                                                                   'Առաջին միջանկյալ ստուգում',
                                                                                   'Երկրորդ միջանկյալ ստուգում',
                                                                                   'Ամփոփիչ քննություն']

                                                    file_path = sys.path[0] + '\\' + db

                                                    if not find_plathform():
                                                        file_path = file_path.replace("\\", "/")
                                                    df = pd.read_csv(file_path)[correlation_func_parameters]
                                                    print(column_names)

                                                    if (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                        0] == 'Ուսանողի անուն' or column_names[
                                                            0] == 'Ուսանողի սեռ' or
                                                        column_names[0] == 'Ծննդավայր (երկիր)' or column_names[
                                                            0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                            0] == 'Ընդունման տարեթիվ' or column_names[
                                                            0] == 'Առարկա' or
                                                        column_names[0] == 'Առաջին միջանկյալ ստուգում' or
                                                        column_names[
                                                            0] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[1] == 'Ֆակուլտետ' or column_names[
                                                        1] == 'Ուսանողի անուն' or column_names[
                                                                1] == 'Ուսանողի սեռ' or
                                                            column_names[1] == 'Ծննդավայր (երկիր)' or column_names[
                                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                1] == 'Ընդունման տարեթիվ' or column_names[
                                                                1] == 'Առարկա' or column_names[
                                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                1] == 'Second_Exam') and (
                                                            column_names[2] == 'Ֆակուլտետ' or column_names[
                                                        2] == 'Ուսանողի անուն' or column_names[
                                                                2] == 'Ուսանողի սեռ' or
                                                            column_names[2] == 'Ծննդավայր (երկիր)' or column_names[
                                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                2] == 'Ընդունման տարեթիվ' or column_names[
                                                                2] == 'Առարկա' or column_names[
                                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                2] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[3] == 'Ֆակուլտետ' or column_names[
                                                        3] == 'Ուսանողի անուն' or column_names[
                                                                3] == 'Ուսանողի սեռ' or
                                                            column_names[3] == 'Ծննդավայր (երկիր)' or column_names[
                                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                3] == 'Ընդունման տարեթիվ' or column_names[
                                                                3] == 'Առարկա' or column_names[
                                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                3] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[4] == 'Ֆակուլտետ' or column_names[
                                                        4] == 'Ուսանողի անուն' or column_names[
                                                                4] == 'Ուսանողի սեռ' or
                                                            column_names[4] == 'Ծննդավայր (երկիր)' or column_names[
                                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                4] == 'Ընդունման տարեթիվ' or column_names[
                                                                4] == 'Առարկա' or column_names[
                                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                4] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[5] == 'Ֆակուլտետ' or column_names[
                                                        5] == 'Ուսանողի անուն' or column_names[
                                                                5] == 'Ուսանողի սեռ' or
                                                            column_names[5] == 'Ծննդավայր (երկիր)' or column_names[
                                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                5] == 'Ընդունման տարեթիվ' or column_names[
                                                                5] == 'Առարկա' or column_names[
                                                                5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                5] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[6] == 'Ֆակուլտետ' or column_names[
                                                        6] == 'Ուսանողի անուն' or column_names[
                                                                6] == 'Ուսանողի սեռ' or
                                                            column_names[6] == 'Ծննդավայր (երկիր)' or column_names[
                                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                6] == 'Ընդունման տարեթիվ' or column_names[
                                                                6] == 'Առարկա' or column_names[
                                                                6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                6] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[7] == 'Ֆակուլտետ' or column_names[
                                                        7] == 'Ուսանողի անուն' or column_names[
                                                                7] == 'Ուսանողի սեռ' or
                                                            column_names[7] == 'Ծննդավայր (երկիր)' or column_names[
                                                                7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                7] == 'Ընդունման տարեթիվ' or column_names[
                                                                7] == 'Առարկա' or column_names[
                                                                7] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                7] == 'Երկրորդ միջանկյալ ստուգում') and (
                                                            column_names[8] == 'Ֆակուլտետ' or column_names[
                                                        8] == 'Ուսանողի անուն' or column_names[
                                                                8] == 'Ուսանողի սեռ' or
                                                            column_names[8] == 'Ծննդավայր (երկիր)' or column_names[
                                                                8] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                8] == 'Ընդունման տարեթիվ' or column_names[
                                                                8] == 'Առարկա' or column_names[
                                                                8] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                8] == 'Երկրորդ միջանկյալ ստուգում'):
                                                        corr_9_path="images/correlation/8/1_Fac_Name_Sex_COB_CV_YOE_Sbj_FrEx_ScEx.png"

                                                    elif (column_names[0] == 'Ուսանողի անուն' or column_names[
                                                        0] == 'Ուսանողի սեռ' or column_names[
                                                              0] == 'Ծննդավայր (երկիր)' or column_names[
                                                              0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                              0] == 'Ընդունման տարեթիվ' or column_names[
                                                              0] == 'Առարկա' or column_names[
                                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                              0] == 'Ամփոփիչ քննություն') and (
                                                            column_names[1] == 'Ուսանողի անուն' or column_names[
                                                        1] == 'Ուսանողի սեռ' or column_names[
                                                                1] == 'Ծննդավայր (երկիր)' or column_names[
                                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                1] == 'Ընդունման տարեթիվ' or column_names[
                                                                1] == 'Առարկա' or column_names[
                                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                1] == 'Ամփոփիչ քննություն') and (
                                                            column_names[2] == 'Ուսանողի անուն' or column_names[
                                                        2] == 'Ուսանողի սեռ' or column_names[
                                                                2] == 'Ծննդավայր (երկիր)' or column_names[
                                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                2] == 'Ընդունման տարեթիվ' or column_names[
                                                                2] == 'Առարկա' or column_names[
                                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                2] == 'Ամփոփիչ քննություն') and (
                                                            column_names[3] == 'Ուսանողի անուն' or column_names[
                                                        3] == 'Ուսանողի սեռ' or column_names[
                                                                3] == 'Ծննդավայր (երկիր)' or column_names[
                                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                3] == 'Ընդունման տարեթիվ' or column_names[
                                                                3] == 'Առարկա' or column_names[
                                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                3] == 'Ամփոփիչ քննություն') and (
                                                            column_names[4] == 'Ուսանողի անուն' or column_names[
                                                        4] == 'Ուսանողի սեռ' or column_names[
                                                                4] == 'Ծննդավայր (երկիր)' or column_names[
                                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                4] == 'Ընդունման տարեթիվ' or column_names[
                                                                4] == 'Առարկա' or column_names[
                                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                4] == 'Ամփոփիչ քննություն') and (
                                                            column_names[5] == 'Ուսանողի անուն' or column_names[
                                                        5] == 'Ուսանողի սեռ' or column_names[
                                                                5] == 'Ծննդավայր (երկիր)' or column_names[
                                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                5] == 'Ընդունման տարեթիվ' or column_names[
                                                                5] == 'Առարկա' or column_names[
                                                                5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                5] == 'Ամփոփիչ քննություն') and (
                                                            column_names[6] == 'Ուսանողի անուն' or column_names[
                                                        6] == 'Ուսանողի սեռ' or column_names[
                                                                6] == 'Ծննդավայր (երկիր)' or column_names[
                                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                6] == 'Ընդունման տարեթիվ' or column_names[
                                                                6] == 'Առարկա' or column_names[
                                                                6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                6] == 'Ամփոփիչ քննություն') and (
                                                            column_names[7] == 'Ուսանողի անուն' or column_names[
                                                        7] == 'Ուսանողի սեռ' or column_names[
                                                                7] == 'Ծննդավայր (երկիր)' or column_names[
                                                                7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                7] == 'Ընդունման տարեթիվ' or column_names[
                                                                7] == 'Առարկա' or column_names[
                                                                7] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                7] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                7] == 'Ամփոփիչ քննություն') and (
                                                            column_names[8] == 'Ուսանողի անուն' or column_names[
                                                        8] == 'Ուսանողի սեռ' or column_names[
                                                                8] == 'Ծննդավայր (երկիր)' or column_names[
                                                                8] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                8] == 'Ընդունման տարեթիվ' or column_names[
                                                                8] == 'Առարկա' or column_names[
                                                                8] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                8] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                8] == 'Ամփոփիչ քննություն'):
                                                        corr_9_path="images/correlation/8/2_Name_Sex_COB_CV_YOE_Sbj_FrEx_ScEx_FnEx.png"


                                                    elif (column_names[0] == 'Ֆակուլտետ' or column_names[
                                                        0] == 'Ուսանողի սեռ' or column_names[
                                                              0] == 'Ծննդավայր (երկիր)' or column_names[
                                                              0] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                              0] == 'Ընդունման տարեթիվ' or column_names[
                                                              0] == 'Առարկա' or column_names[
                                                              0] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                              0] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                              0] == 'Ամփոփիչ քննություն') and (
                                                            column_names[1] == 'Ֆակուլտետ' or column_names[
                                                        1] == 'Ուսանողի սեռ' or column_names[
                                                                1] == 'Ծննդավայր (երկիր)' or column_names[
                                                                1] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                1] == 'Ընդունման տարեթիվ' or column_names[
                                                                1] == 'Առարկա' or column_names[
                                                                1] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                1] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                1] == 'Ամփոփիչ քննություն') and (
                                                            column_names[2] == 'Ֆակուլտետ' or column_names[
                                                        2] == 'Ուսանողի սեռ' or column_names[
                                                                2] == 'Ծննդավայր (երկիր)' or column_names[
                                                                2] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                2] == 'Ընդունման տարեթիվ' or column_names[
                                                                2] == 'Առարկա' or column_names[
                                                                2] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                2] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                2] == 'Ամփոփիչ քննություն') and (
                                                            column_names[3] == 'Ֆակուլտետ' or column_names[
                                                        3] == 'Ուսանողի սեռ' or column_names[
                                                                3] == 'Ծննդավայր (երկիր)' or column_names[
                                                                3] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                3] == 'Ընդունման տարեթիվ' or column_names[
                                                                3] == 'Առարկա' or column_names[
                                                                3] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                3] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                3] == 'Ամփոփիչ քննություն') and (
                                                            column_names[4] == 'Ֆակուլտետ' or column_names[
                                                        4] == 'Ուսանողի սեռ' or column_names[
                                                                4] == 'Ծննդավայր (երկիր)' or column_names[
                                                                4] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                4] == 'Ընդունման տարեթիվ' or column_names[
                                                                4] == 'Առարկա' or column_names[
                                                                4] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                4] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                4] == 'Ամփոփիչ քննություն') and (
                                                            column_names[5] == 'Ֆակուլտետ' or column_names[
                                                        5] == 'Ուսանողի սեռ' or column_names[
                                                                5] == 'Ծննդավայր (երկիր)' or column_names[
                                                                5] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                5] == 'Ընդունման տարեթիվ' or column_names[
                                                                5] == 'Առարկա' or column_names[
                                                                5] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                5] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                5] == 'Ամփոփիչ քննություն') and (
                                                            column_names[6] == 'Ֆակուլտետ' or column_names[
                                                        6] == 'Ուսանողի սեռ' or column_names[
                                                                6] == 'Ծննդավայր (երկիր)' or column_names[
                                                                6] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                6] == 'Ընդունման տարեթիվ' or column_names[
                                                                6] == 'Առարկա' or column_names[
                                                                6] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                6] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                6] == 'Ամփոփիչ քննություն') and (
                                                            column_names[7] == 'Ֆակուլտետ' or column_names[
                                                        7] == 'Ուսանողի սեռ' or column_names[
                                                                7] == 'Ծննդավայր (երկիր)' or column_names[
                                                                7] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                7] == 'Ընդունման տարեթիվ' or column_names[
                                                                7] == 'Առարկա' or column_names[
                                                                7] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                7] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                7] == 'Ամփոփիչ քննություն') and (
                                                            column_names[8] == 'Ֆակուլտետ' or column_names[
                                                        8] == 'Ուսանողի սեռ' or column_names[
                                                                8] == 'Ծննդավայր (երկիր)' or column_names[
                                                                8] == 'Ծննդավայր (քաղաք/գյուղ)' or column_names[
                                                                8] == 'Ընդունման տարեթիվ' or column_names[
                                                                8] == 'Առարկա' or column_names[
                                                                8] == 'Առաջին միջանկյալ ստուգում' or column_names[
                                                                8] == 'Երկրորդ միջանկյալ ստուգում' or column_names[
                                                                8] == 'Ամփոփիչ քննություն'):
                                                        corr_9_path="images/correlation/8/3_Fac_Sex_COB_CV_YOE_Sbj_FrEx_ScEx_FnEx.png"

                                                    image_corr_9 = PhotoImage(file=corr_9_path)
                                                    original_image_corr_9 = image_corr_9.subsample(3,3) # resize image using subsample

                                                    corr_9_im_label = Label(corr_image_frame,image=original_image_corr_9)
                                                    corr_9_im_label.image = original_image_corr_9 # keep a reference
                                                    corr_9_im_label.place(x=387, y=118)   

                                                    def mouse_on_corr_9(event):
                                                        image_corr_9 = PhotoImage(file=corr_9_path)
                                                        original_image_corr_9 = image_corr_9.subsample(2,2) # resize image using subsample

                                                        corr_9_im_label = Label(corr_image_frame,image=original_image_corr_9)
                                                        corr_9_im_label.image = original_image_corr_9 # keep a reference
                                                        corr_9_im_label.place(x=387, y=118) 

                                                        return                                                       

                                                    corr_9_im_label.bind('<Enter>',mouse_on_corr_9)                              

                                                    def rst_cor():
                                                        print("Reset")
                                                        cmb.set('')
                                                        cmb1.set('')
                                                        cmb2.set('')        
                                                        cmb3.set('')        
                                                        cmb4.set('')       
                                                        cmb5.set('')     
                                                        cmb6.set('')         
                                                        cmb7.set('')  
                                                        cmb8.set('')                                                                                                                                                                                                                                                                                       
                                                        number_of_param.set('')
                                                        new_text = " "
                                                        e1.delete(0, tk.END)
                                                        e1.insert(0, new_text)
                                                        cmb.place_forget()
                                                        cmb1.place_forget()
                                                        cmb2.place_forget()       
                                                        cmb3.place_forget() 
                                                        cmb4.place_forget()    
                                                        cmb5.place_forget()       
                                                        cmb6.place_forget()   
                                                        cmb7.place_forget()  
                                                        cmb8.place_forget()                                                                                                                                                                                                                                                                                                     
                                                        corr_9_im_label.image =''                                                                        

                                                    plt_rst_corr=PhotoImage(file="reset.png")  
                                                    sub_plt_rst_corr=plt_rst_corr.subsample(4,4)

                                                    button_corr_rst = Button(corr_input_frame, text="Reset", fg='#026084', command=rst_cor, image=sub_plt_rst_corr, compound=LEFT, width=130)
                                                    button_corr_rst.image=sub_plt_rst_corr
                                                    button_corr_rst.place(x=88, y=466)
                                                    button_arr.append(button_corr_rst)

                                                    ttk.Separator(corr_input_frame).place(x=75, y=536, relwidth=0.29)

                                                    def corr_go_to_menu():

                                                        print("Coming soon")

                                                        corr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                                        #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                                        corr_apr=Label(corr_frame, width=20, bg='white').place(x=10, y=10)

                                                        corr_inner_frame=Frame(corr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                                        #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                                        corr_input_frame=Frame(corr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                                        corr_image_frame=Frame(corr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                                        Label(corr_image_frame, bg='white').place(x=565, y=95)                          

                                                        print("Correlation frame has been destroyed.")      

                                                    plt_up=PhotoImage(file="up.png")  
                                                    sub_plt_up=plt_up.subsample(10,10)     

                                                    button_corr_go_to_menu=Button(corr_input_frame, text="Go to menu", fg='#026084', command=corr_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                                    button_corr_go_to_menu.image=sub_plt_up
                                                    button_corr_go_to_menu.place(x=88, y=538)
                                                    button_arr.append(button_corr_go_to_menu)

                                                # Creating a photoimage object to use image 
                                                plt_gen_corr = PhotoImage(file = "images.png") 
                                                sub_plt_gen_corr = plt_gen_corr.subsample(4, 4)    

                                                button_corr_gen = Button(corr_input_frame, text="Generate", fg='#026084', command=cor_gen, image=sub_plt_gen_corr, compound=LEFT)
                                                button_corr_gen.image=sub_plt_gen_corr
                                                button_corr_gen.place(x=88, y=401)
                                                button_arr.append(button_corr_gen)

                                                ttk.Separator(corr_input_frame).place(x=75, y=396, relwidth=0.29) 

                                            cmb8 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                            cmb8.place(x=75, y=365)
                                            cmb8.bind('<<ComboboxSelected>>', on_ninth_select)

                                        cmb7 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                        cmb7.place(x=75, y=342)
                                        cmb7.bind('<<ComboboxSelected>>', on_eight_select)

                                    cmb6 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                    cmb6.place(x=75, y=319)
                                    cmb6.bind('<<ComboboxSelected>>', on_seventh_select)

                                cmb5 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                cmb5.place(x=75, y=296)
                                cmb5.bind('<<ComboboxSelected>>', on_sixth_select)

                            cmb4 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)

        if (e1.get() == "10" or e1.get() == " 10"):
            # Getting dynamically path for appropriate DB file and backup directory
            file_path = sys.path[0] + '\\' + db

            if not find_plathform():
                file_path = file_path.replace("\\", "/")

            data = pd.read_csv(file_path)

            data = pd.read_csv(file_path, nrows=1).columns.tolist()

            columns = data

            def on_first_select(event=None):
                column_names.clear()
                file_path = sys.path[0] + '\\' + db
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)

                data = pd.read_csv(file_path, nrows=1).columns.tolist()

                frst_curr_val = cmb.get()

                column_names.append(frst_curr_val)

                second_data = data

                for item in data:
                    if item == frst_curr_val:
                        second_data.remove(item)

                def on_second_select(event=None):
                    second_curr_val = cmb1.get()

                    if len(column_names) > 1:
                        column_names.pop(1)

                    column_names.append(second_curr_val)

                    third_data = second_data

                    for item in second_data:
                        if item == second_curr_val:
                            third_data.remove(item)

                    def on_third_select(event=None):
                        third_curr_val = cmb2.get()

                        if len(column_names) > 2:
                            column_names.pop(2)

                        column_names.append(third_curr_val)

                        forth_data = third_data

                        for item in third_data:
                            if item == third_curr_val:
                                forth_data.remove(item)

                        def on_forth_select(event=None):
                            forth_curr_val = cmb3.get()

                            if len(column_names) > 3:
                                column_names.pop(3)

                            column_names.append(forth_curr_val)

                            fifth_data = forth_data

                            for item in forth_data:
                                if item == forth_curr_val:
                                    fifth_data.remove(item)

                            def on_fifth_select(event=None):
                                fifth_curr_val = cmb4.get()

                                if len(column_names) > 4:
                                    column_names.pop(4)

                                column_names.append(fifth_curr_val)

                                sixth_data = fifth_data

                                for item in fifth_data:
                                    if item == fifth_curr_val:
                                        sixth_data.remove(item)

                                def on_sixth_select(event=None):
                                    sixth_curr_val = cmb5.get()

                                    if len(column_names) > 5:
                                        column_names.pop(5)

                                    column_names.append(sixth_curr_val)

                                    seventh_data = sixth_data

                                    for item in sixth_data:
                                        if item == sixth_curr_val:
                                            seventh_data.remove(item)

                                    def on_seventh_select(event=None):
                                        seventh_curr_val = cmb6.get()

                                        if len(column_names) > 6:
                                            column_names.pop(6)

                                        column_names.append(seventh_curr_val)

                                        eight_data = seventh_data

                                        for item in seventh_data:
                                            if item == seventh_curr_val:
                                                eight_data.remove(item)

                                        def on_eight_select(event=None):
                                            eight_curr_val = cmb7.get()

                                            if len(column_names) > 7:
                                                column_names.pop(7)

                                            column_names.append(eight_curr_val)

                                            ninth_data = eight_data

                                            for item in eight_data:
                                                if item == eight_curr_val:
                                                    ninth_data.remove(item)

                                            def on_ninth_select(event=None):
                                                ninth_curr_val = cmb8.get()

                                                if len(column_names) > 8:
                                                    column_names.pop(8)

                                                column_names.append(ninth_curr_val)

                                                tenth_data = ninth_data

                                                for item in ninth_data:
                                                    if item == ninth_curr_val:
                                                        tenth_data.remove(item)

                                                def on_tenth_select(event=None):
                                                    tenth_curr_val = cmb9.get()

                                                    if len(column_names) > 9:
                                                        column_names.pop(9)

                                                    column_names.append(tenth_curr_val)

                                                    def cor_gen():
                                                        print("Corr Generation")
                                                        correlation_func_parameters = ['Ֆակուլտետ',
                                                                                       'Ուսանողի անուն',
                                                                                       'Ուսանողի սեռ',
                                                                                       'Ծննդավայր (երկիր)',
                                                                                       'Ծննդավայր (քաղաք/գյուղ)',
                                                                                       'Ընդունման տարեթիվ',
                                                                                       'Առարկա',
                                                                                       'Առաջին միջանկյալ ստուգում',
                                                                                       'Երկրորդ միջանկյալ ստուգում',
                                                                                       'Ամփոփիչ քննություն']

                                                        file_path = sys.path[0] + '\\' + db

                                                        if not find_plathform():
                                                            file_path = file_path.replace("\\", "/")
                                                        df = pd.read_csv(file_path)[correlation_func_parameters]
                                                        print(column_names)

                                                        corr_10_path="images/correlation/9/corr_10.png"

                                                        image_corr_10 = PhotoImage(file=corr_10_path)
                                                        original_image_corr_10 = image_corr_10.subsample(3,3) # resize image using subsample

                                                        corr_10_im_label = Label(corr_image_frame,image=original_image_corr_10)
                                                        corr_10_im_label.image = original_image_corr_10 # keep a reference
                                                        corr_10_im_label.place(x=387, y=118)   

                                                        def mouse_on_corr_10(event):
                                                            image_corr_10 = PhotoImage(file=corr_10_path)
                                                            original_image_corr_10 = image_corr_10.subsample(2,2) # resize image using subsample

                                                            corr_10_im_label = Label(corr_image_frame,image=original_image_corr_10)
                                                            corr_10_im_label.image = original_image_corr_10 # keep a reference
                                                            corr_10_im_label.place(x=387, y=118) 

                                                            return                                                       

                                                        corr_10_im_label.bind('<Enter>',mouse_on_corr_10)                              

                                                        def rst_cor():
                                                            print("Reset")
                                                            cmb.set('')
                                                            cmb1.set('')
                                                            cmb2.set('')        
                                                            cmb3.set('')        
                                                            cmb4.set('')       
                                                            cmb5.set('')     
                                                            cmb6.set('')         
                                                            cmb7.set('')  
                                                            cmb8.set('') 
                                                            cmb9.set('')                                                                                                                                                                                                                                                                                                                                                    
                                                            number_of_param.set('')
                                                            new_text = " "
                                                            e1.delete(0, tk.END)
                                                            e1.insert(0, new_text)
                                                            cmb.place_forget()
                                                            cmb1.place_forget()
                                                            cmb2.place_forget()       
                                                            cmb3.place_forget() 
                                                            cmb4.place_forget()    
                                                            cmb5.place_forget()       
                                                            cmb6.place_forget()   
                                                            cmb7.place_forget()  
                                                            cmb8.place_forget()   
                                                            cmb9.place_forget()                                                                                                                                                                                                                                                                                                                                                                
                                                            corr_10_im_label.image =''                                                                        

                                                        plt_rst_corr=PhotoImage(file="reset.png")  
                                                        sub_plt_rst_corr=plt_rst_corr.subsample(7,7)

                                                        button_corr_rst = Button(corr_input_frame, text="Reset", fg='#026084', command=rst_cor, image=sub_plt_rst_corr, compound=LEFT, width=130)
                                                        button_corr_rst.image=sub_plt_rst_corr
                                                        button_corr_rst.place(x=88, y=484)
                                                        button_arr.append(button_corr_rst)

                                                        ttk.Separator(corr_input_frame).place(x=75, y=530, relwidth=0.29)

                                                        def corr_go_to_menu():

                                                            print("Coming soon")

                                                            corr_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                                                            #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                                                            corr_apr=Label(corr_frame, width=20, bg='white').place(x=10, y=10)

                                                            corr_inner_frame=Frame(corr_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                                                            #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                                                            corr_input_frame=Frame(corr_inner_frame, width=300, height=500, bg='white').place(x=65, y=85)

                                                            corr_image_frame=Frame(corr_frame, width=490, height=500, bg='white').place(x=385, y=85)

                                                            Label(corr_image_frame, bg='white').place(x=565, y=95)                          

                                                            print("Correlation frame has been destroyed.")      

                                                        plt_up=PhotoImage(file="up.png")  
                                                        sub_plt_up=plt_up.subsample(10,10)     

                                                        button_corr_go_to_menu=Button(corr_input_frame, text="Go to menu", fg='#026084', command=corr_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                                                        button_corr_go_to_menu.image=sub_plt_up
                                                        button_corr_go_to_menu.place(x=88, y=534)
                                                        button_arr.append(button_corr_go_to_menu)

                                                    # Creating a photoimage object to use image 
                                                    plt_gen_corr = PhotoImage(file = "images.png") 
                                                    sub_plt_gen_corr = plt_gen_corr.subsample(5, 5)

                                                    button_corr_gen = Button(corr_input_frame, text="Generate", fg='#026084', command=cor_gen, image=sub_plt_gen_corr, compound=LEFT)
                                                    button_corr_gen.image=sub_plt_gen_corr
                                                    button_corr_gen.place(x=88, y=424)
                                                    button_arr.append(button_corr_gen)

                                                    ttk.Separator(corr_input_frame).place(x=75, y=419, relwidth=0.29) 

                                                cmb9 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28,height=5)
                                                cmb9.place(x=75, y=388)
                                                cmb9.bind('<<ComboboxSelected>>', on_tenth_select)

                                            cmb8 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                            cmb8.place(x=75, y=365)
                                            cmb8.bind('<<ComboboxSelected>>', on_ninth_select)

                                        cmb7 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                        cmb7.place(x=75, y=342)
                                        cmb7.bind('<<ComboboxSelected>>', on_eight_select)

                                    cmb6 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                    cmb6.place(x=75, y=319)
                                    cmb6.bind('<<ComboboxSelected>>', on_seventh_select)

                                cmb5 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                                cmb5.place(x=75, y=296)
                                cmb5.bind('<<ComboboxSelected>>', on_sixth_select)

                            cmb4 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                            cmb4.place(x=75, y=273)
                            cmb4.bind('<<ComboboxSelected>>', on_fifth_select)

                        cmb3 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                        cmb3.place(x=75, y=251)
                        cmb3.bind('<<ComboboxSelected>>', on_forth_select)

                    cmb2 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                    cmb2.place(x=75, y=228)
                    cmb2.bind('<<ComboboxSelected>>', on_third_select)

                cmb1 = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
                cmb1.place(x=75, y=205)
                cmb1.bind('<<ComboboxSelected>>', on_second_select)

            cmb = ttk.Combobox(corr_input_frame, values=data, state='readonly', width=28, height=5)
            cmb.place(x=75, y=182)
            cmb.bind('<<ComboboxSelected>>', on_first_select)
            
    if show_correlation_analysis == True:
        Number_Param_Lbl = Label(corr_input_frame, text="Number of Parameters: [2:10]", width=29,height=2,font=("Sans", 10),bd=3, relief=SUNKEN).place(x=75, y=95)
        number_of_param = ttk.Combobox(corr_input_frame, values=[2, 3, 4, 5, 6, 7, 8, 9, 10], state='readonly', width=28, height=5)
        number_of_param.place(x=75, y=136)
        number_of_param.bind('<<ComboboxSelected>>', lambda event: correlation_func(e1=number_of_param))
        labelForMenuCorr = tk.Label(corr_input_frame, text="Choose correlation input values", width=29,height=1,font=("Sans", 10),bd=2, relief=SUNKEN)
        labelForMenuCorr.place(x=75, y=159)

    def jointplot_func(event=None):
        print("jointplot_func")

        column_names.clear()
        file_path = sys.path[0] + '\\' + db
        if not find_plathform():
            file_path = file_path.replace("\\", "/")
        data = pd.read_csv(file_path)

        data = pd.read_csv(file_path, nrows=1).columns.tolist()

        frst_curr_val = cmb.get()

        column_names.append(frst_curr_val)

        second_data = data

        for item in data:
            if item == frst_curr_val:
                second_data.remove(item)

        def on_second_select(event=None):
            second_curr_val = cmb1.get()

            if len(column_names) > 1:
                column_names.pop(1)

            column_names.append(second_curr_val)

            def cls_gen():
                print("Cluster Generation:")
                jointplot_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ', 'Ծննդավայր (երկիր)',
                                             'Ծննդավայր (քաղաք/գյուղ)', 'Ընդունման տարեթիվ', 'Առարկա',
                                             'Առաջին միջանկյալ ստուգում', 'Երկրորդ միջանկյալ ստուգում',
                                             'Ամփոփիչ քննություն']

                # Getting dynamically path for appropriate DB file and backup directory
                file_path = sys.path[0] + '\\' + db

                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                df = pd.read_csv(file_path, skip_blank_lines=True, na_values='NaN', verbose=True)[
                    jointplot_func_parameters]

                lb_make = LabelEncoder()
                df["Ֆակուլտետ"] = lb_make.fit_transform(df["Ֆակուլտետ"])
                df["Ուսանողի անուն"] = lb_make.fit_transform(df["Ուսանողի անուն"])
                df["Ծննդավայր (երկիր)"] = lb_make.fit_transform(df["Ծննդավայր (երկիր)"])
                df["Ծննդավայր (քաղաք/գյուղ)"] = lb_make.fit_transform(df["Ծննդավայր (քաղաք/գյուղ)"])
                df["Առարկա"] = lb_make.fit_transform(df["Առարկա"])



                def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png')):
                    """
                    Get the latest image file in the given directory
                    """

                    # get filepaths of all files and dirs in the given dir
                    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                    # filter out directories, no-extension, and wrong extension files
                    valid_files = [f for f in valid_files if '.' in f and \
                        f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                    if not valid_files:
                        raise ValueError("No valid images in %s" % dirpath)

                    return max(valid_files, key=os.path.getmtime) 


                sns.jointplot(x=column_names[0], y=column_names[1], data=df, kind='kde', fit_reg=True, size=8)
                mngr = plt.get_current_fig_manager()
                mngr.window.setGeometry(400, 50, 830, 930)
                plt.savefig(
                    'images/jointplot/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                     "") + '.png')

                image_path=get_latest_image('images/jointplot/','png')             
                image = PhotoImage(file=image_path)
                original_image = image.subsample(2,2) # resize image using subsample


                j_im_label = Label(jnt_image_frame,image=original_image)
                j_im_label.image = original_image # keep a reference
                j_im_label.place(x=387, y=118)

                def rst_jnplt():
                    print("Reset")
                    cmb.set('')
                    cmb1.set('')
                    j_im_label.image =''


                plt_rst=PhotoImage(file="reset.png")  
                sub_plt_rst=plt_rst.subsample(4,4)

                button_jnplt_rst = Button(jnt_input_frame, text="Reset", fg='#026084', command=rst_jnplt, image=sub_plt_rst, compound=LEFT, width=130)
                button_jnplt_rst.image=sub_plt_rst
                button_jnplt_rst.place(x=88, y=270)
                button_arr.append(button_jnplt_rst)

                ttk.Separator(jnt_input_frame).place(x=75, y=350, relwidth=0.29)


                def jnt_go_to_menu():
                    print("Coming soon")
                    #jnt_frame.grid_forget()
                    #jnt_inner_frame.grid_forget()
                    #jnt_input_frame.grid_forget()
                    #jnt_image_frame.grid_forget()
                    jnt_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                    lbl=Label(jnt_frame, width=20, bg='white').place(x=10, y=10)

                    jnt_inner_frame=Frame(jnt_frame, width=80, height=150, bg='white',).grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                    #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                    jnt_input_frame=Frame(jnt_inner_frame, width=300, height=380, bg='white').place(x=65, y=85)

                    jnt_image_frame=Frame(jnt_frame, width=490, height=500, bg='white').place(x=385, y=85)
                    print("Jointplot frame has been destroyed.") 


                plt_up=PhotoImage(file="up.png")  
                sub_plt_up=plt_up.subsample(4,4)     

                button_jnt_go_to_menu=Button(jnt_input_frame, text="Go to menu", fg='#026084', command=jnt_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                button_jnt_go_to_menu.image=sub_plt_up
                button_jnt_go_to_menu.place(x=88, y=360)
                button_arr.append(button_jnt_go_to_menu)

			# Creating a photoimage object to use image 
            plt_gen = PhotoImage(file = "images.png") 
            sub_plt_gen = plt_gen.subsample(4, 4)    

            button_clust_gen = Button(jnt_input_frame, text="Generate", fg='#026084', command=cls_gen, image=sub_plt_gen, compound=LEFT)
            button_clust_gen.image=sub_plt_gen
            button_clust_gen.place(x=88, y=200)
            button_arr.append(button_clust_gen)

            ttk.Separator(jnt_input_frame).place(x=75, y=190, relwidth=0.29)

        cmb1 = ttk.Combobox(jnt_input_frame, values=data, state='readonly', width=28,height=5)
        cmb1.place(x=75, y=159)
        cmb1.bind('<<ComboboxSelected>>', on_second_select)
        button_arr.append(cmb1)

    if show_jointplot_analysis == True:
        file_path = sys.path[0] + '\\' + db

        if not find_plathform():
            file_path = file_path.replace("\\", "/")

        data = pd.read_csv(file_path)

        labelForMenu = tk.Label(jnt_input_frame, text="Choose jointplot input value", width=29,height=2,font=("Sans", 10),bd=3, relief=SUNKEN).place(x=75, y=95)

        data = pd.read_csv(file_path, nrows=1).columns.tolist()

        columns = data
        cmb = ttk.Combobox(jnt_input_frame, values=data, state='readonly', width=28, height=5)
        cmb.place(x=75, y=136)
        button_arr.append(cmb)
        cmb.bind('<<ComboboxSelected>>', jointplot_func)

    def cluster_func(event=None):
        print('cluster_func')

        column_names.clear()
        file_path = sys.path[0] + '\\' + db
        if not find_plathform():
            file_path = file_path.replace("\\", "/")
        data = pd.read_csv(file_path)

        data = pd.read_csv(file_path, nrows=1).columns.tolist()

        frst_curr_val = cmb.get()

        column_names.append(frst_curr_val)

        second_data = data

        for item in data:
            if item == frst_curr_val:
                second_data.remove(item)

        def on_second_select(event=None):
            second_curr_val = cmb1.get()

            if len(column_names) > 1:
                column_names.pop(1)

            column_names.append(second_curr_val)

            def cls_gen_2():
                print("Cluster Generation:")
                cluster_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ', 'Ծննդավայր (երկիր)',
                                           'Ծննդավայր (քաղաք/գյուղ)', 'Ընդունման տարեթիվ', 'Առարկա',
                                           'Առաջին միջանկյալ ստուգում', 'Երկրորդ միջանկյալ ստուգում',
                                           'Ամփոփիչ քննություն']  # Create sublist [First_Exam, Second_Exam, Final_Exam]

                # DB file name for Jointplot algorithm
                cluster_points = 50  # 219 was working very slowly

                # Getting dynamically path for appropriate DB file and backup directory
                file_path = sys.path[0] + '\\' + db

                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                data = pd.read_csv(file_path)
                lb_make = LabelEncoder()

                data["Ֆակուլտետ"] = lb_make.fit_transform(data["Ֆակուլտետ"])
                data["Ուսանողի անուն"] = lb_make.fit_transform(data["Ուսանողի անուն"])
                data["Ծննդավայր (երկիր)"] = lb_make.fit_transform(data["Ծննդավայր (երկիր)"])
                data["Ծննդավայր (քաղաք/գյուղ)"] = lb_make.fit_transform(data["Ծննդավայր (քաղաք/գյուղ)"])
                data["Առարկա"] = lb_make.fit_transform(data["Առարկա"])

                def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png')):
                    """
                    Get the latest image file in the given directory
                    """

                    # get filepaths of all files and dirs in the given dir
                    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                    # filter out directories, no-extension, and wrong extension files
                    valid_files = [f for f in valid_files if '.' in f and \
                        f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                    if not valid_files:
                        raise ValueError("No valid images in %s" % dirpath)

                    return max(valid_files, key=os.path.getmtime)                

                inform = {column_names[0]: data[column_names[0]][0:250],
                          column_names[1]: data[column_names[1]][0:250]}
                data = DataFrame(inform, columns=[column_names[0], column_names[1]])

                plt.figure(figsize=(10, 5))
                plt.scatter(data[column_names[0]], data[column_names[1]])
                plt.xlabel(column_names[0])
                plt.ylabel(column_names[1])
                mngr1 = plt.get_current_fig_manager()
                mngr1.window.setGeometry(10, 30, 750, 450)
                plt.savefig(
                    'images/clustering/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                      "") + '.png')

                clust_1_path=get_latest_image("images/clustering/",'png')         
                image_clust_1 = PhotoImage(file=clust_1_path)
                original_image_clust_1= image_clust_1.subsample(5,3) # resize image using subsample

                clust_1_im_label = Label(clust_image_frame,image=original_image_clust_1)
                clust_1_im_label.image=original_image_clust_1
                clust_1_im_label.place(x=387, y=118)  

                x = data.copy()
                kmeans = KMeans(2)
                kmeans.fit(x)

                clusters = x.copy()
                clusters['cluster_pred'] = kmeans.fit_predict(x)

                plt.figure(figsize=(10, 5))
                plt.scatter(clusters[column_names[0]], clusters[column_names[1]], c=clusters['cluster_pred'],
                            cmap='rainbow')
                plt.xlabel(column_names[0])
                plt.ylabel(column_names[1])
                mngr2 = plt.get_current_fig_manager()
                mngr2.window.setGeometry(770, 30, 900, 450)
                plt.savefig(
                    'images/clustering/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                      "") + '.png')

                clust_2_path=get_latest_image("images/clustering/",'png')         
                image_clust_2 = PhotoImage(file=clust_2_path)
                original_image_clust_2= image_clust_2.subsample(5,3) # resize image using subsample

                clust_2_im_label = Label(clust_image_frame,image=original_image_clust_2)
                clust_2_im_label.image=original_image_clust_2
                clust_2_im_label.place(x=627, y=118)                 

                from sklearn import preprocessing
                x_scaled = preprocessing.scale(x)
                x_scaled

                wcss = []
                for i in range(1, cluster_points):
                    kmeans = KMeans(i)
                    kmeans.fit(x_scaled)
                    wcss.append(kmeans.inertia_)

                plt.figure(figsize=(10, 5))
                plt.plot(range(1, cluster_points), wcss)
                plt.xlabel('Number of clusters')
                plt.ylabel('WCSS')
                mngr3 = plt.get_current_fig_manager()
                mngr3.window.setGeometry(10, 505, 1000, 530)
                plt.savefig(
                    'images/clustering/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                      "") + '.png')


                clust_3_path=get_latest_image("images/clustering/",'png')         
                image_clust_3 = PhotoImage(file=clust_3_path)
                original_image_clust_3= image_clust_3.subsample(5,3) # resize image using subsample

                clust_3_im_label = Label(clust_image_frame,image=original_image_clust_3)
                clust_3_im_label.image=original_image_clust_3
                clust_3_im_label.place(x=387, y=308)                

                kmeans_new = KMeans(4)
                kmeans.fit(x_scaled)
                cluster_new = x.copy()
                cluster_new['cluster_pred'] = kmeans_new.fit_predict(x_scaled)
                cluster_new

                plt.figure(figsize=(10, 5))
                plt.scatter(cluster_new[column_names[0]], cluster_new[column_names[1]],
                            c=cluster_new['cluster_pred'], cmap='rainbow')
                plt.xlabel(column_names[0])
                plt.ylabel(column_names[1])
                mngr4 = plt.get_current_fig_manager()
                mngr4.window.setGeometry(1020, 505, 700, 530)
                plt.savefig(
                    'images/clustering/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                      "") + '.png')

                clust_4_path=get_latest_image("images/clustering/",'png')         
                image_clust_4 = PhotoImage(file=clust_4_path)
                original_image_clust_4= image_clust_4.subsample(5,3) # resize image using subsample

                clust_4_im_label = Label(clust_image_frame,image=original_image_clust_4)
                clust_4_im_label.image=original_image_clust_4
                clust_4_im_label.place(x=627, y=308)     


                def mouse_on_clust_1(event):
                    image_clust_1 = PhotoImage(file=clust_1_path)
                    original_image_clust_1 = image_clust_1.subsample(4,2) # resize image using subsample

                    clust_1_im_label = Label(clust_image_frame,image=original_image_clust_1)
                    clust_1_im_label.image = original_image_clust_1 # keep a reference
                    clust_1_im_label.place(x=387, y=118) 

                    return          

                def mouse_on_clust_2(event):
                    image_clust_2 = PhotoImage(file=clust_2_path)
                    original_image_clust_2 = image_clust_2.subsample(4,2) # resize image using subsample

                    clust_2_im_label = Label(clust_image_frame,image=original_image_clust_2)
                    clust_2_im_label.image = original_image_clust_2 # keep a reference
                    clust_2_im_label.place(x=627, y=118)  

                    return        

                def mouse_on_clust_3(event):
                    image_clust_3 = PhotoImage(file=clust_3_path)
                    original_image_clust_3 = image_clust_3.subsample(4,2) # resize image using subsample

                    clust_3_im_label = Label(clust_image_frame,image=original_image_clust_3)
                    clust_3_im_label.image = original_image_clust_3 # keep a reference
                    clust_3_im_label.place(x=387, y=308) 

                    return        

                def mouse_on_clust_4(event):
                    image_clust_4 = PhotoImage(file=clust_4_path)
                    original_image_clust_4 = image_clust_4.subsample(4,2) # resize image using subsample

                    clust_4_im_label = Label(clust_image_frame,image=original_image_clust_4)
                    clust_4_im_label.image = original_image_clust_4 # keep a reference
                    clust_4_im_label.place(x=627, y=308) 

                    return                                                                                  

                clust_1_im_label.bind('<Enter>',mouse_on_clust_1)                    
                clust_2_im_label.bind('<Enter>',mouse_on_clust_2)  
                clust_3_im_label.bind('<Enter>',mouse_on_clust_3)   
                clust_4_im_label.bind('<Enter>',mouse_on_clust_4)                                            

                def rst_clst():
                    print("Reset")
                    cmb.set('')
                    cmb1.set('')
                    clust_1_im_label.image=''
                    clust_2_im_label.image=''
                    clust_3_im_label.image=''
                    clust_4_im_label.image=''                                                            

                plt_rst=PhotoImage(file="reset.png")  
                sub_plt_rst=plt_rst.subsample(4,4)

                button_clust_rst = Button(clust_input_frame, text="Reset", fg='#026084', command=rst_clst, image=sub_plt_rst, compound=LEFT, width=130)
                button_clust_rst.image=sub_plt_rst
                button_clust_rst.place(x=88, y=270)
                button_arr.append(button_clust_rst)

                ttk.Separator(clust_input_frame).place(x=75, y=350, relwidth=0.29)


                def clust_go_to_menu():
                    print("Coming soon")
                    #jnt_frame.grid_forget()
                    #jnt_inner_frame.grid_forget()
                    #jnt_input_frame.grid_forget()
                    #jnt_image_frame.grid_forget()

                    clust_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                    #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                    lbl_clust=Label(clust_frame, width=20, bg='white').place(x=10, y=10)

                    clust_inner_frame=Frame(clust_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                    #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                    clust_input_frame=Frame(clust_inner_frame, width=300, height=380, bg='white').place(x=65, y=85)

                    clust_image_frame=Frame(clust_frame, width=490, height=500, bg='white').place(x=385, y=85)

                    Label(clust_image_frame, bg='white').place(x=565, y=95)  

                    print("Clustering frame has been destroyed.") 


                plt_up=PhotoImage(file="up.png")  
                sub_plt_up=plt_up.subsample(4,4)     

                button_clust_go_to_menu=Button(clust_input_frame, text="Go to menu", fg='#026084', command=clust_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                button_clust_go_to_menu.image=sub_plt_up
                button_clust_go_to_menu.place(x=88, y=360)
                button_arr.append(button_clust_go_to_menu)

            # Creating a photoimage object to use image 
            plt_gen = PhotoImage(file = "images.png") 
            sub_plt_gen = plt_gen.subsample(4, 4)    

            button_clust_gen = Button(clust_input_frame, text="Generate", fg='#026084', command=cls_gen_2, image=sub_plt_gen, compound=LEFT)
            button_clust_gen.image=sub_plt_gen
            button_clust_gen.place(x=88, y=200)
            button_arr.append(button_clust_gen)

            ttk.Separator(clust_input_frame).place(x=75, y=190, relwidth=0.29)

        cmb1 = ttk.Combobox(clust_input_frame, values=data, state='readonly', width=28,height=5)
        cmb1.place(x=75, y=159)
        cmb1.bind('<<ComboboxSelected>>', on_second_select)
        button_arr.append(cmb1)

    if show_cluster_analysis == True:
        file_path = sys.path[0] + '\\' + db

        if not find_plathform():
            file_path = file_path.replace("\\", "/")

        data = pd.read_csv(file_path)

        labelForMenu = tk.Label(clust_input_frame, text="Choose clustering input value", width=29,height=2,font=("Sans", 10),bd=3, relief=SUNKEN).place(x=75, y=95)

        data = pd.read_csv(file_path, nrows=1).columns.tolist()

        columns = data
        cmb = ttk.Combobox(clust_input_frame, values=data, state='readonly', width=28, height=5)
        cmb.place(x=75, y=136)
        button_arr.append(cmb)        
        cmb.bind('<<ComboboxSelected>>', cluster_func)


    def regression_func(event=None):
        column_names.clear()
        file_path = sys.path[0] + '\\' + db

        if not find_plathform():
            file_path = file_path.replace("\\", "/")

        data = pd.read_csv(file_path)

        data = pd.read_csv(file_path, nrows=1).columns.tolist()

        frst_curr_val = cmb.get()

        print("reg cmb",frst_curr_val)

        column_names.append(frst_curr_val)

        second_data = data

        for item in data:
            if item == frst_curr_val:
                second_data.remove(item)

        def on_second_select(event=None):
            second_curr_val = cmb1.get()

            if len(column_names) > 1:
                column_names.pop(1)

            column_names.append(second_curr_val)

            def reg_gen():
                print("Regression Generation:")
                regression_func_parameters = ['Ֆակուլտետ', 'Ուսանողի անուն', 'Ուսանողի սեռ',
                                              'Ծննդավայր (երկիր)',
                                              'Ծննդավայր (քաղաք/գյուղ)', 'Ընդունման տարեթիվ', 'Առարկա',
                                              'Առաջին միջանկյալ ստուգում', 'Երկրորդ միջանկյալ ստուգում',
                                              'Ամփոփիչ քննություն']
                # DB file name for Regression algorithm
                folder_name = ['regression']
                txt_file_name = ['regression.txt', 'regression_ending.txt']

                # Getting dynamically path for appropriate DB file and backup directory
                absolute_path = sys.path[0]
                file_path = sys.path[0] + '\\' + db

                dir_name = absolute_path + '\\' + folder_name[0]
                abs_path = dir_name + '\\' + txt_file_name[0]

                pd.set_option('display.max_columns', None)
                pd.set_option('display.max_rows', None)

                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                dataset = pd.read_csv(file_path)[regression_func_parameters]

                lb_make = LabelEncoder()
                dataset['Ֆակուլտետ'] = lb_make.fit_transform(dataset['Ֆակուլտետ'])
                dataset['Ուսանողի անուն'] = lb_make.fit_transform(dataset['Ուսանողի անուն'])     
                dataset['Ծննդավայր (երկիր)'] = lb_make.fit_transform(dataset['Ծննդավայր (երկիր)'])          
                dataset['Ծննդավայր (քաղաք/գյուղ)'] = lb_make.fit_transform(dataset['Ծննդավայր (քաղաք/գյուղ)']) 
                dataset['Առարկա'] = lb_make.fit_transform(dataset['Առարկա'])   

                def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png','txt')):
                    """
                    Get the latest image file in the given directory
                    """

                    # get filepaths of all files and dirs in the given dir
                    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                    # filter out directories, no-extension, and wrong extension files
                    valid_files = [f for f in valid_files if '.' in f and \
                        f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                    if not valid_files:
                        raise ValueError("No valid images in %s" % dirpath)

                    return max(valid_files, key=os.path.getmtime)  


                X = dataset[column_names[0]].values.reshape(-1, 1)
                y = dataset[column_names[1]].values.reshape(-1, 1)

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

                regressor = LinearRegression()
                regressor.fit(X_train, y_train)  # training the algorithm

                # To retrieve the intercept:
                print(regressor.intercept_)  # For retrieving the slope:
                print(regressor.coef_)

                y_pred = regressor.predict(X_test)

                mae = metrics.mean_absolute_error(y_test, y_pred)
                mse = metrics.mean_squared_error(y_test, y_pred)
                rmqe = np.sqrt(metrics.mean_squared_error(y_test, y_pred))                

                df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
                print(df, file=open('Regression.txt', 'w'))
                print('\nError measures:', file=open('Regression.txt', 'a+'))   
                print('Mean Absolute Error: ' + str(mae), file=open('Regression.txt', 'a+'))    
                print('Mean Squared Error: ' + str(mse), file=open('Regression.txt', 'a+'))    
                print('Root Mean Squared Error: ' + str(rmqe), file=open('Regression.txt', 'a+'))                                                      

                # Taking backup values from above graphs and puting appropriate directory
                try:
                    # Create target Directory
                    os.mkdir(dir_name)
                    print("Directory ", dir_name, " created.")
                except FileExistsError:
                    print("Directory ", dir_name, " already exists.")

                # Writing to file
                file = open(abs_path, 'w', encoding="utf8")
                file.write(str(df))
                file.close()

                now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                now = str(now)
                newname = 'regression_' + now + '.txt'
                os.rename('Regression.txt', newname)
                shutil.move(newname,  "images/regression/")                                                                    


                plt.figure(figsize=(10, 5))
                plt.tight_layout()
                seabornInstance.distplot(dataset[column_names[0]])
                mngr1 = plt.get_current_fig_manager()
                mngr1.window.setGeometry(770, 30, 900, 450)
                plt.savefig(
                    'images/regression/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                      "") + '.png')

                reg_1_path=get_latest_image("images/regression/",'png')          
                image_reg_1 = PhotoImage(file=reg_1_path)
                original_image_reg_1 = image_reg_1.subsample(4,4) # resize image using subsample

                reg_1_im_label = Label(reg_image_frame,image=original_image_reg_1)
                reg_1_im_label.image = original_image_reg_1 # keep a reference
                reg_1_im_label.place(x=387, y=118)                

                plt.figure(figsize=(10, 5))
                plt.tight_layout()
                seabornInstance.distplot(dataset[column_names[1]])
                mngr2 = plt.get_current_fig_manager()
                mngr2.window.setGeometry(770, 30, 900, 450)
                plt.savefig(
                    'images/regression/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                      "") + '.png')     

                reg_2_path=get_latest_image("images/regression/",'png')          
                image_reg_2 = PhotoImage(file=reg_2_path)
                original_image_reg_2 = image_reg_2.subsample(4,4) # resize image using subsample

                reg_2_im_label = Label(reg_image_frame,image=original_image_reg_2)
                reg_2_im_label.image = original_image_reg_2 # keep a reference
                reg_2_im_label.place(x=627, y=118)                                                                                                                  

                df1 = df.head(35)
                df1.plot(kind='bar', figsize=(10, 6))
                plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
                plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
                mngr3 = plt.get_current_fig_manager()
                mngr3.window.setGeometry(10, 505, 1000, 530)
                plt.savefig(
                    'images/regression/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                      "") + '.png')       

                reg_3_path=get_latest_image("images/regression/",'png')          
                image_reg_3 = PhotoImage(file=reg_3_path)
                original_image_reg_3 = image_reg_3.subsample(4,5) # resize image using subsample

                reg_3_im_label = Label(reg_image_frame,image=original_image_reg_3)
                reg_3_im_label.image = original_image_reg_3 # keep a reference
                reg_3_im_label.place(x=387, y=250)       


                def mouse_on_reg_1(event):
                    image_reg_1 = PhotoImage(file=reg_1_path)
                    original_image_reg_1 = image_reg_1.subsample(3,2) # resize image using subsample

                    reg_1_im_label = Label(reg_image_frame,image=original_image_reg_1)
                    reg_1_im_label.image = original_image_reg_1 # keep a reference
                    reg_1_im_label.place(x=387, y=118) 

                    return          

                def mouse_on_reg_2(event):
                    image_reg_2 = PhotoImage(file=reg_2_path)
                    original_image_reg_2 = image_reg_2.subsample(3,2) # resize image using subsample

                    reg_2_im_label = Label(reg_image_frame,image=original_image_reg_2)
                    reg_2_im_label.image = original_image_reg_2 # keep a reference
                    reg_2_im_label.place(x=627, y=118) 

                    return        

                def mouse_on_reg_3(event):
                    image_reg_3 = PhotoImage(file=reg_3_path)
                    original_image_reg_3 = image_reg_3.subsample(2,3) # resize image using subsample

                    reg_3_im_label = Label(reg_image_frame,image=original_image_reg_3)
                    reg_3_im_label.image = original_image_reg_3 # keep a reference
                    reg_3_im_label.place(x=387, y=250) 

                    return                                                                

                reg_1_im_label.bind('<Enter>',mouse_on_reg_1)                    
                reg_2_im_label.bind('<Enter>',mouse_on_reg_2)  
                reg_3_im_label.bind('<Enter>',mouse_on_reg_3)

                reg_txt_path = get_latest_image("images/regression/",'txt')              

                def reg_btn_click():
                    window.filename =  filedialog.askopenfile(mode='r',initialdir = "images/regression/",title = reg_txt_path,filetypes = (("txt files","*.txt"),("all files","*.*")))

                reg_txt_entry=Entry(reg_txt_frame, highlightcolor='#ababba',justify=LEFT, relief=SUNKEN, width=18)
                reg_txt_entry.insert(END,reg_txt_path)
                reg_txt_entry.place(x=637, y=490)

                reg_txt_btn=Button(reg_txt_frame, text="Browse", bd=2, activebackground='#c7c7d1',relief=SUNKEN,command=reg_btn_click).place(x=786, y=486)                                         


                def rst_reg():
                    print("Reset")
                    cmb.set('')
                    cmb1.set('')
                    new_text=" "
                    reg_1_im_label.image=''
                    reg_2_im_label.image=''
                    reg_3_im_label.image=''  
                    reg_txt_entry.delete(0, tk.END)      
                    reg_txt_entry.insert(0, new_text)                                              
                                                                                                         
                plt_rst_reg=PhotoImage(file="reset.png")  
                sub_plt_rst_reg=plt_rst_reg.subsample(4,4)

                button_reg_rst = Button(reg_input_frame, text="Reset", fg='#026084', command=rst_reg, image=sub_plt_rst_reg, compound=LEFT, width=130)
                button_reg_rst.image=sub_plt_rst_reg
                button_reg_rst.place(x=88, y=270)
                button_arr.append(button_reg_rst)

                ttk.Separator(reg_input_frame).place(x=75, y=350, relwidth=0.29)

                def reg_go_to_menu():

                    reg_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                    #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                    reg_clust=Label(reg_frame, width=20, bg='white').place(x=10, y=10)

                    reg_inner_frame=Frame(reg_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                    #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                    reg_input_frame=Frame(reg_inner_frame, width=300, height=380, bg='white').place(x=65, y=85)

                    reg_image_frame=Frame(reg_frame, width=490, height=500, bg='white').place(x=385, y=85)

                    Label(reg_image_frame, bg='white').place(x=565, y=95)         

                    reg_txt_frame=Frame(reg_image_frame, width=250, height=195, bg='white').place(x=627,y=388)

                    lbl_reg_txt=Label(reg_txt_frame, width=17, bg='white').place(x=630, y=392)                           

                    print("Regression frame has been destroyed.")      

                plt_up=PhotoImage(file="up.png")  
                sub_plt_up=plt_up.subsample(4,4)     

                button_reg_go_to_menu=Button(reg_input_frame, text="Go to menu", fg='#026084', command=reg_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                button_reg_go_to_menu.image=sub_plt_up
                button_reg_go_to_menu.place(x=88, y=360)
                button_arr.append(button_reg_go_to_menu) 

            # Creating a photoimage object to use image 
            plt_gen_reg = PhotoImage(file = "images.png") 
            sub_plt_gen_reg = plt_gen_reg.subsample(4, 4)    

            button_reg_gen = Button(reg_input_frame, text="Generate", fg='#026084', command=reg_gen, image=sub_plt_gen_reg, compound=LEFT)
            button_reg_gen.image=sub_plt_gen_reg
            button_reg_gen.place(x=88, y=200)
            button_arr.append(button_reg_gen)

            ttk.Separator(reg_input_frame).place(x=75, y=190, relwidth=0.29)

        cmb1 = ttk.Combobox(reg_input_frame, values=data, state='readonly', width=28, height=5)
        cmb1.place(x=75, y=159)
        cmb1.bind('<<ComboboxSelected>>', on_second_select)
        button_arr.append(cmb1)

    if show_regression_analysis == True:
        file_path = sys.path[0] + '\\' + db
        if not find_plathform():
            file_path = file_path.replace("\\", "/")
        data = pd.read_csv(file_path)

        labelForMenu = tk.Label(reg_input_frame, text="Choose regression input value", width=29,height=2,font=("Sans", 10),bd=3, relief=SUNKEN).place(x=75, y=95)

        data = pd.read_csv(file_path, nrows=1).columns.tolist()
        columns = data

        cmb = ttk.Combobox(reg_input_frame, values=data, state='readonly', width=28, height=5)
        cmb.place(x=75, y=136)
        cmb.bind('<<ComboboxSelected>>', regression_func)
        button_arr.append(cmb)

    def ols_func(event=None):
        print("ols_func")
        db_ols = '13_03_20 _OLS.csv' #new#
        column_names.clear()
        file_path = sys.path[0] + '\\' + db

        if not find_plathform():
            file_path = file_path.replace("\\", "/")
        data = pd.read_csv(file_path)

        data = pd.read_csv(file_path, nrows=1).columns.tolist()

        frst_curr_val = cmb.get()

        column_names.append(frst_curr_val)

        second_data = data

        for item in data:
            if item == frst_curr_val:
                second_data.remove(item)

        def on_second_select(event=None):
            second_curr_val = cmb1.get()

            if len(column_names) > 1:
                column_names.pop(1)

            column_names.append(second_curr_val)

            def ols_gen():
                print("OLS Generation:")
                ols_func_parameters = ['Ֆակուլտետ', 'Ուսանողի_անուն', 'Ուսանողի_սեռ', 'Ծննդավայր_(երկիր)',
                                       'Ծննդավայր_ (քաղաք/գյուղ)', 'Ընդունման_տարեթիվ', 'Առարկա',
                                       'Առաջին_միջանկյալ_ստուգում', 'Երկրորդ_միջանկյալ_ստուգում',
                                       'Ամփոփիչ_ քննություն']

                # DB file name for OLS algorithm
                folder_name = ['ols']
                txt_file_name = ['ols.txt']

                # Getting dynamically path for appropriate DB file and backup directory
                absolute_path = sys.path[0]
                file_path = sys.path[0] + '/' + db_ols

#                dir_name = absolute_path + '/' + folder_name[0]
#                abs_path = dir_name + '\\' + txt_file_name[0]
                ols_path = pathlib.Path(__file__).parent.absolute()
                ols_path = str(ols_path)
                dir_name = ols_path + '/' 'images' + '/' + folder_name[0]
                abs_path = ols_path + '/' + txt_file_name[0]

                lb_make = LabelEncoder()
                if not find_plathform():
                    file_path = file_path.replace("\\", "/")
                df = pd.read_csv(file_path)

                print(column_names[0])
                print(column_names[1])
                print(df)
                print(column_names)

                if (column_names[0] == 'Ուսանողի անուն'):
                    column_names[0] = 'Ուսանողի_անուն'
                if (column_names[1] == 'Ուսանողի անուն'):
                    column_names[1] = 'Ուսանողի_անուն'

                if (column_names[0] == 'Ուսանողի սեռ'):
                    column_names[0] = 'Ուսանողի_սեռ'
                if (column_names[1] == 'Ուսանողի սեռ'):
                    column_names[1] = 'Ուսանողի_սեռ'

                if (column_names[0] == 'Ծննդավայր (երկիր)'):
                    column_names[0] = 'Ծննդավայր_երկիր'
                if (column_names[1] == 'Ծննդավայր (երկիր)'):
                    column_names[1] = 'Ծննդավայր_երկիր'

                if (column_names[0] == 'Ծննդավայր (քաղաք/գյուղ)'):
                    column_names[0] = 'Ծննդավայր_քաղաք_գյուղ'
                if (column_names[1] == 'Ծննդավայր (քաղաք/գյուղ)'):
                    column_names[1] = 'Ծննդավայր_քաղաք_գյուղ'

                if (column_names[0] == 'Ընդունման տարեթիվ'):
                    column_names[0] = 'Ընդունման_տարեթիվ'
                if (column_names[1] == 'Ընդունման տարեթիվ'):
                    column_names[1] = 'Ընդունման_տարեթիվ'

                if (column_names[0] == 'Առաջին միջանկյալ ստուգում'):
                    column_names[0] = 'Առաջին_միջանկյալ_ստուգում'
                if (column_names[1] == 'Առաջին միջանկյալ ստուգում'):
                    column_names[1] = 'Առաջին_միջանկյալ_ստուգում'

                if (column_names[0] == 'Երկրորդ միջանկյալ ստուգում'):
                    column_names[0] = 'Երկրորդ_միջանկյալ_ստուգում'
                if (column_names[1] == 'Երկրորդ միջանկյալ ստուգում'):
                    column_names[1] = 'Երկրորդ_միջանկյալ_ստուգում'

                if (column_names[0] == 'Ամփոփիչ քննություն'):
                    column_names[0] = 'Ամփոփիչ_քննություն'
                if (column_names[1] == 'Ամփոփիչ քննություն'):
                    column_names[1] = 'Ամփոփիչ_քննություն'

                lb_make = LabelEncoder()
                # df[column_names[0]] = lb_make.fit_transform(df[column_names[0]])
                # df[column_names[1]] = lb_make.fit_transform(df[column_names[1]])
                df["Ֆակուլտետ"] = lb_make.fit_transform(df["Ֆակուլտետ"])
                df["Ուսանողի_անուն"] = lb_make.fit_transform(df["Ուսանողի_անուն"])
                df["Ծննդավայր_երկիր"] = lb_make.fit_transform(df["Ծննդավայր_երկիր"])
                df["Ծննդավայր_քաղաք_գյուղ"] = lb_make.fit_transform(df["Ծննդավայր_քաղաք_գյուղ"])
                df["Առարկա"] = lb_make.fit_transform(df["Առարկա"])

                def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png','txt')):

                    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
                    # filter out directories, no-extension, and wrong extension files
                    valid_files = [f for f in valid_files if '.' in f and \
                        f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

                    if not valid_files:
                        raise ValueError("No valid images in %s" % dirpath)

                    return max(valid_files, key=os.path.getmtime)  

                m = ols(column_names[0] + ' ~ ' + column_names[1], df).fit()

                X = df[column_names[0]].values.reshape(-1, 1)
                y = df[column_names[1]].values.reshape(-1, 1)

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
                regressor = LinearRegression()
                regressor.fit(X_train, y_train)  # training the algorithm
                y_pred = regressor.predict(X_test)

                prstd, iv_l, iv_u = wls_prediction_std(m)

                fig, ax = plt.subplots(figsize=(8,6))

                ax.plot(X, y, 'o', label="data")
                ax.plot(X, y, 'b-', label="True")
                ax.plot(X, m.fittedvalues, 'r--.', label="OLS")
                ax.plot(X, iv_u, 'r--')
                ax.plot(X, iv_l, 'r--')
                ax.legend(loc='best')
                plt.tight_layout()
                plt.savefig(
                    'images/ols/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                      "") + '.png')

                ols_1_path=get_latest_image("images/ols/",'png')          
                image_ols_1 = PhotoImage(file=ols_1_path)
                original_image_ols_1 = image_ols_1.subsample(2,3) # resize image using subsample

                ols_1_im_label = Label(ols_image_frame,image=original_image_ols_1)
                ols_1_im_label.image = original_image_ols_1 # keep a reference
                ols_1_im_label.place(x=387, y=118)     


                plt.figure(figsize=(8, 4))
                plt.scatter(X_test, y_test, color='#ccccff')
                plt.plot(X_test, y_pred, color='red', linewidth=2)
                mngr4 = plt.get_current_fig_manager()
                mngr4.window.setGeometry(1020, 505, 700, 530)
                plt.savefig(
                    'images/ols/' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f').replace(" ",
                                                                                                      "") + '.png')

                ols_2_path=get_latest_image("images/ols/",'png')          
                image_ols_2 = PhotoImage(file=ols_2_path)
                original_image_ols_2 = image_ols_2.subsample(4,2) # resize image using subsample

                ols_2_im_label = Label(ols_image_frame,image=original_image_ols_2)
                ols_2_im_label.image = original_image_ols_2 # keep a reference
                ols_2_im_label.place(x=397, y=348)       

                def mouse_on_ols_1(event):
                    image_ols_1 = PhotoImage(file=ols_1_path)
                    original_image_ols_1 = image_ols_1.subsample(2,2) # resize image using subsample

                    ols_1_im_label = Label(ols_image_frame,image=original_image_ols_1)
                    ols_1_im_label.image = original_image_ols_1 # keep a reference
                    ols_1_im_label.place(x=387, y=118)  

                    return          

                def mouse_on_ols_2(event):
                    ols_2_path=get_latest_image("images/ols/",'png')          
                    image_ols_2 = PhotoImage(file=ols_2_path)
                    original_image_ols_2 = image_ols_2.subsample(2,2) # resize image using subsample

                    ols_2_im_label = Label(ols_image_frame,image=original_image_ols_2)
                    ols_2_im_label.image = original_image_ols_2 # keep a reference
                    ols_2_im_label.place(x=397, y=348)  

                    return                                    

                ols_1_im_label.bind('<Enter>',mouse_on_ols_1)                    
                ols_2_im_label.bind('<Enter>',mouse_on_ols_2)  

                # Taking backup values from above graphs and puting appropriate directory
                try:
                    # Create target Directory
                    os.mkdir(dir_name)
                    print("Directory ", dir_name, " created.")
                except FileExistsError:
                    print("Directory ", dir_name, " already exists.")
                file = open(abs_path, 'w', encoding="utf8")
                file.write(str(m.summary()))
                file.close()

                now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                now = str(now)
                newname = 'ols_' + now + '.txt'
                os.rename('ols.txt', newname)

                shutil.move(newname, "images/ols/")

                ols_txt_path = get_latest_image("images/ols/",'txt')              

                def ols_btn_click():
                    window.filename =  filedialog.askopenfile(mode='r',initialdir = "images/ols/",title = ols_txt_path,filetypes = (("txt files","*.txt"),("all files","*.*")))

                ols_txt_entry=Entry(ols_txt_frame, highlightcolor='#ababba',justify=LEFT, relief=SUNKEN, width=18)
                ols_txt_entry.insert(END,ols_txt_path)
                ols_txt_entry.place(x=637, y=490)

                ols_txt_btn=Button(ols_txt_frame, text="Browse", bd=2, activebackground='#c7c7d1',relief=SUNKEN,command=ols_btn_click).place(x=786, y=486)                                                         

                def rst_ols():
                    print("Reset")
                    cmb.set('')
                    cmb1.set('')
                    new_text=" "
                    ols_1_im_label.image=''
                    ols_2_im_label.image=''
                    ols_txt_entry.delete(0, tk.END)      
                    ols_txt_entry.insert(0, new_text)
                                                                                                         
                plt_rst_ols=PhotoImage(file="reset.png")  
                sub_plt_rst_ols=plt_rst_ols.subsample(4,4)

                button_ols_rst = Button(ols_input_frame, text="Reset", fg='#026084', command=rst_ols, image=sub_plt_rst_ols, compound=LEFT, width=130)
                button_ols_rst.image=sub_plt_rst_ols
                button_ols_rst.place(x=88, y=270)
                button_arr.append(button_ols_rst)

                ttk.Separator(ols_input_frame).place(x=75, y=350, relwidth=0.29)

                def ols_go_to_menu():

                    ols_frame=Frame(window, width=950, height=650, bg='white').grid(row=0,column=0, padx=5, pady=5)
                    #jnt_frame.grid(row=0,column=0, padx=5, pady=5)

                    ols_clust=Label(ols_frame,  width=20, bg='white').place(x=10, y=10)

                    ols_inner_frame=Frame(ols_frame, width=80, height=150, bg='white').grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)
                    #jnt_inner_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=400, ipady=190)

                    ols_input_frame=Frame(ols_inner_frame, width=300, height=380, bg='white').place(x=65, y=85)

                    ols_image_frame=Frame(ols_frame, width=490, height=500, bg='white').place(x=385, y=85)

                    Label(ols_image_frame, bg='white').place(x=565, y=95)         

                    ols_txt_frame=Frame(ols_image_frame, width=250, height=195, bg='white').place(x=627,y=388)

                    lbl_ols_txt=Label(ols_txt_frame, bg='white').place(x=630, y=392)                           

                    print("OLS frame has been destroyed.")      

                plt_up=PhotoImage(file="up.png")  
                sub_plt_up=plt_up.subsample(4,4)     

                button_ols_go_to_menu=Button(ols_input_frame, text="Go to menu", fg='#026084', command=ols_go_to_menu, image=sub_plt_up, compound=LEFT, width=130)
                button_ols_go_to_menu.image=sub_plt_up
                button_ols_go_to_menu.place(x=88, y=360)
                button_arr.append(button_ols_go_to_menu) 

            # Creating a photoimage object to use image 
            plt_gen_ols = PhotoImage(file = "images.png") 
            sub_plt_ols_gen = plt_gen_ols.subsample(4, 4)    

            button_ols_gen = Button(ols_input_frame, text="Generate", fg='#026084', command=ols_gen, image=sub_plt_ols_gen, compound=LEFT)
            button_ols_gen.image=sub_plt_ols_gen
            button_ols_gen.place(x=88, y=200)
            button_arr.append(button_ols_gen)


            ttk.Separator(ols_input_frame).place(x=75, y=190, relwidth=0.29)            

        cmb1 = ttk.Combobox(ols_input_frame, values=data, state='readonly', width=28, height=5)
        cmb1.place(x=75, y=159)
        cmb1.bind('<<ComboboxSelected>>', on_second_select)
        button_arr.append(cmb1)

    if show_ols_analysis == True:
        file_path = sys.path[0] + '\\' + db
        if not find_plathform():
            file_path = file_path.replace("\\", "/")
        data = pd.read_csv(file_path)

        labelForMenu = tk.Label(ols_input_frame, text="Choose OLS input value", width=29,height=2,font=("Sans", 10),bd=3, relief=SUNKEN).place(x=75, y=95)

        data = pd.read_csv(file_path, nrows=1).columns.tolist()
        columns = data

        cmb = ttk.Combobox(ols_input_frame, values=data, state='readonly', width=28, height=5)
        cmb.place(x=75, y=136)
        cmb.bind('<<ComboboxSelected>>', ols_func)
        button_arr.append(cmb)

def showAssociationRules():
    global show_association_rules;
    show_association_rules = True;
    print('showAssociationRules');

def showClusterAnalysis():
    global show_cluster_analysis;
    show_cluster_analysis = True;
    print('showClusterAnalysis')

def showJointplotAnalysis():
    global show_jointplot_analysis;
    show_jointplot_analysis = True;
    print('showJointplotAnalysis');

def showCorrelationAnalysis():
    global show_correlation_analysis;
    show_correlation_analysis = True;
    print('showCorrelationAnalysis');

def showRegressionAnalysis():
    global show_regression_analysis;
    show_regression_analysis = True;
    print('showRegressionAnalysis');    

def showOlsAnalysis():
    global show_ols_analysis;
    show_ols_analysis = True;
    print('showOlsAnalysis');      



def dontShowAssociationRules():
    global show_association_rules;
    show_association_rules = False
    print('show_association_rules=False')

def dontShowClusterAnalysis():
    global show_cluster_analysis;
    show_cluster_analysis = False;
    print('show_cluster_analysis=False')

def dontShowJointplotAnalysis():
    global show_jointplot_analysis;
    show_jointplot_analysis = False;
    print('showJointplotAnalysis=False')

def dontShowCorrelationAnalysis():
    global show_correlation_analysis;
    show_correlation_analysis = False;
    print('showCorrelationAnalysis==False')

def dontShowRegressionAnalysis():
    global show_regression_analysis;
    show_regression_analysis = False;
    print('show_regression_analysis==False')    

def dontShowOlsAnalysis():
    global show_ols_analysis;
    show_ols_analysis = False;    
    print('show_ols_analysis==False');  


# Create a menu button
menu = Menu(window)
window.config(menu=menu)

menu.config(bg="#026084")
menu.config(fg="#ffffff")

reg_menu = Menu(menu, tearoff = 0)
reg_menu.add_command(label='   Show Results   ', command=lambda: openFolder('images/regression'))
reg_menu.add_separator()
reg_menu.add_command(label='   Choose Regression   ', command=lambda: (showRegressionAnalysis(), showFunctions(),dontShowRegressionAnalysis()))
reg_menu.config(bg="#026084")
reg_menu.config(fg="#ffffff")

ols_menu = Menu(menu, tearoff = 0)
ols_menu.add_command(label='   Show Results   ', command=lambda: openFolder('images/ols'))
ols_menu.add_separator()
ols_menu.add_command(label='   Choose OLS   ', command=lambda: (showOlsAnalysis(), showFunctions(),dontShowOlsAnalysis()))
ols_menu.config(bg="#026084")
ols_menu.config(fg="#ffffff")

reg_func_menu=Menu(menu, tearoff = 0)
reg_func_menu.add_cascade(label='   Regression   ', menu=reg_menu)
reg_func_menu.add_separator()
reg_func_menu.add_cascade(label='   OLS   ', menu=ols_menu)
reg_func_menu.config(bg="#026084")
reg_func_menu.config(fg="#ffffff")

correlation_menu = Menu(menu, tearoff = 0)
correlation_menu.add_command(label='   Show Results   ', command=lambda: openFolder('images/correlation'))
correlation_menu.add_separator()
correlation_menu.add_command(label='   Choose Correlation   ', command=lambda: (showCorrelationAnalysis(), showFunctions(),dontShowCorrelationAnalysis()))
correlation_menu.config(bg="#026084")
correlation_menu.config(fg="#ffffff")

jntplt_menu = Menu(menu, tearoff = 0)
jntplt_menu.add_command(label='   Show Results   ', command=lambda: openFolder('images/jointplot'))
jntplt_menu.add_separator()
jntplt_menu.add_command(label='   Choose jointplot   ', command=lambda: (showJointplotAnalysis(), showFunctions(),dontShowJointplotAnalysis()))
jntplt_menu.config(bg="#026084")
jntplt_menu.config(fg="#ffffff")

corr_func_menu=Menu(menu, tearoff = 0)
corr_func_menu.add_cascade(label='   Correlation   ', menu=correlation_menu)
corr_func_menu.add_separator()
corr_func_menu.add_cascade(label='   Jointplot   ', menu=jntplt_menu)
corr_func_menu.config(bg="#026084")
corr_func_menu.config(fg="#ffffff")

clustering_menu = Menu(menu, tearoff = 0)
clustering_menu.add_command(label='   Show Results   ', command=lambda: openFolder('images/clustering'))
clustering_menu.add_separator()
clustering_menu.add_command(label='   Choose Clustering   ', command=lambda: (showClusterAnalysis(), showFunctions(),dontShowClusterAnalysis()))
clustering_menu.config(bg="#026084")
clustering_menu.config(fg="#ffffff")

clus_func_menu=Menu(menu, tearoff = 0)
clus_func_menu.add_cascade(label='   Clustering   ', menu=clustering_menu)
clus_func_menu.config(bg="#026084")
clus_func_menu.config(fg="#ffffff")

apriori_menu = Menu(menu, tearoff = 0)
apriori_menu.add_command(label='   Show Results   ', command=lambda: openFolder('images/apriori'))
apriori_menu.add_separator()
apriori_menu.add_command(label='   Choose Apriori   ',  command=lambda: (showAssociationRules(), showFunctions(),dontShowAssociationRules()))
apriori_menu.config(bg="#026084")
apriori_menu.config(fg="#ffffff")

ass_func_menu=Menu(menu, tearoff = 0)
ass_func_menu.add_cascade(label='   Apriori   ', menu=apriori_menu)
ass_func_menu.config(bg="#026084")
ass_func_menu.config(fg="#ffffff")

association_rules_menu = Menu(menu, tearoff = 0)
association_rules_menu.add_cascade(label='    Function    ',menu=ass_func_menu)
association_rules_menu.config(bg="#026084")
association_rules_menu.config(fg="#ffffff")

claster_analysis_menu = Menu(menu, tearoff = 0)
claster_analysis_menu.add_cascade(label='    Function    ',menu=clus_func_menu)
claster_analysis_menu.config(bg="#026084")
claster_analysis_menu.config(fg="#ffffff")

correlation_analysis_menu = Menu(menu, tearoff = 0)
correlation_analysis_menu.add_cascade(label='    Functions    ',menu=corr_func_menu)
correlation_analysis_menu.config(bg="#026084")
correlation_analysis_menu.config(fg="#ffffff")

regression_analysis_menu = Menu(menu, tearoff = 0)
regression_analysis_menu.add_cascade(label='    Functions    ',menu=reg_func_menu)
regression_analysis_menu.config(bg="#026084")
regression_analysis_menu.config(fg="#ffffff")

watch_results_menu = Menu(menu, tearoff = 2)
watch_results_menu.add_cascade(label='  Assosiation Rules  ', menu=association_rules_menu)
watch_results_menu.add_separator()
watch_results_menu.add_cascade(label='  Culster Analysis   ', menu=claster_analysis_menu)
watch_results_menu.add_separator()
watch_results_menu.add_cascade(label='  Correlation Analysis   ', menu=correlation_analysis_menu)
watch_results_menu.add_separator()
watch_results_menu.add_cascade(label='  Regression Analysis   ', menu=regression_analysis_menu)
watch_results_menu.add_separator()
watch_results_menu.add_separator()
watch_results_menu.add_command(label='  Help  ', command=lambda: openFolder('images/help'))
watch_results_menu.config(bg="#026084")
watch_results_menu.config(fg="#ffffff")

menu.add_cascade(label='  Menu  ', menu=watch_results_menu)

CreateToolTip(ass_func_menu, text='Apriori')
CreateToolTip(clus_func_menu, text='Clustering')
CreateToolTip(corr_func_menu, text='Correlation   Jointplot')
CreateToolTip(reg_func_menu, text='Regression   OLS')
CreateToolTip(watch_results_menu, text='AprioriնճսֆճհկֆալՈՀՖԸՔՃԱՀՍՃՀՃՏՍՊՔՀՖՍ\n'
                               'Custering կհկհաճհսճկհատհճաքճպպճատպճ'
                               'Correlation ճհԿՏհաքկտաճկճտկճտըիկֆճհկհֆքճհըքճսպքճկհճպֆհկսեճկ.\n'
                               'Regression.ճպաճհքճհֆճհք')

window.mainloop()