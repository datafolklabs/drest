#!/bin/bash

if [ -z $1 ]; then
    echo 'a version argument is required.'
    exit 1
fi


#status=$(git status --porcelain)
#version=$(cat src/drest/setup.py | grep VERSION | head -n1 | awk -F \' {' print $2 '})
version=$1

res=$(git tag | grep $version)
if [ $? != 0 ]; then
    echo "Git tag ${version} does not exist."
    exit
fi

short=$(echo $version | awk -F . {' print $1"."$2 '})
dir=~/drest-${version}
tmpdir=$(mktemp -d -t drest-$version)

#if [ "${status}" != "" ]; then
#    echo
#    echo "WARNING: not all changes committed"
#fi

mkdir ${dir}
mkdir ${dir}/doc
mkdir ${dir}/sources

# all
git archive ${version} --prefix=drest-${version}/ | gzip > ${dir}/sources/drest-${version}.tar.gz
cp -a ${dir}/sources/drest-${version}.tar.gz $tmpdir/

pushd $tmpdir
    tar -zxvf drest-${version}.tar.gz
    pushd drest-${version}/
        sphinx-build doc/source ${dir}/doc
    popd
popd

