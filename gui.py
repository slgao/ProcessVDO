import os
import sys
import glob
import re
import shutil

if sys.version_info.major < 3:
    import tkFileDialog as fd
    import Tkconstants as tkcst  # change needed when python 3 used
    import ttk
    import Tkinter as tk
else:
    import tkinter.filedialog as fd
    import tkinter.constants as tkcst
    from tkinter import ttk
    import tkinter as tk

#from wand.image import Image
import pandas as pd
import numpy as np
#import Queue, threading, time
# import local modules
import vdo
import vdo.VideoRead.VideoRead as VR


class Options(object):
    attributes = ['debug', 'use_cams',
                  'AbExtCounter', 'save', 'Jumping', 'FrameInfo'
                  ]

    def __init__(self, **kwargs):
        for attr in self.__class__.attributes:
            setattr(self, attr, kwargs.get(attr))


def csv2h5(dir):
    fn_csv = r"{}/*.csv".format(dir)
    fn_csv = glob.glob(fn_csv)
    for fn in fn_csv:
        recp = pd.read_csv(fn,
                           names=['Odometer', 'FrameNum'],
                           skiprows=2, delimiter=',')
        if recp.empty:
            continue
        fn_hdf = fn[:-3] + 'h5'
        h5_var = 'vdo'
        shuffle = True
        fletcher32 = True
        complib_table = 'zlib'
        complib_h5py = 'gzip'
        complevel = 9
        import h5py
        reca = recp.to_records(index=False)
        with h5py.File(fn_hdf, 'w') as hfile:
            hfile.require_dataset(h5_var,
                                  shape=reca.shape,
                                  dtype=reca.dtype,
                                  data=reca,
                                  shuffle=shuffle,
                                  fletcher32=fletcher32,
                                  compression=complib_h5py,
                                  compression_opts=complevel,
                                  )
        os.remove(fn)


class TkFileDialog(tk.Frame):

    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.factor = 8.0
        #self.pano_ante_dist = [3793.5, 30000]
        self.pano_ante_dist = [3793.5, 30000]
        self.pano_cam_ids = []  # get exported cam ids in the vdo image export function
        self.vdo_folders = []
        self.r_d, self.r_d_base = [], []
        self.icon = "euraillogo.ico"
        self.indir, self.LB_dir, self.outdir, self.vdo_dir, self.pano_save_dir, \
            self.seg_dir, self.poi_dir = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), \
            tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.GPS_var_cb5, self.img_export, self.multi_folder = tk.BooleanVar(
        ), tk.BooleanVar(), tk.BooleanVar()
        self.img_export.set(True)
        self.GPS_var_cb5.set(True)
        self.multi_folder.set(True)
        self.deact_rear = False
        self.indir.set("")
        self.LB_dir.set("")
        self.vdo_dir.set("")
        self.seg_dir.set("")
        self.poi_dir.set("")
        current_folder_path, current_folder_name = os.path.split(os.getcwd())
        self.outdir.set(r"{}\{}".format(
            current_folder_path, current_folder_name))
        self.pano_save_dir.set(r"{}\{}".format(
            current_folder_path, current_folder_name))
        root.iconbitmap(self.icon)
        root.geometry("%dx%d%+d%+d" % (300, 220, 350, 225))
        self.center(root)
        root.wm_title("PROCESSVDO_1.0.0.2")
        self.button_panel = ttk.Frame(self, padding=(3, 3, 12, 12))

        self.button_panel.grid(row=0)

        # options for buttons
        button_opt = {'fill': tkcst.BOTH, 'padx': 5, 'pady': 5}

        # define buttons
        #tk.Button(self, text='askopenfile', command=self.askopenfile).pack(**button_opt)
        self.title_write_hd5 = "OUTPUT HDF5"
        self.title_resolution_analyse = "RESOLUTION ANALYSE"
        self.title_pano_img_export = "EXPORT PANO IMG"
        self.title_pano_GPS_export = "EXPORT PANO GPS"
        b1 = ttk.Button(self.button_panel, text=self.title_resolution_analyse,
                        command=lambda: self.creat_res_analyse_win(self.title_resolution_analyse, root), width=30)
        b2 = ttk.Button(self.button_panel, text=self.title_write_hd5,
                        command=lambda: self.creat_cam_chose_win(self.title_write_hd5), width=30)
        b3 = ttk.Button(self.button_panel, text=self.title_pano_img_export,
                        command=lambda: self.creat_export_pano_img_win(self.title_pano_img_export, root), width=30)
        b4 = ttk.Button(self.button_panel, text=self.title_pano_GPS_export,
                        command=lambda: self.creat_pano_GPS_win(self.title_pano_GPS_export, root), width=30)
        b5 = ttk.Button(self.button_panel, text='EXIT',
                        command=lambda: self.main_exit(root), width=30)
        b1.grid(row=0, columnspan=5, sticky=tk.W + tk.E, padx=15, pady=5)
        b2.grid(row=1, column=0, columnspan=5,
                sticky=tk.W + tk.E, padx=15, pady=5)
        b3.grid(row=2, column=0, columnspan=5,
                sticky=tk.W + tk.E, padx=15, pady=5)
        b4.grid(row=3, column=0, columnspan=5,
                sticky=tk.W + tk.E, padx=15, pady=5)
        b5.grid(row=4, column=0, columnspan=5,
                sticky=tk.W + tk.E, padx=15, pady=5)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        self.button_panel.rowconfigure(0, weight=1)
        self.button_panel.rowconfigure(1, weight=1)
        self.button_panel.rowconfigure(2, weight=1)
        self.button_panel.columnconfigure(0, weight=1)
        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'

        # This is only available on the Macintosh, and only when Navigation Services are installed.
        #options['message'] = 'message'

        # if you use the multiple file version of the module functions this option is set automatically.
        #options['multiple'] = 1

        # defining options for opening a directory
        self.in_dir_opt = options = {}
        options['initialdir'] = self.indir.get()
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'

        self.out_dir_opt = options = {}
        options['initialdir'] = self.outdir.get()
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'

        self.LB_dir_opt = options = {}
        options['initialdir'] = self.LB_dir.get()
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'

        self.pano_vdo_dir_opt = options = {}
        options['initialdir'] = self.vdo_dir.get()
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'

        self.pano_save_dir_opt = options = {}
        options['initialdir'] = self.pano_save_dir.get()
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'

        self.seg_dir_opt = options = {}
        options['initialdir'] = self.seg_dir.get()
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'

        self.poi_dir_opt = options = {}
        options['initialdir'] = self.seg_dir.get()
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'

    def askopenfile(self):
        """Returns an opened file in read mode."""

        return fd.askopenfile(mode='r', **self.file_opt)

    def askopenfilename(self):
        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        filename = fd.askopenfilename(**self.file_opt)

        # open file on your own
        if filename:
            return open(filename, 'r')

    def ask_in_directory(self):
        """Returns a selected directoryname."""
        self.in_dir_opt['initialdir'] = self.indir.get()
        self.grab_set()
        self.indir.set(fd.askdirectory(**self.in_dir_opt))
        self.grab_release()
        return self.indir

    def ask_out_directory(self):
        """Returns a selected directoryname."""
        self.out_dir_opt['initialdir'] = self.outdir.get()
        self.grab_set()
        self.outdir.set(fd.askdirectory(**self.out_dir_opt))
        self.grab_release()
        return self.outdir

    def ask_LB_directory(self):
        """Returns a selected directoryname."""
        self.LB_dir_opt['initialdir'] = self.LB_dir.get()
        self.grab_set()
        self.LB_dir.set(fd.askdirectory(**self.LB_dir_opt))
        self.grab_release()
        return self.LB_dir

    def ask_pano_vdo_directory(self):
        """Returns a selected directoryname."""
        self.pano_vdo_dir_opt['initialdir'] = self.vdo_dir.get()
        self.grab_set()
        self.vdo_dir.set(fd.askdirectory(**self.pano_vdo_dir_opt))
        self.grab_release()
        return self.vdo_dir

    def ask_pano_save_directory(self):
        """Returns a selected directoryname."""
        self.pano_save_dir_opt['initialdir'] = self.pano_save_dir.get()
        self.grab_set()
        self.pano_save_dir.set(fd.askdirectory(**self.pano_save_dir_opt))
        self.grab_release()
        return self.pano_save_dir

    def ask_seg_directory(self):
        """Returns a selected directoryname."""
        self.seg_dir_opt['initialdir'] = self.seg_dir.get()
        self.grab_set()
        self.seg_dir.set(fd.askdirectory(**self.seg_dir_opt))
        self.grab_release()
        return self.seg_dir

    def ask_poi_directory(self):
        """Returns a selected directoryname."""
        self.poi_dir_opt['initialdir'] = self.poi_dir.get()
        self.grab_set()
        self.poi_dir.set(fd.askdirectory(**self.poi_dir_opt))
        self.grab_release()
        return self.poi_dir

    def center(self, root):

        root.update_idletasks()
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        root.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def creat_res_analyse_win(self, title_name, root):

        self.top_res_analyse = tk.Toplevel(root)
        self.top_res_analyse.grab_set()
        self.top_res_analyse.geometry("%dx%d%+d%+d" % (350, 80, 450, 125))
        self.center(self.top_res_analyse)
        self.top_res_analyse.wm_title(title_name)
        self.top_res_analyse.iconbitmap(self.icon)
        self.title_b_vdo = "From VDO..."
        self.title_b_h5 = "From HDF5..."
        b_vdo = ttk.Button(self.top_res_analyse, text=self.title_b_vdo,
                           command=lambda: self.creat_res_analyse_vdo_win(self.title_b_vdo, self.top_res_analyse), width=20)
        b_h5 = ttk.Button(self.top_res_analyse, text=self.title_b_h5,
                          comman=lambda: self.creat_res_analyse_h5_win(self.title_b_h5, self.top_res_analyse), width=20)
        b_vdo.grid(row=0, columnspan=5, sticky=tk.W + tk.E, padx=15, pady=5)
        b_h5.grid(row=1, column=0, columnspan=5,
                  sticky=tk.W + tk.E, padx=15, pady=5)
        self.top_res_analyse.rowconfigure(0, weight=0)
        self.top_res_analyse.columnconfigure(0, weight=1)

    def creat_res_analyse_h5_win(self, title_name, root):

        self.top_res_analyse_h5 = tk.Toplevel(root)
        self.top_res_analyse_h5.grab_set()
        self.top_res_analyse_h5.geometry("%dx%d%+d%+d" % (700, 150, 450, 125))
        # self.center(self.top_res_analyse_h5)
        self.top_res_analyse_h5.wm_title(title_name)
        self.top_res_analyse_h5.iconbitmap(self.icon)
        LB_path_label = ttk.Label(
            self.top_res_analyse_h5, text="LockBox Path:")
        h5_path_label = ttk.Label(self.top_res_analyse_h5, text="HDF5 Path:")
        row0 = 0
        LB_path_label.grid(
            row=1 + row0, sticky=(tk.S, tk.N, tk.E, tk.W), padx=5)
        h5_path_label.grid(row=row0, sticky=(tk.S, tk.N, tk.E, tk.W), padx=5)

        LB_button_browse = ttk.Button(
            self.top_res_analyse_h5, text="Browse ...", command=self.ask_LB_directory, width=10)
        h5_button_browse = ttk.Button(
            self.top_res_analyse_h5, text="Browse ...", command=self.ask_out_directory, width=10)

        LB_entry_path = ttk.Entry(
            self.top_res_analyse_h5, textvariable=self.LB_dir)
        h5_entry_path = ttk.Entry(
            self.top_res_analyse_h5, textvariable=self.outdir)
        LB_entry_path.grid(row=1 + row0, column=1, columnspan=4,
                           sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        h5_entry_path.grid(row=row0, column=1, columnspan=4,
                           sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        LB_button_browse.grid(row=1 + row0, column=5,
                              sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        h5_button_browse.grid(row=row0, column=5, sticky=(
            tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)

        self.top_res_analyse_h5.columnconfigure(1, weight=1)
        self.top_res_analyse_h5.rowconfigure(0, weight=0)

        b_ok = ttk.Button(self.top_res_analyse_h5, text="Output Graph",
                          width=13, command=self.show_progress_h52graph)
        button_cancel = ttk.Button(self.top_res_analyse_h5, text="Cancel", width=13,
                                   command=lambda: self.toplevel_exit(self.top_res_analyse_h5, self.top_res_analyse))
        b_ok.grid(row=2 + row0, column=4)
        button_cancel.grid(row=2 + row0, column=5)
        self.pb_h5 = ttk.Progressbar(
            self.top_res_analyse_h5, orient='horizontal', mode='determinate')
        self.pb_h5.grid(row=2 + row0, column=0, columnspan=4,
                        sticky=(tk.W, tk.E, tk.S, tk.N), padx=5, pady=5)
        self.status_frame = tk.Frame(
            self.top_res_analyse_h5, borderwidth=5, width=80, height=100)
        self.status_frame.grid(row=3 + row0, column=0,
                               columnspan=4, sticky=(tk.S, tk.N, tk.W))
        self.status_h5 = ttk.Label(self.status_frame, text="Waiting ...")
        #self.status_h5.grid(row=3 + row0, column=0, sticky=(tk.S, tk.N, tk.W), padx=5)
        self.status_h5.grid(row=0 + row0, column=0,
                            sticky=(tk.S, tk.N, tk.W), padx=5, pady=5)

    def creat_res_analyse_vdo_win(self, title_name, root):

        self.top_cam_chose_res_analyse = tk.Toplevel(root)
        self.top_cam_chose_res_analyse.grab_set()
        self.top_cam_chose_res_analyse.geometry(
            "%dx%d%+d%+d" % (800, 550, 450, 125))
        self.top_cam_chose_res_analyse.wm_title(title_name)
        self.top_cam_chose_res_analyse.iconbitmap(self.icon)
        LB_path_label = ttk.Label(
            self.top_cam_chose_res_analyse, text="LockBox Path:")
        LB_path_label.grid(row=0, sticky=(tk.S, tk.N, tk.E, tk.W), padx=5)
        LB_entry_path = ttk.Entry(
            self.top_cam_chose_res_analyse, textvariable=self.LB_dir)
        LB_entry_path.grid(row=0, column=1, columnspan=4, sticky=(
            tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        LB_button_browse = ttk.Button(
            self.top_cam_chose_res_analyse, text="Browse ...", command=self.ask_LB_directory, width=10)
        LB_button_browse.grid(row=0, column=5, sticky=(
            tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        row0 = 1
        self.cam_chose_widget(self.top_cam_chose_res_analyse, self.top_res_analyse, row0=row0, button_ok_name="Output Graph",
                              command=self.show_progress_vdo2graph)
        self.top_cam_chose_res_analyse.columnconfigure(1, weight=1)
        self.top_cam_chose_res_analyse.rowconfigure(0, weight=0)

    def creat_cam_chose_win(self, title_name):

        self.top1 = tk.Toplevel(self)  # popup new window
        self.top1.grab_set()  # disable the background window
        self.top1.geometry("%dx%d%+d%+d" % (800, 450, 450, 125))
        self.top1.wm_title(title_name)
        self.top1.iconbitmap(self.icon)
        self.cam_chose_widget(self.top1, self.button_panel,
                              command=self.show_progress_generate_h5)

        #content.columnconfigure(2, weight=1)
        #content.columnconfigure(3, weight=1)
        #content.columnconfigure(4, weight=1)

        #l = tk.Label(t, text="lable1")
        # l.pack(side="top",fill="both",expand=True,padx=100,pady=100)

    def cam_chose_widget(self, toplevel, downlevel, row0=0, button_ok_name="Output HDF5", command=None):

        #toplevel = ttk.Frame(toplevel,padding=(3,3,3,3))
        #toplevel.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame_cam_5 = tk.Frame(toplevel, relief="sunken",
                               borderwidth=5, width=80, height=100)
        frame_cam_6 = tk.Frame(toplevel, relief="sunken",
                               borderwidth=5, width=80, height=100)
        frame_cam_7 = tk.Frame(toplevel, relief="sunken",
                               borderwidth=5, width=80, height=100)
        frame_cam_5.grid(row=2 + row0, column=0, rowspan=2,
                         columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame_cam_6.grid(row=4 + row0, column=0, rowspan=2,
                         columnspan=4, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame_cam_7.grid(row=6 + row0, column=0, rowspan=2,
                         columnspan=4, sticky=(tk.N, tk.S, tk.E, tk.W))

        label_in_path = ttk.Label(toplevel, text="VDO Path:")
        label_out_path = ttk.Label(toplevel, text="Save Path:")
        label_in_path.grid(row=row0, sticky=(tk.S, tk.N, tk.E, tk.W), padx=5)
        label_out_path.grid(
            row=1 + row0, sticky=(tk.S, tk.N, tk.E, tk.W), padx=5)
        #self.status = ttk.Label(toplevel, text = "Waiting ...")
        #self.status.grid(row=9 + row0, column=0, sticky=(tk.S, tk.N, tk.W), padx=5)
        self.status_f = tk.Frame(toplevel, borderwidth=5, width=80, height=100)
        self.status_f.grid(row=9 + row0, column=0,
                           columnspan=4, sticky=(tk.S, tk.N, tk.W))
        self.status_lb = ttk.Label(self.status_f, text="Waiting ...")
        self.status_lb.grid(row=0 + row0, column=0,
                            sticky=(tk.S, tk.N, tk.W), padx=5, pady=5)

        in_button_browse = ttk.Button(
            toplevel, text="Browse ...", command=self.ask_in_directory, width=10)
        out_button_browse = ttk.Button(
            toplevel, text="Browse ...", command=self.ask_out_directory, width=10)

        in_entry_path = ttk.Entry(toplevel, textvariable=self.indir)
        out_entry_path = ttk.Entry(toplevel, textvariable=self.outdir)
        in_entry_path.grid(row=row0, column=1, columnspan=4,
                           sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        out_entry_path.grid(row=1 + row0, column=1, columnspan=4,
                            sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        in_button_browse.grid(row=row0, column=5, sticky=(
            tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        out_button_browse.grid(row=1 + row0, column=5,
                               sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)

        self.cam_5 = ["c50", "c51"]
        self.cam_6 = ["60", "61", "64", "65"]
        self.cam_7 = ["70", "71", "74", "75"]
        cb6, cb7, cb5 = {}, {}, {}
        self.var_6, self.var_7, self.var_5 = {}, {}, {}  # checkbutton Boolean variable
        #self.vars_6, self.vars_7, self.vars_5 = [], [], []
        self.m_var_cb5, self.m_var_cb6, self.m_var_cb7 = tk.BooleanVar(
        ), tk.BooleanVar(), tk.BooleanVar()
        self.m_var_cb5.set(True)
        self.m_var_cb6.set(True)
        self.m_var_cb7.set(True)
        main_cb5 = ttk.Checkbutton(frame_cam_5, text="pano_cam", variable=self.m_var_cb5,
                                   command=lambda: self.main_cb5_control(self.m_var_cb5, self.var_5))
        main_cb6 = ttk.Checkbutton(
            frame_cam_6, text="linear_cam_6", variable=self.m_var_cb6, command=self.main_cb6_control)
        main_cb7 = ttk.Checkbutton(
            frame_cam_7, text="linear_cam_7", variable=self.m_var_cb7, command=self.main_cb7_control)
        main_cb5.grid(row=0, sticky=(tk.E), pady=5, padx=5)
        main_cb6.grid(row=0, sticky=(tk.E), pady=5, padx=5)
        main_cb7.grid(row=0, sticky=(tk.E), pady=5, padx=5)

        for i, c_id in enumerate(self.cam_5):
            self.var_5[i] = tk.BooleanVar()
            self.var_5[i].set(1)
            cb5[i] = ttk.Checkbutton(frame_cam_5, variable=self.var_5[
                                     i], onvalue=1, offvalue=0, text="cam_{}".format(c_id))
            # self.vars_5.append(self.var_5[i].get())
            cb5[i].grid(row=1, column=i, sticky=(tk.E), pady=5, padx=5)
        for i, c_id in enumerate(self.cam_6):
            self.var_6[i] = tk.BooleanVar()
            self.var_6[i].set(1)
            cb6[i] = ttk.Checkbutton(frame_cam_6, variable=self.var_6[
                                     i], onvalue=1, offvalue=0, text="cam_{}".format(c_id))
            # self.vars_6.append(self.var_6[i].get())
            cb6[i].grid(row=1, column=i, sticky=(tk.E), pady=5, padx=5)
        for i, c_id in enumerate(self.cam_7):
            self.var_7[i] = tk.BooleanVar()
            self.var_7[i].set(1)
            cb7[i] = ttk.Checkbutton(frame_cam_7, variable=self.var_7[
                                     i], onvalue=1, offvalue=0, text="cam_{}".format(c_id))
            # self.vars_7.append(self.var_7[i].get())
            cb7[i].grid(row=1, column=i, sticky=(tk.E), pady=5, padx=5)

        button_ok = ttk.Button(
            toplevel, text=button_ok_name, width=13, command=command)
        button_cancel = ttk.Button(toplevel, text="Cancel", width=13,
                                   command=lambda: self.toplevel_exit(toplevel, downlevel))
        button_ok.grid(row=8 + row0, column=4)
        button_cancel.grid(row=8 + row0, column=5)
        self.pb = ttk.Progressbar(
            toplevel, orient='horizontal', mode='determinate')
        self.pb.grid(row=8 + row0, column=0, columnspan=4,
                     sticky=(tk.W, tk.E, tk.S, tk.N), padx=5, pady=5)

        toplevel.columnconfigure(0, weight=1)
        toplevel.rowconfigure(0, weight=1)
        #self.top1.rowconfigure(0, weight=1)
        toplevel.columnconfigure(0, weight=0)
        toplevel.columnconfigure(1, weight=1)
        toplevel.columnconfigure(2, weight=1)
        toplevel.rowconfigure(0, weight=0)
        toplevel.rowconfigure(1, weight=0)
        toplevel.rowconfigure(2 + row0, weight=1)
        toplevel.rowconfigure(4 + row0, weight=1)
        toplevel.rowconfigure(6 + row0, weight=1)

    def creat_export_pano_img_win(self, title_name, root):

        self.top_export_pano_img = tk.Toplevel(root)
        self.top_export_pano_img.grab_set()
        self.top_export_pano_img.geometry("%dx%d%+d%+d" % (830, 240, 450, 125))
        # self.center(self.top_export_pano_img)
        self.top_export_pano_img.wm_title(title_name)
        self.top_export_pano_img.iconbitmap(self.icon)
        vdo_path_label = ttk.Label(self.top_export_pano_img, text="VDO Path:")
        pano_img_save_path_label = ttk.Label(
            self.top_export_pano_img, text="Img Save Path:")
        row0 = 0
        vdo_path_label.grid(
            row=0 + row0, sticky=(tk.S, tk.N, tk.E, tk.W), padx=5)
        pano_img_save_path_label.grid(
            row=1 + row0, sticky=(tk.S, tk.N, tk.E, tk.W), padx=5)
        vdo_button_browse = ttk.Button(
            self.top_export_pano_img, text="Browse ...", command=self.ask_pano_vdo_directory, width=10)
        save_button_browse = ttk.Button(
            self.top_export_pano_img, text="Browse ...", command=self.ask_pano_save_directory, width=10)
        vdo_entry_path = ttk.Entry(
            self.top_export_pano_img, textvariable=self.vdo_dir)
        save_entry_path = ttk.Entry(
            self.top_export_pano_img, textvariable=self.pano_save_dir)
        vdo_entry_path.grid(row=row0, column=1, columnspan=4, sticky=(
            tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        save_entry_path.grid(row=1 + row0, column=1, columnspan=4,
                             sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        vdo_button_browse.grid(row=row0, column=5, sticky=(
            tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        save_button_browse.grid(row=1 + row0, column=5,
                                sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)

        frame_cam_5 = tk.Frame(
            self.top_export_pano_img, relief="sunken", borderwidth=5, width=80, height=100)
        frame_cam_5.grid(row=2 + row0, column=0, rowspan=2,
                         columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        # deactivate rear camera "c51"
        if self.deact_rear:
            self.cam_5 = ["c50"]
        else:
            self.cam_5 = ["c50", "c51"]
        cb5 = {}
        self.GPS_var_5 = {}  # checkbutton Boolean variable
        #self.vars_6, self.vars_7, self.vars_5 = [], [], []
        self.GPS_var_cb5 = tk.BooleanVar()
        self.GPS_var_cb5.set(True)
        main_cb5 = ttk.Checkbutton(frame_cam_5, text="pano_cam", variable=self.GPS_var_cb5,
                                   command=lambda: self.main_cb5_control(self.GPS_var_cb5, self.GPS_var_5))
        img_export = ttk.Checkbutton(
            frame_cam_5, text="img_export", variable=self.img_export)
        run_day = ttk.Checkbutton(
            frame_cam_5, text="multi_folder(run_day)", variable=self.multi_folder)
        main_cb5.grid(row=0, sticky=(tk.E), pady=5, padx=5)
        img_export.grid(row=0, column=1, sticky=(tk.E), pady=5, padx=5)
        run_day.grid(row=0, column=2, sticky=(tk.E), pady=5, padx=5)
        for i, c_id in enumerate(self.cam_5):
            self.GPS_var_5[i] = tk.BooleanVar()
            self.GPS_var_5[i].set(1)
            cb5[i] = ttk.Checkbutton(frame_cam_5, variable=self.GPS_var_5[
                                     i], onvalue=1, offvalue=0, text="cam_{}".format(c_id))
            # self.vars_5.append(self.var_5[i].get())
            cb5[i].grid(row=1, column=i, sticky=(tk.E), pady=5, padx=5)

        self.top_export_pano_img.columnconfigure(1, weight=1)
        self.top_export_pano_img.rowconfigure(2, weight=1)

        b_out = ttk.Button(self.top_export_pano_img, text="Output Pano Img",
                           command=lambda: self.show_progress_export_pano_img(self.pb_pano, self.status_pano), width=17)
        b_dpc = ttk.Button(self.top_export_pano_img, text="DPC Img CSV",
                           command=self.show_progress_export_pano_img_dpc, width=17)
        button_cancel = ttk.Button(self.top_export_pano_img, text="Cancel",
                                   width=15, command=lambda: self.main_exit(self.top_export_pano_img))
        b_out.grid(row=4 + row0, column=4)
        b_dpc.grid(row=4 + row0, column=3)
        button_cancel.grid(row=4 + row0, column=5)
        self.pb_pano = ttk.Progressbar(
            self.top_export_pano_img, orient='horizontal', mode='determinate')
        self.pb_pano.grid(row=4 + row0, column=0, columnspan=2,
                          sticky=(tk.W, tk.E, tk.S, tk.N), padx=5, pady=5)
        self.status_frame_pano = tk.Frame(
            self.top_export_pano_img, borderwidth=5, width=80, height=100)
        self.status_frame_pano.grid(
            row=5 + row0, column=0, columnspan=4, sticky=(tk.S, tk.N, tk.W))
        self.status_pano = ttk.Label(
            self.status_frame_pano, text="Waiting ...")
        self.status_pano.grid(row=0 + row0, column=0,
                              sticky=(tk.S, tk.N, tk.W), padx=5, pady=5)

    def creat_pano_GPS_win(self, title_name, root):

        self.top_pano_GPS_export = tk.Toplevel(root)
        self.top_pano_GPS_export.grab_set()
        self.top_pano_GPS_export.geometry("%dx%d%+d%+d" % (800, 320, 450, 125))
        # self.center(self.top_pano_GPS_export)
        self.top_pano_GPS_export.wm_title(title_name)
        self.top_pano_GPS_export.iconbitmap(self.icon)
        vdo_path_label = ttk.Label(
            self.top_pano_GPS_export, text="VDO path (m_d):")
        seg_path_label = ttk.Label(
            self.top_pano_GPS_export, text="Seg file Path:")
        poi_path_label = ttk.Label(
            self.top_pano_GPS_export, text="Poi file Path:")
        GPS_save_path_label = ttk.Label(
            self.top_pano_GPS_export, text="GPS Save Path:")

        row0 = 0
        vdo_path_label.grid(row=row0, sticky=(tk.S, tk.N, tk.E, tk.W), padx=5)
        seg_path_label.grid(
            row=1 + row0, sticky=(tk.S, tk.N, tk.E, tk.W), padx=5)
        poi_path_label.grid(
            row=2 + row0, sticky=(tk.S, tk.N, tk.E, tk.W), padx=5)
        GPS_save_path_label.grid(
            row=3 + row0, sticky=(tk.S, tk.N, tk.E, tk.W), padx=5)

        vdo_button_browse = ttk.Button(
            self.top_pano_GPS_export, text="Browse ...", command=self.ask_pano_vdo_directory, width=10)
        seg_button_browse = ttk.Button(
            self.top_pano_GPS_export, text="Browse ...", command=self.ask_seg_directory, width=10)
        poi_button_browse = ttk.Button(
            self.top_pano_GPS_export, text="Browse ...", command=self.ask_poi_directory, width=10)
        save_button_browse = ttk.Button(
            self.top_pano_GPS_export, text="Browse ...", command=self.ask_pano_save_directory, width=10)

        vdo_entry_path = ttk.Entry(
            self.top_pano_GPS_export, textvariable=self.vdo_dir)
        seg_entry_path = ttk.Entry(
            self.top_pano_GPS_export, textvariable=self.seg_dir)
        poi_entry_path = ttk.Entry(
            self.top_pano_GPS_export, textvariable=self.poi_dir)
        save_entry_path = ttk.Entry(
            self.top_pano_GPS_export, textvariable=self.pano_save_dir)

        vdo_entry_path.grid(row=row0, column=1, columnspan=4, sticky=(
            tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        seg_entry_path.grid(row=1 + row0, column=1, columnspan=4,
                            sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        poi_entry_path.grid(row=2 + row0, column=1, columnspan=4,
                            sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        save_entry_path.grid(row=3 + row0, column=1, columnspan=4,
                             sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)

        vdo_button_browse.grid(row=row0, column=5, sticky=(
            tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        seg_button_browse.grid(row=1 + row0, column=5,
                               sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        poi_button_browse.grid(row=2 + row0, column=5,
                               sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)
        save_button_browse.grid(row=3 + row0, column=5,
                                sticky=(tk.S, tk.N, tk.E, tk.W), pady=5, padx=5)

        frame_cam_5 = tk.Frame(
            self.top_pano_GPS_export, relief="sunken", borderwidth=5, width=80, height=100)
        frame_cam_5.grid(row=4 + row0, column=0, rowspan=2,
                         columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        if self.deact_rear:
            self.cam_5 = ["c50"]
        else:
            self.cam_5 = ["c50", "c51"]
        cb5 = {}
        self.GPS_var_5 = {}  # checkbutton Boolean variable
        #self.vars_6, self.vars_7, self.vars_5 = [], [], []
        main_cb5 = ttk.Checkbutton(frame_cam_5, text="pano_cam", variable=self.GPS_var_cb5,
                                   command=lambda: self.main_cb5_control(self.GPS_var_cb5, self.GPS_var_5))
        img_export = ttk.Checkbutton(
            frame_cam_5, text="img_export", variable=self.img_export)
        run_day = ttk.Checkbutton(
            frame_cam_5, text="multi_folder(run_day)", variable=self.multi_folder)
        main_cb5.grid(row=0, sticky=(tk.E), pady=5, padx=5)
        img_export.grid(row=0, column=1, sticky=(tk.E), pady=5, padx=5)
        run_day.grid(row=0, column=2, sticky=(tk.E), pady=5, padx=5)
        for i, c_id in enumerate(self.cam_5):
            self.GPS_var_5[i] = tk.BooleanVar()
            self.GPS_var_5[i].set(1)
            cb5[i] = ttk.Checkbutton(frame_cam_5, variable=self.GPS_var_5[
                                     i], onvalue=1, offvalue=0, text="cam_{}".format(c_id))
            # self.vars_5.append(self.var_5[i].get())
            cb5[i].grid(row=1, column=i, sticky=(tk.E), pady=5, padx=5)

        self.top_pano_GPS_export.columnconfigure(1, weight=1)
        self.top_pano_GPS_export.rowconfigure(0, weight=0)

        b_ok = ttk.Button(self.top_pano_GPS_export, text="Output GPS",
                          width=13, command=self.show_progress_GPS)
        button_cancel = ttk.Button(self.top_pano_GPS_export, text="Cancel", width=13,
                                   command=lambda: self.toplevel_exit(self.top_pano_GPS_export, root))
        b_ok.grid(row=6 + row0, column=4)
        button_cancel.grid(row=6 + row0, column=5)
        self.pb_GPS = ttk.Progressbar(
            self.top_pano_GPS_export, orient='horizontal', mode='determinate')
        self.pb_GPS.grid(row=6 + row0, column=0, columnspan=4,
                         sticky=(tk.W, tk.E, tk.S, tk.N), padx=5, pady=5)
        self.status_GPS_frame = tk.Frame(
            self.top_pano_GPS_export, borderwidth=5, width=80, height=100)
        self.status_GPS_frame.grid(
            row=7 + row0, column=0, columnspan=4, sticky=(tk.S, tk.N, tk.W))
        self.status_GPS = ttk.Label(self.status_GPS_frame, text="Waiting ...")
        #self.status_h5.grid(row=3 + row0, column=0, sticky=(tk.S, tk.N, tk.W), padx=5)
        self.status_GPS.grid(row=0 + row0, column=0,
                             sticky=(tk.S, tk.N, tk.W), padx=5, pady=5)

    def main_exit(self, root):

        root.grab_release()
        root.destroy()

    def toplevel_exit(self, root, downlevel):

        root.grab_release()
        root.destroy()
        downlevel.grab_set()

    def print_cb_res(self):

        res = [value.get() for key, value in self.var_5.iteritems()]
        print(res)

    def get_entry(self):

        print(self.indir.get())
        return self.indir.get()

    def main_cb5_control(self, m_var_cb5, var_5):

        if m_var_cb5.get() is True:
            for key, value in var_5.iteritems():
                value.set(True)
        else:
            for key, value in var_5.iteritems():
                value.set(False)

    def main_cb6_control(self):

        if self.m_var_cb6.get() is True:
            for key, value in self.var_6.iteritems():
                value.set(True)
        else:
            for key, value in self.var_6.iteritems():
                value.set(False)

    def main_cb7_control(self):

        if self.m_var_cb7.get() is True:
            for key, value in self.var_7.iteritems():
                value.set(True)
        else:
            for key, value in self.var_7.iteritems():
                value.set(False)

    def show_progress_h52graph(self):

        # get run name from the h5 folder
        h5_path = self.outdir.get()
        if not os.path.exists(h5_path):
            self.status_h5["text"] = "HDF5 path does not exist!"
            return
        else:
            # check whether h5 files exist
            h5s = glob.glob("{}/*.h5".format(h5_path))
            if not h5s:
                self.status_h5["text"] = "No HDF5 files found!"
                return
            try:
                fn_evnt = r'{}/*.evnt.txt'.format(h5_path)
                fn_evnt = glob.glob(fn_evnt)
            except ValueError:
                print("event or s3db file(s) ... are missing!")
            evnt = re.split('/|\\\\', fn_evnt[0])[-1]
            run = re.split(r'\.(?!\d)', evnt)[0]

        # check whether the LB data of the processed run exists
        fn_lbd = "{}/{}.lbd".format(self.LB_dir.get(), run)
        fn_lbe = "{}/{}.lbe".format(self.LB_dir.get(), run)
        if not os.path.exists(self.LB_dir.get()):
            self.status_h5["text"] = "LockBox data path does not exist!"
            return
        if not (os.path.exists(fn_lbd) and os.path.exists(fn_lbe)):
            self.status_h5["text"] = "No LockBox data found in the folder!"
            return
        else:
            self.status_h5["text"] = "LB exists! Processing ..."

        # copy LB data to h5 folder
        shutil.copy(fn_lbe, h5_path)
        shutil.copy(fn_lbd, h5_path)

        # resolution analyse
        self.pb_h5.start()
        options = Options()  # fake options
        if options.debug and not options.use_cams:
            options.use_cams = ['60']
        # TODO: handle this also in get_args?
        if options.use_cams is None:
            # use all
            if options.debug:
                options.use_cams = ['60']
            else:
                options.use_cams = vdo.check.VdoRun.default_cams

        if options.save is not None and not len(options.save):
            # empty list -> use_cams
            options.save = options.use_cams

        # TODO: switch automatic between py2exe app and python script app
        # Use this only for py2exe application --Shulin
        elif options.save is None:
            options.save = options.use_cams

        speed_max = 40
        select_range = {'subrange_selected': False}
        # select_range={'subrange_selected' : True, 'offset_dist' : 500,
        # 'select_dist' : 50*1000} #15092918
        self.pb_h5.update()
        vdo.check.analyseVdo(folder=h5_path, run=None, options=options,
                             speed_max=speed_max, select_range=select_range)
        self.pb_h5.update()
        self.pb_h5.stop()
        self.status_h5["text"] = "Done!"
        return

    def show_progress_generate_h5(self):

        self.pb.start()
        folder = self.indir.get()
        if not os.path.exists(folder):
            self.status_lb["text"] = "Please select the correct VDO path!"
            self.pb.stop()
            return 1
        # check where vdo files exit
        vdos = glob.glob("{}/*.vdo".format(folder))
        if not vdos:
            self.pb.stop()
            self.status_lb["text"] = "No VDO files found!"
            return 1
        # select vdo files need to be processed
        vars_5 = [self.var_5[i].get() for i in self.var_5]
        vars_6 = [self.var_6[i].get() for i in self.var_6]
        vars_7 = [self.var_7[i].get() for i in self.var_7]
        arg_list = []
        # generate arg_list for panorama camera
        for i, val in enumerate(vars_5):
            if val:
                arg_list.append(
                    "{}/*{}.vdo".format(self.indir.get(), self.cam_5[i]))

        # generate arg_list for linear camera
        for i, val in enumerate(vars_6):
            if val:
                arg_list.append(
                    "{}/*{}.vdo".format(self.indir.get(), self.cam_6[i]))

        for i, val in enumerate(vars_7):
            if val:
                arg_list.append(
                    r"{}/*{}.vdo".format(self.indir.get(), self.cam_7[i]))

        if not arg_list:
            self.pb.stop()
            self.status_lb["text"] = "Nothing done!"
            return 1
        else:
            # check whether there exist corresponding vdo files for the camera
            # selected
            arg_list_vdo = [re.split('/|\\\\', i)[-1] for i in arg_list]
            for vdo in arg_list_vdo:
                vdos = glob.glob("{}/{}".format(folder, vdo))
                if not vdos:
                    self.pb.stop()
                    self.status_lb["text"] = "No {} files exist! Please un-check camera {}!".format(
                        vdo, re.split('\*|\.', vdo)[1])
                    return 1
            # generate h5 files
            for i, arg in enumerate(arg_list):
                self.pb.update()
                VR.WriteCSV(arg)
                self.pb["maximum"] = 100
                self.pb["value"] = (i + 1) * 100 / len(arg_list)
            # if folder[-1] == "\\":
            #    run = re.split('/|\\\\', folder)[-2]
            # else:
            #    run = re.split('/|\\\\', folder)[-1]

            # copy *.event.txt, *.s3db, files
            try:
                fn_evnt = r'{}/*.evnt.txt'.format(folder)
                fn_s3db = r'{}/*.s3db'.format(folder)
                fn_evnt = glob.glob(fn_evnt)
                fn_s3db = glob.glob(fn_s3db)
                files_copy = [fn_evnt[0], fn_s3db[0]]
                # print fn_evnt, fn_s3db
            except ValueError:
                print("event or s3db file(s) ... are missing!")
            evnt = re.split('/|\\\\', fn_evnt[0])[-1]
            run = re.split(r'\.(?!\d)', evnt)[0]

            try:
                for f in files_copy:
                    shutil.copy(f, run)
            except IOError:
                print("No external lbd lbe files copied!")

            current_folder_path, current_folder_name = os.path.split(
                os.getcwd())
            current_h5_dir = "{}/{}/{}".format(
                current_folder_path, current_folder_name, run)
            if os.path.exists(current_h5_dir):
                csv2h5(run)  # convert csv to h5
                if current_h5_dir != self.outdir.get():
                    des_folder = "{}/".format(self.outdir.get())
                    if not os.path.exists(des_folder):
                        os.makedirs(des_folder)
                    if not os.path.exists("{}/{}".format(des_folder, run)):
                        # move folder to target directory
                        shutil.move(current_h5_dir, des_folder)
                    else:
                        # h5 path and moving path are not the same
                        if os.path.abspath(current_h5_dir) != os.path.abspath("{}/{}".format(des_folder, run)):
                            # overwrite
                            try:
                                shutil.rmtree(os.path.abspath(
                                    "{}/{}".format(des_folder, run)))
                            except IOError:
                                print("Overwritten error occured!")
                            shutil.move(os.path.abspath(
                                current_h5_dir), os.path.abspath(des_folder))
                            #tmp = tpf.mkstemp(dir=os.path.dirname("{}/{}".format(des_folder, run)))
                            #shutil.move(os.path.abspath(current_h5_dir), tmp)
                            # shutil.rmtree(tmp)
                            print("Destination path already exists!\n"
                                  "Files are overwritten!")
                        else:
                            print("self-overwritten is not allowed!\n"
                                  "Files are saved in default (program) folder!")
            else:
                self.pb.stop()
                self.status_lb[
                    "text"] = "Generated hdf5 folder does not exists!"
                return 1
            self.pb.stop()
            self.status_lb["text"] = "Done!"
            self.pb["maximum"] = 100
            self.pb["value"] = 100

            return run

    def show_progress_export_pano_img(self, pb, status):

        pb.start()
        status["text"] = "Start Processing ..."
        pb["maximum"] = 100
        cnt = 0  # count the number of folders which donot consist vdo files
        run_folder = os.path.abspath(self.vdo_dir.get())
        run_p, run_n = os.path.split(run_folder)
        if not len(run_p):
            status["text"] = "Please select VDO folder!"
            pb.stop()
            return 1
        # if vdo base path and save dir path are the same, then stop
        elif os.path.abspath(run_p) == os.path.abspath(self.pano_save_dir.get()):
            status["text"] = "VDO folder and save path are identical!"
            pb.stop()
            return 1
        current_folder_path, current_folder_name = os.path.split(os.getcwd())
        b_path = run_folder
        data_out_option = 1
        save_pano_img = int(self.img_export.get())
        multi_folder = self.multi_folder.get()
        Uncertainty = .5  # to select the vdo file range in VR.VdoRead()
        if not os.path.exists(run_folder):
            status["text"] = "Please select the correct VDO path!"
            pb.stop()
            return 1
        # put the folder string to list
        run_folder = [run_folder]
        # change to multi_folder (run day) mode
        if multi_folder:
            # search existing sub-folders
            self.vdo_folders = next(os.walk(run_folder[0]))[1]
            run_folders = [run_folder[0] + '\\' + v for v in self.vdo_folders]
            if not len(run_folders):
                status["text"] = "No folders in the selected folder!"
                pb.stop()
                return 1
        else:
            run_folders = run_folder

        for n, run_folder in enumerate(run_folders):
            # find vdo files
            vdos = glob.glob(r"{}/*.vdo".format(run_folder))
            if len(vdos):
                vd = re.split('/|\\\\', vdos[0])[-1]
                self.r = re.split(r'\.', vd)[0]
            else:
                if multi_folder:
                    p, n_p = os.path.split(run_folder)
                    if n_p in self.vdo_folders:
                        self.vdo_folders.remove(n_p)
                    cnt += 1
                    continue
                else:
                    status["text"] = "No VDO files found!"
                    pb.stop()
                    return 1

            vars_5 = [self.GPS_var_5[i].get() for i in self.GPS_var_5]
            # generate arg_list for panorama camera
            self.pano_cam_ids[:] = []
            for i, val in enumerate(vars_5):
                if val:
                    self.pano_cam_ids.append("{}".format(self.cam_5[i]))
            # pano_cam_ids = ['c50', 'c51'] # default img are exported for both
            # cams
            if len(self.pano_cam_ids) == 0:
                status["text"] = "Please select at least one camera!"
                pb.stop()
                return 1
            for i, cam_id in enumerate(self.pano_cam_ids):
                pb.update()
                #self.queue = Queue.Queue()
                #ThreadedTask(self.queue, run_folder, cam_id, data_out_option, save_pano_img, Uncertainty).start()
                #self.top_pano_GPS_export.after(100, self.process_queue)
                VR.VdoRead(run_folder, cam_id, data_out_option,
                           save_pano_img, Uncertainty)
                # if save_pano_img:
                #    img_list = glob.glob("{}/{}/*.jpg".format(self.r, cam_id))
                #    print ("images are converting format...\n")
                #    for img in img_list:
                #        with Image(filename=img) as im:
                #            im.save(filename="{}".format(img))
                #    print ("images for pano {} are saved!".format(cam_id))
                if not multi_folder:
                    pb["value"] = (i + 1) * 100 / len(self.pano_cam_ids)
            if multi_folder:
                pb.update()
                pb["value"] = (n + 1) * 100 / len(run_folders)
        if cnt == len(run_folders):
            status["text"] = "No VDO files found!"
            pb.stop()
            return 1

        if multi_folder:
            # remove all generated run folders to base path
            b_path_path, b_path_name = os.path.split(b_path)
            des_folder = os.path.abspath(self.pano_save_dir.get())
            # create run day folder in programme folder
            # check b_path_name
            if not len(b_path_name):
                self.r_d = [re.findall('\d+', vf)[0]
                            for vf in self.vdo_folders]
                if len(self.r_d) > 1:
                    self.r_d_base = self.r_d[0]
                    for r in range(1, len(self.r_d)):
                        self.r_d_base = vdo.check.longestSubstringFinder(
                            self.r_d_base, self.r_d[r])
                else:
                    self.r_d_base = self.r_d[0]
                if len(self.r_d_base):
                    b_path_name = "Prorail{}si12".format(self.r_d_base)
                    self.b_name = b_path_name
                else:
                    b_path_name = "Prorail{}si12"
                    self.b_name = b_path_name
            b_path_abs = des_folder

            if not os.path.isdir(b_path_abs):
                os.mkdir(b_path_abs)
            # else:
            #    shutil.rmtree(b_path_abs, True)
            #    assert(os.path.isdir("b_path_abs") == False)
            #    os.mkdir(b_path_abs)

            # move all generated folders to run day folder
            #b_path_abs = os.path.abspath(b_path_name)
            self.r = b_path_name
            self.vdo_export_folders = []
            for i, vdo_f in enumerate(self.vdo_folders):
                # get digits from vdo_folders and compare with generated folder
                # (given the vdo name and folder name are different)
                run_day = re.findall('\d+', vdo_f)[0]
                # get folders in the current working directory
                f_pwd = next(os.walk('./'))[1]
                vdo_f = [f for f in f_pwd if run_day in f][0]
                if (b_path_abs != os.path.abspath(os.getcwd())):
                    if vdo_f in next(os.walk(b_path_abs))[1]:
                        shutil.rmtree(os.path.join(b_path_abs, vdo_f))
                    shutil.move(vdo_f, b_path_abs)
                # vdo exporting folders names
                self.vdo_export_folders.append(vdo_f)
            current_pano_img_dir = b_path_abs
        else:
            current_pano_img_dir = os.path.abspath(
                "{}/{}/{}".format(current_folder_path, current_folder_name, self.r))
        if os.path.exists(current_pano_img_dir):
            if current_pano_img_dir != os.path.abspath(self.pano_save_dir.get()):
                des_folder = os.path.abspath(self.pano_save_dir.get())
                if not os.path.exists(des_folder):
                    os.makedirs(des_folder)
                if not os.path.exists("{}/{}".format(des_folder, self.r)):
                    # move folder to target directory
                    shutil.move(current_pano_img_dir, des_folder)
                else:
                    # h5 path and moving path are not the same
                    if os.path.abspath(current_pano_img_dir) != os.path.abspath("{}/{}".format(des_folder, self.r)):
                        # overwrite
                        try:
                            shutil.rmtree(os.path.abspath(
                                "{}/{}".format(des_folder, self.r)))
                        except IOError:
                            print("Overwritten error occured!")
                        shutil.move(os.path.abspath(
                            current_pano_img_dir), os.path.abspath(des_folder))
                        #tmp = tpf.mkstemp(dir=os.path.dirname("{}/{}".format(des_folder, run)))
                        #shutil.move(os.path.abspath(current_h5_dir), tmp)
                        # shutil.rmtree(tmp)
                        print("Destination path already exists!\n"
                              "Files are overwritten!")
                    else:
                        print("self-overwritten is not allowed!\n"
                              "Files are saved in default (program) folder!")
        else:
            self.pb.stop()
            self.status_lb["text"] = "Pano image folder does not exists!"
            return 1
        pb.stop()
        status["text"] = "Export from VDO finished!"
        return 0

    def show_progress_export_pano_img_dpc(self):
        # import image (if img_export check box is checked) and the
        # corresponding csv files
        result = self.show_progress_export_pano_img(
            self.pb_pano, self.status_pano)
        if result == 1:
            self.pb_pano.stop()
            return 1
        multi_folder = self.multi_folder.get()
        # if multi_folder:
        #    r_d = re.findall('\d+', self.vdo_folders[0])[0]
        # else:
        #    r_d = re.findall('\d+', self.r)[0]
        self.pb_pano.start()
        if multi_folder:
            b_path_path, b_path_name = os.path.split(
                os.path.abspath(self.vdo_dir.get()))
            if not len(b_path_name):
                b_path_name = self.b_name
            run_folder = os.path.abspath(self.pano_save_dir.get())
            if not len(self.vdo_folders):
                self.pb_pano.stop()
                self.status_pano[
                    "text"] = "No sub-folders found in the input folder!"
                return 1
            run_folders = [run_folder + '\\' +
                           v for v in self.vdo_export_folders]
        else:
            run_folder = os.path.join(self.pano_save_dir.get(), self.r)
            run_folders = [run_folder]

        for n, run_folder in enumerate(run_folders):
            r_d = re.findall('\d+', os.path.split(run_folder)[1])[0]
            if multi_folder:
                run_path, run_name = os.path.split(run_folder)
                # new DPC folder structure
                DPC_folder_CSV = os.path.join(run_path, "GDMimport_CSV")
                DPC_folder_front = os.path.join(run_path, "FrontCam")
                DPC_folder_front_run_l1 = os.path.join(
                    DPC_folder_front, run_name)
                DPC_folder_front_run = os.path.join(
                    DPC_folder_front, run_name, run_name)
                if not self.deact_rear:
                    DPC_folder_rear = os.path.join(run_path, "RearCam")
                    DPC_folder_rear_run_l1 = os.path.join(
                        DPC_folder_rear, run_name)
                    DPC_folder_rear_run = os.path.join(
                        DPC_folder_rear, run_name, run_name)
                vdo_dir = os.path.join(self.vdo_dir.get(), run_name)
            else:
                ##DPC_folder = "{}/{}".format(run_folder, self.r)
                run_path, run_name = os.path.split(run_folder)
                DPC_folder_CSV = os.path.join(run_path, "GDMimport_CSV")
                DPC_folder_front = os.path.join(run_path, "FrontCam")
                DPC_folder_front_run_l1 = os.path.join(
                    DPC_folder_front, self.r)
                DPC_folder_front_run = os.path.join(
                    DPC_folder_front, self.r, self.r)
                if not self.deact_rear:
                    DPC_folder_rear = os.path.join(run_path, "RearCam")
                    DPC_folder_rear_run_l1 = os.path.join(
                        DPC_folder_rear, self.r)
                    DPC_folder_rear_run = os.path.join(
                        DPC_folder_rear, self.r, self.r)
                vdo_dir = os.path.join(self.vdo_dir.get())
            c50_folder = os.path.join(run_folder, "c50")
            c51_folder = os.path.join(run_folder, "c51")
            # read event data
            vdo_dir_path, vdo_dir_n = os.path.split(vdo_dir)
            if multi_folder:
                vdo_dir_n = [f for f in self.vdo_folders if vdo_dir_n in f][0]
            vdo_dir = os.path.join(vdo_dir_path, vdo_dir_n)
            try:
                evnt = vdo.check.get_evnt(vdo_dir)
                dmaSync = vdo.check.get_dmaSync(evnt)
                Odo_Ext_inter = vdo.check.interp1d(
                    dmaSync.Odometer, dmaSync.ExtCounter)
                Odo_Ext_extra = vdo.check.extrap1d(Odo_Ext_inter)
                offset_evnt = vdo.check.get_evnt_offset(dmaSync)
            except ValueError:
                pass
            csv_files, csv_dataframe = [], {}
            if not os.path.exists(run_folder):
                self.status_pano["text"] = "Image export directory not found!"
                self.pb_pano.stop()
                return 1
            else:
                if not os.path.exists(DPC_folder_front):
                    os.mkdir(DPC_folder_front)
                if not os.path.exists(DPC_folder_CSV):
                    os.mkdir(DPC_folder_CSV)
                if not os.path.exists(DPC_folder_front_run_l1):
                    os.mkdir(DPC_folder_front_run_l1)
                    os.mkdir(DPC_folder_front_run)
                if not self.deact_rear:
                    if not os.path.exists(DPC_folder_rear):
                        os.mkdir(DPC_folder_rear)
                    if not os.path.exists(DPC_folder_CSV):
                        os.mkdir(DPC_folder_CSV)
                    if not os.path.exists(DPC_folder_rear_run_l1):
                        os.mkdir(DPC_folder_rear_run_l1)
                        os.mkdir(DPC_folder_rear_run)
                if os.path.isdir(c50_folder):
                    try:
                        csv_files.append(
                            glob.glob("{}/{}/*IntCntFrNum.csv".format(run_folder, "c50"))[0])
                    except IndexError:
                        csv_files.append(os.path.join(run_folder, 'c50', os.path.split(
                            run_folder)[1] + '_c50_IntCntFrNum.csv'))
                if os.path.isdir(c51_folder):
                    try:
                        csv_files.append(
                            glob.glob("{}/{}/*IntCntFrNum.csv".format(run_folder, "c51"))[0])
                    except IndexError:
                        csv_files.append(os.path.join(run_folder, 'c51', os.path.split(
                            run_folder)[1] + '_c51_IntCntFrNum.csv'))
            for i, csv in enumerate(csv_files):
                pano_extcnt_info = pd.DataFrame()
                pano_info = pd.read_csv(
                    csv, names=['Odometer:', 'FrameNum:'], skiprows=2, delimiter=",")
                if (len(pano_info.index) == 0):
                    pano_extcnt_info['IntCnt'] = []
                    pano_extcnt_info['IntCnt_Sync'] = []
                    pano_extcnt_info['ExtCnt'] = []
                    pano_extcnt_info['Frame_No.'] = []
                else:
                    IntCnt_sync = pano_info[
                        'Odometer:'] / self.factor + offset_evnt
                    # external counter of pano images
                    pano_ext = Odo_Ext_extra(pano_info['Odometer:'])
                    pano_extcnt_info['IntCnt'] = pano_info['Odometer:']
                    pano_extcnt_info['IntCnt_Sync'] = IntCnt_sync.astype('int')
                    pano_extcnt_info['ExtCnt'] = pd.Series(
                        pano_ext).astype('int')
                    pano_extcnt_info['Frame_No.'] = pano_info['FrameNum:']
                csv_dataframe[i] = pano_extcnt_info
                csv_bname = os.path.basename(csv)
                fn = re.split('\.', csv_bname)[0]
                cam_id = re.split("\_", fn)[-2]
                # add cam_id column
                if cam_id == "c50":
                    csv_dataframe[i]["Cam_ID"] = 1
                elif cam_id == "c51":
                    csv_dataframe[i]["Cam_ID"] = 2
                # search pics
                # change pic_str if '[' or ']' in run_folder string
                if ('[' or ']') in run_folder:
                    run_folder_temp = self.escape(run_folder)
                    pic_str = "{}/{}/*.jpg".format(run_folder_temp, cam_id)
                else:
                    pic_str = "{}/{}/*.jpg".format(run_folder, cam_id)
                pics = glob.glob(pic_str)
                pic_list = [os.path.basename(x) for x in pics]
                if len(pic_list):
                    csv_dataframe[i]["Img_name"] = pic_list
                if cam_id == "c50":
                    #new_csv_name = "{}/{}.csv".format(DPC_folder_front_run, "Prorail{}si12_DMAImage_Cam1".format(r_d))
                    if ('[' or ']') in DPC_folder_front_run:
                        DPC_folder_front_run_temp = self.escape(
                            DPC_folder_front_run)
                        jpegs = glob.glob(
                            "{}/*.jpg".format(DPC_folder_front_run_temp))
                    else:
                        jpegs = glob.glob(
                            "{}/*.jpg".format(DPC_folder_front_run))
                    for f in jpegs:
                        os.remove(f)
                    for pic in pics:
                        shutil.move(pic, DPC_folder_front_run)
                elif cam_id == "c51":
                    #new_csv_name = "{}/{}.csv".format(DPC_folder_rear_run, "Prorail{}si12_DMAImage_Cam2".format(r_d))
                    if ('[' or ']') in DPC_folder_rear_run:
                        DPC_folder_rear_run_temp = self.escape(
                            DPC_folder_rear_run)
                        jpegs = glob.glob(
                            "{}/*.jpg".format(DPC_folder_rear_run_temp))
                    else:
                        jpegs = glob.glob(
                            "{}/*.jpg".format(DPC_folder_rear_run))
                    for f in jpegs:
                        os.remove(f)
                    for pic in pics:
                        shutil.move(pic, DPC_folder_rear_run)
            if len(csv_files) == 2:
                merge_dataframe = [csv_dataframe[0], csv_dataframe[1]]
                merge = pd.concat(merge_dataframe).sort_values(by=['IntCnt'])
            else:
                merge_dataframe = csv_dataframe[0]
                merge = merge_dataframe.sort_values(by=['IntCnt'])
            new_csv_name = "{}/{}.csv".format(DPC_folder_CSV,
                                              "Prorail{}si12_DMAImage".format(r_d))
            merge.to_csv(new_csv_name, sep=';', index=False)
            # delete run folders
            if os.path.isdir(run_folder):
                shutil.rmtree(run_folder)
        self.pb_pano.stop()
        self.status_pano["text"] = "Structuring data finished!"

        return

    def show_progress_vdo2graph(self):

        self.pb["maximum"] = 100
        self.pb["value"] = 0
        res = self.show_progress_generate_h5()
        self.pb["value"] = 50
        if res == 1:
            return
        h5_path = self.outdir.get()
        h5_path = "{}/{}".format(h5_path, res)
        if not os.path.exists(h5_path):
            self.status_lb["text"] = "HDF5 path does not exist!"
            return

        # check whether the LB data of the processed run exists
        fn_lbd = "{}/{}.lbd".format(self.LB_dir.get(), res)
        fn_lbe = "{}/{}.lbe".format(self.LB_dir.get(), res)
        if not os.path.exists(self.LB_dir.get()):
            self.status_lb["text"] = "LockBox data path does not exist!"
            return
        if not (os.path.exists(fn_lbd) and os.path.exists(fn_lbe)):
            self.status_lb["text"] = "No LockBox data found in the folder!"
            return
        else:
            self.status_lb["text"] = "LB exists! Processing ..."

        # copy LB data to h5 folder
        shutil.copy(fn_lbe, h5_path)
        shutil.copy(fn_lbd, h5_path)

        # resolution analyse
        options = Options()  # fake options
        if options.debug and not options.use_cams:
            options.use_cams = ['60']
        # TODO: handle this also in get_args?
        if options.use_cams is None:
            # use all
            if options.debug:
                options.use_cams = ['60']
            else:
                options.use_cams = vdo.check.VdoRun.default_cams

        if options.save is not None and not len(options.save):
            # empty list -> use_cams
            options.save = options.use_cams

        # TODO: switch automatic between py2exe app and python script app
        # Use this only for py2exe application --Shulin
        elif options.save is None:
            options.save = options.use_cams

        speed_max = 40
        select_range = {'subrange_selected': False}
        vdo.check.analyseVdo(folder=h5_path, run=None, options=options,
                             speed_max=speed_max, select_range=select_range)
        self.pb["value"] = 100
        self.status_lb["text"] = "Done!"
        self.pb.stop()

    def show_progress_GPS(self):
        self.pb_GPS.start()
        res = self.show_progress_export_pano_img(self.pb_GPS, self.status_GPS)
        if res == 1:
            self.pb_GPS.stop()
            return 1
        # debug
        self.pano_cam_ids = ['c50']
        self.pb_GPS.start()
        self.status_GPS["text"] = "Waiting ..."
        self.pb_GPS["maximum"] = 100
        multi_folder = self.multi_folder.get()
        # get vdo folder
        vdo_path = self.vdo_dir.get()
        vdo_p, self.r = os.path.split(vdo_path)
        seg_path, poi_path = self.seg_dir.get(), self.poi_dir.get()
        # get seg, poi file
        if multi_folder:
            # find all seg, poi files in the seg_path, poi_path
            seg_strs, poi_strs = [os.path.join(seg_path, '*{}*seg.csv'.format(v)) for v in self.vdo_folders], [
                os.path.join(poi_path, '*{}*poi.csv'.format(v)) for v in self.vdo_folders]
            seg_file, poi_file = np.atleast_1d(np.squeeze([glob.glob(seg_str) for seg_str in seg_strs])), np.atleast_1d(
                np.squeeze([glob.glob(poi_str) for poi_str in poi_strs]))
        else:
            seg_strs, poi_strs = os.path.join(
                seg_path, '*{}*seg.csv'.format(self.r)), os.path.join(seg_path, '*{}*poi.csv'.format(self.r))
            seg_file, poi_file = glob.glob(seg_strs), glob.glob(poi_strs)
        if multi_folder:
            # get vdo folders
            for j, vdo_folder in enumerate(self.vdo_folders):
                # get path for each measure run folder (in order to read event
                # file)
                vdo_p = os.path.join(vdo_path, vdo_folder)  # vdo_path
                # get vdo base path and vdo base folder
                vdo_bp, vdo_bf = os.path.split(vdo_path)
                if not len(vdo_bf):
                    vdo_bf = "Prorail{}si12".format(self.r_d_base)
                # get save path
                save_p = os.path.join(self.pano_save_dir.get(), vdo_bf)
                # get corresponding seg_file and poi_file
                seg_f = [seg for seg in seg_file if vdo_folder in seg]
                poi_f = [poi for poi in poi_file if vdo_folder in poi]
                if not len(seg_f):
                    self.status_GPS[
                        "text"] = "No seg file for {}".format(vdo_folder)
                    self.pb_GPS.stop()
                    return 1
                if not len(poi_f):
                    self.status_GPS[
                        "text"] = "No poi file for {}".format(vdo_folder)
                    self.pb_GPS.stop()
                    return 1
                for i, cam_id in enumerate(self.pano_cam_ids):
                    vdo.check.save_GPS_coord(vdo_folder, poi_f[0], seg_f[
                                             0], cam_id, vdo_p, self.factor, self.pano_ante_dist, save_path=save_p)
                self.pb_GPS.update()
                self.pb_GPS["value"] = (j + 1) * 100 / len(self.vdo_folders)
        else:  # measure run is selected
            if not len(seg_file):
                self.status_GPS["text"] = "No Seg file found!"
                return 1
            if not len(poi_file):
                self.status_GPS["text"] = "No Poi file found!"
                return 1
            for i, cam_id in enumerate(self.pano_cam_ids):
                self.pb_GPS.update()
                vdo.check.save_GPS_coord(self.r, poi_file[0], seg_file[
                                         0], cam_id, vdo_path, self.factor, self.pano_ante_dist, save_path=self.pano_save_dir.get())
                self.pb_GPS["value"] = (i + 1) * 100 / len(self.pano_cam_ids)
        self.status_GPS["text"] = "Done!"
        self.pb_GPS.stop()
        return 0

    def escape(self, s):
        r = re.compile("(%s)" % "|".join(re.escape(c) for c in "*?["))
        return r.sub(r"[\1]", s)


class CamSlectionDialog(tk.Frame):

    def __init__(self, root):

        tk.Frame.__init__(self, root)
        label_1 = tk.Label(root, text="file path")
        entry_1 = tk.Entry(root)
        label_1.grid(row=0)
        entry_1.grid(row=0, column=1)
