#!/bin/sh
#
# Returns non-zero error code if hostname doesn't match argument
#
# Expected usage:
#   ./if_i_am.sh a.server.net && some command
#
# Author: Lloyd Adams <lloyd.adams@gmail.com>
#
HOST=`uname -n`
if [ $HOST != $1 ]
then
	exit 1
fi
