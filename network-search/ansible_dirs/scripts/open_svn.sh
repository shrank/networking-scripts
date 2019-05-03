#!/bin/bash
wdir=/data/workdir/
repo_dir=/data/repo


repo=file:///data/repo/
test -e $repo_dir || svnadmin create $repo_dir

if [ ! -e $wdir ]; then
mkdir -p $wdir
svn checkout $repo $wdir
fi
cd $wdir
svn update --non-interactive --accept mine-full
