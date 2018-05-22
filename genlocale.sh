#!/bin/bash

xgettext winvo.py

for LANG in 'en' 'es'; do
    mkdir -p locales/$LANG/

    if [ ! -f locales/$LANG/$LANG.po ]; then
        mv messages.po locales/$LANG
        msginit --locale=$LANG --input=locales/$LANG/messages.po
        mv $LANG.po locales/$LANG
    else
        msgmerge -N locales/$LANG/$LANG.po messages.po > new.po
        mv new.po locales/$LANG/$LANG.po
    fi
done
echo -e "When the locales are translated, we must run \033[1m./translate \033[0m"
