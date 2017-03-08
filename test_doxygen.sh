#! /bin/sh

set -eu

test -d work && rm -rf work
mkdir work && cd work

CODEGEN='gdbus-codegen'
DOCEXTRACT='../extract_documentation.py'

$CODEGEN --generate-c-code=upnp_dleynaserver_dbus --c-namespace tdbus_dleynaserver --interface-prefix com.intel.dLeynaServer. ../com_intel_dleynaserver.xml
$CODEGEN --generate-c-code=airable_dbus           --c-namespace tdbus              --interface-prefix de.tahifi.              ../de_tahifi_airable.xml
$CODEGEN --generate-c-code=artcache_dbus          --c-namespace tdbus_artcache     --interface-prefix de.tahifi.ArtCache.     ../de_tahifi_artcache.xml
$CODEGEN --generate-c-code=configuration_dbus     --c-namespace tdbus_config       --interface-prefix de.tahifi.Configuration. ../de_tahifi_configuration.xml
$CODEGEN --generate-c-code=credentials_dbus       --c-namespace tdbus_credentials  --interface-prefix de.tahifi.Credentials.  ../de_tahifi_credentials.xml
$CODEGEN --generate-c-code=dcpd_dbus              --c-namespace tdbus_dcpd         --interface-prefix de.tahifi.Dcpd.         ../de_tahifi_dcpd.xml
$CODEGEN --generate-c-code=debug_dbus             --c-namespace tdbus_debug        --interface-prefix de.tahifi.Debug.        ../de_tahifi_debug.xml
$CODEGEN --generate-c-code=dbusdl_dbus            --c-namespace tdbus              --interface-prefix de.tahifi.              ../de_tahifi_filetransfer.xml
$CODEGEN --generate-c-code=lists_dbus             --c-namespace tdbus_lists        --interface-prefix de.tahifi.Lists.        ../de_tahifi_lists.xml
$CODEGEN --generate-c-code=mounta_dbus            --c-namespace tdbus              --interface-prefix de.tahifi.              ../de_tahifi_mounta.xml
$CODEGEN --generate-c-code=audiopath_dbus         --c-namespace tdbus_aupath       --interface-prefix de.tahifi.AudioPath.    ../de_tahifi_audiopath.xml
$CODEGEN --generate-c-code=streamplayer_dbus      --c-namespace tdbus_splay        --interface-prefix de.tahifi.Streamplayer. ../de_tahifi_streamplayer.xml
$CODEGEN --generate-c-code=connman_dbus           --c-namespace tdbus_connman      --interface-prefix net.connman.            ../net_connman.xml
$CODEGEN --generate-c-code=logind_dbus            --c-namespace tdbus_logind       --interface-prefix org.freedesktop.login1. ../org_freedesktop_login1.xml
$CODEGEN --generate-c-code=upnp_media_dbus        --c-namespace tdbus_upnp         --interface-prefix org.gnome.UPnP.         ../org_gnome_upnp.xml

$DOCEXTRACT -i ../com_intel_dleynaserver.xml -o com_intel_dleynaserver.md -H com_intel_dleynaserver.h -c tdbus_dleynaserver -s com.intel.dLeynaServer. -n dLeyna
$DOCEXTRACT -i ../de_tahifi_airable.xml      -o de_tahifi_airable.md      -H de_tahifi_airable.h      -c tdbus              -s de.tahifi.              -n Airable
$DOCEXTRACT -i ../de_tahifi_artcache.xml     -o de_tahifi_artcache.md     -H de_tahifi_artcache.h     -c tdbus_artcache     -s de.tahifi.ArtCache.     -n 'Cover Art Cache'
$DOCEXTRACT -i ../de_tahifi_configuration.xml -o de_tahifi_configuration.md -H de_tahifi_configuration.h -c tdbus_config    -s de.tahifi.Configuration. -n Configuration
$DOCEXTRACT -i ../de_tahifi_credentials.xml  -o de_tahifi_credentials.md  -H de_tahifi_credentials.h  -c tdbus_credentials  -s de.tahifi.Credentials.  -n Credentials
$DOCEXTRACT -i ../de_tahifi_dcpd.xml         -o de_tahifi_dcpd.md         -H de_tahifi_dcpd.h         -c tdbus_dcpd         -s de.tahifi.Dcpd.         -n DCPD
$DOCEXTRACT -i ../de_tahifi_debug.xml        -o de_tahifi_debug.md        -H de_tahifi_debug.h        -c tdbus_debug        -s de.tahifi.Debug.        -n Debug
$DOCEXTRACT -i ../de_tahifi_filetransfer.xml -o de_tahifi_dbusdl.md       -H de_tahifi_dbusdl.h       -c tdbus              -s de.tahifi.              -n DBus-DL
$DOCEXTRACT -i ../de_tahifi_lists.xml        -o de_tahifi_lists.md        -H de_tahifi_lists.h        -c tdbus_lists        -s de.tahifi.Lists.        -n Lists
$DOCEXTRACT -i ../de_tahifi_mounta.xml       -o de_tahifi_mounta.md       -H de_tahifi_mounta.h       -c tdbus              -s de.tahifi.              -n MounTA
$DOCEXTRACT -i ../de_tahifi_audiopath.xml    -o de_tahifi_audiopath.md    -H de_tahifi_audiopath.h    -c tdbus_aupath       -s de.tahifi.AudioPath.    -n 'Audio Paths'
$DOCEXTRACT -i ../de_tahifi_streamplayer.xml -o de_tahifi_streamplayer.md -H de_tahifi_streamplayer.h -c tdbus_splay        -s de.tahifi.Streamplayer. -n Streamplayer
$DOCEXTRACT -i ../net_connman.xml            -o net_connman.md            -H net_connman.h            -c tdbus_connman      -s net.connman.            -n Connman
$DOCEXTRACT -i ../org_freedesktop_login1.xml -o org_freedesktop_logind.md -H org_freedesktop_logind.h -c tdbus_logind       -s org.freedesktop.login1. -n Logind
$DOCEXTRACT -i ../org_gnome_upnp.xml         -o org_gnome_upnp.md         -H org_gnome_upnp.h         -c tdbus_upnp         -s org.gnome.UPnP.         -n UPnP

rm *.c

ln -s ../de_tahifi_lists_errors.h
ln -s ../de_tahifi_lists_errors.hh
ln -s ../de_tahifi_lists_context.h
ln -s ../de_tahifi_lists_item_kinds.h
ln -s ../de_tahifi_lists_item_kinds.hh
ln -s ../Doxyfile.testall Doxyfile

exec doxygen
