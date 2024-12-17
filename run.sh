model="gpt-3.5-turbo-instruct"
# model="gpt-4o-mini"

python evaluation/topology.py --model $model --mode medium --prompt kmat
python evaluation/topology.py --model $model --mode medium --prompt none
python evaluation/topology.py --model $model --mode medium --prompt k-shot
python evaluation/topology.py --model $model --mode medium --prompt 0-CoT
python evaluation/topology.py --model $model --mode medium --prompt CoT
python evaluation/topology.py --model $model --mode medium --prompt CoT --SC 1
python evaluation/topology.py --model $model --mode medium --prompt mat
python evaluation/topology.py --model $model --mode medium --prompt rp
python evaluation/topology.py --model $model --mode medium --prompt matm
# wait
# 
# python evaluation/topology.py --model $model --mode easy --prompt kmat &
# python evaluation/topology.py --model $model --mode easy --prompt none &
# python evaluation/topology.py --model $model --mode easy --prompt k-shot &
# python evaluation/topology.py --model $model --mode easy --prompt 0-CoT &
# python evaluation/topology.py --model $model --mode easy --prompt CoT &
# python evaluation/topology.py --model $model --mode easy --prompt CoT --SC 1 &
# python evaluation/topology.py --model $model --mode easy --prompt mat &
# python evaluation/topology.py --model $model --mode easy --prompt rp &
# python evaluation/topology.py --model $model --mode easy --prompt matm &
# wait
# 
# python evaluation/topology.py --model $model --mode easy --prompt kmat &
# python evaluation/topology.py --model $model --mode easy --prompt none &
# python evaluation/topology.py --model $model --mode easy --prompt k-shot &
# python evaluation/topology.py --model $model --mode easy --prompt 0-CoT &
# python evaluation/topology.py --model $model --mode easy --prompt CoT &
# python evaluation/topology.py --model $model --mode easy --prompt CoT --SC 1 &
# python evaluation/topology.py --model $model --mode easy --prompt mat &
# python evaluation/topology.py --model $model --mode easy --prompt rp &
# python evaluation/topology.py --model $model --mode easy --prompt matm &
# wait