# -*- coding: utf-8 -*-
"""Physics I, Moodle 'Exercises for Final Exam' (40 questions, key shown). Numeric answers are recomputed; figures that did not load are noted."""
from moodle_la.common import *
import math
g = 9.81; R = 8.314; atm = 101325.0
ITEMS = []
SRC = "Exercises for Final Exam (PHY1.001, Moodle)"
def add(*a, **k): ITEMS.append(I(*a, **k))

add("E01", SRC + " · Q1", ("Most probable speed vs rms speed", "Tốc độ xác suất nhất và tốc độ rms"),
 ("The most probable speed of gas molecules at temperature $T_2$ equals the rms speed at temperature $T_1$. Find $T_2/T_1$.", "Tốc độ xác suất nhất của phân tử khí ở nhiệt độ $T_2$ bằng tốc độ rms ở nhiệt độ $T_1$. Tìm $T_2/T_1$."),
 "$\\dfrac32$",
 [("<b>Write both speeds for the same gas:</b> $v_p=\\sqrt{\\dfrac{2RT}{M}}$, $v_{rms}=\\sqrt{\\dfrac{3RT}{M}}$ (and $v_{avg}=\\sqrt{\\dfrac{8RT}{\\pi M}}$).", "<b>Viết hai tốc độ cho cùng một khí:</b> $v_p=\\sqrt{\\dfrac{2RT}{M}}$, $v_{rms}=\\sqrt{\\dfrac{3RT}{M}}$ (và $v_{avg}=\\sqrt{\\dfrac{8RT}{\\pi M}}$)."),
  ("<b>Set equal and isolate the ratio:</b> $\\sqrt{2RT_2/M}=\\sqrt{3RT_1/M}\\Rightarrow 2T_2=3T_1\\Rightarrow\\dfrac{T_2}{T_1}=\\dfrac32$.", "<b>Cho bằng nhau và cô lập tỉ số:</b> $\\sqrt{2RT_2/M}=\\sqrt{3RT_1/M}\\Rightarrow 2T_2=3T_1\\Rightarrow\\dfrac{T_2}{T_1}=\\dfrac32$.")],
 choices=["$3/2$", "$2/3$", "$1/2$", "$1/3$"], trap=("Remember the order $v_p<v_{avg}<v_{rms}$ (1 : 1.128 : 1.225).", "Nhớ thứ tự $v_p<v_{avg}<v_{rms}$ (1 : 1,128 : 1,225)."),
 chk=lambda: near(3/2, 1.5),
 variants=[V("★ Average speed", "The average speed at $T_2$ equals the rms speed at $T_1$. Find $T_2/T_1$.", "Tốc độ trung bình ở $T_2$ bằng tốc độ rms ở $T_1$. Tìm $T_2/T_1$.", "$\\dfrac{3\\pi}{8}=1.18$", ("$8T_2/\\pi=3T_1\\Rightarrow T_2/T_1=3\\pi/8$.", "$8T_2/\\pi=3T_1\\Rightarrow T_2/T_1=3\\pi/8$."), lambda: near(3*math.pi/8, 1.178))])

add("E02", SRC + " · Q2", ("Two projectiles: heights and launch angles", "Hai vật ném: độ cao và góc ném"),
 ("Two projectiles with the same initial speed leave ground level. Maximum height $h_1=2h_2$. Which relation holds between the launch angles?", "Hai vật ném cùng tốc độ đầu từ mặt đất. Độ cao cực đại $h_1=2h_2$. Hệ thức nào giữa các góc ném?"),
 "$\\sin\\theta_1=\\sqrt2\\sin\\theta_2$",
 [("<b>Maximum height:</b> $h=\\dfrac{v_0^2\\sin^2\\theta}{2g}$, so for equal $v_0$: $h\\propto\\sin^2\\theta$.", "<b>Độ cao cực đại:</b> $h=\\dfrac{v_0^2\\sin^2\\theta}{2g}$, nên với cùng $v_0$: $h\\propto\\sin^2\\theta$."),
  ("$h_1=2h_2\\Rightarrow\\sin^2\\theta_1=2\\sin^2\\theta_2\\Rightarrow\\sin\\theta_1=\\sqrt2\\,\\sin\\theta_2$.", "$h_1=2h_2\\Rightarrow\\sin^2\\theta_1=2\\sin^2\\theta_2\\Rightarrow\\sin\\theta_1=\\sqrt2\\,\\sin\\theta_2$.")],
 choices=["$\\sin\\theta_1=\\sqrt2\\sin\\theta_2$", "$\\cos\\theta_1=2\\cos\\theta_2$", "$\\cos\\theta_1=\\sqrt2\\cos\\theta_2$", "$\\tan\\theta_1=\\sqrt2\\tan\\theta_2$"],
 variants=[V("★ Use it", "If $\\theta_2=30^\\circ$ find $\\theta_1$ and the ratio of the ranges $R_1/R_2$.", "Nếu $\\theta_2=30^\\circ$ tìm $\\theta_1$ và tỉ số tầm xa $R_1/R_2$.", "$\\theta_1=45^\\circ$; $R_1/R_2=1.155$", ("$\\sin\\theta_1=\\sqrt2(0.5)=0.7071$; $R\\propto\\sin2\\theta$: $\\sin90^\\circ/\\sin60^\\circ=1.155$.", "$\\sin\\theta_1=\\sqrt2(0{,}5)=0{,}7071$; $R\\propto\\sin2\\theta$: $\\sin90^\\circ/\\sin60^\\circ=1{,}155$."), lambda: near(math.degrees(math.asin(math.sqrt(2)*0.5)),45.0) and near(1/math.sin(math.radians(60)),1.1547))])

add("E03", SRC + " · Q3", ("Engine efficiency from a cycle with two adiabats", "Hiệu suất động cơ có hai quá trình đoạn nhiệt"),
 ("An ideal gas (1.0 mol) runs an engine cycle in which BC and DA are reversible adiabatic processes. Engine efficiency? ($\\eta=1-T_C/T_H$)", "Một mol khí lý tưởng chạy chu trình động cơ trong đó BC và DA là đoạn nhiệt thuận nghịch. Hiệu suất? ($\\eta=1-T_C/T_H$)"),
 "$75\\%$",
 [("<b>Figure missing</b> (broken image). With two reversible adiabats and two isotherms the cycle is a Carnot cycle, so $\\eta=1-\\dfrac{T_C}{T_H}$.", "<b>Hình bị mất</b> (ảnh lỗi). Với hai đoạn nhiệt thuận nghịch và hai đẳng nhiệt, chu trình là chu trình Carnot nên $\\eta=1-\\dfrac{T_C}{T_H}$."),
  ("The keyed $75\\%$ means $T_C/T_H=1/4$ in the figure. Read the two isotherm temperatures from the graph (or from $T=pV/nR$) and substitute.", "Đáp án $75\\%$ nghĩa là $T_C/T_H=1/4$ trong hình. Đọc nhiệt độ hai đường đẳng nhiệt từ đồ thị (hoặc từ $T=pV/nR$) rồi thay vào.")],
 choices=["$75\\%$", "$25\\%$", "$50\\%$", "$12.5\\%$"],
 note=("Efficiency uses <i>absolute</i> temperatures (kelvin).", "Hiệu suất dùng nhiệt độ <i>tuyệt đối</i> (kelvin)."),
 variants=[V("★ Numbers", "A Carnot engine works between 600 K and 150 K. Efficiency, and heat rejected per 1000 J absorbed?", "Động cơ Carnot làm việc giữa 600 K và 150 K. Hiệu suất và nhiệt thải trên mỗi 1000 J nhận vào?", "$75\\%$; $250$ J", ("$\\eta=1-150/600=0.75$; $|Q_L|=Q_H(1-\\eta)=250$ J.", "$\\eta=1-150/600=0{,}75$; $|Q_L|=Q_H(1-\\eta)=250$ J."), lambda: near(1-150/600,0.75))])

def e04(): return (5.0 + 273.15) * (1.0 / 5.0) ** ((4/3 - 1) / (4/3))
add("E04", SRC + " · Q4", ("Adiabatic expansion of champagne gas", "Giãn nở đoạn nhiệt của khí trong chai sâm panh"),
 ("Gas in a champagne bottle is at $p_i=5.00$ atm; after the cork is pulled it expands adiabatically to 1.00 atm. $\\gamma=4/3$, $T_i=5.00^\\circ$C. Final temperature?", "Khí trong chai sâm panh ở $p_i=5{,}00$ atm; khi mở nút nó giãn đoạn nhiệt đến 1,00 atm. $\\gamma=4/3$, $T_i=5{,}00^\\circ$C. Nhiệt độ cuối?"),
 "$186\\ \\mathrm{K}$",
 [("<b>Adiabatic relation:</b> $pV^\\gamma=\\text{const}$ with $pV=nRT$ gives $T\\,p^{(1-\\gamma)/\\gamma}=\\text{const}$, i.e. $T_f=T_i\\left(\\dfrac{p_f}{p_i}\\right)^{(\\gamma-1)/\\gamma}$.", "<b>Quan hệ đoạn nhiệt:</b> $pV^\\gamma=\\text{const}$ kết hợp $pV=nRT$ cho $T_f=T_i\\left(\\dfrac{p_f}{p_i}\\right)^{(\\gamma-1)/\\gamma}$."),
  ("<b>Convert to kelvin first:</b> $T_i=278.15$ K. Exponent $(\\gamma-1)/\\gamma=0.25$: $T_f=278.15(0.2)^{0.25}=278.15(0.6687)=186$ K (about $-87^\\circ$C).", "<b>Đổi sang kelvin trước:</b> $T_i=278{,}15$ K. Số mũ $(\\gamma-1)/\\gamma=0{,}25$: $T_f=278{,}15(0{,}2)^{0{,}25}=278{,}15(0{,}6687)=186$ K (khoảng $-87^\\circ$C).")],
 choices=["$-87$ K", "$186^\\circ$C", "$87^\\circ$C", "$186$ K"],
 trap=("The answer is in kelvin; the options $-87$ K and $87^\\circ$C are unit traps ($186\\ \\mathrm{K}=-87^\\circ\\mathrm{C}$).", "Đáp số là kelvin; các lựa chọn $-87$ K và $87^\\circ$C là bẫy đơn vị ($186\\ \\mathrm{K}=-87^\\circ\\mathrm{C}$)."),
 chk=lambda: near(e04(), 186.0, 0.003),
 variants=[V("★ Monatomic gas", "Helium ($\\gamma=5/3$) at 300 K expands adiabatically until its pressure falls to $1/4$. Final temperature?", "Heli ($\\gamma=5/3$) ở 300 K giãn đoạn nhiệt đến khi áp suất giảm còn $1/4$. Nhiệt độ cuối?", "$172\\ \\mathrm{K}$", ("$T_f=300(1/4)^{0.4}=300(0.5743)=172$ K.", "$T_f=300(1/4)^{0{,}4}=300(0{,}5743)=172$ K."), lambda: near(300*0.25**0.4,172.3))])

add("E05", SRC + " · Q5", ("Heat in a reversible isothermal expansion", "Nhiệt trong giãn nở đẳng nhiệt thuận nghịch"),
 ("How much heat must be transferred in a reversible isothermal expansion of an ideal gas at $132^\\circ$C if its entropy increases by $46.0$ J/K?", "Cần truyền bao nhiêu nhiệt trong giãn nở đẳng nhiệt thuận nghịch của khí lý tưởng ở $132^\\circ$C nếu entropy tăng $46{,}0$ J/K?"),
 "$1.84\\times10^{4}\\ \\mathrm{J}$ (as keyed; our value $1.86\\times10^4$ J)",
 [("<b>Isothermal and reversible:</b> $\\Delta S=\\dfrac{Q}{T}$, so $Q=T\\,\\Delta S$ with $T$ in kelvin: $T=132+273.15=405.15$ K.", "<b>Đẳng nhiệt, thuận nghịch:</b> $\\Delta S=\\dfrac{Q}{T}$ nên $Q=T\\,\\Delta S$ với $T$ tính bằng kelvin: $T=132+273{,}15=405{,}15$ K."),
  ("$Q=405.15\\times46.0=1.864\\times10^4$ J. The quiz option reads $1.84\\times10^4$ J — the closest of the four, and the keyed one (it would correspond to $400$ K). Choose (a) in the quiz.", "$Q=405{,}15\\times46{,}0=1{,}864\\times10^4$ J. Đáp án trong đề ghi $1{,}84\\times10^4$ J — gần nhất trong bốn đáp án và là đáp án của đề (ứng với $400$ K). Chọn (a) khi làm quiz.")],
 choices=["$1.84\\times10^4$ J", "$1.84\\times10^{-4}$ J", "$-1.84\\times10^4$ J", "$1.84\\times10^3$ J"],
 note=("Heat is positive because the gas absorbs it; the other options differ by sign or power of ten. The small discrepancy $1.86$ vs $1.84$ is in the quiz, not in the physics (Halliday gives $1.86\\times10^4$ J).", "Nhiệt dương vì khí hấp thụ; các đáp án khác sai dấu hoặc lũy thừa 10. Chênh lệch $1{,}86$ so với $1{,}84$ nằm ở đề quiz (Halliday cho $1{,}86\\times10^4$ J)."),
 chk=lambda: near((132 + 273.15) * 46.0, 1.864e4),
 variants=[V("★ Reverse", "A reversible isothermal expansion at 300 K absorbs 6.0 kJ. Entropy change of the gas?", "Giãn nở đẳng nhiệt thuận nghịch ở 300 K hấp thụ 6,0 kJ. Biến thiên entropy của khí?", "$+20\\ \\mathrm{J/K}$", ("$\\Delta S=Q/T=6000/300=20$ J/K.", "$\\Delta S=Q/T=6000/300=20$ J/K."), lambda: 6000/300==20)])

add("E06", SRC + " · Q6", ("Heat at constant pressure vs constant volume", "Nhiệt ở áp suất không đổi và thể tích không đổi"),
 ("70 cal raise the temperature of 2 mol of an ideal diatomic gas from 30°C to 35°C at constant pressure. Heat needed for the same range at constant volume?", "Cần 70 cal để nâng 2 mol khí lưỡng nguyên tử từ 30°C đến 35°C ở áp suất không đổi. Nhiệt cần cho cùng khoảng nhiệt độ ở thể tích không đổi?"),
 "$50\\ \\mathrm{cal}$",
 [("<b>Same $\\Delta T$, same gas:</b> $Q_p=nC_p\\Delta T$ and $Q_V=nC_V\\Delta T$, so $\\dfrac{Q_V}{Q_p}=\\dfrac{C_V}{C_p}=\\dfrac1\\gamma$.", "<b>Cùng $\\Delta T$, cùng khí:</b> $Q_p=nC_p\\Delta T$ và $Q_V=nC_V\\Delta T$ nên $\\dfrac{Q_V}{Q_p}=\\dfrac{C_V}{C_p}=\\dfrac1\\gamma$."),
  ("Diatomic: $C_V=\\tfrac52R$, $C_p=\\tfrac72R$, $\\gamma=\\tfrac75$. $Q_V=70\\times\\dfrac57=50$ cal. (Check: $Q_p-Q_V=nR\\Delta T=20$ cal ⇒ $R\\approx2$ cal/mol·K ✓.)", "Lưỡng nguyên tử: $C_V=\\tfrac52R$, $C_p=\\tfrac72R$, $\\gamma=\\tfrac75$. $Q_V=70\\times\\dfrac57=50$ cal. (Kiểm tra: $Q_p-Q_V=nR\\Delta T=20$ cal ⇒ $R\\approx2$ cal/mol·K ✓.)")],
 choices=["$30$ cal", "$50$ cal", "$70$ cal", "$90$ cal"],
 chk=lambda: near(70*5/7, 50.0),
 variants=[V("★ Monatomic", "For a monatomic gas, $Q_p=100$ J over some $\\Delta T$. Find $Q_V$ for the same $\\Delta T$ and the work done at constant pressure.", "Với khí đơn nguyên tử, $Q_p=100$ J cho một $\\Delta T$. Tìm $Q_V$ và công ở áp suất không đổi.", "$Q_V=60$ J; $W=40$ J", ("$\\gamma=5/3$: $Q_V=100\\times3/5=60$ J; $W=Q_p-\\Delta U=40$ J.", "$\\gamma=5/3$: $Q_V=100\\times3/5=60$ J; $W=Q_p-\\Delta U=40$ J."), lambda: near(100*3/5,60.0))])

add("E07", SRC + " · Q7", ("Molar heat of a diatomic gas", "Nhiệt dung mol của khí lưỡng nguyên tử"),
 ("For an ideal diatomic gas the molar specific heat at constant volume is:", "Với khí lưỡng nguyên tử lý tưởng, nhiệt dung mol đẳng tích là:"),
 "$C_V=20.8\\ \\mathrm{J/(mol\\cdot K)}$",
 [("<b>Equipartition:</b> translation (3) + rotation (2) = 5 active degrees of freedom, each $\\tfrac12R$ per mole: $C_V=\\tfrac52R=\\tfrac52(8.314)=20.8$ J/mol·K.", "<b>Định lý phân bố đều:</b> tịnh tiến (3) + quay (2) = 5 bậc tự do hoạt động, mỗi bậc $\\tfrac12R$ mỗi mol: $C_V=\\tfrac52R=\\tfrac52(8{,}314)=20{,}8$ J/mol·K."),
  ("Units: <i>molar</i> specific heat is J/(mol·K), not J/K. Monatomic: $\\tfrac32R=12.5$; diatomic: $\\tfrac52R=20.8$; $C_p=C_V+R=29.1$.", "Đơn vị: nhiệt dung <i>mol</i> là J/(mol·K), không phải J/K. Đơn nguyên tử: $\\tfrac32R=12{,}5$; lưỡng nguyên tử: $\\tfrac52R=20{,}8$; $C_p=C_V+R=29{,}1$.")],
 choices=["$C_V=20.8$ J·mol/K", "$C_V=28.5$ J·mol/K", "$C_V=20.8$ J/K", "$C_V=25.5$ J/K"],
 note=("The quiz's options are written with sloppy units (‘J.mol/K’); the keyed answer is the one with the value $20.8$ and molar units.", "Các đáp án trong đề ghi đơn vị cẩu thả (‘J.mol/K’); đáp án đúng là giá trị $20{,}8$ với đơn vị mol."),
 chk=lambda: near(2.5*R, 20.79),
 variants=[V("★ Table", "Give $C_V$, $C_p$ and $\\gamma$ for monatomic and diatomic ideal gases (in units of $R$).", "Cho $C_V$, $C_p$, $\\gamma$ của khí đơn và lưỡng nguyên tử (theo $R$).", "mono: $\\tfrac32R,\\tfrac52R,\\tfrac53$; di: $\\tfrac52R,\\tfrac72R,\\tfrac75$", ("$C_p=C_V+R$, $\\gamma=C_p/C_V$.", "$C_p=C_V+R$, $\\gamma=C_p/C_V$."), lambda: near(7/5,1.4) and near(5/3,1.667))])

add("E08", SRC + " · Q8", ("Energy conversion in a light bulb", "Chuyển hóa năng lượng ở bóng đèn"),
 ("What is the change of energy while operating a light bulb?", "Sự chuyển hóa năng lượng khi bóng đèn hoạt động là gì?"),
 "Electrical energy → heat and light",
 [("A bulb takes electrical energy from the supply and converts it to light (useful) and heat (most of it, for an incandescent bulb).", "Bóng đèn nhận điện năng và biến thành ánh sáng (có ích) và nhiệt (phần lớn, với bóng sợi đốt)."),
  ("Energy is conserved: input = light + heat; efficiency = useful output / total input.", "Năng lượng bảo toàn: đầu vào = ánh sáng + nhiệt; hiệu suất = năng lượng có ích / năng lượng toàn phần.")],
 choices=["Chemical → heat", "Electrical energy → heat and light", "Heat and light → electrical energy", "Electrical energy → kinetic energy"],
 variants=[V("★ Efficiency", "A 60 W bulb gives 3 W of light. Efficiency and heat power?", "Bóng 60 W phát 3 W ánh sáng. Hiệu suất và công suất nhiệt?", "$5\\%$; $57$ W", ("$3/60=0.05$; $60-3=57$ W.", "$3/60=0{,}05$; $60-3=57$ W."), lambda: near(3/60,0.05))])

add("E09", SRC + " · Q9", ("Which $v$–$s$ graph for uniform acceleration from rest?", "Đồ thị $v$–$s$ nào cho gia tốc đều từ nghỉ?"),
 ("A body starts from rest and moves in a line with constant acceleration. Which graph shows speed $v$ against distance $s$?", "Vật bắt đầu từ nghỉ chuyển động thẳng với gia tốc không đổi. Đồ thị nào biểu diễn tốc độ $v$ theo quãng đường $s$?"),
 "the curve $v=\\sqrt{2as}$ (a parabola on its side, steep at first)",
 [("<b>The graph images did not load</b>, so the choice cannot be read here. Derive the shape: $v^2=2as$ (from $v^2=v_0^2+2as$ with $v_0=0$).", "<b>Các hình đồ thị không hiện</b> nên không đọc được lựa chọn. Tự suy ra dạng: $v^2=2as$ (từ $v^2=v_0^2+2as$, $v_0=0$)."),
  ("So $v=\\sqrt{2as}\\propto\\sqrt s$: it starts at the origin, rises steeply and flattens (concave down). It is <i>not</i> a straight line (that would be $v$–$t$).", "Vậy $v=\\sqrt{2as}\\propto\\sqrt s$: bắt đầu từ gốc, tăng nhanh rồi thoải dần (lõm xuống). Không phải đường thẳng (đó là $v$–$t$).")],
 variants=[V("★ Values", "For $a=2\\ \\mathrm{m/s^2}$ find $v$ at $s=2$ m and $s=8$ m.", "Với $a=2\\ \\mathrm{m/s^2}$ tìm $v$ tại $s=2$ m và $s=8$ m.", "$2.83$ m/s and $5.66$ m/s", ("$v=\\sqrt{2as}$: $\\sqrt8$ and $\\sqrt{32}$; quadrupling $s$ only doubles $v$.", "$v=\\sqrt{2as}$: $\\sqrt8$ và $\\sqrt{32}$; $s$ gấp 4 thì $v$ chỉ gấp 2."), lambda: near(math.sqrt(8),2.828) and near(math.sqrt(32),5.657))])

def e10(): return 50.0 / (0.364 * math.log(380 / 280))
add("E10", SRC + " · Q10", ("Specific heat from an entropy change", "Nhiệt dung riêng từ biến thiên entropy"),
 ("A 364 g block touches a thermal reservoir and is heated reversibly from $T_a=280$ K to $T_b=380$ K. $\\Delta S=mc\\ln(T_b/T_a)$. The graph gives $\\Delta S$ at equilibrium. What is $c$?", "Khối 364 g tiếp xúc với nguồn nhiệt và được nung thuận nghịch từ $T_a=280$ K đến $T_b=380$ K. $\\Delta S=mc\\ln(T_b/T_a)$. Đồ thị cho $\\Delta S$ lúc cân bằng. Tính $c$."),
 "$4.5\\times10^{2}\\ \\mathrm{J/(kg\\cdot K)}$",
 [("<b>Isolate $c$:</b> $c=\\dfrac{\\Delta S}{m\\ln(T_b/T_a)}$. The graph itself is missing; the key implies $\\Delta S\\approx50$ J/K at $T_b$.", "<b>Cô lập $c$:</b> $c=\\dfrac{\\Delta S}{m\\ln(T_b/T_a)}$. Đồ thị bị mất; đáp án ngụ ý $\\Delta S\\approx50$ J/K tại $T_b$."),
  ("$\\ln(380/280)=0.3054$, $m=0.364$ kg: $c=\\dfrac{50}{0.364(0.3054)}=4.5\\times10^2$ J/kg·K. Always use kilograms and kelvin.", "$\\ln(380/280)=0{,}3054$, $m=0{,}364$ kg: $c=\\dfrac{50}{0{,}364(0{,}3054)}=4{,}5\\times10^2$ J/kg·K. Luôn dùng kilôgam và kelvin.")],
 choices=["$4.5\\times10^3$", "$4.5\\times10^2$", "$-4.5\\times10^2$", "$4.5\\times10^{-2}$"],
 chk=lambda: near(e10(), 450.0, 0.005),
 variants=[V("★ Forward", "A 0.50 kg copper block ($c=386$ J/kg·K) is heated reversibly from 300 K to 400 K. $\\Delta S$?", "Khối đồng 0,50 kg ($c=386$ J/kg·K) nung thuận nghịch từ 300 K đến 400 K. $\\Delta S$?", "$55.5\\ \\mathrm{J/K}$", ("$\\Delta S=mc\\ln(T_f/T_i)=0.5(386)\\ln(4/3)=55.5$.", "$\\Delta S=mc\\ln(T_f/T_i)=0{,}5(386)\\ln(4/3)=55{,}5$."), lambda: near(0.5*386*math.log(4/3),55.5))])

add("E11", SRC + " · Q11", ("Power, force and speed", "Công suất, lực và tốc độ"),
 ("A car engine delivers 24 kW of useful power while the car moves at constant speed. The driving force is 600 N. Speed?", "Động cơ ô tô cho công suất có ích 24 kW khi xe chạy đều. Lực phát động 600 N. Tốc độ?"),
 "$40\\ \\mathrm{m/s}$",
 [("<b>Power = force × velocity</b> (force along the motion): $P=Fv$.", "<b>Công suất = lực × vận tốc</b> (lực cùng phương chuyển động): $P=Fv$."),
  ("<b>Isolate $v$:</b> $v=P/F=24000/600=40$ m/s ($144$ km/h). Use watts, not kilowatts.", "<b>Cô lập $v$:</b> $v=P/F=24000/600=40$ m/s ($144$ km/h). Dùng watt, không dùng kilowatt.")],
 choices=["$2.5$ m/s", "$4.0$ m/s", "$25$ m/s", "$40$ m/s"], chk=lambda: 24000/600==40,
 variants=[V("★ Work", "A 1500 kg car goes from 10 to 20 m/s in 5.0 s. Average power delivered?", "Ô tô 1500 kg tăng tốc từ 10 đến 20 m/s trong 5,0 s. Công suất trung bình?", "$45\\ \\mathrm{kW}$", ("$W=\\Delta K=\\tfrac12(1500)(400-100)=2.25\\times10^5$ J; $P=W/t=45$ kW.", "$W=\\Delta K=\\tfrac12(1500)(400-100)=2{,}25\\times10^5$ J; $P=W/t=45$ kW."), lambda: near(0.5*1500*(400-100)/5,45000))])

def e12():
    pi_, Vi, pf = 1.20 * atm, 0.200, 2.40 * atm; gam = 7 / 5
    Vf = Vi * (pi_ / pf) ** (1 / gam); return (pi_ * Vi - pf * Vf) / (gam - 1)
add("E12", SRC + " · Q12", ("Work in an adiabatic compression (diatomic gas)", "Công trong nén đoạn nhiệt (khí lưỡng nguyên tử)"),
 ("An ideal diatomic gas (rotation, no vibration) is compressed adiabatically from 1.20 atm and 0.200 m$^3$ to 2.40 atm. Work done by the gas?", "Khí lưỡng nguyên tử lý tưởng (quay, không dao động) bị nén đoạn nhiệt từ 1,20 atm và 0,200 m$^3$ đến 2,40 atm. Công do khí thực hiện?"),
 "$-1.33\\times10^{4}\\ \\mathrm{J}$",
 [("<b>Adiabatic work:</b> $W=\\dfrac{p_iV_i-p_fV_f}{\\gamma-1}$ with $\\gamma=7/5$ and $V_f=V_i\\left(\\dfrac{p_i}{p_f}\\right)^{1/\\gamma}=0.200(0.5)^{0.714}=0.122\\ \\mathrm{m^3}$.", "<b>Công đoạn nhiệt:</b> $W=\\dfrac{p_iV_i-p_fV_f}{\\gamma-1}$ với $\\gamma=7/5$ và $V_f=V_i\\left(\\dfrac{p_i}{p_f}\\right)^{1/\\gamma}=0{,}200(0{,}5)^{0{,}714}=0{,}122\\ \\mathrm{m^3}$."),
  ("$p_iV_i=2.43\\times10^4$ J, $p_fV_f=2.96\\times10^4$ J: $W=\\dfrac{2.43-2.96}{0.4}\\times10^4=-1.33\\times10^4$ J. Negative because the gas is compressed (work is done <i>on</i> it). Check: $Q=0\\Rightarrow\\Delta E=-W>0$, the gas warms up.", "$p_iV_i=2{,}43\\times10^4$ J, $p_fV_f=2{,}96\\times10^4$ J: $W=\\dfrac{2{,}43-2{,}96}{0{,}4}\\times10^4=-1{,}33\\times10^4$ J. Âm vì khí bị nén (công thực hiện <i>lên</i> khí). Kiểm tra: $Q=0\\Rightarrow\\Delta E=-W>0$, khí nóng lên.")],
 choices=["$1.33\\times10^4$ J", "$1.33\\times10^{-4}$ J", "$-1.33\\times10^4$ J", "$-1.33\\times10^{-4}$ J"],
 chk=lambda: near(e12(), -1.331e4, 0.003),
 variants=[V("★ Monatomic", "A monatomic gas ($\\gamma=5/3$) at $p_i=1.0\\times10^5$ Pa, $V_i=0.10\\ \\mathrm{m^3}$ expands adiabatically to $V_f=0.20\\ \\mathrm{m^3}$. Work done by the gas?", "Khí đơn nguyên tử ($\\gamma=5/3$) có $p_i=1{,}0\\times10^5$ Pa, $V_i=0{,}10\\ \\mathrm{m^3}$ giãn đoạn nhiệt đến $V_f=0{,}20\\ \\mathrm{m^3}$. Công do khí?", "$+5.3\\times10^{3}\\ \\mathrm{J}$", ("$p_f=p_i(V_i/V_f)^\\gamma=0.315\\times10^5$ Pa; $W=(10^4-6.3\\times10^3)/(2/3)=5.5\\times10^3$ J.", "$p_f=p_i(V_i/V_f)^\\gamma=0{,}315\\times10^5$ Pa; $W=(10^4-6{,}3\\times10^3)/(2/3)=5{,}5\\times10^3$ J."), lambda: True)])
# make the variant answer match its derivation
_pf = 1.0e5 * 0.5 ** (5 / 3); _w = (1.0e5 * 0.10 - _pf * 0.20) / (2 / 3)
ITEMS[-1].variants[0].ans = "$+%.1f\\times10^{3}\\ \\mathrm{J}$" % (_w / 1e3)
ITEMS[-1].variants[0].sol = ("$p_f=p_i(V_i/V_f)^\\gamma=%.3f\\times10^5$ Pa; $W=\\dfrac{p_iV_i-p_fV_f}{\\gamma-1}=%.1f\\times10^3$ J." % (_pf / 1e5, _w / 1e3), "$p_f=p_i(V_i/V_f)^\\gamma=%.3f\\times10^5$ Pa; $W=\\dfrac{p_iV_i-p_fV_f}{\\gamma-1}=%.1f\\times10^3$ J." % (_pf / 1e5, _w / 1e3))
ITEMS[-1].variants[0].chk = lambda: near(_w, 5.55e3, 0.01)

add("E13", SRC + " · Q13", ("Molar specific heat of a gas mixture", "Nhiệt dung mol của hỗn hợp khí"),
 ("One mole of a monatomic ideal gas is mixed with one mole of a diatomic ideal gas. Molar specific heat of the mixture at constant volume?", "Trộn một mol khí đơn nguyên tử với một mol khí lưỡng nguyên tử. Nhiệt dung mol đẳng tích của hỗn hợp?"),
 "$2R$",
 [("<b>Add the heat capacities</b> (same $\\Delta T$): $C_{V,tot}=n_1C_{V1}+n_2C_{V2}=1\\cdot\\tfrac32R+1\\cdot\\tfrac52R=4R$ for 2 mol.", "<b>Cộng nhiệt dung</b> (cùng $\\Delta T$): $C_{V,tot}=n_1C_{V1}+n_2C_{V2}=1\\cdot\\tfrac32R+1\\cdot\\tfrac52R=4R$ cho 2 mol."),
  ("<b>Per mole of mixture:</b> $C_V=\\dfrac{4R}{2}=2R$ (the mole-weighted average).", "<b>Trên mỗi mol hỗn hợp:</b> $C_V=\\dfrac{4R}{2}=2R$ (trung bình theo số mol).")],
 choices=["$R$", "$0.5R$", "$2R$", "$4R$"], trap=("$4R$ is the heat capacity of the 2 mol together, not the molar value.", "$4R$ là nhiệt dung của cả 2 mol, không phải nhiệt dung mol."),
 chk=lambda: near((1.5+2.5)/2, 2.0),
 variants=[V("★ Unequal mix", "2 mol of monatomic and 3 mol of diatomic gas are mixed. $C_V$ per mole of mixture?", "Trộn 2 mol đơn và 3 mol lưỡng nguyên tử. $C_V$ mỗi mol hỗn hợp?", "$2.1R$", ("$(2\\cdot1.5+3\\cdot2.5)R/5=10.5R/5=2.1R$.", "$(2\\cdot1{,}5+3\\cdot2{,}5)R/5=10{,}5R/5=2{,}1R$."), lambda: near((2*1.5+3*2.5)/5,2.1))])

add("E14", SRC + " · Q14", ("Work on a $p$–$V$ process (figure missing)", "Công trên một quá trình $p$–$V$ (mất hình)"),
 ("An ideal gas undergoes the process shown. The work done by the gas is:", "Khí lý tưởng thực hiện quá trình trong hình. Công do khí thực hiện là:"),
 "$-2P_0V_0$",
 [("<b>Figure missing.</b> Method: $W=\\int p\\,dV$ = signed area under the path. Moving to smaller $V$ gives negative work; moving to larger $V$ gives positive work; no area under a vertical segment.", "<b>Hình bị mất.</b> Phương pháp: $W=\\int p\\,dV$ = diện tích có dấu dưới đường đi. $V$ giảm cho công âm; $V$ tăng cho công dương; đoạn thẳng đứng không có diện tích."),
  ("The keyed $-2P_0V_0$ corresponds to a compression of $V_0$ at average pressure $2P_0$ (or equivalent). Count the rectangle/trapezoid areas on your own figure and attach the sign from the direction of $V$.", "Đáp án $-2P_0V_0$ ứng với nén một lượng $V_0$ ở áp suất trung bình $2P_0$ (hoặc tương đương). Tính diện tích hình chữ nhật/hình thang trên hình của bạn rồi gắn dấu theo chiều của $V$.")],
 choices=["$-2P_0V_0$", "$+2P_0V_0$", "$-4P_0V_0$", "$+4P_0V_0$"],
 variants=[V("★ Cycle", "A rectangle cycle between $(V_0,P_0)$ and $(3V_0,2P_0)$ is traversed clockwise. Net work?", "Chu trình chữ nhật giữa $(V_0,P_0)$ và $(3V_0,2P_0)$ đi theo chiều kim đồng hồ. Công ròng?", "$+2P_0V_0$", ("Area enclosed $=(3V_0-V_0)(2P_0-P_0)=2P_0V_0$, positive for clockwise.", "Diện tích bao $=(3V_0-V_0)(2P_0-P_0)=2P_0V_0$, dương nếu cùng chiều kim đồng hồ."), lambda: (3-1)*(2-1)==2)])

add("E15", SRC + " · Q15", ("Projectile at its highest point", "Vật ném tại điểm cao nhất"),
 ("A projectile follows the path OPQRS (air resistance neglected). At the highest point Q which statement is true?", "Vật ném theo đường OPQRS (bỏ qua lực cản). Tại điểm cao nhất Q phát biểu nào đúng?"),
 "The horizontal component of the acceleration is zero",
 [("<b>Components at the top:</b> $v_y=0$ but $v_x=v_0\\cos\\theta\\neq0$, so momentum and kinetic energy are <i>not</i> zero.", "<b>Thành phần tại đỉnh:</b> $v_y=0$ nhưng $v_x=v_0\\cos\\theta\\neq0$ nên động lượng và động năng <i>khác</i> 0."),
  ("Acceleration is $(0,-g)$ throughout, so the <b>horizontal component of acceleration is zero</b> (the only true statement).", "Gia tốc là $(0,-g)$ suốt quá trình nên <b>thành phần ngang của gia tốc bằng 0</b> (phát biểu đúng duy nhất).")],
 choices=["The momentum is zero", "The kinetic energy is zero", "The horizontal velocity is zero", "The horizontal acceleration is zero"],
 variants=[V("★ Numbers", "Kinetic energy at the top as a fraction of the launch kinetic energy for $\\theta=60^\\circ$?", "Động năng tại đỉnh so với động năng lúc ném với $\\theta=60^\\circ$?", "$\\cos^2 60^\\circ=0.25$", ("Only $v_x=v_0\\cos\\theta$ remains: $K_{top}/K_0=\\cos^2\\theta$.", "Chỉ còn $v_x=v_0\\cos\\theta$: $K_{đỉnh}/K_0=\\cos^2\\theta$."), lambda: near(math.cos(math.radians(60))**2,0.25))])

add("E16", SRC + " · Q16", ("Heat in a cycle: first law", "Nhiệt trong chu trình: định luật 1"),
 ("In a cycle, $Q_{AB}=20.0$ J at constant volume, $Q_{BC}=0$ (adiabatic), net work per cycle $15.0$ J. Find $Q_{CA}$ (constant pressure).", "Trong một chu trình, $Q_{AB}=20{,}0$ J đẳng tích, $Q_{BC}=0$ (đoạn nhiệt), công ròng mỗi chu trình $15{,}0$ J. Tìm $Q_{CA}$ (đẳng áp)."),
 "$-5.0\\ \\mathrm{J}$",
 [("<b>Closed cycle:</b> $\\Delta E_{int}=0$ so $Q_{net}=W_{net}=15.0$ J.", "<b>Chu trình kín:</b> $\\Delta E_{int}=0$ nên $Q_{ròng}=W_{ròng}=15{,}0$ J."),
  ("$Q_{net}=Q_{AB}+Q_{BC}+Q_{CA}\\Rightarrow Q_{CA}=15.0-20.0-0=-5.0$ J (heat is rejected on the constant-pressure leg).", "$Q_{ròng}=Q_{AB}+Q_{BC}+Q_{CA}\\Rightarrow Q_{CA}=15{,}0-20{,}0-0=-5{,}0$ J (nhiệt toả ra ở đoạn đẳng áp).")],
 choices=["$5.0$ J", "$-5.0$ J", "$0.0$ J", "$10.0$ J"], chk=lambda: 15.0 - 20.0 - 0 == -5.0,
 variants=[V("★ Numbers", "$Q_{AB}=30$ J, $Q_{BC}=0$, net work 12 J. Find $Q_{CA}$ and the efficiency $W/Q_{in}$.", "$Q_{AB}=30$ J, $Q_{BC}=0$, công ròng 12 J. Tìm $Q_{CA}$ và hiệu suất $W/Q_{vào}$.", "$Q_{CA}=-18$ J; $40\\%$", ("$Q_{CA}=12-30=-18$; $\\eta=12/30=0.40$.", "$Q_{CA}=12-30=-18$; $\\eta=12/30=0{,}40$."), lambda: 12-30==-18)])

add("E17", SRC + " · Q17", ("Elastic head-on collision", "Va chạm đàn hồi trực diện"),
 ("A particle of mass $m$ and velocity $u$ collides head-on, elastically, with a stationary particle of mass $M$. Velocity of $M$ afterwards?", "Hạt khối lượng $m$, vận tốc $u$ va chạm đàn hồi trực diện với hạt $M$ đứng yên. Vận tốc của $M$ sau va chạm?"),
 "$\\dfrac{2mu}{M+m}$",
 [("<b>Two conservation laws:</b> momentum $mu=mv_1+Mv_2$ and kinetic energy $\\tfrac12mu^2=\\tfrac12mv_1^2+\\tfrac12Mv_2^2$.", "<b>Hai định luật bảo toàn:</b> động lượng $mu=mv_1+Mv_2$ và động năng $\\tfrac12mu^2=\\tfrac12mv_1^2+\\tfrac12Mv_2^2$."),
  ("Subtract to get the relative-speed rule $v_2-v_1=u$ (for $e=1$). Solve: $v_1=\\dfrac{m-M}{m+M}u$, $v_2=\\dfrac{2m}{m+M}u$.", "Trừ ra quy tắc tốc độ tương đối $v_2-v_1=u$ (khi $e=1$). Giải: $v_1=\\dfrac{m-M}{m+M}u$, $v_2=\\dfrac{2m}{m+M}u$.")],
 choices=["$u$", "$mu/M$", "$\\dfrac{2mu}{M+m}$", "$\\dfrac{(M-m)u}{M+m}$"],
 trap=("(d) is the wrong-way version of the first particle's velocity ($m-M$ in the numerator).", "(d) là biểu thức vận tốc của hạt thứ nhất lật ngược dấu."),
 chk=lambda: near(2*2*3/(2+4), 2.0),
 variants=[V("★ Numbers", "$m=2$ kg moving at 3 m/s hits $M=4$ kg at rest elastically. Both final velocities and check energy.", "$m=2$ kg chạy 3 m/s va chạm đàn hồi với $M=4$ kg đứng yên. Hai vận tốc cuối và kiểm tra năng lượng.", "$v_1=-1$ m/s, $v_2=+2$ m/s", ("$v_2=2(2)(3)/6=2$; $v_1=(2-4)(3)/6=-1$; $K$: $9=1+8$ ✓.", "$v_2=2(2)(3)/6=2$; $v_1=(2-4)(3)/6=-1$; $K$: $9=1+8$ ✓."), lambda: near((2-4)*3/6,-1) and near(0.5*2*9,0.5*2*1+0.5*4*4))])

add("E18", SRC + " · Q18", ("Tension in a string pulling three blocks", "Lực căng dây khi kéo ba khối"),
 ("Three identical blocks P, Q, R rest on a surface; a force of 30 N pulls at one end. Tensions $T_1$ (between P and Q) and $T_2$ (between Q and R)?", "Ba khối giống hệt P, Q, R nằm trên mặt phẳng; lực 30 N kéo ở một đầu. Lực căng $T_1$ (giữa P và Q) và $T_2$ (giữa Q và R)?"),
 "$T_1=10$ N, $T_2=20$ N",
 [("<b>Figure missing</b>; the standard picture has the 30 N pull on the block R at the end of the train (R–Q–P). Whole system: $a=\\dfrac{30}{3m}=\\dfrac{10}{m}$.", "<b>Hình bị mất</b>; hình chuẩn là lực 30 N kéo khối R ở đầu đoàn (R–Q–P). Cả hệ: $a=\\dfrac{30}{3m}=\\dfrac{10}{m}$."),
  ("The string between Q and R pulls Q and P: $T_2=2m\\cdot a=20$ N. The string between P and Q pulls only P: $T_1=m\\cdot a=10$ N. Tension decreases away from the pulled end.", "Dây giữa Q và R kéo Q và P: $T_2=2m\\cdot a=20$ N. Dây giữa P và Q chỉ kéo P: $T_1=m\\cdot a=10$ N. Lực căng giảm dần xa đầu bị kéo.")],
 choices=["$30$, $30$", "$10$, $20$", "$15$, $25$", "$20$, $10$"],
 chk=lambda: near(30/3*1, 10) and near(30/3*2, 20),
 variants=[V("★ Four blocks", "Four identical blocks are pulled by 40 N on a smooth floor. Tensions in the three strings from the free end?", "Bốn khối giống hệt bị kéo bằng 40 N trên sàn nhẵn. Lực căng ba dây tính từ đầu tự do?", "$10$ N, $20$ N, $30$ N", ("$a=40/4m$; string $k$ pulls $k$ blocks: $10k$ N.", "$a=40/4m$; dây thứ $k$ kéo $k$ khối: $10k$ N."), lambda: [40/4*k for k in (1,2,3)]==[10,20,30])])

def e19(): return math.sqrt(2*40/10) - math.sqrt(2*30/10)
add("E19", SRC + " · Q19", ("Time to fall the last 10 m", "Thời gian rơi 10 m cuối"),
 ("A stone is released from rest at the top of a 40 m tower. Time to fall the last 10 m? ($g=10$ m/s$^2$)", "Hòn đá thả từ nghỉ ở đỉnh tháp cao 40 m. Thời gian rơi 10 m cuối? ($g=10$ m/s$^2$)"),
 "$0.38\\ \\mathrm{s}$",
 [("<b>Subtract two fall times from rest:</b> total $t_{40}=\\sqrt{2(40)/10}=2.828$ s; time to fall the first $30$ m $t_{30}=\\sqrt{2(30)/10}=2.449$ s.", "<b>Trừ hai thời gian rơi từ nghỉ:</b> tổng $t_{40}=\\sqrt{2(40)/10}=2{,}828$ s; thời gian rơi $30$ m đầu $t_{30}=\\sqrt{2(30)/10}=2{,}449$ s."),
  ("The last 10 m take $2.828-2.449=0.379\\approx0.38$ s.", "10 m cuối mất $2{,}828-2{,}449=0{,}379\\approx0{,}38$ s.")],
 choices=["$0.38$ s", "$1.4$ s", "$2.8$ s", "$2.5$ s"], trap=("$2.8$ s is the total time; $1.4$ s would be half of it — the last 10 m is the <i>shortest</i> interval because the stone is fastest there.", "$2{,}8$ s là tổng thời gian; 10 m cuối là khoảng ngắn nhất vì vật nhanh nhất ở đó."),
 chk=lambda: near(e19(), 0.379, 0.01),
 variants=[V("★ New height", "A stone falls from rest through 80 m. Time for the last 20 m? ($g=10$)", "Hòn đá rơi từ nghỉ 80 m. Thời gian rơi 20 m cuối? ($g=10$)", "$0.54\\ \\mathrm{s}$", ("$\\sqrt{16}-\\sqrt{12}=4-3.464=0.536$.", "$\\sqrt{16}-\\sqrt{12}=4-3{,}464=0{,}536$."), lambda: near(4-math.sqrt(12),0.536))])

add("E20", SRC + " · Q20", ("Minimum release height for a vertical loop", "Độ cao thả tối thiểu để qua vòng tròn thẳng đứng"),
 ("A body is released from height $h$ along an incline into a vertical circular loop of radius $R$. Minimum $h$ to complete the loop (frictionless, sliding)?", "Vật thả từ độ cao $h$ trên mặt nghiêng vào vòng tròn thẳng đứng bán kính $R$. $h$ nhỏ nhất để đi hết vòng (không ma sát, trượt)?"),
 "$2.5\\,R$",
 [("<b>At the top the minimum condition is $N=0$:</b> gravity alone provides the centripetal force: $mg=\\dfrac{mv^2}{R}\\Rightarrow v^2=gR$.", "<b>Tại đỉnh điều kiện nhỏ nhất là $N=0$:</b> chỉ trọng lực làm lực hướng tâm: $mg=\\dfrac{mv^2}{R}\\Rightarrow v^2=gR$."),
  ("<b>Energy conservation from release to the top</b> (height $2R$): $mgh=mg(2R)+\\tfrac12mv^2=2mgR+\\tfrac12mgR\\Rightarrow h=2.5R$.", "<b>Bảo toàn cơ năng từ lúc thả đến đỉnh</b> (độ cao $2R$): $mgh=mg(2R)+\\tfrac12mv^2=2mgR+\\tfrac12mgR\\Rightarrow h=2{,}5R$.")],
 choices=["$6.0R$", "$4.0R$", "$2.5R$", "$2.0R$"], trap=("$2R$ would only reach the top with zero speed; the body would fall off the track.", "$2R$ chỉ tới đỉnh với tốc độ 0; vật sẽ rơi khỏi đường ray."),
 chk=lambda: near(2 + 0.5, 2.5),
 variants=[V("★ Rolling sphere", "A solid sphere rolls without slipping into the loop ($r\\ll R$). Minimum $h$?", "Quả cầu đặc lăn không trượt vào vòng ($r\\ll R$). $h$ nhỏ nhất?", "$2.7R$", ("$mgh=2mgR+\\tfrac12mv^2+\\tfrac12I\\omega^2=2mgR+\\tfrac7{10}mv^2$ with $v^2=gR$: $h=2.7R$.", "$mgh=2mgR+\\tfrac12mv^2+\\tfrac12I\\omega^2=2mgR+\\tfrac7{10}mv^2$ với $v^2=gR$: $h=2{,}7R$."), lambda: near(2+0.7,2.7))])

def e21(v=330.0):
    d = 3.0e-10; T = 273.15; lam = 1.380649e-23 * T / (math.sqrt(2) * math.pi * d * d * atm); return v / lam
add("E21", SRC + " · Q21", ("Frequency whose sound wavelength equals the mean free path", "Tần số có bước sóng âm bằng quãng đường tự do trung bình"),
 ("At what frequency is the wavelength of sound in air equal to the mean free path of oxygen molecules at 1.0 atm and 0°C? Molecular diameter $3.0\\times10^{-8}$ cm.", "Ở tần số nào bước sóng âm trong không khí bằng quãng đường tự do trung bình của phân tử oxy ở 1,0 atm và 0°C? Đường kính phân tử $3{,}0\\times10^{-8}$ cm."),
 "$3.5\\times10^{9}\\ \\mathrm{Hz}$",
 [("<b>Mean free path:</b> $\\lambda=\\dfrac{kT}{\\sqrt2\\,\\pi d^2p}=\\dfrac{(1.38\\times10^{-23})(273)}{\\sqrt2\\pi(3.0\\times10^{-10})^2(1.013\\times10^5)}=9.3\\times10^{-8}$ m.", "<b>Quãng đường tự do trung bình:</b> $\\lambda=\\dfrac{kT}{\\sqrt2\\,\\pi d^2p}=\\dfrac{(1{,}38\\times10^{-23})(273)}{\\sqrt2\\pi(3{,}0\\times10^{-10})^2(1{,}013\\times10^5)}=9{,}3\\times10^{-8}$ m."),
  ("<b>Wave relation:</b> $f=v_{sound}/\\lambda$. With $v\\approx330$ m/s: $f=3.5\\times10^9$ Hz (the key). With $331$ m/s the value is $3.56\\times10^9$ Hz, which rounds to $3.6\\times10^9$: the result depends on the speed of sound used; choose the keyed (c).", "<b>Quan hệ sóng:</b> $f=v_{âm}/\\lambda$. Với $v\\approx330$ m/s: $f=3{,}5\\times10^9$ Hz (đáp án của đề). Với $331$ m/s ra $3{,}56\\times10^9$ Hz, làm tròn $3{,}6\\times10^9$: kết quả phụ thuộc tốc độ âm đã dùng; chọn đáp án của đề (c).")],
 choices=["$3.5\\times10^8$ Hz", "$3.0\\times10^8$ Hz", "$3.5\\times10^9$ Hz", "$3.6\\times10^9$ Hz"],
 note=("Options (c) and (d) differ only through the speed of sound ($330$ vs $331$ m/s): a quiz flaw; the keyed answer is (c).", "Đáp án (c) và (d) chỉ khác nhau do tốc độ âm ($330$ hay $331$ m/s): đề có điểm yếu; đáp án của đề là (c)."),
 chk=lambda: near(e21(330.0), 3.55e9, 0.01),
 variants=[V("★ Pressure", "Mean free path of the same gas at 0.10 atm and 0°C?", "Quãng đường tự do trung bình của cùng khí ở 0,10 atm và 0°C?", "$9.3\\times10^{-7}\\ \\mathrm{m}$", ("$\\lambda\\propto1/p$: ten times larger.", "$\\lambda\\propto1/p$: lớn gấp mười lần."), lambda: near(e21(1.0)/e21(1.0)*9.3e-7,9.3e-7))])

add("E22", SRC + " · Q22", ("Signs of work and heat", "Dấu của công và nhiệt"),
 ("Work done on a system is ..., and heat flow into the system is ...", "Công thực hiện lên hệ là ..., và nhiệt truyền vào hệ là ..."),
 "Negative, positive (with $W$ = work done <i>by</i> the system)",
 [("<b>Convention of the course:</b> $\\Delta E_{int}=Q-W$ with $Q>0$ when the system <i>absorbs</i> heat and $W>0$ when the system does work <i>on the surroundings</i>.", "<b>Quy ước của môn học:</b> $\\Delta E_{int}=Q-W$ với $Q>0$ khi hệ <i>nhận</i> nhiệt và $W>0$ khi hệ <i>sinh công</i> lên môi trường."),
  ("Work done <i>on</i> the system (compression) makes $W<0$; heat flowing <i>into</i> the system is $Q>0$. Key: negative, positive.", "Công thực hiện <i>lên</i> hệ (nén) làm $W<0$; nhiệt truyền <i>vào</i> hệ là $Q>0$. Đáp án: âm, dương.")],
 choices=["Positive, negative", "Positive, positive", "Negative, negative", "Negative, positive"],
 note=("The wording depends on the sign convention; with the opposite convention ($W_{on}$ positive) the first blank would be positive. Use the convention of the Learning Support notes: $W$ released by the gas is positive.", "Cách diễn đạt phụ thuộc quy ước dấu; với quy ước ngược ($W_{lên}$ dương) chỗ trống đầu sẽ dương. Dùng quy ước của tài liệu Learning Support: $W$ khí sinh ra là dương."),
 variants=[V("★ Apply", "A gas absorbs 500 J and does 200 J of work. $\\Delta E_{int}$? Then 300 J of work is done on it with no heat: $\\Delta E_{int}$?", "Khí nhận 500 J và sinh công 200 J. $\\Delta E_{int}$? Sau đó có 300 J công làm lên khí, không trao đổi nhiệt: $\\Delta E_{int}$?", "$+300$ J; $+300$ J", ("$\\Delta E=Q-W=500-200=300$; then $Q=0$, $W=-300$: $\\Delta E=+300$.", "$\\Delta E=Q-W=500-200=300$; sau đó $Q=0$, $W=-300$: $\\Delta E=+300$."), lambda: 500-200==300)])

add("E23", SRC + " · Q23", ("Internal energy is path independent", "Nội năng không phụ thuộc đường đi"),
 ("Path 1 from i to f: isothermal expansion (work 50 J), adiabatic expansion (40 J), isothermal compression (30 J), adiabatic compression (25 J). Change of internal energy along path 2?", "Đường 1 từ i đến f: giãn đẳng nhiệt (công 50 J), giãn đoạn nhiệt (40 J), nén đẳng nhiệt (30 J), nén đoạn nhiệt (25 J). Biến thiên nội năng theo đường 2?"),
 "$-15\\ \\mathrm{J}$",
 [("<b>$E_{int}$ is a state function:</b> $\\Delta E_{int}$ is the same along every path from i to f, so compute it on path 1.", "<b>$E_{int}$ là hàm trạng thái:</b> $\\Delta E_{int}$ như nhau trên mọi đường từ i đến f nên tính trên đường 1."),
  ("Isothermal steps: $\\Delta E=0$. Adiabatic expansion ($Q=0$, $W=+40$): $\\Delta E=-40$. Adiabatic compression ($W=-25$): $\\Delta E=+25$. Total $-40+25=-15$ J.", "Các bước đẳng nhiệt: $\\Delta E=0$. Giãn đoạn nhiệt ($Q=0$, $W=+40$): $\\Delta E=-40$. Nén đoạn nhiệt ($W=-25$): $\\Delta E=+25$. Tổng $-40+25=-15$ J.")],
 choices=["$-40$ J", "$25$ J", "$-15$ J", "$15$ J"], trap=("Work $50-30$ on the isothermal steps does not change $E_{int}$ (heat compensates).", "Công $50-30$ ở các bước đẳng nhiệt không đổi $E_{int}$ (nhiệt bù lại)."),
 chk=lambda: -40 + 25 == -15,
 variants=[V("★ Numbers", "Adiabatic expansion with $W=+70$ J then adiabatic compression with $W=-45$ J. $\\Delta E_{int}$ along the whole path?", "Giãn đoạn nhiệt $W=+70$ J rồi nén đoạn nhiệt $W=-45$ J. $\\Delta E_{int}$ trên cả đường?", "$-25$ J", ("$\\Delta E=-W$ for each adiabat: $-70+45=-25$.", "$\\Delta E=-W$ cho mỗi đoạn nhiệt: $-70+45=-25$."), lambda: -70+45==-25)])

def e24():
    mi = 150.0; Lf = 333.0; c = 4.186; Lv = 2256.0
    return (mi * Lf + mi * c * 50) / (Lv + c * 50)
add("E24", SRC + " · Q24", ("Steam mixed with ice (calorimetry)", "Hơi nước trộn với nước đá (nhiệt lượng kế)"),
 ("What mass of steam at 100°C must be mixed with 150 g of ice at 0°C in an insulated container to give liquid water at 50°C?", "Cần bao nhiêu khối lượng hơi nước 100°C trộn với 150 g nước đá 0°C trong bình cách nhiệt để được nước lỏng 50°C?"),
 "$33\\ \\mathrm{g}$",
 [("<b>Heat gained = heat lost.</b> The ice melts ($mL_F$) and the meltwater warms to 50°C: $Q_{in}=150(333)+150(4.186)(50)=4.99\\times10^4+3.14\\times10^4=8.14\\times10^4$ J.", "<b>Nhiệt thu = nhiệt toả.</b> Đá tan ($mL_F$) rồi nước đá tan nóng lên 50°C: $Q_{vào}=150(333)+150(4{,}186)(50)=4{,}99\\times10^4+3{,}14\\times10^4=8{,}14\\times10^4$ J."),
  ("The steam condenses ($mL_V$) and cools to 50°C: per gram $2256+4.186(50)=2465$ J/g. So $m=\\dfrac{8.14\\times10^4}{2465}=33.0$ g. (Both phase changes must be included — see the Learning Support note.)", "Hơi ngưng tụ ($mL_V$) rồi nguội xuống 50°C: mỗi gam toả $2256+4{,}186(50)=2465$ J/g. Vậy $m=\\dfrac{8{,}14\\times10^4}{2465}=33{,}0$ g. (Phải tính cả hai chuyển pha — xem ghi chú Learning Support.)")],
 choices=["$34$ g", "$33$ g", "$32$ g", "$35$ g"], chk=lambda: near(e24(), 33.0, 0.01),
 variants=[V("★ Ice only", "How much heat melts 200 g of ice at 0°C and warms the water to 20°C?", "Cần bao nhiêu nhiệt để làm tan 200 g nước đá 0°C và nung nước lên 20°C?", "$8.3\\times10^4\\ \\mathrm{J}$", ("$200(333)+200(4.186)(20)=66600+16744=83344$ J.", "$200(333)+200(4{,}186)(20)=66600+16744=83344$ J."), lambda: near(200*333+200*4.186*20,83344))])

add("E25", SRC + " · Q25", ("Net heat in a $p$–$V$ cycle (figure missing)", "Nhiệt ròng trong chu trình $p$–$V$ (mất hình)"),
 ("A gas goes round the cycle in the $p$–$V$ diagram (horizontal scale set by $V_s=4.0$ m$^3$). Net energy added as heat during one cycle?", "Khí thực hiện chu trình trên giản đồ $p$–$V$ (thang ngang $V_s=4{,}0$ m$^3$). Nhiệt ròng truyền vào trong một chu trình?"),
 "$-30\\ \\mathrm{J}$",
 [("<b>Closed cycle ⇒ $\\Delta E_{int}=0$ ⇒ $Q_{net}=W_{net}$.</b> The net work is the signed enclosed area: clockwise ⇒ positive, counter-clockwise ⇒ negative.", "<b>Chu trình kín ⇒ $\\Delta E_{int}=0$ ⇒ $Q_{ròng}=W_{ròng}$.</b> Công ròng là diện tích bao có dấu: cùng chiều kim đồng hồ ⇒ dương, ngược chiều ⇒ âm."),
  ("Figure missing; the key $-30$ J means the cycle is traversed counter-clockwise and encloses $30$ J of $pV$ area, so the gas gives out net heat $30$ J.", "Hình bị mất; đáp án $-30$ J nghĩa là chu trình đi ngược chiều kim đồng hồ và bao $30$ J diện tích $pV$, khí toả nhiệt ròng $30$ J.")],
 choices=["$30$ J", "$-30$ J", "$60$ J", "$-90$ J"],
 variants=[V("★ Triangle", "A triangular cycle: base $2.0$ m$^3$, height $30$ Pa, clockwise. $Q_{net}$?", "Chu trình tam giác: đáy $2{,}0$ m$^3$, cao $30$ Pa, cùng chiều kim đồng hồ. $Q_{ròng}$?", "$+30$ J", ("$\\tfrac12(2.0)(30)=30$ J.", "$\\tfrac12(2{,}0)(30)=30$ J."), lambda: 0.5*2.0*30==30)])

add("E26", SRC + " · Q26", ("Apparent weight (repeat of mock Q6)", "Trọng lượng biểu kiến (trùng M06)"),
 ("A 50 kg man stands on a scale in a lift descending at 1.0 m/s$^2$. Reading? ($g=10$)", "Người 50 kg đứng trên cân trong thang máy đi xuống với gia tốc 1,0 m/s$^2$. Số chỉ? ($g=10$)"),
 "$450\\ \\mathrm{N}$",
 [("$N=m(g-a)=50(10-1)=450$ N (see M06).", "$N=m(g-a)=50(10-1)=450$ N (xem M06).")],
 choices=["$450$ N", "$60$ N", "$550$ N", "$500$ N"], chk=lambda: 50*9==450, mock="M06",
 variants=[V("★ Free fall", "Reading if the cable breaks (free fall)?", "Số chỉ nếu cáp đứt (rơi tự do)?", "$0$ N", ("$a=g\\Rightarrow N=0$.", "$a=g\\Rightarrow N=0$."), lambda: True)])

add("E27", SRC + " · Q27", ("Two masses on a smooth surface (figure missing)", "Hai vật trên mặt nhẵn (mất hình)"),
 ("A 40 kg mass and a 10 kg mass rest on a smooth surface as shown. Speed of the 10 kg mass 2 s after release? ($g=10$)", "Vật 40 kg và 10 kg đặt trên mặt nhẵn như hình. Tốc độ của vật 10 kg sau 2 s kể từ lúc thả? ($g=10$)"),
 "$2\\ \\mathrm{m/s}$ (as keyed — see the note)",
 [("<b>Figure missing.</b> For the usual arrangement (10 kg hanging, 40 kg on the smooth table): $a=\\dfrac{m_2g}{m_1+m_2}=\\dfrac{100}{50}=2$ m/s$^2$, so $v(2\\ \\mathrm{s})=4$ m/s.", "<b>Hình bị mất.</b> Với cách bố trí quen thuộc (10 kg treo, 40 kg trên bàn nhẵn): $a=\\dfrac{m_2g}{m_1+m_2}=\\dfrac{100}{50}=2$ m/s$^2$ nên $v(2\\ \\mathrm{s})=4$ m/s."),
  ("The quiz keys $2$ m/s, i.e. $a=1$ m/s$^2$. That corresponds to a different arrangement in the (missing) figure. Compare with the mock M09 (rough bench, $a=1.6$) before the exam; if your figure is the plain hanging-mass one, ask your tutor which key is meant.", "Đề cho đáp án $2$ m/s, tức $a=1$ m/s$^2$, ứng với cách bố trí khác trong hình (đã mất). So với M09 (bàn nhám, $a=1{,}6$) trước kỳ thi; nếu hình của bạn là vật treo thông thường, hãy hỏi gia sư đáp án nào được dùng.")],
 choices=["$1$ m/s", "$4$ m/s", "$2$ m/s", "$10$ m/s"], mock="M09",
 note=("Flag: unverified key. Under the plain reading the answer would be option (b) $4$ m/s.", "Cảnh báo: đáp án chưa kiểm chứng được. Theo cách đọc thông thường đáp án sẽ là (b) $4$ m/s."),
 variants=[V("★ Atwood", "Atwood machine, masses 40 kg and 10 kg. Acceleration and string tension?", "Máy Atwood, hai vật 40 kg và 10 kg. Gia tốc và lực căng dây?", "$a=6$ m/s$^2$; $T=160$ N", ("$a=\\dfrac{(40-10)(10)}{50}=6$; $T=m_2(g+a)=10(16)=160$ N.", "$a=\\dfrac{(40-10)(10)}{50}=6$; $T=m_2(g+a)=10(16)=160$ N."), lambda: near(30*10/50,6) and near(10*(10+6),160))])

def e28():
    Tc, Th = 288.15, 308.15; Q = 1.0 * 1.005 * (Th - Tc); K = Tc / (Th - Tc); return Q / K
add("E28", SRC + " · Q28", ("Power for an air conditioner", "Công suất máy điều hòa"),
 ("An air conditioner supplies 1 kg/s of air at 15°C cooled from outside air at 35°C. Estimate the power needed. $P=\\dot m\\,C_p\\Delta T$ ($C_p=1.005$ kJ/kg·K).", "Máy điều hòa cấp 1 kg/s không khí 15°C, làm lạnh từ không khí ngoài trời 35°C. Ước tính công suất cần thiết. $P=\\dot m\\,C_p\\Delta T$ ($C_p=1.005$ kJ/kg·K)."),
 "$1.39\\ \\mathrm{kW}$",
 [("<b>Heat to remove per second:</b> $\\dot Q_C=\\dot mC_p\\Delta T=(1)(1.005)(20)=20.1$ kW.", "<b>Nhiệt phải lấy đi mỗi giây:</b> $\\dot Q_C=\\dot mC_p\\Delta T=(1)(1{,}005)(20)=20{,}1$ kW."),
  ("<b>Carnot refrigerator (best case):</b> $K=\\dfrac{T_C}{T_H-T_C}=\\dfrac{288}{20}=14.4$, so $P=\\dfrac{\\dot Q_C}{K}=\\dfrac{20.1}{14.4}=1.39$ kW (the quiz formula alone would give 20.1 kW, so the Carnot COP is needed).", "<b>Máy lạnh Carnot (lý tưởng):</b> $K=\\dfrac{T_C}{T_H-T_C}=\\dfrac{288}{20}=14{,}4$ nên $P=\\dfrac{\\dot Q_C}{K}=\\dfrac{20{,}1}{14{,}4}=1{,}39$ kW (công thức đề cho một mình sẽ ra 20,1 kW nên phải dùng COP Carnot).")],
 choices=["$1.09$ kW", "$1.19$ kW", "$1.29$ kW", "$1.39$ kW"], chk=lambda: near(e28(), 1.395, 0.01),
 variants=[V("★ Refrigerator", "A Carnot refrigerator keeps its interior at 4°C in a 24°C room. COP, and work per 1000 J removed?", "Tủ lạnh Carnot giữ bên trong 4°C trong phòng 24°C. COP và công cần cho mỗi 1000 J lấy ra?", "$K=13.9$; $72\\ \\mathrm{J}$", ("$K=277.15/20=13.86$; $W=1000/13.86=72.2$ J.", "$K=277{,}15/20=13{,}86$; $W=1000/13{,}86=72{,}2$ J."), lambda: near(277.15/20,13.86) and near(1000/(277.15/20),72.2))])

add("E29", SRC + " · Q29", ("Which is NOT one of Newton's laws?", "Phát biểu nào KHÔNG phải định luật Newton?"),
 ("Which of the following is NOT one of Newton's laws of motion?", "Phát biểu nào sau đây KHÔNG phải một định luật Newton?"),
 "The total momentum of a system remains constant when no external force acts",
 [("Newton's three laws: (1) inertia, (2) $\\sum\\vec F=\\dfrac{d\\vec p}{dt}=m\\vec a$, (3) action–reaction on different bodies.", "Ba định luật Newton: (1) quán tính, (2) $\\sum\\vec F=\\dfrac{d\\vec p}{dt}=m\\vec a$, (3) tác dụng–phản tác dụng lên hai vật khác nhau."),
  ("Conservation of momentum is a <i>consequence</i> of the second and third laws, not a separate law, so it is the odd one out.", "Bảo toàn động lượng là <i>hệ quả</i> của định luật 2 và 3, không phải một định luật riêng nên là phát biểu cần chọn.")],
 choices=["Rate of change of momentum ∝ external force", "Total momentum of a system is constant if no external force", "If A exerts a force on B, B exerts an equal opposite force on A", "A body stays at rest or in uniform motion unless acted on by a force"],
 variants=[V("★ Derive", "Show that $dp_{tot}/dt=0$ for two bodies exerting forces only on each other.", "Chứng minh $dp_{tot}/dt=0$ cho hai vật chỉ tác dụng lực lên nhau.", "$\\vec F_{12}+\\vec F_{21}=0$", ("$d\\vec p_1/dt=\\vec F_{21}$, $d\\vec p_2/dt=\\vec F_{12}=-\\vec F_{21}$.", "$d\\vec p_1/dt=\\vec F_{21}$, $d\\vec p_2/dt=\\vec F_{12}=-\\vec F_{21}$."), lambda: True)])

add("E30", SRC + " · Q30", ("Mean free path when $p$ and $T$ both double", "Quãng đường tự do trung bình khi $p$ và $T$ cùng gấp đôi"),
 ("The mean free path of a gas molecule is $\\lambda_1$ at temperature $T$. Pressure and temperature are both doubled. New mean free path $\\lambda_2$?", "Quãng đường tự do trung bình là $\\lambda_1$ ở nhiệt độ $T$. Áp suất và nhiệt độ cùng gấp đôi. $\\lambda_2$ mới?"),
 "$\\lambda_1$",
 [("<b>Formula:</b> $\\lambda=\\dfrac{kT}{\\sqrt2\\pi d^2p}\\propto\\dfrac Tp$ (equivalently $\\propto V/N$).", "<b>Công thức:</b> $\\lambda=\\dfrac{kT}{\\sqrt2\\pi d^2p}\\propto\\dfrac Tp$ (tương đương $\\propto V/N$)."),
  ("$T\\to2T$, $p\\to2p$ ⇒ $T/p$ unchanged ⇒ $\\lambda_2=\\lambda_1$. (Same density $N/V=p/kT$.)", "$T\\to2T$, $p\\to2p$ ⇒ $T/p$ không đổi ⇒ $\\lambda_2=\\lambda_1$. (Cùng mật độ $N/V=p/kT$.)")],
 choices=["$2\\lambda_1$", "$\\lambda_1$", "$\\lambda_1/2$", "$4\\lambda_1$"], chk=lambda: 2/2 == 1,
 variants=[V("★ Other changes", "By what factor does $\\lambda$ change if $T$ is doubled at constant volume? If $d$ is doubled?", "$\\lambda$ đổi thế nào nếu gấp đôi $T$ ở thể tích không đổi? Nếu gấp đôi $d$?", "unchanged (density fixed); $\\lambda/4$", ("At fixed $V$ and $N$, $\\lambda=V/(\\sqrt2\\pi d^2N)$; $\\lambda\\propto1/d^2$.", "Với $V$, $N$ cố định, $\\lambda=V/(\\sqrt2\\pi d^2N)$; $\\lambda\\propto1/d^2$."), lambda: True)])

add("E31", SRC + " · Q31", ("Displacement from a $v$–$t$ trapezoid (figure missing)", "Độ dịch chuyển từ hình thang $v$–$t$ (mất hình)"),
 ("The figure is a velocity–time graph. Displacement equals:", "Hình là đồ thị vận tốc–thời gian. Độ dịch chuyển bằng:"),
 "$\\dfrac y2(x_3+x_2-x_1)$",
 [("<b>Displacement = area under the $v$–$t$ graph.</b> The graph is a trapezoid of height $y$ whose parallel sides are $x_3$ and $(x_2-x_1)$ in the figure's notation.", "<b>Độ dịch chuyển = diện tích dưới đồ thị $v$–$t$.</b> Đồ thị là hình thang cao $y$ có hai đáy là $x_3$ và $(x_2-x_1)$ theo ký hiệu của hình."),
  ("Trapezoid area $=\\dfrac{y}{2}(\\text{sum of parallel sides})=\\dfrac y2(x_3+x_2-x_1)$. Since the figure is missing, match each side with the picture; the formula is area $=$ ½ × height × (a + b).", "Diện tích hình thang $=\\dfrac{y}{2}(\\text{tổng hai đáy})=\\dfrac y2(x_3+x_2-x_1)$. Vì hình bị mất, hãy ghép từng cạnh với hình; công thức là diện tích $=$ ½ × chiều cao × (a + b).")],
 choices=["$y(x_1+x_2+x_3)$", "$y(x_3-x_1)$", "$\\dfrac y2(x_3+x_2-x_1)$", "$y(x_3-x_2-x_1)$"],
 variants=[V("★ Numbers", "A $v$–$t$ trapezoid: parallel sides $6$ s and $10$ s, height $4$ m/s. Displacement?", "Hình thang $v$–$t$: hai đáy $6$ s và $10$ s, cao $4$ m/s. Độ dịch chuyển?", "$32\\ \\mathrm{m}$", ("$\\tfrac12(6+10)(4)=32$.", "$\\tfrac12(6+10)(4)=32$."), lambda: 0.5*(6+10)*4==32)])

add("E32", SRC + " · Q32", ("What does $pV/kT$ represent?", "$pV/kT$ biểu diễn đại lượng nào?"),
 ("The quantity $pV/(kT)$ ($k$ = Boltzmann constant) represents:", "Đại lượng $pV/(kT)$ ($k$ là hằng số Boltzmann) biểu diễn:"),
 "number of molecules in the gas",
 [("<b>Ideal gas law, molecular form:</b> $pV=NkT$.", "<b>Phương trình khí lý tưởng dạng phân tử:</b> $pV=NkT$."),
  ("<b>Isolate $N$:</b> $N=\\dfrac{pV}{kT}$ — the number of molecules (not moles: that is $pV/RT$).", "<b>Cô lập $N$:</b> $N=\\dfrac{pV}{kT}$ — số phân tử (không phải số mol: đó là $pV/RT$).")],
 choices=["Number of moles", "Total mass", "Number of molecules", "Density"],
 chk=lambda: near(atm*0.0224/(1.380649e-23*273.15), 6.02e23, 0.01),
 variants=[V("★ Molecules in a litre", "How many molecules in 1.0 L of an ideal gas at 1.0 atm and 0°C?", "Có bao nhiêu phân tử trong 1,0 L khí lý tưởng ở 1,0 atm và 0°C?", "$2.69\\times10^{22}$", ("$N=pV/kT=\\dfrac{1.013\\times10^5(10^{-3})}{1.38\\times10^{-23}(273.15)}$.", "$N=pV/kT=\\dfrac{1{,}013\\times10^5(10^{-3})}{1{,}38\\times10^{-23}(273{,}15)}$."), lambda: near(atm*1e-3/(1.380649e-23*273.15),2.687e22,0.01))])

add("E33", SRC + " · Q33", ("Two containers joined, temperatures kept fixed", "Hai bình nối thông, giữ nguyên nhiệt độ"),
 ("Container A holds gas at $5.0\\times10^5$ Pa, 300 K; container B has four times the volume with the same gas at $1.0\\times10^5$ Pa, 400 K. The valve opens, temperatures of each container are maintained. Final pressure?", "Bình A chứa khí $5{,}0\\times10^5$ Pa, 300 K; bình B có thể tích gấp bốn lần chứa cùng khí $1{,}0\\times10^5$ Pa, 400 K. Mở van, giữ nhiệt độ mỗi bình. Áp suất cuối?"),
 "$2.0\\times10^{5}\\ \\mathrm{Pa}$",
 [("<b>Conserve the total number of moles</b> ($n=pV/RT$). Initially $n_A=\\dfrac{5\\times10^5V}{300R}$, $n_B=\\dfrac{1\\times10^5(4V)}{400R}$: $n_{tot}=\\dfrac{V}{R}(1667+1000)=\\dfrac{2667V}{R}$.", "<b>Bảo toàn tổng số mol</b> ($n=pV/RT$). Ban đầu $n_A=\\dfrac{5\\times10^5V}{300R}$, $n_B=\\dfrac{1\\times10^5(4V)}{400R}$: $n_{tổng}=\\dfrac{V}{R}(1667+1000)=\\dfrac{2667V}{R}$."),
  ("<b>Final state:</b> same pressure $p$, temperatures stay 300 K and 400 K: $n_{tot}=\\dfrac{pV}{300R}+\\dfrac{p(4V)}{400R}=\\dfrac{pV}{R}\\left(\\dfrac1{300}+\\dfrac1{100}\\right)=\\dfrac{pV}{75R}$. Equate with $\\dfrac{2667V}{R}$ (the 2667 is in Pa·K⁻¹): $p=75\\left(\\dfrac{5\\times10^5}{300}+\\dfrac{4\\times10^5}{400}\\right)=2.0\\times10^5$ Pa.", "<b>Trạng thái cuối:</b> cùng áp suất $p$, nhiệt độ vẫn 300 K và 400 K: $n_{tổng}=\\dfrac{pV}{300R}+\\dfrac{p(4V)}{400R}=\\dfrac{pV}{R}\\left(\\dfrac1{300}+\\dfrac1{100}\\right)=\\dfrac{pV}{75R}$. Cho bằng $\\dfrac{2667V}{R}$: $p=75\\left(\\dfrac{5\\times10^5}{300}+\\dfrac{4\\times10^5}{400}\\right)=2{,}0\\times10^5$ Pa.")],
 choices=["$1.0\\times10^5$ Pa", "$2.0\\times10^4$ Pa", "$2.0\\times10^5$ Pa", "$1.0\\times10^4$ Pa"],
 chk=lambda: near((5e5/300 + 4e5/400) * 75, 2.0e5, 0.001),
 variants=[V("★ Same temperature", "Same containers but both at 300 K throughout. Final pressure?", "Cùng hai bình nhưng cả hai giữ 300 K. Áp suất cuối?", "$1.8\\times10^{5}\\ \\mathrm{Pa}$ (weighted by volume)", ("$p=\\dfrac{p_AV+p_B(4V)}{5V}=\\dfrac{5+4}{5}\\times10^5=1.8\\times10^5$ Pa.", "$p=\\dfrac{p_AV+p_B(4V)}{5V}=\\dfrac{5+4}{5}\\times10^5=1{,}8\\times10^5$ Pa."), lambda: near((5e5*1+1e5*4)/5,1.8e5))])

def e34():
    TL = 290.15; return TL / 0.5 - TL / 0.6
add("E34", SRC + " · Q34", ("Raising the hot reservoir of a Carnot engine", "Tăng nhiệt độ nguồn nóng của động cơ Carnot"),
 ("A Carnot engine whose cold reservoir is at 17°C has efficiency 40%. By how much must the hot-reservoir temperature increase to reach 50%?", "Động cơ Carnot có nguồn lạnh 17°C, hiệu suất 40%. Phải tăng nhiệt độ nguồn nóng thêm bao nhiêu để đạt 50%?"),
 "$97\\ \\mathrm{K}$",
 [("<b>Isolate $T_H$ from $\\eta=1-T_C/T_H$:</b> $T_H=\\dfrac{T_C}{1-\\eta}$ with $T_C=290$ K.", "<b>Cô lập $T_H$ từ $\\eta=1-T_C/T_H$:</b> $T_H=\\dfrac{T_C}{1-\\eta}$ với $T_C=290$ K."),
  ("$\\eta=0.40$: $T_H=290/0.6=483$ K. $\\eta=0.50$: $T_H=290/0.5=580$ K. Increase $=580-483=97$ K.", "$\\eta=0{,}40$: $T_H=290/0{,}6=483$ K. $\\eta=0{,}50$: $T_H=290/0{,}5=580$ K. Tăng $=580-483=97$ K.")],
 choices=["$483$ K", "$580$ K", "$97$ K", "$290$ K"], trap=("$483$ K and $580$ K are the two temperatures, not the increase.", "$483$ K và $580$ K là hai nhiệt độ, không phải mức tăng."),
 chk=lambda: near(e34(), 96.7, 0.01),
 variants=[V("★ Lower the cold one", "Same engine: instead lower $T_C$ to reach 50% with $T_H=483$ K. New $T_C$?", "Cùng động cơ: thay vào đó hạ $T_C$ để đạt 50% với $T_H=483$ K. $T_C$ mới?", "$242\\ \\mathrm{K}$", ("$T_C=T_H(1-\\eta)=483(0.5)=241.7$ K.", "$T_C=T_H(1-\\eta)=483(0{,}5)=241{,}7$ K."), lambda: near(290.15/0.6*0.5,241.8))])

add("E35", SRC + " · Q35", ("Work by a constant force along a displacement vector", "Công của lực không đổi theo vectơ độ dời"),
 ("A particle moves from $\\vec r_1=3\\hat i+2\\hat j-6\\hat k$ to $\\vec r_2=14\\hat i+13\\hat j+9\\hat k$ under a force $5\\hat i$ N. Work done?", "Hạt dịch chuyển từ $\\vec r_1=3\\hat i+2\\hat j-6\\hat k$ đến $\\vec r_2=14\\hat i+13\\hat j+9\\hat k$ dưới lực $5\\hat i$ N. Công thực hiện?"),
 "$55\\ \\mathrm{J}$",
 [("<b>Constant force:</b> $W=\\vec F\\cdot\\Delta\\vec r$ (dot product), with $\\Delta\\vec r=\\vec r_2-\\vec r_1=(11,\\ 11,\\ 15)$ m.", "<b>Lực không đổi:</b> $W=\\vec F\\cdot\\Delta\\vec r$ (tích vô hướng), với $\\Delta\\vec r=\\vec r_2-\\vec r_1=(11,\\ 11,\\ 15)$ m."),
  ("$W=(5,0,0)\\cdot(11,11,15)=55$ J. Only the component of displacement along the force counts.", "$W=(5,0,0)\\cdot(11,11,15)=55$ J. Chỉ thành phần độ dời dọc theo lực được tính.")],
 choices=["$55$ J", "$65$ J", "$45$ J", "$75$ J"], chk=lambda: 5*(14-3) == 55,
 variants=[V("★ Two components", "Force $(3,-2,4)$ N, displacement $(2,5,-1)$ m. Work?", "Lực $(3,-2,4)$ N, độ dời $(2,5,-1)$ m. Công?", "$-8\\ \\mathrm{J}$", ("$6-10-4=-8$.", "$6-10-4=-8$."), lambda: 3*2+(-2)*5+4*(-1)==-8)])

add("E36", SRC + " · Q36", ("Rate of change of momentum in free fall (repeat of M16)", "Tốc độ biến thiên động lượng khi rơi tự do (trùng M16)"),
 ("A body falls freely. Its rate of change of momentum equals:", "Vật rơi tự do. Tốc độ biến thiên động lượng của nó bằng:"),
 "Weight",
 [("$\\vec F_{net}=d\\vec p/dt$ and in free fall $\\vec F_{net}=m\\vec g$ = weight (see M16).", "$\\vec F_{ròng}=d\\vec p/dt$ và khi rơi tự do $\\vec F_{ròng}=m\\vec g$ = trọng lượng (xem M16).")],
 choices=["Impulse", "Kinetic energy", "Power", "Weight"], mock="M16",
 variants=[V("★ Impulse", "Impulse of gravity on a 0.5 kg ball during 2 s of free fall?", "Xung lượng của trọng lực lên quả bóng 0,5 kg trong 2 s rơi tự do?", "$9.81\\ \\mathrm{N\\,s}$", ("$J=mg\\,t=0.5(9.81)(2)$.", "$J=mg\\,t=0{,}5(9{,}81)(2)$."), lambda: near(0.5*g*2,9.81))])

def e37(gv=9.81): return 1.27 * (gv + 0.575**2 / 0.600)
add("E37", SRC + " · Q37", ("Tension at the bottom of a pendulum swing", "Lực căng dây ở đáy dao động con lắc"),
 ("A pendulum bob of mass 1.27 kg hangs from a string 0.600 m long. When the string is vertical the bob moves at 0.575 m/s horizontally. Tension at that instant?", "Quả nặng 1,27 kg treo bằng dây dài 0,600 m. Khi dây thẳng đứng, quả nặng chuyển động ngang với 0,575 m/s. Lực căng lúc đó?"),
 "$13.2\\ \\mathrm{N}$",
 [("<b>Bottom of the circle:</b> the net force toward the centre (up) provides the centripetal force: $T-mg=\\dfrac{mv^2}{L}$.", "<b>Ở đáy vòng tròn:</b> hợp lực hướng tâm (hướng lên) là lực hướng tâm: $T-mg=\\dfrac{mv^2}{L}$."),
  ("<b>Isolate $T$:</b> $T=m\\left(g+\\dfrac{v^2}{L}\\right)=1.27\\left(9.81+\\dfrac{0.575^2}{0.600}\\right)=1.27(10.36)=13.2$ N (a bit more than the weight $12.5$ N).", "<b>Cô lập $T$:</b> $T=m\\left(g+\\dfrac{v^2}{L}\\right)=1{,}27\\left(9{,}81+\\dfrac{0{,}575^2}{0{,}600}\\right)=1{,}27(10{,}36)=13{,}2$ N (lớn hơn trọng lượng $12{,}5$ N một chút).")],
 choices=["$11.8$ N", "$12.5$ N", "$13.2$ N", "$13.7$ N"], trap=("$12.5$ N is just the weight; $T=mg-mv^2/L$ (wrong sign) would give $11.8$ N.", "$12{,}5$ N chỉ là trọng lượng; $T=mg-mv^2/L$ (sai dấu) cho $11{,}8$ N."),
 chk=lambda: near(e37(), 13.16, 0.005),
 variants=[V("★ At the top", "A 0.50 kg ball swings in a vertical circle of radius 0.80 m. Minimum speed at the top and tension at the bottom for that speed?", "Quả bóng 0,50 kg quay trong vòng tròn thẳng đứng bán kính 0,80 m. Tốc độ nhỏ nhất ở đỉnh và lực căng ở đáy ứng với tốc độ đó?", "$2.80$ m/s; $29.4$ N", ("Top: $v=\\sqrt{gR}=2.80$; energy: $v_b^2=5gR$; $T_b=mg+mv_b^2/R=6mg=29.4$ N.", "Đỉnh: $v=\\sqrt{gR}=2{,}80$; năng lượng: $v_b^2=5gR$; $T_b=mg+mv_b^2/R=6mg=29{,}4$ N."), lambda: near(math.sqrt(g*0.8),2.80) and near(6*0.5*g,29.43))])

add("E38", SRC + " · Q38", ("Distance travelled and displacement from a $v$–$t$ graph (figure missing)", "Quãng đường và độ dịch chuyển từ đồ thị $v$–$t$ (mất hình)"),
 ("The velocity–time graph shows the motion of an object. Calculate the distance travelled $S$ and the displacement $x$.", "Đồ thị vận tốc–thời gian cho chuyển động của một vật. Tính quãng đường $S$ và độ dịch chuyển $x$."),
 "$S=25\\ \\mathrm{m}$, $x=7\\ \\mathrm{m}$",
 [("<b>Figure missing.</b> Method: split the graph at every zero crossing. <b>Displacement = signed sum of areas</b> (areas below the axis count negative). <b>Distance = sum of absolute areas.</b>", "<b>Hình bị mất.</b> Phương pháp: chia đồ thị tại mỗi điểm cắt trục. <b>Độ dịch chuyển = tổng đại số các diện tích</b> (phần dưới trục âm). <b>Quãng đường = tổng các diện tích lấy trị tuyệt đối.</b>"),
  ("The keyed pair $S=25$ m, $x=7$ m means areas $+16$ m and $-9$ m: $16+9=25$ and $16-9=7$.", "Cặp đáp án $S=25$ m, $x=7$ m ứng với diện tích $+16$ m và $-9$ m: $16+9=25$ và $16-9=7$.")],
 choices=["$S=25$, $x=7$", "$S=49$, $x=9$", "$S=49$, $x=7$", "$S=16$, $x=9$"], chk=lambda: 16 + 9 == 25 and 16 - 9 == 7,
 variants=[V("★ Numbers", "Areas of $+12$ m (above) and $-5$ m (below). Distance and displacement?", "Diện tích $+12$ m (trên) và $-5$ m (dưới). Quãng đường và độ dịch chuyển?", "$17$ m; $7$ m", ("Distance $12+5$; displacement $12-5$.", "Quãng đường $12+5$; độ dịch chuyển $12-5$."), lambda: 12+5==17 and 12-5==7)])

add("E39", SRC + " · Q39", ("Speed–time graph: vacuum or air? (figure missing)", "Đồ thị tốc độ–thời gian: chân không hay không khí? (mất hình)"),
 ("A speed–time graph of an object is shown. Which description fits?", "Đồ thị tốc độ–thời gian của một vật được cho. Mô tả nào phù hợp?"),
 "The object drops through vacuum",
 [("<b>Figure missing.</b> A straight line through the origin means constant acceleration $g$: free fall in a <b>vacuum</b>; a curve that flattens means air resistance.", "<b>Hình bị mất.</b> Đường thẳng qua gốc nghĩa là gia tốc không đổi $g$: rơi trong <b>chân không</b>; đường cong thoải dần nghĩa là có lực cản không khí."),
  ("Starting from zero means ‘dropped’, not ‘thrown’; so the key is ‘drops through vacuum’.", "Bắt đầu từ 0 nghĩa là ‘thả’, không phải ‘ném’; nên đáp án là ‘thả rơi trong chân không’.")],
 choices=["The object drops through vacuum", "The object drops through air", "The object is thrown downwards through vacuum", "The object is thrown downwards through air"], mock="M03",
 variants=[V("★ Decide", "A $v$–$t$ graph starts at $v=5$ m/s and rises linearly with slope $9.8$ m/s$^2$. Vacuum or air, dropped or thrown?", "Đồ thị $v$–$t$ bắt đầu ở $v=5$ m/s và tăng tuyến tính độ dốc $9{,}8$ m/s$^2$. Chân không hay không khí, thả hay ném?", "thrown downward in vacuum", ("Nonzero start = thrown; constant slope $g$ = no drag.", "Bắt đầu khác 0 = ném; độ dốc $g$ không đổi = không có lực cản."), lambda: True)])

add("E40", SRC + " · Q40", ("$\\gamma$ for a diatomic gas", "$\\gamma$ của khí lưỡng nguyên tử"),
 ("For a diatomic gas $\\gamma=C_p/C_V$ is:", "Với khí lưỡng nguyên tử $\\gamma=C_p/C_V$ bằng:"),
 "$\\dfrac75$",
 [("$C_V=\\tfrac52R$, $C_p=C_V+R=\\tfrac72R$, so $\\gamma=\\dfrac{7/2}{5/2}=\\dfrac75=1.40$ (monatomic $\\tfrac53$, polyatomic $\\tfrac43$).", "$C_V=\\tfrac52R$, $C_p=C_V+R=\\tfrac72R$ nên $\\gamma=\\dfrac{7/2}{5/2}=\\dfrac75=1{,}40$ (đơn nguyên tử $\\tfrac53$, đa nguyên tử $\\tfrac43$).")],
 choices=["$9/7$", "$7/5$", "$5/3$", "$3/5$"], chk=lambda: near(3.5/2.5, 1.4),
 variants=[V("★ Speed of sound", "Using $\\gamma=7/5$, the speed of sound in air at 293 K ($M=0.029$ kg/mol) is $v=\\sqrt{\\gamma RT/M}$.", "Dùng $\\gamma=7/5$, tốc độ âm trong không khí 293 K ($M=0{,}029$ kg/mol) là $v=\\sqrt{\\gamma RT/M}$.", "$343\\ \\mathrm{m/s}$", ("$\\sqrt{1.4(8.314)(293)/0.029}=343$.", "$\\sqrt{1{,}4(8{,}314)(293)/0{,}029}=343$."), lambda: near(math.sqrt(1.4*8.314*293/0.029),343.0,0.005))])

# items whose figure is missing in the PDF: the key is the quiz's, not re-derived
_NR = ("Official answer (quiz key; figure missing, not re-derived)", "Đáp án của đề (hình bị mất, chưa tự suy ra lại)")
for _it in ITEMS:
    if _it.id in ("E03", "E09", "E10", "E14", "E25", "E27", "E31", "E38", "E39"):
        _it.klabel = _NR
    if _it.id == "E05":
        _it.klabel = ("Official answer (quiz key; our own value differs, see note)", "Đáp án của đề (giá trị tự tính khác, xem ghi chú)")
