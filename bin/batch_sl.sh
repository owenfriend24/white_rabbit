#!/bin/env bash
#
# batch sl one at a time

if [[ $# -lt 1 ]]; then
    echo "Usage:  batch_sl corr"
    exit 1
fi

corr=$1

for sub in wr200 wr201 wr202 wr203 wr204 wr205 wr206 wr207 wr208 wr209 wr211 wr212 wr214 wr216  wr219 wr220 wr221 wr222 wr223 wr224 wr225 wr227 wr228 wr229 wr230 wr232 wr234 wr235 wr237 wr238 wr239 wr240 wr241 wr242 wr243 wr245 wr246 wr248 wr250 wr251 wr254 wr255 wr256; do
  #/home1/09123/ofriend/analysis/white_rabbit/bin/batch_betaseries.sh ${sub}
  /home1/09123/ofriend/analysis/white_rabbit/bin/wr_similarity_sl.py ${sub} 14 gm
  /home1/09123/ofriend/analysis/white_rabbit/bin/sl_to_mni.sh ${sub} ${corr} 14 b_gray_func
done





