from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector cimport vector

cimport cython
from libc.stdlib cimport malloc, free

cimport numpy as np
import numpy as np
np.import_array()
import cv2
#import ipdb
import os, sys
import math

try: # requires python 3.4
    from enum import IntEnum
except ImportError:
    from enum34 import IntEnum

## provide function to create Break in Windows (then choose Visual Studio as debugger)
#~ cdef extern from "<Windows.h>":
   #~ void DebugBreak()

# Utility function to convert from numpy array to vector
cdef vector[double] arrayToVector(np.ndarray[np.double_t, ndim=1] array):
    cdef long size = array.size
    cdef vector[double] vec
    cdef long i
    for i in range(size):
        vec.push_back(array[i])
    return vec

cdef extern from "opencv2/core/core.hpp":
 cdef int  CV_WINDOW_AUTOSIZE
 cdef int CV_8UC3

cdef extern from "opencv2/core/core.hpp" namespace "cv":
  cdef cppclass Mat:
    Mat() except +
    void create(int, int, int)
    void* data

cdef extern from "VDOPro.h":
    cdef struct infelHd_ss:
        unsigned int infid
        int totlen
    ctypedef infelHd_ss infelHd_s

    cdef struct Stamp_ss:
        int Clock
        int Odom
    ctypedef Stamp_ss Stamp_s

    cdef struct Video_d_ss:
        int sid
        Stamp_s St
        unsigned int frameCnt
        unsigned int exposition
        unsigned int image_type
        unsigned int position
        unsigned int width
        unsigned int w_step
        unsigned int w_offset
        unsigned int height
        unsigned int h_step
        unsigned int h_offset
    ctypedef Video_d_ss Video_d_s

    cdef int OutputExtCnt_FNumfromVDO(string)
    cdef int GetMetadataFromIntCnt(string, string, vector[Video_d_s] *, vector[infelHd_s] *, vector[vector[char]] *, int, bool, bool, double)
    cdef int GetNumFrameFromIntCnt(string, string);

def WriteCSV(VDOFiles):
    """ Output CSV files to analyse the camera performance"""
    result = OutputExtCnt_FNumfromVDO(VDOFiles)
    return result

def VdoRead(directory, saverange, int OutputOption, save_pano_img, Uncertainty):
    """ Read in VDO files to get the metadata and video data"""
    cdef vector[Video_d_s] RangeVData
    cdef vector[infelHd_s] RangeHData
    cdef vector[vector[char]] VideoData
    cdef bool save_csv_info = True
    result = GetMetadataFromIntCnt(directory, saverange, &RangeVData, &RangeHData, &VideoData, OutputOption, save_pano_img, save_csv_info, Uncertainty)
    return [RangeHData, RangeVData, VideoData]

def get_num_frame(directory, saverange):
    num_frame = GetNumFrameFromIntCnt(directory, saverange)
    return num_frame    
    
def CamIm(Data, CamInfo, len_frame=10000):
    """ Save camera images """
    cdef unsigned int i, j
    cdef int LiNum = len(Data[2])
    cdef int width = Data[1][0].get('width')
    cdef int IndiLiNum, IndiLiNumConst, ImNum, Modulus
    directory = '{}/{}'.format(CamInfo.Folder, CamInfo.CamID)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Output linear camera images
    if CamInfo.ImType in ('BWLinear', 'CLinear'):
        PixDim = 1 if CamInfo.ImType == 'BWLinear' else 3
        # If the rail Image is larger than 10m, split it
        # Calculate how many lines for 10 meter long rail
        IndiLiNum = int(math.floor(len_frame / (0.125 * CamInfo.divider)))
        # Get IndiLiNum for later use while IndiLiNum will change later
        IndiLiNumConst = IndiLiNum
        # Calculate how many images the range of the rail can be split
        # and how many lines for the last image
        ImNum = LiNum / IndiLiNum
        Modulus = LiNum % IndiLiNum
        print 'ImNum is{}. Modulus is{}'.format(ImNum, Modulus)
        ImList = []
        for i in xrange(ImNum + 1):
            # Assign IndiLiNum to Modulus for the last splitted image
            if ((ImNum > 0) and (i == ImNum)) or (ImNum == 0):
                IndiLiNum = Modulus
            # Append lines to list in order to construct an image
            if IndiLiNum > 0:
                for j in xrange(IndiLiNum):
                    ImList.append(Data[2][j + i * IndiLiNumConst])
                # Calculate the distance for the current rail image
                dist = IndiLiNum * CamInfo.divider * 0.125 / 1000
                Image = np.vstack(ImList)
                del ImList[:]
                Image = np.reshape(Image, (IndiLiNum, width, PixDim))
                cv2.imwrite('{}/{}_ExtCnt[{},{}]_{}Meter.jpg'.format(directory, i, CamInfo.ExtCounterRange[1], CamInfo.ExtCounterRange[2], dist), Image)

    # Output JPEG images
    elif CamInfo.ImType in ('JPEG'):
        for i in xrange(LiNum):
            with open('{}/{}.jpg'.format(directory, i), "wb") as f:
                f.write(bytearray(Data[2][i][0:2]))
                f.write(bytearray(Data[2][i][6:]))
                f.close()
    return

# Define load function to get rail image data
if sys.version_info.major==2:
    bytes = lambda s, e: str(s)

class imgType(IntEnum):
    raw = 0
    rgb = 1
    yuv = 2

def load(path, cam, begin=0, end=None, itype=imgType.rgb):
    """ Get rail image from internal counter 'begin' to internal counter 'end' """
    if end is None:
        end = begin + 30000
    data = VdoRead(3, 
                   [b'', 
                   bytes('{}/*.{}.vdo'.format(path,cam), 'ascii'),
                   bytes('{}[{},{}]'.format(cam,begin,end), 'ascii')], 
                   itype)

    if itype==imgType.raw:
        img = np.array(data[2])
    else:
        img = np.array(data[2], dtype=np.uint8)
        img = img.reshape(img.shape[0], -1, 3)
    return img
