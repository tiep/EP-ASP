%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%initial states%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#program initial.
#external _heuristic.
package(1..np).

1 { holds(armed(P),0) : package(P) } 1. 


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

fluent(armed(P)) :- package(P). 
inertial(armed(P)) :- package(P). 
fluent(clogged).
inertial(clogged).

fluent(unsafe). 

%%%%%%%  actions   %%%%%%%%
action(dunk(P)) :- package(P). 
action(flush).

%%%%%%  executable  %%%%%%% 
executable(dunk(P), T):- action(dunk(P)), not holds(clogged,T), step(T).

%executable(dunk(P), T):- action(dunk(P)), not holds(clogged,T), step(T), 0 {occurs(dunk(P),T1) : step(T1), T1 < T}0.

executable(flush,T) :- action(flush), step(T).

%%%%%  effects   %%%%%%%
-holds(armed(P), T+1) :- occurs(dunk(P), T), step(T). 
1{ -holds(clogged, T+1) ; holds(clogged, T+1)}1 :- occurs(dunk(P), T), step(T).
-holds(clogged, T+1) :- occurs(flush, T), step(T).
holds(unsafe, T) :- holds(armed(P), T), step(T). 
-holds(unsafe, T) :- not holds(unsafe, T), step(T). 


%%%%% occurs  %%%%%%%
1{occurs(A,S) : action(A), executable(A,S)} 1 :- stepless(S), _heuristic.
:- package(P), 2 {occurs(dunk(P),S) : stepless(S)}.

%%%%% goal  %%%%%%%
goal :- -holds(unsafe, LEN), -holds(is_impossible,LEN), max(LEN).

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




