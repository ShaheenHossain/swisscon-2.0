#!/bin/sh

set -e

SWISS_CONFIGURATION_DIR=/etc/swiss
SWISS_CONFIGURATION_FILE=$SWISS_CONFIGURATION_DIR/swiss.conf
SWISS_DATA_DIR=/var/lib/swiss
SWISS_GROUP="swiss"
SWISS_LOG_DIR=/var/log/swiss
SWISS_LOG_FILE=$SWISS_LOG_DIR/swiss-server.log
SWISS_USER="swiss"

if ! getent passwd | grep -q "^swiss:"; then
    groupadd $SWISS_GROUP
    adduser --system --no-create-home $SWISS_USER -g $SWISS_GROUP
fi
# Register "$SWISS_USER" as a postgres user with "Create DB" role attribute
su - postgres -c "createuser -d -R -S $SWISS_USER" 2> /dev/null || true
# Configuration file
mkdir -p $SWISS_CONFIGURATION_DIR
# can't copy debian config-file as addons_path is not the same
if [ ! -f $SWISS_CONFIGURATION_FILE ]
then
    echo "[options]
; This is the password that allows database operations:
; admin_passwd = admin
db_host = False
db_port = False
db_user = $SWISS_USER
db_password = False
addons_path = /usr/lib/python3.7/site-packages/swiss/addons
" > $SWISS_CONFIGURATION_FILE
    chown $SWISS_USER:$SWISS_GROUP $SWISS_CONFIGURATION_FILE
    chmod 0640 $SWISS_CONFIGURATION_FILE
fi
# Log
mkdir -p $SWISS_LOG_DIR
chown $SWISS_USER:$SWISS_GROUP $SWISS_LOG_DIR
chmod 0750 $SWISS_LOG_DIR
# Data dir
mkdir -p $SWISS_DATA_DIR
chown $SWISS_USER:$SWISS_GROUP $SWISS_DATA_DIR

INIT_FILE=/lib/systemd/system/swiss.service
touch $INIT_FILE
chmod 0700 $INIT_FILE
cat << EOF > $INIT_FILE
[Unit]
Description=SwissCRM Open Source ERP and CRM
After=network.target

[Service]
Type=simple
User=swiss
Group=swiss
ExecStart=/usr/bin/swiss --config $SWISS_CONFIGURATION_FILE --logfile $SWISS_LOG_FILE
KillMode=mixed

[Install]
WantedBy=multi-user.target
EOF
