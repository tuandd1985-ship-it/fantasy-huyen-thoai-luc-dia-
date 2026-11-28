#!/usr/bin/env bash
# Character LoRA for SDXL (Animagine XL 4.0) with kohya sd-scripts, 8 GB settings.
# Usage: train_lora_kohya.sh <name> <max_train_steps> [resolution]
set -e
NAME=$1; STEPS=$2; RES=${3:-1024}
ROOT=/c/AI/GAME-ART-CORE
PY=$ROOT/.venv-train/Scripts/python.exe
# free the GPU first: ComfyUI keeps models in VRAM
curl -s -X POST 127.0.0.1:8188/free -H "Content-Type: application/json" -d '{"unload_models": true, "free_memory": true}' >/dev/null || true
cd $ROOT/vendor/sd-scripts
$PY -s sdxl_train_network.py \
  --pretrained_model_name_or_path "C:/AI/ComfyUI-Local/ComfyUI/models/checkpoints/animagine-xl-4.0-opt.safetensors" \
  --train_data_dir "C:/AI/GAME-ART-CORE/lora/$NAME/img" --caption_extension ".txt" \
  --output_dir "C:/AI/GAME-ART-CORE/lora/$NAME/out" --output_name "$NAME" --save_model_as safetensors \
  --resolution "$RES,$RES" --enable_bucket --min_bucket_reso 512 --max_bucket_reso 1024 \
  --network_module networks.lora --network_dim 16 --network_alpha 8 --network_train_unet_only \
  --learning_rate 1e-4 --unet_lr 1e-4 --lr_scheduler cosine --lr_warmup_steps 50 \
  --optimizer_type AdamW8bit --train_batch_size 1 --max_train_steps $STEPS --save_every_n_steps 400 \
  --mixed_precision fp16 --save_precision fp16 --no_half_vae \
  --gradient_checkpointing --cache_latents --cache_latents_to_disk --cache_text_encoder_outputs \
  --sdpa --max_data_loader_n_workers 0 --seed 750001 --logging_dir "C:/AI/GAME-ART-CORE/lora/$NAME/logs"
