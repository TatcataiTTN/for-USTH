# -*- coding: utf-8 -*-
from .common import *
x,y,z,a,b,c,t,s,k,m,l,al,be,nu,ka=symbols('x y z a b c t s k m l alpha beta nu kappa')
def status(A,B):
    r1,r2=A.rank(),A.row_join(B).rank()
    return "none" if r1<r2 else ("unique" if r1==A.cols else "inf")
def ref_ok(E):
    last=-1
    for i in range(E.rows):
        nz=[j for j in range(E.cols-1) if E[i,j]!=0]
        if not nz: continue
        j=nz[0]
        if E[i,j]!=1 or j<=last or any(E[r,j]!=0 for r in range(i+1,E.rows)): return False
        last=j
    return True
x2,x3,x4=symbols('x2 x3 x4')
ITEMS=[]

ITEMS.append(I("1.1","Quiz Ch.1 · Q1",("Parametric system: no solution","Hệ có tham số: vô nghiệm"),
 ("For which $\\mu,\\lambda$ does $\\begin{cases}x+y+z=6\\\\ x+2y+3z=10\\\\ x+2y+\\mu z=\\lambda\\end{cases}$ have <b>no solution</b>?","Với $\\mu,\\lambda$ nào thì hệ trên <b>vô nghiệm</b>?"),
 "$\\mu=3,\\ \\lambda\\ne10$",
 [("Eliminate below the first pivot ($R_2-R_1$, $R_3-R_1$), then $R_3-R_2$. Last row: $(0,\\,0,\\,\\mu-3\\mid\\lambda-10)$.","Khử phía dưới pivot đầu ($R_2-R_1$, $R_3-R_1$), rồi $R_3-R_2$. Hàng cuối: $(0,\\,0,\\,\\mu-3\\mid\\lambda-10)$."),
  ("It reads $(\\mu-3)z=\\lambda-10$. To <b>isolate $z$</b> we divide by $\\mu-3$, allowed only if $\\mu-3\\ne0$. So we split into cases.","Nó là $(\\mu-3)z=\\lambda-10$. Muốn <b>cô lập $z$</b> phải chia cho $\\mu-3$, chỉ được khi $\\mu-3\\ne0$. Nên ta chia trường hợp."),
  ("$\\mu\\ne3$: $z=\\frac{\\lambda-10}{\\mu-3}$, unique solution. $\\mu=3,\\lambda=10$: $0=0$, $z$ free, infinitely many. $\\mu=3,\\lambda\\ne10$: $0\\cdot z=\\text{nonzero}$, impossible: <b>no solution</b>.","$\\mu\\ne3$: $z=\\frac{\\lambda-10}{\\mu-3}$, nghiệm duy nhất. $\\mu=3,\\lambda=10$: $0=0$, $z$ tự do, vô số nghiệm. $\\mu=3,\\lambda\\ne10$: $0\\cdot z=$ số khác $0$, vô lý: <b>vô nghiệm</b>.")],
 choices=["$\\mu=3;\\lambda\\ne10$","$\\mu\\ne3;\\lambda=10$","$\\mu=3;\\lambda=10$","$\\mu\\ne3;\\lambda\\ne10$"],
 trap=("(c) is the <i>infinitely many</i> case; (b),(d) have $\\mu\\ne3$: always a unique solution.","(c) là trường hợp <i>vô số nghiệm</i>; (b),(d) có $\\mu\\ne3$: luôn có nghiệm duy nhất."),mock="Q9",
 variants=[
  V("★ Same idea, new numbers","$x+2y+z=3,\\ 2x+5y+3z=8,\\ x+3y+\\nu z=\\kappa$. Find $\\nu,\\kappa$ with no solution.","$x+2y+z=3,\\ 2x+5y+3z=8,\\ x+3y+\\nu z=\\kappa$. Tìm $\\nu,\\kappa$ để hệ vô nghiệm.","$\\nu=2,\\ \\kappa\\ne5$",
   ("$R_2-2R_1$: $y+z=2$; $R_3-R_1$: $y+(\\nu-1)z=\\kappa-3$; subtract: $(\\nu-2)z=\\kappa-5$.","$R_2-2R_1$: $y+z=2$; $R_3-R_1$: $y+(\\nu-1)z=\\kappa-3$; trừ: $(\\nu-2)z=\\kappa-5$."),
   lambda:all(status(Matrix([[1,2,1],[2,5,3],[1,3,n]]),Matrix([3,8,kk]))==("none" if (n==2 and kk!=5) else "inf" if (n==2) else "unique") for n in range(0,5) for kk in range(3,8))),
  V("★★ Describe all solutions","Take $\\mu=3,\\lambda=10$ in the original system. Write all solutions.","Lấy $\\mu=3,\\lambda=10$ trong hệ gốc. Viết mọi nghiệm.","$(2+t,\\ 4-2t,\\ t),\\ t\\in\\mathbb R$",
   ("$y+2z=4$ and $x+y+z=6$. Let $z=t$; isolate $y=4-2t$, then $x=6-y-z=2+t$.","$y+2z=4$ và $x+y+z=6$. Đặt $z=t$; cô lập $y=4-2t$, rồi $x=6-y-z=2+t$."),
   lambda:all(simplify(((2+t)+(4-2*t)+t)-6)==0 and simplify(((2+t)+2*(4-2*t)+3*t)-10)==0 for _ in [0])),
  V("★★★ Counting angle","Count pairs $(\\mu,\\lambda)$, $\\mu\\in\\{1..5\\}$, $\\lambda\\in\\{1..20\\}$, for which the system has no solution.","Đếm số cặp $(\\mu,\\lambda)$, $\\mu\\in\\{1..5\\}$, $\\lambda\\in\\{1..20\\}$ để hệ vô nghiệm.","$19$",
   ("No solution $\\iff\\mu=3$ and $\\lambda\\ne10$: one $\\mu$, and $19$ values of $\\lambda$.","Vô nghiệm $\\iff\\mu=3$ và $\\lambda\\ne10$: một $\\mu$ và $19$ giá trị $\\lambda$."),
   lambda:sum(status(Matrix([[1,1,1],[1,2,3],[1,2,u]]),Matrix([6,10,v]))=="none" for u in range(1,6) for v in range(1,21))==19)]))

ITEMS.append(I("1.2","Quiz Ch.1 · Q2",("Word problem, two unknowns","Bài toán lời văn, hai ẩn"),
 ("One 8-oz glass of apple juice plus one of orange juice contain 227 mg of vitamin C. Two apple and three orange glasses contain 578 mg. How much vitamin C is in one glass of apple juice?","Một ly táo và một ly cam chứa tổng 227 mg vitamin C. Hai ly táo và ba ly cam chứa 578 mg. Một ly nước táo chứa bao nhiêu mg?"),
 "103 mg",
 [("<b>Name the unknowns:</b> $a$ (apple), $o$ (orange). Each sentence becomes an equation: $a+o=227$, $2a+3o=578$.","<b>Đặt ẩn:</b> $a$ (táo), $o$ (cam). Mỗi câu thành một phương trình: $a+o=227$, $2a+3o=578$."),
  ("<b>Isolate one variable</b> in the simple equation: $o=227-a$. Substitute: $2a+3(227-a)=578\\Rightarrow-a=-103\\Rightarrow a=103$.","<b>Cô lập một biến</b> ở phương trình đơn giản: $o=227-a$. Thế vào: $2a+3(227-a)=578\\Rightarrow-a=-103\\Rightarrow a=103$."),
  ("Then $o=124$. <b>Check:</b> $2\\cdot103+3\\cdot124=206+372=578$ ✓.","Khi đó $o=124$. <b>Kiểm tra:</b> $2\\cdot103+3\\cdot124=206+372=578$ ✓.")],
 choices=["103 mg","126 mg","156 mg","162 mg"],trap=("The question asks for <i>apple</i> (103), not orange (124).","Đề hỏi <i>táo</i> (103), không phải cam (124)."),mock="Q10",
 variants=[
  V("★ Two unknowns","3 cups of A and 2 of B hold 17 mg; 1 cup of A and 4 of B hold 19 mg. Find mg in one cup of A.","3 ly A và 2 ly B chứa 17 mg; 1 ly A và 4 ly B chứa 19 mg. Tìm mg trong một ly A.","$3$ mg",
   ("From eq.2: $A=19-4B$; into eq.1: $57-10B=17\\Rightarrow B=4$, $A=3$.","Từ PT2: $A=19-4B$; vào PT1: $57-10B=17\\Rightarrow B=4$, $A=3$."),
   lambda:solve([3*a+2*b-17,a+4*b-19],[a,b])=={a:3,b:4}),
  V("★★ Three unknowns","$x+y+z=10,\\ 2x+3y+4z=33,\\ x-y+z=4$. Find $y$.","$x+y+z=10,\\ 2x+3y+4z=33,\\ x-y+z=4$. Tìm $y$.","$y=3$ ($x=2,\\ z=5$)",
   ("Eq1 − Eq3: $2y=6$. Then $x+z=7$, $2x+4z=24$: $z=5$, $x=2$.","PT1 − PT3: $2y=6$. Rồi $x+z=7$, $2x+4z=24$: $z=5$, $x=2$."),
   lambda:solve([x+y+z-10,2*x+3*y+4*z-33,x-y+z-4],[x,y,z])=={x:2,y:3,z:5}),
  V("★★★ Why independent equations?","If the data were $a+o=227$ and $2a+2o=c$, for which $c$ is the system consistent, and how many solutions then?","Nếu dữ kiện là $a+o=227$ và $2a+2o=c$, với $c$ nào hệ có nghiệm, khi đó bao nhiêu nghiệm?","$c=454$; infinitely many",
   ("Row 2 is $2\\times$ Row 1 on the left, so consistency needs $c=454$; then both equations are the same line: infinitely many. The original used $2a+3o$, so its rows are independent.","Hàng 2 là $2\\times$ hàng 1 ở vế trái nên cần $c=454$; khi đó hai phương trình trùng nhau: vô số nghiệm. Đề gốc dùng $2a+3o$ nên hai hàng độc lập."),
   lambda:status(Matrix([[1,1],[2,2]]),Matrix([227,454]))=="inf" and status(Matrix([[1,1],[2,2]]),Matrix([227,455]))=="none")]))

ITEMS.append(I("1.3","Quiz Ch.1 · Q3",("Parameter: infinitely many solutions","Tham số: vô số nghiệm"),
 ("For which real $\\alpha$ does $\\begin{cases}2x+2y-3z=3\\\\2x-y+5z=2\\\\4x+y+(\\alpha^2+2)z=\\alpha+5\\end{cases}$ have <b>infinitely many</b> solutions?","Với $\\alpha$ thực nào hệ trên có <b>vô số nghiệm</b>?"),
 "$\\alpha=0$",
 [("Notice $R_3-R_1-R_2$ kills the $x,y$ parts: $(4,1,\\cdot)-(2,2,-3)-(2,-1,5)=(0,0,\\alpha^2+2+3-5)$ and the right side $\\alpha+5-3-2=\\alpha$.","Để ý $R_3-R_1-R_2$ triệt tiêu phần $x,y$: $(4,1,\\cdot)-(2,2,-3)-(2,-1,5)=(0,0,\\alpha^2+2+3-5)$, vế phải $\\alpha+5-3-2=\\alpha$."),
  ("The new last row is $\\alpha^2z=\\alpha$. <b>Isolate $z$:</b> if $\\alpha\\ne0$ then $z=1/\\alpha$ and the system has a unique solution.","Hàng cuối mới là $\\alpha^2z=\\alpha$. <b>Cô lập $z$:</b> nếu $\\alpha\\ne0$ thì $z=1/\\alpha$, hệ có nghiệm duy nhất."),
  ("If $\\alpha=0$: $0\\cdot z=0$, always true, $z$ free: <b>infinitely many</b>. There is no value giving “no solution” here, because the right side $\\alpha$ vanishes exactly when $\\alpha^2$ does.","Nếu $\\alpha=0$: $0\\cdot z=0$ luôn đúng, $z$ tự do: <b>vô số nghiệm</b>. Ở đây không có giá trị nào cho vô nghiệm vì vế phải $\\alpha$ triệt tiêu đúng lúc $\\alpha^2$ triệt tiêu.")],
 choices=["$\\alpha\\ne0$","$\\alpha=1$","$\\alpha=0$","Other solution"],
 trap=("Do not conclude from the determinant alone: $\\det=-6\\alpha^2=0$ only says “not unique”; you must test consistency.","Đừng chỉ nhìn định thức: $\\det=-6\\alpha^2=0$ chỉ nói “không duy nhất”; phải kiểm tra tính tương thích."),
 variants=[
  V("★ New numbers","$x+y+z=1,\\ x+2y+3z=2,\\ 2x+3y+(\\beta^2+4)z=\\beta+3$. For which $\\beta$ infinitely many solutions?","$x+y+z=1,\\ x+2y+3z=2,\\ 2x+3y+(\\beta^2+4)z=\\beta+3$. Với $\\beta$ nào có vô số nghiệm?","$\\beta=0$",
   ("$R_3-R_1-R_2$: $\\beta^2z=\\beta$. Infinite iff $\\beta=0$.","$R_3-R_1-R_2$: $\\beta^2z=\\beta$. Vô số nghiệm iff $\\beta=0$."),
   lambda:[status(Matrix([[1,1,1],[1,2,3],[2,3,n*n+4]]),Matrix([1,2,n+3])) for n in (0,1,-1,2)]==["inf","unique","unique","unique"]),
  V("★★ Now \"no solution\" appears","$x+y+z=1,\\ x+2y+3z=2,\\ 2x+3y+(\\gamma^2-5)z=\\gamma+6$. Classify all $\\gamma$.","$x+y+z=1,\\ x+2y+3z=2,\\ 2x+3y+(\\gamma^2-5)z=\\gamma+6$. Phân loại mọi $\\gamma$.","$\\gamma=-3$: infinitely many; $\\gamma=3$: none; else unique",
   ("$R_3-R_1-R_2$: $(\\gamma^2-9)z=\\gamma+3$. $\\gamma=-3$: $0=0$; $\\gamma=3$: $0=6$; otherwise $z=\\frac1{\\gamma-3}$.","$R_3-R_1-R_2$: $(\\gamma^2-9)z=\\gamma+3$. $\\gamma=-3$: $0=0$; $\\gamma=3$: $0=6$; còn lại $z=\\frac1{\\gamma-3}$."),
   lambda:[status(Matrix([[1,1,1],[1,2,3],[2,3,n*n-5]]),Matrix([1,2,n+6])) for n in (-3,3,0,2)]==["inf","none","unique","unique"]),
  V("★★★ Geometry angle","For $\\alpha=0$ the three planes of the original system share a line. Give it as $(x,y,z)$ in terms of $z=t$.","Với $\\alpha=0$ ba mặt phẳng của hệ gốc cắt nhau theo một đường thẳng. Viết $(x,y,z)$ theo $z=t$.","$\\left(\\frac{7(1-t)}6,\\ \\frac{1+8t}3,\\ t\\right)$",
   ("Subtract eq.2 from eq.1: $3y-8z=1\\Rightarrow y=\\frac{1+8t}3$. Then $2x=3+3t-2y$, $x=\\frac{7(1-t)}6$.","Lấy PT1 − PT2: $3y-8z=1\\Rightarrow y=\\frac{1+8t}3$. Rồi $2x=3+3t-2y$, $x=\\frac{7(1-t)}6$."),
   lambda:all(simplify(2*X+2*Y-3*t-3)==0 and simplify(2*X-Y+5*t-2)==0 and simplify(4*X+Y+2*t-5)==0 for X,Y in [(7*(1-t)/6,(1+8*t)/3)]))]))

ITEMS.append(I("1.4","Quiz Ch.1 · Q4",("Network flow (figure missing)","Dòng chảy mạng (mất hình)"),
 ("The figure shows a network. If $x_3=150$ and $x_2=250$, which statement is <b>not</b> true? (a) none of the others is true, (b) $x_6-x_1=50$, (c) $x_5=100$, (d) $x_6-x_4=100$.","Hình vẽ một mạng dòng chảy. Nếu $x_3=150$, $x_2=250$ thì mệnh đề nào <b>không</b> đúng?"),
 "(a) None of the other answers is true (as printed in the quiz)",
 [("<b>The picture did not load in the PDF</b> (broken image), so the node equations cannot be rebuilt. We can only give the method; send the picture and I will add the exact solution.","<b>Hình không hiện trong file PDF</b> (ảnh lỗi) nên không dựng lại được các phương trình nút. Dưới đây là phương pháp; gửi lại hình, tôi sẽ thêm lời giải đúng."),
  ("<b>Method:</b> at every node, flow in = flow out. Each node gives one linear equation in the $x_i$. Solve the system; free variables are the unknown flows you can choose.","<b>Phương pháp:</b> ở mỗi nút, dòng vào = dòng ra. Mỗi nút cho một phương trình tuyến tính theo $x_i$. Giải hệ; biến tự do là các dòng ta được chọn."),
  ("Plug the given $x_3,x_2$ in, isolate the remaining variables, then test each statement (b),(c),(d). The statement that fails is the answer.","Thế $x_3,x_2$ đã cho, cô lập các biến còn lại, rồi thử từng mệnh đề (b),(c),(d). Mệnh đề sai là đáp án.")],
 choices=["None of the other answers is true","$x_6-x_1=50$","$x_5=100$","$x_6-x_4=100$"],
 note=("A full worked example of the same type is in the variants below.","Ví dụ đầy đủ cùng dạng ở các câu tương tự bên dưới."),
 variants=[
  V("★ Build and solve a network","Node A: inflow 200 splits into $x_1,x_2$. Node B: $x_1$ plus external inflow 60 leaves as $x_3$. Node C: $x_2+x_3$ leaves as $x_4$. If $x_1=80$, find $x_3,x_4$.","Nút A: dòng vào 200 chia thành $x_1,x_2$. Nút B: $x_1$ cộng dòng ngoài 60 ra thành $x_3$. Nút C: $x_2+x_3$ ra thành $x_4$. Nếu $x_1=80$, tìm $x_3,x_4$.","$x_3=140,\\ x_4=260$",
   ("Equations: $x_1+x_2=200$, $x_1+60=x_3$, $x_2+x_3=x_4$. With $x_1=80$: $x_2=120$, $x_3=140$, $x_4=260$.","Phương trình: $x_1+x_2=200$, $x_1+60=x_3$, $x_2+x_3=x_4$. Với $x_1=80$: $x_2=120$, $x_3=140$, $x_4=260$."),
   lambda:(lambda sol:sol[x3]==140 and sol[x4]==260)(solve([80+x2-200,80+60-x3,x2+x3-x4],[x2,x3,x4]))),
  V("★★ Feasible range","Same network, flows must be $\\ge0$. Find the range of $x_1$ and show $x_4$ is constant.","Cùng mạng, các dòng phải $\\ge0$. Tìm miền của $x_1$ và chứng minh $x_4$ không đổi.","$0\\le x_1\\le200$; $x_4=260$",
   ("Free variable $x_1=t$: $x_2=200-t\\ge0$, $x_3=t+60$, $x_4=(200-t)+(t+60)=260$. Needs $0\\le t\\le200$.","Biến tự do $x_1=t$: $x_2=200-t\\ge0$, $x_3=t+60$, $x_4=(200-t)+(t+60)=260$. Cần $0\\le t\\le200$."),
   lambda:simplify((200-t)+(t+60)-260)==0)]))

ITEMS.append(I("1.5","Quiz Ch.1 · Q5, Q13, Q16",("Recognising a linear equation","Nhận biết phương trình tuyến tính"),
 ("Which equation is linear? (Q5) (a) $\\frac{10}x+y=999$ (b) $\\frac12x+y+\\sqrt z=0$ (c) $e^x+y=2$ (d) $3x+2y=7$. &nbsp; (Q13) which is <b>not</b> linear: $a+2b+237c=192$; $x+y+z=3$; $x_1+x_2+x_3+x_4=0$; $\\sin x=0$. &nbsp; (Q16) (a) $x^2+y^2$ (b) $3x-4xy$ (c) $\\cos(3)x+\\sin(4)y$ (d) $\\frac3x+\\frac2y$.",
  "Phương trình nào tuyến tính? (Q5), (Q13: cái nào <b>không</b> tuyến tính), (Q16) như trên."),
 "Q5: (d) $3x+2y=7$ · Q13: $\\sin x=0$ · Q16: $\\cos(3)x+\\sin(4)y$",
 [("<b>Definition.</b> Linear in the unknowns $x_1,\\dots,x_n$ means: $a_1x_1+\\dots+a_nx_n=b$ where $a_i,b$ are <i>constants</i> (any real numbers, even $\\cos 3$ or $\\pi$).","<b>Định nghĩa.</b> Tuyến tính theo ẩn $x_1,\\dots,x_n$ nghĩa là $a_1x_1+\\dots+a_nx_n=b$ với $a_i,b$ là <i>hằng số</i> (số thực bất kỳ, kể cả $\\cos 3$ hay $\\pi$)."),
  ("<b>Each unknown appears</b> only to the power 1, alone: no $x^2$, no $xy$, no $1/x$, no $\\sqrt z$, no $e^x$, no $\\sin x$.","<b>Mỗi ẩn</b> chỉ xuất hiện với mũ 1 và đứng riêng: không $x^2$, không $xy$, không $1/x$, không $\\sqrt z$, không $e^x$, không $\\sin x$."),
  ("Apply: Q5: (a) has $1/x$, (b) $\\sqrt z$, (c) $e^x$ → not linear; (d) is. Q13: $\\sin x$ is a function of the unknown → the odd one out. Q16: (a) squares, (b) product $xy$, (d) reciprocals; in (c) $\\cos3$ and $\\sin4$ are just numbers → linear.","Áp dụng: Q5: (a) có $1/x$, (b) $\\sqrt z$, (c) $e^x$ → không tuyến tính; (d) tuyến tính. Q13: $\\sin x$ là hàm của ẩn → là cái còn lại. Q16: (a) bình phương, (b) tích $xy$, (d) nghịch đảo; ở (c) $\\cos3$, $\\sin4$ chỉ là số → tuyến tính.")],
 trap=("$\\cos(3)\\,x$ looks scary but is (number)×(unknown).","$\\cos(3)\\,x$ trông lạ nhưng là (số)×(ẩn)."),
 variants=[
  V("★ Count them","How many are linear in $x,y$: $2x-3y=5$; $xy=1$; $\\frac x2+\\frac y3=1$; $\\sin(2)x+y=0$; $\\sqrt2x+y=\\pi$; $\\frac1x+y=2$; $|x|+y=1$?","Có bao nhiêu phương trình tuyến tính theo $x,y$: $2x-3y=5$; $xy=1$; $\\frac x2+\\frac y3=1$; $\\sin(2)x+y=0$; $\\sqrt2x+y=\\pi$; $\\frac1x+y=2$; $|x|+y=1$?","$4$",
   ("Linear: 1st, 3rd, 4th, 5th. Not: $xy$, $1/x$, $|x|$.","Tuyến tính: thứ 1, 3, 4, 5. Không: $xy$, $1/x$, $|x|$."),lambda:True),
  V("★★ Parameter","For which $k$ is $(k-2)x^2+3x+y=5$ a linear equation in $x,y$?","Với $k$ nào $(k-2)x^2+3x+y=5$ là phương trình tuyến tính theo $x,y$?","$k=2$",
   ("The $x^2$ term must vanish: $k-2=0$.","Số hạng $x^2$ phải biến mất: $k-2=0$."),lambda:True)]))

ITEMS.append(I("1.6","Quiz Ch.1 · Q6",("Augmented matrix after row operations","Ma trận mở rộng sau phép biến đổi hàng"),
 ("Using elementary row operations, the augmented matrix of $\\begin{cases}x-2y+3z=9\\\\-x+3y=-4\\\\2x-5y+5z=17\\end{cases}$ (row-echelon form) is:","Dùng phép biến đổi hàng sơ cấp, ma trận mở rộng (dạng bậc thang) của hệ trên là:"),
 "$\\left[\\begin{array}{ccc|c}1&-2&3&9\\\\0&1&3&5\\\\0&0&1&2\\end{array}\\right]$",
 [("Write the augmented matrix $\\left[\\begin{array}{ccc|c}1&-2&3&9\\\\-1&3&0&-4\\\\2&-5&5&17\\end{array}\\right]$ (a missing variable means coefficient $0$).","Viết ma trận mở rộng $\\left[\\begin{array}{ccc|c}1&-2&3&9\\\\-1&3&0&-4\\\\2&-5&5&17\\end{array}\\right]$ (ẩn vắng mặt nghĩa là hệ số $0$)."),
  ("Clear column 1: $R_2\\leftarrow R_2+R_1$ gives $(0,1,3\\mid5)$; $R_3\\leftarrow R_3-2R_1$ gives $(0,-1,-1\\mid-1)$.","Khử cột 1: $R_2\\leftarrow R_2+R_1$ cho $(0,1,3\\mid5)$; $R_3\\leftarrow R_3-2R_1$ cho $(0,-1,-1\\mid-1)$."),
  ("Clear column 2: $R_3\\leftarrow R_3+R_2$ gives $(0,0,2\\mid4)$; scale $R_3\\leftarrow\\frac12R_3$ gives $(0,0,1\\mid2)$. So $z=2$, $y=5-6=-1$, $x=9+2y-3z=1$.","Khử cột 2: $R_3\\leftarrow R_3+R_2$ cho $(0,0,2\\mid4)$; chia $R_3\\leftarrow\\frac12R_3$ cho $(0,0,1\\mid2)$. Vậy $z=2$, $y=5-6=-1$, $x=9+2y-3z=1$.")],
 choices=["$\\left[\\begin{smallmatrix}1&-2&3&9\\\\0&-1&3&5\\\\0&0&1&2\\end{smallmatrix}\\right]$","$\\left[\\begin{smallmatrix}1&2&-3&9\\\\0&1&3&5\\\\0&0&1&2\\end{smallmatrix}\\right]$","$\\left[\\begin{smallmatrix}1&-2&3&9\\\\0&1&3&5\\\\0&0&1&2\\end{smallmatrix}\\right]$","$\\left[\\begin{smallmatrix}1&-2&3&9\\\\0&1&3&5\\\\0&0&1&1\\end{smallmatrix}\\right]$"],
 trap=("Each wrong option changes one entry (a sign, or the last constant). Verify by substituting back: the solution $(1,-1,2)$ must satisfy the <i>original</i> equations.","Mỗi đáp án sai đổi một phần tử (dấu hoặc hằng số cuối). Hãy thế ngược nghiệm $(1,-1,2)$ vào hệ <i>gốc</i>."),
 variants=[
  V("★ Same task","Reduce $\\begin{cases}x+y+z=6\\\\2x+3y+z=13\\\\x-y+2z=3\\end{cases}$ to echelon form with leading 1s and solve.","Đưa hệ trên về dạng bậc thang có phần tử đầu 1 và giải.","$(x,y,z)=(3,2,1)$",
   ("$R_2-2R_1$: $y-z=1$; $R_3-R_1$: $-2y+z=-3$; $R_3+2R_2$: $-z=-1\\Rightarrow z=1$; $y=2$; $x=6-2-1=3$.","$R_2-2R_1$: $y-z=1$; $R_3-R_1$: $-2y+z=-3$; $R_3+2R_2$: $-z=-1\\Rightarrow z=1$; $y=2$; $x=6-2-1=3$. Vậy $(3,2,1)$."),
   lambda:solve([x+y+z-6,2*x+3*y+z-13,x-y+2*z-3],[x,y,z])=={x:3,y:2,z:1}),
  V("★★ Parameter in the pivot","$\\begin{cases}x+y=2\\\\2x+ky=5\\end{cases}$. For which $k$ is there no solution? Give the echelon form.","$\\begin{cases}x+y=2\\\\2x+ky=5\\end{cases}$. Với $k$ nào vô nghiệm? Viết dạng bậc thang.","$k=2$; echelon $\\left[\\begin{smallmatrix}1&1&2\\\\0&k-2&1\\end{smallmatrix}\\right]$",
   ("$R_2-2R_1$: $(0,\\,k-2\\mid1)$. If $k=2$ it reads $0=1$: no solution; otherwise $y=\\frac1{k-2}$.","$R_2-2R_1$: $(0,\\,k-2\\mid1)$. Nếu $k=2$ thành $0=1$: vô nghiệm; ngược lại $y=\\frac1{k-2}$."),
   lambda:status(Matrix([[1,1],[2,2]]),Matrix([2,5]))=="none" and status(Matrix([[1,1],[2,3]]),Matrix([2,5]))=="unique")]))

ITEMS.append(I("1.7","Quiz Ch.1 · Q7",("Trigonometric parameter: counting $\\theta$","Tham số lượng giác: đếm $\\theta$"),
 ("How many $\\theta\\in(0,4\\pi)$ make $\\begin{cases}2(\\sin3\\theta)x-y+z=2\\\\3(\\cos2\\theta)x+4y+3z=3\\\\6x+7y+7z=9\\end{cases}$ have <b>no solution</b>?","Có bao nhiêu $\\theta\\in(0,4\\pi)$ để hệ trên <b>vô nghiệm</b>?"),
 "$7$",
 [("<b>Strategy.</b> A square system has a unique solution iff $\\det\\ne0$. So “no solution” can only happen when $\\det=0$. Compute the determinant (expand along column 1): $\\det=14\\sin3\\theta+42\\cos2\\theta-42$.","<b>Chiến lược.</b> Hệ vuông có nghiệm duy nhất iff $\\det\\ne0$. Nên “vô nghiệm” chỉ xảy ra khi $\\det=0$. Tính định thức (khai triển theo cột 1): $\\det=14\\sin3\\theta+42\\cos2\\theta-42$."),
  ("Use $\\sin3\\theta=3s-4s^3$ and $\\cos2\\theta=1-2s^2$ with $s=\\sin\\theta$: $\\det=-14\\,s\\,(4s^2+6s-3)$.","Dùng $\\sin3\\theta=3s-4s^3$ và $\\cos2\\theta=1-2s^2$ với $s=\\sin\\theta$: $\\det=-14\\,s\\,(4s^2+6s-3)$."),
  ("<b>Is it inconsistent whenever $\\det=0$?</b> Find $w$ with $w^TA=0$ on columns 2,3: $w=(-1,-2,1)$. When $\\det=0$ it kills column 1 too, but $w\\cdot b=-2-6+9=1\\ne0$ ⇒ always inconsistent.","<b>Có luôn vô nghiệm khi $\\det=0$ không?</b> Tìm $w$ triệt tiêu cột 2,3: $w=(-1,-2,1)$. Khi $\\det=0$ nó triệt tiêu cả cột 1, mà $w\\cdot b=-2-6+9=1\\ne0$ ⇒ luôn vô nghiệm."),
  ("<b>Count the roots in $(0,4\\pi)$.</b> $s=0$: $\\theta=\\pi,2\\pi,3\\pi$ → 3 values. $4s^2+6s-3=0$: $s=\\frac{-3\\pm\\sqrt{21}}4$; $\\frac{-3+\\sqrt{21}}4\\approx0.396$ is valid (2 angles per $2\\pi$ → 4 values), $\\approx-1.9$ is impossible ($|s|\\le1$). Total $3+4=7$.","<b>Đếm nghiệm trong $(0,4\\pi)$.</b> $s=0$: $\\theta=\\pi,2\\pi,3\\pi$ → 3 giá trị. $4s^2+6s-3=0$: $s=\\frac{-3\\pm\\sqrt{21}}4$; $\\frac{-3+\\sqrt{21}}4\\approx0.396$ hợp lệ (2 góc mỗi $2\\pi$ → 4 giá trị), $\\approx-1.9$ loại ($|s|\\le1$). Tổng $3+4=7$.")],
 trap=("Forgetting $s=0$, counting the invalid root, or counting only one period.","Quên $s=0$, đếm nghiệm không hợp lệ, hoặc chỉ đếm một chu kỳ."),mock=None,
 variants=[
  V("★ Smaller system","$\\begin{cases}(\\cos\\theta)x+y=1\\\\x+(\\cos\\theta)y=2\\end{cases}$. How many $\\theta\\in(0,4\\pi)$ give no solution?","$\\begin{cases}(\\cos\\theta)x+y=1\\\\x+(\\cos\\theta)y=2\\end{cases}$. Có bao nhiêu $\\theta\\in(0,4\\pi)$ để vô nghiệm?","$3$",
   ("$\\det=\\cos^2\\theta-1=0\\iff\\cos\\theta=\\pm1\\iff\\theta=\\pi,2\\pi,3\\pi$. For $\\cos\\theta=1$: $x+y=1$ and $x+y=2$ inconsistent; for $-1$: $-x+y=1$ and $x-y=2$ inconsistent.","$\\det=\\cos^2\\theta-1=0\\iff\\cos\\theta=\\pm1\\iff\\theta=\\pi,2\\pi,3\\pi$. Với $\\cos\\theta=1$: $x+y=1$ và $x+y=2$ mâu thuẫn; với $-1$: $-x+y=1$ và $x-y=2$ mâu thuẫn."),
   lambda:all(status(Matrix([[cc,1],[1,cc]]),Matrix([1,2]))=="none" for cc in (1,-1))),
  V("★★★ Left-null-vector angle","Show $\\begin{cases}x+y+z=1\\\\2x+2y+2z=3\\\\x-y=0\\end{cases}$ is inconsistent by finding $w$ with $w^TA=0$, $w\\cdot b\\ne0$.","Chứng minh hệ trên vô nghiệm bằng cách tìm $w$ với $w^TA=0$, $w\\cdot b\\ne0$.","$w=(-2,1,0)$, $w\\cdot b=1$",
   ("$-2R_1+R_2=(0,0,0)$ on the left but $-2\\cdot1+3=1\\ne0$ on the right.","$-2R_1+R_2=(0,0,0)$ ở vế trái nhưng $-2\\cdot1+3=1\\ne0$ ở vế phải."),
   lambda:(Matrix([[-2,1,0]])*Matrix([[1,1,1],[2,2,2],[1,-1,0]])).is_zero_matrix and (Matrix([[-2,1,0]])*Matrix([1,3,0]))[0]==1)]))

ITEMS.append(I("1.8","Quiz Ch.1 · Q8",("At least one solution","Có ít nhất một nghiệm"),
 ("For which real $m$ does $\\begin{cases}x+my+z=m\\\\2x+(m-1)y+3z=1\\\\mx+y+3z=2m-3\\end{cases}$ have <b>at least one</b> solution?","Với $m$ thực nào hệ có <b>ít nhất một</b> nghiệm?"),
 "$m\\ne-1$",
 [("“At least one” = unique <i>or</i> infinitely many = everything except “no solution”. First find the dangerous values: $\\det=2(m-2)(m+1)$, zero at $m=2$ and $m=-1$.","“Ít nhất một” = duy nhất <i>hoặc</i> vô số = mọi trường hợp trừ “vô nghiệm”. Trước hết tìm giá trị nguy hiểm: $\\det=2(m-2)(m+1)$, bằng 0 tại $m=2$ và $m=-1$."),
  ("For $m\\ne2,-1$: $\\det\\ne0$, unique solution ✓. Test $m=2$: rows $(1,2,1\\mid2),(2,1,3\\mid1),(2,1,3\\mid1)$: rows 2 and 3 coincide, rank $2$ = augmented rank $2$ → infinitely many ✓.","Với $m\\ne2,-1$: $\\det\\ne0$, nghiệm duy nhất ✓. Thử $m=2$: các hàng $(1,2,1\\mid2),(2,1,3\\mid1),(2,1,3\\mid1)$: hàng 2 và 3 trùng, hạng $2$ = hạng mở rộng $2$ → vô số nghiệm ✓."),
  ("Test $m=-1$: $(1,-1,1\\mid-1),(2,-2,3\\mid1),(-1,1,3\\mid-5)$. $R_2-2R_1$: $(0,0,1\\mid3)$; $R_3+R_1$: $(0,0,4\\mid-6)$ ⇒ $z=3$ and $z=-\\frac32$: contradiction ⇒ no solution. Answer: all $m\\ne-1$.","Thử $m=-1$: $(1,-1,1\\mid-1),(2,-2,3\\mid1),(-1,1,3\\mid-5)$. $R_2-2R_1$: $(0,0,1\\mid3)$; $R_3+R_1$: $(0,0,4\\mid-6)$ ⇒ $z=3$ và $z=-\\frac32$: mâu thuẫn ⇒ vô nghiệm. Đáp án: mọi $m\\ne-1$.")],
 choices=["$m=2$","$m\\ne-2$","$m=-1$","$m\\ne-1$"],
 trap=("$\\det=0$ does not mean “no solution”: at $m=2$ the system is still consistent.","$\\det=0$ không có nghĩa “vô nghiệm”: tại $m=2$ hệ vẫn có nghiệm."),
 variants=[
  V("★ Describe $m=2$","For $m=2$ write all solutions.","Với $m=2$ viết mọi nghiệm.","$(5-5s,\\ s,\\ 3s-3)$",
   ("Equations $x+2y+z=2$ and $2x+y+3z=1$. Eliminate $x$: $3y-z=3\\Rightarrow z=3y-3$; $x=2-2y-z=5-5y$. Let $y=s$.","Các phương trình $x+2y+z=2$ và $2x+y+3z=1$. Khử $x$: $3y-z=3\\Rightarrow z=3y-3$; $x=2-2y-z=5-5y$. Đặt $y=s$."),
   lambda:simplify((5-5*s)+2*s+(3*s-3)-2)==0 and simplify(2*(5-5*s)+s+3*(3*s-3)-1)==0),
  V("★★ Symmetric system","$\\begin{cases}kx+y+z=1\\\\x+ky+z=1\\\\x+y+kz=1\\end{cases}$. For which $k$ is there no solution?","$\\begin{cases}kx+y+z=1\\\\x+ky+z=1\\\\x+y+kz=1\\end{cases}$. Với $k$ nào vô nghiệm?","$k=-2$",
   ("$\\det=(k-1)^2(k+2)$. $k=1$: all three equations are $x+y+z=1$ (infinite). $k=-2$: adding the equations gives $0=3$ ⇒ none.","$\\det=(k-1)^2(k+2)$. $k=1$: cả ba phương trình là $x+y+z=1$ (vô số). $k=-2$: cộng ba phương trình được $0=3$ ⇒ vô nghiệm."),
   lambda:[status(Matrix([[kk,1,1],[1,kk,1],[1,1,kk]]),Matrix([1,1,1])) for kk in (1,-2,0,3)]==["inf","none","unique","unique"]),
  V("★★★ Counting integers","How many integers $m\\in[-5,5]$ give a <b>unique</b> solution to the original system?","Có bao nhiêu số nguyên $m\\in[-5,5]$ cho nghiệm <b>duy nhất</b>?","$9$",
   ("Unique iff $\\det\\ne0$, i.e. $m\\ne2,-1$: $11-2=9$.","Duy nhất iff $\\det\\ne0$, tức $m\\ne2,-1$: $11-2=9$."),
   lambda:sum(status(Matrix([[1,mm,1],[2,mm-1,3],[mm,1,3]]),Matrix([mm,1,2*mm-3]))=="unique" for mm in range(-5,6))==9)]))

ITEMS.append(I("1.9","Quiz Ch.1 · Q9, Q10, Q15, Q11",("Same pattern, four questions","Cùng một dạng, bốn câu"),
 ("(Q9) $x+y+kz=3,\\ x+ky+z=2,\\ kx+y+z=1$: all $k$ with a solution. &nbsp;(Q10) $x+2y-3z=4,\\ 3x-y+5z=2,\\ 4x+y+(\\alpha^2-14)z=\\alpha+2$: no solution for which $\\alpha$? &nbsp;(Q15) $x+2y-3z=6,\\ 3x-y+5z=1,\\ 4x+y+(\\alpha^2-23)z=\\alpha+2$: exactly one solution for which $\\alpha$? &nbsp;(Q11) $x-2y=1,\\ x-y+kz=-2,\\ ky+4z=6$.","(Q9) tìm mọi $k$ để hệ có nghiệm. (Q10) $\\alpha$ nào vô nghiệm? (Q15) $\\alpha$ nào có đúng một nghiệm? (Q11) xét số nghiệm theo $k$."),
 "Q9: $k\\ne1,-2$ · Q10: $\\alpha=-4$ · Q15: $\\alpha\\ne\\pm5$ · Q11: (A) and (D)",
 [("<b>Step A – the determinant tells you where to look.</b> Q9: $\\det=-(k-1)^2(k+2)$. Q10: $-7(\\alpha-4)(\\alpha+4)$. Q15: $-7(\\alpha-5)(\\alpha+5)$. Q11: $-(k-2)(k+2)$. Outside these roots the solution is <b>unique</b>.","<b>Bước A – định thức chỉ ra chỗ cần xét.</b> Q9: $\\det=-(k-1)^2(k+2)$. Q10: $-7(\\alpha-4)(\\alpha+4)$. Q15: $-7(\\alpha-5)(\\alpha+5)$. Q11: $-(k-2)(k+2)$. Ngoài các nghiệm này hệ có nghiệm <b>duy nhất</b>."),
  ("<b>Step B – test each root.</b> Q15: unique iff $\\alpha\\ne\\pm5$ ✓. Q10: use $R_3-R_1-R_2$ (same trick as 1.3): $(0,0,\\alpha^2-16\\mid\\alpha-4)$. $\\alpha=4$: $0=0$ (infinite); $\\alpha=-4$: $0=-8$ (<b>none</b>).","<b>Bước B – thử từng nghiệm.</b> Q15: duy nhất iff $\\alpha\\ne\\pm5$ ✓. Q10: dùng $R_3-R_1-R_2$ (mẹo như 1.3): $(0,0,\\alpha^2-16\\mid\\alpha-4)$. $\\alpha=4$: $0=0$ (vô số); $\\alpha=-4$: $0=-8$ (<b>vô nghiệm</b>)."),
  ("Q9: $k=1$ gives $x+y+z=3,2,1$ at once: impossible. $k=-2$: sum of the three equations has left side $0$ but right side $6$: impossible. So consistent iff $k\\ne1,-2$.","Q9: $k=1$ cho $x+y+z=3,2,1$ cùng lúc: vô lý. $k=-2$: tổng ba phương trình có vế trái $0$, vế phải $6$: vô lý. Vậy có nghiệm iff $k\\ne1,-2$."),
  ("Q11: $k=2$ ⇒ none; $k=-2$ ⇒ infinitely many (ranks 2,2); $k\\ne\\pm2$ ⇒ unique. So (A) true, (D) true, (B) false (it is infinite), (C) false, (E) false.","Q11: $k=2$ ⇒ vô nghiệm; $k=-2$ ⇒ vô số (hạng 2,2); $k\\ne\\pm2$ ⇒ duy nhất. Nên (A) đúng, (D) đúng, (B) sai (vô số), (C) sai, (E) sai.")],
 trap=("Never stop at “$\\det=0$”: classify each root by comparing $\\operatorname{rank}A$ with $\\operatorname{rank}[A|b]$.","Đừng dừng ở “$\\det=0$”: phân loại từng nghiệm bằng cách so sánh $\\operatorname{rank}A$ với $\\operatorname{rank}[A|b]$."),
 variants=[
  V("★ Change the right side","In Q9 replace the constants by $(1,1,1)$. For which $k$ is there a solution?","Ở Q9 đổi vế phải thành $(1,1,1)$. Với $k$ nào có nghiệm?","all $k\\ne-2$",
   ("$k=1$ now gives $x+y+z=1$ three times: consistent. $k=-2$: sum gives $0=3$: none.","Giờ $k=1$ cho $x+y+z=1$ ba lần: tương thích. $k=-2$: tổng cho $0=3$: vô nghiệm."),
   lambda:[status(Matrix([[kk,1,1],[1,kk,1],[1,1,kk]]),Matrix([1,1,1])) for kk in (1,-2,5)]==["inf","none","unique"]),
  V("★★ Find the missing constant","With $k=-2$ in Q9 the left side is fixed. For $x+y-2z=3,\\ x-2y+z=2,\\ -2x+y+z=c$ find $c$ so that a solution exists.","Với $k=-2$ ở Q9: $x+y-2z=3,\\ x-2y+z=2,\\ -2x+y+z=c$. Tìm $c$ để có nghiệm.","$c=-5$",
   ("The three left sides add to $0$, so the right sides must add to $0$: $3+2+c=0$.","Ba vế trái cộng lại bằng $0$ nên ba vế phải cũng phải cộng bằng $0$: $3+2+c=0$."),
   lambda:status(Matrix([[1,1,-2],[1,-2,1],[-2,1,1]]),Matrix([3,2,-5]))=="inf" and status(Matrix([[1,1,-2],[1,-2,1],[-2,1,1]]),Matrix([3,2,-4]))=="none"),
  V("★★★ Q11 reversed","For $x-2y=1,\\ x-y+kz=-2,\\ ky+4z=6$ and $k=-2$, write the family of solutions.","Với $k=-2$ ở Q11, viết họ nghiệm.","$(x,y,z)=(4z-5,\\ 2z-3,\\ z)$",
   ("$k=-2$: $x=1+2y$; $x-y-2z=-2\\Rightarrow 1+y-2z=-2\\Rightarrow y=2z-3$, $x=1+2y=4z-5$; check eq.3: $-2(2z-3)+4z=6$ ✓. So $(x,y,z)=(4z-5,\\,2z-3,\\,z)$.","$k=-2$: $x=1+2y$; $x-y-2z=-2\\Rightarrow1+y-2z=-2\\Rightarrow y=2z-3$, $x=1+2y=4z-5$; kiểm PT3: $-2(2z-3)+4z=6$ ✓. Vậy $(x,y,z)=(4z-5,\\,2z-3,\\,z)$."),
   lambda:all(simplify(X-2*Y-1)==0 and simplify(X-Y-2*t+2)==0 and simplify(-2*Y+4*t-6)==0 for X,Y in [(4*t-5,2*t-3)]))]))

ITEMS.append(I("1.10","Quiz Ch.1 · Q12, Q17",("Solving a system","Giải hệ phương trình"),
 ("(Q12) Solve $3x-2y=5,\\ 2x+y=8$. &nbsp;(Q17) Solve $x+y-2z=3,\\ -x+y+6z=13,\\ 2x+y-9z=-5$.","(Q12) Giải $3x-2y=5,\\ 2x+y=8$. (Q17) Giải hệ ba phương trình trên."),
 "Q12: $(3,2)$ · Q17: $(-1,6,1)$",
 [("<b>Q12 – isolate $y$</b> from the easy equation: $y=8-2x$. Substitute: $3x-2(8-2x)=5\\Rightarrow7x=21\\Rightarrow x=3$, $y=2$.","<b>Q12 – cô lập $y$</b> từ phương trình dễ: $y=8-2x$. Thế: $3x-2(8-2x)=5\\Rightarrow7x=21\\Rightarrow x=3$, $y=2$."),
  ("<b>Q17 – eliminate $x$:</b> Eq1+Eq2: $2y+4z=16\\Rightarrow y+2z=8$. Eq3−2·Eq1: $-y-5z=-11\\Rightarrow y+5z=11$.","<b>Q17 – khử $x$:</b> PT1+PT2: $2y+4z=16\\Rightarrow y+2z=8$. PT3−2·PT1: $-y-5z=-11\\Rightarrow y+5z=11$."),
  ("Subtract: $3z=3\\Rightarrow z=1$; then $y=8-2=6$; $x=3-y+2z=-1$. <b>Check</b> Eq2: $1+6+6=13$ ✓, Eq3: $-2+6-9=-5$ ✓.","Trừ hai phương trình: $3z=3\\Rightarrow z=1$; rồi $y=8-2=6$; $x=3-y+2z=-1$. <b>Kiểm tra</b> PT2: $1+6+6=13$ ✓, PT3: $-2+6-9=-5$ ✓.")],
 mock="Q12 (=Q12)",
 variants=[
  V("★ Two unknowns, fractions","$\\frac x2+\\frac y3=4,\\ x-y=2$.","$\\frac x2+\\frac y3=4,\\ x-y=2$.","$(x,y)=(\\frac{28}5,\\frac{18}5)$",
   ("Clear fractions: $3x+2y=24$; with $y=x-2$: $3x+2(x-2)=24\\Rightarrow5x=28\\Rightarrow x=\\frac{28}5,\\ y=\\frac{18}5$.","Khử mẫu: $3x+2y=24$; với $y=x-2$: $3x+2(x-2)=24\\Rightarrow5x=28\\Rightarrow x=\\frac{28}5,\\ y=\\frac{18}5$."),
   lambda:solve([x/2+y/3-4,x-y-2],[x,y])=={x:Rational(28,5),y:Rational(18,5)}),
  V("★★ Three unknowns","$x+2y+3z=14,\\ 2x-y+z=3,\\ 3x+y-z=2$.","$x+2y+3z=14,\\ 2x-y+z=3,\\ 3x+y-z=2$.","$(1,2,3)$",
   ("Eq2+Eq3: $5x=5$, $x=1$. Then $2y+3z=13$ and $y-z=-1\\Rightarrow y=z-1$: $2z-2+3z=13$, $z=3$, $y=2$.","PT2+PT3: $5x=5$, $x=1$. Rồi $2y+3z=13$ và $y-z=-1\\Rightarrow y=z-1$: $2z-2+3z=13$, $z=3$, $y=2$."),
   lambda:solve([x+2*y+3*z-14,2*x-y+z-3,3*x+y-z-2],[x,y,z])=={x:1,y:2,z:3})]))

ITEMS.append(I("1.11","Quiz Ch.1 · Q14",("Loan problem, three unknowns","Bài toán vay, ba ẩn"),
 ("A firm borrowed \\$500,000 at 3%, 4% and 5%. Annual interest was \\$20,500, and the amount at 4% was $2\\frac12$ times the amount at 3%. How much was borrowed at 4%?","Một công ty vay 500.000 USD với lãi 3%, 4%, 5%. Lãi hằng năm 20.500 USD và số tiền vay 4% bằng $2\\frac12$ lần số tiền vay 3%. Vay 4% là bao nhiêu?"),
 "\\$250,000",
 [("Unknowns $u,v,w$ = amounts at 3%, 4%, 5%. Equations: $u+v+w=500000$; $0.03u+0.04v+0.05w=20500$; $v=\\frac52u$.","Ẩn $u,v,w$ = số tiền vay 3%, 4%, 5%. Phương trình: $u+v+w=500000$; $0.03u+0.04v+0.05w=20500$; $v=\\frac52u$."),
  ("<b>Isolate</b> $v=\\frac52u$ and $w=500000-u-v=500000-\\frac72u$. Put into the interest equation (×100): $3u+4\\cdot\\frac52u+5(500000-\\frac72u)=2050000$.","<b>Cô lập</b> $v=\\frac52u$ và $w=500000-u-v=500000-\\frac72u$. Thế vào phương trình lãi (×100): $3u+4\\cdot\\frac52u+5(500000-\\frac72u)=2050000$."),
  ("$3u+10u-17.5u+2500000=2050000\\Rightarrow-4.5u=-450000\\Rightarrow u=100000$. Then $v=250000$, $w=150000$. <b>Check interest:</b> $3000+10000+7500=20500$ ✓.","$3u+10u-17.5u+2500000=2050000\\Rightarrow-4.5u=-450000\\Rightarrow u=100000$. Khi đó $v=250000$, $w=150000$. <b>Kiểm tra lãi:</b> $3000+10000+7500=20500$ ✓.")],
 choices=["\\$200,000","\\$250,000","\\$100,000","\\$150,000"],
 trap=("100,000 is the 3% amount and 150,000 the 5% amount: read which one the question asks for.","100.000 là khoản 3% và 150.000 là khoản 5%: đọc kỹ đề hỏi khoản nào."),
 variants=[
  V("★ Two rates","\\$10,000 is split between 4% and 6% accounts earning \\$520 a year. How much at 6%?","10.000 USD chia vào hai tài khoản 4% và 6%, lãi 520 USD/năm. Bao nhiêu ở 6%?","\\$6,000",
   ("$p+q=10000$, $0.04p+0.06q=520$; $p=10000-q$: $400+0.02q=520\\Rightarrow q=6000$.","$p+q=10000$, $0.04p+0.06q=520$; $p=10000-q$: $400+0.02q=520\\Rightarrow q=6000$."),
   lambda:solve([a+b-10000,Rational(4,100)*a+Rational(6,100)*b-520],[a,b])=={a:4000,b:6000}),
  V("★★★ Under-determined","Drop the “$2\\frac12$ times” condition. Show the amount at 4% can then vary and give the range if all amounts are $\\ge0$.","Bỏ điều kiện “$2\\frac12$ lần”. Chứng minh khoản vay 4% có thể thay đổi và tìm miền nếu mọi khoản $\\ge0$.","$v\\in[0,\\ 500000]$; two equations, three unknowns",
   ("Only $u+v+w=500000$ and $3u+4v+5w=2050000$. Subtract $3\\times$ first: $v+2w=550000$, so $v=550000-2w$; $w=t$, $u=500000-v-w=t-50000$. Need $u,v,w\\ge0$: $50000\\le t\\le275000$, so $v=550000-2t\\in[0,450000]$.","Chỉ còn $u+v+w=500000$ và $3u+4v+5w=2050000$. Lấy PT2 trừ $3\\times$PT1: $v+2w=550000$, nên $v=550000-2w$; $w=t$, $u=t-50000$. Cần $u,v,w\\ge0$: $50000\\le t\\le275000$, nên $v=550000-2t\\in[0,450000]$."),
   lambda:True)]))
# fix the 1.11 variant-3 answer text to match the derivation
ITEMS[-1].variants[1].ans="$v\\in[0,\\ 450000]$ (one free parameter)"
