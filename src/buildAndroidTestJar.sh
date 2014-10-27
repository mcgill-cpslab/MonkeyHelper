#!/bin/bash
if [ $# -ne 0 ];then
    target=$1
else
    read -p "please input the path for storing the jar file, press enter to use the current path." target
fi
if [ -z $target ];then
    target=`pwd`
fi
curDir=`pwd`
cd AndroidTest
ant build
cp bin/AndroidTest.jar $target
cd $curDir
