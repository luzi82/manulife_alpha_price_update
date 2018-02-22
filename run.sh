#!/bin/bash

set -e

TIMESTAMP=`date +%Y%m%d-%H%M%S`

if [ ! -d manulife_alpha_price ]; then
    git clone git@github.com:luzi82/manulife_alpha_price.git
fi

if [ ! -d manulife_alpha_price_csv ]; then
    git clone git@github.com:luzi82/manulife_alpha_price_csv.git
fi

pushd manulife_alpha_price
git pull
popd

pushd manulife_alpha_price_csv
git pull
popd

pushd manulife_alpha_price
./run.sh
popd

rm -rf manulife_alpha_price_csv/csv
mv manulife_alpha_price/output manulife_alpha_price_csv/csv

pushd manulife_alpha_price_csv
git add --all csv
git commit -m "update ${TIMESTAMP}" || true
git push
popd
