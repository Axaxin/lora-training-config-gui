$pretrained_model = "D:/stablediffusion/stable-diffusion-webui/models/Stable-diffusion/Basil_mix_fixed.safetensors"
$train_data_dir = "D:/temp_share/train"
$reg_data_dir = "" 

$resolution = "512,768" 
$batch_size = 1 
$max_train_epoches = 16 
$save_every_n_epochs = 2 

$network_dim = 32
$network_alpha = 32 

$train_unet_only = 0 
$train_text_encoder_only = 0 

$noise_offset = 0 
$keep_tokens = 0 


$lr = "1e-4"
$unet_lr = "1e-4"
$text_encoder_lr = "1e-5"
$lr_scheduler = "cosine_with_restarts"
$lr_warmup_steps = 0 
$lr_restart_cycles = 1 


$output_name = "aki11" 
$save_model_as = "safetensors"
$output_dir = "./output" 

$network_weights = "" 
$min_bucket_reso = 256 
$max_bucket_reso = 1024 
$persistent_data_loader_workers = 0 
$clip_skip = 2


$use_8bit_adam = 1 
$use_lion = 0 


$enable_locon_train = 0 
$conv_dim = 4 
$conv_alpha = 4 

.\venv\Scripts\activate

$Env:HF_HOME = "huggingface"
$network_module = "networks.lora"
$ext_args = [System.Collections.ArrayList]::new()

if ($train_unet_only) {
  [void]$ext_args.Add("--network_train_unet_only")
}

if ($train_text_encoder_only) {
  [void]$ext_args.Add("--network_train_text_encoder_only")
}

if ($network_weights) {
  [void]$ext_args.Add("--network_weights=" + $network_weights)
}

if ($reg_data_dir) {
  [void]$ext_args.Add("--reg_data_dir=" + $reg_data_dir)
}

if ($use_8bit_adam) {
  [void]$ext_args.Add("--use_8bit_adam")
}

if ($use_lion) {
  [void]$ext_args.Add("--use_lion_optimizer")
}

if ($persistent_data_loader_workers) {
  [void]$ext_args.Add("--persistent_data_loader_workers")
}

if ($enable_locon_train) {
  $network_module = "locon.locon_kohya"
  [void]$ext_args.Add("--network_args")
  [void]$ext_args.Add("conv_dim=$conv_dim")
  [void]$ext_args.Add("conv_alpha=$conv_alpha")
}

if ($noise_offset) {
  [void]$ext_args.Add("--noise_offset=$noise_offset")
}

accelerate launch --num_cpu_threads_per_process=8 "./sd-scripts/train_network.py" `
  --enable_bucket `
  --pretrained_model_name_or_path=$pretrained_model `
  --train_data_dir=$train_data_dir `
  --output_dir=$output_dir `
  --logging_dir="./logs" `
  --resolution=$resolution `
  --network_module=$network_module `
  --max_train_epochs=$max_train_epoches `
  --learning_rate=$lr `
  --unet_lr=$unet_lr `
  --text_encoder_lr=$text_encoder_lr `
  --lr_scheduler=$lr_scheduler `
  --lr_warmup_steps=$lr_warmup_steps `
  --lr_scheduler_num_cycles=$lr_restart_cycles `
  --network_dim=$network_dim `
  --network_alpha=$network_alpha `
  --output_name=$output_name `
  --train_batch_size=$batch_size `
  --save_every_n_epochs=$save_every_n_epochs `
  --mixed_precision="fp16" `
  --save_precision="fp16" `
  --seed="1337" `
  --cache_latents `
  --clip_skip=$clip_skip `
  --prior_loss_weight=1 `
  --max_token_length=225 `
  --caption_extension=".txt" `
  --save_model_as=$save_model_as `
  --min_bucket_reso=$min_bucket_reso `
  --max_bucket_reso=$max_bucket_reso `
  --keep_tokens=$keep_tokens `
  --xformers --shuffle_caption $ext_args
Write-Output "Train finished"
Read-Host | Out-Null ;