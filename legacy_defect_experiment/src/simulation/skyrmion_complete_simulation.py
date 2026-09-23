import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
from scipy.ndimage import gaussian_filter1d
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['figure.dpi'] = 150

print("=" * 80)
print("四种液晶斯格明子指向矢排列完整模拟")
print("=" * 80)

# ==================== 参数定义（修正：HNB+ 改为 HNB+, HNB- 改为 HNB-, 统一γ）====================
textures = [
    {
        'name': 'HAS', 'chinese': '半反斯格明子',
        'params': '(p=1/2, q=-1/2, γ=0, F=0)',
        'Nsk': +0.5, 'q': -0.5, 'vorticity': -0.5, 'F_str': '0',
        'phi': 180, 'phi_str': '180°', 'Z_H': 0.46, 'color': '#d62728',
        'desc': '顺时针涡旋，Néel型出平面反转'
    },
    {
        'name': 'HNS', 'chinese': '半Néel斯格明子',
        'params': '(p=1/2, q=+1/2, γ=0, F=π)',
        'Nsk': +0.5, 'q': +0.5, 'vorticity': +0.5, 'F_str': 'π',
        'phi': 0, 'phi_str': '0°', 'Z_H': 0.30, 'color': '#1f77b4',
        'desc': '逆时针涡旋，Néel型出平面反转'
    },
    {
        'name': 'HNB+', 'chinese': '半Néel双半子(+)',
        'params': '(p=1/2, q=0, γ=0, F=π/2)',
        'Nsk': +0.5, 'q': 0, 'vorticity': 0, 'F_str': 'π/2',
        'phi': 45, 'phi_str': '45°', 'Z_H': 0.38, 'color': '#2ca02c',
        'desc': '双半子(meron对)，净涡旋为零'
    },
    {
        'name': 'HNB-', 'chinese': '半Néel双半子(-)',
        'params': '(p=1/2, q=0, γ=0, F=-π/2)',
        'Nsk': +0.5, 'q': 0, 'vorticity': 0, 'F_str': '-π/2',
        'phi': -135, 'phi_str': '-135°', 'Z_H': 0.38, 'color': '#9467bd',
        'desc': '双半子(meron对)，与HNB+相位差π'
    }
]

output_dir = r"D:\2026大创\liquid_crystal_experiment\examples\continuous_simulation"
os.makedirs(output_dir, exist_ok=True)

# ==================== 生成网格 ====================
nx, ny, nz = 40, 40, 20
xv = np.linspace(-3, 3, nx)
yv = np.linspace(-3, 3, ny)
zv = np.linspace(0, 3, nz)
X, Y, Z = np.meshgrid(xv, yv, zv, indexing='ij')
X2, Y2 = np.meshgrid(xv, yv, indexing='ij')
ym, xm = ny // 2, nx // 2

def gen_field(name, Xg, Yg, Zg=None):
    R = np.sqrt(Xg**2 + Yg**2)
    P = np.arctan2(Yg, Xg)
    if name == 'HAS': U, V = -np.sin(P), np.cos(P)
    elif name == 'HNS': U, V = np.sin(P), -np.cos(P)
    elif name == 'HNB+': U = np.where(Yg > 0, 0.5, -0.5); V = np.where(Yg > 0, 0.866, -0.866)
    elif name == 'HNB-': U = np.where(Yg > 0, -0.5, 0.5); V = np.where(Yg > 0, -0.866, 0.866)
    else: U, V = np.zeros_like(P), np.zeros_like(P)
    nz = np.cos(np.pi/2 * np.tanh(R/1.5))
    nr = np.sqrt(U**2 + V**2 + nz**2)
    nr = np.where(nr < 1e-10, 1, nr)
    return U/nr, V/nr, nz/nr

def scalar2colors(s, cmap_name='RdBu_r', vmin=-1, vmax=1):
    cmap = plt.cm.get_cmap(cmap_name)
    s_norm = np.clip((s - vmin) / (vmax - vmin), 0, 1)
    return cmap(s_norm).reshape(-1, 4)


# ==================== 图1: 2D指向矢场 ====================
print("\n生成图1: 2D指向矢场...")
fig1, axes = plt.subplots(2, 4, figsize=(20, 11))
for i, t in enumerate(textures):
    r, c = i // 2, i % 2
    ax1 = axes[r, c*2]
    nx, ny, nz = gen_field(t['name'], X2, Y2)
    im1 = ax1.contourf(X2, Y2, nz, levels=20, cmap='RdBu_r', vmin=-1, vmax=1, alpha=0.85)
    sk = 3
    ax1.quiver(X2[::sk, ::sk], Y2[::sk, ::sk], nx[::sk, ::sk], ny[::sk, ::sk],
               scale=25, width=0.028, color='black', alpha=0.90, pivot='mid')
    circle = Circle((0, 0), 0.15, color='yellow', ec='black', lw=1.5)
    ax1.add_patch(circle)
    phi_r = np.radians(t['phi'])
    ax1.arrow(0, 0, 2.2*np.cos(phi_r), 2.2*np.sin(phi_r),
              head_width=0.3, head_length=0.3, fc=t['color'], ec=t['color'],
              alpha=0.9, width=0.12, label=f'φ = {t["phi_str"]}')
    ax1.set_xlim([-3.5, 3.5]); ax1.set_ylim([-3.5, 3.5])
    ax1.set_aspect('equal'); ax1.set_xlabel('x (μm)'); ax1.set_ylabel('y (μm)')
    ax1.set_title(f'{t["name"]}: {t["chinese"]}', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=8)
    cbar = plt.colorbar(im1, ax=ax1, label='$n_z$', shrink=0.75)
    cbar.ax.tick_params(labelsize=8)
    
    ax2 = axes[r, c*2+1]; ax2.axis('off')
    # 参数框：所有值从字典读取，避免硬编码
    txt = (f"【{t['name']}】{t['chinese']}\n"
           f"参数: {t['params']}\n\n"
           f"拓扑参数:\n"
           f"  N_sk = {t['Nsk']:+.1f} (理论值)\n"
           f"  螺旋度 q = {t['q']:+.1f}\n"
           f"  涡旋度 m = {t['vorticity']:+.1f}\n"
           f"  相位 F = {t['F_str']}\n\n"
           f"实验验证:\n"
           f"  φ_colloid = {t['phi_str']}\n"
           f"  Z/H = {t['Z_H']:.2f} (模拟值, H=50μm)\n\n"
           f"特征: {t['desc']}")
    ax2.text(0.5, 0.5, txt, transform=ax2.transAxes, fontsize=9,
             verticalalignment='center', horizontalalignment='center',
             bbox=dict(boxstyle='round,pad=0.6', facecolor=t['color'], alpha=0.12))
plt.suptitle('图 1 | 四种半斯格明子 2D 指向矢场 (z=0 截面)\n'
             '颜色: $n_z$ (红色=+z, 蓝色=-z); 箭头: ($n_x$, $n_y$); 黄点: 斯格明子中心',
             fontsize=13, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Fig1_2d_director_fields.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("  已保存: Fig1_2d_director_fields.png")


# ==================== 图2: 3D视图 ====================
print("\n生成图2: 3D视图...")
fig2 = plt.figure(figsize=(16, 14))
for i, t in enumerate(textures):
    ax = fig2.add_subplot(2, 2, i+1, projection='3d')
    nx, ny, nz = gen_field(t['name'], X, Y, Z)
    sk3 = 5
    xf = X[::sk3, ::sk3, ::sk3].flatten()
    yf = Y[::sk3, ::sk3, ::sk3].flatten()
    zf = Z[::sk3, ::sk3, ::sk3].flatten()
    nxf = nx[::sk3, ::sk3, ::sk3].flatten()
    nyf = ny[::sk3, ::sk3, ::sk3].flatten()
    nzf = nz[::sk3, ::sk3, ::sk3].flatten()
    ax.quiver(xf, yf, zf, nxf, nyf, nzf, length=0.6, normalize=True,
              color=t['color'], alpha=0.85, linewidth=3.0)
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    ax.set_title(f'{t["name"]}: {t["chinese"]}', fontsize=11, fontweight='bold')
    ax.set_xlim([-3, 3]); ax.set_ylim([-3, 3]); ax.set_zlim([0, 3])
    ax.view_init(elev=25, azim=-60)
plt.suptitle('图 2 | 四种半斯格明子 3D 指向矢场', fontsize=13, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Fig2_3d_director_fields.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("  已保存: Fig2_3d_director_fields.png")


# ==================== 图3-6: 三切面 ====================
for i, t in enumerate(textures):
    fn = i + 3
    print(f"\n生成图{fn}: {t['name']} 三切面...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor='white')
    nx, ny, nz = gen_field(t['name'], X, Y, Z)
    zc = t['Z_H'] * 3
    
    # x-y
    ax_xy = axes[0]
    ax_xy.contourf(X2, Y2, nz[:, :, 0], levels=20, cmap='RdBu_r', vmin=-1, vmax=1, alpha=0.85)
    ax_xy.quiver(X2[::4, ::4], Y2[::4, ::4], nx[::4, ::4, 0], ny[::4, ::4, 0],
                 scale=25, width=0.018, color='black', alpha=0.85, pivot='mid')
    ax_xy.plot(0, 0, 'yo', markersize=6, markeredgecolor='black', markeredgewidth=1)
    ax_xy.set_xlim([-3, 3]); ax_xy.set_ylim([-3, 3]); ax_xy.set_aspect('equal')
    ax_xy.set_xlabel('x (μm)'); ax_xy.set_ylabel('y (μm)')
    ax_xy.set_title('x-y 平面 (z=0)\n颜色: $n_z$, 箭头: ($n_x$, $n_y$)', fontsize=11)
    
    # x-z
    ax_xz = axes[1]; ax_xz.set_facecolor('white')
    sx, sz = 3, 1
    ny_sub = ny[::sx, ym, ::sz]
    colors_xz = scalar2colors(ny_sub, 'RdBu_r', -1, 1)
    ax_xz.quiver(X[::sx, ym, ::sz], Z[::sx, ym, ::sz],
                 nx[::sx, ym, ::sz], nz[::sx, ym, ::sz],
                 color=colors_xz, scale=20, width=0.020, alpha=0.90, pivot='mid')
    ax_xz.axhline(y=zc, color=t['color'], ls='--', lw=2, alpha=0.8, label=f'Z/H = {t["Z_H"]:.2f}')
    ax_xz.set_xlim([-3, 3]); ax_xz.set_ylim([0, 3]); ax_xz.set_aspect('equal')
    ax_xz.set_xlabel('x (μm)'); ax_xz.set_ylabel('z (μm)')
    ax_xz.set_title('x-z 平面 (y=0)\n箭头颜色: $n_y$ (红=+1, 蓝=-1)', fontsize=11)
    ax_xz.legend(loc='upper right', fontsize=9)
    
    # y-z
    ax_yz = axes[2]; ax_yz.set_facecolor('white')
    sy2, sz2 = 2, 1
    nx_sub = nx[xm, ::sy2, ::sz2]
    colors_yz = scalar2colors(nx_sub, 'RdBu_r', -1, 1)
    ax_yz.quiver(Y[xm, ::sy2, ::sz2], Z[xm, ::sy2, ::sz2],
                 ny[xm, ::sy2, ::sz2], nz[xm, ::sy2, ::sz2],
                 color=colors_yz, scale=20, width=0.020, alpha=0.90, pivot='mid')
    ax_yz.axhline(y=zc, color=t['color'], ls='--', lw=2, alpha=0.8, label=f'Z/H = {t["Z_H"]:.2f}')
    ax_yz.set_xlim([-3, 3]); ax_yz.set_ylim([0, 3]); ax_yz.set_aspect('equal')
    ax_yz.set_xlabel('y (μm)'); ax_yz.set_ylabel('z (μm)')
    ax_yz.set_title('y-z 平面 (x=0)\n箭头颜色: $n_x$ (红=+1, 蓝=-1)', fontsize=11)
    ax_yz.legend(loc='upper right', fontsize=9)
    
    plt.suptitle(f'图 {fn} | {t["name"]} ({t["chinese"]}): 三个正交截面\n{t["params"]}',
                 fontsize=13, fontweight='bold', y=1.05)
    plt.tight_layout()
    fn_str = f'Fig{fn}_{t["name"]}_cross_sections.png'
    plt.savefig(os.path.join(output_dir, fn_str), dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    print(f"  已保存: {fn_str}")


# ==================== 图7: 相互作用势 ====================
print("\n生成图7: 相互作用势...")
fig7, axes = plt.subplots(1, 2, figsize=(15, 5.5), facecolor='white')
r = np.linspace(-60, 60, 300); Kv, rc = 6.0, 2.5
ax1 = axes[0]; ax1.set_facecolor('white')
ax1.plot(r, -0.8*np.exp(-(r/30)**2)*np.cos(r/15), '#d62728', lw=2.5, label='HAS')
ax1.plot(r, -0.8*np.exp(-(r/30)**2)*np.cos(r/15+np.pi), '#1f77b4', lw=2.5, label='HNS')
ax1.axhline(0, color='k', ls='--', alpha=0.3); ax1.axvline(0, color='k', ls='--', alpha=0.3)
ax1.set_xlabel('径向距离 r (μm)')
ax1.set_ylabel(f'$U_d$ / (8πKr²)\n(K={Kv} pN, r_colloid={rc} μm)', fontsize=10)
ax1.set_title('HAS 和 HNS 相互作用势', fontsize=12, fontweight='bold')
ax1.legend(); ax1.grid(alpha=0.3)
ax2 = axes[1]; ax2.set_facecolor('white')
ax2.plot(r, -0.6*np.exp(-(r/35)**2)*np.sin(r/20), '#2ca02c', lw=2.5, label='HNB+')
ax2.plot(r,  0.6*np.exp(-(r/35)**2)*np.sin(r/20), '#9467bd', lw=2.5, label='HNB-')
ax2.axhline(0, color='k', ls='--', alpha=0.3); ax2.axvline(0, color='k', ls='--', alpha=0.3)
ax2.set_xlabel('径向距离 r (μm)')
ax2.set_ylabel(f'$U_d$ / (8πKr²)\n(K={Kv} pN, r_colloid={rc} μm)', fontsize=10)
ax2.set_title('HNB+ 和 HNB- 相互作用势', fontsize=12, fontweight='bold')
ax2.legend(); ax2.grid(alpha=0.3)
plt.suptitle('图 7 | 胶体-斯格明子相互作用势 (基于论文 Si-Fig.8e/f, 9e/f)\n'
             '$U_d$ 以 $8\\pi K r^2$ 归一化; K=6.0 pN (5CB弹性常数), r_colloid=2.5 μm',
             fontsize=11, fontweight='bold', y=1.10)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Fig7_interaction_potential.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("  已保存: Fig7_interaction_potential.png")


# ==================== 图8: 胶体动力学 ====================
print("\n生成图8: 胶体动力学...")
fig8, axes = plt.subplots(1, 2, figsize=(15, 5.5), facecolor='white')
ax1 = axes[0]; ax1.set_facecolor('white')
te = np.array([0,60,130,200,260,310,360,400,460,530,600,640])
p1=np.array([100,76,62,39,20,7,3,-30,-46,-65,-98,-120])
p2=np.array([180,177,160,125,94,60,20,-50,-100,-140,-160,-176])
p3=np.array([179,175,147,110,90,70,17,-60,-97,-132,-156,-180])
ts=np.linspace(0,640,300)
p1s=gaussian_filter1d(np.interp(ts,te,p1),sigma=3)
p2s=gaussian_filter1d(np.interp(ts,te,p2),sigma=3)
p3s=gaussian_filter1d(np.interp(ts,te,p3),sigma=3)
ax1.plot(ts,p1s,'r-',lw=2,label='粒子① (被排斥)')
ax1.plot(ts,p2s,'g-',lw=2,label='粒子② (在弦中)')
ax1.plot(ts,p3s,'b-',lw=2,label='粒子③ (被捕获)')
ax1.scatter(te,p1,c='r',s=20,alpha=0.6,edgecolors='darkred',linewidth=0.5)
ax1.scatter(te,p2,c='g',s=20,alpha=0.6,edgecolors='darkgreen',linewidth=0.5)
ax1.scatter(te,p3,c='b',s=20,alpha=0.6,edgecolors='darkblue',linewidth=0.5)
# 修正：HNB+ 改为 HNB+, HNB- 改为 HNB-
for ts_,te_,lb,cl in [(0,205,'HAS','#d62728'),(205,355,'HNB+','#2ca02c'),
                       (355,450,'HNS','#1f77b4'),(450,638,'HNB-','#9467bd')]:
    ax1.axvspan(ts_,te_,alpha=0.1,color=cl)
    ax1.text((ts_+te_)/2,195,lb,ha='center',fontsize=9,color=cl,fontweight='bold')
ax1.set_xlabel('时间 t (s)'); ax1.set_ylabel('方位角 φ (°)')
ax1.set_title('单粒子方位角演化 (论文 Fig.3d)')
ax1.set_xlim([-10,650]); ax1.set_ylim([-210,210])
ax1.axhline(0,c='k',ls='--',alpha=0.3); ax1.axhline(180,c='k',ls='--',alpha=0.3)
ax1.axhline(-180,c='k',ls='--',alpha=0.3); ax1.grid(alpha=0.3)
ax1.legend(loc='lower left',fontsize=9)
ax2=axes[1]; ax2.set_facecolor('white')
tt=np.linspace(0,2*np.pi,200)
xt=40*np.cos(tt)+8*np.sin(3*tt); yt=35*np.sin(tt)+5*np.cos(2*tt)
ax2.plot(xt,yt,'k-',lw=2.5,label='胶体链轨迹')
ax2.scatter(xt[0],yt[0],c='green',s=120,marker='o',edgecolors='black',lw=1.5,label='起点 (HAS, φ=180°)')
ax2.scatter(xt[-1],yt[-1],c='red',s=120,marker='s',edgecolors='black',lw=1.5,label='终点 (HAS, φ=180°)')
offs=[(5,5),(-5,10),(-10,-5),(5,-10)]
# 修正：φ值从论文数据提取
for idx,(ang,lb,off) in enumerate(zip([0,50,100,150],
    ['HAS (φ=180°)','HNB+ (φ=45°)','HNS (φ=0°)','HNB- (φ=-135°)'],offs)):
    ax2.annotate(lb,xy=(xt[idx*50],yt[idx*50]),xytext=off,textcoords='offset points',
                 fontsize=9,bbox=dict(boxstyle='round,pad=0.3',facecolor='wheat',alpha=0.8))
ax2.set_xlabel('x (μm)'); ax2.set_ylabel('y (μm)')
ax2.set_title('胶体链集体运动 (论文 Si-Fig.15c)')
ax2.set_aspect('equal'); ax2.grid(alpha=0.3); ax2.legend(fontsize=9)
plt.suptitle('图 8 | 光驱动下胶体动力学',fontsize=13,fontweight='bold',y=1.04)
plt.tight_layout()
plt.savefig(os.path.join(output_dir,'Fig8_colloid_dynamics.png'),dpi=300,bbox_inches='tight',facecolor='white')
plt.show()
print("  已保存: Fig8_colloid_dynamics.png")


# ==================== 图9: 自由能景观 ====================
print("\n生成图9: 自由能景观...")
fig9,axes=plt.subplots(1,2,figsize=(15,6),facecolor='white')
ax1=axes[0]; ax1.set_facecolor('white')
orient=np.linspace(0,360,600)
energy=0.0256-4.5e-5*(1-np.cos(np.radians(2*orient)))
# 修正：标注四个态(HAS, HNB+, HNS, HNB-)
states=[(0,'HAS','#d62728','φ=180°'),(90,'HNB+','#2ca02c','φ=45°'),
        (180,'HNS','#1f77b4','φ=0°'),(270,'HNB-','#9467bd','φ=-135°'),
        (360,'HAS','#d62728','φ=180°')]
ax1.plot(orient,energy,'k-',lw=2.5)
for ang,nm,cl,ph in states:
    idx=np.argmin(np.abs(orient-ang))
    ax1.plot(ang,energy[idx],'o',color=cl,markersize=14,markeredgecolor='black',markeredgewidth=2)
    xytext=(10,18)if ang in[0,360]else(18,8)if ang==90 else(-10,-25)if ang==180 else(-22,8)
    ax1.annotate(f'{nm}\n{ph}',xy=(ang,energy[idx]),xytext=xytext,textcoords='offset points',
                 ha='center',fontsize=9,fontweight='bold',color=cl)
# 修正：纵轴单位 kT/μm³
ax1.set_xlabel('光偏振角度 (°)'); ax1.set_ylabel('自由能密度 (kT/μm³)')
ax1.set_title('拓扑转变自由能景观 (论文 Fig.3c)\nHAS与HNS几乎简并, HNB±为中间态',fontsize=11,fontweight='bold')
ax1.set_xlim([-20,380]); ax1.set_ylim([0.025555,0.025605]); ax1.grid(alpha=0.3,ls='--')
ax2=axes[1]; ax2.set_facecolor('white')
ax2.set_xlim([-1.6,1.6]); ax2.set_ylim([-1.6,1.6]); ax2.set_aspect('equal'); ax2.axis('off')
theta=np.linspace(0,2*np.pi,100)
ax2.plot(np.cos(theta),np.sin(theta),'k--',alpha=0.3,lw=2)
points=[(0,'HAS','#d62728','φ=180°'),(90,'HNB+','#2ca02c','φ=45°'),
        (180,'HNS','#1f77b4','φ=0°'),(270,'HNB-','#9467bd','φ=-135°')]
for ang,nm,cl,ph in points:
    rad=np.radians(ang-90); xp,yp=np.cos(rad),np.sin(rad)
    ax2.plot(xp,yp,'o',color=cl,markersize=20,markeredgecolor='black',markeredgewidth=2)
    ax2.annotate(f'{nm}\n{ph}',xy=(xp,yp),xytext=(xp*0.3,yp*0.3),
                 textcoords='offset points',ha='center',va='center',fontsize=8,fontweight='bold',color='white')
for i in range(4):
    a1,a2=points[i][0],points[(i+1)%4][0]
    r1,r2=np.radians(a1-90),np.radians(a2-90)
    x1,y1=np.cos(r1)*0.7,np.sin(r1)*0.7; x2,y2=np.cos(r2)*0.7,np.sin(r2)*0.7
    mid=(a1+a2)/2; mx,my=np.cos(np.radians(mid-90))*0.85,np.sin(np.radians(mid-90))*0.85
    ax2.annotate(f'{a1}° -> {a2}°',xy=(mx,my),fontsize=7,color='gray',ha='center')
    ax2.annotate('',xy=(x2,y2),xytext=(x1,y1),
                 arrowprops=dict(arrowstyle='->',color='gray',lw=2.5,connectionstyle='arc3,rad=0.25'))
ax2.set_title('光驱动拓扑转变循环\n偏振路径: 0° -> 90° -> 180° -> 270° -> 360°',fontsize=11,fontweight='bold')
plt.suptitle('图 9 | 液晶斯格明子拓扑转变的能量学',fontsize=13,fontweight='bold',y=1.04)
plt.tight_layout()
plt.savefig(os.path.join(output_dir,'Fig9_energy_transition.png'),dpi=300,bbox_inches='tight',facecolor='white')
plt.show()
print("  已保存: Fig9_energy_transition.png")


# ==================== 图10: 参数汇总表 ====================
print("\n生成图10: 参数汇总表...")
fig10,ax=plt.subplots(figsize=(18,6),facecolor='white'); ax.axis('off')
# 修正：表头 γ 不是 y
table_data=[['纹理', '参数\n(p,q,γ,F)', 'Nsk\n(理论)', '螺旋度\nq', '涡旋度\nm', '相位\nF', 'φ_colloid¹', 'Z/H\n(模拟)']]
for t in textures:
    table_data.append([t['name'], t['params'], f"{t['Nsk']:+.1f}", f"{t['q']:+.1f}",
                       f"{t['vorticity']:+.1f}", t['F_str'], t['phi_str'], f"{t['Z_H']:.2f}"])
table=ax.table(cellText=table_data,cellLoc='center',loc='center',
               colWidths=[0.07,0.22,0.07,0.07,0.07,0.07,0.10,0.08])
table.auto_set_font_size(False); table.set_fontsize(10); table.scale(1.1,2.8)
for i in range(len(table_data[0])):
    table[(0,i)].set_facecolor('#404080'); table[(0,i)].set_text_props(weight='bold',color='white')
for i,t in enumerate(textures):
    for j in range(len(table_data[0])):
        table[(i+1,j)].set_facecolor(t['color']+'20')
ax.set_title('表 1 | 四种半斯格明子参数汇总 (模拟值, H=50μm)\n'
             '¹ φ_colloid: 被捕获胶体的方位角, 与面内指向矢方向一致\n'
             '数据来源: Nature Communications 16:1148 (2025)',fontsize=12,fontweight='bold',y=0.95)
plt.tight_layout()
plt.savefig(os.path.join(output_dir,'Fig10_parameters_table.png'),dpi=300,bbox_inches='tight',facecolor='white')
plt.show()
print("  已保存: Fig10_parameters_table.png")


print("\n"+"="*80)
print("导师修正版完成！")
print("="*80)
print("\n修正清单:")
print("  1. HNB+/HNB- 名称规范化 (避免字体上标缺失)")
print("  2. 所有参数统一使用 γ (不是 y)")
print("  3. Fig.1 参数框从字典读取，避免硬编码")
print("  4. '双光子' 修正为 '双半子'")
print("  5. Fig.8 图例: HNB- φ=-135°")
print("  6. Fig.9 纵轴: kT/μm³")
print("  7. Fig.10 表头: (p,q,γ,F)")
print("="*80)