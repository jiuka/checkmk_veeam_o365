#!/bin/bash
set -e

NAME=$(python3 -c 'print(eval(open("package").read())["name"])')
VERSION=$(python3 -c 'print(eval(open("package").read())["version"])')
rm /omd/sites/cmk/var/check_mk/packages/${NAME} \
   /omd/sites/cmk/var/check_mk/packages_local/${NAME}-*.mkp ||:

mkp -v package package

rm $NAME-$VERSION.mkp
cp /omd/sites/cmk/var/check_mk/packages_local/$NAME-$VERSION.mkp .

mkp inspect $NAME-$VERSION.mkp
