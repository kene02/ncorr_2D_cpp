
module load suitesparse/7.7.0-cpu   
module load opencv/4.10.0  
# i had to go to src directory and make soft pointers
# to all the include files. I could not work out a way to add it to cmake file.
//include_directories(/home/kely0001/ja84/Resolution/install/include)
//target_include_directories(all PUBLIC /home/kely0001/ja84/Resolution/install/include)
#both failed into Cm CMakeLists.txt
g++ ncorr_test.cpp  ${CXXFLAGS} -L/home/kely0001/ja84/Resolution/install/lib -L. -lncorr -lfftw3 ${LDFLAGS} `pkg-config --cflags --libs opencv4`  -lopenblas -L/apps/suitesparse/7.7.0-cpu/lib64 -lsuitesparseconfig -lspqr  -lcamd   -lcholmod -lamd


Includ strings in above paths



cd /home/kely0001/ja84/Resolution/ncorr_2D_cpp/test/src

cmake -DGFORTRAN_LIBRARY=/usr/lib64/gfortran/ -DCMAKE_INSTALL_PREFIX=/home/kely0001/ja84/Resolution/ncorr_2D_cpp/test/build -DSUITESPARSE_LIBRARY1=/apps/suitesparse/7.7.0-cpu/lib64 .

To give is a proper name go
-o ncorr_2D_cpp.exe

