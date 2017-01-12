rem ## set in environment
rem setenv /debug /x64
rem setenv /release /x64

rem set DEBUG=1
set BOOST=C:\Users\SGao0001\boost_1_59_0
set BOOST_VC=msvc-14.0
set OPENCV=C:\Users\SGao0001\opencv3.1
set OPENCV_VERS=310
set OPENCV_VC=vc14

set MSSDK=1
set DISTUTILS_USE_SDK=1

del /s VideoRead.cpp
rmdir /s /q build

python setup_svn.py build_ext --inplace --compiler=msvc
