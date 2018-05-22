#!/bin/bash

for LANG in 'en' 'es'; do
    msgfmt locales/$LANG/$LANG.po -o winvo.mo
    mkdir -p mo/$LANG/LC_MESSAGES
    mv winvo.mo mo/$LANG/LC_MESSAGES
done
