# Velocity
> $$ v = \frac{\Delta d}{\Delta t} \tag{unit = m/s}$$

> $$ a = \frac{\Delta v}{\Delta t} \tag{$unit = m/s^2$} $$

> $$ g = 9.81 m/s $$

### linear constant acceleration:
> $$ v = v_0 + at $$

proof:  
$$ \begin{aligned}
a &= \frac{dv}{dt} \\
a\,dt &= dv \\
\int_{v_0}^{v} dv &= \int_{0}^{t} a\,dt \\
v &= at + C \\
\because v_0 &= a(0) + C \\
C &= v_0 \\
v &= at + v_0
\end{aligned} $$

> $$ x = x_0 + v_0t + \frac{1}{2}at^2 $$

proof:  
$$ \begin{aligned}
v &= \frac{dx}{dt} \\
dx &= v\,dt \\
\because v &= v_0 + at \\
dx &= (v_0 + at)dt \\
\int_{x_0}^{x} dx &= \int_{0}^{t} (v_0 + at)dt \\
x - x_0 &= v_0t+\frac{1}{2}at^2 
\end{aligned} $$

> $$ v^2 = v_0^2 + 2a(x-x_0) $$

proof:  
$$ \begin{aligned}
\because v &= v_0 + at \\
v^2 &= v_0^2 +  2v_0at + a^2t^2 \qquad \qquad (1) \\
\because x - x_0 &= v_0t+\frac{1}{2}at^2 \\
a(x-x_0) &= v_0at + \frac{1}{2}a^2t^2 \\
2a(x-x_0) &= 2v_0at + a^2t^2 \qquad \qquad (2) \\
(1,2) \implies v^2 &= v_0^2 + 2a(x-x_0)



\end{aligned} $$

# Vector
> $$ \vec{A}+\vec{B} = (A_x+B_x)\hat{x} + (A_y+B_y)\hat{y} + (A_z+B_z)\hat{z} $$

> $$ |\vec{A}| = \sqrt{A_x^2 + A_y^2 + A_z^2} $$

proof:
$$ \begin{aligned}
\vec{A} \text{ component on the xy plane length: } &\sqrt{A_x^2 + A_y^2} \\
|\vec{A}| &= \sqrt{\sqrt{A_x^2 + A_y^2}^2 + A_z^2} \\
|\vec{A}| &= \sqrt{A_x^2 + A_y^2 + A_z^2}
\end{aligned} $$

# Force
> $$ F = ma \tag{unit = N} $$

> $$ \text{every action has an equal and opposite reaction} $$

### gravity
> Fg: on earth, gravity force on each object is m * g

> Fn: normal force is the perpendicular force supporting an object to not fall through another

### friction

> $$ Ff static <= μs*Fn $$

> $$ Ff dynamic = μd*Fn $$

Static friction keeps an object in place, dynamic friction acts on oppositite direction of a moving object  
Static friction can go from 0 to μs*Fn depending on force applied. Static friction coefficient is always bigger than dynamic friction  

### spring 
> $$ Fs = -kx $$
x is the displacement of the object from the spring's rest position. k is the sptring constant. the force is always the opposite to the displacement direction, pointing at the rest position  

# Energy
> $$W = F * d * cos(θ) =  \vec{F} \cdot \vec{d} \tag{unit = J}$$

> $$\text{in isolated system, energy cannot be created or destroyed, only transformed} $$

work is force on an object times the displacement along the direction of the force for that object. θ is the angle between the force and displacement vectors  
energy is the ability to do work. the ability of an object to do work and the work required to get this object to its energy level is the same. 

> $$E_k = \frac{1}{2}mv^2$$

proof:
$$ \begin{aligned}
E_k &= Fd \\
E_k &= mad \\
\because v^2 &= v_0^2 + 2a(x-x_0) \\
\because \text{energy is work required to get to this energy from zero energy }\\
v_0 &= 0\\
v^2 &= 2ad \\
ad &= \frac{1}{2}v^2 \\
E_k &= \frac{1}{2}v^2m 
\end{aligned} $$

> $$E_g = mgh $$

proof:
$$ \begin{aligned}
E_g &= Fd \\
E_G &= mad \\
\text{mg is force required to lift the object}\\
a &= g \\
\text{gravity only cares about the z component}\\
d &= h \\
E_G &= mgh
\end{aligned} $$


> $$E_s = \frac{1}{2}kx^2$$

proof:
$$ \begin{aligned}
E_s &= Fd \\
\because F &= -kx \\
\text{since the force here is pulling the spring, }&\text{it is opposite of spring }\\
F&= kx \\
\int_{x=0}^{x=d} Fdx &= \int_{x=0}^{x=d} kx \\
Fd &= \frac{1}{2}kx^2 \\
E_s &= \frac{1}{2}kx^2
\end{aligned} $$


# Momentum
> $$ p = mv \tag{unit = $kgm/s^2$} = \frac{dF}{dt} $$

> $$ \text{in an isolated enviroment, momentum is conserved} $$

Inelastic Collision: Kinetic energy is not conserved. Some converted to heat or deformation    

Elastic Collision: Kinetic energy is conserved. Object bounce off  

### elastic collision

> $$v_1 + v_1f = v_2 + v_2f $$

proof:
$$ \begin{aligned}
\because m_1v_1 + m_2v_2 &= m_1v_1f + m_2v_2f \\
m_1(v_1-v_1f) &= -m_2(v_2-v_2f) \qquad \qquad (1)\\
\because \frac{1}{2}m_1v_2^2 + \frac{1}{2}m_2v_2^2 &= \frac{1}{2}m_1v_1f^2 + \frac{1}{2}m_2v_2f^2 \\
m_1(v_1^2-v_1f^2) &= -m_2(v_2^2-v_2f^2) \qquad \qquad \\
m_1(v_1+v_1f)(v_1-v_1f) &= -m_2(v_2+v_2f)(v_2-v_2f) \qquad \qquad (2)\\
(1,2) \implies v_1 + v_1f &= v_2 + v_2f
\end{aligned}$$

> $$v_1f = \frac{(m_1-m_2)v_1 + 2m_2v_2}{m_1+m_2}$$

$$ \begin{aligned}
\because v_1 + v_1f &= v_2 + v_2f \\
v_2f &= v_1 + v_1f - v_2 \\
\because m_1v_1 + m_2v_2 &= m_1v_1f + m_2v_2f \\
m_1v_1 + m_2v_2 &= m_1v_1f + m_2(v_1+v_1f-v_2) \\
m_1v_1 + m_2v_2 &= m_1v_1f + m_2v_1 + m_2+v_1f - m_2v_2 \\
m_1v_1 -m_2v_1 + 2m_2v_2 &= (m_1+m_2)v_1f \\
\frac{v_1(m_1-m_2) + 2m_2v_2}{m_1+m_2} &= v_1f
\end{aligned}$$

# Rotation
> $$s = rθ$$

> $$ds = \frac{dv}{dt}$$

> $$ w = \frac{d\Theta}{dt} = \frac{v}{r} \tag{unit = $rad/s$}$$

> $$ \alpha = \frac{dw}{dt} = \frac{a}{r} \tag{unit = $rad/s^2$}$$

> $$ a_c = \frac{v^2}{r} $$
centripital acceleration is the acceleration needed to keep an object in a circular motion giver it's speed. centripital acceleration points towards the rotation pivot.  centripital force can come from normal force, gravity, friction, tension, etc.  
proof:  
$$ \begin{aligned}
\text{$v_1$, $v_2$, dv, $\Theta$ form a triangle similar to r, r, ds, $\Theta$. assume $v_1$ = $v_2$, express them as v} \\
\frac{dv}{v} &= \frac{ds}{r} \\
rdv &= vds \\
\frac{d(rdv)}{dt} &= \frac{d{vds}}{dt} \\
ra &= vv \\
a &= \frac{v^2}{r}




\end{aligned}$$

> $$ I = \int_{body}{}r^2dm \tag{unit = $kgm^2$}$$

inertia meaures how resistant is a rigit body to rotation, with contribution of masses across the body. r is the distance from that point of mass to the pivot of rotation. 
body in the integral mean summing over the contribution of entire object body  

> $$ T = Fsin(\Theta)r \tag{unit = Nm}$$

torque is the rotational effect of a force, measured by force component against the perpendicular of the rotational axis (angle difference is $\Theta$) times its distance from the pivot. 

> $$ T = I\alpha $$

proof:
$$ \begin{aligned}

\because T &= F_{original} sin(\Theta)r \\
let\,F &= F_{original}sin(\Theta) \\
T &= Fr \\
\int_{body}{}dT &= \int_{body}{}rdF \\
\because F &= ma \\
dF &= adm \\
dF &= \alpha rdm \\
\int_{body}{}dT &= \int_{body}{}r^2\alpha dm \\
T &= \alpha \int_{body}{}r^2 dm \\
T &= \alpha I
\end{aligned}$$

> $$ x_{cm} = \frac{m_1x_1+m_2x_2}{m_1+m_2} (discrete) = \frac{\int_{body}{}rdm}{\int_{body}{}dm}(continuous) $$

the motion of a rigid body can be separated into the translational motion of its center of mass and rotational motion around the center of mass (if no external pivot)  

> $$I = I_{cm} + md^2$$

parallel axis theorem: formula for when the pivot is not the center of mass. d is the distance between center of mass and the pivot.  
proof:  
$$ \begin{aligned}
I &= \int_{body}{}|\vec{r}|^2dm \\
I &= \int_{body}{}|\vec{r_{cm}}+\vec{d}|^2dm \\
I &= \int_{body}{}|\vec{r_{cm}}|^2+|\vec{d}|^2+2\vec{r_{cm}}\cdot\vec{d}\,dm \\
I &= \int_{body}{}|\vec{r_{cm}}|^2dm + |\vec{d}|^2\int_{body}{}dm + 2\vec{d}\cdot\int_{body}{}\vec{r_{cm}}dm \\
\text{since each dimension of $\int_{body}{}\vec{r_{cm}}dm$ equals 0}\\
I &= \int_{body}{}|\vec{r_{cm}}|^2dm + d^2m + 0 \\
I &= I_{cm} + md^2
\end{aligned}$$

> $$L = Iw \tag{unit = $kgm^2/s$}$$

> $$\vec{L_{total}} = \sum_{i}I_i\vec{w_i} + \sum_{i}m_i\vec{r_i}\times\vec{v_i}$$

the first part is the object's angular momentum along it's own spin and pivot. the second part is the object's angular momentum with a arbiatry point. r is the vector from that point to the object    

> $$\text{in an isolated enviroment, angular momentum is conserved, seperately from linear momentum}$$

> $$E_r = \frac{1}{2}Iw^2 \tag{unit = J}$$

# Gravitation

> $$F_g = \frac{G(m_1m_2)}{r^2}$$

universal gravitation is the attraction between any two objects. r is the distance between two centers of mass. 

> $$G = 6.67*10^{-11} \tag{unit = $Nm^2/km^2$}$$

> $$U = -W{gravity} = \frac{-Gm_1m_2}{r}$$

gravitation energy is 0 when objects are infinitely far apart.  the current gravitational energy's absolute value is the amount of energy needed to push it to infinitely far apart   
proof:
$$ \begin{aligned}
U &= -F_{gravity}d \\
U &= -\int_{r=\infty}^{r=r}-Gm_1m_2r^{-2}dr \\
U &= -Gm_1m_2r^{-1}
\end{aligned} $$



> $$v_{esc} = \sqrt{\frac{2Gm}{r}}$$

escape velocity is the initial velocity at the surface of a planet needed to completely escape gravitation pull of the planet  
proof:
$$ \begin{aligned}
\frac{1}{2}mv^2-\frac{GmM}{r} &= -\frac{GmM}{\infty} \\
\frac{1}{2}mv^2 &= 0+\frac{GmM}{r} \\
v^2 &= \frac{2GM}{r} \\
v &= \sqrt{\frac{2GM}{r}}

\end{aligned} $$