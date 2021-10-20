# Superposition of 3D waves
import tkinter
from matplotlib import cm
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np


def change_k(value):
    global k
    k = float(value)


def change_o(value):
    global omega
    omega = float(value)


def change_num(value):
    global num
    num = value


def set_axis():
    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(y_min, y_max)
    ax1.set_zlim(z_min, z_max)
    ax1.set_title('Waves')
    ax1.set_xlabel('x * pi')
    ax1.set_ylabel('y * pi')
    ax1.set_zlabel('z')
    ax1.grid()

    ax2.set_xlim(x_min, x_max)
    ax2.set_ylim(y_min, y_max)
    ax2.set_zlim(z_min * num, z_max * num)
    ax2.set_title('Superposed wave')
    ax2.set_xlabel('x * pi')
    ax2.set_ylabel('y * pi')
    ax2.set_zlabel('z')
    ax2.grid()


def update(f):
    ax1.cla()  # Clear ax
    ax2.cla()  # Clear ax
    set_axis()

    global zz, zz_superposed
    ax1.text(x_min, y_min, z_max * 1.4, "Step(as t)=" + str(f))
    ax1.text(x_min, y_min, z_max * 1.2, "Number of waves=" + str(num))
    ax1.text(x_min, y_min, z_max * 1.0, "k=" + str(f'{k:.1f}') + ", omega=" + str(f'{omega:.2f}'))

    theta_step = 2 * np.pi / num  # Increase/decrease of theta in 1 step
    # Draw waves and a superposed waves
    zz_superposed = xx * 0. + yy * 0.
    for i in range(num):
        theta0to2pi_n = (i * theta_step) % (2 * np.pi)
        zz = np.sin((k * np.sqrt(xx ** 2 + yy ** 2) * np.cos(np.arctan2(yy, xx) - theta0to2pi_n) - omega * f) * np.pi)
        ax1.plot_surface(xx, yy, zz, rstride=1, cstride=1, cmap=cm.coolwarm, alpha=0.2)
        zz_superposed = zz_superposed + zz
    ax2.plot_surface(xx, yy, zz_superposed, rstride=1, cstride=1, cmap=cm.coolwarm, alpha=0.6)


# Global variables
min_max = 2.
x_min = -min_max
x_max = min_max
y_min = -min_max
y_max = min_max
z_min = -4.
z_max = 4.

# Parameter of waves
num = 1     # Num of waves

k = 1.     # Wave number
k_min = 0.
k_max = 20.
k_step = 1.

omega = 0.1
omega_min = -0.25
omega_max = 0.25
omega_step = 0.01

# Generate arrange
x = y = np.arange(x_min, x_max, 0.1)
xx, yy = np.meshgrid(x, y)
zz = xx * 0. + yy * 0.
zz_superposed = zz

# Generate tkinter
root = tkinter.Tk()
root.title("Superposed wave")

# Generate figure and axes
fig = Figure(figsize=(10, 6))
ax1 = fig.add_subplot(121, projection='3d')
ax1.set_box_aspect((1, 1, 1))
ax2 = fig.add_subplot(122, projection='3d')
ax2.set_box_aspect((1, 1, 1))

# Embed a figure in canvas
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack()

# Animation
anim = animation.FuncAnimation(fig, update, interval=100)

# Toolbar
toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

# Label and spinbox for k
label_k = tkinter.Label(root, text="k1")
label_k.pack(side='left')
var_k = tkinter.StringVar(root)  # variable for spinbox-value
var_k.set(k)  # Initial value
s_k = tkinter.Spinbox(
    root, textvariable=var_k, format="%.1f", from_=k_min, to=k_max, increment=k_step,
    command=lambda: change_k(var_k.get()), width=5
    )
s_k.pack(side='left')
# Label and spinbox for omega
label_o = tkinter.Label(root, text="omega1")
label_o.pack(side='left')
var_o = tkinter.StringVar(root)  # variable for spinbox-value
var_o.set(omega)  # Initial value
s_o = tkinter.Spinbox(
    root, textvariable=var_o, format="%.2f", from_=omega_min, to=omega_max,
    increment=omega_step, command=lambda: change_o(var_o.get()), width=5
    )
s_o.pack(side='left')
# Label and spinbox for num of waves
label_n = tkinter.Label(root, text="Number of waves")
label_n.pack(side='left')
var_n = tkinter.IntVar(root)  # variable for spinbox-value
var_n.set(num)  # Initial value
s_n = tkinter.Spinbox(
    root, textvariable=var_n, from_=0, to=20, increment=1,
    command=lambda: change_num(var_n.get()), width=5
    )
s_n.pack(side='left')

# main loop
set_axis()
tkinter.mainloop()
