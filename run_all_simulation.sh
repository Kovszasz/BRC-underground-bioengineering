#!/bin/bash

#Compound production prediction
#   - underground
#ipython CompoundProductionPrediction.py
#curl --include --request POST --header "Content-Type: application/json" --header "X-Authorization: ML5U5PCQQ68A8ZHN52W4BHXKBWVNVF5TEYHYKLXLWJ5RQXDFWUEE7IJZ3HCPR1QC9G2H36YMY8XWE1973I7W55P9LHI2JX5L9N7C" --header "X-UserId: kovszasz" --data-binary "{\"message\": \"Compound predictions are done for underground model\"}" --url 'https://api.spontit.com/v3/push'
#   - heterologous
ipython CompoundProductionPredictionHet.py

curl --include --request POST --header "Content-Type: application/json" --header "X-Authorization: ML5U5PCQQ68A8ZHN52W4BHXKBWVNVF5TEYHYKLXLWJ5RQXDFWUEE7IJZ3HCPR1QC9G2H36YMY8XWE1973I7W55P9LHI2JX5L9N7C" --header "X-UserId: kovszasz" --data-binary "{\"message\": \"Compound predictions are done for heterologous model\"}" --url 'https://api.spontit.com/v3/push'
#underground MILP
ipython minimal_underground_set_milp.py > underground_milp.log
curl --include --request POST --header "Content-Type: application/json" --header "X-Authorization: ML5U5PCQQ68A8ZHN52W4BHXKBWVNVF5TEYHYKLXLWJ5RQXDFWUEE7IJZ3HCPR1QC9G2H36YMY8XWE1973I7W55P9LHI2JX5L9N7C" --header "X-UserId: kovszasz" --data-binary "{\"message\": \"Underground MILP done\"}" --url 'https://api.spontit.com/v3/push'
#Statistical analysis of random heterologous reaction sets
(ipython heterologous_statistical_analysis.py 20000 20125 1 > minimal_het_stat_1.log)&
(ipython heterologous_statistical_analysis.py 20125 20250 2 > minimal_het_stat_2.log)&
(ipython heterologous_statistical_analysis.py 20250 20325 3 > minimal_het_stat_3.log)&
(ipython heterologous_statistical_analysis.py 20325 20500 4 > minimal_het_stat_4.log)&
(ipython heterologous_statistical_analysis.py 20500 20625 5 > minimal_het_stat_5.log)&
(ipython heterologous_statistical_analysis.py 20625 20750 6 > minimal_het_stat_6.log)&
(ipython heterologous_statistical_analysis.py 20750 20825 7 > minimal_het_stat_7.log)&
(ipython heterologous_statistical_analysis.py 20900 21000 8 > minimal_het_stat_8.log)&

##ipython check.py 1 minimal_heterologous_set_statistical_milp.py "Heterologous statistical analysis is done!"
#Statistical MILP analysis of random heterologous reaction sets
#(ipython minimal_heterologous_set_statistical_milp.py 20000 20125 1 > minimal_het_stat_milp_1.log)&
#(ipython minimal_heterologous_set_statistical_milp.py 20125 20250 2 > minimal_het_stat_milp_2.log)&
#(ipython minimal_heterologous_set_statistical_milp.py 20250 20325 3 > minimal_het_stat_milp_3.log)&
#(ipython minimal_heterologous_set_statistical_milp.py 20325 20500 4 > minimal_het_stat_milp_4.log)&
#(ipython minimal_heterologous_set_statistical_milp.py 20500 20625 5 > minimal_het_stat_milp_5.log)&
#(ipython minimal_heterologous_set_statistical_milp.py 20625 20750 6 > minimal_het_stat_milp_6.log)&
#(ipython minimal_heterologous_set_statistical_milp.py 20750 20875 7 > minimal_het_stat_milp_7.log)&
#(ipython minimal_heterologous_set_statistical_milp.py 20875 21000 8 > minimal_het_stat_milp_8.log)&

#ipython check.py 1 minimal_heterologous_set_statistical_milp.py "Heterologous statistical MILP analysis is done!"
