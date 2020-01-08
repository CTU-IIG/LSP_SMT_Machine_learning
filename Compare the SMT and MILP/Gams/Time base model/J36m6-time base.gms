sets
j jobs /j1*j6/
o operations /o1*o6/
m machines/m1*m6/
t short period/t1*t70/
alias (o,oo);
alias (t,tt);
alias (j,jj);

scalar G a Big number  /100000/ ;

$onecho > myspread.txt
I="%system.fp%myspread.xls"
R1=j36m6!A1:g7
O1=myspread1.inc
R2=j36m6!H1:N37
O2=myspread2.inc

$offecho
$call =xls2gms @myspread.txt

table p(j,o)
$include myspread1.inc
;
table a(j,o,m)
$include myspread2.inc
;



variables
s(j,o,t) if operation o of job j started at short period t
cmax(j) cmax of job j
obj objective function ;

binary Variable s ;
positive Variable cmax ;

Equations
c_max objective function
e1(j,o)
e2(j,o,oo,t)
e3(j,o,m,t)
e4(j,o,t)
;

c_max .. obj=e=sum(j,cmax(j));

e1(j,o) .. sum(t,s(j,o,t))=e=1;
e2(j,o,oo,t)$(ord(o)=ord(oo)+1) .. sum(tt$(ord(tt)<ord(t)+p(j,oo)),s(j,o,tt))=l=(1-s(j,oo,t))*G;
e3(j,o,m,t)$(a(j,o,m)=1) .. sum((jj,oo,tt)$(a(jj,oo,m)=1 and ord(jj)<>ord(j) and ord(tt)>=ord(t) and ord(tt)<ord(t)+p(j,o)),s(jj,oo,tt))=l=(1-s(j,o,t))*G;
e4(j,o,t)$(ord(o)=6) .. cmax(j)=g=(ord(t)-1)+p(j,o)-(1-s(j,o,t))*G;

option mip=cplex;
option reslim=3600 ;
option optcr=0 ;
Model jobsop /all/ ;
solve jobsop miniminzing obj using mip;
Display s.l , cmax.l ;

** objective function= 265
** time= 178 s

