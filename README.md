# EP-ASP

(****) EP-ASP has been fully tested on macOS Sierra with 2.8 GHz Intel Core i7, 16GB RAM, and with CLINGO version 4.5.3


----------------------------------------------------
(****) Requirement:
- CLINGO version 4.5.3. (make sure that ``clingo" is in CLASSPATH)

- Java(TM) SE Runtime Environment (build 1.8.0_111-b14)


----------------------------------------------------
(****) The zip file contains:
+ bt_conf.lp, btc_conf.lp, bmtc_conf.lp, btuc_conf.lp, bmtuc_conf.lp are EP-ASP input files (under ``planning" format) for 'bomb in the toilet',  'bomb in the toilet with certain clog', 'bomb in the toilet with multiple toilet', 'bomb in the toilet with uncertain clog', 'bomb in the toilet with multiple toilet and uncertain clog' problems, respectively.

+ eligibleProblems, yaleProblems, and bombProblems folders contain materials and experimental results for EP-ASP to solve ``eligible", ``yale", ``bomb in the toilet" problems, respectively, that are reported in [1]

+ README.md is this file

+ ForPlanning.md is the file consisting instructions how to run EP-ASP specifically for planning mode.

+ solver.py is EP-ASP solver.

+ script_bomb.sh is a script to run experiments on ``bomb in the toilet" problems. 

+ elps.jar is a jar file used to translate an ELP \Pi to an ASP(\Pi) (see [2]), downloaded from [3].

+ ELPS_manual is a manual file for ELPS format, copied from [3]. 

+ eligible01.elps is an example of an ELP that follows ELPS format (see ELPS_manual.pdf)

+ eligible01.elps.elp is the translation of ``eligible01.elps" into an ASP file using elps.jar (see [2]) 


----------------------------------------------------
(****) How to run EP-ASP
+ Download the folder EP-ASP.
+ Change the current directory into the folder EP-ASP.
+ Run the following commands:

	java -jar elps.jar [ELPS file] -o

	clingo solver.py [ELPS file].elp [options] -q2 --outf=3  

where:
	[ELPS file] is an ELP file under ELPS format (see ELPS_manual.pdf)


	[options] are:	

		``-c pre={0|1}" specifies whether EP-ASP needs to compute brave and cautious consequences as preprocessing. [see Line 4 in Algorithm 3 in [1];

		``-c max={0|1}" specifies whether EP-ASP computes world views under Shen and Eiter's semantics [4].  

		``-c goal_directed_mode=1" specifies that EP-ASP computes world views that satisfies subjective literal ``Kgoal". In general, if users want to compute world view that satisfies Kl_1, ..., Kl_n, ones just simply put a rule ``goal :- l_1, ..., l_n" in the input file, and set ``-c goal_directed_mode=1".

		``-c planning=1" specifies EP-ASP is solving a conformant planning problem. If -c planning=1, the [input_file] must be under ``Conformant Planning" Format, which is described in ``ForPlanning.md" in detail;


	``-q2 --outf=3" option are used to disable all output from clingo.

(***) Example: In order to compute the world views of an ELP, e.g., ``eligible01.elps", which is under ELPS format (see ELPS_manual.pdf), using Shen and Eiter's semantics and having preprocessing, run the following commands:

	java -jar elps.jar eligible01.elps -o

	clingo solver.py eligible01.elps.elp -c pre=1 -c max=1 -q2 --outf=3
  

Note that the output of the first command is the file ``eligible01.elps.elp", that is used as input for the second command. 
 
----------------------------------------------------
References:

[1]. Tran Cao Son, Tiep Le, Patrick T. Kahl, and Anthony P. Leclerc. On Computing World Views of Epistemic Logic Programs. IJCAI, 2017.

[2]. Balai, E., Kahl, P. Epistemic logic programs with sorts. In ASPOCP, 2014.

[3]. https://github.com/iensen/elps

[4]. Yi-Dong Shen and Thomas Eiter. Evaluating epistemic negation in answer set programming. Artificial Intelligence, 2016.


