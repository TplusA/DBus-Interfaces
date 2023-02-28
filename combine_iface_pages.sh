#! /bin/sh

set -eu

usage()
{
    echo "Usage: ${SCRIPTNAME} -toc <TOCFILE> -ifaces <IFACESFILE> <INPUTFILE> [<INPUTFILES>]"
    exit 1
}

SCRIPTNAME="$0"

if test $# -lt 5
then
    usage
fi

TOCFILE=''
IFACESFILE=''

while test $# -gt 0
do
    case "$1"
    in
        -toc)
            TOCFILE="$2"
            shift
            shift
            ;;
        -ifaces)
            IFACESFILE="$2"
            shift
            shift
            ;;
        -*)
            usage
            ;;
        *)
            break
            ;;
    esac
done

if test "x${TOCFILE}" = x || test "x${IFACESFILE}" = x
then
    usage
fi

echo '\page dbus_interfaces D-Bus interface documentation' >"${TOCFILE}"
echo -n '' >"${IFACESFILE}"

for f in "$@"
do
    tail -n +2 "$f" | sed -n '/^\\page /q;p' >>"${TOCFILE}"
    tail +"$(grep -m 2 -n '^\\page ' "$f" | tail -1 | cut -f 1 -d :)" "$f" >>"${IFACESFILE}"
done
