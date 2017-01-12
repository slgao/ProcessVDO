import os, sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy

defaultdir = os.environ.get('LOCAL', r'C:\Users\SGao0001')
boost = os.environ.get('BOOST', os.path.join(defaultdir, 'boost_1_59_0'))
boost_vc = os.environ.get('BOOST_VC', 'msvc-14.0')
opencv = os.environ.get('OPENCV', os.path.join(defaultdir, 'opencv3.1'))
opencv_vers = os.environ.get('OPENCV_VERS', '310')
opencv_vc = os.environ.get('OPENCV_VC', 'vc14')
debug = os.environ.get('DEBUG', False)

this_include = os.path.join(os.path.dirname(sys.argv[0]), 'include')

opencv_includes = [os.path.join(opencv, 'build', *d)
                   for d in [('include',),
                             ('x64', opencv_vc, 'bin'),
                             ('x64', opencv_vc, 'lib'),
                             ]
                   ]

fmts = [opencv_vers, 'd' if debug else '']
opencv_lib_dir = os.path.join(opencv, 'build', 'x64', opencv_vc, 'lib')
opencv_libs = [os.path.join(opencv_lib_dir, f.format(*fmts))
               for f in ['opencv_world{}{}.lib',
                         #'opencv_core{}{}.lib',
                         #'opencv_highgui{}{}.lib',
                         #'opencv_imgproc{}{}.lib',
                         ]
               ]

if debug:
    extra_compile_args = ["-Zi", "/Od",
                          #"-std=c++11",
                          ]
    extra_link_args = ["-debug"]
else:
    extra_compile_args = ["/EHsc",
                          #"-std=c++11",
                          ]
    extra_link_args = []
extra_link_args += opencv_libs

setup(cmdclass={'build_ext': build_ext},
      ext_modules=cythonize(Extension("VideoRead",
                                      sources=["VideoRead.pyx", "VDOPro.cpp"],
                                      language="c++",
                                      extra_compile_args=extra_compile_args,
                                      include_dirs=\
                                      [this_include]
                                      + [numpy.get_include()]\
                                      + [boost]\
                                      + opencv_includes,
                                      library_dirs=[os.path.join(boost, 'lib64-{}'.format(boost_vc))],
                                      extra_link_args=extra_link_args,
                                      )
                            )
      )
