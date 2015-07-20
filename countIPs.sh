#!/bin/bash

clear
# match the ip address strings
ipraw=`grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' ~/Downloads/access.txt | sort | uniq`
# echo $ipraw
uniqueips=`echo $ipraw | wc -w`
echo $uniqueips unique IP Addresses
echo 

# separate unique IPs
iplist=( $ipraw )
for i in "${iplist[@]}"; do
	echo $i  `grep -c $i ~/Downloads/access.txt`
done

echo 
echo 

# search only for status codes in the lines and not others
counter=0
declare -a allcodes
while read line
do
	codes=`echo $line | grep -o '\b[1-5][0-1][0-9]\b'`
	a=( $codes )
	allcodes[$counter]=${a[0]}
	counter=$counter+1
done <~/Downloads/access.txt
# echo "${allcodes[@]}"

# retain unique values
uniquecode=( $(echo "${allcodes[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' ') )
# echo "${uniquecode[@]}"

for i in "${uniquecode[@]}"; do
	echo $i  $(echo "${allcodes[*]}" | tr ' ' '\n' | grep -c $i)
done
