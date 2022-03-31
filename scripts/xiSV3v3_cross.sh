#!/bin/bash

VERSPEC='fuji'
VER='3'
WT='default_angular_bitwise'
OUTDIR='/global/cfs/cdirs/desi/survey/catalogs/SV3/LSS/fuji/LSScats/3/xi/'


srun -N 1  python xirunpc.py --tracer ELG LRG --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 &
srun -N 1  python xirunpc.py --tracer ELG LRG --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 --bin_type log &
srun -N 1  python xirunpc.py --tracer ELG_HIP LRG --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 &
srun -N 1  python xirunpc.py --tracer ELG_HIP LRG --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 --bin_type log &
srun -N 1  python xirunpc.py --tracer ELG_HIPnotqso LRG --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 &
srun -N 1  python xirunpc.py --tracer ELG_HIPnotqso LRG --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 --bin_type log &
srun -N 1  python xirunpc.py --tracer ELG LRG_main --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 &
srun -N 1  python xirunpc.py --tracer ELG LRG_main --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 --bin_type log &
srun -N 1  python xirunpc.py --tracer ELG_HIP LRG_main --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 &
srun -N 1  python xirunpc.py --tracer ELG_HIP LRG_main --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 --bin_type log &
srun -N 1  python xirunpc.py --tracer ELG_HIPnotqso LRG_main --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 &
srun -N 1  python xirunpc.py --tracer ELG_HIPnotqso LRG_main --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 --bin_type log &
srun -N 1  python xirunpc.py --tracer ELG_HIPnotqso QSO --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 &
srun -N 1  python xirunpc.py --tracer ELG_HIPnotqso QSO --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT --nran 8 --bin_type log &
srun -N 1  python xirunpc.py --tracer QSO LRG --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT  &
srun -N 1  python xirunpc.py --tracer QSO LRG --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT  --bin_type log &
srun -N 1  python xirunpc.py --tracer QSO LRG_main --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT  &
srun -N 1  python xirunpc.py --tracer QSO LRG_main --outdir $OUTDIR --verspec $VERSPEC --version $VER --weight_type $WT  --bin_type log &
wait