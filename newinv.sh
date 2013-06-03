#!/bin/bash

# Sets the winvo invoices directory
INVOICES_DIR="./invoices"

# default configuration file
SKEL_FILE="./example.conf"

[ -f custom_config.sh ] && source custom_config.sh

# create the file that keeps track of next invoice number
[ -d "${INVOICES_DIR}" ] || mkdir -p "${INVOICES_DIR}"
[ -f "${INVOICES_DIR}/n" ] || echo 1 >> "${INVOICES_DIR}/n"

# this app requires at least one argument,
# show usage if it's not provided
if [ $# -lt 1 ]
then
    echo "usage: $0 invoicename"
    exit 1
fi

# try to find the previous configuration file with the same invoice name
previous="$(find "${INVOICES_DIR}" | grep "^\\./20.*/$1.*conf$" | head -1)"

if [ "$previous" ]
then
    SKEL_FILE="$previous"
fi

invname=$1
nf=$(cat "${INVOICES_DIR}/n")

# create this invoice's directory
folder="${INVOICES_DIR}/$(date +%Y%m)/$1.$nf"
mkdir -p "$folder"

# create this invoice's conf file, with the given invoice no
filename="$folder/$1.$nf.conf"
cp "$SKEL_FILE" "$filename"
sed -i "s/number: .*/number: $nf/" "$filename"

# update the next invoice no
(( nf++ ))
echo $nf > "${INVOICES_DIR}/n"
echo "DONE, edit the file ${filename} and type ./winvo.py ${filename} to generate the pdf in place"
