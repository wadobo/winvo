#!/bin/bash

# Sets the winvo invoices directory
INVOICES_DIR="./invoices"

# default client configuration file
SKEL_FILE="./example.conf"

[ -f custom_config.sh ] && source custom_config.sh

# create the file that keeps track of next invoice number
[ -d "${INVOICES_DIR}" ] || mkdir -p "${INVOICES_DIR}"
[ -f "${INVOICES_DIR}/n" ] || echo 1 >> "${INVOICES_DIR}/n"

# this app requires at least one argument,
# show usage if it's not provided
if [ $# -lt 1 ]
then
    echo "usage: $0 [invoicename] [OPTION]"
    printf "Options:\n --pro\t Generate proforma invoice, n not increment."
    exit
fi

# try to find the previous configuration file with the same invoice name
previous="$(find "${INVOICES_DIR}" | grep "^\\./20.*/$1.*conf$" | sort | tail -1)"

if [ $previous ]
then
    SKEL_FILE=$previous
fi

invname=$1
nf=$(cat "${INVOICES_DIR}/n")

fname=$1.$(echo $nf|sed 's/\//./')
echo $fname

# create this invoice's directory
if [ "$2" != "--pro" ]
then
    folder="${INVOICES_DIR}/$(date +%Y%m)/$fname"
    mkdir -p "$folder"
else
    folder="${INVOICES_DIR}/pro.$(date +%Y%m)/$fname"
    mkdir -p "$folder"
fi

# create this invoice's conf file, with the given invoice no
filename="$folder/$fname.conf"

ny=$(echo $nf | cut -d"/" -f1)
nn=$(echo $nf | cut -d"/" -f2)
num=$(echo $nn | sed 's/^0*//g')

cp "$SKEL_FILE" "$filename"
sed -i "s/^number: .*/number: $ny\/$nn/" $filename

# update the next invoice no
if [ "$2" != "--pro" ]
then
    (( num++ ))
    printf "%s/%03d\n" $ny $num > "${INVOICES_DIR}/n"
fi
echo "DONE, edit the file ${filename} and type ./winvo.py ${filename} to generate the pdf in place"
