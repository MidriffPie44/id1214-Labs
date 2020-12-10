%  A template for the parser in Prolog - change all Varibles to words (from uppercase to lowercase):
% Use Definite Clause Grammar
% http://www.pathwayslms.com/swipltuts/dcg/
%
% ?- phrase(s(sentence(NP,VP)), phrase(s(sentence(X, V)), [the, girl, likes, the, dog]))
%
% s
%
% op
%:-op(700,:-, '-->').


s --> np(NP, Thing),vp(VP,Thing).

np(Num,Thing) --> n_n(Num,Thing).
np(Num,Thing) --> n_t(Num,Thing).
np(Num,Thing) --> det_n(Num,Thing), n_n(Num,Thing).
np(Num,Thing) --> det_t(Num,Thing), n_t(Num,Thing).


vp(Num,Thing) --> v(Num,Thing).
vp(Num,Thing) --> v(Num,Thing), np(XNum,XThing).


% v(t,alive) --> [XX].
% v(it,alive) --> [XX].

v(t,alive) --> [eats].
v(t,alive) --> [likes].
v(it,alive) --> [run].

% det_n(s,Ting) --> [DET].

det_n(s,Ting) --> [the].
det_t(s,Ting) --> [a].

% n_n(s,alive) --> [BB].
n_n(s,alive) --> [girl].
n_n(s,alive) --> [dog].
n_n(s,alive) --> [boy].

% n_n(s,object) --> [GG].
n_n(s,object) --> [computer].

n_n(pl,alive) --> ['Dogs'].