#!/usr/bin/env bash
# AUTO-ANIM-2D: flat hero PNG -> parts -> PSD -> Rigby2D AutoRig -> motion set -> sprite sheets + GIF previews.
# Usage: run_pipeline.sh <name> <source.png> <template.json>
set -e
NAME=$1; SRC=$2; TPL=$3
ROOT=/c/AI/AUTO-ANIM-2D; W=$ROOT/work/$NAME; WW=$(cd $ROOT/work && pwd -W)/$NAME
PY="/c/AI/ComfyUI-Local/.venv/Scripts/python.exe"
export PATH="$ROOT/tools/node:$PATH"
RIGBY="node $ROOT/_vendor/rigby2d/bin/rigby.js"
mkdir -p $W/parts $W/export
T() { date +%s.%N; }
t0=$(T)
$PY -s -I $ROOT/tools/auto_cut.py "$SRC" "$TPL" $W/parts >/dev/null;                                   t1=$(T)
$PY -s -I -c "
import json,numpy as np;from PIL import Image
m=json.load(open(r'$WW/parts/parts.json'))
for k in m['order']: open(r'$WW/parts/'+k+'.rgba','wb').write(np.asarray(Image.open(r'$WW/parts/'+k+'.png').convert('RGBA')).tobytes())"
node $ROOT/tools/layers_to_psd.mjs $WW/parts $WW/$NAME.psd >/dev/null;                                   t2=$(T)
$RIGBY autorig $WW/$NAME.psd --out $WW/$NAME.rigby --force -q;                                           t3=$(T)
$RIGBY run $WW/$NAME.rigby --script $(cd $ROOT/tools && pwd -W)/anim_humanoid.py --out $WW/${NAME}_anim.rigby --force -q; t4=$(T)
rm -rf $W/export/*
# game export: TexturePacker/Aseprite JSON hash + PNG sheet (PixiJS/Phaser/plain canvas), max 2048 for iPhone
$RIGBY export $WW/${NAME}_anim.rigby --format spritesheet --sheet json --out $WW/export/${NAME}_loop.json --fps 12 --scale 0.5 --animation idle,walk,run --max-width 2048 -q
$RIGBY export $WW/${NAME}_anim.rigby --format spritesheet --sheet json --out $WW/export/${NAME}_once.json --fps 12 --scale 0.5 --animation attack,skill,hit,death --no-loop --max-width 2048 -q
$RIGBY export $WW/${NAME}_anim.rigby --format spritesheet --sheet frames --out $WW/export/frames --fps 12 --scale 0.5 --animation idle,walk,run -q
$RIGBY export $WW/${NAME}_anim.rigby --format spritesheet --sheet frames --out $WW/export/frames_once --fps 12 --scale 0.5 --animation attack,skill,hit,death --no-loop -q
$RIGBY export $WW/${NAME}_anim.rigby --out $WW/export/skeleton/${NAME}.json -q;                         t5=$(T)
$PY -s -I $ROOT/tools/previews.py $W/export >/dev/null;                                                  t6=$(T)
$PY -s -I -c "
import json
t=[$t0,$t1,$t2,$t3,$t4,$t5,$t6]; n=['cut_parts','layers_to_psd','autorig','motion_script','export_sheets','previews_gif']
d={k:round(t[i+1]-t[i],2) for i,k in enumerate(n)}; d['total']=round(t[-1]-t[0],2); print(json.dumps(d))
open(r'$WW/export/timings.json','w').write(json.dumps(d,indent=1))"
