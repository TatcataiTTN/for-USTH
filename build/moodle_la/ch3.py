# -*- coding: utf-8 -*-
from .common import *
x,m,a,b,c,t,th,Aa,Bb=symbols('x m a b c t theta A B')
R=Rational
def mat(M,env="pmatrix"): return "\\begin{%s}%s\\end{%s}"%(env," \\\\ ".join(" & ".join(str(latex(e)) for e in M.row(i)) for i in range(M.rows)),env)
D=lambda *r:Matrix(r).det()
ITEMS=[]
ITEMS.append(I("3.1","Quiz Ch.3 · Q2, Q7, Q8, Q9",("Small determinants and $\\det(AB)$, $\\det(cA)$","Định thức nhỏ, $\\det(AB)$, $\\det(cA)$"),
 ("(Q7) $\\det\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}$? (Q2) $A=\\begin{bmatrix}4&0\\\\1&3\\end{bmatrix}$, $B=\\begin{bmatrix}0&2\\\\5&1\\end{bmatrix}$: $\\det(AB)$? (Q8) $A=\\begin{bmatrix}2&3\\\\1&0\\end{bmatrix}$, $B=\\begin{bmatrix}1&4\\\\5&2\\end{bmatrix}$: $\\det(AB)$? (Q9) $A$ is $2\\times2$, $\\det A=-7$: $\\det3A$?","(Q7) $\\det$ của ma trận trên? (Q2) $\\det(AB)$? (Q8) $\\det(AB)$? (Q9) $A$ cỡ $2\\times2$, $\\det A=-7$: $\\det3A$?"),
 "Q7: $-2$ · Q2: $-120$ · Q8: $54$ · Q9: $-63$",
 [("$2\\times2$: $\\det\\begin{bmatrix}a&b\\\\c&d\\end{bmatrix}=ad-bc$. Q7: $1\\cdot4-2\\cdot3=-2$.","$2\\times2$: $\\det\\begin{bmatrix}a&b\\\\c&d\\end{bmatrix}=ad-bc$. Q7: $1\\cdot4-2\\cdot3=-2$."),
  ("<b>Product rule</b> $\\det(AB)=\\det A\\cdot\\det B$ (no need to multiply the matrices). Q2: $\\det A=12$, $\\det B=0-10=-10$ ⇒ $-120$. Q8: $\\det A=0-3=-3$, $\\det B=2-20=-18$ ⇒ $54$.","<b>Quy tắc tích</b> $\\det(AB)=\\det A\\cdot\\det B$ (không cần nhân ma trận). Q2: $\\det A=12$, $\\det B=0-10=-10$ ⇒ $-120$. Q8: $\\det A=0-3=-3$, $\\det B=2-20=-18$ ⇒ $54$."),
  ("<b>Scalar rule</b> $\\det(cA)=c^n\\det A$ for $n\\times n$: every one of the $n$ rows gets a factor $c$. Q9: $n=2$: $3^2(-7)=-63$ (not $3\\cdot(-7)=-21$).","<b>Quy tắc số nhân</b> $\\det(cA)=c^n\\det A$ cho ma trận $n\\times n$: mỗi một trong $n$ hàng đều được nhân $c$. Q9: $n=2$: $3^2(-7)=-63$ (không phải $3\\cdot(-7)=-21$).")],
 trap=("Q9: (a) $-21$ forgets the power $n$.","Q9: (a) $-21$ quên lũy thừa $n$."),
 variants=[
  V("★ Product","$A=\\begin{bmatrix}3&1\\\\2&4\\end{bmatrix}$, $B=\\begin{bmatrix}1&2\\\\0&5\\end{bmatrix}$. $\\det(AB)$ and $\\det(A^2B^{-1})$?","$A=\\begin{bmatrix}3&1\\\\2&4\\end{bmatrix}$, $B=\\begin{bmatrix}1&2\\\\0&5\\end{bmatrix}$. $\\det(AB)$ và $\\det(A^2B^{-1})$?","$50$ and $20$",
   ("$\\det A=10$, $\\det B=5$. $\\det(AB)=50$; $\\det(A^2B^{-1})=\\frac{10^2}5=20$.","$\\det A=10$, $\\det B=5$. $\\det(AB)=50$; $\\det(A^2B^{-1})=\\frac{10^2}5=20$."),
   lambda:(lambda A,B:(A*B).det()==50 and (A*A*B.inv()).det()==20)(Matrix([[3,1],[2,4]]),Matrix([[1,2],[0,5]]))),
  V("★★ Combine all rules","$A$ is $2\\times2$ with $\\det A=-7$. Find $\\det(2A^{-1}A^T)$.","$A$ cỡ $2\\times2$, $\\det A=-7$. Tìm $\\det(2A^{-1}A^T)$.","$4$",
   ("$\\det(2M)=2^2\\det M$, $\\det A^{-1}=-\\frac17$, $\\det A^T=-7$: $4\\cdot(-\\frac17)(-7)=4$.","$\\det(2M)=2^2\\det M$, $\\det A^{-1}=-\\frac17$, $\\det A^T=-7$: $4\\cdot(-\\frac17)(-7)=4$."),
   lambda:4*R(-1,7)*(-7)==4),
  V("★★★ Find the size","$\\det(3A)=243\\det A$ with $\\det A\\ne0$. What is the size $n$?","$\\det(3A)=243\\det A$ với $\\det A\\ne0$. Cỡ $n$ bằng bao nhiêu?","$n=5$",
   ("$3^n=243=3^5$.","$3^n=243=3^5$."),lambda:3**5==243)]))

ITEMS.append(I("3.2","Quiz Ch.3 · Q1",("A determinant as a function","Định thức như một hàm"),
 ("If $f(x)=\\begin{vmatrix}1&2\\\\x&a\\end{vmatrix}$, then $2f(x)-f(2x)$ equals:","Nếu $f(x)=\\begin{vmatrix}1&2\\\\x&a\\end{vmatrix}$ thì $2f(x)-f(2x)$ bằng:"),
 "$a$",
 [("Compute $f$: $f(x)=1\\cdot a-2x=a-2x$. Hence $f(2x)=a-4x$ (replace $x$ by $2x$).","Tính $f$: $f(x)=1\\cdot a-2x=a-2x$. Do đó $f(2x)=a-4x$ (thay $x$ bởi $2x$)."),
  ("$2f(x)-f(2x)=2a-4x-(a-4x)=a$.","$2f(x)-f(2x)=2a-4x-(a-4x)=a$.")],
 variants=[
  V("★ Same","$g(x)=\\begin{vmatrix}x&1\\\\3&x\\end{vmatrix}$. Compute $g(2x)-4g(x)$.","$g(x)=\\begin{vmatrix}x&1\\\\3&x\\end{vmatrix}$. Tính $g(2x)-4g(x)$.","$9$",("$g(x)=x^2-3$, $g(2x)=4x^2-3$; $4x^2-3-4x^2+12=9$.","$g(x)=x^2-3$, $g(2x)=4x^2-3$; $4x^2-3-4x^2+12=9$."),
   lambda:simplify((4*x**2-3)-4*(x**2-3)-9)==0),
  V("★★ Roots","For which $x$ does $\\begin{vmatrix}1&x&x^2\\\\1&2&4\\\\1&3&9\\end{vmatrix}=0$?","Với $x$ nào $\\begin{vmatrix}1&x&x^2\\\\1&2&4\\\\1&3&9\\end{vmatrix}=0$?","$x=2$ or $x=3$",
   ("If $x=2$ or $x=3$ the first row equals a row below it, so $\\det=0$. The determinant is a quadratic in $x$ (Vandermonde): $(x-2)(x-3)$, so no other roots.","Nếu $x=2$ hoặc $x=3$ hàng đầu trùng một hàng dưới nên $\\det=0$. Định thức là đa thức bậc hai theo $x$ (Vandermonde): $(x-2)(x-3)$, nên không còn nghiệm khác."),
   lambda:factor(Matrix([[1,x,x**2],[1,2,4],[1,3,9]]).det())==(x-3)*(x-2))]))

ITEMS.append(I("3.3","Quiz Ch.3 · Q3",("Inverse from a matrix polynomial","Nghịch đảo từ đa thức ma trận"),
 ("$A=\\begin{pmatrix}a-1&1\\\\2+a&1\\end{pmatrix}$ is invertible and $A^2-2A+I=0$. Which matrix is $A^{-1}$?","$A=\\begin{pmatrix}a-1&1\\\\2+a&1\\end{pmatrix}$ khả nghịch và $A^2-2A+I=0$. $A^{-1}$ là ma trận nào?"),
 "$\\begin{pmatrix}3-a&-1\\\\-2-a&1\\end{pmatrix}$",
 [("<b>Isolate $I$:</b> $A^2-2A+I=0\\Rightarrow I=2A-A^2=A(2I-A)$.","<b>Cô lập $I$:</b> $A^2-2A+I=0\\Rightarrow I=2A-A^2=A(2I-A)$."),
  ("A matrix $X$ with $AX=I$ is the inverse, so $A^{-1}=2I-A$ (you never need to know $a$ or invert anything).","Ma trận $X$ với $AX=I$ chính là nghịch đảo, nên $A^{-1}=2I-A$ (không cần biết $a$ hay nghịch đảo gì)."),
  ("$2I-A=\\begin{pmatrix}2-(a-1)&-1\\\\-(2+a)&2-1\\end{pmatrix}=\\begin{pmatrix}3-a&-1\\\\-2-a&1\\end{pmatrix}$.","$2I-A=\\begin{pmatrix}2-(a-1)&-1\\\\-(2+a)&2-1\\end{pmatrix}=\\begin{pmatrix}3-a&-1\\\\-2-a&1\\end{pmatrix}$.")],
 trap=("Direct inversion with the $2\\times2$ formula also works but needs $\\det=-a+1-2-a$… the polynomial trick is shorter.","Nghịch đảo trực tiếp cũng được nhưng dài; mẹo đa thức nhanh hơn."),
 variants=[
  V("★ Another polynomial","$A^2-4A+3I=0$. Express $A^{-1}$.","$A^2-4A+3I=0$. Biểu diễn $A^{-1}$.","$A^{-1}=\\frac13(4I-A)$",("$3I=4A-A^2=A(4I-A)$, then divide by $3$.","$3I=4A-A^2=A(4I-A)$, rồi chia cho $3$."),
   lambda:(lambda A:A*(4*eye(2)-A)/3==eye(2))(Matrix([[2,0],[0,2]])+Matrix([[1,0],[0,-1]])*0+Matrix([[0,0],[0,0]])) or True),
  V("★★★ Nilpotent","$N=\\begin{pmatrix}0&1&0\\\\0&0&1\\\\0&0&0\\end{pmatrix}$, $N^3=0$. Show $(I-N)^{-1}=I+N+N^2$ and write it.","$N$ như trên, $N^3=0$. Chứng minh $(I-N)^{-1}=I+N+N^2$ và viết ra.","$\\begin{pmatrix}1&1&1\\\\0&1&1\\\\0&0&1\\end{pmatrix}$",
   ("$(I-N)(I+N+N^2)=I-N^3=I$.","$(I-N)(I+N+N^2)=I-N^3=I$."),
   lambda:(lambda N:(eye(3)-N)*(eye(3)+N+N*N)==eye(3))(Matrix([[0,1,0],[0,0,1],[0,0,0]])))]))
ITEMS[-1].variants[0].chk=lambda:(lambda A:(A*A-4*A+3*eye(2)).is_zero_matrix and A*(4*eye(2)-A)/3==eye(2))(Matrix([[1,0],[0,3]])) or False
ITEMS[-1].trap=("Direct $2\\times2$ inversion also works but is longer; the polynomial trick avoids $a$ completely.","Nghịch đảo $2\\times2$ trực tiếp cũng được nhưng dài hơn; mẹo đa thức tránh hẳn $a$.")

ITEMS.append(I("3.4","Quiz Ch.3 · Q4",("$\\det(A^2)=64$: solve for $x$","$\\det(A^2)=64$: tìm $x$"),
 ("$A=\\begin{bmatrix}x&2\\\\4&x\\end{bmatrix}$ and $\\det(A^2)=64$. Find $x$.","$A=\\begin{bmatrix}x&2\\\\4&x\\end{bmatrix}$ và $\\det(A^2)=64$. Tìm $x$."),
 "$\\pm4$ (also $x=0$, see note)",
 [("$\\det(A^2)=(\\det A)^2$ and $\\det A=x^2-8$. So $(x^2-8)^2=64$.","$\\det(A^2)=(\\det A)^2$ và $\\det A=x^2-8$. Nên $(x^2-8)^2=64$."),
  ("Take square roots <b>with both signs</b>: $x^2-8=8$ or $x^2-8=-8$. First: $x^2=16\\Rightarrow x=\\pm4$. Second: $x^2=0\\Rightarrow x=0$.","Khai căn <b>cả hai dấu</b>: $x^2-8=8$ hoặc $x^2-8=-8$. Trường hợp 1: $x^2=16\\Rightarrow x=\\pm4$. Trường hợp 2: $x^2=0\\Rightarrow x=0$.")],
 choices=["$\\pm2$","$\\pm5$","$\\pm4$","$\\pm3$"],
 note=("Strictly the full solution set is $\\{-4,0,4\\}$ ($x=0$ gives $\\det A=-8$, $\\det A^2=64$). The question only lists $\\pm4$ among the options, so (c) is the best answer — but on a free-response question you must include $0$.","Chặt chẽ thì tập nghiệm là $\\{-4,0,4\\}$ ($x=0$ cho $\\det A=-8$, $\\det A^2=64$). Đề chỉ có $\\pm4$ trong các lựa chọn nên chọn (c) — nhưng ở bài tự luận phải ghi thêm $x=0$."),mock="Q8",
 variants=[
  V("★ Similar","$A=\\begin{bmatrix}x&1\\\\1&x\\end{bmatrix}$, $\\det(A^2)=9$. Real $x$?","$A=\\begin{bmatrix}x&1\\\\1&x\\end{bmatrix}$, $\\det(A^2)=9$. $x$ thực?","$x=\\pm2$",("$(x^2-1)^2=9\\Rightarrow x^2-1=3$ ($x=\\pm2$) or $x^2-1=-3$ ($x^2=-2$, no real $x$).","$(x^2-1)^2=9\\Rightarrow x^2-1=3$ ($x=\\pm2$) hoặc $x^2-1=-3$ ($x^2=-2$, không có $x$ thực)."),
   lambda:set(solve((x**2-1)**2-9,x,dict=False))>={2,-2} and not any(im(s)==0 and s not in (2,-2) for s in solve((x**2-1)**2-9,x))),
  V("★★ Determinant of 3×3 scaling","$A$ is $3\\times3$, $\\det(2A)=-40$. Find $\\det A$ and $\\det(A^{-1})$.","$A$ cỡ $3\\times3$, $\\det(2A)=-40$. Tìm $\\det A$ và $\\det(A^{-1})$.","$\\det A=-5$, $\\det A^{-1}=-\\frac15$",("$2^3\\det A=-40$.","$2^3\\det A=-40$."),lambda:-40/8==-5)]))

ITEMS.append(I("3.5","Quiz Ch.3 · Q5, Q14, Q13",("Dependent rows ⇒ $\\det=0$","Hàng phụ thuộc ⇒ $\\det=0$"),
 ("(Q5) $\\det\\begin{pmatrix}x-a&y-b&z-c\\\\x&y&z\\\\a&b&c\\end{pmatrix}$? (Q14) $\\det\\begin{bmatrix}-3&6&9\\\\6&9&12\\\\9&12&15\\end{bmatrix}$? (Q13) $A=\\begin{pmatrix}a&1&2\\\\1&a&2\\\\2&2&4\\end{pmatrix}$ singular ⇒ $a=$?","(Q5) $\\det$ của ma trận trên? (Q14) $\\det$? (Q13) $A$ suy biến ⇒ $a=$?"),
 "Q5: $0$ · Q14: $54$ · Q13: $1$",
 [("Q5: Row 1 $=$ Row 2 $-$ Row 3: one row is a combination of the others ⇒ $\\det=0$. (Or do $R_1\\leftarrow R_1-R_2+R_3=0$: a zero row.)","Q5: Hàng 1 $=$ hàng 2 $-$ hàng 3: một hàng là tổ hợp của các hàng khác ⇒ $\\det=0$. (Hoặc $R_1\\leftarrow R_1-R_2+R_3=0$: hàng toàn 0.)"),
  ("Q14: factor $3$ out of <b>each of the three rows</b>: $27\\det\\begin{bmatrix}-1&2&3\\\\2&3&4\\\\3&4&5\\end{bmatrix}$. Expand: $-1(15-16)-2(10-12)+3(8-9)=1+4-3=2$. So $27\\cdot2=54$.","Q14: đặt $3$ ra khỏi <b>cả ba hàng</b>: $27\\det\\begin{bmatrix}-1&2&3\\\\2&3&4\\\\3&4&5\\end{bmatrix}$. Khai triển: $-1(15-16)-2(10-12)+3(8-9)=1+4-3=2$. Vậy $27\\cdot2=54$."),
  ("Q13: singular ⇔ $\\det=0$. $\\det A=4(a-1)^2$ (e.g. $R_3-2R_2$ and expand), zero only for $a=1$. At $a=1$ rows 1 and 2 are equal.","Q13: suy biến ⇔ $\\det=0$. $\\det A=4(a-1)^2$ (ví dụ $R_3-2R_2$ rồi khai triển), bằng 0 chỉ khi $a=1$. Tại $a=1$ hàng 1 và 2 trùng nhau.")],
 variants=[
  V("★ Dependent rows","$\\det\\begin{pmatrix}1&1&1\\\\a&b&c\\\\b+c&c+a&a+b\\end{pmatrix}$?","$\\det\\begin{pmatrix}1&1&1\\\\a&b&c\\\\b+c&c+a&a+b\\end{pmatrix}$?","$0$",("Row 3 $=(a+b+c)\\cdot$Row 1 $-$ Row 2.","Hàng 3 $=(a+b+c)\\cdot$ hàng 1 $-$ hàng 2."),
   lambda:Matrix([[1,1,1],[a,b,c],[b+c,c+a,a+b]]).det().expand()==0),
  V("★★ Singular family","For which $a$ is $\\begin{pmatrix}a&1&1\\\\1&a&1\\\\1&1&a\\end{pmatrix}$ singular? Give the rank in each case.","Với $a$ nào ma trận trên suy biến? Cho hạng mỗi trường hợp.","$a=1$ (rank 1), $a=-2$ (rank 2)",("$\\det=(a-1)^2(a+2)$. At $a=1$ all rows equal ⇒ rank 1; at $a=-2$ rows sum to $0$ but two are independent ⇒ rank 2.","$\\det=(a-1)^2(a+2)$. Tại $a=1$ ba hàng bằng nhau ⇒ hạng 1; tại $a=-2$ tổng ba hàng bằng $0$ nhưng hai hàng độc lập ⇒ hạng 2."),
   lambda:(lambda M:factor(M.det())==(a-1)**2*(a+2) and M.subs(a,1).rank()==1 and M.subs(a,-2).rank()==2)(Matrix([[a,1,1],[1,a,1],[1,1,a]]))),
  V("★★★ Parameter $q$","For which $p$ is $\\begin{pmatrix}2&p\\\\3&6\\end{pmatrix}$ singular?","Với $p$ nào $\\begin{pmatrix}2&p\\\\3&6\\end{pmatrix}$ suy biến?","$p=4$",("$12-3p=0$.","$12-3p=0$."),lambda:Matrix([[2,4],[3,6]]).det()==0)]))

ITEMS.append(I("3.6","Quiz Ch.3 · Q6",("A $4\\times4$ determinant with $x^2$","Định thức $4\\times4$ chứa $x^2$"),
 ("$\\det A$ for $A=\\begin{pmatrix}1&1&2&3\\\\1&2-x^2&2&3\\\\2&3&1&5\\\\3&3&1&9-x^2\\end{pmatrix}$.","$\\det A$ với $A$ như trên."),
 "$-3x^4+8x^2-5$",
 [("Create zeros in column 1 (row operations of the type $R_i-cR_1$ do not change $\\det$): $R_2-R_1=(0,\\,1-x^2,\\,0,\\,0)$, $R_3-2R_1=(0,1,-3,-1)$, $R_4-3R_1=(0,0,-5,-x^2)$.","Tạo số $0$ ở cột 1 (phép $R_i-cR_1$ không đổi $\\det$): $R_2-R_1=(0,\\,1-x^2,\\,0,\\,0)$, $R_3-2R_1=(0,1,-3,-1)$, $R_4-3R_1=(0,0,-5,-x^2)$."),
  ("Expand along column 1: $\\det=1\\cdot\\det\\begin{pmatrix}1-x^2&0&0\\\\1&-3&-1\\\\0&-5&-x^2\\end{pmatrix}$. Expand along its first row: $(1-x^2)\\big[(-3)(-x^2)-(-1)(-5)\\big]=(1-x^2)(3x^2-5)$.","Khai triển theo cột 1: $\\det=1\\cdot\\det\\begin{pmatrix}1-x^2&0&0\\\\1&-3&-1\\\\0&-5&-x^2\\end{pmatrix}$. Khai triển theo hàng đầu: $(1-x^2)\\big[(-3)(-x^2)-(-1)(-5)\\big]=(1-x^2)(3x^2-5)$."),
  ("Multiply out: $3x^2-5-3x^4+5x^2=-3x^4+8x^2-5$.","Nhân ra: $3x^2-5-3x^4+5x^2=-3x^4+8x^2-5$.")],
 variants=[
  V("★ Block structure","$\\det\\begin{pmatrix}x&1&0&0\\\\1&x&0&0\\\\0&0&x&1\\\\0&0&1&x\\end{pmatrix}$?","$\\det$ của ma trận khối trên?","$(x^2-1)^2$",("Block diagonal: $\\det=\\det B_1\\cdot\\det B_2=(x^2-1)(x^2-1)$.","Ma trận khối chéo: $\\det=\\det B_1\\cdot\\det B_2=(x^2-1)(x^2-1)$."),
   lambda:factor(Matrix([[x,1,0,0],[1,x,0,0],[0,0,x,1],[0,0,1,x]]).det())==(x-1)**2*(x+1)**2),
  V("★★ When is it zero?","For which $x$ is the matrix in the question singular?","Với $x$ nào ma trận ở câu hỏi suy biến?","$x=\\pm1$ and $x=\\pm\\sqrt{5/3}$",("$(1-x^2)(3x^2-5)=0$.","$(1-x^2)(3x^2-5)=0$."),
   lambda:set(solve((1-x**2)*(3*x**2-5),x))=={1,-1,sqrt(R(5,3)),-sqrt(R(5,3))})]))

ITEMS.append(I("3.7","Quiz Ch.3 · Q15, Q16",("$\\det(cA)$ with numbers","$\\det(cA)$ bằng số"),
 ("(Q15) $A$ is $3\\times3$, $\\det A=-27$. $\\det\\left(\\frac13A\\right)$? (Q16) $A=\\begin{bmatrix}4&7&1\\\\-1&3&2\\\\-2&0&5\\end{bmatrix}$. $\\det(3A)$?","(Q15) $A$ cỡ $3\\times3$, $\\det A=-27$. $\\det\\left(\\frac13A\\right)$? (Q16) $\\det(3A)$?"),
 "Q15: $-1$ · Q16: $1971$",
 [("Q15: $\\det(cA)=c^n\\det A$ with $n=3$, $c=\\frac13$: $\\left(\\frac13\\right)^3(-27)=\\frac1{27}(-27)=-1$.","Q15: $\\det(cA)=c^n\\det A$ với $n=3$, $c=\\frac13$: $\\left(\\frac13\\right)^3(-27)=\\frac1{27}(-27)=-1$."),
  ("Q16: first $\\det A$ by expansion on row 1: $4(15-0)-7(-5+4)+1(0+6)=60+7+6=73$.","Q16: trước hết $\\det A$ khai triển hàng 1: $4(15-0)-7(-5+4)+1(0+6)=60+7+6=73$."),
  ("Then $\\det(3A)=3^3\\cdot73=27\\cdot73=1971$ ✓.","Rồi $\\det(3A)=3^3\\cdot73=27\\cdot73=1971$ ✓.")],
 variants=[
  V("★ Four by four","$A$ is $4\\times4$, $\\det A=32$. Find $\\det(\\tfrac12A)$ and $\\det(-A)$.","$A$ cỡ $4\\times4$, $\\det A=32$. Tìm $\\det(\\tfrac12A)$ và $\\det(-A)$.","$2$ and $32$",("$(\\tfrac12)^4\\cdot32=2$; $(-1)^4\\cdot32=32$ (even size: $\\det(-A)=\\det A$).","$(\\tfrac12)^4\\cdot32=2$; $(-1)^4\\cdot32=32$ (cỡ chẵn: $\\det(-A)=\\det A$)."),lambda:R(1,16)*32==2),
  V("★★ Odd size","$A$ is $3\\times3$ with $A^T=-A$. Show $\\det A=0$.","$A$ cỡ $3\\times3$ với $A^T=-A$. Chứng minh $\\det A=0$.","$\\det A=0$",("$\\det A=\\det A^T=\\det(-A)=(-1)^3\\det A=-\\det A$ ⇒ $2\\det A=0$.","$\\det A=\\det A^T=\\det(-A)=(-1)^3\\det A=-\\det A$ ⇒ $2\\det A=0$."),
   lambda:Matrix([[0,1,-2],[-1,0,3],[2,-3,0]]).det()==0)]))

ITEMS.append(I("3.8","Quiz Ch.3 · Q10",("Use $\\det A=0$ to find $m$","Dùng $\\det A=0$ để tìm $m$"),
 ("$A=\\begin{pmatrix}1&m&2\\\\-2&0&1\\\\1&1&-3\\end{pmatrix}$, $B=\\begin{pmatrix}1&2&3\\\\0&1&0\\\\m&1&1\\end{pmatrix}$. If $\\det A=0$, what is $\\det B$?","$A,B$ như trên. Nếu $\\det A=0$ thì $\\det B$ bằng?"),
 "$4$",
 [("<b>Isolate $m$:</b> expand $\\det A$ along row 1: $1(0-1)-m(6-1)+2(-2-0)=-1-5m-4=-5m-5$. Set to $0$: $m=-1$.","<b>Cô lập $m$:</b> khai triển $\\det A$ theo hàng 1: $1(0-1)-m(6-1)+2(-2-0)=-1-5m-4=-5m-5$. Cho bằng $0$: $m=-1$."),
  ("$B$ has a row of the form $(0,1,0)$: expand along row 2: $\\det B=1\\cdot\\det\\begin{pmatrix}1&3\\\\m&1\\end{pmatrix}=1-3m$.","$B$ có hàng $(0,1,0)$: khai triển theo hàng 2: $\\det B=1\\cdot\\det\\begin{pmatrix}1&3\\\\m&1\\end{pmatrix}=1-3m$."),
  ("With $m=-1$: $\\det B=1+3=4$.","Với $m=-1$: $\\det B=1+3=4$.")],
 variants=[
  V("★ Find the parameter","$\\begin{pmatrix}1&m&1\\\\2&1&3\\\\1&1&2\\end{pmatrix}$ is singular. Find $m$.","$\\begin{pmatrix}1&m&1\\\\2&1&3\\\\1&1&2\\end{pmatrix}$ suy biến. Tìm $m$.","$m=0$",("$\\det=1(2-3)-m(4-3)+1(2-1)=-m$.","$\\det=1(2-3)-m(4-3)+1(2-1)=-m$."),lambda:Matrix([[1,m,1],[2,1,3],[1,1,2]]).det()==-m),
  V("★★ Chain","$\\det\\begin{pmatrix}2&m\\\\3&6\\end{pmatrix}=0$. Then find $\\det\\begin{pmatrix}m&1\\\\1&m\\end{pmatrix}$.","$\\det\\begin{pmatrix}2&m\\\\3&6\\end{pmatrix}=0$. Khi đó tìm $\\det\\begin{pmatrix}m&1\\\\1&m\\end{pmatrix}$.","$15$",("$12-3m=0\\Rightarrow m=4$; $m^2-1=15$.","$12-3m=0\\Rightarrow m=4$; $m^2-1=15$."),lambda:16-1==15)]))

ITEMS.append(I("3.9","Quiz Ch.3 · Q11",("A structured $3\\times3$ determinant","Định thức $3\\times3$ có cấu trúc"),
 ("$\\det\\begin{pmatrix}a&a&a+b\\\\a&a+b&a\\\\a+b&a&a\\end{pmatrix}$.","Tính $\\det$ của ma trận trên."),
 "$-b^2(3a+b)$",
 [("Every column sums to $3a+b$. <b>Add columns 2 and 3 to column 1</b> (does not change $\\det$) and factor $(3a+b)$ out of column 1: $(3a+b)\\det\\begin{pmatrix}1&a&a+b\\\\1&a+b&a\\\\1&a&a\\end{pmatrix}$.","Mỗi cột có tổng $3a+b$. <b>Cộng cột 2 và 3 vào cột 1</b> (không đổi $\\det$) rồi đặt $(3a+b)$ ra khỏi cột 1: $(3a+b)\\det\\begin{pmatrix}1&a&a+b\\\\1&a+b&a\\\\1&a&a\\end{pmatrix}$."),
  ("$R_2-R_1=(0,b,-b)$, $R_3-R_1=(0,0,-b)$: triangular with diagonal $1,b,-b$, determinant $-b^2$.","$R_2-R_1=(0,b,-b)$, $R_3-R_1=(0,0,-b)$: tam giác với đường chéo $1,b,-b$, định thức $-b^2$."),
  ("Result: $(3a+b)(-b^2)=-b^2(3a+b)$.","Kết quả: $(3a+b)(-b^2)=-b^2(3a+b)$.")],
 variants=[
  V("★ Equal off-diagonal","$\\det\\begin{pmatrix}a&b&b\\\\b&a&b\\\\b&b&a\\end{pmatrix}$.","$\\det$ của ma trận trên.","$(a-b)^2(a+2b)$",("Row sums are $a+2b$; add columns to column 1, then subtract row 1.","Tổng mỗi hàng $a+2b$; cộng các cột vào cột 1, rồi trừ hàng 1."),
   lambda:factor(Matrix([[a,b,b],[b,a,b],[b,b,a]]).det())==(a-b)**2*(a+2*b)),
  V("★★ When singular?","For which $(a,b)$ is the matrix of the question singular?","Với $(a,b)$ nào ma trận trong câu hỏi suy biến?","$b=0$ or $3a+b=0$",("$-b^2(3a+b)=0$.","$-b^2(3a+b)=0$."),lambda:factor(Matrix([[a,a,a+b],[a,a+b,a],[a+b,a,a]]).det())==-b**2*(3*a+b))]))

ITEMS.append(I("3.10","Quiz Ch.3 · Q12",("Trigonometric determinant","Định thức lượng giác"),
 ("If $\\begin{vmatrix}\\cos(A+B)&-\\sin(A+B)&\\cos2B\\\\\\sin A&\\cos A&\\sin B\\\\-\\cos A&\\sin A&\\cos B\\end{vmatrix}=0$, then $B=$?","Nếu định thức trên bằng $0$ thì $B=$?"),
 "$(2n+1)\\frac\\pi2,\\ n\\in\\mathbb Z$",
 [("Expand along row 1. The three minors are: $\\cos A\\cos B-\\sin B\\sin A=\\cos(A+B)$; $\\sin A\\cos B+\\cos A\\sin B=\\sin(A+B)$; $\\sin^2A+\\cos^2A=1$.","Khai triển theo hàng 1. Ba định thức con: $\\cos A\\cos B-\\sin B\\sin A=\\cos(A+B)$; $\\sin A\\cos B+\\cos A\\sin B=\\sin(A+B)$; $\\sin^2A+\\cos^2A=1$."),
  ("$\\det=\\cos(A+B)\\cos(A+B)-(-\\sin(A+B))\\sin(A+B)+\\cos2B\\cdot1=\\cos^2+\\sin^2+\\cos2B=1+\\cos2B$.","$\\det=\\cos(A+B)\\cos(A+B)-(-\\sin(A+B))\\sin(A+B)+\\cos2B\\cdot1=\\cos^2+\\sin^2+\\cos2B=1+\\cos2B$."),
  ("$1+\\cos2B=0\\Rightarrow\\cos2B=-1\\Rightarrow2B=\\pi+2n\\pi\\Rightarrow B=(2n+1)\\frac\\pi2$. (Also $1+\\cos2B=2\\cos^2B$, zero iff $\\cos B=0$.)","$1+\\cos2B=0\\Rightarrow\\cos2B=-1\\Rightarrow2B=\\pi+2n\\pi\\Rightarrow B=(2n+1)\\frac\\pi2$. (Cũng có $1+\\cos2B=2\\cos^2B$, bằng $0$ iff $\\cos B=0$.)")],
 mock="Q15",
 trap=("The result does not depend on $A$ — a sign that the computation is right (identities cancel $A$).","Kết quả không phụ thuộc $A$ — dấu hiệu tính đúng (các đồng nhất thức triệt tiêu $A$)."),
 variants=[
  V("★ Rotation","$\\det\\begin{pmatrix}\\cos\\theta&-\\sin\\theta\\\\\\sin\\theta&\\cos\\theta\\end{pmatrix}$ and $\\det\\begin{pmatrix}\\cos\\theta&\\sin\\theta\\\\\\sin\\theta&-\\cos\\theta\\end{pmatrix}$.","Tính hai định thức trên.","$1$ and $-1$",("$\\cos^2+\\sin^2=1$; $-\\cos^2-\\sin^2=-1$ (rotation vs reflection).","$\\cos^2+\\sin^2=1$; $-\\cos^2-\\sin^2=-1$ (phép quay và phép đối xứng)."),
   lambda:simplify(Matrix([[cos(th),-sin(th)],[sin(th),cos(th)]]).det()-1)==0 and simplify(Matrix([[cos(th),sin(th)],[sin(th),-cos(th)]]).det()+1)==0),
  V("★★ Solve","Solve $\\begin{vmatrix}\\cos B&\\sin B\\\\\\sin B&\\cos B\\end{vmatrix}=0$ for $B\\in[0,2\\pi)$.","Giải $\\begin{vmatrix}\\cos B&\\sin B\\\\\\sin B&\\cos B\\end{vmatrix}=0$ với $B\\in[0,2\\pi)$.","$B=\\frac\\pi4,\\frac{3\\pi}4,\\frac{5\\pi}4,\\frac{7\\pi}4$",("$\\cos^2B-\\sin^2B=\\cos2B=0\\Rightarrow2B=\\frac\\pi2+k\\pi$.","$\\cos^2B-\\sin^2B=\\cos2B=0\\Rightarrow2B=\\frac\\pi2+k\\pi$."),
   lambda:all(abs(cos(v)**2-sin(v)**2)<1e-12 for v in [pi/4,3*pi/4,5*pi/4,7*pi/4]))]))

ITEMS.append(I("3.11","Quiz Ch.3 · Q17",("Symmetric $A$: which has $\\det=0$?","$A$ đối xứng: biểu thức nào có $\\det=0$?"),
 ("If $A$ is symmetric, which has $\\det=0$? (a) $AA^T$ (b) $A-A^T$ (c) $A\\cdot A$ (d) $A^n$.","Nếu $A$ đối xứng, biểu thức nào có $\\det=0$?"),
 "(b) $A-A^T$",
 [("Symmetric means $A^T=A$. Then $A-A^T=A-A=\\mathbf 0$, the zero matrix, whose determinant is $0$.","Đối xứng nghĩa là $A^T=A$. Khi đó $A-A^T=A-A=\\mathbf 0$, ma trận không, có định thức $0$."),
  ("The others: $\\det(AA^T)=(\\det A)^2$, $\\det(A^2)=(\\det A)^2$, $\\det A^n=(\\det A)^n$: zero only if $\\det A=0$, which is not given.","Các cái còn lại: $\\det(AA^T)=(\\det A)^2$, $\\det(A^2)=(\\det A)^2$, $\\det A^n=(\\det A)^n$: bằng $0$ chỉ khi $\\det A=0$, đề không cho.")],
 variants=[
  V("★ Skew part","For any square $A$, show $A-A^T$ is skew-symmetric. For $A=\\begin{bmatrix}1&2\\\\5&3\\end{bmatrix}$ compute $A-A^T$ and its determinant.","Với $A=\\begin{bmatrix}1&2\\\\5&3\\end{bmatrix}$ tính $A-A^T$ và định thức của nó.","$\\begin{bmatrix}0&-3\\\\3&0\\end{bmatrix}$, $\\det=9$",("$(A-A^T)^T=A^T-A=-(A-A^T)$. Here $\\det=0\\cdot0-(-3)(3)=9$. For an <i>even</i> size the determinant need not be $0$ (odd size: always $0$).","$(A-A^T)^T=A^T-A=-(A-A^T)$. Ở đây $\\det=0\\cdot0-(-3)(3)=9$. Với cỡ <i>chẵn</i> định thức không nhất thiết bằng $0$ (cỡ lẻ: luôn bằng $0$)."),
   lambda:(lambda A:(A-A.T).det()==9)(Matrix([[1,2],[5,3]])))]))
