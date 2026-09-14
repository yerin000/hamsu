import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Streamlit 페이지 설정
st.set_page_config(page_title="함수 그래프 맞추기 게임", layout="wide")

st.title("🎯 목표 함수 그래프 맞추기")
st.write("목표 그래프(빨간색 점선)와 일치하도록 아래 슬라이더를 조작해 보세요!")

# Sidebar - 컨트롤러
st.sidebar.header("🎛️ 파라미터 조작")
amplitude = st.sidebar.slider("진폭 (Amplitude)", 0.5, 3.0, 1.0, 0.1)
frequency = st.sidebar.slider("주기/주파수 (Frequency)", 0.5, 3.0, 1.0, 0.1)
phase = st.sidebar.slider("위상 이동 (Phase Shift)", -180, 180, 0, 10)

# 데이터 생성
x_g_deg = np.linspace(0, 360, 500)
x_rad = np.radians(x_g_deg)

# 목표 함수 (예: 2 * sin(1.5 * x + 45deg))
y_target = 2.0 * np.sin(1.5 * x_rad + np.radians(45))

# 사용자 예측 함수
y_user = amplitude * np.sin(frequency * x_rad + np.radians(phase))

# Plotly 그래프 생성
fig_game = go.Figure()

# 1. 목표 그래프 (수정된 코드: opacity를 line 밖으로 이동)
fig_game.add_trace(go.Scatter(
    x=x_g_deg, 
    y=y_target, 
    mode='lines', 
    name='🎯 목표 그래프', 
    opacity=0.6,
    line=dict(color='red', width=5, dash='dash')
))

# 2. 사용자 그래프
fig_game.add_trace(go.Scatter(
    x=x_g_deg, 
    y=y_user, 
    mode='lines', 
    name='✏️ 내 그래프', 
    line=dict(color='blue', width=3)
))

# 그래프 레이아웃 설정
fig_game.update_layout(
    title="사인(Sine) 파형 맞추기",
    xaxis_title="각도 (Degree)",
    yaxis_title="진폭 (Y)",
    yaxis=dict(range=[-3.5, 3.5]),
    legend=dict(x=0.01, y=0.99),
    margin=dict(l=20, r=20, t=40, b=20)
)

# Streamlit에 Plotly 그래프 출력
st.plotly_chart(fig_game, use_container_width=True)

# 일치도 확인 로직 (오차 계산)
error = np.mean(np.abs(y_target - y_user))
if error < 0.05:
    st.balloons()
    st.success("🎉 정답입니다! 목표 그래프와 일치합니다!")
else:
    st.info(f"💡 정답과의 평균 오차: {error:.3f}")
