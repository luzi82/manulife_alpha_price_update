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

#rm -rf manulife_alpha_price_csv/csv
#mv manulife_alpha_price/output manulife_alpha_price_csv/csv
rm -rf last_csv
cp -R manulife_alpha_price_csv/csv last_csv

if [ ! -d venv ]; then
    python3 -m venv venv
fi
. venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
python3 merge_csv.py
deactivate

pushd manulife_alpha_price_csv
git add --all csv
git commit -m "update ${TIMESTAMP}" || true
git push
popd

rm -rf last_csv
