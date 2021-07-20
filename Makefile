GXX = g++

closuresGen:	src/closuresGen.cpp
	cd src; $(GXX) closuresGen.cpp -o ../bin/closuresGen.out

closuresGenV2:	src/closuresGenV2.cpp
	cd src; $(GXX) closuresGenV2.cpp -o ../bin/closuresGenV2.out