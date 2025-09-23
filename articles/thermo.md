
# Fluid  

States: three common ones are solid, liquid, gas. Solid is fixed size fixed volume. Fluid is fixed size vary volume. Gas is vary size vary volume. Fluids include liquid and gas.  


> $$Density:\quad \rho = \frac{m}{v} \tag{$unit = kg/m^3$} $$
$$1 kg/m^3 = 1000 g/cm^3$$
> $$Pressure:\quad P = \frac{F}{A} \tag{$unit = Pa = N/m^2$}$$
In stable fluid, the pressure at the same depth is the same in all directions. Because if pressure is not the same, the fluid would flow. 
> $$P =P_0+ \rho gh$$
proof: 
$$ \begin{aligned}
P &= \frac{F}{A} \\
P &= \frac{\rho V g}{A} \\
P &= \frac{\rho A h g}{A} \\
P &= \rho gh\\

\end{aligned} $$

> $$ 1 atm = 101.3kPA $$


>$$\text{ Pascal's principle: if an external pressure is applied to a confined fluid, the pressure at every point within the fluid increases by that amount.}

> $$\text{Archimede's principle:} F_b = V_{\text{displaced}} \rho_{\text{fluid}} g$$
proof: 

$h_1$ is the distance from surface to top, $h_2$ is the distance from surface to bot

$$ \begin{aligned}
F_B &= F_{\text{bot}} - F_{\text{top}}\\
\Delta h &= h_2 - h_1 \\
F_B &= \rho g h_2 A - \rho g h_1 A \\
F_B &= \rho g V

\end{aligned} $$

Bernoulli's equation: assume flow is steady and laminar and fluid is incompressible. 

>$$ \text{if fluid is incompressible:  } A_1 v_1 = A_2 v_2$$


> $$P + \frac{1}{2}\rho v^2 + \rho g y = constant$$

proof:  
say in a closed fluid pipe, one side is P1 A1 at height y1 another is P2 A2 at height y2. length moved is $\Delta \ell$  
W1 is work done by P1 to move the entire segment from 1 to 2, W2 is work done by P2, W3 is work done by gravity  
total W equal change in kinetic energy  
$$ \begin{aligned}
W &= W_1 + W_2 + W_3 \\
W &= P_1 A_1 \Delta \ell_1 - P_2 A_2 \Delta \ell_2 - m g y_2 + m g y_1 \\
\frac{1}{2} m v_2^2 - \frac{1}{2} m v_1^2 &= P_1 A_1 \Delta \ell - P_2 A_2 \Delta \ell - m g y_2 + m g y_1 \\
\because m &= \rho A_1 \Delta \ell_1 =\rho A_2 \Delta \ell_2 , \text{divide both sides by m}\\
\frac{1}{2}\rho v_2^2 - \frac{1}{2}\rho v_1^2 &= P_1 - P_2 - \rho g y_2 + \rho g y_1 \\
P_1 + \frac{1}{2}\rho v_1^2 + \rho gy_1 &= P_2 + \frac{1}{2} \rho v_2^2 + \rho g y_2 



\end{aligned} $$

# Temperature
Unified Atomic Mass: roughly weight of one proton or neutron. C12 has 12 unified atomic mass (u)

> $$ 1u = 1.6605 * 10^{-27} kg$$

> $$n = \frac{m}{M} \tag{mole}$$
M: g/mole. roughly equal to number of proton + neutron.

volume expansion: 

> $$\Delta V = \beta V_0 \Delta T \tag{$\beta$ unit = $°C^{-1}$}$$

> $$Q = mc\Delta T \tag{Q unit = J}$$
c: specific heat (J/(g·°C))

>$$\text{in a closed enviroment, } \sum Q = 0$$

>$$Q = mL \tag{L unit = J/kG}$$
latent heat: the heat absored or released in phase change. i.e. ice into water

ideal gas law: 
> $$PV = nRT \tag{R = 8.314 J / (mol K)}$$

>$\text{Avogadro's Number:  } N_A = 6.022 * 10^{23} particles / mol$

N: total number of molecules. N = n * $N_A$  
k: Boltzmann constant: $1.38 * 10^{-23} J/K$

>$$\text{ each quadratic energy term is worth 1/2 kT, i.e. translational axis, rotational axis, vibration}$$

>$$ PV = NkT$$

proof:  
Assumptions: 1. large number of molecules. 2. molecules are on average far apart. 3. molecules obey classical mechanics. 4. collisions are perfectly elastic  
in a closed box, say we are calculating the pressure on one vertical side  
for example, on a certain side, Velocity X component goes opposite and other component no change

$$ \begin{aligned}
F &= I \Delta t \\
F_{atom} &= \frac{2mv_x}{2\ell / V_x}\\
F_{atom} &= \frac{mv_x^2}{\ell} \\
\because \bar{v^2} &= \frac{\bar{v_x^2}}{3} \text{ and } P = F/A\\
P &= N\frac{m\bar{v^2}}{3\ell A} \\
PV &= \frac{2}{3}N (\frac{1}{2}m\bar{v^2})\\
\because \bar{K} &= \frac{1}{2}m\bar{v^2} = \frac{3}{2}kT \text{ (Boltzmann constant)}\\
PV &= NkT
\end{aligned} $$


>$$\Delta E = Q - W$$
energy change of a gas equal to the heat transfered into the gas minus the work done by the gas
>$$ E_{internal} = \frac{f}{2} nRT $$

>$$\text{ monoatomic f = 3, diatomic f = 5, nonlinear polyatomic f = 6}$$

> $$C_v = M c_v \quad C_p = M c_p $$
$C_v$ means constant volume $C_p$ means constant pressure. M means molar mass  
> $$C_P - C_V = R$$
proof:
$$ \begin{aligned}
Q_v &= \Delta E_{\text{int}} \\
Q_p &= \Delta E_{\text{int}}  + P\Delta V
Q_p - Q-v &= P\Delta V \\
\because \text{ideal gas law and Q = nCT} \\
nC_P \Delta T - nC_v \Delta T &= P (\frac{nR \Delta T}{P}) \\
C_p - C_v &= R
\end{aligned} $$

>$$C_V = \frac{f}{2}R$$
proof:
$$ \begin{aligned}
Q_v &= \Delta E_{\text{int}} \\
nC_v T &= \frac{f}{2} nRT \\
C_v &= \frac{f}{2} R

\end{aligned} $$


>$$W = \int_{V_0}^{V_1} P dV $$
proof: 
$$ \begin{aligned}
W &= \int dW \\
W &= \int F d\ell \\
W &= \int P A d\ell \\
W &= \int_{V_0}^{V_1} P dV 
\end{aligned} $$

work done by a gas equal to pressure times change in volume


> $$\text{Conduction: } \frac{Q}{t} = kA\frac{T_1 - T_2}{\ell}$$
k is the thermal conductivity of a specific material, $\ell$ is the length of the material

>$$\text{radiation: } \frac{Q}{t} = \epsilon \sigma A (T_1^4 - T_2 ^4)$$
$\epsilon$ is the specific emissivity of the material both for radiantion and absorbtion between 0 and 1
$\sigma$ is the constant $5.67*10^{-8} W/m^2 K^4$  
Q is heat flowing out. $T_1$ is object's energy $T_2$ is surronding's energy

# Thermodynamics

>$$\text{first law: energy cannot be created or destroyed, only coverted from one form to another}$$

>$$\text{second law: heat naturally flows from hot to cold, never the reverse without external work}$$

>$$\text{third law: as temperature approahces absolute zero, the entropy of a perfect crystal approaches zero}$$


> $$e = \frac{W}{Q_H}$$
efficiency of a engine equals work put out divided by heat put into the hot side

> $$Q_H = W + Q_L$$
since energy is conserved, heat input equals work done plus heat output


> $$e = 1 - \frac{Q_L}{Q_H}$$
proof:
$$ \begin{aligned}
e &= \frac{W}{Q_H} \\
e &= \frac{Q_H-Q_L}{Q_H} \\
e &= 1 - \frac{Q_L}{Q_H}
\end{aligned} $$

> $$\Delta S = \frac{Q}{T} = S_b - S_a = \int_{a}^{b}\frac{dQ}{T}$$
entropy. T is not constant, need to integrate. 

in an ideal engine where heat resevoair temperature doesn't change, and entropy does not change
> $$\frac{Q_L}{T_L} = \frac{Q_H}{T_H}$$

# Oscillation

>$$ \text{A: amplitude. maximum displacement from origin. (m)  }$$

>$$ \text{T: period. time required to complete one cycle  }$$

>$$ \text{f: freqency. f = 1 / T. (Hz). cycles per second  }$$

>$$ \text{SHM: simple harmonic motion, restoring force is linearly proportional to displacement}$$

> $$x = Acos(wt + \emptyset)$$

> $$w^2 = \frac{k}{m}$$

proof:
$$\begin {aligned}
ma &= F \\
m\frac{d^2x}{dt^2} &= -kx \\
\frac{d^2x}{dt^2} + \frac{kx}{m} &= 0\\
\text{let } x &= Acos(wt + \phi) \\
\frac{dx}{dt} &= -wAsin(wt + \phi) \\
\frac{d^2x}{dt^2} &= -w^2Acos(wt + \phi) \\
-w^2Acos(wt + \phi) + \frac{k}{m}Acos(wt + \phi)  &= 0 \\
(\frac{k}{m}-w^2)Acos(wt + \phi)  &= 0\\
w^2 &= \frac{k}{m}
\end{aligned}$$

> $$E = K + U = \frac{1}{2}mv^2 + \frac{1}{2}kx^2 = \frac{1}{2}k A^2$$

> $$v = \pm v_{\text{max}} \sqrt{1 - \frac{x^2}{A^2}}$$

simple pendulum

>$$ F = -mg sin(\theta) \approx -mg\theta = -mg\frac{s}{\ell}$$

restorative force is linearly proportional to the displacement ($\theta$) so it is SHM

> $$F = -\frac{mg}{\ell}s$$

>$$\theta = \theta_{max} cos (wt + \emptyset)$$


>$$w = \sqrt{\frac{g}{\ell}}$$

>$$\tau = -mgh sin{\theta}$$
physical torque pendulum. h is distance from center of mass to pivot, $\theta$ is angle between vertical and pendulum



# Waves

if the source is a SHM then the wave both in space and a single point in time is SHM
> $$\text{crest: high points. trough: low points. wavelength $\lambda$: distance between two successive identical points}$$

> $$ v = \lambda f$$

tranverse waves are vertical normal looking waves, longitudinal waves are like a spring compression and expansion wave. longitudinal waves can be plotted in density graphs as a tranverse wave

> $$\text{small amplitude: } v = \sqrt{\frac{F_T}{\mu}}$$
$F_T$: tension in the string, $\mu$ = m / $\ell$

proof:  
say there is a small segment, with length v*t, vertical velocity v' vertical displacement at v' t on one end 0 at other (rising)  
Tension is $F_T$ due to the shape of the triangle, $F_y = \frac{v'}{v} F_T$

$$\begin {aligned}
F \Delta t &= m \Delta v \\
\frac{v'}{v} F_T t &= vt \mu v' \\
v &= \sqrt{\frac{F_T}{\mu}}

\end{aligned}$$

> $$\text{fluid longitudinal wave: } v = \sqrt{\frac{B}{\rho}}$$

> $$\bar{P} = 2 \pi^2 \rho S v f^2 A^2$$
proof:
$$\begin {aligned}
E &= \frac{1}{2} k A^2 \\
\because k &= f^2 4 \pi ^2 m \\
E &= 2 f^2  \pi ^2 m A^2\\
\because m &= \rho V \\
\because V &= S \ell = S v t \\
E &= 2 f^2 \pi ^2 Svt \rho A^2 \\

\bar{P} &= \frac{E}{t} \\
\bar{P} &= 2 f^2 \pi ^2 Sv \rho A^2 \\

\end{aligned}$$

> $$I \propto A^2$$
proof:
$$\begin {aligned}
I &= \frac{\bar{P}}{S} \\
I &= 2 f^2 \pi ^2 v \rho A^2 \\
\end{aligned}$$

>$$\text{sphere: } I \propto \frac{1}{R^2}$$
proof:
$$\begin {aligned}
I &= \frac{\bar{P}}{S} \\
I &= \frac{\bar{P}}{4 \pi r^2} \\

\end{aligned}$$

>$$\text{sphere two distances from the source: } \frac{I_2}{I_1} = \frac{r_1^2}{r_2^2} \quad \frac{A_2}{A_1} = \frac{r_1}{r_2}$$

> $$\text{1d travelling wave: } D(x,t) = Asin(2\pi \frac{x-vt}{\lambda})$$
proof: think of the original wave as without the t component. then when x = 0, the y = 0, and when x = 2 $\lambda$ it is a full wave.
now adding the t component, at time t, vt equals how far that point has travelled from the original wave position. 
x - vt should equal how far a certain point has traveled from the original position the y value should be the same.  

>$$D(x,t) = Asin(kx-wt + \emptyset) \quad k = \frac{2\pi}{\lambda}$$

proof: 
$$\begin {aligned}
D(x,t) &= Asin(2\pi \frac{x-vt}{\lambda}) \\
D(x,t) &= Asin(\frac{2\pi x}{\lambda} - \frac{2 \pi vt}{\lambda}) \\
\because f &= \frac{v}{\lambda} , w = 2\pi f \\
w &= 2\pi \frac{v}{\lambda} \\
D(x,T) &= Asin(kx - wt)
\end{aligned}$$

>$$\text{small amplitude linear waves: }\frac{\partial ^2 D}{\partial x ^2} = \frac{1}{v^2} \frac{\partial ^2 D}{\partial t^2}$$

mathmatically always stands, physically derivation requires small amplitude

proof:  
assume a small segment on a wave starting at A to B with distance $\Delta x$. at A the angle from horizontal to string is $\theta_1$ at B it's $\theta_2$ 
since amplitude is small, $\theta$ is small for both, and $\theta \approx \sin\theta \approx \tan\theta$ for both
vertical displacement is D

$$\begin {aligned}
\sum F &=ma \\
F_T\sin\theta_2 - F_T\sin\theta_1 &= \mu\Delta x \frac{\partial ^2 D}{\partial t^2} \\
\because \sin\theta &\approx \tan\theta = \frac{\partial D}{\partial x} = S \\
F_T(s_2 - s_1) &= \mu \Delta x \frac{\partial ^2 D}{\partial t^2} \\
\frac{\Delta s}{\Delta x} &= \frac{\mu}{F_T} \frac{\partial ^2 D}{\partial t^2} \\
\because s_2 - s_1 &= \frac{\Delta s}{\Delta x} = \frac{\partial ^2 D}{\partial x ^2} \\
\because \text{for small amplitude: } v &= \sqrt{\frac{F_T}{\mu}} \\
\frac{\partial ^2 D}{\partial x ^2} &= \frac{1}{v^2} \frac{\partial ^2 D}{\partial t^2} \\
\end{aligned}$$

>$$\text{principle of superposition: linear small amplitude waves, displacement of result equal the algebraic sum of displacement of all waves}$$

constructive interference is when two waves at the same side adds together towards greater amplitude,
destructive interference is when two waves at opposite side adds together for less amplitude,
both tension and momentum helps the waves keep moving and not cancel out

>$$\text{reflection on fixed end is opposite, reflection on lose end is same direction}$$

>$$\text{transmission wave amplitude decrease as density of medium increase. but frequency always stay the same}$$
transmission is the wave moving along the same medium but different density, for example a string wave from lighter to heavier parts

>$$\text{law of reflection: the angle incoming wave makes with reflecting surface is equal to angle made by reflected wave}$$

>$$\text{standing wave: a wave that appears to not move. Nodes are zero amplitude and Antinodes are maximal amplitude}$$
natural frequencies determine how many nodes there are and they are multiples of the base natural frequency based on how many nodes there are  
standing waves form because the reflection is the opposite at the ending but moves in the opposite direction also. so sometimes they cancel out sometimes they amplify as they move towards each other

>$$\lambda_n = \frac{2 \ell}{n}$$

>$$f_n = n f_1$$

proof:
$$\begin {aligned}
f_n &= \frac{v}{\lambda_n} \\
\because \lambda &= \frac{2\ell}{n} \\
f_n &= n \frac{v}{2\ell} \\
f_n &= n f_1
\end{aligned}$$

>$$D = 2A \sin kx \cos wt$$
proof: 
$$\begin {aligned}
D = D_1 + D_2 = A[sin (kx - wt) + sin (kx + wt)] \\
\because \sin \theta_1 + \sin \theta_2 = 2 \sin \left(\frac{\theta_1 + \theta_2}{2}\right) \cos \left(\frac{\theta_1 - \theta_2}{2}\right)
D = 2A \sin kx \cos wt
\end{aligned}$$


# Sound Waves

> $$B = \frac{\Delta P }{\Delta V / V}\tag{unit = Pa}$$
bulk modulus is how hard to compress something

> $$\Delta P = -BAk\cos(kx-wt)$$

> $$\Delta P_{max} = BAk = 2\pi \rho VAf $$


$$\begin{aligned}
\text{Bulk modulus definition: } B &= -\frac{\Delta P}{\Delta V/V} \\
\therefore \Delta P &= -B \frac{\Delta V}{V} \\
\text{Volume change in a slice: } \frac{\Delta V}{V} &= \frac{\partial s}{\partial x} \\
\because \text{ compression/expansion} &\text{ depends on displacement gradient} \\
\frac{\partial s}{\partial x} &= \frac{\partial}{\partial x}[A \cos(kx - \omega t)] \\
&= -Ak \sin(kx - \omega t) \\
\therefore \Delta P &= -B(-Ak \sin(kx - \omega t)) \\
&= BAk \sin(kx - \omega t) \\
\text{Using phase shift: } \Delta P &= BAk \cos(kx - \omega t) \\
\text{Maximum pressure amplitude: } \Delta P_m &= BAk \\
\because k &= \frac{2\pi}{\lambda} = \frac{2\pi f}{v} \\
\text{and } v^2 &= \frac{B}{\rho} \\
\therefore \Delta P_m &= 2\pi \rho v A f
\end{aligned}$$

> $$L = 10 \log_{10} \left(\frac{I}{I_0}\right) \tag{unit = dB}$$
decibel level $L$ is calculated using the intensity $I$ of the sound and the reference intensity $I_0$, which is typically $10^{-12} \text{W/m}^2$ for air, representing the threshold of hearing.

>$$f_o = f_s \frac{v_{\text{sound}} + v_o}{v_{\text{sound} - v_s}}$$
s is source o is observer


# Light Waves

>$$c = \lambda f \tag{ $c= 3*10^8m/s$}$$

> $$E = hf \tag{ $h= 6.63 \times 10^{-34} \text{Js}$}$$
energy of a photon

> $$n = \frac{c}{v}$$
refractive index $n$ is the ratio of the speed of light in vacuum $c$ to the speed of light in the medium $v$

> $$n_1 \sin \theta_1 = n_2 \sin \theta_2$$
Snell's Law: the product of the refractive index and the sine of the angle of incidence is equal to the product of the refractive index and the sine of the angle of refraction
>$$\lambda_n = \frac{\lambda_0}{n}$$
$\lambda_0$ is the light wavelength in vacuum

>$$\text{constructive two slit: } d \sin\theta = m \lambda \quad m = 0,1,2 ...$$

>$$\text{destructive two slit: } d \sin\theta = (m + \frac{1}{2}) \lambda \quad m = 0,1,2 ...$$


two slit inteference of distance d. $\theta$ is the angle of the diffracted ray to the vertical. new distance travelled approximately equal $\sin \theta$ to make the new two rays
approximately parallel  
if the two waves match exactly it's constructive if crest match trough it's destructive

> $$\text{thin film: replace d$\sin\theta$ with } 2nt\cos\theta$$


# Matter Waves

> $$E = nhf$$
n = quantum number  
h = 6.626 * 10^-34 Js  
f = frequency  

>$$\text{unit eV} = 1.602*10^{-19} J$$
one electron kinetic energy = 1eV

>$$hf = K + W_0$$

>$$\lambda = \frac{h}{mv}$$

K is amount of energy electron escapes in. W_0 is energy required for it to esacpe, hf is a photon's energy

