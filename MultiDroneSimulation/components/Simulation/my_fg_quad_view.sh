#!/bin/sh

if [ -z "$1" ]; then
    echo "usage: my_fg_quad_view INSTANCE_NUMBER"
    exit 1
fi
INSTANCE=$1
PORT=$(expr 5503 + 10 \* $INSTANCE)

AUTOTESTDIR=$(dirname $0)/ardupilot$INSTANCE/Tools/autotest

nice fgfs \
    --native-fdm=socket,in,10,,$PORT,udp \
    --fdm=external \
    --aircraft=arducopter \
    --fg-aircraft="$AUTOTESTDIR/aircraft" \
    --airport=ENBR \
    --geometry=650x550 \
    --bpp=32 \
    --disable-anti-alias-hud \
    --disable-hud-3d \
    --disable-horizon-effect \
    --timeofday=noon \
    --disable-sound \
    --disable-fullscreen \
    --disable-random-objects \
    --disable-ai-models \
    --fog-disable \
    --disable-specular-highlight \
    --disable-anti-alias-hud \
    --wind=0@0
