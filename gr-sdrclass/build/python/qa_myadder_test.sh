#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/student/ray/gr-sdrclass/python
export PATH=/home/student/ray/gr-sdrclass/build/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/student/ray/gr-sdrclass/build/swig:$PYTHONPATH
/usr/bin/python2 /home/student/ray/gr-sdrclass/python/qa_myadder.py 
