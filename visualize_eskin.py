import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np

# === CSV読み込み ===
file_path = "eskin_61_R1_49_7_TL_s3.csv"
df = pd.read_csv(file_path, skiprows=7)

# === 骨格構造（joint名はCSVの列と一致）===
bones = [
    # 頭部・胴体
    # ('Head_q_gs', 'Neck_g'),
    ('Neck_g', 'C7'),
    ('C7', 'T2'),
    ('T2', 'Sternum_g'),
    ('Sternum_g', 'L5'),
    ('L5', 'Pelvis_g'),  # PelvisCenter → Pelvis_g に修正

    # 左腕
    ('Neck_g', 'LeftShoulder_g'),
    ('LeftShoulder_g', 'LeftUpperArm_g'),
    ('LeftUpperArm_g', 'LUA'),
    ('LUA', 'LeftForearm_g'),
    ('LeftForearm_g', 'LHME'),
    ('LHME', 'LHM2'),

    # 右腕
    ('Neck_g', 'RightShoulder_g'),
    ('RightShoulder_g', 'RightUpperArm_g'),
    ('RightUpperArm_g', 'RUA'),
    ('RUA', 'RightForearm_g'),
    ('RightForearm_g', 'RHME'),
    ('RHME', 'RHM2'),

    # 左脚
    ('Pelvis_g', 'LeftHip_g'),
    ('LeftHip_g', 'LeftUpperLeg_g'),
    ('LeftUpperLeg_g', 'LeftLowerLeg_g'),
    ('LeftLowerLeg_g', 'LeftKnee_g'),
    ('LeftKnee_g', 'LMM'),
    ('LMM', 'LeftAnkle_g'),
    ('LeftAnkle_g', 'LCA'),

    # 右脚
    ('Pelvis_g', 'RightHip_g'),
    ('RightHip_g', 'RightUpperLeg_g'),
    ('RightUpperLeg_g', 'RightLowerLeg_g'),
    ('RightLowerLeg_g', 'RightKnee_g'),
    ('RightKnee_g', 'RMM'),
    ('RMM', 'RightAnkle_g'),
    ('RightAnkle_g', 'RCA'),
]

# === 描画 ===
fig = plt.figure(figsize=(10, 9))  # キャンバスを大きく
ax = fig.add_subplot(111, projection='3d')

# === 軸設定（固定） ===
ax.set_xlim(-1.2, 0.8)
ax.set_ylim(-3, 0)

# z軸だけ自動範囲を先に計算
z_vals = []
for j1, j2 in bones:
    try:
        p1 = df[[f"{j1}_z"]].values.flatten()
        p2 = df[[f"{j2}_z"]].values.flatten()
        z_vals.extend(p1)
        z_vals.extend(p2)
    except:
        pass

z_center = (max(z_vals) + min(z_vals)) / 2
span = (max(z_vals) - min(z_vals)) / 2
ax.set_zlim(z_center - span, z_center + span)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.view_init(elev=15, azim=90)

# === 各ラインを初期化 ===
lines = []
for _ in bones:
    line, = ax.plot([], [], [], 'o-', lw=2)
    lines.append(line)

# === アニメーション関数 ===
def update(frame):
    for i, (j1, j2) in enumerate(bones):
        try:
            p1 = df[[f"{j1}_x", f"{j1}_y", f"{j1}_z"]].iloc[frame].values
            p2 = df[[f"{j2}_x", f"{j2}_y", f"{j2}_z"]].iloc[frame].values
            lines[i].set_data([p1[0], p2[0]], [p1[1], p2[1]])
            lines[i].set_3d_properties([p1[2], p2[2]])
        except KeyError:
            lines[i].set_data([], [])
            lines[i].set_3d_properties([])
    return lines

# === アニメーション実行 ===
n_frames = len(df)
# ani = FuncAnimation(fig, update, frames=n_frames, interval=10, blit=True)

# 実測フレーム間隔（ms）を自動で取得
frame_interval_ms = np.mean(np.diff(df['Timestamp'].values)) * 1000

# アニメーション実行（実測スピードで再生）
ani = FuncAnimation(fig, update, frames=n_frames, interval=frame_interval_ms, blit=True)


plt.tight_layout()
plt.show()