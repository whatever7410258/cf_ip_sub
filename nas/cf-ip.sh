#!/bin/bash
cd cf_ip_sub/nas/
python main.py
cd ../
git add vlworker.yaml
git commit -m 'update yaml'
git push