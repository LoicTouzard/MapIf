#!/usr/bin/env bash
# -!- encoding:utf8 -!-
MAPIF_WSGI_INI=./wsgi.ini
MAINTENANCE_ON=./maintenance_on.html
MAINTENANCE_OFF=./maintenance_off.html
MAPIF_PID_FILE=/tmp/mapif.pid

function toggle_maintenance_state {
        if [ -e ${MAINTENANCE_OFF} ]
        then
                echo " - entering maintenance mode - "
                mv ${MAINTENANCE_OFF} ${MAINTENANCE_ON}
        elif [ -e ${MAINTENANCE_ON} ]
        then
                echo " - /!\ leaving maintenance mode /!\ - "
                mv ${MAINTENANCE_ON} ${MAINTENANCE_OFF}
        else
                echo "[!] maintenance_(off|on).html is missing!"
        fi
}

function start {
        echo "starting..."
        if [ -e ${MAPIF_PID_FILE} ]
        then
                echo "mapif is already being served. (${MAPIF_PID_FILE} exists)"
        else
                uwsgi --ini ${MAPIF_WSGI_INI} && echo "done." || echo "failed!"
                toggle_maintenance_state
        fi
}

function stop {
        echo "stopping..."
        if [ -e ${MAPIF_PID_FILE} ]
        then
                uwsgi --stop ${MAPIF_PID_FILE} && echo "done." || echo "failed!"
                toggle_maintenance_state
        else
                echo "mapif is already stopped. (${MAPIF_PID_FILE} does not exist)"
        fi
}

function usage {
        echo "usage: $0 (start|stop)"
}

case $1 in
        start)
        start
        ;;
        stop)
        stop
        ;;
        restart)
        stop
        start
        ;;
        *)
        usage $0
        ;;
esac
