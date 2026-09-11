import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

# -----------------------------------------------------------------------------
# 페이지 기본 설정
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="한눈에 이해하는 삼각함수 놀이터 📐",
    page_icon="🌊",
    layout="wide"
)

# 세션 상태 초기화 (게임 모드용)
if 'target_a' not in st.session_state:
    st.session_state.target_a = random.choice([1.0, 2.0, 3.0])
if 'target_b' not in st.session_state:
    st.session_state.target_b = random.choice([1.0, 2.0])
if 'target_d' not in st.session_state:
    st.session_state.target_d = random.choice([-1.0, 0.0, 1.0, 2.0])

def reset_game():
    st.session_state.target_a = random.choice([1.0, 2.0, 3.0])
    st.session_state.target_b = random.choice([1.0, 2.0])
    st.session_state.target_d = random.choice([-1.0, 0.0, 1.0, 2.0])

# 헤더 타이틀
st.title("🌊 한눈에 이해하는 고교 삼각함수 탐구실")
st.caption("베테랑 개발자가 만든 인터랙티브 시각화로 삼각함수의 원리를 직관적으로 마스터해보세요!")

# 탭 메뉴 구성
tab1, tab2, tab3, tab4 = st.tabs([
    "🎡 1단계: 단위원과 삼각함수의 탄생",
    "🎛️ 2단계: 파동 그래프 변신 ($y=a\\sin(bx)+d$)",
    "🎯 3단계: 파동 맞추기 미니게임",
    "📖 4단계: 핵심 공식 요약노트"
])

# -----------------------------------------------------------------------------
# TAB 1: 단위원과 삼각함수의 탄생
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("🎡 단위원(Unit Circle) 위 점의 움직임이 파동이 됩니다!")
    st.markdown("""
    고등학교 삼각함수의 핵심 비밀: **"반지름이 1인 원 위의 점 $(x, y)$에서 $x$좌표는 코사인($\\cos$), $y$좌표는 사인($\\sin$)입니다!"**  
    아래 슬라이더를 움직여 각도를 바꿔보며, 원 위 점의 $y$높이가 오른쪽 파동 그래프로 연결되는 과정을 관찰해보세요.
    """)
    
    col_input, col_info = st.columns([2, 1])
    with col_input:
        theta_deg = st.slider("각도 $\\theta$ (도/Degree)", 0, 720, 45, step=5)
        func_choice = st.radio("관찰할 삼각함수 선택", ["$\\sin(\\theta)$ (높이 / y좌표)", "$\\cos(\\theta)$ (밑변 / x좌표)"], horizontal=True)
    
    theta_rad = np.radians(theta_deg)
    sin_val = np.sin(theta_rad)
    cos_val = np.cos(theta_rad)
    tan_val = np.tan(theta_rad) if abs(np.cos(theta_rad)) > 1e-5 else "정의되지 않음 (무한대)"

    with col_info:
        st.info(f"""
        **현재 각도 정보**:
        - **각도**: ${theta_deg}^\\circ = {theta_rad/np.pi:.2f}\\pi$ rad
        - **$\\sin(\\theta)$ (y높이)**: `{sin_val:.3f}`
        - **$\\cos(\\theta)$ (x밑변)**: `{cos_val:.3f}`
        - **$\\tan(\\theta)$ (기울기)**: `{tan_val if isinstance(tan_val, str) else f"{tan_val:.3f}"}`
        """)

    # Plotly 시각화 (서브플롯: 단위원 + 그래프)
    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.4, 0.6],
        subplot_titles=("단위원 (Unit Circle)", "삼각함수 그래프 Trace")
    )

    # 1. 단위원 그리기
    circle_angles = np.linspace(0, 2*np.pi, 200)
    fig.add_trace(go.Scatter(x=np.cos(circle_angles), y=np.sin(circle_angles), mode='lines', name='단위원', line=dict(color='lightgray', dash='dash')), row=1, col=1)
    
    # 단위원 x,y 축
    fig.add_shape(type="line", x0=-1.3, y0=0, x1=1.3, y1=0, line=dict(color="gray", width=1), row=1, col=1)
    fig.add_shape(type="line", x0=0, y0=-1.3, x1=0, y1=1.3, line=dict(color="gray", width=1), row=1, col=1)
    
    # 동경 (반지름 선)
    fig.add_trace(go.Scatter(x=[0, cos_val], y=[0, sin_val], mode='lines+markers', name='동경 선분', line=dict(color='orange', width=3)), row=1, col=1)
    
    # 높이/밑변 직각삼각형 표시
    if "sin" in func_choice:
        fig.add_trace(go.Scatter(x=[cos_val, cos_val], y=[0, sin_val], mode='lines', name='y높이 (sin)', line=dict(color='red', width=4)), row=1, col=1)
        fig.add_trace(go.Scatter(x=[cos_val], y=[sin_val], mode='markers', marker=dict(size=12, color='red'), name='현재 점'), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(x=[0, cos_val], y=[0, 0], mode='lines', name='x밑변 (cos)', line=dict(color='blue', width=4)), row=1, col=1)
        fig.add_trace(go.Scatter(x=[cos_val], y=[sin_val], mode='markers', marker=dict(size=12, color='blue'), name='현재 점'), row=1, col=1)

    # 2. 파동 그래프 그리기
    wave_x_deg = np.linspace(0, 720, 500)
    wave_x_rad = np.radians(wave_x_deg)
    
    if "sin" in func_choice:
        wave_y = np.sin(wave_x_rad)
        curr_y = sin_val
        line_color = 'red'
        title_y = "sin(θ)"
    else:
        wave_y = np.cos(wave_x_rad)
        curr_y = cos_val
        line_color = 'blue'
        title_y = "cos(θ)"

    fig.add_trace(go.Scatter(x=wave_x_deg, y=wave_y, mode='lines', name=title_y, line=dict(color='lightgray')), row=1, col=2)
    
    # 현재 각도까지의 궤적 강조
    mask = wave_x_deg <= theta_deg
    fig.add_trace(go.Scatter(x=wave_x_deg[mask], y=wave_y[mask], mode='lines', name='진행 궤적', line=dict(color=line_color, width=3)), row=1, col=2)
    fig.add_trace(go.Scatter(x=[theta_deg], y=[curr_y], mode='markers', marker=dict(size=12, color=line_color), name='현재 값'), row=1, col=2)

    # 축 설정 및 레이아웃 조정
    fig.update_xaxes(title_text="X 좌표", range=[-1.4, 1.4], scaleanchor="y", scaleratio=1, row=1, col=1)
    fig.update_yaxes(title_text="Y 좌표", range=[-1.4, 1.4], row=1, col=1)
    
    fig.update_xaxes(title_text="각도 θ (도)", range=[0, 720], row=1, col=2)
    fig.update_yaxes(title_text="값", range=[-1.4, 1.4], row=1, col=2)
    
    fig.update_layout(height=450, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------------------------------------------------
# TAB 2: 파동 그래프 변신 ($y = a \sin(bx) + d$)
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("🎛️ 삼각함수 그래프 변형 기계: $y = a \\cdot \\sin(b \\cdot x) + d$")
    st.markdown("""
    내신과 수능 단골 문제! **진폭 $a$**, **주기 계수 $b$**, **위아래 이동 $d$**가 그래프의 형태를 어떻게 바꾸는지 실시간으로 실험해보세요.
    """)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        param_a = st.slider("진폭 $a$ (위아래 확대/축소)", 0.5, 4.0, 1.0, step=0.5)
        st.caption(f"최댓값: {param_a}, 최솟값: {-param_a}")
    with c2:
        param_b = st.slider("주기 계수 $b$ (좌우 압축/팽창)", 0.5, 4.0, 1.0, step=0.5)
        period = 360 / param_b
        st.caption(f"주기 $T = \\frac{{360^\\circ}}{{|b|}} = {period:.1f}^\\circ$ ({2/param_b:.2f}$\\pi$ rad)")
    with c3:
        param_d = st.slider("Y축 이동 $d$ (위아래 평행이동)", -3.0, 3.0, 0.0, step=0.5)
        st.caption(f"중심축 위치: $y = {param_d}$")

    x_deg = np.linspace(0, 720, 500)
    x_rad = np.radians(x_deg)
    
    y_base = np.sin(x_rad)
    y_transformed = param_a * np.sin(param_b * x_rad) + param_d

    fig2 = go.Figure()
    # 기준 sin(x) 그래프
    fig2.add_trace(go.Scatter(x=x_deg, y=y_base, mode='lines', name='기본 sin(x)', line=dict(color='gray', dash='dash')))
    # 변형된 그래프
    fig2.add_trace(go.Scatter(x=x_deg, y=y_transformed, mode='lines', name=f'{param_a}sin({param_b}x)+{param_d}', line=dict(color='purple', width=3)))
    
    # 중심선 표시
    fig2.add_shape(type="line", x0=0, y0=param_d, x1=720, y1=param_d, line=dict(color="violet", width=1, dash="dot"))

    fig2.update_layout(
        title=f"현재 완성된 그래프: $y = {param_a} \\sin({param_b}x) + {param_d}$",
        xaxis_title="각도 (도)",
        yaxis_title="y 값",
        yaxis=dict(range=[-7, 7]),
        xaxis=dict(range=[0, 720]),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig2, use_container_width=True)


# -----------------------------------------------------------------------------
# TAB 3: 파동 맞추기 미니게임
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("🎯 타겟 파동 그래프 맞추기 챌린지!")
    st.markdown("랜덤으로 생성된 **빨간색 목표 그래프**에 맞춰 슬라이더를 조작해 **보라색 내 그래프**를 포개어보세요!")
    
    t_a = st.session_state.target_a
    t_b = st.session_state.target_b
    t_d = st.session_state.target_d
    
    gc1, gc2, gc3, gc4 = st.columns([1, 1, 1, 1])
    with gc1:
        user_a = st.slider("내 진폭 $a$", 0.5, 4.0, 1.0, step=0.5, key="game_a")
    with gc2:
        user_b = st.slider("내 주기계수 $b$", 0.5, 4.0, 1.0, step=0.5, key="game_b")
    with gc3:
        user_d = st.slider("내 Y이동 $d$", -3.0, 3.0, 0.0, step=0.5, key="game_d")
    with gc4:
        st.write("### ")
        if st.button("🎲 새로운 문제 도전", use_container_width=True):
            reset_game()
            st.rerun()

    # 그래프 비교
    x_g_deg = np.linspace(0, 720, 400)
    x_g_rad = np.radians(x_g_deg)
    
    y_target = t_a * np.sin(t_b * x_g_rad) + t_d
    y_user = user_a * np.sin(user_b * x_g_rad) + user_d

    fig_game = go.Figure()
    fig_game.add_trace(go.Scatter(x=x_g_deg, y=y_target, mode='lines', name='🎯 목표 그래프', line=dict(color='red', width=5, opacity=0.6)))
    fig_game.add_trace(go.Scatter(x=x_g_deg, y=y_user, mode='lines', name='🔮 내가 만든 그래프', line=dict(color='blue', width=3, dash='dash')))

    fig_game.update_layout(
        xaxis_title="각도 (도)",
        yaxis_title="y 값",
        yaxis=dict(range=[-7, 7]),
        xaxis=dict(range=[0, 720]),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_game, use_container_width=True)

    # 정답 판정
    if user_a == t_a and user_b == t_b and user_d == t_d:
        st.balloons()
        st.success(f"🎉 완벽합니다! 성공입니다! 정답 식: $y = {t_a:g}\\sin({t_b:g}x) + {t_d:g}$")
    else:
        st.info("💡 힌트: 목표 그래프의 **위아래 폭(진폭 $a$)**, **파동의 촘촘한 정도(주기 $b$)**, **위아래 위치($d$)**를 맞춰보세요.")


# -----------------------------------------------------------------------------
# TAB 4: 핵심 공식 요약노트
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("📖 고교 삼각함수 필수 암기 공식 요약노트")
    
    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown("""
        ### 1. 삼각비의 기본 관계
        - **탄젠트 관계식**:
          $$\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}$$
        - **제곱 공식 (피타고라스 정리)**:
          $$\\sin^2\\theta + \\cos^2\\theta = 1$$
        - **호도법과 60분법 변환**:
          $$180^\\circ = \\pi \\text{ rad}$$
          $$\\theta^\\circ = \\theta \\times \\frac{\\pi}{180} \\text{ rad}$$
        """)
    with mc2:
        st.markdown("""
        ### 2. $y = a \\sin(bx + c) + d$ 의 성질
        - **최댓값 (Maximum)**: $|a| + d$
        - **최솟값 (Minimum)**: $-|a| + d$
        - **주기 (Period)**: $T = \\frac{2\\pi}{|b|}$ (도 단위: $\\frac{360^\\circ}{|b|}$)
        - **평행이동**: $x$축 방향으로 $-\\frac{c}{b}$, $y$축 방향으로 $d$만큼 이동
        """)
