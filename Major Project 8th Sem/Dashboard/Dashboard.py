import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import pandas as pd
import numpy as np
from pandas import DataFrame

pd.set_option("precision",3)

LARGE_FONT= ("Verdana", 12)
style.use("bmh")

df1 = DataFrame()
df2 = DataFrame()
filename = 'Book1.csv'
graph = 0

def open_file(name):
    global df1, df2
    df1 = pd.read_csv(filename, comment=',')
    df1 = df1.dropna(how='all')
    df1 = df1.fillna(0)
    df2 = DataFrame(df1['Particulars'])

indexes = [0,3,7,11]

def cal_diff(selection, **kwargs):
    global df1, df2, graph
    graph = selection
    if selection == 1:
        for year_idx in range(1,len(df1.columns[1:])):
            year2 = df1.columns[year_idx]
            year1 = df1.columns[year_idx+1]
            period = 'Period ' + year1[2:] + '-' + year2[2:]
            df2[period] = (df1[year2] - df1[year1])*100
            df2[period] = (df2[period]/df1[year1]).replace({ 0 : np.nan, np.inf : np.nan })

    elif selection == 2:
        year1 = kwargs['yr1']
        year2 = kwargs['yr2']
        period = 'Period ' + year1[2:] + '-' + year2[2:]
        df2[period] = (df1[year2] - df1[year1])*100
        df2[period] = (df2[period]/df1[year1]).replace({ 0 : np.nan, np.inf : np.nan })

    else:
        pass
    df2 = df2.fillna(0)

def plotgraph(window):
    global df2, indexes, f, a, b

    f = Figure()

    plot_df = df2.ix[indexes]
    plot_df = plot_df.set_index('Particulars')

    if graph == 1:
        a = f.add_subplot(211)
        b = f.add_subplot(212)

        a.clear()
        b.clear()

        plot_df1 = plot_df.T
        plot_df1.plot(ax=a, title='% Change of Particulars in Income Statement as Trends')
        plot_df1.plot(ax=b, kind='barh', title='% Change of Particulars in Income Statement as Bars')
        f.subplots_adjust(left=0.2,bottom=0.2,hspace=0.5)
    elif graph == 2:
        a = f.add_subplot(111)
        a.clear()
        plot_df.plot(ax=a, kind='barh', title='% Change of Particulars in Income Statement as Bars')
        f.subplots_adjust(left=0.2,bottom=0.2,hspace=0.5)
    canvas = FigureCanvasTkAgg(f, window)
    canvas.show()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2TkAgg(canvas, window)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

class MyApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.iconbitmap(self, 'myicon.ico')
        tk.Tk.wm_title(self, "My Dashboard")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, PageOne, GraphPage):
                   
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Visit Page 1",
                            command= lambda: controller.show_frame(PageOne))
        button1.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        self.header = tk.Frame(self)
        self.header.pack(side=tk.TOP)
        label1 = tk.Label(self.header, text="Page One", font=LARGE_FONT)
        label1.pack(pady=10, padx=10)

        open_file(filename)

        self.rb_var = tk.IntVar(self)
        self.rb_var.set(1)

        rb1 = tk.Radiobutton(self.header, text="Percentage Change Year-over-Year", variable=self.rb_var, value=1,
                            command=self.hide_years, indicatoron = 0)
        rb1.pack(side=tk.TOP)

        rb2 = tk.Radiobutton(self.header, text="Percentage Change over any two years", variable=self.rb_var, value=2,
                            command=self.choose_years, indicatoron = 0)
        rb2.pack(side = tk.TOP, pady=10)

        self.year1_var = tk.StringVar(self)
        self.year1_var.set("2013") # default value

        self.year2_var = tk.StringVar(self)
        self.year2_var.set("2014") # default value

        options = df1.columns[1:].tolist()
        self.label2 = tk.Label(self.header, text="Choose year 1: ")
        self.year1_menu = ttk.OptionMenu(self.header, self.year1_var, *options)
        self.label3 = tk.Label(self.header, text="Choose year 2: ")
        self.year2_menu = ttk.OptionMenu(self.header, self.year2_var, *options)

        button1 = ttk.Button(self.header, text="Plot",
                             command= lambda: controller.show_frame(GraphPage))
        button1.pack(side=tk.TOP, pady=10)

        self.label4 = tk.Label(self.header, text="Hi")
        self.label4.pack(side=tk.TOP)

        """i = 0
        Lb1 = tk.Listbox(self)
        for column in df2['Particulars']:
            Lb1.insert(i, str(column))
            i =  i + 1
        Lb1.pack()"""

        footer = tk.Frame(self)
        footer.pack(side=tk.TOP)

        button3 = ttk.Button(self, text="Back to Home",
                            command= lambda: controller.show_frame(StartPage))
        button3.pack(side=tk.BOTTOM)

    def hide_years(self):
        self.label2.pack_forget()
        self.year1_menu.pack_forget()
        self.label3.pack_forget()
        self.year2_menu.pack_forget()
        cal_diff(self.rb_var.get())
        self.label4.config(text=self.year1_var.get() + ' ' + self.year2_var.get())

    def choose_years(self):
        self.label2.pack(in_=self.header)
        self.year1_menu.pack(in_=self.header)
        self.label3.pack(in_=self.header)
        self.year2_menu.pack(in_=self.header)
        self.wait_variable(self.year1_var)
        self.wait_variable(self.year2_var)
        cal_diff(self.rb_var.get(),yr1=self.year1_var.get(),yr2=self.year2_var.get())
        self.label4.config(text=self.year1_var.get() + ' ' + self.year2_var.get())

class GraphPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.header = tk.Frame(self)
        self.header.pack(side=tk.TOP)
        label1 = tk.Label(self.header, text="Graph Page", font=LARGE_FONT)
        label1.pack(pady=10, padx=10)

        button1 = ttk.Button(self.header, text="Plot",
                             command= lambda: plotgraph(self))
        button1.pack(side=tk.TOP, pady=10)

        button3 = ttk.Button(self, text="Back to Home",
                            command= lambda: controller.show_frame(StartPage))
        button3.pack(side=tk.BOTTOM)

app = MyApp()
app.mainloop()