#!/bin/bash
NAME='ServerAutoSys'                             
DJANGODIR=/data/django_serverauto/ServerAutoSys
SOCKFILE=/var/run/gunicorn_${NAME}.sock  
USER=root                  
GROUP=root                          
NUM_WORKERS=3                         
DJANGO_SETTINGS_MODULE=settings     
DJANGO_WSGI_MODULE=wsgi  

echo "starting $NAME as `whoami`"

cd $DJANGODIR
#source ../env/bin/activate
. ../env/bin/activate
#mkvirtualenv djangoenv
export  DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec ../env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user=$USER --group=$GROUP \
    --bind=unix:$SOCKFILE
#    --log-level=debug 
