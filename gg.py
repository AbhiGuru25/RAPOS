import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np

tz = ZoneInfo("Asia/Kolkata")

def angle_rad(angle, length):
    theta = np.radians(90 - angle)
    return length * np.cos(theta), length * np.sin(theta)

fig, ax = plt.subplots(figsize=(6, 6))

circle = plt.Circle((0, 0), 1, fill=False, linewidth=2)
ax.add_artist(circle)

ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect('equal')
ax.axis('off')

hour_hand, = ax.plot([], [], linewidth=6, color='black')
minute_hand, = ax.plot([], [], linewidth=3, color='blue')
second_hand, = ax.plot([], [], linewidth=1, color='red')

title = ax.set_title("")

def update(frame):
    now = datetime.now(tz)

    hour = now.hour % 12
    minute = now.minute
    second = now.second

    hour_angle = (hour + minute / 60) * 30
    minute_angle = (minute + second / 60) * 6
    second_angle = second * 6

    hx, hy = angle_rad(hour_angle, 0.5)
    mx, my = angle_rad(minute_angle, 0.7)
    sx, sy = angle_rad(second_angle, 0.9)

    hour_hand.set_data([0, hx], [0, hy])
    minute_hand.set_data([0, mx], [0, my])
    second_hand.set_data([0, sx], [0, sy])

    title.set_text(f"Analog Clock - IST ({now.strftime('%H:%M:%S')})")

ani = FuncAnimation(fig, update, interval=1000)

plt.show()