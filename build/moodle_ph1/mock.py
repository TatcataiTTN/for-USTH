# -*- coding: utf-8 -*-
"""Physics I, Moodle 'Mocktest Midterm' (20 questions, key shown in the quiz). Every numeric answer is recomputed (chk); figures that did not load are noted."""
from moodle_la.common import *
import math
g = 9.81
ITEMS = []
SRC = "Mocktest Midterm (PHY1.001, Moodle)"
def kmh(v): return v / 3.6

# ---------------- M01
def m01():
    vbar = kmh(85); v0 = kmh(110); v = 2 * vbar - v0; t = 120 / vbar
    return (v - v0) / t
ITEMS.append(I("M01", SRC + " · Q1", ("Speed trap: constant deceleration", "Bẫy tốc độ: giảm tốc đều"),
 ("Two strips 120 m apart on a road with limit 85 km/h. A driver at 110 km/h slows down immediately at the first strip. What deceleration makes the average speed equal to the limit at the second strip?",
  "Hai dải cảm biến cách nhau 120 m trên đường giới hạn 85 km/h. Tài xế đang chạy 110 km/h bắt đầu giảm tốc ngay tại dải đầu. Gia tốc nào làm vận tốc trung bình bằng giới hạn khi qua dải thứ hai?"),
 "$-2.73\\ \\mathrm{m/s^2}$",
 [("<b>Convert units first:</b> $85\\ \\mathrm{km/h}=23.61\\ \\mathrm{m/s}$, $110\\ \\mathrm{km/h}=30.56\\ \\mathrm{m/s}$. For constant acceleration the average speed is $\\bar v=\\frac{v_0+v}{2}$, so $v=2\\bar v-v_0=2(23.61)-30.56=16.67\\ \\mathrm{m/s}$.",
   "<b>Đổi đơn vị trước:</b> $85\\ \\mathrm{km/h}=23.61\\ \\mathrm{m/s}$, $110\\ \\mathrm{km/h}=30.56\\ \\mathrm{m/s}$. Với gia tốc không đổi, vận tốc trung bình $\\bar v=\\frac{v_0+v}{2}$ nên $v=2\\bar v-v_0=2(23.61)-30.56=16.67\\ \\mathrm{m/s}$."),
  ("<b>Time and acceleration:</b> $t=d/\\bar v=120/23.61=5.08$ s, then $a=\\dfrac{v-v_0}{t}=\\dfrac{16.67-30.56}{5.08}=-2.73\\ \\mathrm{m/s^2}$. Second route: $a=\\dfrac{v^2-v_0^2}{2d}=\\dfrac{277.8-934.0}{240}=-2.73$ ✓.",
   "<b>Thời gian và gia tốc:</b> $t=d/\\bar v=120/23.61=5.08$ s, rồi $a=\\dfrac{v-v_0}{t}=\\dfrac{16.67-30.56}{5.08}=-2.73\\ \\mathrm{m/s^2}$. Cách hai: $a=\\dfrac{v^2-v_0^2}{2d}=\\dfrac{277.8-934.0}{240}=-2.73$ ✓.")],
 choices=["$-2.73\\ \\mathrm{m/s^2}$", "$2.73\\ \\mathrm{m/s^2}$", "$5.46\\ \\mathrm{m/s^2}$", "$-5.46\\ \\mathrm{m/s^2}$"],
 trap=("The sign is negative because the axis points along the motion (deceleration). $5.46$ is exactly double: it comes from using $v_{avg}=v_0-\\ldots$ wrongly.", "Dấu âm vì trục dọc theo chuyển động (giảm tốc). $5.46$ gấp đôi: do dùng sai công thức vận tốc trung bình."),
 chk=lambda: near(m01(), -2.73), 
 variants=[V("★ Same idea", "Limit 60 km/h, strips 80 m apart, driver at 90 km/h. Required constant deceleration?", "Giới hạn 60 km/h, hai dải cách 80 m, tài xế 90 km/h. Gia tốc cần thiết?", "$-3.47\\ \\mathrm{m/s^2}$",
   ("$\\bar v=16.67$ m/s, $v_0=25$ m/s, $v=2\\bar v-v_0=8.33$ m/s, $t=80/16.67=4.8$ s, $a=(8.33-25)/4.8=-3.47$.", "$\\bar v=16.67$ m/s, $v_0=25$ m/s, $v=2\\bar v-v_0=8.33$ m/s, $t=80/16.67=4.8$ s, $a=(8.33-25)/4.8=-3.47$."),
   lambda: near((2*kmh(60)-kmh(90)-kmh(90))/(80/kmh(60)), -3.472))]))

# ---------------- M02
def m02():
    vy = 200 * math.sin(math.radians(30)); return (vy + math.sqrt(vy**2 + 2 * g * 50)) / g
ITEMS.append(I("M02", SRC + " · Q2", ("Projectile fired from a cliff", "Vật ném từ vách đá"),
 ("A cannon on a 50 m cliff fires a ball at $v=200$ m/s, $30^\\circ$ above the horizontal, over the edge. How long is the ball in the air? (no air resistance)",
  "Một khẩu pháo trên vách đá cao 50 m bắn viên đạn với $v=200$ m/s, góc $30^\\circ$ so với phương ngang, qua mép vách. Viên đạn ở trên không bao lâu? (bỏ qua lực cản)"),
 "$20.88\\ \\mathrm{s}$",
 [("<b>Vertical motion only decides the time.</b> $v_{y0}=200\\sin30^\\circ=100$ m/s. Take the launch point as $y=0$, the ground at $y=-50$: $-50=100t-\\tfrac12gt^2$.", "<b>Chỉ chuyển động thẳng đứng quyết định thời gian.</b> $v_{y0}=200\\sin30^\\circ=100$ m/s. Lấy điểm bắn $y=0$, mặt đất $y=-50$: $-50=100t-\\tfrac12gt^2$."),
  ("Rearrange: $4.905t^2-100t-50=0$, so $t=\\dfrac{100+\\sqrt{100^2+4(4.905)(50)}}{2(4.905)}=\\dfrac{100+104.79}{9.81}=20.88$ s (keep the positive root).", "Biến đổi: $4.905t^2-100t-50=0$, nên $t=\\dfrac{100+\\sqrt{100^2+4(4.905)(50)}}{2(4.905)}=\\dfrac{100+104.79}{9.81}=20.88$ s (lấy nghiệm dương).")],
 choices=["$30.88$ s", "$28$ s", "$30.28$ s", "$20.88$ s"],
 trap=("Ignoring the cliff gives $2v_{y0}/g=20.39$ s; the extra $0.49$ s is the fall from the launch level to the ground.", "Bỏ qua vách đá cho $2v_{y0}/g=20.39$ s; $0.49$ s thêm là thời gian rơi từ mức bắn xuống đất."),
 chk=lambda: near(m02(), 20.88),
 variants=[V("★ Horizontal launch", "A ball is thrown horizontally at 25 m/s from a 45 m cliff. Time of flight and horizontal distance?", "Một quả bóng ném ngang 25 m/s từ vách cao 45 m. Thời gian bay và tầm xa?", "$t=3.03$ s, $x=75.7$ m",
   ("$t=\\sqrt{2h/g}=\\sqrt{90/9.81}=3.03$ s; $x=v_xt=25(3.03)=75.7$ m.", "$t=\\sqrt{2h/g}=\\sqrt{90/9.81}=3.03$ s; $x=v_xt=25(3.03)=75.7$ m."),
   lambda: near(math.sqrt(90/g), 3.029) and near(25*math.sqrt(90/g), 75.7))]))

# ---------------- M03
ITEMS.append(I("M03", SRC + " · Q3", ("Speed–time graph with air resistance", "Đồ thị tốc độ–thời gian có lực cản"),
 ("The speed–time graph of an object thrown downward through air rises steeply at first then flattens. Which sentence describes it best?", "Đồ thị tốc độ–thời gian của vật ném xuống trong không khí tăng nhanh lúc đầu rồi thoải dần. Câu nào mô tả đúng nhất?"),
 "It starts with an initial speed, accelerates at first, but the acceleration decreases until the speed becomes constant",
 [("<b>Slope of a $v$–$t$ graph = acceleration.</b> The curve begins above zero (initial speed) and is steep (large $a$), then its slope shrinks to zero.", "<b>Độ dốc đồ thị $v$–$t$ = gia tốc.</b> Đường cong bắt đầu trên 0 (có tốc độ đầu), dốc lớn (a lớn) rồi độ dốc giảm về 0."),
  ("Air drag grows with speed, so net force $mg-F_{drag}$ falls until it is zero: the object reaches <b>terminal speed</b> ($a=0$).", "Lực cản tăng theo tốc độ nên hợp lực $mg-F_{c}$ giảm tới 0: vật đạt <b>tốc độ giới hạn</b> ($a=0$).")],
 choices=["Starts with an initial speed, constant acceleration, speed increases linearly", "Starts from rest, constant acceleration, speed increases without limit", "Starts with an initial speed, accelerates at first, acceleration decreases until speed is constant", "Starts with zero speed, slows down, then stops"],
 trap=("Options (a),(b) describe motion in a vacuum (straight line). The graph starts above zero, so ‘from rest’ is wrong.", "Đáp án (a),(b) mô tả chuyển động trong chân không (đường thẳng). Đồ thị bắt đầu trên 0 nên ‘từ nghỉ’ là sai."),
 variants=[V("★ Conceptual", "Sketch description: the $v$–$t$ graph of an object dropped from rest (i) in vacuum, (ii) in air.", "Mô tả đồ thị $v$–$t$ của vật thả rơi từ nghỉ (i) trong chân không, (ii) trong không khí.", "(i) straight line from the origin, slope $g$; (ii) curve from the origin that flattens at $v_t$",
   ("In vacuum $a=g$ is constant; with drag $a$ decreases to $0$ at the terminal speed.", "Trong chân không $a=g$ không đổi; có lực cản thì $a$ giảm về $0$ ở tốc độ giới hạn."), lambda: True)]))

# ---------------- M04
ITEMS.append(I("M04", SRC + " · Q4", ("Ranking average speed from paths on a grid", "Xếp hạng tốc độ trung bình từ các đường đi trên lưới"),
 ("Four paths over an equally spaced grid are taken in the same time interval. Rank them by average speed, greatest first.", "Bốn đường đi trên lưới đều trong cùng một khoảng thời gian. Xếp hạng theo tốc độ trung bình, lớn nhất trước."),
 "$4>1=2>3$",
 [("<b>Figure missing in the PDF</b> (broken image), so the grid count cannot be repeated here. The method is the point: <b>average speed = total path length / time</b>.", "<b>Hình bị mất trong PDF</b> (ảnh lỗi) nên không đếm lại được ô lưới. Phương pháp mới quan trọng: <b>tốc độ trung bình = tổng độ dài quãng đường / thời gian</b>."),
  ("Same time for all paths ⇒ rank by <i>path length</i> (count grid segments along each curve), not by the straight distance between the end points. The quiz key is $4>1=2>3$: path 4 is longest, paths 1 and 2 tie, path 3 shortest.", "Cùng thời gian ⇒ xếp theo <i>độ dài đường đi</i> (đếm các đoạn lưới dọc theo mỗi đường cong), không phải khoảng cách thẳng giữa hai đầu. Đáp án: $4>1=2>3$.")],
 choices=["$4>1>2>3$", "$4>2>1>3$", "$4>1=2>3$", "$4=2>1>3$"],
 note=("Average <i>velocity</i> would use the displacement (same start and end ⇒ all equal); average <i>speed</i> uses the path length.", "Vận tốc trung bình dùng độ dịch chuyển (cùng đầu cuối ⇒ bằng nhau); tốc độ trung bình dùng độ dài đường đi."),
 variants=[V("★ Numbers", "Paths of 14, 10, 10 and 6 grid units, each unit 0.50 m, all taken in 2.0 s. Average speeds?", "Các đường dài 14, 10, 10 và 6 ô, mỗi ô 0,50 m, đều đi trong 2,0 s. Tốc độ trung bình?", "$3.5,\\ 2.5,\\ 2.5,\\ 1.5\\ \\mathrm{m/s}$",
   ("$\\bar v=\\dfrac{\\text{units}\\times0.5}{2.0}$.", "$\\bar v=\\dfrac{\\text{số ô}\\times0{,}5}{2{,}0}$."), lambda: [u*0.5/2.0 for u in (14,10,10,6)] == [3.5,2.5,2.5,1.5])]))

# ---------------- M05
ITEMS.append(I("M05", SRC + " · Q5", ("Contact force between two blocks", "Lực tiếp xúc giữa hai khối"),
 ("Blocks X (mass $m$) and Y (mass $3m$) touch on a smooth surface and are accelerated by a force $F$ applied to X. What is the magnitude of the force exerted by X on Y?", "Hai khối X (khối lượng $m$) và Y ($3m$) tiếp xúc trên mặt nhẵn, lực $F$ tác dụng lên X. Độ lớn lực X tác dụng lên Y?"),
 "$\\dfrac{3F}{4}$",
 [("<b>Treat both blocks as one system:</b> $a=\\dfrac{F}{m+3m}=\\dfrac{F}{4m}$.", "<b>Coi cả hai khối là một hệ:</b> $a=\\dfrac{F}{m+3m}=\\dfrac{F}{4m}$."),
  ("<b>Isolate Y:</b> the only horizontal force on Y is the push of X, so $F_{XY}=3m\\cdot a=3m\\cdot\\dfrac{F}{4m}=\\dfrac{3F}{4}$. (Check on X: $F-F_{XY}=ma\\Rightarrow F/4$ ✓, Newton's third law.)", "<b>Tách Y:</b> lực ngang duy nhất lên Y là lực đẩy của X nên $F_{XY}=3m\\cdot a=3m\\cdot\\dfrac{F}{4m}=\\dfrac{3F}{4}$. (Kiểm tra với X: $F-F_{XY}=ma\\Rightarrow F/4$ ✓, định luật 3.)")],
 choices=["$F/3$", "$F/4$", "$4F/3$", "$3F/4$"],
 trap=("$F/4$ is the force on X from Y's reaction, and the net force on X — not the force on Y.", "$F/4$ là hợp lực lên X, không phải lực lên Y."),
 chk=lambda: near(3*(1/4), 0.75),
 variants=[V("★★ Three blocks", "Blocks $m,\\ 2m,\\ 3m$ in a row on a smooth floor are pushed by $F$ on the first. Contact forces between 1–2 and 2–3?", "Ba khối $m,\\ 2m,\\ 3m$ nối tiếp trên sàn nhẵn, đẩy bằng $F$ lên khối đầu. Lực tiếp xúc giữa 1–2 và 2–3?", "$\\dfrac{5F}{6}$ and $\\dfrac{F}{2}$",
   ("$a=F/6m$. Force on blocks 2+3 $=5m\\cdot a=5F/6$; force on block 3 $=3m\\cdot a=F/2$.", "$a=F/6m$. Lực lên khối 2+3 $=5m\\cdot a=5F/6$; lực lên khối 3 $=3m\\cdot a=F/2$."), lambda: near(5/6,0.8333) and near(3/6,0.5))]))

# ---------------- M06
ITEMS.append(I("M06", SRC + " · Q6", ("Apparent weight in a lift", "Trọng lượng biểu kiến trong thang máy"),
 ("A 50 kg man stands on a scale in a lift that descends with acceleration 1.0 m/s$^2$ (downward). Scale reading? ($g=10$ N/kg)", "Người 50 kg đứng trên cân trong thang máy đi xuống với gia tốc 1,0 m/s$^2$ (hướng xuống). Số chỉ cân? ($g=10$ N/kg)"),
 "$450\\ \\mathrm{N}$",
 [("<b>Newton's second law, axis downward:</b> $mg-N=ma\\Rightarrow N=m(g-a)$.", "<b>Định luật 2 Newton, trục hướng xuống:</b> $mg-N=ma\\Rightarrow N=m(g-a)$."),
  ("$N=50(10-1.0)=450$ N. The scale reads the normal force, so it reads <i>less</i> than the true weight $500$ N.", "$N=50(10-1{,}0)=450$ N. Cân đo phản lực nên chỉ <i>nhỏ hơn</i> trọng lượng thật $500$ N.")],
 choices=["$450$ N", "$550$ N", "$500$ N", "$400$ N"],
 trap=("$550$ N is for a lift <i>accelerating upward</i>; $500$ N for constant velocity.", "$550$ N là khi thang <i>tăng tốc đi lên</i>; $500$ N khi chuyển động đều."),
 chk=lambda: 50*(10-1.0) == 450,
 variants=[V("★ Three cases", "Same man, $g=10$: scale reading when (i) going up with $a=2$ m/s$^2$ upward, (ii) at constant speed, (iii) in free fall.", "Cùng người, $g=10$: số chỉ cân khi (i) đi lên với $a=2$ m/s$^2$ hướng lên, (ii) chuyển động đều, (iii) rơi tự do.", "$600$ N; $500$ N; $0$ N", ("$N=m(g\\pm a)$, $N=0$ when $a=g$.", "$N=m(g\\pm a)$, $N=0$ khi $a=g$."), lambda: 50*(10+2)==600)]))

# ---------------- M07
ITEMS.append(I("M07", SRC + " · Q7", ("Free fall from a cloud", "Rơi tự do từ đám mây"),
 ("Raindrops fall 1700 m. If there were no air resistance, how fast would they hit the ground?", "Giọt mưa rơi từ độ cao 1700 m. Nếu không có lực cản không khí thì chúng chạm đất với tốc độ bao nhiêu?"),
 "$183\\ \\mathrm{m/s}$",
 [("<b>No time given ⇒ use $v^2=v_0^2+2gh$</b> with $v_0=0$: $v=\\sqrt{2gh}=\\sqrt{2(9.8)(1700)}=182.5\\approx183$ m/s.", "<b>Không cho thời gian ⇒ dùng $v^2=v_0^2+2gh$</b> với $v_0=0$: $v=\\sqrt{2gh}=\\sqrt{2(9{,}8)(1700)}=182{,}5\\approx183$ m/s."),
  ("Energy route: $mgh=\\tfrac12mv^2$ gives the same result. (Real raindrops reach only ~10 m/s because of drag.)", "Cách năng lượng: $mgh=\\tfrac12mv^2$ cho cùng kết quả. (Giọt mưa thật chỉ đạt ~10 m/s vì lực cản.)")],
 choices=["$183$ m/s", "$184$ m/s", "$180$ m/s", "$188$ m/s"],
 chk=lambda: near(math.sqrt(2*9.8*1700), 182.5),
 variants=[V("★ Reverse", "From what height must a stone fall to hit the ground at 30 m/s?", "Phải thả hòn đá từ độ cao nào để chạm đất với 30 m/s?", "$45.9\\ \\mathrm{m}$", ("$h=v^2/2g=900/19.62=45.9$ m.", "$h=v^2/2g=900/19{,}62=45{,}9$ m."), lambda: near(900/(2*g),45.87))]))

# ---------------- M08
ITEMS.append(I("M08", SRC + " · Q8", ("Newton's first law with friction", "Định luật 1 Newton có ma sát"),
 ("A box is pushed across horizontal ground at constant speed. If the push stops, the box will:", "Một thùng được đẩy trên mặt đất nằm ngang với tốc độ không đổi. Nếu ngừng đẩy, thùng sẽ:"),
 "start slowing down",
 [("Constant speed means the push equals the kinetic friction ($F=f$, net force $0$). Remove the push and only friction remains, directed against the motion.", "Tốc độ không đổi nghĩa là lực đẩy bằng ma sát trượt ($F=f$, hợp lực $0$). Bỏ lực đẩy, chỉ còn ma sát ngược chiều chuyển động."),
  ("Net force $\\neq0$ ⇒ acceleration opposite to velocity ⇒ it <b>starts slowing down at once</b> (not immediately stop, not constant speed).", "Hợp lực $\\neq0$ ⇒ gia tốc ngược chiều vận tốc ⇒ thùng <b>bắt đầu chậm dần ngay</b> (không dừng ngay, không giữ tốc độ).")],
 choices=["continue at constant speed", "stop immediately", "start slowing down", "move at constant speed for a while then slow down"],
 trap=("‘Objects need a force to keep moving’ is the Aristotle misconception; here the force needed is only to cancel friction.", "‘Vật cần lực để tiếp tục chuyển động’ là quan niệm sai; ở đây lực chỉ để cân bằng ma sát."),
 variants=[V("★ Numbers", "A 20 kg box slides at constant speed under a 40 N push. After the push stops, find its deceleration.", "Thùng 20 kg trượt đều dưới lực đẩy 40 N. Sau khi ngừng đẩy, tìm gia tốc chậm dần.", "$2\\ \\mathrm{m/s^2}$", ("$f=40$ N, $a=f/m=40/20=2$ m/s$^2$ opposite to the motion.", "$f=40$ N, $a=f/m=40/20=2$ m/s$^2$ ngược chiều chuyển động."), lambda: 40/20==2)]))

# ---------------- M09
def m09(mu_f=20.0):
    return (10*10 - mu_f) / 50
ITEMS.append(I("M09", SRC + " · Q9", ("Hanging mass pulling a block on a rough bench", "Vật treo kéo khối trên mặt nhám"),
 ("A 40 kg mass at rest on a rough bench is pulled by a 10 kg mass attached to it (string over a pulley). Friction on the 40 kg mass is 20 N. Speed of the 10 kg mass 2 s after release? ($g=10$)", "Khối 40 kg nằm yên trên bàn nhám được kéo bởi vật 10 kg nối qua ròng rọc. Ma sát lên khối 40 kg là 20 N. Tốc độ của vật 10 kg sau 2 s? ($g=10$)"),
 "$3.2\\ \\mathrm{m/s}$",
 [("<b>Figure missing</b>; the standard arrangement (10 kg hanging, 40 kg on the bench). <b>Treat the connected bodies as one system along the string:</b> driving force $m_2g=100$ N, opposing friction $20$ N, total mass $50$ kg.", "<b>Hình bị mất</b>; cách bố trí chuẩn (10 kg treo, 40 kg trên bàn). <b>Coi hệ nối dây là một:</b> lực kéo $m_2g=100$ N, ma sát $20$ N, tổng khối lượng $50$ kg."),
  ("$a=\\dfrac{100-20}{50}=1.6$ m/s$^2$; from rest $v=at=1.6(2)=3.2$ m/s.", "$a=\\dfrac{100-20}{50}=1{,}6$ m/s$^2$; từ nghỉ $v=at=1{,}6(2)=3{,}2$ m/s.")],
 choices=["$2.4$ m/s", "$3.2$ m/s", "$2$ m/s", "$4$ m/s"],
 chk=lambda: near(m09()*2, 3.2),
 variants=[V("★ Smooth bench", "Same masses but a frictionless bench. Acceleration and speed after 2 s?", "Cùng khối lượng nhưng bàn không ma sát. Gia tốc và tốc độ sau 2 s?", "$a=2\\ \\mathrm{m/s^2}$, $v=4\\ \\mathrm{m/s}$", ("$a=100/50=2$, $v=4$ m/s. (This is also what the exercises' Q27 gives for a smooth surface.)", "$a=100/50=2$, $v=4$ m/s. (Đây cũng là kết quả của câu Q27 trong bộ bài tập khi mặt nhẵn.)"), lambda: near(m09(0)*2,4.0)),
            V("★★ With a coefficient", "Friction coefficient $\\mu_k=0.10$ for the 40 kg block ($N=400$ N). Acceleration?", "Hệ số ma sát $\\mu_k=0{,}10$ cho khối 40 kg ($N=400$ N). Gia tốc?", "$1.2\\ \\mathrm{m/s^2}$", ("$f=0.1(400)=40$ N, $a=(100-40)/50=1.2$.", "$f=0{,}1(400)=40$ N, $a=(100-40)/50=1{,}2$."), lambda: near(m09(40.0),1.2))]))

# ---------------- M10
ITEMS.append(I("M10", SRC + " · Q10", ("Net force on a rocket sled", "Hợp lực lên xe trượt tên lửa"),
 ("A 500 kg rocket sled accelerates uniformly from rest to 1600 km/h in 1.8 s. Magnitude of the net force?", "Xe trượt tên lửa 500 kg tăng tốc đều từ nghỉ đến 1600 km/h trong 1,8 s. Độ lớn hợp lực?"),
 "$1.23\\times10^{5}\\ \\mathrm{N}$",
 [("<b>SI units:</b> $1600\\ \\mathrm{km/h}=444.4$ m/s. $a=\\dfrac{\\Delta v}{\\Delta t}=\\dfrac{444.4}{1.8}=246.9$ m/s$^2$ (about $25g$).", "<b>Đổi sang SI:</b> $1600\\ \\mathrm{km/h}=444{,}4$ m/s. $a=\\dfrac{\\Delta v}{\\Delta t}=\\dfrac{444{,}4}{1{,}8}=246{,}9$ m/s$^2$ (khoảng $25g$)."),
  ("$F=ma=500(246.9)=1.23\\times10^5$ N.", "$F=ma=500(246{,}9)=1{,}23\\times10^5$ N.")],
 choices=["$1.32\\times10^5$ N", "$1.23\\times10^5$ N", "$1.25\\times10^5$ N", "$1.35\\times10^5$ N"],
 trap=("Forgetting to convert km/h gives an answer off by a factor $3.6$.", "Quên đổi km/h sai hệ số $3{,}6$."),
 chk=lambda: near(500*kmh(1600)/1.8, 1.2346e5),
 variants=[V("★ Distance", "How far does the sled travel in those 1.8 s?", "Trong 1,8 s đó xe đi được bao xa?", "$400\\ \\mathrm{m}$", ("$d=\\tfrac12\\bar v t=\\tfrac12(444.4)(1.8)=400$ m.", "$d=\\tfrac12\\bar v t=\\tfrac12(444{,}4)(1{,}8)=400$ m."), lambda: near(0.5*kmh(1600)*1.8,400.0))]))

# ---------------- M11
ITEMS.append(I("M11", SRC + " · Q11", ("The bird and the two trains", "Con chim và hai đoàn tàu"),
 ("Two trains, each at 30 km/h, approach each other on the same track. A bird flying at 60 km/h shuttles between them when they are 60 km apart. Total distance flown by the bird before the trains collide?", "Hai đoàn tàu, mỗi tàu 30 km/h, chạy ngược chiều trên cùng đường ray. Con chim bay 60 km/h đi lại giữa hai tàu khi chúng cách nhau 60 km. Tổng quãng đường chim bay trước khi hai tàu gặp nhau?"),
 "$60\\ \\mathrm{km}$",
 [("<b>Do not sum the infinite zigzags.</b> Find the <i>time</i>: the gap closes at $30+30=60$ km/h, so $t=\\dfrac{60}{60}=1$ h.", "<b>Đừng cộng vô hạn đoạn zích zắc.</b> Tìm <i>thời gian</i>: khoảng cách giảm với tốc độ $30+30=60$ km/h nên $t=\\dfrac{60}{60}=1$ h."),
  ("The bird flies the whole time at constant speed: $d=vt=60(1)=60$ km.", "Chim bay suốt thời gian đó với tốc độ không đổi: $d=vt=60(1)=60$ km.")],
 choices=["$45$ km", "$50$ km", "$60$ km", "$55$ km"],
 chk=lambda: 60*(60/(30+30))==60,
 variants=[V("★ New numbers", "Trains 100 km apart at 40 km/h each, bird at 90 km/h. Distance flown by the bird?", "Hai tàu cách 100 km, mỗi tàu 40 km/h, chim 90 km/h. Quãng đường chim bay?", "$112.5\\ \\mathrm{km}$", ("$t=100/80=1.25$ h; $d=90(1.25)=112.5$ km.", "$t=100/80=1{,}25$ h; $d=90(1{,}25)=112{,}5$ km."), lambda: near(90*(100/80),112.5))]))

# ---------------- M12
def m12(g=9.8):
    t = 0.25; v = (2.0 - 0.5*g*t*t) / t; return v*v/(2*g)
ITEMS.append(I("M12", SRC + " · Q12", ("Flowerpot passing a window", "Chậu hoa bay qua cửa sổ"),
 ("A flowerpot sails up then down past a window 2.00 m tall; it is in view for a total of 0.50 s. How high above the window top does it rise?", "Chậu hoa bay lên rồi rơi xuống qua cửa sổ cao 2,00 m; nó nằm trong tầm nhìn tổng cộng 0,50 s. Nó lên cao hơn mép trên cửa sổ bao nhiêu?"),
 "$2.34\\ \\mathrm{m}$",
 [("<b>Use symmetry:</b> up and down take equal times, so the pot needs $0.25$ s to cross the window going down. With $v_{top}$ the speed at the window top: $2.00=v_{top}(0.25)+\\tfrac12(9.8)(0.25)^2\\Rightarrow v_{top}=6.78$ m/s.", "<b>Dùng tính đối xứng:</b> lên và xuống mất thời gian như nhau nên chậu cần $0{,}25$ s để qua cửa sổ khi rơi xuống. Với $v_{top}$ là tốc độ ở mép trên: $2{,}00=v_{top}(0{,}25)+\\tfrac12(9{,}8)(0{,}25)^2\\Rightarrow v_{top}=6{,}78$ m/s."),
  ("The extra height above the top: $h=\\dfrac{v_{top}^2}{2g}=\\dfrac{6.775^2}{19.6}=2.34$ m.", "Độ cao thêm trên mép trên: $h=\\dfrac{v_{top}^2}{2g}=\\dfrac{6{,}775^2}{19{,}6}=2{,}34$ m.")],
 choices=["$2.34$ m", "$2.42$ m", "$2$ m", "$2.14$ m"],
 chk=lambda: near(m12(), 2.342),
 variants=[V("★ New numbers", "Window 1.50 m tall, pot in view for a total of 0.40 s. How high above the window top does it rise?", "Cửa sổ cao 1,50 m, chậu nằm trong tầm nhìn tổng cộng 0,40 s. Nó lên cao hơn mép trên bao nhiêu?", "$1.31\\ \\mathrm{m}$ (computed below)",
   ("$t=0.20$ s, $v_{top}=(1.5-4.9(0.04))/0.2=6.52$ m/s, $h=v^2/2g=2.17$ m.", "$t=0{,}20$ s, $v_{top}=(1{,}5-4{,}9(0{,}04))/0{,}2=6{,}52$ m/s, $h=v^2/2g=2{,}17$ m."), lambda: True)]))
# fix the variant answer to the computed value
def _v12():
    t = 0.20; v = (1.5 - 0.5*9.8*t*t)/t; return v*v/(2*9.8)
ITEMS[-1].variants[0].ans = "$%.2f\\ \\mathrm{m}$" % _v12()
ITEMS[-1].variants[0].chk = lambda: near(_v12(), 2.169)

# ---------------- M13
ITEMS.append(I("M13", SRC + " · Q13", ("Reading an acceleration graph", "Đọc đồ thị gia tốc"),
 ("The graph gives $a(t)$ of a dog chasing another along an axis. In which indicated period does it move at constant speed?", "Đồ thị cho $a(t)$ của một con chó. Trong khoảng thời gian nào nó chuyển động với tốc độ không đổi?"),
 "E",
 [("<b>Constant speed ⇔ $a=0$</b> (no change in velocity). Look for the stretch where the curve lies <i>on the time axis</i> for a whole interval.", "<b>Tốc độ không đổi ⇔ $a=0$</b> (vận tốc không đổi). Tìm đoạn mà đường cong nằm <i>trên trục thời gian</i> suốt cả khoảng."),
  ("Only segment <b>E</b> is flat at $a=0$. At A–B and H the curve merely crosses zero at an instant (speed changing before and after), and C, G have non-zero constant $a$.", "Chỉ đoạn <b>E</b> nằm ngang ở $a=0$. Ở A–B và H đường chỉ cắt trục tại một thời điểm, còn C, G có $a$ không đổi nhưng khác 0.")],
 choices=["A", "C", "E", "H"],
 trap=("A constant <i>non-zero</i> $a$ (flat but off the axis) is uniform acceleration, not constant speed.", "$a$ không đổi nhưng <i>khác 0</i> là chuyển động biến đổi đều, không phải tốc độ không đổi."),
 variants=[V("★ Compare graphs", "What do constant-speed motion look like on the $x$–$t$, $v$–$t$ and $a$–$t$ graphs?", "Chuyển động đều trông thế nào trên đồ thị $x$–$t$, $v$–$t$, $a$–$t$?", "straight sloped line; horizontal line; $a=0$", ("$v=dx/dt$ constant, $a=dv/dt=0$.", "$v=dx/dt$ không đổi, $a=dv/dt=0$."), lambda: True)]))

# ---------------- M14
def m14():
    v0, vf, T = 5.0, -3.0, 4.0
    a = (vf - v0) / T; t0 = -v0 / a; up = 0.5*v0*t0; dn = 0.5*abs(vf)*(T - t0)
    return a, (up - dn) / T, up - dn, up + dn
ITEMS.append(I("M14", SRC + " · Q14", ("Average velocity and acceleration from a $v$–$t$ graph", "Vận tốc trung bình và gia tốc từ đồ thị $v$–$t$"),
 ("The $v$–$t$ graph is a straight line from $v=5$ m/s at $t=0$ to $v=-3$ m/s at $t=4$ s. Find the average velocity and the acceleration.", "Đồ thị $v$–$t$ là đường thẳng từ $v=5$ m/s lúc $t=0$ đến $v=-3$ m/s lúc $t=4$ s. Tìm vận tốc trung bình và gia tốc."),
 "$\\bar v=1.0\\ \\mathrm{m/s},\\ a=-2\\ \\mathrm{m/s^2}$",
 [("<b>Slope = acceleration:</b> $a=\\dfrac{-3-5}{4-0}=-2$ m/s$^2$.", "<b>Độ dốc = gia tốc:</b> $a=\\dfrac{-3-5}{4-0}=-2$ m/s$^2$."),
  ("<b>Area = displacement (signed):</b> $v=0$ at $t=2.5$ s. Area above: $\\tfrac12(5)(2.5)=6.25$ m; below: $\\tfrac12(3)(1.5)=2.25$ m. Displacement $=6.25-2.25=4.0$ m, so $\\bar v=\\dfrac{4.0}{4}=1.0$ m/s. Shortcut for uniform $a$: $\\bar v=\\dfrac{5+(-3)}{2}=1.0$ ✓.", "<b>Diện tích = độ dịch chuyển (có dấu):</b> $v=0$ tại $t=2{,}5$ s. Diện tích trên: $\\tfrac12(5)(2{,}5)=6{,}25$ m; dưới: $\\tfrac12(3)(1{,}5)=2{,}25$ m. Độ dịch chuyển $=4{,}0$ m nên $\\bar v=1{,}0$ m/s. Mẹo khi $a$ không đổi: $\\bar v=\\dfrac{5+(-3)}{2}=1{,}0$ ✓.")],
 choices=["$v=1.0$ m/s & $a=-2$ m/s$^2$", "$v=-1.0$ m/s & $a=-2$ m/s$^2$", "$v=-1.0$ m/s & $a=2$ m/s$^2$", "$v=1.0$ m/s & $a=2$ m/s$^2$"],
 trap=("The distance travelled is $6.25+2.25=8.5$ m; the <i>average speed</i> would be $2.125$ m/s, different from the average velocity.", "Quãng đường đi được là $6{,}25+2{,}25=8{,}5$ m; <i>tốc độ trung bình</i> $2{,}125$ m/s khác vận tốc trung bình."),
 chk=lambda: near(m14()[0], -2) and near(m14()[1], 1.0),
 variants=[V("★★ Distance vs displacement", "A line from $v=8$ m/s at $t=0$ to $v=-2$ m/s at $t=5$ s. Find $a$, displacement and total distance.", "Đường thẳng từ $v=8$ m/s lúc $t=0$ đến $v=-2$ m/s lúc $t=5$ s. Tìm $a$, độ dịch chuyển và quãng đường.", "$a=-2$ m/s$^2$; $15$ m; $17$ m",
   ("$a=-10/5=-2$; $v=0$ at $t=4$; areas $16$ and $-1$: displacement $15$ m, distance $17$ m.", "$a=-10/5=-2$; $v=0$ lúc $t=4$; diện tích $16$ và $-1$: độ dịch chuyển $15$ m, quãng đường $17$ m."), lambda: (lambda a: near(a,-2) and near(0.5*8*4-0.5*2*1,15) and near(0.5*8*4+0.5*2*1,17))((-2-8)/5))]))

# ---------------- M15
ITEMS.append(I("M15", SRC + " · Q15", ("Vertical acceleration of a projectile", "Gia tốc thẳng đứng của vật ném"),
 ("A ball projected from P follows a parabola; T is the highest point; air resistance is negligible. Which statement applies to the <i>vertical component of acceleration</i>?", "Quả bóng ném từ P theo parabol; T là điểm cao nhất; bỏ qua lực cản. Phát biểu nào đúng cho <i>thành phần gia tốc thẳng đứng</i>?"),
 "It is the same at P as at T",
 [("Once launched, the only force is gravity, so $\\vec a=(0,-g)$ <b>everywhere</b>: $a_x=0$ and $a_y=-g$ at every point.", "Sau khi ném, lực duy nhất là trọng lực nên $\\vec a=(0,-g)$ <b>tại mọi điểm</b>: $a_x=0$, $a_y=-g$."),
  ("At the top only $v_y=0$ (not $a_y$): velocity component vanishes, acceleration does not. So the vertical acceleration is the same at P and T.", "Ở đỉnh chỉ có $v_y=0$ (không phải $a_y$): thành phần vận tốc triệt tiêu, gia tốc thì không. Vậy gia tốc thẳng đứng bằng nhau ở P và T.")],
 choices=["It is zero at P", "It is zero at T", "It is the same at P as at T", "It is greatest at T"],
 trap=("Confusing $v_y=0$ at the peak with $a_y=0$ is the classic error.", "Nhầm $v_y=0$ ở đỉnh với $a_y=0$ là lỗi kinh điển."),
 variants=[V("★ Components at the top", "At the highest point of a projectile launched at $40^\\circ$ with $20$ m/s, find $v_x$, $v_y$, $a_x$, $a_y$.", "Tại điểm cao nhất của vật ném $20$ m/s, góc $40^\\circ$, tìm $v_x$, $v_y$, $a_x$, $a_y$.", "$v_x=15.3$ m/s, $v_y=0$, $a_x=0$, $a_y=-9.81$ m/s$^2$", ("$v_x=20\\cos40^\\circ=15.3$ m/s constant.", "$v_x=20\\cos40^\\circ=15{,}3$ m/s không đổi."), lambda: near(20*math.cos(math.radians(40)),15.32))]))

# ---------------- M16
ITEMS.append(I("M16", SRC + " · Q16", ("Rate of change of momentum", "Tốc độ biến thiên động lượng"),
 ("A body falls freely under gravity. Its rate of change of momentum equals:", "Một vật rơi tự do. Tốc độ biến thiên động lượng của nó bằng:"),
 "weight",
 [("<b>Newton's second law in momentum form:</b> $\\vec F_{net}=\\dfrac{d\\vec p}{dt}$.", "<b>Định luật 2 Newton dạng động lượng:</b> $\\vec F_{net}=\\dfrac{d\\vec p}{dt}$."),
  ("In free fall the only force is the weight $mg$, so $dp/dt=mg$. (Impulse is $\\int F\\,dt$, power is $F\\cdot v$, kinetic energy is $\\tfrac12mv^2$: none is $dp/dt$.)", "Khi rơi tự do lực duy nhất là trọng lượng $mg$ nên $dp/dt=mg$. (Xung lượng là $\\int F\\,dt$, công suất là $F\\cdot v$, động năng là $\\tfrac12mv^2$: đều khác $dp/dt$.)")],
 choices=["power", "impulse", "weight", "kinetic"],
 variants=[V("★ Numbers", "A 2 kg stone falls freely. Find $dp/dt$ and its momentum after 3 s.", "Hòn đá 2 kg rơi tự do. Tìm $dp/dt$ và động lượng sau 3 s.", "$19.6$ N; $58.9\\ \\mathrm{kg\\,m/s}$", ("$dp/dt=mg=19.62$ N; $p=mgt=58.9$.", "$dp/dt=mg=19{,}62$ N; $p=mgt=58{,}9$."), lambda: near(2*g*3,58.86))]))

# ---------------- M17
ITEMS.append(I("M17", SRC + " · Q17", ("Direction of travel from the sign of velocity", "Chiều chuyển động từ dấu của vận tốc"),
 ("The figure gives the velocity of a particle along an axis. Point 1 is the highest point of the curve, point 4 the lowest; points 2 and 6 are at the same height. What is the direction of travel at $t=0$ and at point 4?", "Hình cho vận tốc của một hạt trên một trục. Điểm 1 là điểm cao nhất, điểm 4 là điểm thấp nhất; điểm 2 và 6 cùng độ cao. Chiều chuyển động tại $t=0$ và tại điểm 4?"),
 "positive direction, negative direction",
 [("<b>Direction of travel = sign of the velocity.</b> Above the axis ⇒ positive direction; below the axis ⇒ negative direction.", "<b>Chiều chuyển động = dấu của vận tốc.</b> Trên trục ⇒ chiều dương; dưới trục ⇒ chiều âm."),
  ("At $t=0$ the curve is above the axis (positive); point 4 is described as the lowest point, below the axis (negative). Key: positive, negative.", "Tại $t=0$ đường cong nằm trên trục (dương); điểm 4 là điểm thấp nhất, dưới trục (âm). Đáp án: dương, âm.")],
 choices=["negative, positive", "negative, negative", "positive, positive", "positive, negative"],
 note=("The picture is labelled $a$ (acceleration) and shows point 4 on the axis, while the text speaks of velocity and calls point 4 the lowest point: the figure and text disagree. Follow the text; the key is (d).", "Hình ghi trục $a$ (gia tốc) và điểm 4 nằm trên trục, trong khi đề nói về vận tốc và gọi điểm 4 là điểm thấp nhất: hình và chữ không khớp. Theo chữ; đáp án (d)."),
 variants=[V("★ Reversal", "$v(t)=4-2t$ (m/s). When does the particle reverse direction and which way does it move at $t=3$ s?", "$v(t)=4-2t$ (m/s). Khi nào hạt đổi chiều và chuyển động theo chiều nào lúc $t=3$ s?", "at $t=2$ s; negative direction", ("$v=0$ at $t=2$; $v(3)=-2<0$.", "$v=0$ lúc $t=2$; $v(3)=-2<0$."), lambda: 4-2*2==0 and 4-2*3<0)]))

# ---------------- M18
ITEMS.append(I("M18", SRC + " · Q18", ("Girl and sled on frictionless ice", "Cô gái và xe trượt trên băng nhẵn"),
 ("A 40 kg girl and an 8.4 kg sled are on frictionless ice, 15 m apart, joined by a light rope. The girl pulls with a horizontal 5.2 N. How far from the girl's initial position do they meet?", "Cô gái 40 kg và xe trượt 8,4 kg ở trên băng không ma sát, cách nhau 15 m, nối bằng dây nhẹ. Cô kéo bằng lực ngang 5,2 N. Họ gặp nhau cách vị trí đầu của cô gái bao xa?"),
 "$2.6\\ \\mathrm{m}$",
 [("<b>Accelerations (equal and opposite force):</b> $a_g=5.2/40=0.130$ m/s$^2$, $a_s=5.2/8.4=0.619$ m/s$^2$. They meet when $x_g+x_s=15$; with the same $t$, $x\\propto a$.", "<b>Gia tốc (lực bằng nhau, ngược chiều):</b> $a_g=5{,}2/40=0{,}130$ m/s$^2$, $a_s=5{,}2/8{,}4=0{,}619$ m/s$^2$. Gặp nhau khi $x_g+x_s=15$; cùng $t$ nên $x\\propto a$."),
  ("$x_g=15\\cdot\\dfrac{a_g}{a_g+a_s}=15\\cdot\\dfrac{0.130}{0.749}=2.6$ m. Centre-of-mass check: it does not move, so $x_g=15\\dfrac{m_s}{m_g+m_s}=15\\dfrac{8.4}{48.4}=2.60$ m ✓.", "$x_g=15\\cdot\\dfrac{a_g}{a_g+a_s}=15\\cdot\\dfrac{0{,}130}{0{,}749}=2{,}6$ m. Kiểm tra bằng khối tâm: khối tâm đứng yên nên $x_g=15\\dfrac{m_s}{m_g+m_s}=15\\dfrac{8{,}4}{48{,}4}=2{,}60$ m ✓.")],
 choices=["$2.6$ m", "$2.4$ m", "$2.8$ m", "$2.2$ m"],
 trap=("The pulling force (5.2 N) does not matter for the meeting point — only the masses do.", "Độ lớn lực kéo (5,2 N) không ảnh hưởng đến điểm gặp — chỉ khối lượng quyết định."),
 chk=lambda: near(15*8.4/48.4, 2.603),
 variants=[V("★ Reverse masses", "A 60 kg skater and a 20 kg raft, 8 m apart, pull on each other with a rope. Where do they meet, measured from the skater?", "Người trượt 60 kg và bè 20 kg cách 8 m kéo nhau bằng dây. Họ gặp nhau cách vị trí người trượt bao xa?", "$2.0\\ \\mathrm{m}$", ("$x=8\\cdot\\dfrac{20}{80}=2.0$ m (the lighter body moves farther).", "$x=8\\cdot\\dfrac{20}{80}=2{,}0$ m (vật nhẹ hơn đi xa hơn)."), lambda: near(8*20/80,2.0))]))

# ---------------- M19
def m19():
    g_ = 9.8; v0 = g_ * 2.5; return v0 * 1.5 - 0.5 * g_ * 1.5**2
ITEMS.append(I("M19", SRC + " · Q19", ("Rock passing the top of a tower", "Hòn đá bay qua đỉnh tháp"),
 ("A rock is thrown vertically upward from the ground at $t=0$. At $t=1.5$ s it passes the top of a tall tower and 1.0 s later it reaches its maximum height. Height of the tower?", "Hòn đá ném thẳng đứng lên từ mặt đất lúc $t=0$. Lúc $t=1{,}5$ s nó qua đỉnh tháp và 1,0 s sau đạt độ cao cực đại. Chiều cao tháp?"),
 "$25.7\\ \\mathrm{m}$",
 [("<b>Apex at $t=2.5$ s</b> where $v=0$: $v_0=gt=9.8(2.5)=24.5$ m/s.", "<b>Điểm cao nhất lúc $t=2{,}5$ s</b> khi $v=0$: $v_0=gt=9{,}8(2{,}5)=24{,}5$ m/s."),
  ("Height at $t=1.5$ s: $y=v_0t-\\tfrac12gt^2=24.5(1.5)-4.9(2.25)=36.75-11.03=25.7$ m. Second route: apex height $30.6$ m minus the fall in the last $1.0$ s ($4.9$ m) $=25.7$ m ✓.", "Độ cao lúc $t=1{,}5$ s: $y=v_0t-\\tfrac12gt^2=24{,}5(1{,}5)-4{,}9(2{,}25)=36{,}75-11{,}03=25{,}7$ m. Cách hai: độ cao cực đại $30{,}6$ m trừ quãng rơi $1{,}0$ s cuối ($4{,}9$ m) $=25{,}7$ m ✓.")],
 choices=["$25.4$ m", "$25.7$ m", "$24.5$ m", "$27.5$ m"],
 chk=lambda: near(m19(), 25.73),
 variants=[V("★ New numbers", "Same set-up: passes the tower top at $t=2.0$ s and reaches the apex $0.8$ s later. Tower height?", "Cùng bài: qua đỉnh tháp lúc $t=2{,}0$ s và đạt điểm cao nhất sau $0{,}8$ s. Chiều cao tháp?", "$35.3\\ \\mathrm{m}$", ("$v_0=9.8(2.8)=27.44$; $y(2.0)=54.88-19.6=35.28$ m.", "$v_0=9{,}8(2{,}8)=27{,}44$; $y(2{,}0)=54{,}88-19{,}6=35{,}28$ m."), lambda: near(9.8*2.8*2-0.5*9.8*4,35.28))]))

# ---------------- M20
ITEMS.append(I("M20", SRC + " · Q20", ("Friction on a driven wheel", "Ma sát lên bánh xe được dẫn động"),
 ("A unicycle is being pedalled in the direction shown. Which force represents the frictional force on the wheel? (A: forward along the ground, B: up, C: backward, D: down)", "Xe một bánh đang được đạp theo chiều chuyển động. Lực nào là lực ma sát lên bánh xe? (A: hướng về phía trước dọc mặt đất, B: lên, C: ngược lại, D: xuống)"),
 "A (forward, in the direction of motion)",
 [("<b>Driven wheel:</b> the wheel pushes the ground <i>backward</i> at the contact point (no slipping).", "<b>Bánh được dẫn động:</b> bánh đẩy mặt đất <i>về phía sau</i> tại điểm tiếp xúc (không trượt)."),
  ("By Newton's third law the ground pushes the wheel <b>forward</b>: the friction on the wheel is in the direction of motion (this is the force that accelerates the bike). B is the normal force, D is the weight, C would be friction on a braking or free-rolling wheel.", "Theo định luật 3 mặt đất đẩy bánh <b>về phía trước</b>: ma sát lên bánh cùng chiều chuyển động (lực làm xe tăng tốc). B là phản lực, D là trọng lực, C là ma sát khi phanh hoặc bánh lăn tự do.")],
 choices=["B", "C", "A", "D"],
 trap=("‘Friction always opposes motion’ is false for the driving wheel: it opposes the <i>slipping</i> of the contact point, not the motion of the bike.", "‘Ma sát luôn cản chuyển động’ là sai với bánh dẫn động: nó chống lại sự <i>trượt</i> của điểm tiếp xúc."),
 variants=[V("★ Cases", "Direction of the friction force on the tyres of (i) an accelerating car, (ii) a braking car, (iii) a person's shoe while walking forward.", "Chiều lực ma sát lên lốp của (i) ô tô tăng tốc, (ii) ô tô phanh, (iii) đế giày khi đi bộ về phía trước.", "(i) forward; (ii) backward; (iii) forward", ("The friction is forward whenever the contact point is pushed backward.", "Ma sát hướng về phía trước khi điểm tiếp xúc bị đẩy về phía sau."), lambda: True)]))

for _it in ITEMS:
    if _it.id == "M04":
        _it.klabel = ("Official answer (quiz key; figure missing, not re-derived)", "Đáp án của đề (hình bị mất, chưa tự suy ra lại)")
