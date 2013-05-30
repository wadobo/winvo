#!/bin/bash

xgettext winvo.py
mkdir -p locales/$1/
mv messages.po locales/$1
msginit --locale=$1 --input=locales/$1/messages.po
mv $1.po locales/$1
