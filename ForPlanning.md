# EP-ASP

(****) EP-ASP for solving conformant planning has been fully tested on macOS Sierra with 2.8 GHz Intel Core i7, 16GB RAM, and with CLINGO version 4.5.3




----------------------------------------------------
(****) Requirement:
- CLINGO version 4.5.3. (make sure that "clingo" is in CLASSPATH)




----------------------------------------------------
 (****) How to run EP-ASP
+ Run the command:

	clingo solver.py [input_file] -c len=<len> -c length=<length> -c planning=1 -c heuristic={0|1}  [options] -q2 --outf=3 

where:
    
    [input_file] is an ASP file under ``Conformant Planning" Format, which is described later;

   
    ``-c len=<integer>" is to specify the preset length of solution of all planning problems whose initial states are completion of the conformant planning problem. If ``-c planning=1", ``-c len=<integer>" must be given in [options];

    
    ``-c length=<integer>" is to specify the preset length of solution of the conformant problem. If ``-c planning=1", ``-c length=<integer>" must be given in [options];

    
    ``-c planning=1" specifies EP-ASP is solving a conformant planning problem. If -c planning=1, the [input_file] must be under ``Conformant Planning" Format

    
    ``-c heuristic={0|1}" specifies whether EP-ASP uses the heuristic (mentioned in paper [Son et al., IJCAI-17]). If -c heuristic=1, it must be -c planning=1;


	[options] are:			

		``-c initials_only=1" specifies that EP-ASP needs to solve only classical planning problems whose initial states are completion of the conformant planning problem. This will give users an estimation of what 'len' should be;

		``-c max=1" specifies that EP-ASP computes world views under Shen and Eiter's semantics [Shen. and Eiter., AIJ-2016] as solutions of the conformant planning problem.  



Example: Command to run 'bomb in the toilet with uncertain clog' with 3 packages using heuristic and using conformant planning format is:

	clingo solver.py btuc_conf.lp -c np=3 -c len=1 -c length=6 -c planning=1 -c heuristic=1 -q2 --outf=3

 
****Furthermore, you might want to start clingo using the ``-q2 --outf=3" option to disable all output from clingo.




----------------------------------------------------
(****) Conformant Planning Format (we use 'btuc_conf.lp' for input example)

+ Input file consists of 'initial' part and 'problem' part where:

+ The format of 'initial part' is:

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%initial states%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
#program initial.
#external _heuristic.

<fact_1.>
<fact_2.>
......
<fact_n.>

%%%%%%%%%% finish initial part%%%%%%%%%%%%%%
in which { <fact_i> } is a set of fact specifying possible initial states.   


E.g., The set of facts below specifies that there are np packages, and there is exact one package that is armed in the initial state (state 0): 

package(1..np).
1 { holds(armed(P),0) : package(P) } 1. 


+ The format of 'problem part' is:

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%problem description%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#program problem.

step(0..len):- _heuristic.
step(0..length) :- not _heuristic.
 

max(len) :- _heuristic.
1{max(len); max(length)}1.
max(length) :- not _heuristic.

stepless(0..L-1) :- max(L).


%%%%%%%  fluents   %%%%%%%%%
<fluent_1.>
..........
<fluent_n.>

%%%%%%%  actions   %%%%%%%%
<action_1.>
...........
<action_n.>

%%%%%%  executable  %%%%%%%
<rule_for_determining_if_an_action_1_is_executable_in_step_T.>
...........
<rule_for_determining_if_an_action_n_is_executable_in_step_T.>

%%%%% occurs  %%%%%%%
1{occurs(A,S) : action(A), executable(A,S)} 1 :- stepless(S), _heuristic.

%%%%% goal  %%%%%%%
<goal :-  holds(l_1, LEN), ..., holds(l_{j},LEN), -holds(l_{j+1}, LEN),..., -holds(l_{m},LEN), -holds(is_impossible,LEN), max(LEN).>

%%%% epistemic %%%%%%%
fluent(is_impossible).
inertial(is_impossible).

holds(is_impossible,S+1):- step(S), action(A), occurs(A, S), not executable(A, S). 

-holds(is_impossible, 0).  

-holds(F,0):-not  holds(F,0),fluent(F).

holds(F,S+1):-fluent(F),inertial(F), stepless(S),holds(F,S),not  -holds(F,S+1).

-holds(F,S+1):-fluent(F),inertial(F), stepless(S),-holds(F,S),not  holds(F,S+1).

:-goal,-k_goal.
:-not  m_goal.

k1_goal:-not k0_goal.
k0_goal:-not k1_goal.

k0_goal:-m0_goal.
-k_goal:-k0_goal.
-k_goal:-k1_goal, not goal.
m1_goal:-not m0_goal.
m0_goal:-not m1_goal.
m1_goal:-k1_goal.

m_goal:-m1_goal.
%%%%%%m_goal:-m0_goal, not not goal.
m_goal:-m0_goal, goal.

m1_occurs(A,S):-not m0_occurs(A,S), stepless(S), action(A).
m0_occurs(A,S):-not m1_occurs(A,S), stepless(S), action(A).

m_occurs(A,S):-m1_occurs(A,S), stepless(S), action(A).
m_occurs(A,S):-m0_occurs(A,S), not not occurs(A,S), stepless(S), action(A).

occurs(A,S):-m_occurs(A,S), stepless(S),action(A).

m1_occurs(A,S) :- occurs(A,S),  action(A), step(S). 

 
%%%%%%%%%% finish program part%%%%%%%%%%%%%%

in which:
	+ { <fluent_i.> } is a set of facts representing fluents in conformant planning problem.  
	+ { <action_i.> } is a set of facts representing actions in conformant planning problem.
	+ { <rule_for_determining_if_an_action_i_is_executable_in_step_T.> } is a set of rules, each of which specifies if an action is executable in a step T.

E.g., the rule below specifies the action of dunking a package into a toilet is executable in step T if the toilet is not clogged in step T:
executable(dunk(P), T):- action(dunk(P)), not holds(clogged,T), step(T).

	+ <goal :-  holds(l_1, LEN), ..., holds(l_{j},LEN), -holds(l_{j+1}, LEN),..., -holds(l_{m},LEN), -holds(is_impossible,LEN), max(LEN).> is a rule specifies when the goal is accomplished 

E.g, the rule below specifies if "unsafe" does not hold in a step LEN (i.e., -holds(unsafe, LEN)) , then the goal is accomplished

goal :- -holds(unsafe, LEN), -holds(is_impossible,LEN), max(LEN).


IMPORTANT NOTES: 

1/ All of other facts and rules that are not of the form <....> in the description above are copied into the input file.

2/ If one wants to specify that, for a literal l, it is either l is hold or -l is hold in the initial states, one has to specify as below: 	
	+ in 'initial part', a fact of the form:
		1 { l , neg_l} 1.
	where 'neg_l' is a fresh atom whose meaning is -l, and
	+ in somewhere in 'problem part', a rule of the form:
		-l :- neg_l.

3/ All fluents 'fluent_i' in the problem are considered as not being hold (i.e., -holds(fluent_i,0) in initial states if the fluents is not specified in initial state. 

E.g., Assume the 'initial part' is
#program initial.
#external _heuristic.
package(1..np).

1 { holds(armed(P),0) : package(P) } 1. 

Since this does specify neither holds(unsafe,0) nor -holds(unsafe,0), then it is -holds(unsafe,0).

4/ The constants 'len' and 'length' are integer numbers specified externally from the command to execute EP-ASP. 'len' is the preset length of solution of all planning problems whose initial states are completion of the conformant planning problem, and 'length' is the preset length of solution of the conformant problem.   


5/ For YALE problems translated from elps, they need to add the following rule (for much faster):
m1_occurs(A,S) :- occurs(A,S),  action(A), step(S).


