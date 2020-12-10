%  A template for the parser in Prolog - change all Varibles to words (from uppercase to lowercase):
%
% ?- phrase(s(sentence(NP,VP)), phrase(s(sentence(X, V)), [the, girl, likes, the, dog]))

s --> np(NP, Thing),vp(VP,Thing).

np(Num,Thing) --> n_n(Num,Thing).
np(Num,Thing) --> n_t(Num,Thing).
np(Num,Thing) --> det_n(Num,Thing), n_n(Num,Thing).
np(Num,Thing) --> det_t(Num,Thing), n_t(Num,Thing).


vp(Num,Thing) --> v(Num,Thing).
vp(Num,Thing) --> v(Num,Thing), np(XNum,XThing).

v(it,alive) --> [eats].

v(t,alive) --> [runs].
v(it,alive) --> [run].

v(t,alive) --> [is].
v(it,alive) --> [are].
v(t,alive) --> [likes].


det_n(s,Ting) --> [the].
det_n(s,Ting) --> [those].


det_t(s,Ting) --> [an].
det_t(s,Ting) --> [a].

n_n(s,alive) --> [boy].
n_n(s,alive) --> [girl].
n_n(s,alive) --> [dog].

n_n(s,object) --> [house].

n_n(pl,alive) --> [boys].
n_n(s,alive) --> [girl].
n_n(s,alive) --> [dog].

n_t(s,object) --> [].
n_t(s,object) --> [LL].
n_t(pl,object) --> [crackers].
n_t(s,object) --> [NN].
n_t(pl,object) --> [OO].