import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.makedirs("assets", exist_ok=True)
INK="#1f2933"; GRID="#d9dee3"; BLUE="#2563eb"; ORANGE="#e8702a"; GREEN="#2f9e44"; GREY="#8a949e"; RED="#c92a2a"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "text.color":INK,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,
 "figure.facecolor":"white","axes.facecolor":"white","svg.fonttype":"path","axes.titleweight":"bold","axes.titlesize":13})
PREVIEW=os.environ.get("PREVIEW")
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white")
    if PREVIEW: fig.savefig(f"/tmp/sb_{name}.png",bbox_inches="tight",facecolor="white",dpi=70)
    plt.close(fig)
def implied(o):
    o=np.asarray(o,float)
    with np.errstate(divide="ignore",invalid="ignore"): return np.where(o<0,-o/(-o+100),100/(o+100))
def sgn(o): return ("−" if o<0 else "+")+f"{abs(o):g}"
def profit(o,stake=100): o=np.asarray(o,float); return np.where(o<0,stake*100/-o,stake*o/100)
neg=np.linspace(-500,-100,300); pos=np.linspace(100,500,300)

# 1 Implied probability
fig,ax=plt.subplots(figsize=(8.5,4.4))
ax.plot(neg,implied(neg)*100,color=ORANGE,lw=2.6,label="Favorite: |O| ÷ (|O| + 100)")
ax.plot(pos,implied(pos)*100,color=BLUE,lw=2.6,label="Underdog: 100 ÷ (O + 100)")
ax.axvspan(-100,100,color=GREY,alpha=.12,lw=0); ax.text(0,73,"Not used:\n−100 and +100\nare the same\nprice (50%)",ha="center",fontsize=9.5,color=GREY)
ax.axhline(50,color=GREY,ls=":",lw=1)
for o,c,dx,dy in [(-150,ORANGE,-8,10),(-110,ORANGE,-8,10),(130,BLUE,8,8)]:
    p=float(implied(o))*100; ax.plot(o,p,"o",color=c,ms=8,zorder=5)
    ax.annotate(f"{sgn(o)} → {p:.2f}%",xy=(o,p),xytext=(dx,dy),textcoords="offset points",ha="right" if dx<0 else "left",fontsize=9.5,color=c)
ax.set_xlim(-500,500); ax.set_ylim(10,90); ax.set_xticks([-500,-400,-300,-200,-100,100,200,300,400,500])
ax.set_xticklabels(["−500","−400","−300","−200","−100","+100","+200","+300","+400","+500"])
ax.set_xlabel("American odds"); ax.set_ylabel("Implied probability (%)"); ax.legend(frameon=False,loc="upper right",fontsize=9.5)
ax.set_title("Implied Probability from American Odds",loc="left"); save(fig,"implied_probability")

# 2 Overround and no-vig
mk=[("−150 / +130",150,130),("−110 / −110",110,110)]
fig,ax=plt.subplots(figsize=(9,4.6)); ax.grid(axis="y",visible=False)
rows=[]
for name,F,U in mk:
    A=F/(F+100); B=(100/(U+100)) if F!=U else F/(F+100); T=A+B
    rows.append((f"{name}\nimplied",A*100,B*100)); rows.append((f"{name}\nfair (no-vig)",A/T*100,B/T*100))
ys=[4.2,3.2,1.6,0.6]
for (lab,a,b),y in zip(rows,ys):
    ax.barh(y,a,height=.62,color=ORANGE,alpha=.9); ax.barh(y,b,left=a,height=.62,color=BLUE,alpha=.9)
    ax.text(a/2,y,f"{a:.2f}",ha="center",va="center",color="white",fontweight="bold",fontsize=10)
    ax.text(a+b/2,y,f"{b:.2f}",ha="center",va="center",color="white",fontweight="bold",fontsize=10)
    if a+b>100.001:
        ax.barh(y,a+b-100,left=100,height=.62,color=RED,alpha=.25,hatch="///",edgecolor=RED,lw=0)
        ax.text(a+b+1,y,f"total {a+b:.2f}%\noverround {a+b-100:.2f}%",va="center",fontsize=9.5,color=RED)
    else: ax.text(a+b+1,y,"total 100%",va="center",fontsize=9.5,color=GREEN)
ax.axvline(100,color=INK,lw=1.2,ls="--")
ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows],fontsize=9.5)
ax.set_xlim(0,128); ax.set_ylim(0,4.9); ax.set_xlabel("Probability (%)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=ORANGE,label="Favorite / first side"),Patch(color=BLUE,label="Underdog / second side"),Patch(fc=RED,alpha=.25,hatch="///",ec=RED,label="Margin above 100%")],frameon=False,loc="upper center",bbox_to_anchor=(.45,-.14),ncol=3,fontsize=9.5)
ax.set_title("Removing the Margin: implied ÷ total = fair",loc="left"); save(fig,"no_vig")

# 3 Profit on 100 stake
fig,ax=plt.subplots(figsize=(8.5,4.4))
ax.plot(neg,profit(neg),color=ORANGE,lw=2.6,label="Negative odds: stake × 100 ÷ |O|")
ax.plot(pos,profit(pos),color=BLUE,lw=2.6,label="Positive odds: stake × O ÷ 100")
ax.axvspan(-100,100,color=GREY,alpha=.12,lw=0); ax.axhline(100,color=GREY,ls=":",lw=1); ax.text(490,82,"Even money: profit = stake",fontsize=9,color=GREY,ha="right")
for o,c,dx,dy in [(-150,ORANGE,-10,14),(-110,ORANGE,10,14),(130,BLUE,8,-16)]:
    p=float(profit(o)); ax.plot(o,p,"o",color=c,ms=8,zorder=5)
    ax.annotate(f"{sgn(o)} → {p:.2f}",ha="right" if dx<0 else "left",xy=(o,p),xytext=(dx,dy),textcoords="offset points",fontsize=9.5,color=c)
ax.set_xlim(-500,500); ax.set_ylim(0,520); ax.set_xticks([-500,-400,-300,-200,-100,100,200,300,400,500])
ax.set_xticklabels(["−500","−400","−300","−200","−100","+100","+200","+300","+400","+500"])
ax.set_xlabel("American odds"); ax.set_ylabel("Profit on a 100 stake"); ax.legend(frameon=False,loc="upper center",fontsize=9.5)
ax.set_title("Profit on a Winning 100 Stake",loc="left"); save(fig,"profit")

# 4 Conversion
fig,ax=plt.subplots(figsize=(8.5,4.4))
d1=np.linspace(1.12,2,300); d2=np.linspace(2,4,300)
ax.plot(d1,-100/(d1-1),color=ORANGE,lw=2.6,label="d < 2:  O = −100 ÷ (d − 1)")
ax.plot(d2,(d2-1)*100,color=BLUE,lw=2.6,label="d ≥ 2:  O = (d − 1) × 100")
ax.plot([2,2],[-100,100],color=GREY,ls=":",lw=1.5); ax.text(2.06,-250,"At 2.00, −100 and +100\nare the same price",fontsize=9,color=GREY,va="top")
pts=[(1.5,ORANGE,(-10,-6)),(1+2/3,ORANGE,(10,-12)),(2.3,BLUE,(10,-14)),(2.5,BLUE,(-10,10))]
for d,c,off in pts:
    o=-100/(d-1) if d<2 else (d-1)*100; ax.plot(d,o,"o",color=c,ms=8,zorder=5)
    ax.annotate(f"{d:.2f} ↔ {sgn(round(o))}",xy=(d,o),xytext=off,textcoords="offset points",fontsize=9.5,color=c,ha="right" if off[0]<0 else "left")
ax.axhline(0,color=INK,lw=.8); ax.set_xlim(1,4); ax.set_ylim(-800,420)
ax.set_xlabel("Decimal odds d"); ax.set_ylabel("American odds O"); ax.legend(frameon=False,loc="lower right",fontsize=9.5)
ax.set_title("Decimal and American Odds",loc="left"); save(fig,"odds_conversion")
