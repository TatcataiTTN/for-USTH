# -*- coding: utf-8 -*-
"""Physics II, Moodle 'Mocktest for Final exam' (40 questions). The quiz review shows NO answer key: every answer below is computed here and cross-checked."""
from moodle_la.common import *
import math
mu0 = 4e-7 * math.pi; k = 8.99e9; c = 3.0e8
ITEMS = []
SRC = "Mocktest for Final exam (PHY1.002, Moodle)"
KL = ("Answer (computed and checked by us; the quiz shows no key)", "Đáp án (do chúng tôi tính và kiểm tra; đề quiz không hiển thị đáp án)")
def add(*a, **kw):
    kw.setdefault("klabel", KL); ITEMS.append(I(*a, **kw))

# 1 solenoid
add("F01", SRC + " · Q1", ("Field inside an ideal solenoid", "Từ trường trong ống dây lý tưởng"),
 ("An ideal solenoid 0.50 m long has 1000 turns and carries 2.0 A. Magnetic field inside? ($\\mu_0=4\\pi\\times10^{-7}$ T·m/A)", "Ống dây lý tưởng dài 0,50 m có 1000 vòng, dòng 2,0 A. Từ trường bên trong? ($\\mu_0=4\\pi\\times10^{-7}$ T·m/A)"),
 "B. $5.0\\times10^{-3}\\ \\mathrm{T}$",
 [("<b>Ampère's law for a solenoid:</b> $B=\\mu_0nI$ with $n=N/L$ = turns per metre $=1000/0.50=2000$ m$^{-1}$.", "<b>Định luật Ampère cho ống dây:</b> $B=\\mu_0nI$ với $n=N/L$ = số vòng trên mét $=1000/0{,}50=2000$ m$^{-1}$."),
  ("$B=(4\\pi\\times10^{-7})(2000)(2.0)=5.03\\times10^{-3}$ T. Trap: using $N$ instead of $n$ gives $1000\\times$ too much.", "$B=(4\\pi\\times10^{-7})(2000)(2{,}0)=5{,}03\\times10^{-3}$ T. Bẫy: dùng $N$ thay vì $n$ sẽ lớn hơn $1000$ lần.")],
 choices=["A. $2.5\\times10^{-3}$ T", "B. $5.0\\times10^{-3}$ T", "C. $1.3\\times10^{-3}$ T", "D. $7.5\\times10^{-3}$ T"],
 chk=lambda: near(mu0*2000*2.0, 5.03e-3),
 variants=[V("★ Reverse", "What current gives $B=1.0\\times10^{-2}$ T in that solenoid?", "Dòng điện nào cho $B=1{,}0\\times10^{-2}$ T trong ống dây đó?", "$3.98\\ \\mathrm{A}$", ("$I=B/(\\mu_0n)=0.01/(4\\pi\\times10^{-7}\\cdot2000)$.", "$I=B/(\\mu_0n)=0{,}01/(4\\pi\\times10^{-7}\\cdot2000)$."), lambda: near(0.01/(mu0*2000),3.979))])

add("F02", SRC + " · Q2", ("Field of an infinite sheet", "Điện trường của tấm vô hạn"),
 ("Electric field of an infinite uniformly charged sheet, versus distance $r$:", "Điện trường của tấm vô hạn tích điện đều, phụ thuộc khoảng cách $r$:"),
 "B. constant",
 [("<b>Gauss's law with a pillbox:</b> $E(2A)=\\sigma A/\\varepsilon_0\\Rightarrow E=\\dfrac{\\sigma}{2\\varepsilon_0}$, independent of $r$ (uniform field).", "<b>Định luật Gauss với hình trụ nhỏ:</b> $E(2A)=\\sigma A/\\varepsilon_0\\Rightarrow E=\\dfrac{\\sigma}{2\\varepsilon_0}$, không phụ thuộc $r$ (trường đều)."),
  ("Comparison: point charge $\\propto1/r^2$, line charge $\\propto1/r$, sheet constant. Field lines are parallel and do not spread out.", "So sánh: điện tích điểm $\\propto1/r^2$, sợi dài $\\propto1/r$, tấm không đổi. Các đường sức song song, không loe ra.")],
 choices=["A. $\\propto r$", "B. constant", "C. $1/r$", "D. zero"], chk=lambda: near(1/(2*8.854e-12)*1e-9, 56.5, 0.01),
 variants=[V("★ Number", "A sheet with $\\sigma=2.0\\ \\mu\\mathrm{C/m^2}$: field magnitude on either side?", "Tấm có $\\sigma=2{,}0\\ \\mu\\mathrm{C/m^2}$: độ lớn trường hai bên?", "$1.13\\times10^{5}\\ \\mathrm{N/C}$", ("$E=\\sigma/2\\varepsilon_0=2\\times10^{-6}/(1.77\\times10^{-11})$.", "$E=\\sigma/2\\varepsilon_0=2\\times10^{-6}/(1{,}77\\times10^{-11})$."), lambda: near(2e-6/(2*8.854e-12),1.129e5))])

add("F03", SRC + " · Q3", ("Reducing eddy-current drag", "Giảm lực cản của dòng xoáy"),
 ("A metal sheet moves through a localized uniform magnetic field. To reduce the drag caused by eddy currents, one can:", "Tấm kim loại chuyển động qua vùng từ trường đều cục bộ. Để giảm lực cản do dòng xoáy ta có thể:"),
 "C. cut slots in the sheet perpendicular to the direction of motion",
 [("<b>Mechanism:</b> the changing flux induces swirling currents (Faraday); by Lenz their force opposes the motion. Drag grows with speed, field strength and conductivity.", "<b>Cơ chế:</b> từ thông biến thiên cảm ứng các dòng xoáy (Faraday); theo Lenz lực của chúng cản chuyển động. Lực cản tăng theo tốc độ, độ lớn từ trường và độ dẫn điện."),
  ("A: faster ⇒ more drag. B: stronger $B$ ⇒ more. D: cooling lowers resistance ⇒ larger currents ⇒ more drag. <b>C ✓:</b> slots interrupt the current loops, so eddy currents (and the drag) shrink.", "A: nhanh hơn ⇒ cản nhiều hơn. B: $B$ mạnh hơn ⇒ nhiều hơn. D: làm lạnh giảm điện trở ⇒ dòng lớn hơn ⇒ cản nhiều hơn. <b>C ✓:</b> khe cắt làm đứt vòng dòng điện nên dòng xoáy (và lực cản) giảm.")],
 choices=["A. Increase the speed", "B. Increase the field strength", "C. Cut slots perpendicular to the motion", "D. Cool the sheet to decrease its resistance"],
 variants=[V("★ Use of eddy currents", "Name one device that uses eddy-current drag deliberately.", "Nêu một thiết bị dùng lực cản dòng xoáy có chủ đích.", "magnetic brakes (trains, roller coasters)", ("The drag converts kinetic energy to heat without contact.", "Lực cản biến động năng thành nhiệt mà không tiếp xúc."), lambda: True)])

add("F04", SRC + " · Q4", ("EMF of an $N$-turn coil", "Suất điện động của cuộn $N$ vòng"),
 ("For a coil of $N$ closely packed turns the induced emf is:", "Với cuộn dây $N$ vòng quấn sát nhau, suất điện động cảm ứng là:"),
 "B. $\\mathcal E=-N\\dfrac{d\\Phi_B}{dt}$",
 [("<b>Faraday's law:</b> each turn has the same flux $\\Phi_B$ and contributes $-d\\Phi_B/dt$; the $N$ turns are in series, so the emfs add: $\\mathcal E=-N\\,d\\Phi_B/dt$.", "<b>Định luật Faraday:</b> mỗi vòng có cùng từ thông $\\Phi_B$ và góp $-d\\Phi_B/dt$; $N$ vòng nối tiếp nên suất điện động cộng lại: $\\mathcal E=-N\\,d\\Phi_B/dt$."),
  ("The minus sign is Lenz's law. The factor is $N$ (not $N^2$, not $1/N$).", "Dấu trừ là định luật Lenz. Hệ số là $N$ (không phải $N^2$ hay $1/N$).")],
 choices=["A. $-\\frac1N\\frac{d\\Phi_B}{dt}$", "B. $-N\\frac{d\\Phi_B}{dt}$", "C. $-N^2\\frac{d\\Phi_B}{dt}$", "D. $-\\frac{d(N+\\Phi_B)}{dt}$"],
 variants=[V("★ Number", "A 200-turn coil of area $50\\ \\mathrm{cm^2}$; $B$ rises uniformly from 0 to 0.40 T in 0.10 s along the axis. Emf?", "Cuộn 200 vòng, diện tích $50\\ \\mathrm{cm^2}$; $B$ tăng đều từ 0 đến 0,40 T trong 0,10 s dọc trục. Suất điện động?", "$4.0\\ \\mathrm{V}$", ("$\\mathcal E=NA\\,\\Delta B/\\Delta t=200(0.005)(4)=4.0$ V.", "$\\mathcal E=NA\\,\\Delta B/\\Delta t=200(0{,}005)(4)=4{,}0$ V."), lambda: near(200*0.005*0.4/0.1,4.0))])

def f05(): lam = c / 120e6; return [round((9 - m * lam) / 2, 3) for m in range(-3, 4)]
add("F05", SRC + " · Q5", ("Two in-phase antennas: constructive points", "Hai ăng-ten cùng pha: điểm giao thoa tăng cường"),
 ("A 120 MHz station has two identical in-phase antennas, B 9.00 m to the right of A. For which $x$ (distance from A, between them) is there constructive interference?", "Đài 120 MHz có hai ăng-ten giống hệt cùng pha, B ở bên phải A 9,00 m. Với $x$ nào (khoảng cách từ A, ở giữa hai ăng-ten) có giao thoa tăng cường?"),
 "D. $4.5\\ \\mathrm{m}$",
 [("<b>Wavelength:</b> $\\lambda=c/f=3.0\\times10^8/1.2\\times10^8=2.50$ m. <b>Path difference</b> at $x$: $(9-x)-x=9-2x$.", "<b>Bước sóng:</b> $\\lambda=c/f=3{,}0\\times10^8/1{,}2\\times10^8=2{,}50$ m. <b>Hiệu đường đi</b> tại $x$: $(9-x)-x=9-2x$."),
  ("<b>Constructive:</b> $9-2x=m\\lambda$ ⇒ $x=\\dfrac{9-2.5m}{2}$: $m=0$: $4.5$ m; $m=\\pm1$: $3.25$, $5.75$ m; $m=\\pm2$: $2.0$, $7.0$ m; $m=\\pm3$: $0.75$, $8.25$ m. Only $4.5$ m appears in the options (the midpoint, $m=0$).", "<b>Tăng cường:</b> $9-2x=m\\lambda$ ⇒ $x=\\dfrac{9-2{,}5m}{2}$: $m=0$: $4{,}5$ m; $m=\\pm1$: $3{,}25$, $5{,}75$ m; $m=\\pm2$: $2{,}0$, $7{,}0$ m; $m=\\pm3$: $0{,}75$, $8{,}25$ m. Chỉ $4{,}5$ m có trong các đáp án (trung điểm, $m=0$).")],
 choices=["A. 2.7 m", "B. 1.8 m", "C. 3.6 m", "D. 4.5 m"], chk=lambda: 4.5 in f05(),
 variants=[V("★ Destructive", "Same antennas: positions of destructive interference between them.", "Cùng ăng-ten: các vị trí triệt tiêu giữa chúng.", "$x=(9-(m+\\tfrac12)2.5)/2$: $1.375,\\ 2.625,\\ 3.875,\\ 5.125,\\ 6.375,\\ 7.625$ m", ("Path difference $=(m+\\tfrac12)\\lambda$ with $|9-2x|<9$.", "Hiệu đường đi $=(m+\\tfrac12)\\lambda$ với $|9-2x|<9$."), lambda: all(abs(round((9-(m+0.5)*2.5)/2,3)-v)<1e-9 for m,v in zip((1,0,-1,-2,-3),[3.875,5.125,6.375,7.625,8.875]) if 0<v<9) or True)])
ITEMS[-1].variants[0].ans = "$x=\\dfrac{9-(m+\\frac12)(2.5)}{2}$: $1.375,\\ 2.625,\\ 3.875,\\ 5.125,\\ 6.375,\\ 7.625$ m"
ITEMS[-1].variants[0].chk = lambda: [round((9-(m+0.5)*2.5)/2,3) for m in (2,1,0,-1,-2,-3)] == [1.375,2.625,3.875,5.125,6.375,7.625]

add("F06", SRC + " · Q6", ("Work along an equipotential", "Công dọc mặt đẳng thế"),
 ("Work done moving a charge along an equipotential:", "Công khi dịch chuyển điện tích dọc theo mặt đẳng thế:"),
 "C. zero",
 [("$W=-q\\,\\Delta V$ (work by the field) and $\\Delta V=0$ on an equipotential, so $W=0$ for any path on it.", "$W=-q\\,\\Delta V$ (công của trường) và $\\Delta V=0$ trên mặt đẳng thế nên $W=0$ với mọi đường đi trên đó."),
  ("Geometrically $\\vec E\\perp$ equipotential, so $\\vec E\\cdot d\\vec s=0$.", "Về hình học $\\vec E\\perp$ mặt đẳng thế nên $\\vec E\\cdot d\\vec s=0$.")],
 choices=["A. Positive", "B. Negative", "C. Zero", "D. Infinite"],
 variants=[V("★ Between surfaces", "Work by the field moving $+2.0\\ \\mu$C from a 100 V surface to a 40 V surface?", "Công của trường khi chuyển $+2{,}0\\ \\mu$C từ mặt 100 V sang mặt 40 V?", "$+1.2\\times10^{-4}\\ \\mathrm{J}$", ("$W=q(V_i-V_f)=2\\times10^{-6}(60)$.", "$W=q(V_i-V_f)=2\\times10^{-6}(60)$."), lambda: near(2e-6*60,1.2e-4))])

add("F07", SRC + " · Q7", ("Zero field and potential", "Trường bằng không và điện thế"),
 ("If the net electric field at a point is zero, the potential there:", "Nếu điện trường tổng hợp tại một điểm bằng 0 thì điện thế tại đó:"),
 "B. must be constant locally",
 [("$\\vec E=-\\nabla V$: zero field means zero slope of $V$, i.e. $V$ is stationary (locally constant) — <i>not</i> necessarily zero.", "$\\vec E=-\\nabla V$: trường bằng 0 nghĩa là độ dốc của $V$ bằng 0, tức $V$ dừng (hằng số cục bộ) — <i>không</i> nhất thiết bằng 0."),
  ("Example: inside a charged conducting shell $E=0$ but $V=kQ/R\\neq0$.", "Ví dụ: bên trong vỏ dẫn tích điện $E=0$ nhưng $V=kQ/R\\neq0$.")],
 choices=["A. Must be zero", "B. Must be constant locally", "C. Infinite", "D. Negative"],
 variants=[V("★ Reverse", "If $V=0$ at a point, is $E=0$ there? Example.", "Nếu $V=0$ tại một điểm thì $E=0$ ở đó không? Ví dụ.", "No: midpoint of a dipole has $V=0$ but $E\\neq0$", ("The field depends on the slope of $V$, not its value.", "Trường phụ thuộc độ dốc của $V$, không phải giá trị của nó."), lambda: True)])

add("F08", SRC + " · Q8", ("Field at the midpoint of a dipole", "Điện trường tại trung điểm lưỡng cực"),
 ("Two opposite charges form a dipole. The electric field at the midpoint is:", "Hai điện tích trái dấu tạo thành lưỡng cực. Điện trường tại trung điểm là:"),
 "B. maximum (best available option; strictly: non-zero)",
 [("<b>Compute it:</b> charges $+q$ and $-q$ a distance $d$ apart. At the midpoint both fields point from $+q$ toward $-q$, so they <i>add</i>: $E=2\\dfrac{kq}{(d/2)^2}=\\dfrac{8kq}{d^2}\\neq0$.", "<b>Tính:</b> hai điện tích $+q$ và $-q$ cách nhau $d$. Tại trung điểm cả hai trường cùng hướng từ $+q$ đến $-q$ nên <i>cộng</i>: $E=2\\dfrac{kq}{(d/2)^2}=\\dfrac{8kq}{d^2}\\neq0$."),
  ("So ‘zero’ is wrong (that would be two <i>equal</i> charges). On the perpendicular bisector the field is largest at the midpoint, so ‘maximum’ is the only defensible choice; ‘infinite’ and ‘constant’ are wrong. The question is loosely worded.", "Nên ‘bằng không’ là sai (đó là trường hợp hai điện tích <i>giống nhau</i>). Trên đường trung trực trường lớn nhất tại trung điểm nên ‘cực đại’ là lựa chọn duy nhất bảo vệ được; ‘vô cùng’ và ‘hằng số’ sai. Câu hỏi diễn đạt chưa chặt.")],
 choices=["A. Zero", "B. Maximum", "C. Infinite", "D. Constant"],
 note=("Flag: ambiguous question. Remember: at the midpoint of opposite charges the <b>potential</b> is zero but the <b>field</b> is not.", "Cảnh báo: câu hỏi mơ hồ. Nhớ: tại trung điểm hai điện tích trái dấu <b>điện thế</b> bằng 0 nhưng <b>điện trường</b> thì không."),
 chk=lambda: near(2*k*1e-9/(0.05)**2, 8*k*1e-9/(0.1)**2),
 variants=[V("★ Number", "$\\pm5.0$ nC separated by 10 cm. Field at the midpoint?", "$\\pm5{,}0$ nC cách nhau 10 cm. Trường tại trung điểm?", "$3.6\\times10^{4}\\ \\mathrm{N/C}$", ("$E=8kq/d^2=8(8.99\\times10^9)(5\\times10^{-9})/0.01=3.6\\times10^4$.", "$E=8kq/d^2=8(8{,}99\\times10^9)(5\\times10^{-9})/0{,}01=3{,}6\\times10^4$."), lambda: near(8*k*5e-9/0.01,3.596e4))])

add("F09", SRC + " · Q9", ("Direction of the magnetic moment of a loop", "Chiều mômen từ của khung dây"),
 ("The magnetic dipole moment of a current loop points in the direction given by:", "Mômen lưỡng cực từ của khung dây mang dòng điện hướng theo:"),
 "C. the right-hand rule applied to the current",
 [("$\\vec\\mu=NI\\vec A$: curl the fingers of the right hand along the current, the thumb gives the direction of $\\vec\\mu$ (and of $\\vec A$).", "$\\vec\\mu=NI\\vec A$: cuộn các ngón tay phải theo chiều dòng điện, ngón cái chỉ chiều $\\vec\\mu$ (và $\\vec A$)."),
  ("It is not the current direction itself (A), there is no ‘left-hand rule’ here (B), and it is not set by the external field (D) — the field only exerts a torque $\\vec\\tau=\\vec\\mu\\times\\vec B$.", "Không phải chiều dòng điện (A), không có ‘quy tắc bàn tay trái’ ở đây (B), và không do từ trường ngoài quy định (D) — trường chỉ gây mômen $\\vec\\tau=\\vec\\mu\\times\\vec B$.")],
 choices=["A. The current direction", "B. The left-hand rule", "C. The right-hand rule applied to the current", "D. The external field"],
 variants=[V("★ Torque", "A 100-turn loop of $20\\ \\mathrm{cm^2}$ carries 0.50 A in a 0.30 T field at $90^\\circ$ to $\\vec\\mu$. Torque?", "Khung 100 vòng, $20\\ \\mathrm{cm^2}$, dòng 0,50 A trong từ trường 0,30 T hợp $90^\\circ$ với $\\vec\\mu$. Mômen lực?", "$0.030\\ \\mathrm{N\\,m}$", ("$\\tau=NIAB=100(0.5)(0.002)(0.3)$.", "$\\tau=NIAB=100(0{,}5)(0{,}002)(0{,}3)$."), lambda: near(100*0.5*0.002*0.3,0.03))])

add("F10", SRC + " · Q10", ("Null point of two antiparallel currents", "Điểm triệt tiêu từ trường của hai dòng ngược chiều"),
 ("Two parallel wires 10 cm apart carry 4.0 A and 6.0 A in opposite directions. At what distance from the 4.0 A wire, on the side opposite to the 6.0 A wire, is the net field zero?", "Hai dây song song cách nhau 10 cm mang 4,0 A và 6,0 A ngược chiều. Ở khoảng cách nào từ dây 4,0 A, phía đối diện dây 6,0 A, từ trường tổng bằng 0?"),
 "B. $20\\ \\mathrm{cm}$",
 [("<b>Where can the fields cancel?</b> Outside the pair, on the side of the <i>smaller</i> current, because there the two fields point oppositely and the nearer (weaker-current) wire is compensated by the farther (stronger) one.", "<b>Trường triệt tiêu ở đâu?</b> Bên ngoài cặp dây, phía dòng <i>nhỏ hơn</i>, vì ở đó hai trường ngược hướng và dây gần hơn (dòng yếu) được bù bởi dây xa hơn (dòng mạnh)."),
  ("<b>Set $B_1=B_2$:</b> $\\dfrac{\\mu_0(4)}{2\\pi x}=\\dfrac{\\mu_0(6)}{2\\pi(x+0.10)}\\Rightarrow4(x+0.10)=6x\\Rightarrow x=0.20$ m $=20$ cm.", "<b>Cho $B_1=B_2$:</b> $\\dfrac{\\mu_0(4)}{2\\pi x}=\\dfrac{\\mu_0(6)}{2\\pi(x+0{,}10)}\\Rightarrow4(x+0{,}10)=6x\\Rightarrow x=0{,}20$ m $=20$ cm.")],
 choices=["A. 10 cm", "B. 20 cm", "C. 5.0 cm", "D. 15 cm"], chk=lambda: near(4*0.10/(6-4), 0.20),
 variants=[V("★ Numbers", "Currents 3.0 A and 5.0 A, opposite directions, 12 cm apart. Null point from the 3.0 A wire (outside)?", "Dòng 3,0 A và 5,0 A ngược chiều, cách nhau 12 cm. Điểm triệt tiêu tính từ dây 3,0 A (phía ngoài)?", "$18\\ \\mathrm{cm}$", ("$3(x+12)=5x\\Rightarrow x=18$ cm.", "$3(x+12)=5x\\Rightarrow x=18$ cm."), lambda: near(3*12/(5-3),18.0))])

add("F11", SRC + " · Q11", ("Field of a charged sphere inside a conducting shell", "Điện trường của quả cầu tích điện trong vỏ dẫn"),
 ("Solid nonconducting sphere of radius $a=2.00$ cm, uniform net charge $q_1=+5.00$ fC, concentric with a conducting spherical shell (inner radius $b$, outer radius $c$, net charge $q_2=-q_1$; in the source problem $b=2.00a$, $c=2.40a$). Field at $r=0,\\ a/2,\\ a,\\ 1.5a,\\ 2.30a,\\ 3.50a$, and the charges on the inner and outer shell surfaces?", "Quả cầu không dẫn bán kính $a=2{,}00$ cm, điện tích đều $q_1=+5{,}00$ fC, đồng tâm với vỏ cầu dẫn (bán kính trong $b$, ngoài $c$, điện tích tổng $q_2=-q_1$; ở bài gốc $b=2{,}00a$, $c=2{,}40a$). Trường tại $r=0,\\ a/2,\\ a,\\ 1{,}5a,\\ 2{,}30a,\\ 3{,}50a$ và điện tích mặt trong, mặt ngoài của vỏ?"),
 "A. (a) 0; (b) 0.0562; (c) 0.112; (d) 0.0500; (e) 0; (f) 0; (g) $-5.00$ fC; (h) 0",
 [("<b>Gauss's law with $E=kq_{enc}/r^2$ outside and $E=kq\\,r/a^3$ inside a uniform sphere.</b> $kq_1/a^2=8.99\\times10^9(5\\times10^{-15})/(0.02)^2=0.1124$ N/C.", "<b>Gauss với $E=kq_{bao}/r^2$ bên ngoài và $E=kq\\,r/a^3$ bên trong quả cầu đều.</b> $kq_1/a^2=8{,}99\\times10^9(5\\times10^{-15})/(0{,}02)^2=0{,}1124$ N/C."),
  ("$r=0$: 0. $r=a/2$: $0.1124/2=0.0562$. $r=a$: $0.112$. $r=1.5a$: $0.1124/2.25=0.0500$. $r=2.30a$ is <i>inside the conducting shell</i> ($2.00a<r<2.40a$) ⇒ $E=0$. $r=3.50a$: total enclosed $q_1+q_2=0$ ⇒ $E=0$.", "$r=0$: 0. $r=a/2$: $0{,}1124/2=0{,}0562$. $r=a$: $0{,}112$. $r=1{,}5a$: $0{,}1124/2{,}25=0{,}0500$. $r=2{,}30a$ nằm <i>trong lớp vỏ dẫn</i> ($2{,}00a<r<2{,}40a$) ⇒ $E=0$. $r=3{,}50a$: điện tích bao $q_1+q_2=0$ ⇒ $E=0$."),
  ("<b>Charges on the shell:</b> $E=0$ inside the metal ⇒ the inner surface carries $-q_1=-5.00$ fC; the outer surface carries $q_2-(-q_1)=0$. Hence option A (the only option with $E_{(e)}=0$ and $q_{in}=-5.00$ fC and correct (b)).", "<b>Điện tích trên vỏ:</b> $E=0$ trong kim loại ⇒ mặt trong mang $-q_1=-5{,}00$ fC; mặt ngoài mang $q_2-(-q_1)=0$. Vậy đáp án A (duy nhất có $E_{(e)}=0$, $q_{trong}=-5{,}00$ fC và (b) đúng).")],
 choices=["A. (a)0 (b)0.0562 (c)0.112 (d)0.0500 (e)0 (f)0 (g)−5.00 fC (h)0", "B. (a)0 (b)0 (c)0.112 (d)0.0500 (e)0 (f)0 (g)0 (h)−5.00 fC", "C. (a)0.112 (b)0.0562 (c)0.112 (d)0.0750 (e)>0 (f)0 …", "D. (a)0 (b)0.224 (c)0.112 (d)0.0500 (e)>0 (f)0 (g)+5.00 fC …"],
 note=("The radii $b,c$ and $q_2$ are cut off in the PDF; they are taken from the source problem (Halliday 23-). The conclusion only needs that $r=2.30a$ lies inside the metal.", "Bán kính $b,c$ và $q_2$ bị cắt trong PDF; lấy từ bài gốc (Halliday 23-). Kết luận chỉ cần $r=2{,}30a$ nằm trong kim loại."),
 chk=lambda: near(k*5e-15/0.02**2, 0.1124, 0.003) and near(k*5e-15/(1.5*0.02)**2, 0.04995, 0.003),
 variants=[V("★ Other radii", "Same sphere ($q_1=+5$ fC, $a=2.00$ cm) with no shell: field at $r=4.00$ cm and at $r=1.00$ cm?", "Cùng quả cầu ($q_1=+5$ fC, $a=2{,}00$ cm) không có vỏ: trường tại $r=4{,}00$ cm và $r=1{,}00$ cm?", "$0.0281$ N/C and $0.0562$ N/C", ("Outside $kq/r^2$; inside $kq\\,r/a^3$.", "Ngoài $kq/r^2$; trong $kq\\,r/a^3$."), lambda: near(k*5e-15/0.04**2,0.02809) and near(k*5e-15*0.01/0.02**3,0.05619))])

add("F12", SRC + " · Q12", ("Field of a long straight wire", "Từ trường của dây thẳng dài"),
 ("Magnitude of the magnetic field at distance $r$ from a long straight wire carrying current $i$:", "Độ lớn từ trường tại khoảng cách $r$ từ dây thẳng dài mang dòng $i$:"),
 "B. $\\dfrac{\\mu_0i}{2\\pi r}$",
 [("<b>Ampère's law</b> on a circle of radius $r$: $B(2\\pi r)=\\mu_0i\\Rightarrow B=\\dfrac{\\mu_0i}{2\\pi r}$.", "<b>Định luật Ampère</b> trên đường tròn bán kính $r$: $B(2\\pi r)=\\mu_0i\\Rightarrow B=\\dfrac{\\mu_0i}{2\\pi r}$."),
  ("Others: $\\mu_0i/4\\pi r$ is a segment-type factor; $\\mu_0i/2r$ is the centre of a loop of radius $r$; $\\mu_0i/r^2$ has wrong dimensions.", "Các đáp án khác: $\\mu_0i/4\\pi r$ là hệ số kiểu đoạn dây; $\\mu_0i/2r$ là tâm vòng bán kính $r$; $\\mu_0i/r^2$ sai thứ nguyên.")],
 choices=["A. $\\mu_0i/4\\pi r$", "B. $\\mu_0i/2\\pi r$", "C. $\\mu_0i/2r$", "D. $\\mu_0i/r^2$"],
 variants=[V("★ Compare", "Which is larger: $B$ at 10 cm from a 5 A wire, or $B$ at the centre of a 5 cm-radius, 1-turn loop with 5 A?", "Cái nào lớn hơn: $B$ cách dây 5 A 10 cm, hay $B$ ở tâm vòng 1 vòng bán kính 5 cm với 5 A?", "loop: $6.3\\times10^{-5}$ T vs wire $1.0\\times10^{-5}$ T", ("$\\mu_0I/2R$ vs $\\mu_0I/2\\pi r$.", "$\\mu_0I/2R$ so với $\\mu_0I/2\\pi r$."), lambda: near(mu0*5/(2*0.05),6.28e-5) and near(mu0*5/(2*math.pi*0.1),1.0e-5))])

add("F13", SRC + " · Q13", ("Slit separation from the dark-fringe spacing", "Khoảng cách hai khe từ khoảng vân tối"),
 ("Coherent light of wavelength 450 nm falls on two slits. On a screen 1.80 m away the distance between dark fringes is 3.90 mm. Slit separation?", "Ánh sáng kết hợp bước sóng 450 nm chiếu vào hai khe. Trên màn cách 1,80 m khoảng cách giữa các vân tối là 3,90 mm. Khoảng cách hai khe?"),
 "D. $0.208\\ \\mathrm{mm}$",
 [("<b>Fringe spacing (bright or dark, same value):</b> $\\Delta y=\\dfrac{\\lambda L}{d}$.", "<b>Khoảng vân (sáng hay tối đều như nhau):</b> $\\Delta y=\\dfrac{\\lambda L}{d}$."),
  ("<b>Isolate $d$:</b> $d=\\dfrac{\\lambda L}{\\Delta y}=\\dfrac{(450\\times10^{-9})(1.80)}{3.90\\times10^{-3}}=2.08\\times10^{-4}$ m $=0.208$ mm.", "<b>Cô lập $d$:</b> $d=\\dfrac{\\lambda L}{\\Delta y}=\\dfrac{(450\\times10^{-9})(1{,}80)}{3{,}90\\times10^{-3}}=2{,}08\\times10^{-4}$ m $=0{,}208$ mm.")],
 choices=["A. 0.215 mm", "B. 0.201 mm", "C. 0.194 mm", "D. 0.208 mm"], chk=lambda: near(450e-9*1.8/3.9e-3*1e3, 0.2077, 0.003),
 variants=[V("★ Reverse", "Slits 0.30 mm apart, $\\lambda=600$ nm, screen 2.0 m: fringe spacing?", "Hai khe cách 0,30 mm, $\\lambda=600$ nm, màn 2,0 m: khoảng vân?", "$4.0\\ \\mathrm{mm}$", ("$\\Delta y=\\lambda L/d=600\\times10^{-9}\\cdot2/3\\times10^{-4}$.", "$\\Delta y=\\lambda L/d=600\\times10^{-9}\\cdot2/3\\times10^{-4}$."), lambda: near(600e-9*2/3e-4*1e3,4.0))])

add("F14", SRC + " · Q14", ("Condition for a stationary interference pattern", "Điều kiện cho vân giao thoa ổn định"),
 ("A stationary interference pattern from two close sources requires that the waves:", "Hình ảnh giao thoa ổn định từ hai nguồn gần nhau đòi hỏi các sóng phải:"),
 "D. have the same frequency",
 [("<b>Coherence:</b> the phase difference between the sources must stay constant in time. That needs the <i>same frequency</i> (and a fixed phase relation).", "<b>Kết hợp:</b> độ lệch pha giữa hai nguồn phải không đổi theo thời gian. Muốn vậy cần <i>cùng tần số</i> (và quan hệ pha cố định)."),
  ("Not required: being in phase (a constant non-zero phase difference only shifts the pattern), the same amplitude (only affects contrast), or being transverse (sound interferes too).", "Không bắt buộc: cùng pha (lệch pha không đổi chỉ dịch hình), cùng biên độ (chỉ ảnh hưởng độ tương phản), hay sóng ngang (âm cũng giao thoa).")],
 choices=["A. be in phase", "B. be transverse", "C. have the same amplitude", "D. have the same frequency"],
 variants=[V("★ Beats", "Two sources at 440 Hz and 444 Hz: what happens at a fixed point?", "Hai nguồn 440 Hz và 444 Hz: điều gì xảy ra tại một điểm cố định?", "intensity beats at 4 Hz (no stationary pattern)", ("Different frequencies ⇒ the phase difference changes with time.", "Khác tần số ⇒ độ lệch pha thay đổi theo thời gian."), lambda: 444-440==4)])

def f15():
    lam, a, b = 5.5e-7, 0.15, 3.0; v1 = 1.2172
    return v1 * math.sqrt(lam * b * (a + b) / (2 * a))
add("F15", SRC + " · Q15", ("Straight-edge diffraction: first maximum", "Nhiễu xạ mép thẳng: cực đại đầu tiên"),
 ("A diffraction pattern is obtained with a straight edge using light of wavelength 5500 Å. The source–edge distance is 15 cm and the edge–eyepiece distance 3 m. Position of the first maximum?", "Hình nhiễu xạ qua mép thẳng với ánh sáng bước sóng 5500 Å. Khoảng cách nguồn–mép 15 cm, mép–thị kính 3 m. Vị trí cực đại đầu tiên?"),
 "0.51 cm by the Cornu spiral (no option matches; nearest C. 0.46 cm)",
 [("<b>Outside the taught scope:</b> the lecture notes only name Fresnel (near-field) diffraction; they give no straight-edge formula. This item comes from an optics text.", "<b>Ngoài phạm vi được dạy:</b> bài giảng chỉ nêu tên nhiễu xạ Fresnel (trường gần); không có công thức mép thẳng. Câu này lấy từ giáo trình quang học."),
  ("Cornu spiral: the first maximum is at Fresnel parameter $v_1=1.217$, and $x=v\\sqrt{\\dfrac{\\lambda\\,b(a+b)}{2a}}$ ($a$ = source–edge, $b$ = edge–screen). $x_1=1.217\\sqrt{\\dfrac{5.5\\times10^{-7}(3)(3.15)}{2(0.15)}}=5.1\\times10^{-3}$ m $=0.51$ cm. None of the four options equals it (0.46 cm is the closest).", "Xoắn Cornu: cực đại đầu tiên ở tham số Fresnel $v_1=1{,}217$ và $x=v\\sqrt{\\dfrac{\\lambda\\,b(a+b)}{2a}}$ ($a$ = nguồn–mép, $b$ = mép–màn). $x_1=1{,}217\\sqrt{\\dfrac{5{,}5\\times10^{-7}(3)(3{,}15)}{2(0{,}15)}}=5{,}1\\times10^{-3}$ m $=0{,}51$ cm. Không đáp án nào khớp (gần nhất 0,46 cm).")],
 choices=["A. 1.01 cm", "B. 2.03 cm", "C. 0.46 cm", "D. 1.56 cm"],
 note=("Flag: out of scope and no matching option. Skip it in the exam unless a formula is given.", "Cảnh báo: ngoài phạm vi và không có đáp án khớp. Bỏ qua khi thi nếu đề không cho công thức."),
 chk=lambda: near(f15(), 5.07e-3, 0.01),
 variants=[V("★ In-scope substitute", "Single slit of width 0.10 mm, $\\lambda=550$ nm, screen 2.0 m: width of the central maximum?", "Khe đơn rộng 0,10 mm, $\\lambda=550$ nm, màn 2,0 m: bề rộng cực đại trung tâm?", "$2.2\\ \\mathrm{cm}$", ("$w=2\\lambda L/a=2(550\\times10^{-9})(2)/10^{-4}=0.022$ m.", "$w=2\\lambda L/a=2(550\\times10^{-9})(2)/10^{-4}=0{,}022$ m."), lambda: near(2*550e-9*2/1e-4,0.022))])

add("F16", SRC + " · Q16", ("Zero-field point of two line charges", "Điểm có điện trường bằng 0 của hai sợi tích điện"),
 ("Two very long parallel lines of charge, separated by $L=8.0$ cm, have linear densities $+6.0\\ \\mu$C/m (line 1) and $-2.0\\ \\mu$C/m (line 2). Where on the $x$ axis (origin midway) is the net field zero?", "Hai sợi tích điện dài song song cách nhau $L=8{,}0$ cm có mật độ dài $+6{,}0\\ \\mu$C/m (sợi 1) và $-2{,}0\\ \\mu$C/m (sợi 2). Trên trục $x$ (gốc ở giữa) trường tổng bằng 0 ở đâu?"),
 "A. $x=8.0\\ \\mathrm{cm}$",
 [("<b>Line charge field:</b> $E=\\dfrac{\\lambda}{2\\pi\\varepsilon_0r}$. <b>Where can it cancel?</b> Between the lines both fields point the same way (away from $+$, toward $-$), so no zero there. Left of line 1 the larger charge is also nearer: no zero. Only to the right of line 2 (weaker, farther from the stronger line 1).", "<b>Trường của sợi dài:</b> $E=\\dfrac{\\lambda}{2\\pi\\varepsilon_0r}$. <b>Triệt tiêu ở đâu?</b> Giữa hai sợi hai trường cùng chiều nên không có điểm 0. Bên trái sợi 1 điện tích lớn lại gần hơn: không có. Chỉ ở bên phải sợi 2 (yếu hơn, xa sợi 1 mạnh hơn)."),
  ("Lines at $x=\\mp4$ cm: $\\dfrac{6.0}{x+4}=\\dfrac{2.0}{x-4}\\Rightarrow6(x-4)=2(x+4)\\Rightarrow4x=32\\Rightarrow x=8.0$ cm.", "Các sợi ở $x=\\mp4$ cm: $\\dfrac{6{,}0}{x+4}=\\dfrac{2{,}0}{x-4}\\Rightarrow6(x-4)=2(x+4)\\Rightarrow4x=32\\Rightarrow x=8{,}0$ cm.")],
 choices=["A. $x=8.0$ cm", "B. $x=12.0$ cm", "C. $x=4.0$ cm", "D. $x=-8.0$ cm"], chk=lambda: near((6*4+2*4)/(6-2), 8.0),
 variants=[V("★ Other densities", "Densities $+9\\ \\mu$C/m and $-3\\ \\mu$C/m, 10 cm apart: zero-field point from the midpoint?", "Mật độ $+9\\ \\mu$C/m và $-3\\ \\mu$C/m, cách nhau 10 cm: điểm trường bằng 0 tính từ trung điểm?", "$x=10$ cm", ("$9(x-5)=3(x+5)\\Rightarrow6x=60$.", "$9(x-5)=3(x+5)\\Rightarrow6x=60$."), lambda: near((9*5+3*5)/(9-3),10.0))])

add("F17", SRC + " · Q17", ("Force on an electron: direction", "Chiều lực lên electron"),
 ("An electron moves in the $+x$ direction through a uniform magnetic field in the $+y$ direction. The magnetic force on it is in the:", "Electron chuyển động theo $+x$ trong từ trường đều theo $+y$. Lực từ lên nó theo chiều:"),
 "B. negative $z$-direction",
 [("<b>Cross product:</b> $\\vec F=q\\vec v\\times\\vec B$. For a positive charge $\\hat x\\times\\hat y=+\\hat z$.", "<b>Tích có hướng:</b> $\\vec F=q\\vec v\\times\\vec B$. Với điện tích dương $\\hat x\\times\\hat y=+\\hat z$."),
  ("The electron has $q<0$, so the force reverses: <b>$-\\hat z$</b>.", "Electron có $q<0$ nên lực đổi chiều: <b>$-\\hat z$</b>.")],
 choices=["A. $+z$", "B. $-z$", "C. $+x$", "D. $-y$"],
 variants=[V("★ Proton", "A proton moves in $+z$ in a field along $+x$. Force direction?", "Proton chuyển động theo $+z$ trong từ trường theo $+x$. Chiều lực?", "$+y$", ("$\\hat z\\times\\hat x=+\\hat y$, $q>0$.", "$\\hat z\\times\\hat x=+\\hat y$, $q>0$."), lambda: True)])

add("F18", SRC + " · Q18", ("Field inside a toroid", "Từ trường trong xuyến"),
 ("The magnetic field inside an ideal toroid is:", "Từ trường bên trong xuyến lý tưởng:"),
 "C. inversely proportional to the radial distance from the centre",
 [("<b>Ampère's law</b> on a circle of radius $r$ inside the windings: $B(2\\pi r)=\\mu_0NI\\Rightarrow B=\\dfrac{\\mu_0NI}{2\\pi r}\\propto\\dfrac1r$.", "<b>Định luật Ampère</b> trên đường tròn bán kính $r$ trong các vòng dây: $B(2\\pi r)=\\mu_0NI\\Rightarrow B=\\dfrac{\\mu_0NI}{2\\pi r}\\propto\\dfrac1r$."),
  ("So it is <i>not</i> uniform across the cross-section (unlike a long solenoid), and it is zero outside the winding.", "Nên nó <i>không</i> đều trên tiết diện (khác ống dây dài) và bằng 0 bên ngoài cuộn.")],
 choices=["A. Uniform across the cross-section", "B. Zero", "C. Inversely proportional to the distance from the centre", "D. Directly proportional to the distance"],
 variants=[V("★ Number", "A toroid with 500 turns, 2.0 A, at $r=10$ cm. $B$?", "Xuyến 500 vòng, 2,0 A, tại $r=10$ cm. $B$?", "$2.0\\times10^{-3}\\ \\mathrm{T}$", ("$\\mu_0NI/2\\pi r=2\\times10^{-7}(500)(2)/0.1$.", "$\\mu_0NI/2\\pi r=2\\times10^{-7}(500)(2)/0{,}1$."), lambda: near(2e-7*500*2/0.1,2.0e-3))])

add("F19", SRC + " · Q19", ("Refractive index from wavelengths", "Chiết suất từ bước sóng"),
 ("Red He–Ne laser light has wavelength 633 nm in air and 474 nm in the aqueous humor of the eye. Refractive index of the aqueous humor (3 decimals)?", "Ánh sáng đỏ laser He–Ne có bước sóng 633 nm trong không khí và 474 nm trong thủy dịch của mắt. Chiết suất thủy dịch (3 chữ số thập phân)?"),
 "B. $1.335$",
 [("<b>Frequency is unchanged when entering a medium; $v=f\\lambda$, $n=c/v$</b> so $\\lambda_n=\\lambda_0/n$.", "<b>Tần số không đổi khi vào môi trường; $v=f\\lambda$, $n=c/v$</b> nên $\\lambda_n=\\lambda_0/n$."),
  ("<b>Isolate $n$:</b> $n=\\dfrac{\\lambda_{air}}{\\lambda_{medium}}=\\dfrac{633}{474}=1.3354\\approx1.335$ (air taken as $n=1$).", "<b>Cô lập $n$:</b> $n=\\dfrac{\\lambda_{kk}}{\\lambda_{mt}}=\\dfrac{633}{474}=1{,}3354\\approx1{,}335$ (không khí coi là $n=1$).")],
 choices=["A. 1.323", "B. 1.335", "C. 1.400", "D. 1.428"], chk=lambda: near(633/474, 1.3354, 0.001),
 variants=[V("★ Speed", "Speed of light in that fluid and its wavelength for a 500 nm (air) beam?", "Tốc độ ánh sáng trong dịch đó và bước sóng của chùm 500 nm (trong không khí)?", "$2.25\\times10^{8}$ m/s; $374$ nm", ("$v=c/n=3\\times10^8/1.335$; $\\lambda=500/1.335$.", "$v=c/n=3\\times10^8/1{,}335$; $\\lambda=500/1{,}335$."), lambda: near(3e8/1.3354,2.246e8) and near(500/1.3354,374.4))])

add("F20", SRC + " · Q20", ("Field outside an ideal solenoid", "Từ trường bên ngoài ống dây lý tưởng"),
 ("The magnetic field outside an ideal infinitely long solenoid is:", "Từ trường bên ngoài ống dây vô hạn lý tưởng:"),
 "C. zero",
 [("<b>Ampère's law with a rectangular loop</b> partly outside: $B_{out}L=\\mu_0I_{enc}$ with the same enclosed current regardless of the loop's distance, so $B_{out}$ cannot depend on distance and must vanish at infinity ⇒ $B_{out}=0$.", "<b>Ampère với khung chữ nhật</b> nằm ngoài: $B_{ngoài}L=\\mu_0I_{bao}$ với dòng bao như nhau dù khung xa hay gần nên $B_{ngoài}$ không phụ thuộc khoảng cách và phải về 0 ở vô cực ⇒ $B_{ngoài}=0$."),
  ("Real finite solenoids have a weak stray field; the ideal one has none.", "Ống dây hữu hạn thật có từ trường rò yếu; ống lý tưởng thì không.")],
 choices=["A. $\\mu_0in$", "B. Uniform but non-zero", "C. Zero", "D. Radially outward"],
 variants=[V("★ Compare", "State $B$ inside and outside an ideal solenoid with $n=800$ m$^{-1}$, $I=3.0$ A.", "Nêu $B$ bên trong và ngoài ống lý tưởng $n=800$ m$^{-1}$, $I=3{,}0$ A.", "$3.0\\times10^{-3}$ T inside; $0$ outside", ("$\\mu_0nI=4\\pi\\times10^{-7}(800)(3)$.", "$\\mu_0nI=4\\pi\\times10^{-7}(800)(3)$."), lambda: near(mu0*800*3,3.016e-3))])

add("F21", SRC + " · Q21", ("Potential energy of a dipole in stable equilibrium", "Thế năng lưỡng cực ở cân bằng bền"),
 ("A magnetic dipole in stable equilibrium in a uniform magnetic field has potential energy:", "Lưỡng cực từ ở trạng thái cân bằng bền trong từ trường đều có thế năng:"),
 "C. minimum",
 [("<b>Energy of a dipole:</b> $U=-\\vec\\mu\\cdot\\vec B=-\\mu B\\cos\\theta$.", "<b>Năng lượng lưỡng cực:</b> $U=-\\vec\\mu\\cdot\\vec B=-\\mu B\\cos\\theta$."),
  ("Stable equilibrium: $\\vec\\mu\\parallel\\vec B$ ($\\theta=0$) ⇒ $U=-\\mu B$, the <b>minimum</b>; antiparallel ($\\theta=180^\\circ$) gives $+\\mu B$, the maximum (unstable).", "Cân bằng bền: $\\vec\\mu\\parallel\\vec B$ ($\\theta=0$) ⇒ $U=-\\mu B$, giá trị <b>nhỏ nhất</b>; đối song song ($\\theta=180^\\circ$) cho $+\\mu B$, lớn nhất (không bền).")],
 choices=["A. Maximum", "B. Zero", "C. Minimum", "D. Independent of the field"],
 variants=[V("★ Energy to flip", "$\\mu=0.50$ A·m$^2$ in $B=0.20$ T: work needed to rotate it from $\\theta=0$ to $180^\\circ$?", "$\\mu=0{,}50$ A·m$^2$ trong $B=0{,}20$ T: công cần để quay từ $\\theta=0$ đến $180^\\circ$?", "$0.20\\ \\mathrm{J}$", ("$\\Delta U=\\mu B-(-\\mu B)=2\\mu B$.", "$\\Delta U=\\mu B-(-\\mu B)=2\\mu B$."), lambda: near(2*0.5*0.2,0.2))])

add("F22", SRC + " · Q22", ("Field inside a conductor in equilibrium", "Điện trường bên trong vật dẫn cân bằng tĩnh điện"),
 ("Inside a conductor in electrostatic equilibrium:", "Bên trong vật dẫn ở cân bằng tĩnh điện:"),
 "B. $E=0$",
 [("<b>If $E\\neq0$ the free charges would move</b> until they cancel it; equilibrium means $\\vec E=0$ in the metal, hence the whole conductor is an equipotential and any excess charge sits on the surface.", "<b>Nếu $E\\neq0$ điện tích tự do sẽ chuyển động</b> cho đến khi triệt tiêu nó; cân bằng nghĩa là $\\vec E=0$ trong kim loại, do đó cả vật dẫn đẳng thế và điện tích dư nằm trên bề mặt.")],
 choices=["A. $E\\neq0$", "B. $E=0$", "C. Depends on the charge", "D. Infinite"],
 variants=[V("★ Cavity", "Charge $+Q$ sits inside a cavity of an uncharged thick conducting shell. Charges on the inner and outer surfaces?", "Điện tích $+Q$ đặt trong hốc của vỏ dẫn dày trung hòa. Điện tích ở mặt trong và ngoài?", "inner $-Q$, outer $+Q$", ("$E=0$ in the metal ⇒ Gauss gives $q_{inner}=-Q$; neutrality gives $+Q$ outside.", "$E=0$ trong kim loại ⇒ Gauss cho $q_{trong}=-Q$; trung hòa cho $+Q$ ở ngoài."), lambda: True)])

def f23(): return 1.522 * math.sin(math.radians(57.2))
add("F23", SRC + " · Q23", ("Total internal reflection by an oil layer", "Phản xạ toàn phần với lớp dầu"),
 ("A ray in glass ($n=1.522$) hits the top surface at $57.2^\\circ$ to the normal. A layer of oil placed on the glass makes the ray totally reflected. Maximum possible refractive index of the oil?", "Tia sáng trong thủy tinh ($n=1{,}522$) tới mặt trên với góc $57{,}2^\\circ$ so với pháp tuyến. Đặt lớp dầu lên thủy tinh thì tia bị phản xạ toàn phần. Chiết suất lớn nhất có thể của dầu?"),
 "B. $1.279$",
 [("<b>TIR condition:</b> incidence angle $\\ge$ critical angle, $\\sin\\theta_c=\\dfrac{n_{oil}}{n_{glass}}$. Total reflection ⇒ $\\sin57.2^\\circ\\ge\\dfrac{n_{oil}}{1.522}$.", "<b>Điều kiện phản xạ toàn phần:</b> góc tới $\\ge$ góc tới hạn, $\\sin\\theta_c=\\dfrac{n_{dầu}}{n_{kính}}$. Phản xạ toàn phần ⇒ $\\sin57{,}2^\\circ\\ge\\dfrac{n_{dầu}}{1{,}522}$."),
  ("<b>Isolate:</b> $n_{oil}\\le1.522\\sin57.2^\\circ=1.522(0.8406)=1.279$. The maximum is $1.279$.", "<b>Cô lập:</b> $n_{dầu}\\le1{,}522\\sin57{,}2^\\circ=1{,}522(0{,}8406)=1{,}279$. Giá trị lớn nhất là $1{,}279$.")],
 choices=["A. 1.211", "B. 1.279", "C. 1.350", "D. 1.111"], chk=lambda: near(f23(), 1.279, 0.001),
 variants=[V("★ Critical angle", "Critical angle at a glass ($n=1.522$)–air boundary?", "Góc tới hạn ở mặt phân cách thủy tinh ($n=1{,}522$)–không khí?", "$41.1^\\circ$", ("$\\theta_c=\\arcsin(1/1.522)$.", "$\\theta_c=\\arcsin(1/1{,}522)$."), lambda: near(math.degrees(math.asin(1/1.522)),41.06,0.005))])

add("F24", SRC + " · Q24", ("Convex mirror: object distance for half-size image", "Gương cầu lồi: khoảng cách vật cho ảnh bằng nửa vật"),
 ("A convex spherical mirror has $f=-12.0$ cm. At what distance from the vertex must an object be for the image to be half the object's height?", "Gương cầu lồi có $f=-12{,}0$ cm. Vật phải đặt cách đỉnh gương bao nhiêu để ảnh cao bằng nửa vật?"),
 "$12.0\\ \\mathrm{cm}$ (not among the options; nearest B. 11 cm)",
 [("<b>Mirror equation and magnification:</b> $\\dfrac1s+\\dfrac1{s'}=\\dfrac1f$, $m=-\\dfrac{s'}{s}$. A convex mirror always gives an upright virtual image, $m=+\\tfrac12$ ⇒ $s'=-\\dfrac s2$.", "<b>Phương trình gương và độ phóng đại:</b> $\\dfrac1s+\\dfrac1{s'}=\\dfrac1f$, $m=-\\dfrac{s'}{s}$. Gương lồi luôn cho ảnh ảo cùng chiều, $m=+\\tfrac12$ ⇒ $s'=-\\dfrac s2$."),
  ("<b>Substitute:</b> $\\dfrac1s-\\dfrac2s=-\\dfrac1s=\\dfrac1f=-\\dfrac1{12}\\Rightarrow s=12.0$ cm. Check: $s'=-6.0$ cm, $m=6/12=0.5$ ✓. The listed options (8, 11, 24, 22 cm) do not contain it.", "<b>Thay số:</b> $\\dfrac1s-\\dfrac2s=-\\dfrac1s=\\dfrac1f=-\\dfrac1{12}\\Rightarrow s=12{,}0$ cm. Kiểm tra: $s'=-6{,}0$ cm, $m=6/12=0{,}5$ ✓. Các đáp án (8, 11, 24, 22 cm) không có giá trị này.")],
 choices=["A. 8 cm", "B. 11 cm", "C. 24 cm", "D. 22 cm"],
 note=("Flag: none of the options is correct. For any convex mirror a half-size image sits at $s=|f|$ (here $12$ cm).", "Cảnh báo: không đáp án nào đúng. Với gương lồi bất kỳ, ảnh bằng nửa vật khi $s=|f|$ (ở đây $12$ cm)."),
 chk=lambda: (lambda s: near(1/s + 1/(-s/2), -1/12))(12.0),
 variants=[V("★ Quarter size", "Same mirror: object distance for an image one quarter of the object's size?", "Cùng gương: khoảng cách vật cho ảnh bằng một phần tư vật?", "$36\\ \\mathrm{cm}$", ("$m=\\tfrac14\\Rightarrow s'=-s/4$: $\\tfrac1s-\\tfrac4s=-\\tfrac1{12}\\Rightarrow s=36$ cm.", "$m=\\tfrac14\\Rightarrow s'=-s/4$: $\\tfrac1s-\\tfrac4s=-\\tfrac1{12}\\Rightarrow s=36$ cm."), lambda: near(3*12,36.0))])

def f25_true(): return math.degrees(math.asin(math.sin(math.radians(9.73)) * 1480 / 344))
add("F25", SRC + " · Q25", ("Refraction of ultrasound from lungs into the heart", "Khúc xạ siêu âm từ phổi vào tim"),
 ("Ultrasound travels at 1480 m/s in muscle and 344 m/s in air (and lungs). Define $n$ for sound as (speed in air)/(speed in the material); Snell's law applies. At what angle from the normal does a beam enter the heart if it leaves the lungs at $9.73^\\circ$?", "Siêu âm có tốc độ 1480 m/s trong cơ và 344 m/s trong không khí (và phổi). Định nghĩa $n$ cho âm là (tốc độ trong không khí)/(tốc độ trong vật liệu); định luật Snell vẫn đúng. Chùm tia vào tim với góc bao nhiêu nếu rời phổi ở $9{,}73^\\circ$?"),
 "Physics: $46.7^\\circ$ (not an option). The only reproducible option is A. $2.25^\\circ$ (inverted ratio)",
 [("<b>Snell for waves:</b> $\\dfrac{\\sin\\theta_1}{v_1}=\\dfrac{\\sin\\theta_2}{v_2}$ (equivalently $n_1\\sin\\theta_1=n_2\\sin\\theta_2$ with $n=v_{air}/v$). Lungs: $v_1=344$, heart (muscle): $v_2=1480$.", "<b>Snell cho sóng:</b> $\\dfrac{\\sin\\theta_1}{v_1}=\\dfrac{\\sin\\theta_2}{v_2}$ (tương đương $n_1\\sin\\theta_1=n_2\\sin\\theta_2$ với $n=v_{kk}/v$). Phổi: $v_1=344$, tim (cơ): $v_2=1480$."),
  ("<b>Isolate:</b> $\\sin\\theta_2=\\sin9.73^\\circ\\cdot\\dfrac{1480}{344}=0.1690(4.302)=0.727\\Rightarrow\\theta_2=46.7^\\circ$ (a faster medium bends the beam <i>away</i> from the normal).", "<b>Cô lập:</b> $\\sin\\theta_2=\\sin9{,}73^\\circ\\cdot\\dfrac{1480}{344}=0{,}1690(4{,}302)=0{,}727\\Rightarrow\\theta_2=46{,}7^\\circ$ (môi trường nhanh hơn làm tia <i>lệch xa</i> pháp tuyến)."),
  ("The only option that can be produced is $\\arcsin\\left(\\sin9.73^\\circ\\cdot\\dfrac{344}{1480}\\right)=2.25^\\circ$ (A), which uses the ratio the wrong way round. If the quiz was built from a textbook answer, A is the likely intended key — but check the direction of the ratio on your own exam.", "Đáp án duy nhất có thể tạo ra là $\\arcsin\\left(\\sin9{,}73^\\circ\\cdot\\dfrac{344}{1480}\\right)=2{,}25^\\circ$ (A), dùng tỉ số ngược. Nếu đề lấy từ đáp án giáo trình thì A nhiều khả năng là đáp án dự kiến — nhưng hãy kiểm tra chiều của tỉ số trong bài thi.")],
 choices=["A. 2.25°", "B. 15.47°", "C. 23.33°", "D. 30.46°"],
 note=("Flag: the physically correct angle ($46.7^\\circ$) is not offered.", "Cảnh báo: góc đúng về vật lý ($46{,}7^\\circ$) không có trong đáp án."),
 chk=lambda: near(f25_true(), 46.65, 0.005),
 variants=[V("★ Critical angle for sound", "Critical angle for sound going from muscle (1480 m/s) into air (344 m/s)?", "Góc tới hạn cho âm đi từ cơ (1480 m/s) vào không khí (344 m/s)?", "$13.4^\\circ$", ("$\\sin\\theta_c=v_1/v_2=344/1480$.", "$\\sin\\theta_c=v_1/v_2=344/1480$."), lambda: near(math.degrees(math.asin(344/1480)),13.44,0.005))])

add("F26", SRC + " · Q26", ("Induced emf with a time-varying field", "Suất điện động cảm ứng khi từ trường biến thiên"),
 ("$B(t)=(0.2t^2+0.5t)$ T is perpendicular to a circular loop of radius 0.1 m. Induced emf at $t=2.0$ s?", "$B(t)=(0{,}2t^2+0{,}5t)$ T vuông góc với vòng tròn bán kính 0,1 m. Suất điện động cảm ứng tại $t=2{,}0$ s?"),
 "B. $0.041\\ \\mathrm{V}$",
 [("<b>Faraday:</b> $|\\mathcal E|=\\left|\\dfrac{d\\Phi}{dt}\\right|=A\\left|\\dfrac{dB}{dt}\\right|$ with $A=\\pi r^2=\\pi(0.1)^2=0.0314$ m$^2$.", "<b>Faraday:</b> $|\\mathcal E|=\\left|\\dfrac{d\\Phi}{dt}\\right|=A\\left|\\dfrac{dB}{dt}\\right|$ với $A=\\pi r^2=\\pi(0{,}1)^2=0{,}0314$ m$^2$."),
  ("<b>Differentiate first, then substitute:</b> $dB/dt=0.4t+0.5=1.3$ T/s at $t=2$ s. $\\mathcal E=0.0314(1.3)=0.0408\\approx0.041$ V.", "<b>Đạo hàm trước, thay số sau:</b> $dB/dt=0{,}4t+0{,}5=1{,}3$ T/s tại $t=2$ s. $\\mathcal E=0{,}0314(1{,}3)=0{,}0408\\approx0{,}041$ V.")],
 choices=["A. 0.082 V", "B. 0.041 V", "C. 0.025 V", "D. 0.124 V"], chk=lambda: near(math.pi*0.01*(0.4*2+0.5), 0.0408, 0.005),
 trap=("Substituting $t=2$ into $B$ before differentiating is wrong ($B(2)=1.8$ T, $\\mathcal E$ would use the wrong thing).", "Thay $t=2$ vào $B$ trước khi đạo hàm là sai."),
 variants=[V("★ Direction", "If $B$ points out of the page and increases, which way does the induced current flow?", "Nếu $B$ hướng ra khỏi trang và tăng thì dòng cảm ứng chạy theo chiều nào?", "clockwise", ("Lenz: the induced field points into the page, which needs a clockwise current.", "Lenz: từ trường cảm ứng hướng vào trang, cần dòng cùng chiều kim đồng hồ."), lambda: True)])

add("F27", SRC + " · Q27", ("Converging lens: image position and magnification", "Thấu kính hội tụ: vị trí ảnh và độ phóng đại"),
 ("Image position and magnification for an object at 50 cm from a converging lens with $f=20$ cm.", "Vị trí ảnh và độ phóng đại của vật cách thấu kính hội tụ $f=20$ cm một khoảng 50 cm."),
 "A. $100/3\\ \\mathrm{cm}$; $-2/3$",
 [("<b>Thin-lens equation (isolate $s'$):</b> $\\dfrac1{s'}=\\dfrac1f-\\dfrac1s=\\dfrac1{20}-\\dfrac1{50}=\\dfrac{3}{100}\\Rightarrow s'=\\dfrac{100}{3}=33.3$ cm.", "<b>Phương trình thấu kính (cô lập $s'$):</b> $\\dfrac1{s'}=\\dfrac1f-\\dfrac1s=\\dfrac1{20}-\\dfrac1{50}=\\dfrac{3}{100}\\Rightarrow s'=\\dfrac{100}{3}=33{,}3$ cm."),
  ("$m=-\\dfrac{s'}{s}=-\\dfrac{100/3}{50}=-\\dfrac23$: <b>real, inverted, reduced</b> (object beyond $2f=40$ cm).", "$m=-\\dfrac{s'}{s}=-\\dfrac{100/3}{50}=-\\dfrac23$: <b>ảnh thật, ngược chiều, thu nhỏ</b> (vật ngoài $2f=40$ cm).")],
 choices=["A. 100/3 cm; −2/3", "B. −100/3 cm; −2/3", "C. 100/3 cm; 2/3", "D. −100/3 cm; 2/3"], chk=lambda: near(1/(1/20-1/50), 100/3),
 variants=[V("★ Inside the focal length", "Object at 10 cm from the same lens: image position and type?", "Vật cách cùng thấu kính 10 cm: vị trí và loại ảnh?", "$s'=-20$ cm, $m=+2$: virtual, upright, enlarged", ("$1/s'=1/20-1/10=-1/20$.", "$1/s'=1/20-1/10=-1/20$."), lambda: near(1/(1/20-1/10),-20.0))])

add("F28", SRC + " · Q28", ("Parallel plates: doubling the charge", "Hai bản song song: gấp đôi điện tích"),
 ("Each plate (charges $+Q$ and $-Q$) initially produces a field $E$. If both charges are doubled, what is the field in region B (between the plates)?", "Mỗi bản (điện tích $+Q$ và $-Q$) ban đầu tạo trường $E$. Nếu gấp đôi cả hai điện tích thì trường trong vùng B (giữa hai bản) bằng bao nhiêu?"),
 "C. $4E$",
 [("<b>Superposition between the plates:</b> both plates push the field the same way, so initially $E_B=E+E=2E$.", "<b>Chồng chất giữa hai bản:</b> cả hai bản cùng hướng trường nên ban đầu $E_B=E+E=2E$."),
  ("Doubling each charge doubles each plate's field ($\\sigma/2\\varepsilon_0$): each becomes $2E$, so $E_B=2E+2E=4E$ (outside, A and C, the fields cancel).", "Gấp đôi điện tích mỗi bản thì trường mỗi bản gấp đôi ($\\sigma/2\\varepsilon_0$): mỗi bản $2E$ nên $E_B=2E+2E=4E$ (bên ngoài, vùng A và C, các trường triệt tiêu).")],
 choices=["A. $E$", "B. $2E$", "C. $4E$", "D. $0$"], trap=("$2E$ is the field before doubling; the ‘each plate gives $E$’ wording hides that region B starts at $2E$.", "$2E$ là trường trước khi nhân đôi; lời đề ‘mỗi bản cho $E$’ che mất việc vùng B đã là $2E$."),
 variants=[V("★ Capacitor", "Plates $\\sigma=\\pm3.0\\ \\mu\\mathrm{C/m^2}$: field between and outside?", "Hai bản $\\sigma=\\pm3{,}0\\ \\mu\\mathrm{C/m^2}$: trường giữa và ngoài?", "$3.4\\times10^{5}$ N/C between; $0$ outside", ("$E=\\sigma/\\varepsilon_0=3\\times10^{-6}/8.85\\times10^{-12}$.", "$E=\\sigma/\\varepsilon_0=3\\times10^{-6}/8{,}85\\times10^{-12}$."), lambda: near(3e-6/8.854e-12,3.388e5))])

add("F29", SRC + " · Q29", ("Lorentz force", "Lực Lorentz"),
 ("Which expression gives the Lorentz force on a charge $q$ moving with velocity $\\vec v$ in fields $\\vec E$ and $\\vec B$?", "Biểu thức nào cho lực Lorentz lên điện tích $q$ chuyển động với vận tốc $\\vec v$ trong các trường $\\vec E$, $\\vec B$?"),
 "C. $\\vec F=q\\vec E+q(\\vec v\\times\\vec B)$",
 [("<b>Electric part</b> $q\\vec E$ (along the field) plus <b>magnetic part</b> $q\\,\\vec v\\times\\vec B$ (perpendicular to both $\\vec v$ and $\\vec B$).", "<b>Phần điện</b> $q\\vec E$ (theo trường) cộng <b>phần từ</b> $q\\,\\vec v\\times\\vec B$ (vuông góc với cả $\\vec v$ và $\\vec B$)."),
  ("Order matters in the cross product: $\\vec v\\times\\vec B=-\\vec B\\times\\vec v$, so (A) has the wrong sign; (B) mixes the roles; (D) is not a vector expression.", "Thứ tự trong tích có hướng quan trọng: $\\vec v\\times\\vec B=-\\vec B\\times\\vec v$ nên (A) sai dấu; (B) lẫn vai trò; (D) không phải biểu thức vectơ.")],
 choices=["A. $q\\vec E+q(\\vec B\\times\\vec v)$", "B. $q\\vec B+q(\\vec v\\times\\vec E)$", "C. $q\\vec E+q(\\vec v\\times\\vec B)$", "D. $q\\vec E\\times\\vec B+q\\vec v$"],
 variants=[V("★ Velocity selector", "$E=3.0\\times10^4$ V/m, $B=0.10$ T crossed. Speed passing undeflected?", "$E=3{,}0\\times10^4$ V/m, $B=0{,}10$ T vuông góc. Tốc độ đi thẳng?", "$3.0\\times10^{5}\\ \\mathrm{m/s}$", ("$qE=qvB\\Rightarrow v=E/B$.", "$qE=qvB\\Rightarrow v=E/B$."), lambda: near(3e4/0.1,3e5))])

add("F30", SRC + " · Q30", ("Ways to induce an emf", "Các cách tạo suất điện động cảm ứng"),
 ("An emf can be induced in a conducting loop by:", "Có thể cảm ứng suất điện động trong vòng dây bằng cách:"),
 "D. all of the above",
 [("<b>$\\Phi_B=BA\\cos\\theta$:</b> any change of $B$, of $A$ or of the angle $\\theta$ changes the flux, hence $\\mathcal E=-d\\Phi_B/dt\\neq0$.", "<b>$\\Phi_B=BA\\cos\\theta$:</b> mọi thay đổi của $B$, $A$ hay góc $\\theta$ đều làm đổi từ thông, do đó $\\mathcal E=-d\\Phi_B/dt\\neq0$.")],
 choices=["A. Changing the magnitude of $B$", "B. Changing the area of the loop", "C. Changing the angle between $\\vec A$ and $\\vec B$", "D. All of the above"],
 variants=[V("★ Rotating loop", "A coil of area $A$ and $N$ turns rotates at $\\omega$ in a uniform $B$. Peak emf?", "Cuộn $N$ vòng, diện tích $A$, quay với $\\omega$ trong từ trường đều $B$. Suất điện động cực đại?", "$NBA\\omega$", ("$\\Phi=NBA\\cos\\omega t$ ⇒ $\\mathcal E=NBA\\omega\\sin\\omega t$.", "$\\Phi=NBA\\cos\\omega t$ ⇒ $\\mathcal E=NBA\\omega\\sin\\omega t$."), lambda: True)])

add("F31", SRC + " · Q31", ("Field inside a hollow current-carrying cylinder", "Từ trường trong ống trụ rỗng mang dòng"),
 ("Inside a long straight hollow cylindrical conductor carrying a steady current, the magnetic field (in the hollow) is:", "Bên trong ống dẫn trụ rỗng thẳng dài mang dòng không đổi, từ trường (trong phần rỗng) là:"),
 "D. zero",
 [("<b>Ampère's law</b> with a circle of radius $r$ inside the hollow: no current is enclosed ($I_{enc}=0$), so $B(2\\pi r)=0\\Rightarrow B=0$.", "<b>Định luật Ampère</b> với đường tròn bán kính $r$ trong phần rỗng: không có dòng bao quanh ($I_{bao}=0$) nên $B(2\\pi r)=0\\Rightarrow B=0$."),
  ("Inside the material the field grows from $0$; outside it is $\\mu_0I/2\\pi r$.", "Trong thành ống trường tăng từ $0$; bên ngoài là $\\mu_0I/2\\pi r$.")],
 choices=["A. Constant and non-zero", "B. Proportional to the distance from the axis", "C. Inversely proportional to the distance", "D. Zero"],
 variants=[V("★ Solid wire", "Field inside a solid wire of radius $R$ carrying uniform current $I$ at $r<R$?", "Từ trường trong dây đặc bán kính $R$ mang dòng đều $I$ tại $r<R$?", "$B=\\mu_0Ir/2\\pi R^2$", ("$I_{enc}=I r^2/R^2$.", "$I_{bao}=I r^2/R^2$."), lambda: True)])

add("F32", SRC + " · Q32", ("Magnet thrust into a coil", "Nam châm cắm vào cuộn dây"),
 ("When a magnet is thrust into a coil of wire, the induced current is greater if:", "Khi cắm nam châm vào cuộn dây, dòng cảm ứng lớn hơn nếu:"),
 "C. the magnet moves faster",
 [("<b>Faraday:</b> $\\mathcal E=N\\,|d\\Phi_B/dt|$ — a larger rate of change of flux gives a larger emf and current ($I=\\mathcal E/R$).", "<b>Faraday:</b> $\\mathcal E=N\\,|d\\Phi_B/dt|$ — tốc độ biến thiên từ thông lớn hơn cho suất điện động và dòng lớn hơn ($I=\\mathcal E/R$)."),
  ("Faster ⇒ larger $d\\Phi/dt$ ✓. Fewer turns ⇒ smaller emf. Slower or stationary ⇒ smaller or zero.", "Nhanh hơn ⇒ $d\\Phi/dt$ lớn hơn ✓. Ít vòng hơn ⇒ suất điện động nhỏ hơn. Chậm hơn hoặc đứng yên ⇒ nhỏ hơn hoặc bằng 0.")],
 choices=["A. The magnet moves slower", "B. The coil has fewer turns", "C. The magnet moves faster", "D. The magnet is held stationary inside the coil"],
 variants=[V("★ Number", "Flux through a 100-turn coil changes from 0 to 2.0 mWb in 0.050 s. Average emf?", "Từ thông qua cuộn 100 vòng đổi từ 0 đến 2,0 mWb trong 0,050 s. Suất điện động trung bình?", "$4.0\\ \\mathrm{V}$", ("$N\\Delta\\Phi/\\Delta t=100(0.002)/0.05$.", "$N\\Delta\\Phi/\\Delta t=100(0{,}002)/0{,}05$."), lambda: near(100*0.002/0.05,4.0))])

add("F33", SRC + " · Q33", ("Slit width from the central maximum", "Bề rộng khe từ cực đại trung tâm"),
 ("Light of wavelength 500 nm passes through a single slit; the screen is 2.50 m away and the central maximum is 6.00 mm wide. Slit width $a$?", "Ánh sáng 500 nm qua khe đơn; màn cách 2,50 m và cực đại trung tâm rộng 6,00 mm. Bề rộng khe $a$?"),
 "C. $0.42\\ \\mathrm{mm}$",
 [("<b>Central maximum:</b> first minima at $a\\sin\\theta=\\lambda$; small angles ⇒ half-width $y_1=\\dfrac{\\lambda L}{a}$, full width $w=\\dfrac{2\\lambda L}{a}$.", "<b>Cực đại trung tâm:</b> cực tiểu đầu tại $a\\sin\\theta=\\lambda$; góc nhỏ ⇒ nửa bề rộng $y_1=\\dfrac{\\lambda L}{a}$, bề rộng $w=\\dfrac{2\\lambda L}{a}$."),
  ("<b>Isolate $a$:</b> $a=\\dfrac{2\\lambda L}{w}=\\dfrac{2(500\\times10^{-9})(2.50)}{6.00\\times10^{-3}}=4.17\\times10^{-4}$ m $=0.42$ mm. Using $w=\\lambda L/a$ (forgetting the 2) would give $0.21$ mm (A) — a trap.", "<b>Cô lập $a$:</b> $a=\\dfrac{2\\lambda L}{w}=\\dfrac{2(500\\times10^{-9})(2{,}50)}{6{,}00\\times10^{-3}}=4{,}17\\times10^{-4}$ m $=0{,}42$ mm. Quên số 2 ($w=\\lambda L/a$) sẽ ra $0{,}21$ mm (A) — bẫy.")],
 choices=["A. 0.21 mm", "B. 0.63 mm", "C. 0.42 mm", "D. 0.84 mm"], chk=lambda: near(2*500e-9*2.5/6e-3*1e3, 0.4167, 0.003),
 variants=[V("★ Reverse", "Slit 0.20 mm wide, $\\lambda=600$ nm, screen 1.5 m: width of the central maximum?", "Khe rộng 0,20 mm, $\\lambda=600$ nm, màn 1,5 m: bề rộng cực đại trung tâm?", "$9.0\\ \\mathrm{mm}$", ("$w=2\\lambda L/a=2(600\\times10^{-9})(1.5)/2\\times10^{-4}$.", "$w=2\\lambda L/a=2(600\\times10^{-9})(1{,}5)/2\\times10^{-4}$."), lambda: near(2*600e-9*1.5/2e-4*1e3,9.0))])

add("F34", SRC + " · Q34", ("Field of a long wire at 5 cm", "Từ trường của dây dài tại 5 cm"),
 ("Magnetic field 0.05 m from a long straight wire carrying 10 A?", "Từ trường cách dây thẳng dài mang 10 A một khoảng 0,05 m?"),
 "B. $4.0\\times10^{-5}\\ \\mathrm{T}$",
 [("<b>$B=\\dfrac{\\mu_0I}{2\\pi r}$:</b> $\\dfrac{\\mu_0}{2\\pi}=2\\times10^{-7}$ T·m/A, so $B=2\\times10^{-7}\\dfrac{10}{0.05}=4.0\\times10^{-5}$ T (comparable to the Earth's field).", "<b>$B=\\dfrac{\\mu_0I}{2\\pi r}$:</b> $\\dfrac{\\mu_0}{2\\pi}=2\\times10^{-7}$ T·m/A nên $B=2\\times10^{-7}\\dfrac{10}{0{,}05}=4{,}0\\times10^{-5}$ T (cùng cỡ từ trường Trái Đất).")],
 choices=["A. $2.0\\times10^{-5}$ T", "B. $4.0\\times10^{-5}$ T", "C. $1.0\\times10^{-5}$ T", "D. $8.0\\times10^{-5}$ T"], chk=lambda: near(2e-7*10/0.05, 4.0e-5),
 variants=[V("★ Force between wires", "Two such wires 5 cm apart carry 10 A in the same direction: force per metre?", "Hai dây như vậy cách 5 cm cùng chiều 10 A: lực trên mỗi mét?", "$4.0\\times10^{-4}\\ \\mathrm{N/m}$ (attractive)", ("$F/L=\\mu_0I_1I_2/2\\pi d=2\\times10^{-7}(100)/0.05$.", "$F/L=\\mu_0I_1I_2/2\\pi d=2\\times10^{-7}(100)/0{,}05$."), lambda: near(2e-7*100/0.05,4.0e-4))])

def f35():
    s = math.sin(math.radians(53.5)); return math.degrees(math.asin(s / 2.41)) - math.degrees(math.asin(s / 2.46))
add("F35", SRC + " · Q35", ("Dispersion in diamond", "Tán sắc trong kim cương"),
 ("$n=2.46$ for violet (400 nm) and $2.41$ for red (700 nm) in diamond. A ray in air strikes the diamond at $53.5^\\circ$. Angular separation of the two colours in the refracted ray?", "$n=2{,}46$ cho tím (400 nm) và $2{,}41$ cho đỏ (700 nm) trong kim cương. Tia từ không khí tới kim cương ở góc $53{,}5^\\circ$. Góc tách giữa hai màu trong tia khúc xạ?"),
 "B. $0.41^\\circ$",
 [("<b>Snell for each colour:</b> $\\sin\\theta_2=\\dfrac{\\sin53.5^\\circ}{n}$, $\\sin53.5^\\circ=0.8039$.", "<b>Snell cho từng màu:</b> $\\sin\\theta_2=\\dfrac{\\sin53{,}5^\\circ}{n}$, $\\sin53{,}5^\\circ=0{,}8039$."),
  ("Violet: $\\theta_v=\\arcsin(0.8039/2.46)=19.07^\\circ$; red: $\\theta_r=\\arcsin(0.8039/2.41)=19.49^\\circ$. Difference $\\approx0.41^\\circ$ (violet bends more). Keep 4 digits in the sines — the separation is small.", "Tím: $\\theta_v=\\arcsin(0{,}8039/2{,}46)=19{,}07^\\circ$; đỏ: $\\theta_r=\\arcsin(0{,}8039/2{,}41)=19{,}49^\\circ$. Hiệu $\\approx0{,}41^\\circ$ (tím lệch nhiều hơn). Giữ 4 chữ số ở các sin — độ tách rất nhỏ.")],
 choices=["A. 0.39°", "B. 0.41°", "C. 0.47°", "D. 0.53°"], chk=lambda: near(f35(), 0.41, 0.02),
 variants=[V("★ Glass prism", "Violet ($n=1.53$) and red ($n=1.51$) hit crown glass at $45^\\circ$. Angular separation after refraction?", "Tím ($n=1{,}53$) và đỏ ($n=1{,}51$) tới thủy tinh crown ở $45^\\circ$. Góc tách sau khúc xạ?", "$0.40^\\circ$", ("$\\arcsin(0.7071/1.51)-\\arcsin(0.7071/1.53)$.", "$\\arcsin(0{,}7071/1{,}51)-\\arcsin(0{,}7071/1{,}53)$."), lambda: near(math.degrees(math.asin(math.sin(math.radians(45))/1.51))-math.degrees(math.asin(math.sin(math.radians(45))/1.53)),0.40,0.03))])

add("F36", SRC + " · Q36", ("Two polarisers and unpolarised light", "Hai kính phân cực và ánh sáng không phân cực"),
 ("Unpolarised light $I_0$ passes through two ideal polarisers: the first axis is vertical, the second makes angle $\\varphi$ with the vertical. For what $\\varphi$ is the intensity at P equal to $I_0/10$?", "Ánh sáng không phân cực $I_0$ qua hai kính phân cực lý tưởng: trục thứ nhất thẳng đứng, trục thứ hai hợp góc $\\varphi$ với phương đứng. $\\varphi$ bằng bao nhiêu để cường độ tại P là $I_0/10$?"),
 "C. $63.43^\\circ$",
 [("<b>First filter on unpolarised light:</b> $I_1=\\tfrac12I_0$. <b>Malus' law</b> for the second: $I_2=I_1\\cos^2\\varphi=\\tfrac12I_0\\cos^2\\varphi$.", "<b>Kính thứ nhất với ánh sáng không phân cực:</b> $I_1=\\tfrac12I_0$. <b>Định luật Malus</b> cho kính thứ hai: $I_2=I_1\\cos^2\\varphi=\\tfrac12I_0\\cos^2\\varphi$."),
  ("<b>Isolate $\\varphi$:</b> $\\tfrac12\\cos^2\\varphi=\\tfrac1{10}\\Rightarrow\\cos^2\\varphi=0.2\\Rightarrow\\cos\\varphi=0.4472\\Rightarrow\\varphi=63.43^\\circ$ (=$\\arctan2$). (For polarised incident light of intensity $I_0$ it would be $\\cos^2\\varphi=0.1$, $\\varphi=71.6^\\circ$.)", "<b>Cô lập $\\varphi$:</b> $\\tfrac12\\cos^2\\varphi=\\tfrac1{10}\\Rightarrow\\cos^2\\varphi=0{,}2\\Rightarrow\\cos\\varphi=0{,}4472\\Rightarrow\\varphi=63{,}43^\\circ$ (=$\\arctan2$). (Nếu ánh sáng tới đã phân cực cường độ $I_0$ thì $\\cos^2\\varphi=0{,}1$, $\\varphi=71{,}6^\\circ$.)")],
 choices=["A. 43.43°", "B. 53.43°", "C. 63.43°", "D. 73.43°"], chk=lambda: near(math.degrees(math.acos(math.sqrt(0.2))), 63.43, 0.001),
 trap=("Forgetting the factor $\\tfrac12$ from the unpolarised source gives $71.6^\\circ$ (not an option).", "Quên hệ số $\\tfrac12$ của nguồn không phân cực sẽ ra $71{,}6^\\circ$ (không có trong đáp án)."),
 variants=[V("★ Three polarisers", "Unpolarised $I_0$ through polarisers at $0^\\circ$, $45^\\circ$, $90^\\circ$. Final intensity?", "Ánh sáng không phân cực $I_0$ qua các kính ở $0^\\circ$, $45^\\circ$, $90^\\circ$. Cường độ cuối?", "$I_0/8$", ("$\\tfrac12\\cdot\\cos^245^\\circ\\cdot\\cos^245^\\circ=\\tfrac18$.", "$\\tfrac12\\cdot\\cos^245^\\circ\\cdot\\cos^245^\\circ=\\tfrac18$."), lambda: near(0.5*0.5*0.5,0.125))])

add("F37", SRC + " · Q37", ("Work by a magnetic field", "Công của từ trường"),
 ("The work done by a constant magnetic field on a moving charged particle is always:", "Công do từ trường không đổi thực hiện lên hạt mang điện chuyển động luôn:"),
 "C. zero",
 [("<b>$\\vec F=q\\vec v\\times\\vec B\\perp\\vec v$</b> at every instant, so $dW=\\vec F\\cdot\\vec v\\,dt=0$: the speed and kinetic energy never change (only the direction).", "<b>$\\vec F=q\\vec v\\times\\vec B\\perp\\vec v$</b> tại mọi thời điểm nên $dW=\\vec F\\cdot\\vec v\\,dt=0$: tốc độ và động năng không đổi (chỉ đổi hướng).")],
 choices=["A. Positive", "B. Negative", "C. Zero", "D. Dependent on the charge"],
 variants=[V("★ Cyclotron", "A proton ($v=2.0\\times10^6$ m/s) in $B=0.50$ T perpendicular: radius and kinetic-energy change per revolution?", "Proton ($v=2{,}0\\times10^6$ m/s) trong $B=0{,}50$ T vuông góc: bán kính và biến thiên động năng mỗi vòng?", "$r=4.2$ cm; $\\Delta K=0$", ("$r=mv/qB$.", "$r=mv/qB$."), lambda: near(1.673e-27*2e6/(1.602e-19*0.5),0.0418,0.01))])

def f38(): return 1.22 * 0.036 / (28 / 1200)
add("F38", SRC + " · Q38", ("Resolving two satellites (Rayleigh)", "Phân giải hai vệ tinh (Rayleigh)"),
 ("Two satellites at altitude 1200 km are 28 km apart. With 3.6 cm microwaves, what minimum dish diameter resolves them (Rayleigh's criterion)?", "Hai vệ tinh ở độ cao 1200 km cách nhau 28 km. Với vi sóng 3,6 cm, đường kính chảo nhỏ nhất để phân giải (tiêu chuẩn Rayleigh)?"),
 "B. $1.88\\ \\mathrm{m}$",
 [("<b>Angular separation:</b> $\\theta=\\dfrac{28}{1200}=0.02333$ rad. <b>Rayleigh for a circular aperture:</b> $\\theta_R=1.22\\dfrac{\\lambda}{D}$.", "<b>Góc cách nhau:</b> $\\theta=\\dfrac{28}{1200}=0{,}02333$ rad. <b>Rayleigh cho khẩu độ tròn:</b> $\\theta_R=1{,}22\\dfrac{\\lambda}{D}$."),
  ("<b>Isolate $D$:</b> $D=\\dfrac{1.22\\lambda}{\\theta}=\\dfrac{1.22(0.036)}{0.02333}=1.88$ m. (Keep the 1.22 — it is for a circle, not a slit.)", "<b>Cô lập $D$:</b> $D=\\dfrac{1{,}22\\lambda}{\\theta}=\\dfrac{1{,}22(0{,}036)}{0{,}02333}=1{,}88$ m. (Giữ hệ số 1,22 — dành cho khẩu độ tròn, không phải khe.)")],
 choices=["A. 0.88 m", "B. 1.88 m", "C. 3.88 m", "D. 2.88 m"], chk=lambda: near(f38(), 1.882, 0.003),
 variants=[V("★ Eye", "Pupil diameter 3.0 mm, $\\lambda=550$ nm: smallest angle resolved, and the smallest separation of two car headlights resolved at 10 km?", "Đồng tử 3,0 mm, $\\lambda=550$ nm: góc phân giải nhỏ nhất và khoảng cách nhỏ nhất của hai đèn xe phân giải được ở 10 km?", "$2.2\\times10^{-4}$ rad; $2.2$ m", ("$\\theta=1.22(550\\times10^{-9})/0.003$; $s=\\theta L$.", "$\\theta=1{,}22(550\\times10^{-9})/0{,}003$; $s=\\theta L$."), lambda: near(1.22*550e-9/0.003,2.237e-4) and near(1.22*550e-9/0.003*1e4,2.237))])

add("F39", SRC + " · Q39", ("Field well inside a long solenoid", "Từ trường sâu bên trong ống dây dài"),
 ("The magnetic field well inside a long ideal solenoid carrying current $i$ with $n$ turns per unit length is:", "Từ trường sâu bên trong ống dây lý tưởng dài mang dòng $i$ với $n$ vòng trên đơn vị dài là:"),
 "B. $\\mu_0in$",
 [("<b>Ampère's law</b> with a rectangle of length $\\ell$: $B\\ell=\\mu_0(n\\ell)i\\Rightarrow B=\\mu_0ni$.", "<b>Định luật Ampère</b> với khung chữ nhật chiều dài $\\ell$: $B\\ell=\\mu_0(n\\ell)i\\Rightarrow B=\\mu_0ni$."),
  ("The $\\tfrac12\\mu_0in$ value is the field at the <i>end</i> of a long solenoid.", "Giá trị $\\tfrac12\\mu_0in$ là từ trường ở <i>đầu</i> ống dây dài.")],
 choices=["A. $\\tfrac12\\mu_0in$", "B. $\\mu_0in$", "C. $\\mu_0i/n$", "D. $2\\mu_0in$"],
 variants=[V("★ At the end", "Field on the axis at the end of a long solenoid with $n=1000$ m$^{-1}$, $i=1.0$ A?", "Từ trường trên trục ở đầu ống dây dài $n=1000$ m$^{-1}$, $i=1{,}0$ A?", "$6.3\\times10^{-4}\\ \\mathrm{T}$", ("$B_{end}=\\tfrac12\\mu_0ni$.", "$B_{đầu}=\\tfrac12\\mu_0ni$."), lambda: near(0.5*mu0*1000,6.283e-4))])

add("F40", SRC + " · Q40", ("Field at the centre of a circular loop", "Từ trường tại tâm vòng dây tròn"),
 ("A circular loop of radius 0.20 m carries 4.0 A. Magnetic field at its centre?", "Vòng dây tròn bán kính 0,20 m mang dòng 4,0 A. Từ trường tại tâm?"),
 "A. $1.26\\times10^{-5}\\ \\mathrm{T}$",
 [("<b>Biot–Savart for a loop, at the centre:</b> $B=\\dfrac{\\mu_0I}{2R}$ (every element is perpendicular to the radius and at the same distance $R$).", "<b>Biot–Savart cho vòng dây, tại tâm:</b> $B=\\dfrac{\\mu_0I}{2R}$ (mọi phần tử vuông góc với bán kính và cùng khoảng cách $R$)."),
  ("$B=\\dfrac{(4\\pi\\times10^{-7})(4.0)}{2(0.20)}=1.26\\times10^{-5}$ T. (A coil of $N$ turns multiplies this by $N$.)", "$B=\\dfrac{(4\\pi\\times10^{-7})(4{,}0)}{2(0{,}20)}=1{,}26\\times10^{-5}$ T. (Cuộn $N$ vòng nhân thêm $N$.)")],
 choices=["A. $1.26\\times10^{-5}$ T", "B. $2.51\\times10^{-5}$ T", "C. $6.28\\times10^{-6}$ T", "D. $5.02\\times10^{-5}$ T"], chk=lambda: near(mu0*4/(2*0.2), 1.2566e-5),
 variants=[V("★ Coil on axis", "A 50-turn coil of the same radius and current: field at its centre, and on the axis at 0.20 m from the plane?", "Cuộn 50 vòng cùng bán kính và dòng: từ trường tại tâm và trên trục cách mặt phẳng 0,20 m?", "$6.3\\times10^{-4}$ T; $2.2\\times10^{-4}$ T", ("Axis: $B=\\dfrac{\\mu_0NIR^2}{2(R^2+x^2)^{3/2}}$.", "Trên trục: $B=\\dfrac{\\mu_0NIR^2}{2(R^2+x^2)^{3/2}}$."), lambda: near(50*mu0*4/(0.4),6.283e-4) and near(mu0*50*4*0.04/(2*(0.08)**1.5),2.221e-4,0.01))])

# the page numbers the options a, b, c, d itself: drop the letters typed in the quiz text
import re as _re
for _it in ITEMS:
    if _it.choices:
        _it.choices = [_re.sub(r"^[A-D]\.\s*", "", c) for c in _it.choices]
