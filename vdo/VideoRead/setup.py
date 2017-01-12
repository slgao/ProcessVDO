from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy
import subprocess

setup (
      cmdclass = {'build_ext': build_ext},
	  ext_modules = cythonize(
	      Extension("VideoRead",
		            sources=["VideoRead.pyx", "VDOPro.cpp"],
					language="c++",
					extra_compile_args=["-std=c++11"],
					include_dirs=[numpy.get_include(), 
					"C:/Users/SGao0001/boost_1_59_0", "C:/Users/SGao0001/boost_1_59_0/lib/x64", 
                              "c:/opencv3.0/mybuild_x64/install/include/", "c:/opencv3.0/mybuild_x64/install/x64/vc14/bin/",
                              "c:/opencv3.0/mybuild_x64/install/x64/vc14/lib/"],
					extra_link_args=[          'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_core300.lib',
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_features2d300.lib',
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_flann300.lib',
                                     
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_highgui300.lib',
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_imgproc300.lib',
                                     
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_imgcodecs300.lib',
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_ml300.lib',
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_objdetect300.lib',
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_photo300.lib',
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_stitching300.lib',
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_ts300.lib',
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_video300.lib',
                                     'C:/opencv3.0/mybuild_x64/install/x64/vc14/lib/opencv_videostab300.lib']
					)
      ))