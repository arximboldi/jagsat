#!/bin/bash

ORIG=/home/raskolnikov/dev/pigeoncide/svn/trunk/src
DEST=/home/raskolnikov/dev/jagsat/svn/trunk/src
OLDCOMMENTSIZE=17

NEWCOMMENT="#\n\
#  Copyright (C) 2009 The JAGSAT project team.\n\
#\n\
#  This software is in development and the distribution terms have not\n\
#  been decided yet. Therefore, its distribution outside the JAGSAT\n\
#  project team or the Project Course evalautors in Abo Akademy is\n\
#  completly forbidden without explicit permission of their authors.\n\
#"

FILES="
base/*.py
core/error.py
core/state.py
core/task.py
core/timer.py
test/base_*.py
test/core_state.py
test/core_task.py
"

function cp_make_dir
{
    source=$1
    target=$2

    if [ ! -d `dirname $target` ]
    then
	mkdir -m 755 -p $(dirname $target)
    fi
    cp -rf $source $target
}

for loc_or_file in $FILES
do
    ret=`pwd`
    cd $ORIG
    files=$(ls $loc_or_file)
    cd $ret

    for file in $files
    do
	echo "* Importing file: $file"
	cp_make_dir $ORIG/$file $DEST/$file
	(echo -e $NEWCOMMENT; tail -n +$OLDCOMMENTSIZE $DEST/$file) > tmp-file
	mv -f tmp-file $DEST/$file
    done
done
