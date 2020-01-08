sets
j jobs /j1*j6/
o operations /o1*o6/
m machines/m1*m6/
t positions/t1*t6/

alias (j,jj);
alias (o,oo);
alias (t,tt);

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
x(j,o,t) operation o of job j assigned to position t of related machine
s(j,o)    start time of operation o of job j
cmax(j) cmax of job j
obj objective function ;

binary Variable x ;
positive Variable s ;
positive Variable cmax ;

Equations
c_max objective function
e1(j,o)
e2(j,o,jj,oo,t,tt,m)
e3(j,o,oo)
e4(m,t)
e5(j,o)
;

c_max .. obj=e=sum(j,cmax(j));

e1(j,o)$(ord(o)=6) .. cmax(j)=g=s(j,o)+p(j,o);
e2(j,o,jj,oo,t,tt,m)$(ord(t)=ord(tt)+1 and a(j,o,m)=1 and a(jj,oo,m)=1) .. s(j,o)=g=s(jj,oo)+p(jj,oo)-(2-x(j,o,t)-x(jj,oo,tt))*G;
e3(j,o,oo)$(ord(o)=ord(oo)+1) .. s(j,o)=g=s(j,oo)+p(j,oo);
e4(m,t) .. sum((j,o)$(a(j,o,m)=1),x(j,o,t))=l=1;
e5(j,o) .. sum(t,x(j,o,t))=g=1;

option mip=cplex;
option reslim=3600 ;
option optcr=0 ;
Model jobsop /all/ ;
solve jobsop miniminzing obj using mip;
Display x.l , s.l , cmax.l ;

** objective function= 265
** time= 59 s

