#!/bin/bash


for i in *.root; 
do 
  ch="${i: -6:1}"
  #echo $ch ; 
  if [ "$ch" = "b" ] 
  then
    echo "$i";
  else
    rm $i
  fi
done 

for i in *.root
do
  rename b.r .r $i
done

echo "END"

