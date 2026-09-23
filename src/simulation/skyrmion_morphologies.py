import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patches

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 8
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.dpi'] = 300

class SkyrmionMorphologies:
    def __init__(self, grid_size=200, box_length=200):
        self.grid_size = grid_size
        self.box_length = box_length
        self.x = np.linspace(-box_length/2, box_length/2, grid_size)
        self.y = np.linspace(-box_length/2, box_length/2, grid_size)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.r = np.sqrt(self.X**2 + self.Y**2)
        self.theta = np.arctan2(self.Y, self.X)

    def generate_half_anti_skyrmion(self):
        n_x = np.cos(self.theta / 2)
        n_y = -np.sin(self.theta / 2)
        n_z = np.zeros_like(self.X)
        mask = self.Y < 0
        return n_x*mask, n_y*mask, n_z*mask

    def generate_half_neel_skyrmion(self):
        n_x = np.cos(self.theta / 2)
        n_y = np.sin(self.theta / 2)
        n_z = np.zeros_like(self.X)
        mask = self.Y < 0
        return n_x*mask, n_y*mask, n_z*mask

    def generate_half_neel_bimeron_1(self):
        n_x = np.cos(self.theta / 2 + np.pi/4)
        n_y = np.sin(self.theta / 2 + np.pi/4)
        n_z = np.zeros_like(self.X)
        mask = self.X < 0
        return n_x*mask, n_y*mask, n_z*mask

    def generate_half_neel_bimeron_2(self):
        n_x = np.cos(self.theta / 2 - np.pi/4)
        n_y = np.sin(self.theta / 2 - np.pi/4)
        n_z = np.zeros_like(self.X)
        mask = self.X < 0
        return n_x*mask, n_y*mask, n_z*mask

    def plot_vector_field(self, ax, n_x, n_y, title, is_zoom=False):
        step = 4
        if is_zoom:
            s = self.grid_size
            x_samp = self.X[s//4 : 3*s//4, s//4 : 3*s//4]
            y_samp = self.Y[s//4 : 3*s//4, s//4 : 3*s//4]
            nx_samp = n_x[s//4 : 3*s//4, s//4 : 3*s//4]
            ny_samp = n_y[s//4 : 3*s//4, s//4 : 3*s//4]
            extent = [-50, 50, -50, 50]
        else:
            x_samp = self.X
            y_samp = self.Y
            nx_samp = n_x
            ny_samp = n_y
            extent = [-100, 100, -100, 100]

        ax.quiver(x_samp[::step, ::step], y_samp[::step, ::step],
                  nx_samp[::step, ::step], ny_samp[::step, ::step],
                  color='black', alpha=0.6, linewidth=0.3, headwidth=2)

        im = ax.imshow(n_y, cmap='RdBu_r', origin='lower', extent=extent, vmin=-1, vmax=1)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel('x (μm)', fontsize=8)
        ax.set_ylabel('y (μm)', fontsize=8)
        ax.set_aspect('equal')
        ax.tick_params(labelsize=7)
        return im

    def plot_unit_sphere(self, ax, title):
        circle = patches.Circle((0,0), 1, fill=False, linewidth=1)
        ax.add_patch(circle)
        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.4, 1.4)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=8)

    def visualize_all_morphologies(self, save_path="skyrmion_final.png"):
        fig = plt.figure(figsize=(16, 12))
        gs = GridSpec(4, 4, wspace=0.5, hspace=0.6)

        morphs = [
            (self.generate_half_anti_skyrmion, "Half-anti-skyrmion", "(1/2, -1/2, 0, 0)"),
            (self.generate_half_neel_skyrmion, "Half-Néel-skyrmion", "(1/2, 1/2, 0, π)"),
            (self.generate_half_neel_bimeron_1, "Half-Néel-bimeron 1", "(1/2, 0, 0, π/2)"),
            (self.generate_half_neel_bimeron_2, "Half-Néel-bimeron 2", "(1/2, 0, 0, -π/2)"),
        ]

        for i, (gen, name, param) in enumerate(morphs):
            nx, ny, nz = gen()

            ax1 = fig.add_subplot(gs[i, 0])
            im = self.plot_vector_field(ax1, nx, ny, f"{name}\n{param}", is_zoom=False)

            ax2 = fig.add_subplot(gs[i, 1])
            self.plot_unit_sphere(ax2, "Wrapping")

            ax3 = fig.add_subplot(gs[i, 2])
            self.plot_vector_field(ax3, nx, ny, "Magnified view", is_zoom=True)

            ax4 = fig.add_subplot(gs[i, 3])
            self.plot_unit_sphere(ax4, "Magnified")

        cbar_ax = fig.add_axes([0.91, 0.15, 0.015, 0.7])
        fig.colorbar(im, cax=cbar_ax).set_label('n_y', fontsize=8)

        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    sim = SkyrmionMorphologies(grid_size=200)
    sim.visualize_all_morphologies()