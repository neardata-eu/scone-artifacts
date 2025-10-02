#!/bin/bash

set -x

cd /python/arrow

#python3 -m venv pyarrow-dev
#source ./pyarrow-dev/bin/activate; 
pip install -r arrow/python/requirements-build.txt; 
pip install --upgrade pip

mkdir dist; 
#export ARROW_HOME=$(pwd)/dist
#export LD_LIBRARY_PATH=$(pwd)/dist/lib:$LD_LIBRARY_PATH
export ARROW_HOME=/usr
export LD_LIBRARY_PATH=/usr/lib:$LD_LIBRARY_PATH
export CMAKE_PREFIX_PATH=$ARROW_HOME:$CMAKE_PREFIX_PATH

# TODO change to -DCMAKE_BUILD_TYPE=Release
mkdir arrow/cpp/build; 
pushd arrow/cpp/build
cmake -DCMAKE_INSTALL_PREFIX=$ARROW_HOME \
      -DCMAKE_INSTALL_LIBDIR=lib \
      -DCMAKE_BUILD_TYPE=Debug \
      -DARROW_BUILD_TESTS=ON \
      -DARROW_COMPUTE=ON \
      -DARROW_CSV=ON \
      -DARROW_DATASET=ON \
      -DARROW_FILESYSTEM=ON \
      -DARROW_HDFS=ON \
      -DARROW_JSON=ON \
      -DARROW_PARQUET=ON \
      -DARROW_WITH_BROTLI=ON \
      -DARROW_WITH_BZ2=ON \
      -DARROW_WITH_LZ4=ON \
      -DARROW_WITH_SNAPPY=ON \
      -DARROW_WITH_ZLIB=ON \
      -DARROW_WITH_ZSTD=ON \
      -DCMAKE_INSTALL_LIBDIR=lib \
      -DPARQUET_REQUIRE_ENCRYPTION=ON \
      ..; 
make -j4; 
make install; 
popd

pushd arrow/python
export PYARROW_WITH_PARQUET=1; 
export PYARROW_WITH_DATASET=1; 
export PYARROW_PARALLEL=4; 
#python3 setup.py build_ext --inplace
#
python3 setup.py build_ext
pip install -e . --no-build-isolation

exit 0
