#!/bin/bash
x="13-20"

if [[ x==*_{-}_* ]];
then
    echo ${x/-/\\-};
else
    echo "False";
fi