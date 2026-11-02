# -*- coding: utf-8 -*-
from .common import *
t,k,p,q,r,s=symbols('t k p q r s')
def mat(M,env="pmatrix"): return "\\begin{%s}%s\\end{%s}"%(env," \\\\ ".join(" & ".join(str(latex(e)) for e in M.row(i)) for i in range(M.rows)),env)
R=Rational
ITEMS=[]
A1=Matrix([[2,1,0],[1,3,1],[0,3,1]])
ITEMS.append(I("2.1","Quiz Ch.2 · Q1",("Inverse of a $3\\times3$ matrix","Ma trận nghịch đảo $3\\times3$"),
 ("The inverse of $A=\\begin{pmatrix}2&1&0\\\\1&3&1\\\\0&3&1\\end{pmatrix}$ is:","Ma trận nghịch đảo của $A$ là:"),
 "$\\begin{pmatrix}0&1&-1\\\\1&-2&2\\\\-3&6&-5\\end{pmatrix}$",
 [("<b>Method.</b> Row-reduce $[A\\mid I]$ until the left block is $I$; the right block is then $A^{-1}$. First $\\det A=2(3-3)-1(1-0)=-1\\ne0$, so $A^{-1}$ exists.","<b>Phương pháp.</b> Rút gọn $[A\\mid I]$ đến khi khối trái là $I$; khối phải khi đó là $A^{-1}$. Trước tiên $\\det A=2(3-3)-1(1-0)=-1\\ne0$ nên $A^{-1}$ tồn tại."),
  ("Alternative: $A^{-1}=\\frac1{\\det A}\\operatorname{adj}A=-\\operatorname{adj}A$ (transpose of the cofactor matrix, then divide by $\\det A$).","Cách khác: $A^{-1}=\\frac1{\\det A}\\operatorname{adj}A=-\\operatorname{adj}A$ (chuyển vị ma trận phần phụ đại số rồi chia cho $\\det A$)."),
  ("<b>Fast exam check:</b> $A\\,(0,1,-3)^T=(0+1+0,\\ 0+3-3,\\ 0+3-3)^T=(1,0,0)^T$ ✓, the first column of $I$. Only option (c) has first column $(0,1,-3)^T$.","<b>Kiểm tra nhanh khi thi:</b> $A\\,(0,1,-3)^T=(0+1+0,\\ 0+3-3,\\ 0+3-3)^T=(1,0,0)^T$ ✓, đúng cột đầu của $I$. Chỉ đáp án (c) có cột đầu $(0,1,-3)^T$.")],
 choices=[mat(Matrix([[0,-1,-3],[-1,-2,-6],[-1,-2,-5]])),mat(Matrix([[0,-1,-1],[-1,-2,-2],[-3,-6,-5]])),mat(Matrix([[0,1,-1],[1,-2,2],[-3,6,-5]])),mat(Matrix([[0,1,-3],[1,-2,6],[-1,2,5]]))],
 trap=("Testing <i>one column</i> of $AA^{-1}=I$ is faster than inverting from scratch.","Thử <i>một cột</i> của $AA^{-1}=I$ nhanh hơn nghịch đảo từ đầu."),
 variants=[
  V("★ Triangular","Find $B^{-1}$ for $B=\\begin{pmatrix}1&2&0\\\\0&1&3\\\\0&0&1\\end{pmatrix}$.","Tìm $B^{-1}$ với $B=\\begin{pmatrix}1&2&0\\\\0&1&3\\\\0&0&1\\end{pmatrix}$.","$\\begin{pmatrix}1&-2&6\\\\0&1&-3\\\\0&0&1\\end{pmatrix}$",
   ("In $[B\\mid I]$ do $R_2-3R_3$ then $R_1-2R_2$.","Trong $[B\\mid I]$ làm $R_2-3R_3$ rồi $R_1-2R_2$."),
   lambda:Matrix([[1,2,0],[0,1,3],[0,0,1]]).inv()==Matrix([[1,-2,6],[0,1,-3],[0,0,1]])),
  V("★★ Parameter","For which $p$ is $\\begin{pmatrix}1&2&p\\\\2&4&6\\\\1&0&1\\end{pmatrix}$ <b>not</b> invertible?","Với $p$ nào ma trận $\\begin{pmatrix}1&2&p\\\\2&4&6\\\\1&0&1\\end{pmatrix}$ <b>không</b> khả nghịch?","$p=3$",
   ("Expanding along row 1: $\\det=4+8-4p=12-4p$, zero iff $p=3$. (Geometrically row 2 $=2(1,2,3)$ is parallel to row 1 exactly then.)","Khai triển theo hàng 1: $\\det=4+8-4p=12-4p$, bằng 0 iff $p=3$. (Hình học: khi đó hàng 2 $=2(1,2,3)$ song song hàng 1.)"),
   lambda:Matrix([[1,2,p],[2,4,6],[1,0,1]]).det().expand()==12-4*p),
  V("★★★ Use the inverse","With $A$ from the question, solve $A\\mathbf x=(1,2,3)^T$ using $A^{-1}$.","Với $A$ ở câu hỏi, giải $A\\mathbf x=(1,2,3)^T$ bằng $A^{-1}$.","$\\mathbf x=(-1,\\ 3,\\ -6)^T$",
   ("$\\mathbf x=A^{-1}\\mathbf b$: row 1: $0+2-3=-1$; row 2: $1-4+6=3$; row 3: $-3+12-15=-6$. Check: $2(-1)+3=1$ ✓, $-1+9-6=2$ ✓, $9-6=3$ ✓.","$\\mathbf x=A^{-1}\\mathbf b$: hàng 1: $0+2-3=-1$; hàng 2: $1-4+6=3$; hàng 3: $-3+12-15=-6$. Kiểm tra: $2(-1)+3=1$ ✓, $-1+9-6=2$ ✓, $9-6=3$ ✓."),
   lambda:A1*Matrix([-1,3,-6])==Matrix([1,2,3]))]))

ITEMS.append(I("2.2","Quiz Ch.2 · Q2, Q7, Q8, Q11",("Sizes and existence of products","Kích thước và sự tồn tại của tích"),
 ("(Q2) $B$ is $3\\times4$, $E$ is $4\\times3$: size of $BE$? (Q7) $A=[a_{ij}]_{m\\times n}$, $B=[b_{ij}]_{p\\times q}$: when does $AB$ exist? (Q8) $A:4\\times6$, $B:6\\times3$: sizes of $AB$ and $BA^T$? (Q11) $A:2\\times3$, $B:3\\times5$: size of $AB$?","(Q2) $B$ cỡ $3\\times4$, $E$ cỡ $4\\times3$: cỡ của $BE$? (Q7) khi nào $AB$ tồn tại? (Q8) cỡ của $AB$ và $BA^T$? (Q11) cỡ của $AB$?"),
 "Q2: $3\\times3$ · Q7: $n=p$ · Q8: $4\\times3$; $BA^T$ does not exist · Q11: $2\\times5$",
 [("<b>Rule.</b> $(m\\times n)(p\\times q)$ exists iff the <b>inner</b> numbers match, $n=p$; the result has the <b>outer</b> numbers: $m\\times q$.","<b>Quy tắc.</b> $(m\\times n)(p\\times q)$ tồn tại iff hai số <b>trong</b> bằng nhau, $n=p$; kết quả có cỡ hai số <b>ngoài</b>: $m\\times q$."),
  ("Q2: $(3\\times\\underline4)(\\underline4\\times3)\\to3\\times3$. Q11: $(2\\times\\underline3)(\\underline3\\times5)\\to2\\times5$. Q7: need $n=p$.","Q2: $(3\\times\\underline4)(\\underline4\\times3)\\to3\\times3$. Q11: $(2\\times\\underline3)(\\underline3\\times5)\\to2\\times5$. Q7: cần $n=p$."),
  ("Q8: $AB=(4\\times\\underline6)(\\underline6\\times3)\\to4\\times3$. But $A^T$ is $6\\times4$, so $BA^T=(6\\times\\underline3)(\\underline6\\times4)$: inner numbers $3\\ne6$ ⇒ <b>does not exist</b>.","Q8: $AB=(4\\times\\underline6)(\\underline6\\times3)\\to4\\times3$. Nhưng $A^T$ cỡ $6\\times4$ nên $BA^T=(6\\times\\underline3)(\\underline6\\times4)$: hai số trong $3\\ne6$ ⇒ <b>không tồn tại</b>.")],
 trap=("Remember to transpose the sizes ($m\\times n\\to n\\times m$) before testing.","Nhớ đổi cỡ khi chuyển vị ($m\\times n\\to n\\times m$) rồi mới kiểm tra."),mock="Q2, Q13",
 variants=[
  V("★ Which exist?","$C:2\\times3$, $D:3\\times2$, $E:2\\times2$. Which of $CD,\\ DC,\\ CE,\\ EC,\\ CDE$ exist and what sizes?","$C:2\\times3$, $D:3\\times2$, $E:2\\times2$. Tích nào trong $CD,\\ DC,\\ CE,\\ EC,\\ CDE$ tồn tại, cỡ bao nhiêu?","$CD:2\\times2$; $DC:3\\times3$; $CE$ no; $EC:2\\times3$; $CDE:2\\times2$",
   ("$CE=(2\\times\\underline3)(\\underline2\\times2)$ fails. $CD=2\\times2$, $DC=3\\times3$, $EC=2\\times3$, and $CDE=(CD)E=(2\\times2)(2\\times2)=2\\times2$.","$CE=(2\\times\\underline3)(\\underline2\\times2)$ không được. $CD=2\\times2$, $DC=3\\times3$, $EC=2\\times3$, và $CDE=(CD)E=(2\\times2)(2\\times2)=2\\times2$."),
   lambda:Matrix(2,3,lambda i,j:1)*Matrix(3,2,lambda i,j:1)!=None),
  V("★★ Sums and products","$A:3\\times4$, $B:4\\times3$. Which exist: $AB,\\ BA,\\ A+B^T,\\ A+B$, and what are the sizes?","$A:3\\times4$, $B:4\\times3$. Tích/tổng nào tồn tại: $AB,\\ BA,\\ A+B^T,\\ A+B$ và cỡ?","$AB:3\\times3$; $BA:4\\times4$; $A+B^T:3\\times4$; $A+B$ no",
   ("Sums need <i>equal</i> sizes: $B^T$ is $3\\times4$ ✓, but $B$ is $4\\times3\\ne3\\times4$.","Tổng cần hai ma trận <i>cùng cỡ</i>: $B^T$ cỡ $3\\times4$ ✓, còn $B$ cỡ $4\\times3\\ne3\\times4$."),lambda:True),
  V("★★★ Rank/size angle","$A:m\\times n$. Show $AA^T$ and $A^TA$ always exist and give their sizes; for $A$ of size $2\\times5$ say which can be invertible.","$A:m\\times n$. Chứng minh $AA^T$ và $A^TA$ luôn tồn tại, cho cỡ; với $A$ cỡ $2\\times5$, ma trận nào có thể khả nghịch?","$AA^T:m\\times m$, $A^TA:n\\times n$; for $2\\times5$ only $AA^T$ ($2\\times2$) can be invertible",
   ("$(m\\times\\underline n)(\\underline n\\times m)$ and $(n\\times\\underline m)(\\underline m\\times n)$. $A^TA$ is $5\\times5$ but has rank $\\le2<5$ ⇒ singular.","$(m\\times\\underline n)(\\underline n\\times m)$ và $(n\\times\\underline m)(\\underline m\\times n)$. $A^TA$ cỡ $5\\times5$ nhưng hạng $\\le2<5$ ⇒ suy biến."),
   lambda:Matrix([[1,2,3,4,5],[0,1,0,1,0]]).T.multiply(Matrix([[1,2,3,4,5],[0,1,0,1,0]])).det()==0)]))

ITEMS.append(I("2.3","Quiz Ch.2 · Q3",("Recover $A$ from $(3A)^{-1}$","Tìm $A$ từ $(3A)^{-1}$"),
 ("Let $(3A)^{-1}=\\begin{bmatrix}4&-1\\\\2&3\\end{bmatrix}$. Find $A$.","Cho $(3A)^{-1}=\\begin{bmatrix}4&-1\\\\2&3\\end{bmatrix}$. Tìm $A$."),
 "$\\begin{bmatrix}1/14&1/42\\\\-1/21&2/21\\end{bmatrix}$",
 [("<b>Isolate $A$.</b> Invert both sides: $3A=\\begin{bmatrix}4&-1\\\\2&3\\end{bmatrix}^{-1}$. Then divide by the scalar $3$: $A=\\frac13\\begin{bmatrix}4&-1\\\\2&3\\end{bmatrix}^{-1}$.","<b>Cô lập $A$.</b> Nghịch đảo hai vế: $3A=\\begin{bmatrix}4&-1\\\\2&3\\end{bmatrix}^{-1}$. Rồi chia cho số $3$: $A=\\frac13\\begin{bmatrix}4&-1\\\\2&3\\end{bmatrix}^{-1}$."),
  ("$2\\times2$ inverse: $\\begin{bmatrix}a&b\\\\c&d\\end{bmatrix}^{-1}=\\frac1{ad-bc}\\begin{bmatrix}d&-b\\\\-c&a\\end{bmatrix}$. Here $ad-bc=12+2=14$, so the inverse is $\\frac1{14}\\begin{bmatrix}3&1\\\\-2&4\\end{bmatrix}$.","Nghịch đảo $2\\times2$: $\\begin{bmatrix}a&b\\\\c&d\\end{bmatrix}^{-1}=\\frac1{ad-bc}\\begin{bmatrix}d&-b\\\\-c&a\\end{bmatrix}$. Ở đây $ad-bc=12+2=14$, nên nghịch đảo là $\\frac1{14}\\begin{bmatrix}3&1\\\\-2&4\\end{bmatrix}$."),
  ("Multiply by $\\frac13$: $A=\\frac1{42}\\begin{bmatrix}3&1\\\\-2&4\\end{bmatrix}=\\begin{bmatrix}1/14&1/42\\\\-1/21&2/21\\end{bmatrix}$.","Nhân với $\\frac13$: $A=\\frac1{42}\\begin{bmatrix}3&1\\\\-2&4\\end{bmatrix}=\\begin{bmatrix}1/14&1/42\\\\-1/21&2/21\\end{bmatrix}$.")],
 trap=("$(cA)^{-1}=\\frac1cA^{-1}$, so $A=\\frac1c(\\ldots)^{-1}$, not $c(\\ldots)^{-1}$ (that is option (a)).","$(cA)^{-1}=\\frac1cA^{-1}$, nên $A=\\frac1c(\\ldots)^{-1}$, không phải nhân $c$ (đó là đáp án (a))."),
 variants=[
  V("★ Same type","$(2A)^{-1}=\\begin{bmatrix}1&2\\\\3&5\\end{bmatrix}$. Find $A$.","$(2A)^{-1}=\\begin{bmatrix}1&2\\\\3&5\\end{bmatrix}$. Tìm $A$.","$\\begin{bmatrix}-5/2&1\\\\3/2&-1/2\\end{bmatrix}$",
   ("$\\det=5-6=-1$, inverse $=\\begin{bmatrix}-5&2\\\\3&-1\\end{bmatrix}$; divide by $2$.","$\\det=5-6=-1$, nghịch đảo $=\\begin{bmatrix}-5&2\\\\3&-1\\end{bmatrix}$; chia $2$."),
   lambda:(Matrix([[-R(5,2),1],[R(3,2),-R(1,2)]])*2).inv()==Matrix([[1,2],[3,5]])),
  V("★★ With a transpose","$A^{-1}=\\begin{bmatrix}1&2\\\\0&1\\end{bmatrix}$. Find $(2A^T)^{-1}$.","$A^{-1}=\\begin{bmatrix}1&2\\\\0&1\\end{bmatrix}$. Tìm $(2A^T)^{-1}$.","$\\begin{bmatrix}1/2&0\\\\1&1/2\\end{bmatrix}$",
   ("$(2A^T)^{-1}=\\frac12(A^T)^{-1}=\\frac12(A^{-1})^T=\\frac12\\begin{bmatrix}1&0\\\\2&1\\end{bmatrix}$.","$(2A^T)^{-1}=\\frac12(A^T)^{-1}=\\frac12(A^{-1})^T=\\frac12\\begin{bmatrix}1&0\\\\2&1\\end{bmatrix}$."),
   lambda:(2*Matrix([[1,2],[0,1]]).inv().T).inv()==Matrix([[R(1,2),0],[1,R(1,2)]]))]))

ITEMS.append(I("2.4","Quiz Ch.2 · Q4",("When is $(A+B)(A-B)=A^2-B^2$?","Khi nào $(A+B)(A-B)=A^2-B^2$?"),
 ("$A=\\begin{bmatrix}1&-1\\\\2&2\\end{bmatrix}$, $B=\\begin{bmatrix}1&\\alpha\\\\\\beta&1\\end{bmatrix}$. If $(A+B)(A-B)=A^2-B^2$ then:","$A=\\begin{bmatrix}1&-1\\\\2&2\\end{bmatrix}$, $B=\\begin{bmatrix}1&\\alpha\\\\\\beta&1\\end{bmatrix}$. Nếu $(A+B)(A-B)=A^2-B^2$ thì:"),
 "$\\alpha=\\beta=0$",
 [("Expand: $(A+B)(A-B)=A^2-AB+BA-B^2$. This equals $A^2-B^2$ iff $-AB+BA=0$, i.e. <b>$AB=BA$</b> (matrices must commute).","Khai triển: $(A+B)(A-B)=A^2-AB+BA-B^2$. Bằng $A^2-B^2$ iff $-AB+BA=0$, tức <b>$AB=BA$</b> (hai ma trận giao hoán)."),
  ("$AB=\\begin{bmatrix}1-\\beta&\\alpha-1\\\\2+2\\beta&2\\alpha+2\\end{bmatrix}$, $BA=\\begin{bmatrix}1+2\\alpha&-1+2\\alpha\\\\\\beta+2&-\\beta+2\\end{bmatrix}$.","$AB=\\begin{bmatrix}1-\\beta&\\alpha-1\\\\2+2\\beta&2\\alpha+2\\end{bmatrix}$, $BA=\\begin{bmatrix}1+2\\alpha&-1+2\\alpha\\\\\\beta+2&-\\beta+2\\end{bmatrix}$."),
  ("Equate entries: $(1,2)$: $\\alpha-1=2\\alpha-1\\Rightarrow\\alpha=0$; $(1,1)$: $1-\\beta=1+2\\alpha=1\\Rightarrow\\beta=0$. Check $(2,1)$: $2=2$ ✓, $(2,2)$: $2=2$ ✓.","So khớp các phần tử: $(1,2)$: $\\alpha-1=2\\alpha-1\\Rightarrow\\alpha=0$; $(1,1)$: $1-\\beta=1+2\\alpha=1\\Rightarrow\\beta=0$. Kiểm $(2,1)$: $2=2$ ✓, $(2,2)$: $2=2$ ✓.")],
 variants=[
  V("★ Commuting family","$A=\\begin{bmatrix}1&2\\\\0&1\\end{bmatrix}$, $B=\\begin{bmatrix}1&p\\\\q&1\\end{bmatrix}$. For which $p,q$ does $AB=BA$?","$A=\\begin{bmatrix}1&2\\\\0&1\\end{bmatrix}$, $B=\\begin{bmatrix}1&p\\\\q&1\\end{bmatrix}$. $p,q$ nào cho $AB=BA$?","$q=0$, $p$ any",
   ("$AB-BA=\\begin{bmatrix}2q&0\\0&-2q\\end{bmatrix}$ (entry $2q$ at $(1,1)$, $-2q$ at $(2,2)$, $0$ elsewhere), so only $q=0$ is needed.","$AB-BA=\\begin{bmatrix}2q&0\\0&-2q\\end{bmatrix}$ (phần tử $(1,1)$ là $2q$, $(2,2)$ là $-2q$, còn lại $0$); nên chỉ cần $q=0$."),
   lambda:(Matrix([[1,2],[0,1]])*Matrix([[1,p],[q,1]])-Matrix([[1,p],[q,1]])*Matrix([[1,2],[0,1]])).applyfunc(expand)==Matrix([[2*q,0],[0,-2*q]])),
  V("★★ Failure size","For $A=\\begin{bmatrix}0&1\\\\0&0\\end{bmatrix}$, $B=\\begin{bmatrix}0&0\\\\1&0\\end{bmatrix}$ compute $(A+B)^2-(A^2+2AB+B^2)$.","Với $A,B$ trên tính $(A+B)^2-(A^2+2AB+B^2)$.","$\\begin{bmatrix}-1&0\\\\0&1\\end{bmatrix}$",
   ("$(A+B)^2=A^2+AB+BA+B^2$, so the difference is $BA-AB=\\begin{bmatrix}0&0\\\\0&1\\end{bmatrix}-\\begin{bmatrix}1&0\\\\0&0\\end{bmatrix}$.","$(A+B)^2=A^2+AB+BA+B^2$, nên hiệu là $BA-AB=\\begin{bmatrix}0&0\\\\0&1\\end{bmatrix}-\\begin{bmatrix}1&0\\\\0&0\\end{bmatrix}$."),
   lambda:(lambda A,B:(A+B)**2-(A*A+2*A*B+B*B)==Matrix([[-1,0],[0,1]]))(Matrix([[0,1],[0,0]]),Matrix([[0,0],[1,0]]))),
  V("★★★ Commutant","Find all $B=\\begin{bmatrix}p&q\\\\r&s\\end{bmatrix}$ commuting with $A=\\begin{bmatrix}1&1\\\\0&1\\end{bmatrix}$.","Tìm mọi $B=\\begin{bmatrix}p&q\\\\r&s\\end{bmatrix}$ giao hoán với $A=\\begin{bmatrix}1&1\\\\0&1\\end{bmatrix}$.","$B=\\begin{bmatrix}p&q\\\\0&p\\end{bmatrix}$",
   ("$AB=BA$ gives $r=0$ (from entry $(1,1)$) and $s=p$ (from entry $(1,2)$); $q$ is free.","$AB=BA$ cho $r=0$ (phần tử $(1,1)$) và $s=p$ (phần tử $(1,2)$); $q$ tự do."),
   lambda:solve(list(Matrix([[1,1],[0,1]])*Matrix([[p,q],[r,s]])-Matrix([[p,q],[r,s]])*Matrix([[1,1],[0,1]])),[r,s])=={r:0,s:p})]))

ITEMS.append(I("2.5","Quiz Ch.2 · Q5, Q9",("Special matrices and building a matrix from a formula","Ma trận đặc biệt và dựng ma trận từ công thức"),
 ("(Q5) What type is $A=\\begin{bmatrix}a_{11}&0&\\dots&0\\\\0&a_{22}&\\dots&0\\\\\\vdots&&\\ddots&\\vdots\\\\0&0&\\dots&a_{nn}\\end{bmatrix}$? &nbsp;(Q9) If $a_{ij}=\\frac12(3i-2j)$ and $A=[a_{ij}]_{2\\times2}$, then $A=$?","(Q5) Loại ma trận nào? (Q9) Nếu $a_{ij}=\\frac12(3i-2j)$, $A=[a_{ij}]_{2\\times2}$ thì $A=$?"),
 "Q5: diagonal <b>and</b> square · Q9: $\\begin{bmatrix}1/2&-1/2\\\\2&1\\end{bmatrix}$",
 [("Q5: it has $n$ rows and $n$ columns ⇒ <b>square</b>; all entries off the main diagonal are $0$ ⇒ <b>diagonal</b>. Both labels are true (the quiz accepts both).","Q5: có $n$ hàng $n$ cột ⇒ <b>vuông</b>; mọi phần tử ngoài đường chéo chính bằng $0$ ⇒ <b>chéo</b>. Cả hai nhãn đều đúng (đề chấp nhận cả hai)."),
  ("Q9: $a_{ij}$ means row $i$, column $j$. Compute the four entries: $a_{11}=\\frac12(3-2)=\\frac12$; $a_{12}=\\frac12(3-4)=-\\frac12$; $a_{21}=\\frac12(6-2)=2$; $a_{22}=\\frac12(6-4)=1$.","Q9: $a_{ij}$ là hàng $i$, cột $j$. Tính bốn phần tử: $a_{11}=\\frac12(3-2)=\\frac12$; $a_{12}=\\frac12(3-4)=-\\frac12$; $a_{21}=\\frac12(6-2)=2$; $a_{22}=\\frac12(6-4)=1$.")],
 trap=("In Q9 the first index is the <i>row</i>: do not fill column by column (that gives the transpose, option (d)).","Ở Q9 chỉ số đầu là <i>hàng</i>: đừng điền theo cột (sẽ ra ma trận chuyển vị, đáp án (d))."),
 variants=[
  V("★ Build","$a_{ij}=i^2-j$, $A$ of size $3\\times2$. Write $A$.","$a_{ij}=i^2-j$, $A$ cỡ $3\\times2$. Viết $A$.","$\\begin{bmatrix}0&-1\\\\3&2\\\\8&7\\end{bmatrix}$",("Row $i$: $(i^2-1,\\ i^2-2)$ for $i=1,2,3$.","Hàng $i$: $(i^2-1,\\ i^2-2)$ với $i=1,2,3$."),
   lambda:Matrix(3,2,lambda i,j:(i+1)**2-(j+1))==Matrix([[0,-1],[3,2],[8,7]])),
  V("★★ Determinant of a pattern","$a_{ij}=\\min(i,j)$, $3\\times3$. Write $A$ and compute $\\det A$.","$a_{ij}=\\min(i,j)$, $3\\times3$. Viết $A$ và tính $\\det A$.","$A=\\begin{bmatrix}1&1&1\\\\1&2&2\\\\1&2&3\\end{bmatrix}$, $\\det A=1$",("$R_2-R_1$, $R_3-R_2$ give an upper triangular matrix with diagonal $1,1,1$.","$R_2-R_1$, $R_3-R_2$ cho ma trận tam giác trên với đường chéo $1,1,1$."),
   lambda:Matrix(3,3,lambda i,j:min(i,j)+1).det()==1),
  V("★★★ Diagonal powers","$D=\\operatorname{diag}(2,3,-1)$. Find $D^5$ and $D^{-1}$.","$D=\\operatorname{diag}(2,3,-1)$. Tìm $D^5$ và $D^{-1}$.","$D^5=\\operatorname{diag}(32,243,-1)$, $D^{-1}=\\operatorname{diag}(\\frac12,\\frac13,-1)$",("For a diagonal matrix powers and inverses act entry by entry on the diagonal.","Với ma trận chéo, lũy thừa và nghịch đảo tác động lên từng phần tử đường chéo."),
   lambda:diag(2,3,-1)**5==diag(32,243,-1) and diag(2,3,-1).inv()==diag(R(1,2),R(1,3),-1))]))

ITEMS.append(I("2.6","Quiz Ch.2 · Q6 (figure missing)",("Grade matrices (method)","Ma trận điểm (phương pháp)"),
 ("Two midterms and a final determine the grade. The matrices for six students under two grading systems are shown (the matrices did <b>not</b> load in the PDF). How many received an “A” ($\\ge85$) in each system?","Hai bài giữa kỳ và một bài cuối kỳ quyết định điểm. Các ma trận của sáu sinh viên theo hai cách chấm đã được cho (ma trận <b>không hiện</b> trong PDF). Mỗi cách có bao nhiêu sinh viên được “A” ($\\ge85$)?"),
 "G1 has 4 and G2 has 4 (as printed)",
 [("<b>Method.</b> Put the scores in a $6\\times3$ matrix $S$ (rows = students) and the weights in a column $w$ ($3\\times1$). The final grades are the vector $S\\,w$ — a matrix-vector product.","<b>Phương pháp.</b> Đặt điểm vào ma trận $S$ cỡ $6\\times3$ (hàng = sinh viên) và trọng số vào cột $w$ ($3\\times1$). Điểm cuối là vectơ $S\\,w$ — tích ma trận với vectơ."),
  ("Compute each entry (row·weights), then count how many are $\\ge85$. Send me the picture of the two matrices if you want the exact numbers.","Tính từng phần tử (hàng·trọng số), rồi đếm số phần tử $\\ge85$. Gửi lại hình hai ma trận nếu muốn có số liệu chính xác.")],
 variants=[
  V("★ Worked example","Scores $S=\\begin{bmatrix}80&90&100\\\\70&60&90\\\\95&85&80\\end{bmatrix}$, weights $w=(0.25,0.25,0.5)^T$. Who gets an A ($\\ge85$)?","Điểm $S=\\begin{bmatrix}80&90&100\\\\70&60&90\\\\95&85&80\\end{bmatrix}$, trọng số $w=(0.25,0.25,0.5)^T$. Ai được A ($\\ge85$)?","Only student 1 ($92.5$); others $71.25$ and $84.0$",
   ("$Sw=(20+22.5+50,\\ 17.5+15+45,\\ 23.75+21.25+40)=(92.5,\\ 77.5,\\ 85)$. So students 1 and 3 reach $\\ge85$.","$Sw=(20+22.5+50,\\ 17.5+15+45,\\ 23.75+21.25+40)=(92.5,\\ 77.5,\\ 85)$. Nên sinh viên 1 và 3 đạt $\\ge85$."),
   lambda:True)]))
# correct the answer string of the worked example to match the computation
ITEMS[-1].variants[0].ans="Students 1 and 3 ($92.5$ and $85$); student 2 has $77.5$"

ITEMS.append(I("2.7","Quiz Ch.2 · Q10",("Householder matrix","Ma trận Householder"),
 ("$u$ is an $n\\times1$ column with $u^Tu=1$ (so $|u|=1$). $H=I_n-2uu^T$. Which is true: (a) $H^2=I_n$, (b) $\\det H=0$, (c) $uu^T=I_n$, (d) $H$ not symmetric?","$u$ là cột $n\\times1$ với $u^Tu=1$. $H=I_n-2uu^T$. Mệnh đề nào đúng?"),
 "(a) $H^2=I_n$",
 [("Compute $H^2=(I-2uu^T)(I-2uu^T)=I-4uu^T+4u(u^Tu)u^T$.","Tính $H^2=(I-2uu^T)(I-2uu^T)=I-4uu^T+4u(u^Tu)u^T$."),
  ("Use $u^Tu=1$ (a $1\\times1$ number, so it can be pulled out): $4u(u^Tu)u^T=4uu^T$. Hence $H^2=I-4uu^T+4uu^T=I$.","Dùng $u^Tu=1$ (số $1\\times1$ nên đưa ra ngoài được): $4u(u^Tu)u^T=4uu^T$. Vậy $H^2=I-4uu^T+4uu^T=I$."),
  ("Eliminate the others: $H^T=I-2(uu^T)^T=I-2uu^T=H$ (symmetric, so (d) false); $uu^T$ is $n\\times n$ of rank 1, not $I_n$ for $n\\ge2$ (c false); $Hu=u-2u(u^Tu)=-u\\ne0$ so $H$ is invertible, $\\det H\\ne0$ (b false); in fact $\\det H=-1$.","Loại trừ: $H^T=I-2(uu^T)^T=I-2uu^T=H$ (đối xứng nên (d) sai); $uu^T$ hạng 1, không phải $I_n$ khi $n\\ge2$ (c sai); $Hu=u-2u(u^Tu)=-u$ nên $H$ khả nghịch, $\\det H\\ne0$ (b sai); thực ra $\\det H=-1$.")],
 mock="Q18",
 variants=[
  V("★ Explicit","$u=\\frac15(3,4)^T$. Compute $H$ and verify $H^2=I$.","$u=\\frac15(3,4)^T$. Tính $H$ và kiểm $H^2=I$.","$H=\\frac1{25}\\begin{bmatrix}7&-24\\\\-24&-7\\end{bmatrix}$",
   ("$uu^T=\\frac1{25}\\begin{bmatrix}9&12\\\\12&16\\end{bmatrix}$, so $H=I-\\frac2{25}\\begin{bmatrix}9&12\\\\12&16\\end{bmatrix}$. $H^2$: $\\frac1{625}(49+576)=1$ on the diagonal, $0$ off it.","$uu^T=\\frac1{25}\\begin{bmatrix}9&12\\\\12&16\\end{bmatrix}$, nên $H=I-\\frac2{25}\\begin{bmatrix}9&12\\\\12&16\\end{bmatrix}$. $H^2$: đường chéo $\\frac1{625}(49+576)=1$, ngoài đường chéo $0$."),
   lambda:(lambda u:(eye(2)-2*u*u.T)**2==eye(2) and eye(2)-2*u*u.T==Matrix([[R(7,25),-R(24,25)],[-R(24,25),-R(7,25)]]))(Matrix([R(3,5),R(4,5)]))),
  V("★★★ Geometry","Show $Hu=-u$, and $Hv=v$ if $u^Tv=0$. What does $H$ do geometrically?","Chứng minh $Hu=-u$ và $Hv=v$ nếu $u^Tv=0$. $H$ làm gì về hình học?","Reflection across the hyperplane $u^\\perp$; $\\det H=-1$",
   ("$Hu=u-2u(u^Tu)=-u$; $Hv=v-2u(u^Tv)=v$. It flips the component along $u$ and keeps the rest: a reflection.","$Hu=u-2u(u^Tu)=-u$; $Hv=v-2u(u^Tv)=v$. Nó đổi dấu thành phần theo $u$ và giữ phần còn lại: phép đối xứng gương."),
   lambda:(lambda u:(eye(2)-2*u*u.T).det()==-1)(Matrix([R(3,5),R(4,5)])))]))

ITEMS.append(I("2.8","Quiz Ch.2 · Q12",("Powers of $iI$","Lũy thừa của $iI$"),
 ("$i=\\sqrt{-1}$, $A=\\begin{bmatrix}i&0\\\\0&i\\end{bmatrix}$. Find $A^4$.","$i=\\sqrt{-1}$, $A=\\begin{bmatrix}i&0\\\\0&i\\end{bmatrix}$. Tìm $A^4$."),
 "$\\begin{bmatrix}1&0\\\\0&1\\end{bmatrix}$",
 [("$A=iI$ is diagonal, so $A^n=\\operatorname{diag}(i^n,i^n)=i^nI$ (powers act entry by entry).","$A=iI$ là ma trận chéo, nên $A^n=\\operatorname{diag}(i^n,i^n)=i^nI$ (lũy thừa tác động từng phần tử)."),
  ("$i^2=-1$, so $i^4=(i^2)^2=1$. Hence $A^4=1\\cdot I=I$.","$i^2=-1$ nên $i^4=(i^2)^2=1$. Vậy $A^4=1\\cdot I=I$.")],
 trap=("(b) is $A^2=-I$; do not stop at the square.","(b) là $A^2=-I$; đừng dừng ở bình phương."),
 variants=[
  V("★ Large power","Find $(iI_2)^{2025}$.","Tìm $(iI_2)^{2025}$.","$iI_2$",("$i^n$ repeats with period 4; $2025=4\\cdot506+1$, so $i^{2025}=i$.","$i^n$ lặp chu kỳ 4; $2025=4\\cdot506+1$ nên $i^{2025}=i$."),lambda:2025%4==1),
  V("★★ Rotation matrix","$R=\\begin{bmatrix}0&-1\\\\1&0\\end{bmatrix}$ (90° rotation). Find $R^{2025}$.","$R=\\begin{bmatrix}0&-1\\\\1&0\\end{bmatrix}$ (quay 90°). Tìm $R^{2025}$.","$R$ itself",("$R^2=-I$, $R^4=I$; $2025\\bmod4=1$.","$R^2=-I$, $R^4=I$; $2025\\bmod4=1$."),
   lambda:Matrix([[0,-1],[1,0]])**2025==Matrix([[0,-1],[1,0]]))]))

ITEMS.append(I("2.9","Quiz Ch.2 · Q13, Q14",("Rules that do and do not hold","Quy tắc đúng và sai"),
 ("(Q13) For same-size $M,N$ and scalar $c$, which property does <b>not</b> always hold? (a) $(M+N)^T=M^T+N^T$ (b) $MN=NM$ (c) $(M^T)^T=M$ (d) $(cM)^T=cM^T$. &nbsp;(Q14) $A,D,P$ are $n\\times n$, $AP=PD$, $P$ nonsingular. Must $A=D$?","(Q13) Tính chất nào <b>không</b> luôn đúng? (Q14) $AP=PD$, $P$ không suy biến. $A=D$ có bắt buộc không?"),
 "Q13: (b) $MN=NM$ · Q14: False",
 [("Q13: (a),(c),(d) are the standard transpose rules. Matrix multiplication is <b>not commutative</b>: e.g. $M=\\begin{bmatrix}0&1\\\\0&0\\end{bmatrix}$, $N=\\begin{bmatrix}0&0\\\\1&0\\end{bmatrix}$: $MN=\\operatorname{diag}(1,0)\\ne NM=\\operatorname{diag}(0,1)$.","Q13: (a),(c),(d) là quy tắc chuyển vị chuẩn. Phép nhân ma trận <b>không giao hoán</b>: ví dụ $M=\\begin{bmatrix}0&1\\\\0&0\\end{bmatrix}$, $N=\\begin{bmatrix}0&0\\\\1&0\\end{bmatrix}$: $MN=\\operatorname{diag}(1,0)\\ne NM=\\operatorname{diag}(0,1)$."),
  ("Q14: <b>isolate $A$</b>: multiply on the right by $P^{-1}$ (allowed since $P$ is invertible): $APP^{-1}=PDP^{-1}\\Rightarrow A=PDP^{-1}$.","Q14: <b>cô lập $A$</b>: nhân bên phải với $P^{-1}$ (được vì $P$ khả nghịch): $APP^{-1}=PDP^{-1}\\Rightarrow A=PDP^{-1}$."),
  ("$A=PDP^{-1}$ is <i>similar</i> to $D$, not equal. Counterexample: $P=\\begin{bmatrix}1&1\\\\0&1\\end{bmatrix}$, $D=\\operatorname{diag}(2,3)$ gives $A=\\begin{bmatrix}2&1\\\\0&3\\end{bmatrix}\\ne D$. So <b>False</b>. (Order matters: $P$ goes on the <i>left</i>, $P^{-1}$ on the <i>right</i>.)","$A=PDP^{-1}$ là ma trận <i>đồng dạng</i> với $D$, không bằng $D$. Phản ví dụ: $P=\\begin{bmatrix}1&1\\\\0&1\\end{bmatrix}$, $D=\\operatorname{diag}(2,3)$ cho $A=\\begin{bmatrix}2&1\\\\0&3\\end{bmatrix}\\ne D$. Vậy <b>Sai</b>. (Thứ tự quan trọng: $P$ bên <i>trái</i>, $P^{-1}$ bên <i>phải</i>.)")],
 mock="Q1, Q17",
 variants=[
  V("★ Compute a power","With the counterexample $A=PDP^{-1}$ compute $A^5$ without multiplying five times.","Với phản ví dụ trên tính $A^5$ mà không nhân 5 lần.","$A^5=\\begin{bmatrix}32&211\\\\0&243\\end{bmatrix}$",
   ("$A^5=PD^5P^{-1}$ (the inner $P^{-1}P$ cancel), $D^5=\\operatorname{diag}(32,243)$.","$A^5=PD^5P^{-1}$ ($P^{-1}P$ ở giữa triệt tiêu), $D^5=\\operatorname{diag}(32,243)$."),
   lambda:(lambda P,D:(P*D*P.inv())**5==Matrix([[32,211],[0,243]]))(Matrix([[1,1],[0,1]]),diag(2,3))),
  V("★★ Which identities hold?","Which are always true for square $A,B$: $(AB)^T=B^TA^T$; $(A+B)^2=A^2+2AB+B^2$; $(AB)^{-1}=B^{-1}A^{-1}$; $\\det(AB)=\\det A\\det B$?","Đẳng thức nào luôn đúng với $A,B$ vuông: $(AB)^T=B^TA^T$; $(A+B)^2=A^2+2AB+B^2$; $(AB)^{-1}=B^{-1}A^{-1}$; $\\det(AB)=\\det A\\det B$?","1st, 3rd (if invertible) and 4th; the 2nd only if $AB=BA$",
   ("Reverse order for transpose and inverse; $\\det$ is multiplicative; the square expands as $A^2+AB+BA+B^2$.","Đảo thứ tự khi chuyển vị và nghịch đảo; $\\det$ nhân tính; bình phương khai triển là $A^2+AB+BA+B^2$."),lambda:True)]))

ITEMS.append(I("2.10","Quiz Ch.2 · Q15, Q16",("Gauss elimination and a matrix equation","Khử Gauss và phương trình ma trận"),
 ("(Q15) Gauss elimination triangularises the system to: upper/lower triangular, diagonal, singular? &nbsp;(Q16) $A=\\begin{bmatrix}-1&2\\\\3&4\\end{bmatrix}$, $B=\\begin{bmatrix}3&-2\\\\1&5\\end{bmatrix}$, $2A+B+X=0$. Find $X$.","(Q15) Khử Gauss đưa hệ về dạng nào? (Q16) $2A+B+X=0$. Tìm $X$."),
 "Q15: upper triangular · Q16: $\\begin{bmatrix}-1&-2\\\\-7&-13\\end{bmatrix}$",
 [("Q15: forward elimination zeroes the entries <i>below</i> the diagonal, leaving an <b>upper triangular</b> matrix; back-substitution then solves from the last row up.","Q15: khử xuôi làm các phần tử <i>dưới</i> đường chéo bằng $0$, còn lại ma trận <b>tam giác trên</b>; thế ngược giải từ hàng cuối lên."),
  ("Q16: <b>isolate $X$</b>: $X=-2A-B$ (move $2A+B$ to the other side: signs change).","Q16: <b>cô lập $X$</b>: $X=-2A-B$ (chuyển $2A+B$ sang vế kia: đổi dấu)."),
  ("$2A=\\begin{bmatrix}-2&4\\\\6&8\\end{bmatrix}$, $2A+B=\\begin{bmatrix}1&2\\\\7&13\\end{bmatrix}$, so $X=\\begin{bmatrix}-1&-2\\\\-7&-13\\end{bmatrix}$.","$2A=\\begin{bmatrix}-2&4\\\\6&8\\end{bmatrix}$, $2A+B=\\begin{bmatrix}1&2\\\\7&13\\end{bmatrix}$, nên $X=\\begin{bmatrix}-1&-2\\\\-7&-13\\end{bmatrix}$.")],
 trap=("Option (d) is $+(2A+B)$: remember the minus sign when isolating.","Đáp án (d) là $+(2A+B)$: nhớ dấu trừ khi cô lập."),
 variants=[
  V("★ Solve $3X-A=2(B+X)$","$A=\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}$, $B=\\begin{bmatrix}1&0\\\\1&1\\end{bmatrix}$. Solve $3X-A=2(B+X)$.","$A=\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}$, $B=\\begin{bmatrix}1&0\\\\1&1\\end{bmatrix}$. Giải $3X-A=2(B+X)$.","$X=A+2B=\\begin{bmatrix}3&2\\\\5&6\\end{bmatrix}$",
   ("Expand: $3X-A=2B+2X$. Collect $X$ on the left: $3X-2X=A+2B$, so $X=A+2B$.","Khai triển: $3X-A=2B+2X$. Gom $X$ về trái: $3X-2X=A+2B$, nên $X=A+2B$."),
   lambda:(lambda A,B:(lambda X:3*X-A==2*(B+X))(A+2*B))(Matrix([[1,2],[3,4]]),Matrix([[1,0],[1,1]]))),
  V("★★ $AX=B$","$A=\\begin{bmatrix}2&1\\\\5&3\\end{bmatrix}$, $B=\\begin{bmatrix}1&0\\\\2&1\\end{bmatrix}$. Solve $AX=B$.","$A=\\begin{bmatrix}2&1\\\\5&3\\end{bmatrix}$, $B=\\begin{bmatrix}1&0\\\\2&1\\end{bmatrix}$. Giải $AX=B$.","$X=A^{-1}B=\\begin{bmatrix}1&-1\\\\-1&2\\end{bmatrix}$",
   ("$\\det A=1$, $A^{-1}=\\begin{bmatrix}3&-1\\\\-5&2\\end{bmatrix}$ multiplies <i>on the left</i>: $X=A^{-1}B$.","$\\det A=1$, $A^{-1}=\\begin{bmatrix}3&-1\\\\-5&2\\end{bmatrix}$ nhân <i>bên trái</i>: $X=A^{-1}B$."),
   lambda:Matrix([[2,1],[5,3]])*Matrix([[1,-1],[-1,2]])==Matrix([[1,0],[2,1]])),
  V("★★★ $XA=B$","Same $A,B$. Solve $XA=B$ (note the side).","Cùng $A,B$. Giải $XA=B$ (chú ý bên nhân).","$X=BA^{-1}=\\begin{bmatrix}3&-1\\\\1&0\\end{bmatrix}$",
   ("Now multiply on the <i>right</i>: $X=BA^{-1}$. Not the same as $A^{-1}B$ because matrices do not commute.","Giờ nhân <i>bên phải</i>: $X=BA^{-1}$. Khác $A^{-1}B$ vì ma trận không giao hoán."),
   lambda:Matrix([[3,-1],[1,0]])*Matrix([[2,1],[5,3]])==Matrix([[1,0],[2,1]]))]))
