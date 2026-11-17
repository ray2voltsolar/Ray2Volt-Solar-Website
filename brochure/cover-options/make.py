# Generates 10 cover-art options (SVG fragments) for the brochure cover panel (696 x 448).
import math, json, random
W,H=696,448
NAVY,NAVY2,GOLD,GOLD2,CYAN,CYAN2,BLUE,GREEN='#0B1F3A','#12305A','#E0A106','#F2C24B','#0C9BBE','#7CCBE0','#1257C9','#17855A'
def wrap(body,defs=''):
    return f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Abstract cover graphic"><defs>{defs}<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY2}"/></linearGradient></defs>{body}</svg>'
bg=f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
light=f'<rect width="{W}" height="{H}" fill="#F5F7FA"/>'
o={}

# 1 Concentric arcs: a sun rising from the lower-right corner
b=bg
for i,r in enumerate(range(60,620,40)):
    b+=f'<circle cx="{W-150}" cy="{H}" r="{r}" fill="none" stroke="{GOLD2}" stroke-width="{1.6 if i<3 else 1}" stroke-opacity="{max(.12,.95-i*.07):.2f}"/>'
b+=f'<circle cx="{W-150}" cy="{H}" r="56" fill="{GOLD}"/>'
o['01 Rising arcs']=wrap(b)

# 2 Cell grid with a band of light sweeping across
b=bg; cs=40; gap=4
for r in range(-1,H//cs+2):
    for c in range(-1,W//cs+2):
        x=c*cs+gap/2+8; y=r*cs+gap/2+4
        d=(c*1.0 - r*1.35) - 6.0          # distance from a diagonal band
        t=math.exp(-(d/2.6)**2)
        if t>.04:
            col=GOLD2 if d<0 else CYAN2
            b+=f'<rect x="{x}" y="{y}" width="{cs-gap}" height="{cs-gap}" rx="2" fill="{col}" fill-opacity="{t*.95:.2f}"/>'
        b+=f'<rect x="{x}" y="{y}" width="{cs-gap}" height="{cs-gap}" rx="2" fill="none" stroke="#fff" stroke-opacity=".10"/>'
o['02 Light on cells']=wrap(b)

# 3 Horizon: half sun on a line, panel rows receding below
b=bg+f'<circle cx="{W/2}" cy="250" r="118" fill="{GOLD}"/><rect x="0" y="250" width="{W}" height="{H-250}" fill="{NAVY}"/>'
b+=f'<path d="M0 250H{W}" stroke="#fff" stroke-opacity=".7" stroke-width="1"/>'
for i in range(1,9):
    y=250+ (i**1.75)*4.6
    b+=f'<path d="M0 {y:.1f}H{W}" stroke="{CYAN2}" stroke-opacity="{.55-i*.045:.2f}" stroke-width="1"/>'
for k in range(-12,13):
    b+=f'<path d="M{W/2+k*14:.1f} 250L{W/2+k*120:.1f} {H}" stroke="{CYAN2}" stroke-opacity=".16" stroke-width="1"/>'
o['03 Horizon']=wrap(b)

# 4 Rays: fine lines radiating from a point, on white
b=light; cx,cy=120,H+40
for i in range(0,61):
    a=math.radians(-88+i*1.55); L=900
    col=GOLD if i%5==0 else '#B9C4D1'
    b+=f'<path d="M{cx} {cy}L{cx+L*math.cos(a):.1f} {cy+L*math.sin(a):.1f}" stroke="{col}" stroke-width="{1.4 if i%5==0 else .8}"/>'
b+=f'<circle cx="{cx}" cy="{cy}" r="150" fill="#F5F7FA"/><circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="{NAVY}" stroke-width="1.200"/>'
o['04 Rays']=wrap(b)

# 5 Monthly bars: twelve columns, gold fading to navy
b=bg; vals=[.62,.72,.86,.95,1,.88,.70,.68,.74,.80,.70,.60]; bw=30; gp=(W-120-12*bw)/11
dfs=f'<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD2}"/><stop offset="1" stop-color="{GOLD}" stop-opacity=".15"/></linearGradient>'
for i,v in enumerate(vals):
    x=60+i*(bw+gp); h=v*290
    b+=f'<rect x="{x:.1f}" y="{380-h:.1f}" width="{bw}" height="{h:.1f}" fill="url(#bar)"/>'
b+=f'<path d="M40 380H{W-40}" stroke="#fff" stroke-opacity=".5"/>'
o['05 Twelve months']=wrap(b,dfs)

# 6 Technical drawing: one large tilted panel in line art on light ground
b=light
P=[(150,330),(470,330),(580,110),(260,110)]
def lerp(a,b,t): return (a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
b+=f'<path d="M{P[0][0]} {P[0][1]}L{P[1][0]} {P[1][1]}L{P[2][0]} {P[2][1]}L{P[3][0]} {P[3][1]}Z" fill="{NAVY}"/>'
for i in range(1,8):
    a=lerp(P[0],P[1],i/8); c=lerp(P[3],P[2],i/8); b+=f'<path d="M{a[0]:.1f} {a[1]:.1f}L{c[0]:.1f} {c[1]:.1f}" stroke="{CYAN2}" stroke-opacity=".5" stroke-width="1"/>'
for i in range(1,5):
    a=lerp(P[0],P[3],i/5); c=lerp(P[1],P[2],i/5); b+=f'<path d="M{a[0]:.1f} {a[1]:.1f}L{c[0]:.1f} {c[1]:.1f}" stroke="{CYAN2}" stroke-opacity=".5" stroke-width="1"/>'
b+=f'<path d="M230 330V392M420 330V392M180 392H470" stroke="{NAVY}" stroke-width="1.400" fill="none"/>'
b+=f'<path d="M40 392H{W-40}" stroke="{NAVY}" stroke-width="1"/>'
b+=f'<circle cx="112" cy="96" r="30" fill="none" stroke="{GOLD}" stroke-width="2"/>'
for k in range(5): b+=f'<path d="M{146+k*0} {118+k*0}" />'
for k in range(4):
    b+=f'<path d="M{150+k*26} {112+k*26}L{232+k*26} {146+k*26}" stroke="{GOLD}" stroke-width="1" stroke-dasharray="3 4"/>'
o['06 Blueprint']=wrap(b)

# 7 Swiss blocks: circle, quarter, square
u=H/2
b=f'<rect width="{W}" height="{H}" fill="#F5F7FA"/>'
b+=f'<rect x="0" y="0" width="{u}" height="{u}" fill="{NAVY}"/><circle cx="{u/2}" cy="{u/2}" r="{u*.32}" fill="{GOLD}"/>'
b+=f'<rect x="{u}" y="0" width="{u}" height="{u}" fill="{GOLD}"/><path d="M{u} {u}A{u} {u} 0 0 1 {2*u} 0V{u}Z" fill="{NAVY}"/>'
b+=f'<rect x="{2*u}" y="0" width="{W-2*u}" height="{u}" fill="{CYAN}"/>'
b+=f'<rect x="0" y="{u}" width="{u}" height="{u}" fill="{CYAN2}"/><path d="M0 {u}A{u} {u} 0 0 0 {u} {2*u}H0Z" fill="{BLUE}"/>'
b+=f'<rect x="{u}" y="{u}" width="{u}" height="{u}" fill="{NAVY2}"/>'
for i in range(1,6): b+=f'<path d="M{u+i*u/6:.1f} {u}V{2*u}" stroke="{CYAN2}" stroke-opacity=".45"/><path d="M{u} {u+i*u/6:.1f}H{2*u}" stroke="{CYAN2}" stroke-opacity=".45"/>'
b+=f'<rect x="{2*u}" y="{u}" width="{W-2*u}" height="{u}" fill="{NAVY}"/><path d="M{2*u} {2*u}A{W-2*u} {W-2*u} 0 0 1 {W} {2*u-(W-2*u)}V{2*u}Z" fill="{GOLD2}"/>'
o['07 Colour blocks']=wrap(b)

# 8 Ribbons: energy flowing left to right
b=bg
def rib(y0a,y0b,y1a,y1b,col,op):
    m=W/2
    return f'<path d="M0 {y0a}C{m} {y0a} {m} {y1a} {W} {y1a}L{W} {y1b}C{m} {y1b} {m} {y0b} 0 {y0b}Z" fill="{col}" fill-opacity="{op}"/>'
b+=rib(70,190,40,120,GOLD2,.9)+rib(190,250,170,290,GREEN,.85)+rib(250,380,330,410,BLUE,.85)+rib(190,196,120,170,CYAN2,.5)
o['08 Energy ribbons']=wrap(b)

# 9 Halftone sun: dots sized by distance from a centre
b=bg; cx,cy=W*.68,H*.42; st=18
for r in range(0,H//st+2):
    for c in range(0,W//st+2):
        x=c*st+ (st/2 if r%2 else 0); y=r*st
        d=math.hypot(x-cx,y-cy); rad=max(0,7.2*(1-d/330))
        if rad>.5: b+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.2f}" fill="{GOLD2}"/>'
        else: b+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r=".7" fill="#fff" fill-opacity=".18"/>'
o['09 Halftone sun']=wrap(b)

# 10 Contours: nested sine "sun path" lines, one for each month, on white
b=light
for i in range(12):
    amp=60+i*17; col=GOLD if i in(11,) else NAVY
    pts=' L'.join(f'{x:.1f} {400-amp*math.sin(math.pi*(x-60)/(W-120))**1.2:.1f}' for x in range(60,W-59,6))
    b+=f'<path d="M{pts}" fill="none" stroke="{col}" stroke-width="{2 if i==11 else .9}" stroke-opacity="{1 if i==11 else .2+i*.05:.2f}"/>'
b+=f'<path d="M40 400H{W-40}" stroke="{NAVY}" stroke-width="1"/><circle cx="{W/2}" cy="{400-(60+11*17)}" r="6" fill="#F5F7FA" stroke="{GOLD}" stroke-width="2"/>'
o['10 Sun paths']=wrap(b)

json.dump(o,open('cover-options/options.json','w'))
print(len(o))
