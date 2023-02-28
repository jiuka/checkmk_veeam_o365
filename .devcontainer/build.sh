#!/bin/bash

NAME=$(python3 -c 'print(eval(open("package").read())["name"])')
rm /omd/sites/cmk/var/check_mk/packages/* ||:
ln -s $WORKSPACE/package /omd/sites/cmk/var/check_mk/packages/$NAME

mkp -v pack $NAME

# Set Outputs for GitHub Workflow steps
if [ -n "$GITHUB_WORKSPACE" ]; then
    echo "pkgfile=$(ls *.mkp)" >> $GITHUB_OUTPUT
    echo "pkgname=${NAME}" >> $GITHUB_OUTPUT
    VERSION=$(python3 -c 'print(eval(open("package").read())["version"])')
    echo "pkgversion=${VERSION}" >> $GITHUB_OUTPUT
fi