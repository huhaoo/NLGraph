# model="gpt-3.5-turbo-instruct"
model="gpt-4o-mini"

python evaluation/topology.py --model $model --mode easy --prompt kmat &
python evaluation/topology.py --model $model --mode easy --prompt none &
python evaluation/topology.py --model $model --mode easy --prompt k-shot &
python evaluation/topology.py --model $model --mode easy --prompt 0-CoT &
python evaluation/topology.py --model $model --mode easy --prompt CoT &
python evaluation/topology.py --model $model --mode easy --prompt CoT --SC 1 &
python evaluation/topology.py --model $model --mode easy --prompt mat &
python evaluation/topology.py --model $model --mode easy --prompt rp &