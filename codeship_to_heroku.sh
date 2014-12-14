#!/bin/bash -e

function usage {
    echo "Usage: $0 <staging|production>"
    echo
    echo 'You must have the heroku utility installed and have push access on'
    echo 'Heroku.'
    echo
    echo 'HINT: Only Jenkins is allowed to deploy...'
}

THIS_SCRIPT=$(readlink -f $0)
THIS_DIR=$(dirname ${THIS_SCRIPT})

ENVIRONMENT=$1

STAGING_APP='sea-level-api-staging'
PRODUCTION_APP='sea-level-api'


function check_command_line {

    if [ "${ENVIRONMENT}" = "" ] ; then
        usage
        exit 1
    fi
}

function enable_shell_echo {
    set -x
}

function get_heroku_app_name {
    case "${ENVIRONMENT}" in
        'staging' )
            HEROKU_APP=${STAGING_APP} ;;
        'production' )
            HEROKU_APP=${PRODUCTION_APP} ;;
    esac

    if [ "${HEROKU_APP}" = "" ]; then
        echo 'You must specify one of staging/production'
        exit 1
    fi
}

function enable_maintenance_mode {
    heroku maintenance:on --app ${HEROKU_APP}
}

function disable_maintenance_mode {
    heroku maintenance:off --app ${HEROKU_APP}
}

function deploy_code_to_heroku {
    if [ "" != "$(git remote |grep -e '^heroku$')" ]; then
        git remote rm heroku
    fi

    git remote add heroku git@heroku.com:${HEROKU_APP}.git
    git push -f heroku HEAD:master
}

function copy_production_database_to_staging {
    backup_production_database
    nuke_staging_database

    BACKUP_URL="$(heroku pgbackups:url --app ${PRODUCTION_APP})"
    heroku pgbackups:restore DATABASE_URL ${BACKUP_URL} --confirm ${STAGING_APP} --app ${STAGING_APP}
}

function backup_production_database {
    heroku pgbackups:capture --expire --app ${PRODUCTION_APP}
}

function nuke_staging_database {
    heroku pg:reset DATABASE_URL --confirm ${STAGING_APP} --app ${STAGING_APP}
}

function run_database_migrations {
    heroku run python manage.py migrate --noinput --app ${HEROKU_APP}
}

function start_a_web_worker {
    if [ "" = "$(heroku ps --app ${HEROKU_APP} |grep -e '=== web ([0-9]\+X): `gunicorn api.wsgi`')" ]; then
        heroku ps:scale web=1 --app ${HEROKU_APP}
    fi
}

function disable_emergency_debug {
    heroku config:unset EMERGENCY_DEBUG --app ${HEROKU_APP}
}

check_command_line
enable_shell_echo
get_heroku_app_name

case "${ENVIRONMENT}" in
    'staging' )
        copy_production_database_to_staging ;;
    'production' )
        backup_production_database ;;
esac

enable_maintenance_mode
deploy_code_to_heroku
run_database_migrations
disable_emergency_debug
start_a_web_worker
disable_maintenance_mode