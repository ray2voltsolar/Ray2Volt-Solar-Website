# Variations on cover option 10 ("Sun paths"): nested arcs like the sun's path through the year.
import math, json
W,H=696,448
NAVY,NAVY2,GOLD,GOLD2,CYAN,CYAN2,PAPER='#0B1F3A','#12305A','#E0A106','#F2C24B','#0C9BBE','#7CCBE0','#F5F7FA'
def mix(a,b,t):
    a=[int(a[i:i+2],16) for i in(1,3,5)]; b=[int(b[i:i+2],16) for i in(1,3,5)]
    return '#%02X%02X%02X'%tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def arc(amp,x0=60,x1=W-60,base=400,p=1.2,step=5):
    return 'M'+' L'.join(f'{x:.1f} {base-amp*math.sin(math.pi*(x-x0)/(x1-x0))**p:.1f}' for x in range(int(x0),int(x1)+1,step))
def svg(body,defs='',w=W,h=H): return f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Abstract cover graphic: nested arcs like the sun\'s path across the sky through the year"><defs>{defs}</defs>{body}</svg>'
bgd=f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY2}"/></linearGradient>'
dark=f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'; light=f'<rect width="{W}" height="{H}" fill="{PAPER}"/>'; white=f'<rect width="{W}" height="{H}" fill="#fff"/>'
amps=[60+i*17 for i in range(12)]; top=amps[-1]
o={}

# A: the original, light ground
b=light
for i,a in enumerate(amps): b+=f'<path d="{arc(a)}" fill="none" stroke="{GOLD if i==11 else NAVY}" stroke-width="{2 if i==11 else .9}" stroke-opacity="{1 if i==11 else .2+i*.05:.2f}"/>'
b+=f'<path d="M40 400H{W-40}" stroke="{NAVY}"/><circle cx="{W/2}" cy="{400-top}" r="6" fill="{PAPER}" stroke="{GOLD}" stroke-width="2"/>'
o['A  Original, light']={'svg':svg(b)}

# B: navy ground, gold lines
b=dark
for i,a in enumerate(amps): b+=f'<path d="{arc(a)}" fill="none" stroke="{GOLD2}" stroke-width="{2.2 if i==11 else 1}" stroke-opacity="{1 if i==11 else .18+i*.055:.2f}"/>'
b+=f'<path d="M40 400H{W-40}" stroke="#fff" stroke-opacity=".5"/><circle cx="{W/2}" cy="{400-top}" r="6" fill="{NAVY}" stroke="{GOLD2}" stroke-width="2.200"/>'
o['B  Navy and gold']={'svg':svg(b,bgd)}

# C: navy ground, lines graded from cyan (low) to gold (high)
b=dark
for i,a in enumerate(amps): b+=f'<path d="{arc(a)}" fill="none" stroke="{mix(CYAN2,GOLD2,i/11)}" stroke-width="{2.2 if i==11 else 1.200}" stroke-opacity="{.5+i*.045:.2f}"/>'
b+=f'<path d="M40 400H{W-40}" stroke="#fff" stroke-opacity=".5"/>'
o['C  Cyan to gold']={'svg':svg(b,bgd)}

# D: white ground, translucent gold layers between arcs
b=white
for i,a in enumerate(reversed(amps)): b+=f'<path d="{arc(a)} L{W-60} 400 L60 400 Z" fill="{GOLD}" fill-opacity=".085"/>'
b+=f'<path d="{arc(top)}" fill="none" stroke="{GOLD}" stroke-width="2"/><path d="M40 400H{W-40}" stroke="{NAVY}"/>'
o['D  Layered gold']={'svg':svg(b)}

# E: with a time axis and month marks
b=light
for i,a in enumerate(amps): b+=f'<path d="{arc(a,base=372)}" fill="none" stroke="{GOLD if i==11 else NAVY}" stroke-width="{2 if i==11 else .9}" stroke-opacity="{1 if i==11 else .2+i*.05:.2f}"/>'
b+=f'<path d="M40 372H{W-40}" stroke="{NAVY}"/><path d="M{W/2} 372V{372-top+8}" stroke="{GOLD}" stroke-dasharray="2 3"/>'
for i,a in enumerate(amps): b+=f'<circle cx="{W/2}" cy="{372-a}" r="{3 if i==11 else 1.600}" fill="{GOLD if i==11 else NAVY}"/>'
for x,t in [(60,'SUNRISE'),(W/2,'NOON'),(W-60,'SUNSET')]: b+=f'<path d="M{x} 372v6" stroke="{NAVY}"/><text x="{x}" y="394" text-anchor="middle" font-size="7.500" font-weight="600" letter-spacing="1.800" style="fill:#627287">{t}</text>'
b+=f'<text x="{W/2+12}" y="{372-top+3}" font-size="7.500" font-weight="700" letter-spacing="1.800" style="fill:#8A5F00">SUMMER</text><text x="{W/2+12}" y="{372-amps[0]+3}" font-size="7.500" font-weight="700" letter-spacing="1.800" style="fill:#627287">WINTER</text>'
o['E  With axis labels']={'svg':svg(b)}

# F: fine and dense, 30 hairlines
b=light; A=[40+i*8.3 for i in range(30)]
for i,a in enumerate(A): b+=f'<path d="{arc(a,p=1.15)}" fill="none" stroke="{GOLD if i==29 else NAVY}" stroke-width="{1.800 if i==29 else .6}" stroke-opacity="{1 if i==29 else .25+i*.02:.2f}"/>'
b+=f'<path d="M40 400H{W-40}" stroke="{NAVY}"/>'
o['F  Fine lines']={'svg':svg(b)}

# G: cropped and large, arcs running off the right edge, navy
b=dark; A=[90+i*30 for i in range(12)]
for i,a in enumerate(A): b+=f'<path d="{arc(a,x0=120,x1=W+420,base=430,p=1.1)}" fill="none" stroke="{GOLD2}" stroke-width="{2.2 if i==11 else 1}" stroke-opacity="{1 if i==11 else .2+i*.055:.2f}"/>'
o['G  Cropped, navy']={'svg':svg(b,bgd)}

# H: cropped and large on light ground
b=light
for i,a in enumerate(A): b+=f'<path d="{arc(a,x0=120,x1=W+420,base=430,p=1.1)}" fill="none" stroke="{GOLD if i==11 else NAVY}" stroke-width="{2.2 if i==11 else .9}" stroke-opacity="{1 if i==11 else .2+i*.05:.2f}"/>'
o['H  Cropped, light']={'svg':svg(b)}

# I: three arcs only
b=light
for a,c,wd in [(110,NAVY,1),(190,NAVY,1),(270,GOLD,2.2)]: b+=f'<path d="{arc(a)}" fill="none" stroke="{c}" stroke-width="{wd}" stroke-opacity="{1 if c==GOLD else .55}"/>'
b+=f'<path d="M40 400H{W-40}" stroke="{NAVY}"/><circle cx="{W/2}" cy="130" r="6" fill="{PAPER}" stroke="{GOLD}" stroke-width="2"/>'
o['I  Three arcs']={'svg':svg(b)}

# J: no panel at all: arcs on the white page, wider, with a solid gold sun at the peak
b=white
for i,a in enumerate(amps): b+=f'<path d="{arc(a,x0=0,x1=W)}" fill="none" stroke="{NAVY}" stroke-width=".9" stroke-opacity="{.16+i*.05:.2f}"/>'
b+=f'<path d="{arc(top,x0=0,x1=W)}" fill="none" stroke="{GOLD}" stroke-width="2"/><path d="M0 400H{W}" stroke="{NAVY}"/><circle cx="{W/2}" cy="{400-top}" r="11" fill="{GOLD}"/>'
o['J  Open page, gold sun']={'svg':svg(b)}

# K: full-bleed navy band across the whole page width
b=dark
for i,a in enumerate(amps): b+=f'<path d="{arc(a,x0=20,x1=W-20)}" fill="none" stroke="{GOLD2}" stroke-width="{2.2 if i==11 else 1}" stroke-opacity="{1 if i==11 else .18+i*.055:.2f}"/>'
b+=f'<path d="M0 400H{W}" stroke="#fff" stroke-opacity=".5"/>'
o['K  Full-width navy band']={'svg':svg(b,bgd),'css':'.p01 .photo{margin-left:0!important;margin-right:0!important}'}

# L: gold ground, navy lines
b=f'<rect width="{W}" height="{H}" fill="{GOLD2}"/>'
for i,a in enumerate(amps): b+=f'<path d="{arc(a)}" fill="none" stroke="{NAVY}" stroke-width="{2.2 if i==11 else 1}" stroke-opacity="{1 if i==11 else .25+i*.05:.2f}"/>'
b+=f'<path d="M40 400H{W-40}" stroke="{NAVY}"/>'
o['L  Gold ground']={'svg':svg(b)}

json.dump(o,open('cover-options/options10.json','w')); print(len(o))
