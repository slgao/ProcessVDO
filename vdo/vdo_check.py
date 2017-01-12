# coding: utf-8
import glob, os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
from scipy.interpolate import interp1d
from scipy import array
import sqlite3
import re
import math
# local
from data_proc.signal import detect_peaks, get_clusters_single1D, get_regions
from LocBox.LocBox_parse import LB
from text_converters import DataColumns
from enum import Enum

## run class(es)
class VdoRun(object):
    ## TODO: derive from generic Run class
    default_cams = {'60', '61', '62', '64', '65',
                    '70', '71', '72', '74', '75',
                    'c50', 'c51'}
    def __init__(self, folder, use_cams,
                 cams=None,
                 run=None,
                 processBundle=None,
                 ):
        self.folder = folder
        self.run = run
        self.res = Results()
        if cams is not None:
            cams = set(cams)
        else:
            cams = self.__class__.default_cams
        assert set(use_cams).issubset(cams)
        self.use_cams = use_cams
    def __repr__(self):
        patt = '{}: run {} - uses cams {} in path "{}"'
        return patt.format(self.__class__.__name__, 
                           self.run, 
                           self.use_cams, 
                           self.folder)
    def load(self):
        pass
        ## TODO
        #self.load_extern()
        #if self.res.lb:
         #   self.set_default_run()
        #self.load_vdo()
    def analyse(self):
        pass


class VdoData(object):
    ## TODO: derive from generic Data class
    def __init__(self,
                 lb=None,
                 evnt=None,
                 trackNetCfg=None,
                 vdos={},
                 ):
        self.lb = lb
        self.evnt = evnt,
        self.trackNetCfg = trackNetCfg
        self.vdos = vdos
    def load(self, folder, run):
        ext = get_extData(folder, run)
        run = ext.keys()[0]
        self.lb = ext[run]['lb']
        self.trackNetCfg = ext[run]['s3db']
        self.evnt = ext[run]['evnt']
        return run

## derived
class VdoResults(object):
    ## TODO: eventually derive from generic Data class
    ## TODO: improve initialization
    ## TODO: shift processing function as 'load' method into this class
    ## TODO: extend with figs, ...
    attributes = ['vdoProc', 
                  'cnts', 'speed', 'speed_max',
                  'factor', 'divider',
                  'dmaSync', 'exInterp', 'cntExt_interpf', 'cntInt_interpf',
                  'speed_cnts_odo', 'odo_clusters', 'select_range'
                  ]
    def __init__(self, cam_id, 
                 **kwargs):
        self.cam_id = cam_id
        for attr in self.__class__.attributes:
            setattr(self, attr, kwargs.get(attr))
    def as_dict(self):
        return {self.cam_id: self}

## classes for Figure creation
class Fig(object):
    def __init__(self, num, nrows=0, ncols=0):
        self.num = num
        self.fig = None
        self.nrows = nrows
        self.ncols = ncols
        self._attrs = ['nrows', 'ncols']
        self.filename = ''
        
    def update(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
        
    class _FigError(Exception):
        def __init__(self, attrs):
            self.attrs = attrs
        def __str__(self):
            return '\n## One or more of attributes {} \n## is/are not set (or not correct).'.format(self.attrs)
            
    def _do_check(self):
        ## TODO: with setter for to be checked attributes
        ## value of self.check could be updated automatically
        attributes = getattr(self, 'attributes', []) + self._attrs
        def _raise():
            raise self._FigError(attributes)
        self.raise_FigError = _raise 
        self.check = np.asarray([hasattr(self, a)
                                 for a in attributes]).all()
        # Commented by Shulin, this keeps the number of subplots from changing
        #self.check &= self.nrows*self.ncols
        return self.check
        
    def create_fig(self, sharex=True, sharey=False):
        if not self._do_check():
            self.raise_FigError()
        self.fig, self.axs = plt.subplots(self.nrows, self.ncols, 
                                          sharex=sharex,
                                          sharey=sharey,
                                          num=self.num,
                                          )
        if len(self.fig.axes)==1:
            # stupid change in subplots output for single subplot
            self.ax = self.axs
            self.axs = [self.ax]
        else:
            self.ax = self.axs[0] # could be set also to None or -1 ...
    
    def _plot(self):
        pass
        
    def plot(self):
        plt.close(self.num)
        self.create_fig()
        self._plot()
        
    def save(self, 
             imgtype='png',
             bbox_inches='tight',
             dpi=150,
             ):
        if self.fig:
            if self.filename:
                self.fig.savefig('{}.{}'.format(self.filename, imgtype), 
                                dpi=dpi,
                                bbox_inches=bbox_inches,
                                )
                
    def close(self):
        plt.close(self.num)


class FigSpeed(Fig):
    attributes = ['folder','run',
                  'cnts', 'speed',
                  ]
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.suffix = kwargs.get('suffix', 'speed')
        
    def _plot(self):
        self.filename = '{}/{}-speed'.format(self.folder, self.run, self.suffix)
        #percs = range(0, 101, 10)
        #pd.DataFrame(dict(percentile=percs, speed_kmph=ml.prctile(speed, percs)))
        ax = self.ax
        ax.plot(self.cnts, self.speed, 'k.')
        ax.set_xlabel('LocBox cnts')
        ax.set_ylabel('speed (km/h)')
        ax.set_title(self.run)
        
class FigCam(Fig):
    attributes = [##'folder', 'run',
                  'folder',
                  'vdoData', 'vdoResults',
                  ]
    def __init__(self, *args, **kwargs):
        super(FigCam, self).__init__(*args, **kwargs)
        self.suffix = kwargs.get('suffix', self.num)
        # use cam_id as default num, but can be set differently
        self.cam_id = kwargs.get('cam_id', self.num)
        
    def _extract_attrs(self):
        # attributes
        cam_id = self.vdoResults.cam_id
        recp = self.vdoData.vdos[cam_id]
        lb = self.vdoData.lb
        factor = self.vdoResults.factor
        divider = self.vdoResults.divider
        dmaSync = self.vdoResults.dmaSync
        exInterp = self.vdoResults.exInterp
        cntExt_interpf = self.vdoResults.cntExt_interpf
        cntInt_interpf = self.vdoResults.cntInt_interpf
        select_range = self.vdoResults.select_range
        resolution = np.float(divider)/factor
        # when sub range is selected the num_frame_should is calculated by the range distance
        if select_range['subrange_selected']:
            num_frame_should = round((cntExt_interpf(recp.Odometer.iloc[-1]) - cntExt_interpf(recp.Odometer.iloc[0])) \
            / resolution)
        #    num_frame_should = round((exInterpf(recp.Odometer.iloc[-1], cntExt_interpf) - exInterpf(recp.Odometer.iloc[0], cntExt_interpf)) \
        #/ resolution)
        else:
            num_frame_should = round((lb._data_TCP.Counter.iloc[-1] - dmaSync.ExtCounter.iloc[0]) \
            / resolution)
        # title
        text = '{} - camera {} (frame each {:.3f} mm)\n\
        Frames: #{} should, #{} recorded'
        title = text.format(lb.filename,
                            self.num,
                            resolution,
                            np.int(num_frame_should),
                            np.size(recp.FrameNum),
                            )
        return (recp, 
                lb, 
                divider, factor,
                dmaSync, exInterp, cntExt_interpf, cntInt_interpf,
                ), title
        
    def _plot(self):
        #
        (recp, lb, divider, factor, dmaSync, exInterp, _, cntInt_interpf), title = \
            self._extract_attrs()
        #
        speed = self.vdoResults.speed
        speed_max = self.vdoResults.speed_max
        speed_cnts_odo = self.vdoResults.speed_cnts_odo
        cam_id = self.cam_id
        self.filename = '{}/{}-{}'.format(self.folder, lb.filename, self.suffix)
        fig = self.fig
        axs = self.axs
        n , ms , eps , threshold = 0, 1.0, 1E-3, 2 * divider / factor  # eps = 1E-3 lowest difference to show (in mm)
        diff_odo = np.diff(recp.Odometer)
        # correct misaligned resolution
        diff_odo = correct_res_misalignment(diff_odo, divider)
        recp_odo = (recp.Odometer.values[:-1]/1E6)

        # reduce the number of points to be plotted
        reduce_plot_points = False
        if (reduce_plot_points):
            step = 201 # should be an odd number
            min_diff, median_diff, max_diff, min_ind, median_ind, max_ind = data_filter(diff_odo, step = step) # get min, max aver arrays respectively
            diff_odo = np.r_[min_diff, median_diff, max_diff] # concatenate the arrays to plot
            diff_ind = np.r_[min_ind, median_ind, max_ind]
            recp_odo = recp_odo[diff_ind]

        # cluster points to be plotted
        data_fit_ind = np.where((diff_odo > 0) & (diff_odo <= threshold * factor) & (diff_odo != divider))
        data_out_ind = np.where(np.logical_or((diff_odo <= 0),  (diff_odo > threshold * factor)))
        data_right_ind = np.where((diff_odo == divider))
        if len(data_fit_ind):
            axs[n].plot(recp_odo[data_fit_ind], diff_odo[data_fit_ind] / factor,
                        'c.', ms = ms, label='Odometer_under_threshold')
        if len(data_right_ind):
            axs[n].plot(recp_odo[data_right_ind], diff_odo[data_right_ind] / factor,
                        'b.', ms = ms, label='Odometer_exact')
        if len(data_out_ind):
            axs[n].plot(recp_odo[data_out_ind], diff_odo[data_out_ind] / factor,
                        'm.', ms = ms, label='Odometer_outlier')
        axs[n].plot(axs[n].get_xlim(), [threshold] * 2, 'k-.', label = 'threshold = {} mm'.format(threshold))
        left, right = recp_odo[0], recp_odo[-1]
        axs[n].set_title('diff of Int Cnt (Odometer) / {}'.format(int(factor),
                         fontsize=10))
        # change resolution represented by internal counter to mm
        #axs[n].set_ylabel('(in 1/{} mm)'.format(int(factor)))
        axs[n].set_ylabel("resolution")

        axs[n].set_yscale('symlog', linthreshy = threshold, linscaley = 5)
        axs[n].set_ylim(ymin = 0)
        if (cam_id == 'c50' or cam_id == 'c51'):
            axs[n].set_yticks(np.arange(0, threshold, 1000), minor = True)
        else:
            axs[n].set_yticks(np.arange(0, threshold, 1), minor = True)
        axs[n].legend(prop={'size':4}, loc='upper left')
        # plot speed
        n += 1
        axs[n].plot(speed_cnts_odo/1E6, speed, 'b.', ms = ms, label = 'Speed')
        axs[n].plot([left, right], [speed_max]*2,
                    'r--', ms = ms/2, label='chosen maximum')
        axs[n].plot([left, right], [speed_max + 30]*2,
                    'r--', ms = ms/2, label='chosen maximum')
        axs[n].set_title('Speed',
                         fontsize=10)
        axs[n].set_xlim(left, right)
        axs[n].set_ylim(0, 120)
        """
        # Change figure size in cam_check function if the following block is commented
        n += 1
        axs[n].plot((recp.Odometer[:-1]/1E6), np.diff(recp.FrameNum),
                    'k.', ms = ms, label='FrameNum')
        axs[n].set_title('diff of FrameNum'.format(int(factor)),
                         fontsize=10)
        axs[n].set_ylabel('(cnts)'.format(int(factor)))
        axs[n].set_ylim(ymin=min(0, axs[0].get_ylim()[0]))
        #
        if divider<=8:
            n += 1
            X = abs((exInterp-dmaSync.ExtCounter.iloc[0]) - recp.Odometer/factor)
            X[X<eps] = eps
            axs[n].plot((recp.Odometer/1E6), X, 'g.', ms = ms,
                        label='recorded')
            axs[n].set_yscale('log')
            # missing frames
            # (DMA evnt does not show latest Odometer cnt, using latest SYNC)
            if recp.Odometer.iloc[-1]<dmaSync.Odometer.iloc[-2]:
                axs[n].plot(np.r_[recp.Odometer.iloc[-1], dmaSync.Odometer.iloc[-1]]/1E6,
                            2*[axs[1].get_ylim()[1]], 'r-',
                            lw=5.0, label='Missing!')
                axs[n].plot(np.r_[recp.Odometer.iloc[-1], dmaSync.Odometer.iloc[-1]]/1E6,
                            2*[axs[n].get_ylim()[1]], 'r-',
                            lw=5.0, label='Missing!')            
            axs[n].set_title('Ext Cnt - Int Cnt/{}'.format(int(factor)),
                             fontsize=10)
            axs[n].set_ylabel('(in mm)')
            axs[n].set_xlabel('Int Cnt (1/{} km)'.format(int(factor)))
            axs[n].legend(prop={'size':8}, loc='lower right')
        """
        # can be deleted if the upper commented codes uncommented
        axs[n].set_xlabel('Int Cnt (1/{} km)'.format(int(factor)))
        ## TODO: could be also separate class method
        fig.suptitle(title, fontsize=13)
        for i in range(n + 1):
            axs[i].tick_params(axis='both', which='major', labelsize=7)
        fig.tight_layout()
        fig.subplots_adjust(top=0.85)

class FigCam2(FigCam):
    def _extract_attrs(self):
        # attributes
        cam_id = self.vdoResults.cam_id
        recp = self.vdoData.vdos[cam_id]
        lb = self.vdoData.lb
        factor = self.vdoResults.factor
        divider = self.vdoResults.divider
        dmaSync = self.vdoResults.dmaSync
        exInterp = self.vdoResults.exInterp
        cntExt_interpf = self.vdoResults.cntExt_interpf
        cntInt_interpf = self.vdoResults.cntInt_interpf
        odo = self.vdoResults.vdoProc.Odometer_regions
        odo_clusters = self.vdoResults.odo_clusters
        select_range = self.vdoResults.select_range
        resolution = np.float(divider)/factor
        ## zero out the negative elements
        odo_clusters[odo_clusters < 0] = 0
        # obtain should from LocBox counter
        num_frame_should = np.int(np.nansum(np.diff(cntExt_interpf(odo)))/(divider/factor)) + len(odo_clusters)
        num_frame_recorded = np.count_nonzero(~np.isnan(odo))
        if num_frame_should == 0:
            record_percentage = np.nan
        else:
            record_percentage = round(np.float(num_frame_recorded)/num_frame_should*100, 3)
        ## title
        text = '{} - camera {} (frame each {:.3f} mm)\n\
        Frames: #{} should, #{} recorded, i.e. {:.3f}%'
        title = text.format(lb.filename,
                            self.num,
                            resolution,
                            num_frame_should,
                            num_frame_recorded,
                            record_percentage
                            )
        return (recp,
                lb,
                divider, factor,
                dmaSync, exInterp, cntExt_interpf, cntInt_interpf,
                ), title

    def _plot(self):
        #
        (_, lb, divider, factor, _, exInterp, _, _), title = \
            self._extract_attrs()
        ## TODO: modify or use another extraction method
        cnts = self.vdoResults.cnts
        speed = self.vdoResults.speed
        speed_max = self.vdoResults.speed_max
        odo = self.vdoResults.vdoProc.Odometer_regions
        ## TODO: plot also FrameNum regions
        frame = self.vdoResults.vdoProc.FrameNum_regions
        #
        self.filename = '{}/{}-{}'.format(self.folder, lb.filename, self.suffix)
        #
        fig = self.fig
        axs = self.axs
        ms = 1. # marker size
        lw = .1
        n = 0
        udiffs0 = np.diff(odo)
        udiffs0 = correct_res_misalignment(udiffs0, divider)
        # TODO: cluster exInterp so that the 'num_frame_should' can be calculated in the subrange_selected case
        axs[n].plot(exInterp[1:], udiffs0/factor, 'k.'+'-', ms=ms, lw=lw)
        axs[n].set_title('run {} - cam {} = {}'.format(lb.filename, self.cam_id, speed_max))
        axs[n].set_ylabel('line/frame sample distance (in mm)')
        axs[n].set_ylim(ymin=0)
        left, right = axs[n].get_xlim()[0], axs[n].get_xlim()[1]
        n += 1
        axs[n].plot(cnts, speed, 'b.', ms=ms, label='speed')
        axs[n].plot(axs[0].get_xlim(), [speed_max]*2, 
                    'r--', label='chosen maximum')
        axs[n].set_ylabel('(km/h)')
        axs[n].set_ylim(0, 120)
        axs[n].set_xlabel('LB cnts')
        axs[n].set_xlim(left, right)
        ## TODO: could be also separate class method
        fig.suptitle(title, fontsize=13)
        fig.tight_layout()
        fig.subplots_adjust(top=0.85)

class FigCam3(FigCam):
    def _plot(self):
        #
        (_, lb, _, factor, _, _, _, _), title = \
            self._extract_attrs()
        ## TODO: modify or use another extraction method
        speed = self.cam_results['speed_region']
        speed_all = self.cam_results['speed_all']
        speed_max = self.vdoResults.speed_max
        cam_id = self.vdoResults.cam_id
        divider = self.vdoResults.divider
        odo = self.cam_results['odo_under_max_{}'.format(cam_id)]
        odo_all = self.cam_results['odo_all_{}'.format(cam_id)]
        self.filename = '{}/{}-{}'.format(self.folder, lb.filename, self.suffix)
        fig = self.fig
        axs = self.axs
        resolution = np.float(divider)/factor
        ms, lw, bar_width, opacity, n, res_threshold = 6., 1.5, .002, .4, 0, 4 * resolution + .1 # marker size
        speed_threshold = 120
        axs[n].bar(speed.index, speed[speed.columns[0]], bar_width, alpha=opacity, color = 'b')
        l1 = axs[n].plot(speed.index, speed[speed.columns[0]], 'b.-', lw = lw, ms = ms, label = 'Speed')
        axs2 = axs[n].twinx()
        axs2.bar(odo.index, odo[odo.columns[0]], bar_width, alpha = opacity, color = 'r')
        l2 = axs2.plot(odo.index, odo[odo.columns[0]], 'r.-', lw = lw, ms = ms, label = 'Resolution')
        #axs[n].set_xlim((math.floor(speed.index[speed[speed.columns[0]]>0][0]/10), 105))
        axs[n].set_xlim(95, 100.1)
        axs[n].set_ylim(0, speed_max + 1)
        axs2.grid(b = True, which = 'major', color = 'r', linestyle = '--')
        axs[n].grid(b = True, color = 'b')
        axs2.set_yticks(np.arange(0, max(odo[odo.columns[0]]) + .1, resolution))
        axs[n].set_title('below {}km/h'.format(speed_max),
                         fontsize=10)
        ls = l1 + l2
        labels = [l.get_label() for l in ls]
        axs2.legend(ls, labels, prop={'size':7}, loc='upper left')

        # plot the second figure
        n += 1
        axs[n].bar(speed_all.index, speed_all[speed_all.columns[0]], bar_width, alpha=opacity, color = 'b')
        l1 = axs[n].plot(speed_all.index, speed_all[speed_all.columns[0]], 'b.-', lw = lw, ms = ms, label = 'speed_all')
        axs[n].set_yscale('symlog', linthreshy = speed_threshold, linscaley = 15)
        axs[n].set_yticks(np.arange(0, speed_threshold, speed_max), minor = True)
        l2 = axs[n].plot(axs[n].get_xlim(), [speed_threshold] * 2, 'k-.', label = 'speed_threshold = {}'.format(speed_threshold))
        axs3 = axs[n].twinx()
        axs3.bar(odo_all.index, odo_all[odo_all.columns[0]], bar_width, alpha = opacity, color = 'r')
        l3 = axs3.plot(odo_all.index, odo_all[odo_all.columns[0]], 'r.-', lw = lw, ms = ms, label = 'Resolution')
        ls = l1 + l3 + l2
        labels = [l.get_label() for l in ls]
        axs3.legend(ls, labels, prop={'size':7}, loc='upper left')
        axs[n].set_title('all speed',
                         fontsize=10)
        axs[n].set_xticks(np.arange(axs[n].get_xlim()[0], axs[n].get_xlim()[1], .1), minor = True)
        axs[n].set_xlabel('Percentage')
        axs[n].set_xlim(95, 100.1)
        axs3.set_yscale('symlog', linthreshy = res_threshold, linscaley = 15)
        axs3.set_yticks(np.arange(0, res_threshold, resolution), minor = True)
        axs3.grid(b = True, which = 'minor', color = 'r')
        axs[n].grid(b = True, color = 'b', axis = 'y', which = 'minor')
        axs[n].grid(b = True, color = 'b', axis = 'x', which = 'major')
        for i in range(n + 1):
            axs[i].tick_params(axis='both', which='major', labelsize=7)
        axs2.tick_params(axis='both', which='major', labelsize=7)
        axs3.tick_params(axis='both', which='major', labelsize=7)
        ## TODO: could be also separate class method
        fig.suptitle(title, fontsize=13)
        fig.tight_layout()
        fig.subplots_adjust(top=0.85)


class Filetype(Enum):
    none = 0
    hdf5 = 1
    csv = 2

def extrap1d(interpolator):
    xs = interpolator.x
    ys = interpolator.y

    def pointwise(x):
        if x < xs[0]:
            return ys[0]+(x-xs[0])*(ys[1]-ys[0])/(xs[1]-xs[0])
        elif x > xs[-1]:
            return ys[-1]+(x-xs[-1])*(ys[-1]-ys[-2])/(xs[-1]-xs[-2])
        else:
            return interpolator(x)

    def ufunclike(xs):
        return array(map(pointwise, array(xs)))

    return ufunclike

def exInterpf(vec, interpf):
    exInter = extrap1d(interpf)(vec)
    return exInter

def get_lb(folder, 
           run=None, verbose=True):
    if run:
        fn_lb = os.path.join(folder, '{}.lbe'.format(run))
    else:
        lbes = glob.glob(os.path.join(folder, '*.lbe'))
        if len(lbes) == 0:
            run = re.split('/|\\\\', folder)[-1]
            lbes = glob.glob('{}.lbe'.format(run))
        # assert len(lbes)==1, '# zero or more than one lbe file in directory'
        if len(lbes) == 1:
            fn_lb = lbes[0]
    if len(lbes) == 1:
        lb = LB(fn_lb)
        lb.parse_data()
        if verbose:
            print('## loaded: {}'.format(fn_lb))
    else:
        lb = None
    return lb

def get_default_run(lb):
    ## TODO: add additional check based on folder name or vdo file prefix?
    return os.path.basename(lb.filename)

def get_lb_speed(lb):
    acond = lb.recp_event.Label_Req_ID!=0
    cnts = lb.recp_event.Tacho[acond]
    speed = 1E4/lb.recp_event.Inv_Speed[acond]*3.6
    return cnts, speed

def get_evnt(folder, run=None,
             config=None, verbose=True):
    if config is None:
        config = os.path.join(os.path.dirname(__file__), 'columns.yaml')
    DataColumns.init(config=config)
    d_col_e = DataColumns('event.txt')
    if run == None:
        fn_evnt = '{}/*.evnt.txt'.format(folder)
        fn_evnt = glob.glob(fn_evnt)[0]
    else:
        fn_evnt = '{}/{}.evnt.txt'.format(folder, run)
    event_rec = pd.DataFrame(d_col_e.load(fn_evnt, delimiter='; ', skip_header=1))
    if verbose:
        print('## loaded: {}'.format(fn_evnt))
    return event_rec

def get_dmaSync(evnt, factor=8.0):
    # currently External Counter in Comment only
    def get_lb_entry(rec, index, convf=lambda v: v):
        return [convf(s[index]) for s in rec.Comment.str.split(';')]
    # check if START available, and which counter
    lb_start = get_lb_entry(evnt[evnt.Type=='ODOM_KM'], 3)
    assert (len(lb_start)==1) & (lb_start[0]=='START')
    lb_start_cnt = get_lb_entry(evnt[evnt.Type=='ODOM_KM'], 2, int)[0]
    cond_evnt = (evnt.Type=='ODOM_KM') | (evnt.Type=='SYNC')
    dmaSync = evnt[['Odometer', 'Comment']].loc[cond_evnt]
    dmaSync['ExtCounter'] = get_lb_entry(dmaSync, 2, int)
    # sometimes before STOP command Odometer already set to 0 ...
    bad_odo = ((dmaSync.ExtCounter!=lb_start_cnt) & (dmaSync.Odometer==0))
    dmaSync = fix_verbose(dmaSync, bad_odo, 'bad odo entry in sync event table')
    # currently STOP needs to be faked because not recorded in evnt!
    dmaSync.loc[dmaSync.index[-1]+1] = [dmaSync.Odometer.iloc[-1]+5E4*factor,
                                        'STOP faked' + ' '*(len(dmaSync.Comment.iloc[-1])-10),
                                        dmaSync.ExtCounter.iloc[-1]+5E4]
    return dmaSync

def get_TrackNetCfg(folder,
                    filename='TrackNetCfg.s3db',
                    table='Cams_ZL_Cfg',
                    cols=['stationId', 'triggerDivider'],
                    verbose=True,
                    ):
    fn_s3db = os.path.join(folder, filename)
    with sqlite3.connect(fn_s3db) as conn:
        c = conn.cursor()
        res = c.execute('select {} from {};'.format(','.join(cols),
                                                    table,
                                                    )).fetchall()
    if verbose:
        print('## loaded: {}'.format(fn_s3db))
    return pd.DataFrame(res, columns=cols)

def get_divider(trackNetCfg, cam_id):
    if cam_id.isdigit():
        divider = trackNetCfg.triggerDivider[trackNetCfg.stationId==int(cam_id)]\
                  .iloc[0].astype(float)
    else:
        divider = 8000.
    return divider

def get_extData(folder, run=None):
    """load external data: *.lb*, *evnt.txt, TrackNetCfg.s3db
    """
    lb = get_lb(folder, run)
    trackNetCfg = get_TrackNetCfg(folder)
    if run is None and lb is not None:
        run = get_default_run(lb)
    elif run is None and lb is None:
        run = re.split('/|\\\\', folder)[-1]
    evnt = get_evnt(folder, run)
    return {run: dict(lb=lb, s3db=trackNetCfg, evnt=evnt)}

def get_VDOs(folder, run, cam_ids):
    """load csv or hdf5 file names depending on availability
       returns file names and types as dictionary of cam_id keys
    """
    pattern_hdf5 = 'VdoDscr_{}.000.{}.vdo.h5'
    pattern_csv = 'VdoDscr_{}.000.{}.vdo.csv'
    vdodscrs = {}
    for cam_id in cam_ids:
        available = False
        for filetype, patt in [(Filetype.hdf5, pattern_hdf5), 
                               (Filetype.csv, pattern_csv), # original one at last position
                               ]:
            fn = os.path.join(folder, patt.format(run, cam_id))
            if os.path.exists(fn):
                vdodscrs[cam_id] = fn, filetype
                available = True
                break
        if not available:
            #print('#Warning: {} (and converted versions) not available.'.format(fn))
            vdodscrs[cam_id] = None, Filetype.none
    return vdodscrs
    
 
def process_extData(lb,
                    trackNetCfg,
                    evnt,
                    factor=8.0):
    """process external data: *.lb*, *evnt.txt, TrackNetCfg.s3db
    """
    if lb == None:
        cnts, speed = None, None
    else:
        cnts, speed = get_lb_speed(lb)
    dmaSync = get_dmaSync(evnt, factor)
    dividers = trackNetCfg
    cntInt_interpf = interp1d(dmaSync.ExtCounter, dmaSync.Odometer, bounds_error=False, fill_value=0)
    cntExt_interpf = interp1d(dmaSync.Odometer, dmaSync.ExtCounter, bounds_error=False, fill_value=0)
    return {'lb': (cnts, speed), 
            's3db': (dividers),
            'evnt': (dmaSync, cntExt_interpf, cntInt_interpf),
            }

def mask_regions_high_speed(cnts, speed, dmaSync, odo,
                            vec2=None, speed_max=40):
    """returns odo or another vector 'vec2' (of equal size)
       with regions above max speed set no NaNs
    """


    cond_speed = np.isfinite(speed) & (speed<=speed_max)
    cnts_cond = cnts[cond_speed]
    # only take the ascending speed region
    #cond_speed1 = np.isfinite(speed) & (speed<=speed_max) & np.insert((np.diff(speed) > 0), 0, True)
    #speed_cond1 = speed[cond_speed1]
    #cond_speed2 = (np.insert((np.diff(speed_cond1) > 0), 0, True))
    #speed_cond2 = speed_cond1[cond_speed2]
    #cond_speed3 = (np.insert((np.diff(speed_cond2) > 0),0, True))
    #speed_cond3 = speed_cond2[cond_speed3]
    #cond_speed4 = (np.insert((np.diff(speed_cond3) > 0),0, True))
    #speed_cond4 = speed_cond3[cond_speed4]
    #cond_speed5 = (np.insert((np.diff(speed_cond4) > 0),0, True))
#
    #cnts_cond1 = cnts[cond_speed1]
    #cnts_cond2 = cnts_cond1[cond_speed2]
    #cnts_cond3 = cnts_cond2[cond_speed3]
    #cnts_cond4 = cnts_cond3[cond_speed4]
    #cnts_cond5 = cnts_cond4[cond_speed5]

    ## TODO: intInterpfunc should be defined before
    intInterpfunc = interp1d(dmaSync.ExtCounter, dmaSync.Odometer,
                             bounds_error=False, fill_value = -1)
    #odo_low_speed = intInterpfunc(cnts[cond_speed])
    odo_low_speed = intInterpfunc(cnts_cond)
    odo_low_speed = np.nan_to_num(odo_low_speed)
    # split in clusters of larger gaps, say 8*10E3 (equiv. to 10 m), or equivalent to some cluster statistics
    thres = np.percentile(np.diff(odo_low_speed), 98) + 8E4
    assert ~np.isnan(thres)
    odo_clusters = get_clusters_single1D(odo_low_speed, thres)
    regions = get_regions(odo, odo_clusters, vec2)
    regions.append(odo_clusters)
    return regions

def stats_speed(speed, speed_max=40):
    ps_speed = np.r_[0, 1, 5, 15, 25, 50, 55, 60, 65, 70, 75, 80, 85, 90, 91, 93, 95, 96, \
                     96.5, 97, 97.5, 98, 98.5, 99, 99.1, 99.2, 99.3, 99.4, 99.5, 99.6, 99.7, \
                     99.8, 99.9, 99.92, 99.95, 99.98, 99.99999]
    try:
        res = pd.DataFrame({'<={} km/h'.format(speed_max):
                            ml.prctile(speed[speed<=speed_max], ps_speed).round(3)},
                           index=ps_speed)
    except IndexError:
        res = pd.DataFrame({'<={} km/h'.format(speed_max):
                            ml.prctile(0, ps_speed).round(3)},
                           index=ps_speed)
    return res

def stats_odo(odo, cam='cam', factor=8, divider=6):
    ps = [0.02, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.3, 0.4, 0.5, 50, 55, 60, 65, 70, 75, 80, 85, \
          90, 91, 93, 93.2, 93.3, 93.4, 93.5, 93.7, 94, 95, 96, 96.5, 97, 97.5, 98, 98.5, 98.6, 98.7, \
          98.8, 98.9, 99, 99.1, 99.2, 99.3, 99.4, 99.5, 99.6, 99.7, 99.8, \
          99.9, 99.92, 99.95, 99.98, 99.99999]
    if np.isnan(odo).all():
        res = pd.DataFrame({cam: {p : np.nan for p in ps}})
        return res
    udiffs0 = np.diff(odo)
    # correct misaligned resolution
    udiffs0 = correct_res_misalignment(udiffs0, divider)
    #bins = range(int(max(udiffs0)+2))
    ## missing iteration!
    try:
        #udiffs = pd.DataFrame({cam: np.histogram(udiffs0[~np.isnan(udiffs0)], bins=bins)[0]})
        udiffs = pd.DataFrame({cam: np.bincount(udiffs0[~np.isnan(udiffs0)].astype(int))})
    except ValueError:
        print("invalid values evaluated!")
        udiffs = pd.DataFrame({cam: np.bincount(udiffs0[np.bitwise_and(~np.isnan(udiffs0), udiffs0 > 0)].astype(int))})
    ndiffs = (udiffs/udiffs.sum(0)).cumsum(0)


    get_res = lambda p: (ndiffs.loc[ndiffs[cam]>=p/100.,cam].index[0]/factor).round(3)
    res = pd.DataFrame({cam: {p : get_res(p)
                              for p in ps}})
    return res

def speed_check(cnts, speed, folder, run,
                figs={}, save=False):
    figure = FigSpeed(0, 1, 1)
    figure.update(cnts=cnts, 
                  speed=speed,
                  folder=folder,
                  run=run,
                  )
    figure.plot()
    if save:
        figure.save()
    figs[figure.num] = figure
    return figure

def cam_check(cam_id,
              figs={}, save=False,
              FigClass=FigCam, ## TODO: change default?
              fig_num=None,
              **kwargs):
    if fig_num is None:
        fig_num = cam_id
    if FigClass == FigCam:
        figure = FigClass(fig_num, 2, 1)
    elif FigClass == FigCam2:
        figure = FigClass(fig_num, 2, 1)
    elif FigClass == FigCam3:
        figure = FigClass(fig_num, 2, 1)
    figure.update(**kwargs)
    figure.plot()
    if save:
        figure.save()
    figs[figure.num] = figure
    return figure

def analyseVdo(folder='.',
               run=None,
               factor=8.0,  # TODO: move in some way to options
               speed_max=40, # TODO dto.
               select_range={'subrange_selected' : False}, # TODO dto.
               options=None,
               vdoData=None,
               recps=None, # TODO: remove this, vdoData probably sufficient for interactive usage
               delete_csv=True,
               verbose=True,
               ):
    """Analyse vdo data based on VdoDscr conversion output.

    Keyword arguments:
    folder      -- file folder (default: '.')
    run         -- run name (default: None, then automatically determined)
    ...
    delete_csv  -- toggle deletion of converted csvs (default: True)
    """
    if recps is None: recps = {}
    cam_results = {}
    figs = {}
    # py2exe app cannot be used with pytables
    with_tables = False
    if vdoData is None:
        vdoData = VdoData()
        run = vdoData.load(folder, run)
    else:
        assert run is not None
    lb = vdoData.lb
    stats_under_max_speed = pd.ExcelWriter('{}/{}-stats_under_max_speed.xlsx'.format(folder, run))
    stats_all_speed = pd.ExcelWriter('{}/{}-stats_all_speed.xlsx'.format(folder, run))
    processed = process_extData(lb,
                                vdoData.trackNetCfg, 
                                vdoData.evnt, 
                                factor)
    cnts, speed = processed['lb']
    # set cnts and speed to other values
    #lbedata = pd.read_csv("{}/Prorail15110416si12-lbe.csv".format(run), names=['Count', 'Speed'], \
    #                      skiprows = 1, usecols = (1,2), delimiter=';')
    #lbedata = lbedata.convert_objects(convert_numeric=True)
    #lbedata = lbedata.drop_duplicates(cols = 'Count')
    #cnts, speed = lbedata.Count, lbedata.Speed
    dividers = processed['s3db']
    dmaSync, cntExt_interpf, cntInt_interpf = processed['evnt']

    speed_check(cnts, speed, folder, run,
                figs=figs, save=options.save)
    # speed statistics under max speed needs to be recorded in excel book
    cam_results['speed_region'] = stats_speed(speed, speed_max=speed_max)
    cam_results['speed_all'] = stats_speed(speed, speed_max = float('inf'))
    cam_results['speed_region'].to_excel(stats_under_max_speed, 'speed')
    cam_results['speed_all'].to_excel(stats_all_speed, 'speed')

    vdodscrs = get_VDOs(folder, run, options.use_cams)
    errors = {}
    FrameNumber = {}
    AbExtCounter = {}
    wb = pd.ExcelWriter('{}/jumps.xlsx'.format(folder))
    wbb = pd.ExcelWriter('{}/FrameInfo.xlsx'.format(folder))
    wbbb = pd.ExcelWriter('{}/AbExtCounter.xlsx'.format(folder))

    speed_max_orig = speed_max # save the speed_max for linear cameras
    for cam_id in vdodscrs:
        if cam_id == "c50" or cam_id == "c51": # set manually speed limit for panorama camera
            speed_max = 88
            speed_min = 0.1
        else:
            speed_max = speed_max_orig # set speed limit for linear cameras by the value given
        fn, filetype = vdodscrs[cam_id]
        # prevent load of existing recps in interactive runs!
        if cam_id not in recps:
            if filetype.name == "hdf5":
                try:
                    if with_tables:
                        recp = recps[cam_id] = pd.read_hdf(fn, 'vdo')
                    else:
                        import h5py
                        with h5py.File(fn,'r') as f:
                            recp = pd.DataFrame(f['vdo'][()])
                            recps[cam_id] = recp
                except IOError:
                    print('# IOError for h5 file {}'.format(fn))
                    continue
            elif filetype.name == "csv":
                # current logic is: always auto-convert to hdf5
                try:
                    recp = pd.read_csv(fn,
                               names=['Odometer', 'FrameNum'],
                               skiprows=2, delimiter=',')
                    if recp.empty:
                        continue
                    # Convert csv files to hdf5 files
                    fn_hdf = fn[:-3]+'h5'
                    h5_var = 'vdo'
                    shuffle = True
                    fletcher32 = True
                    complib_table = 'zlib'
                    complib_h5py = 'gzip'
                    complevel = 9
                    if with_tables:
                        recp.to_hdf(fn_hdf, h5_var,
                                    shuffle=shuffle,
                                    fletcher32=fletcher32,
                                    complib=complib_table,
                                    complevel=complevel,
                                    format = 'table')
                    else:
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
                    if delete_csv:
                        os.remove(fn)
                except IOError:
                    print('# IOError for csv file {}'.format(fn))
                    continue
            elif filetype.name == 'none':
                # TODO logging.warn instead of print
                print('#Warning: VdoDscr file for camera {} not found in {}.'.format(cam_id, folder))
                continue
            else:
                raise NotImplementedError
            if verbose:
                print('## loaded: {}'.format(fn))

        # fix bad odo entries
        bad_odo = pd.Series(np.append(np.diff(recp.Odometer.values)<=0, True))
        recp = fix_verbose(recp, bad_odo, 'bad odo entry in index data of {}'.format(cam_id))

        # only saved data needs to be analysed
        sub_recp = select_odometer_range(recp, **select_range)
        # large dataset is broken into several chunks in order to reduce memory usage (out of core processing)
        #hdf_fake = pd.HDFStore('fake.hdf5')
        #hdf_fake.put('vdo', sub_recp, format = 'table')
        vdoData.vdos[cam_id] = sub_recp #recp
        divider = get_divider(dividers, cam_id)

        # inter-/extra-polate odo
        exInterp = exInterpf(vdoData.vdos[cam_id].Odometer, cntExt_interpf)
        speed_cnts_odo = exInterpf(cnts, cntInt_interpf)

        odo, frame, odo_clusters = mask_regions_high_speed(cnts, speed, dmaSync, vdoData.vdos[cam_id].Odometer,
                                                           vec2=vdoData.vdos[cam_id].FrameNum, speed_max=speed_max)

        # get resolutions between two given speed limit (in a speed range)
        #odo1, frame1, odo_clusters1 = mask_regions_high_speed(cnts, speed, dmaSync, vdoData.vdos[cam_id].Odometer,
        #                                                   vec2=vdoData.vdos[cam_id].FrameNum, speed_max=speed_min)
        #odo[np.where(odo == odo1)[0]] = np.nan
        # Analyse 0 resolution frames
        #res_neighbour, _, _ = get_neighbour_0_res(odo, divider)
        #fig_neighbour = FigCam('neighbour', 1, 1)
        #pd.tools.plotting.parallel_coordinates(res_neighbour, 'type')

        vdoProc = pd.DataFrame(np.c_[odo, frame], 
                               columns=['Odometer_regions', 'FrameNum_regions'],
                               )
        
        ## TODO: vdoResults could be also created only once per run,
        ##       then an update method is needed for results to be stored per per cam_id
        vdoResults = VdoResults(cam_id,
                                vdoProc=vdoProc,
                                cnts=cnts,
                                speed=speed,
                                speed_max=speed_max,
                                factor=factor,
                                divider=divider,
                                dmaSync=dmaSync,
                                exInterp=exInterp,
                                cntExt_interpf=cntExt_interpf,
                                cntInt_interpf=cntInt_interpf,
                                speed_cnts_odo = speed_cnts_odo,
                                odo_clusters = odo_clusters,
                                select_range = select_range,
                                )
        cam_results.update(vdoResults.as_dict())

        if options.AbExtCounter:
            if vdoData.vdos[cam_id].Odometer.iloc[-1] < dmaSync.Odometer.iloc[-2]:
                 AbExtCounter[cam_id] =pd.DataFrame(np.c_[cntExt_interpf(vdoData.vdos[cam_id].Odometer.iloc[-1])],columns=['Ext Cnt'])
                 AbExtCounter[cam_id].to_excel(wbbb, cam_id)

        if options.Jumping:
            idx = np.where(np.diff(vdoData.vdos[cam_id].Odometer) > 2 * divider)[0]
            if np.size(idx) > 0:
                errors[cam_id] = pd.DataFrame(np.c_[vdoData.vdos[cam_id].Odometer[idx], cntExt_interpf(vdoData.vdos[cam_id].Odometer[idx]),\
                np.diff(vdoData.vdos[cam_id].Odometer)[idx]],columns=['Odometer', 'Ext Cnt', 'diff val'])
                errors[cam_id].to_excel(wb, cam_id)

        if options.FrameInfo:
            FrameNumber[cam_id] = pd.DataFrame(np.c_[round((lb._data_TCP.Counter.iloc[-1] - dmaSync.ExtCounter.iloc[0]) \
                                          * factor / divider), np.size(vdoData.vdos[cam_id].FrameNum)],columns=['FrameNum(should)', 'FrameNum(recorded)'])
            FrameNumber[cam_id].to_excel(wbb, cam_id)
        
        fig_save = options.save and (cam_id in options.save)
        ## TODO: move functionality of cam_check into FigCam
        _ = cam_check(cam_id, vdoData=vdoData, vdoResults=vdoResults,
                      figs=figs, save=fig_save,
                      FigClass=FigCam, folder = folder)
        # plot newer figures if necessary
        #if len(set(speed)) != 1: # If the run is not a simulation
        _ = cam_check(cam_id, vdoData=vdoData, vdoResults=vdoResults,
                      figs=figs, save=fig_save,
                      FigClass=FigCam2, fig_num='-'.join([cam_id, 'under_speed_max={}'.format(speed_max)]), folder = folder)
        # under max speed needs to be saved in Excel book
        cam_results['odo_under_max_{}'.format(cam_id)] = stats_odo(odo, cam=cam_id, factor=factor, divider=divider)
        cam_results['odo_all_{}'.format(cam_id)] = stats_odo(vdoData.vdos[cam_id].Odometer, cam=cam_id, factor=factor, divider=divider)
        cam_results['odo_under_max_{}'.format(cam_id)].to_excel(stats_under_max_speed, 'cam_{}'.format(cam_id))
        cam_results['odo_all_{}'.format(cam_id)].to_excel(stats_all_speed, 'cam_{}'.format(cam_id))
        _ = cam_check(cam_id, vdoData=vdoData, vdoResults=vdoResults,
                      figs=figs, save=fig_save, cam_results = cam_results,
                      FigClass=FigCam3, fig_num='-'.join([cam_id, 'stats']), folder = folder)

    stats_under_max_speed.save()
    if options.FrameInfo:
        ExttoOdofunc = interp1d(dmaSync.ExtCounter, dmaSync.Odometer)
        Counter = {'Odometer' : pd.Series([dmaSync.Odometer.iloc[0], dmaSync.Odometer.iloc[1],\
                                            dmaSync.Odometer.iloc[-2], ExttoOdofunc(lb._data_TCP.Counter.iloc[-1])], index=['START', 'FIRST SYNC', 'LAST SYNC', 'STOP']),\
                    'ExtCounter' : pd.Series([dmaSync.ExtCounter.iloc[0], dmaSync.ExtCounter.iloc[1],\
                                              dmaSync.ExtCounter.iloc[-2], lb._data_TCP.Counter.iloc[-1]], index=['START', 'FIRST SYNC', 'LAST SYNC', 'STOP'])}
        FrameNumber['Counter'] = pd.DataFrame(Counter, index=['START', 'FIRST SYNC', 'LAST SYNC', 'STOP'], columns=['Odometer', 'ExtCounter'])
        FrameNumber['Counter'].to_excel(wbb, 'Counter')
        wbb.save()
    if options.Jumping:
        wb.save()
    if options.AbExtCounter:
        wbbb.save()
    
    return vdoData, cam_results, figs

def analyseVdo_multiDir(args, speed_max):
    folder_glob = 'Prorail*si12'
    folders = glob.glob(folder_glob)
    for f in folders:
        _ = analyseVdo(folder=f, run=f, options=args, speed_max = speed_max)

def data_filter(input_array, step):
    """
    return min, max and median value vectors in step (odd) length
    range elements of the 1-dimensional input_array
    """
    mod = input_array.shape[0] % step
    rows = input_array.shape[0]//step
    factor = np.arange(rows)
    if mod:
        in_mat = np.reshape(input_array[:-mod], (rows, -1))
        min_array = np.r_[in_mat.min(axis=1), min(input_array[-mod:])]
        max_array = np.r_[in_mat.max(axis=1), max(input_array[-mod:])]
        median = np.median(in_mat, axis = 1)
        median_rest = np.median(input_array[-mod:])
        median_array = np.r_[median, median_rest]

        # get min, max and average value indices
        min_ind = in_mat.argmin(axis=1)
        min_ind += factor * step
        min_ind = np.append(min_ind, input_array[-mod:].argmin() + rows * step)

        max_ind = in_mat.argmax(axis=1)
        max_ind += factor * step
        max_ind = np.append(max_ind, input_array[-mod:].argmax() + rows * step)

        median_trans = np.reshape(median, (rows, -1))
        median_ind = abs(in_mat - median_trans).argmin(axis=1)
        median_ind += factor * step
        median_ind = np.append(median_ind, abs(input_array[-mod:] - median_rest).argmin() + rows * step)

    else:
        in_mat = np.reshape(input_array, (input_array.shape[0]//step, -1))
        min_array = in_mat.min(axis=1)
        max_array = in_mat.max(axis=1)
        median_array = np.median(in_mat, axis = 1)

        # get min, max and average value indices
        min_ind = in_mat.argmin(axis=1)
        min_ind += factor * step

        max_ind = in_mat.argmax(axis=1)
        max_ind += factor * step

        median_trans = np.reshape(median_array, (rows, -1))
        median_ind = abs(in_mat - median_trans).argmin(axis=1)
        median_ind += factor * step

    return min_array, median_array, max_array, min_ind, median_ind, max_ind

def select_odometer_range(recp, subrange_selected =  False, offset_dist = None, select_dist = None):
    if not subrange_selected:
        print ("#Information: run range is not specified - therefore using whole run.")
        return recp
    odo_first = recp.Odometer.iloc[0]
    factor = 8000
    rows = len(recp.index)
    offset_odo_dist = factor * offset_dist
    select_odo_dist = factor * select_dist
    idx_odo_offset = recp.Odometer.sub(offset_odo_dist + odo_first).abs().idxmin()
    idx_odo_select = recp.Odometer.sub(offset_odo_dist + select_odo_dist + odo_first).abs().idxmin()
    if idx_odo_offset > rows - 1 or idx_odo_select > rows - 1 or idx_odo_offset > idx_odo_select:
        print ("specified offset or distance error!")
        return recp
    return pd.concat([recp.Odometer.iloc[idx_odo_offset:idx_odo_select], \
           recp.FrameNum.iloc[idx_odo_offset:idx_odo_select]], axis = 1)

def get_neighbour_0_res(odo, divider):
    udiffs0 = np.diff(odo) # get difference of the odometer counter
    udiffs0 = correct_res_misalignment(udiffs0, divider)
    type = ['wrong', 'right']
    res_0_ind = np.where(udiffs0 == 0)[0]
    res_0_left = udiffs0[res_0_ind - 1]
    res_0_right = udiffs0[res_0_ind + 1]
    bool_left = np.bitwise_or(res_0_left == divider, res_0_left == 2 * divider)
    bool_1res = np.bitwise_and(res_0_left == divider, res_0_right == divider)
    bool_2res = np.bitwise_and(res_0_left == 2 * divider, res_0_right == 2 * divider)
    bool_right = np.bitwise_or(res_0_right == divider, res_0_right == 2 * divider)
    bool_sum = (res_0_left + res_0_right) == 3 * divider
    bool_all = np.bitwise_and(bool_left, np.bitwise_and(bool_right, bool_sum))
    types = [type[i] for i in bool_all]
    res_neighbour = pd.DataFrame(np.c_[res_0_left, res_0_right],
                               columns=['res_0_left', 'res_0_right'],
                               )
    res_neighbour['type'] = pd.Series(types)
    # get odometer counts whose left and right neighbour resolutions are 6
    odo_res_0_lr_1res = odo[res_0_ind[bool_1res]]
    # get odometer counts whose left and right neighbour resolutions are 12
    odo_res_0_lr_2res = odo[res_0_ind[bool_2res]]
    return res_neighbour, odo_res_0_lr_1res, odo_res_0_lr_2res

def correct_res_misalignment(udiffs0, divider):
    '''
    get resolution and correct the misaligned pairs ([0, 2r] / [2r, 0])
    '''
    # find indices whose resolutions are zero
    res_0_ind = np.where(udiffs0 == 0)[0]
    if res_0_ind.size == 0:
        return udiffs0
    # delete indices on the boundary
    if res_0_ind[0] == 0:
        res_0_ind = np.delete(res_0_ind, 0)
    elif res_0_ind[-1] == len(udiffs0) - 1:
        res_0_ind = np.delete(res_0_ind, -1)

    res_0_left = udiffs0[res_0_ind - 1]
    res_0_right = udiffs0[res_0_ind + 1]
    # correct misaligned left
    cond1 = res_0_left == 2 * divider
    udiffs0[res_0_ind[cond1]] = divider
    udiffs0[res_0_ind[cond1] - 1] = divider
    # correct misaligned right
    cond2 = res_0_right == 2 * divider
    cond2 = np.bitwise_and(~cond1, cond2)
    udiffs0[res_0_ind[cond2]] = divider
    udiffs0[res_0_ind[cond2] + 1] = divider
    return udiffs0

def fix_verbose(recp, bad_cond, msg):
    # TODO: use logging module
    if bad_cond.any():
        faulty = recp[bad_cond]
        print('\n\n#WARNING: {}: \n{}\n#\t=> This is removed as dirty FIX for further processing!\n'.format(msg, faulty))
        return recp[~bad_cond]
    else:
        return recp

def get_evnt_offset(dmaSync):

    try:
        offset_evnt = int(re.split('\;', dmaSync.Comment.iloc[0])[-3])
    except ValueError:
        print ("offset is not correctly calculated!")
    return offset_evnt

def save_GPS_coord(run, poi_file, seg_file, cam_id, folder, factor, pano_ante_dist, save_path=None):
        '''
        Calculate GPS coordinates for the imported panorama images -- both antenna and camera
        '''
        # get interpolation between internal counter and external counter
        if save_path == None:
            save_path = os.getcwd()
        evnt = get_evnt(folder)
        dmaSync = get_dmaSync(evnt, factor)
        offset_evnt = get_evnt_offset(dmaSync)
        Odo_Ext_inter = interp1d(dmaSync.Odometer, dmaSync.ExtCounter)
        Odo_Ext_extra = extrap1d(Odo_Ext_inter)

        # read exported csv to get internal counter of the images
        run_int = re.findall(r'\d+', run)[0]
        pano_extcnt_dir = glob.glob('{}/*{}*/'.format(save_path, run_int))[0]
        pano_file =  glob.glob( "{}/*{}*/{}/*{}*IntCntFrNum.csv".format(save_path, run_int, cam_id, run_int))[0]
        try:
            pano_info = pd.read_csv(pano_file, names = ['Odometer:', 'FrameNum:'], skiprows = 2, delimiter=',')
        except IOError:
            print("IOError for reading pano.csv(internal counter of panorama images) file")
            sys.exit()
        pano_ext = Odo_Ext_extra(pano_info['Odometer:']) # external counter of pano images
        IntCnt_sync = pano_info['Odometer:'] / factor + offset_evnt
        to_GDM = False
        if to_GDM: # this is exported as a csv file to import into GDM for GPS calculation (to LabVIEW)
            pano_extcnt_info = pd.DataFrame()
            pano_extcnt_info['IntCnt'] = pano_info['Odometer:']

            pano_extcnt_info['IntCnt_Sync'] = IntCnt_sync.astype('int')
            pano_extcnt_info['ExtCnt'] = pd.Series(pano_ext).astype('int')
            pano_extcnt_info['Frame_No.'] = pano_info['FrameNum:']
            pano_extcnt_file = "{}{}_{}.csv".format(pano_extcnt_dir, run, cam_id)
            pano_extcnt_info.to_csv(pano_extcnt_file, sep = ';', index = False)
        # read poi.csv file to get external counter and GPS coordinates, make a interpolation
        try:
            poi_info = pd.read_csv(poi_file, names=['CNT', 'LAT','LON', 'EAST','NORTH'], usecols = (0,1,2,4,5), skiprows=8,delimiter=';')
        except IOError:
            print("No _poi.csv file in main directory found, which contains external counter and GPS coordinates")
            exit()
        CNT_LAT_inter = interp1d(poi_info.CNT, poi_info.LAT)
        CNT_LON_inter = interp1d(poi_info.CNT, poi_info.LON)
        CNT_LAT_extra = extrap1d(CNT_LAT_inter)
        CNT_LON_extra = extrap1d(CNT_LON_inter)

        # read *_seg.csv file to get train direction and corresponding external counter range
        try:
            seg_info = pd.read_csv(seg_file, names=['PRV5_CNT_BGN', 'PRV5_CNT_END', 'PRV5_ERS-DIR'], usecols = (0,1,14), skiprows=8, delimiter=';')
        except IOError:
            print("No _seg.csv file in main directory found, which contains external counter and train direction")
            exit()
        dir_change = np.diff(seg_info['PRV5_ERS-DIR']) # get train direction change
        dir_change_idx_end = np.where(dir_change != 0)[0] # get index where the train changed its direction
        if not len(dir_change_idx_end): # if no direction change
            run_dire = seg_info['PRV5_ERS-DIR'].unique()
            cnt_bgn = seg_info['PRV5_CNT_BGN'].iloc[0]
            cnt_end = seg_info['PRV5_CNT_END'].iloc[-1]
            dir_cluster = np.c_[cnt_bgn, cnt_end, run_dire]
        else:
            # use 1 and -1 to mark the train direction at certain run range
            dir_bool = -np.append(dir_change[dir_change_idx_end], -dir_change[dir_change_idx_end][-1]) / 2
            dir_change_idx_bgn = dir_change_idx_end + 1
            dir_change_idx_end = np.append(dir_change_idx_end, seg_info.index[-1]) # end of one direction range index
            dir_change_idx_bgn = np.insert(dir_change_idx_bgn,0,[0]) # begin of one direction range index
            cnt_end = seg_info['PRV5_CNT_END'][dir_change_idx_end]
            cnt_bgn = seg_info['PRV5_CNT_BGN'][dir_change_idx_bgn]
            dir_cluster = np.c_[cnt_bgn, cnt_end, dir_bool] # get external counter range and its running direction

        # calculate GPS coordinates with internal counter of the exported images
        # GPS coordinates of the antenna when the images are taken

        ante_LAT = CNT_LAT_extra(pano_ext)
        ante_LON = CNT_LON_extra(pano_ext)
        # get shift distance for the processing camera
        if cam_id == "c50":
            ante_shift_dist = pano_ante_dist[0]
        elif cam_id == "c51":
            ante_shift_dist = -pano_ante_dist[1]
        # shift the external counter to get the panorama camera position
        for i in range(0, len(pano_ext) - 1):
            idx1 = np.where(dir_cluster[:,0] < pano_ext[i])[0]
            #idx2 = np.where(dir_cluster[:,1] > pano_ext[i])
            if len(idx1) == 0:
                pano_ext[i] = np.nan
            else:
                if dir_cluster[:,2][idx1[-1]] < 0:
                    pano_ext[i] -= ante_shift_dist
                    IntCnt_sync[i] -= ante_shift_dist
                else:
                    pano_ext[i] += ante_shift_dist
                    IntCnt_sync[i] -= ante_shift_dist
        # calculate panorama camera coordinates
        pano_info['IntCnt_Sync_Pano'] = IntCnt_sync.astype('int')
        pano_info['EXT_Pano:'] = pd.Series(pano_ext.astype('int'))
        pano_LAT = CNT_LAT_extra(pano_ext)
        pano_LON = CNT_LON_extra(pano_ext)
        pano_info['ANTE_LAT'] = pd.Series(ante_LAT)
        pano_info['ANTE_LON'] = pd.Series(ante_LON)
        pano_info['PANO_LAT'] = pd.Series(pano_LAT)
        pano_info['PANO_LON'] = pd.Series(pano_LON)
        pano_GPS_file = "{}{}/{}_{}_GPS.csv".format(pano_extcnt_dir, cam_id, run, cam_id)
        pano_info.to_csv(pano_GPS_file, sep = ';', index = False)
        return pano_info

def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""
    return answer