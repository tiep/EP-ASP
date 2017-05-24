#!/bin/bash

for i in 30 50 70 90 100 150
do
    clingo solver.py bt_conf.lp -c np=${i} -c len=1 -c length=${i} -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c pre=0 -c max=0 -q2 --outf=3 > bombProblems/bt_${i}.txt
    clingo solver.py bt_conf.lp -c np=${i} -c len=1 -c length=${i} -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c pre=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_bt_${i}.txt
    echo "Done bt ${i}"
done



clingo solver.py btc_conf.lp -c np=30 -c len=1 -c length=60 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max =0 -q2 --outf=3 > bombProblems/b1tc_30.txt
clingo solver.py btc_conf.lp -c np=30 -c len=1 -c length=60 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max =1 -q2 --outf=3 > bombProblems/eiter_b1tc_30.txt
echo "Done b1tc 30"

clingo solver.py btc_conf.lp -c np=50 -c len=1 -c length=100 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max =0 -q2 --outf=3 > bombProblems/b1tc_50.txt
clingo solver.py btc_conf.lp -c np=50 -c len=1 -c length=100 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max =1 -q2 --outf=3 > bombProblems/eiter_b1tc_50.txt
echo "Done b1tc 50"

clingo solver.py btc_conf.lp -c np=100 -c len=1 -c length=200 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max =0 -q2 --outf=3 > bombProblems/b1tc_100.txt
clingo solver.py btc_conf.lp -c np=100 -c len=1 -c length=200 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max =1 -q2 --outf=3 > bombProblems/eiter_b1tc_100.txt
echo "Done b1tc 100"

clingo solver.py btc_conf.lp -c np=150 -c len=1 -c length=300 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max =0 -q2 --outf=3 > bombProblems/b1tc_150.txt
clingo solver.py btc_conf.lp -c np=150 -c len=1 -c length=300 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max =1 -q2 --outf=3 > bombProblems/eiter_b1tc_150.txt
echo "Done b1tc 150"



clingo solver.py bmtc_conf.lp -c np=3 -c nt=2 -c len=1 -c length=6 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b2tc_3.txt
clingo solver.py bmtc_conf.lp -c np=3 -c nt=2 -c len=1 -c length=6 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b2tc_3.txt
echo "Done b2tc 3"

clingo solver.py bmtc_conf.lp -c np=5 -c nt=2 -c len=1 -c length=10 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b2tc_5.txt
clingo solver.py bmtc_conf.lp -c np=5 -c nt=2 -c len=1 -c length=10 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b2tc_5.txt
echo "Done b2tc 5"

clingo solver.py bmtc_conf.lp -c np=7 -c nt=2 -c len=1 -c length=14 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b2tc_7.txt
clingo solver.py bmtc_conf.lp -c np=7 -c nt=2 -c len=1 -c length=14 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b2tc_7.txt
echo "Done b2tc 7"

clingo solver.py bmtc_conf.lp -c np=10 -c nt=2 -c len=1 -c length=20 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b2tc_10.txt
clingo solver.py bmtc_conf.lp -c np=10 -c nt=2 -c len=1 -c length=20 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b2tc_10.txt
echo "Done b2tc 10"

clingo solver.py bmtc_conf.lp -c np=30 -c nt=2 -c len=1 -c length=61 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b2tc_30.txt
clingo solver.py bmtc_conf.lp -c np=30 -c nt=2 -c len=1 -c length=61 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b2tc_30.txt
echo "Done b2tc 30"

clingo solver.py bmtc_conf.lp -c np=100 -c nt=2 -c len=1 -c length=200 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b2tc_100.txt
clingo solver.py bmtc_conf.lp -c np=100 -c nt=2 -c len=1 -c length=200 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b2tc_100.txt
echo "Done b2tc 100"



clingo solver.py bmtc_conf.lp -c np=3 -c nt=3 -c len=1 -c length=6 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b3tc_3.txt
clingo solver.py bmtc_conf.lp -c np=3 -c nt=3 -c len=1 -c length=6 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b3tc_3.txt
echo "Done b3tc 3"

clingo solver.py bmtc_conf.lp -c np=5 -c nt=3 -c len=1 -c length=10 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b3tc_5.txt
clingo solver.py bmtc_conf.lp -c np=5 -c nt=3 -c len=1 -c length=10 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b3tc_5.txt
echo "Done b3tc 5"

clingo solver.py bmtc_conf.lp -c np=7 -c nt=3 -c len=1 -c length=14 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b3tc_7.txt
clingo solver.py bmtc_conf.lp -c np=7 -c nt=3 -c len=1 -c length=14 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b3tc_7.txt
echo "Done b3tc 7"

clingo solver.py bmtc_conf.lp -c np=10 -c nt=3 -c len=1 -c length=20 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b3tc_10.txt
clingo solver.py bmtc_conf.lp -c np=10 -c nt=3 -c len=1 -c length=20 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b3tc_10.txt
echo "Done b3tc 10"

clingo solver.py bmtc_conf.lp -c np=30 -c nt=3 -c len=1 -c length=60 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b3tc_30.txt
clingo solver.py bmtc_conf.lp -c np=30 -c nt=3 -c len=1 -c length=60 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b3tc_30.txt
echo "Done b3tc 30"

clingo solver.py bmtc_conf.lp -c np=50 -c nt=3 -c len=1 -c length=100 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=0 -q2 --outf=3 > bombProblems/b3tc_50.txt
clingo solver.py bmtc_conf.lp -c np=50 -c nt=3 -c len=1 -c length=100 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c max=1 -q2 --outf=3 > bombProblems/eiter_b3tc_50.txt
echo "Done b3tc 50"



clingo solver.py btuc_conf.lp -c np=4 -c len=1 -c length=8 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c eiter=0 -q2 --outf=3 > bombProblems/btuc_4.txt
clingo solver.py btuc_conf.lp -c np=4 -c len=1 -c length=8 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c eiter=1 -q2 --outf=3 > bombProblems/eiter_btuc_4.txt
echo "Done btuc 4"

clingo solver.py btuc_conf.lp -c np=6 -c len=1 -c length=18 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c eiter=0 -q2 --outf=3 > bombProblems/btuc_6.txt
clingo solver.py btuc_conf.lp -c np=6 -c len=1 -c length=18 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c eiter=1 -q2 --outf=3 > bombProblems/eiter_btuc_6.txt
echo "Done btuc 6"

clingo solver.py btuc_conf.lp -c np=8 -c len=1 -c length=35 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c eiter=0 -q2 --outf=3 > bombProblems/btuc_8.txt
clingo solver.py btuc_conf.lp -c np=8 -c len=1 -c length=35 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c eiter=1 -q2 --outf=3 > bombProblems/eiter_btuc_8.txt
echo "Done btuc 8"

clingo solver.py btuc_conf.lp -c np=10 -c len=1 -c length=55 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c eiter=0 -q2 --outf=3 > bombProblems/btuc_10.txt
clingo solver.py btuc_conf.lp -c np=10 -c len=1 -c length=55 -c planning=1 -c heuristic=1 -c debug=0 -c initials_only=0 -c eiter=1 -q2 --outf=3 > bombProblems/eiter_btuc_10.txt
echo "Done btuc 10"


