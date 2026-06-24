mkdir /home/kely0001/ja84/Resolution/install
cd /home/kely0001/ja84/Resolution/ncorr_2D_cpp/build
mkdir build
################
 module load opencv
 module load suitesparse/7.7.0-cpu
################
 cmake -DCMAKE_INSTALL_PREFIX=/home/kely0001/ja84/Resolution/install ..

#simon change to codew
Modified imshow function proforma to remvoe default value
in many files

Added "suitesparse" to path to include of  SuiteSparseQR.hpp

#
make
 
 [kely0001@m3-login2 build]$ make install
[100%] Built target ncorr
Install the project...
-- Install configuration: ""
-- Installing: /home/kely0001/ja84/Resolution/install/lib/libncorr.a
-- Installing: /home/kely0001/ja84/Resolution/install/include/ncorr.h
-- Installing: /home/kely0001/ja84/Resolution/install/include/Strain2D.h
-- Installing: /home/kely0001/ja84/Resolution/install/include/Disp2D.h
-- Installing: /home/kely0001/ja84/Resolution/install/include/Data2D.h
-- Installing: /home/kely0001/ja84/Resolution/install/include/ROI2D.h
-- Installing: /home/kely0001/ja84/Resolution/install/include/Image2D.h
-- Installing: /home/kely0001/ja84/Resolution/install/include/Array2D.h
