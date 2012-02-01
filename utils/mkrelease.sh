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
mkdir ${dir}/pypi

# all
git archive ${version} --prefix=drest-${version}/ | gzip > ${dir}/downloads/drest-${version}.tar.gz
cp -a ${dir}/downloads/drest-${version}.tar.gz $tmpdir/

# individual
for i in drest; do
    pushd src/$i
    git archive ${version} --prefix=${i}-${version}/ | gzip > ${dir}/pypi/${i}-${version}.tar.gz
    popd
done

pushd $tmpdir
    tar -zxvf drest-${version}.tar.gz
    pushd drest-${version}/
        sphinx-build doc/source ${dir}/doc
    popd
popd

