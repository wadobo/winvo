#!/bin/bash

msgfmt locales/$1/$1.po -o winvo.mo
mkdir -p mo/$1/LC_MESSAGES
mv winvo.mo mo/$1/LC_MESSAGES
