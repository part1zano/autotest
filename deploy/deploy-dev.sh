#!/usr/bin/env bash

cd ~/deploy/rek
git checkout develop
git fetch
git merge origin/develop
git checkout master
git merge develop
git tag 'Automatic deploy'
cd client_side
ant production || exit 1
cd ~/deploy
./deploy.sh
cd ~/deploy_build/rekvizitka_prod/
git add --all
git commit -m
git push origin master
cd /web/production/rekvizitka_prod
sudo git pull
sudo supervisorctl restart all
sudo service nginx restart
sudo service memcached restart
