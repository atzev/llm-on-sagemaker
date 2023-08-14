#!/bin/bash

export USERS=20
export RUN_TIME=15m
export LOCUST_UI=false # Use Locust UI
export WORKERS=2
export ENDPOINT_NAME=https://{YOUR_ENDPOINT_NAME}

#replace with the locust script that you are testing, this is the locust_script that will be used to make the InvokeEndpoint API calls. 
export SCRIPT=locust_script.py

    locust -f $SCRIPT -H $ENDPOINT_NAME --master --expect-workers $WORKERS -u $USERS -t $RUN_TIME --csv results --headless &

for (( c=1; c<=$WORKERS; c++ ))
do 
    locust -f $SCRIPT -H $ENDPOINT_NAME --worker --master-host=localhost &
done
