import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. 페이지 기본 설정
st.set_page_config(page_title="단위원 기반 삼각함수 시각화", layout="wide")

st.title("📐 단위원으로 배우는 삼각함수 (Sin, Cos, Tan)")
st.write("""
**단위원(반지름이 1인 원)** 상에서 각도 $\\theta$가 변할 때 삼각함수의 값들이 어떻게 결정되는지 확인해 보세요:
- **$\cos(\\theta)$ (코사인)**: 동경 끝점의 **X좌표** (파란색)
- **$\sin(\\theta)$ (사인)**: 동경 끝점의 **Y좌표** (빨간색)
- **$\\tan(\\theta)$ (탄젠트)**: 접선 $X=1$ 과 만나는 **높이** (초록색)
""")

# 2. 사이드바 - 각도 입력
st.sidebar.header("🎛️ 각도 조절")
angle_deg = st.sidebar.slider("각도 θ (도, Degree)", 0, 360, 45, step=5)
angle_rad = np.radians(angle_deg)

# 삼각함수 값 계산
cos_val = np.cos(angle_rad)
sin_val = np.sin(angle_rad)
tan_val = np.tan(angle_rad) if abs(np.cos(angle_rad)) > 1e-5 else np.nan

# 정보 표시
col_info1, col_info2, col_info3 = st.columns(3)
col_info1.metric("Cos (X좌표)", f"{cos_val:.3f}")
col_info2.metric("Sin (Y좌표)", f"{sin_val:.3f}")
col_info3.metric("Tan (높이)", f"{tan_val:.3f}" if not np.isnan(tan_val) else "무한대 (Undefined)")

# 3. 서브플롯 생성 (1행 2열: 왼쪽 단위원, 오른쪽 그래프)
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("1. 단위원 (Unit Circle)", "2. 삼각함수 그래프"),
    column_widths=[0.45, 0.55]
)

# -------------------------------------------------------------
# [왼쪽] 단위원 시각화
# -------------------------------------------------------------
# 단위원 (원) 데이터
theta_full = np.linspace(0, 2*np.pi, 300)
circle_x = np.cos(theta_full)
circle_y = np.sin(theta_full)

# 1) 단위원 배경
fig.add_trace(
    go.Scatter(x=circle_x, y=circle_y, mode='lines', name='단위원', line=dict(color='gray', dash='dot')),
    row=1, col=1
)

# 2) 동경 (원점에서 해당 점까지의 선)
fig.add_trace(
    go.Scatter(x=[0, cos_val], y=[0, sin_val], mode='lines+markers', name='동경 (r=1)', line=dict(color='purple', width=3)),
    row=1, col=1
)

# 3) Cos (X축 성분 선)
fig.add_trace(
    go.Scatter(x=[0, cos_val], y=[0, 0], mode='lines', name='Cos (X축)', line=dict(color='blue', width=4)),
    row=1, col=1
)

# 4) Sin (Y축 성분 선)
fig.add_trace(
    go.Scatter(x=[cos_val, cos_val], y=[0, sin_val], mode='lines', name='Sin (Y축)', line=dict(color='red', width=4)),
    row=1, col=1
)

# 5) Tan (접선 x=1 상에서의 높이)
if not np.isnan(tan_val) and abs(tan_val) <= 3:
    fig.add_trace(
        go.Scatter(x=[1, 1], y=[0, tan_val], mode='lines', name='Tan (접선)', line=dict(color='green', width=4)),
        row=1, col=1
    )
    # 동경 연장선 (원점에서 접점까지)
    fig.add_trace(
        go.Scatter(x=[0, 1], y=[0, tan_val], mode='lines', showlegend=False, line=dict(color='green', dash='dot')),
        row=1, col=1
    )

# -------------------------------------------------------------
# [오른쪽] 삼각함수 그래프 시각화
# -------------------------------------------------------------
x_deg = np.linspace(0, 360, 360)
x_rad_arr = np.radians(x_deg)

y_sin = np.sin(x_rad_arr)
y_cos = np.cos(x_rad_arr)
y_tan = np.tan(x_rad_arr)
y_tan[np.abs(y_tan) > 5] = np.nan  # 점근선 부근 값 제한

# 전체 함수 곡선
fig.add_trace(go.Scatter(x=x_deg, y=y_sin, mode='lines', name='Sin 함수', line=dict(color='red')), row=1, col=2)
fig.add_trace(go.Scatter(x=x_deg, y=y_cos, mode='lines', name='Cos 함수', line=dict(color='blue')), row=1, col=2)
fig.add_trace(go.Scatter(x=x_deg, y=y_tan, mode='lines', name='Tan 함수', line=dict(color='green')), row=1, col=2)

# 현재 각도에서의 위치 점 표시
fig.add_trace(go.Scatter(x=[angle_deg], y=[sin_val], mode='markers', name='현재 Sin 점', marker=dict(color='red', size=10)), row=1, col=2)
fig.add_trace(go.Scatter(x=[angle_deg], y=[cos_val], mode='markers', name='현재 Cos 점', marker=dict(color='blue', size=10)), row=1, col=2)
if not np.isnan(tan_val) and abs(tan_val) <= 5:
    fig.add_trace(go.Scatter(x=[angle_deg], y=[tan_val], mode='markers', name='현재 Tan 점', marker=dict(color='green', size=10)), row=1, col=2)

# 현재 선택된 각도를 세로선으로 표시
fig.add_vline(x=angle_deg, line_width=1, line_dash="dash", line_color="gray", row=1, col=2)

# -------------------------------------------------------------
# Layout 및 축 설정
# -------------------------------------------------------------
# 1. 단위원 비율을 1:1로 맞추어 원이 일그러지지 않도록 설정
fig.update_xaxes(range=[-1.5, 1.5], zeroline=True, zerolinecolor='black', row=1, col=1)
fig.update_yaxes(range=[-1.5, 1.5], zeroline=True, zerolinecolor='black', scaleanchor="x", scaleratio=1, row=1, col=1)

# 2. 오른쪽 그래프 축 설정
fig.update_xaxes(title_text="각도 (Degree)", range=[0, 360], dtick=90, zeroline=True, row=1, col=2)
fig.update_yaxes(title_text="값 (Value)", range=[-3, 3], zeroline=True, row=1, col=2)

fig.update_layout(
    height=550,
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
)

# Streamlit 앱 출력
st.plotly_chart(fig, use_container_width=True)
