sets
j jobs (last job is dummy) /j1*j11/
o operations /o1*o15/
m machines/m1*m15/

alias (o,oo);
alias (j,jj);

scalar G a Big number  /100000/ ;

$onecho > myspread.txt
I="%system.fp%myspread.xls"
R1=j150m15!A1:P12
O1=myspread1.inc
R2=j150m15!T1:AI12
O2=myspread2.inc

$offecho
$call =xls2gms @myspread.txt

table p(j,o)
$include myspread1.inc
;
table a(j,o)
$include myspread2.inc
;



variables
s(j,o) start time of operation o of job j
y(j,o,jj,oo) if operation oo of job jj do after operation o of job j
cmax(j) cmax of job j
obj objective function ;

binary Variable y;
positive Variable s;
positive Variable cmax;

Equations
c_max objective function
e1(j,o,jj,oo)
e2(j,o)
e3(j,o)
e4(j,o,oo)
e5(j,o,jj,oo)
e6(j,o)
;

c_max .. obj=e=sum(j,cmax(j));

e1(j,o,jj,oo)$((ord(j)<>ord(jj) or ord(o)<>ord(oo)) and (a(j,o)=a(jj,oo) or a(j,o)=16 or a(jj,oo)=16) and a(j,o)<=16 and a(jj,oo)<=16) .. y(jj,oo,j,o)+y(j,o,jj,oo)=e=1;
e2(j,o)$(ord(j)=11 and ord(o)=1) .. sum((jj,oo),y(jj,oo,j,o))=l=0;
e3(j,o)$(ord(j)=11 and ord(o)=2) .. sum((jj,oo),y(j,o,jj,oo))=l=0;
e4(j,o,oo)$(ord(j)<>11 and ord(o)=ord(oo)+1) .. s(j,o)=g=s(j,oo)+p(j,oo);
e5(j,o,jj,oo)$((ord(j)<>ord(jj) or ord(o)<>ord(oo)) and (a(j,o)=a(jj,oo) or a(j,o)=16 or a(jj,oo)=16) and a(j,o)<=16 and a(jj,oo)<=16) .. s(j,o)=g=s(jj,oo)+p(jj,oo)-(1-y(jj,oo,j,o))*G;
e6(j,o)$(ord(j)<>11 and ord(o)=15) .. cmax(j)=g=s(j,o)+p(j,o);

option mip=cplex;
option reslim=3600 ;
option optcr=0 ;
Model jobsop /all/ ;
solve jobsop miniminzing obj using mip;
Display y.l, s.l , cmax.l ;

** objective function= 1067
** time=  >3600 s

