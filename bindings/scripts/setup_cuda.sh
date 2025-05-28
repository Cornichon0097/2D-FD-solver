#!/bin/sh
# Cuda setup script

sed -i 's/src\/solver\.cpp/src\/cuda_solver.cpp/' setup.py

if ! make all
then
        exit 1
fi

nvcc --compiler-options -fPIC -shared -g -O2 -I./include/armanpy/ -I./src/ -I/home/cornichon/Documents/projects/prsa/venv/include -I/usr/include/python3.11 -c src/cuda_helper.cu -o build/temp.linux-x86_64-cpython-311/src/cuda_helper.o

if [ $? -ne 0 ]
then
        exit 1
fi

g++ -shared -Wl,-O1 -Wl,-Bsymbolic-functions -g -fwrapv -O2 build/temp.linux-x86_64-cpython-311/solver_wrap.o build/temp.linux-x86_64-cpython-311/src/cuda_solver.o build/temp.linux-x86_64-cpython-311/src/cuda_helper.o -L/usr/lib/x86_64-linux-gnu -lm -lz -larmadillo -L/usr/local/cuda-12.9/lib64 -lcudart -o build/lib.linux-x86_64-cpython-311/_solver.cpython-311-x86_64-linux-gnu.so

if [ $? -ne 0 ]
then
        exit 1
fi

pip install .

sed -i 's/src\/cuda_solver\.cpp/src\/solver.cpp/' setup.py
