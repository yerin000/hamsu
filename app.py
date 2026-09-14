import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Page Config
st.set_page_config(
    page_title="삼각함수 단계별 학습 앱",
    page_icon="📐",
    layout="wide"
)

# 2. Sidebar Navigation (완전히 분리된 4개 모듈)
st.sidebar.title("📐 삼각함수 학습 메뉴")
menu = st.sidebar.radio(
    "학습할 항목을 선택하세요:",
    [
        "1. 단위원과 삼각함수의 개념",
        "2. 사인(Sine) 함수 개형",
        "3. 코사인(Cosine) 함수 개형",
        "4. 탄젠트(Tangent) 함수 개형"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 왼쪽 메뉴에서 원하시는 학습 주제를 클릭하시면 해당 학습 화면만 독립적으로 나타납니다.")


# ==============================================================================
# [모듈 1] 단위원과 삼각함수의 개념
# ==============================================================================
if menu == "1. 단위원과 삼각함수의 개념":
    st.title("1. 단위원으로 배우는 삼각함수 개념")
    st.write("""
    반지름의 길이가 1인 **단위원(Unit Circle)** 상에서 각도 $\\theta$에 따른 삼각함수의 정의를 확인하세요:
    - **$\cos(\\theta)$ (파란색)**: 동경 끝점의 **X좌표**
    - **$\sin(\\theta)$ (빨간색)**: 동경 끝점의 **Y좌표**
    - **$\\tan(\\theta)$ (초록색)**: 접선 $X=1$ 과 만나는 **Y 높이**
    """)

    # 조작 파라미터
    col_input, col_metric = st.columns([2, 3])
    with col_input:
        angle_deg = st.slider("각도 θ (도, Degree)", 0, 360, 45, step=5)
        angle_rad = np.radians(angle_deg)

    cos_val = np.cos(angle_rad)
    sin_val = np.sin(angle_rad)
    tan_val = np.tan(angle_rad) if abs(np.cos(angle_rad)) > 1e-5 else np.nan

    with col_metric:
        c1, c2, c3 = st.columns(3)
        c1.metric("Cos (X좌표)", f"{cos_val:.3f}")
        c2.metric("Sin (Y좌표)", f"{sin_val:.3f}")
        c3.metric("Tan (접선높이)", f"{tan_val:.3f}" if not np.isnan(tan_val) else "무한대")

    # 서브플롯 생성 (왼쪽: 단위원 / 오른쪽: 사인파 매핑)
    fig1 = make_subplots(
        rows=1, cols=2,
        subplot_titles=("단위원 (Unit Circle)", "Sin 파형 실시간 매핑"),
        column_widths=[0.45, 0.55]
    )

    # 단위원 배경
    theta_full = np.linspace(0, 2 * np.pi, 300)
    fig1.add_trace(go.Scatter(x=np.cos(theta_full), y=np.sin(theta_full), mode='lines', name='단위원', line=dict(color='gray', dash='dot')), row=1, col=1)
    
    # 동경 & 성분
    fig1.add_trace(go.Scatter(x=[0, cos_val], y=[0, sin_val], mode='lines+markers', name='동경 (r=1)', line=dict(color='purple', width=3)), row=1, col=1)
    fig1.add_trace(go.Scatter(x=[0, cos_val], y=[0, 0], mode='lines', name='Cos (X축)', line=dict(color='blue', width=4)), row=1, col=1)
    fig1.add_trace(go.Scatter(x=[cos_val, cos_val], y=[0, sin_val], mode='lines', name='Sin (Y축)', line=dict(color='red', width=4)), row=1, col=1)

    if not np.isnan(tan_val) and abs(tan_val) <= 3:
        fig1.add_trace(go.Scatter(x=[1, 1], y=[0, tan_val], mode='lines', name='Tan (접선)', line=dict(color='green', width=4)), row=1, col=1)
        fig1.add_trace(go.Scatter(x=[0, 1], y=[0, tan_val], mode='lines', showlegend=False, line=dict(color='green', dash='dot')), row=1, col=1)

    # 우측 파형 매핑
    x_deg_arr = np.linspace(0, 360, 360)
    y_sin_full = np.sin(np.radians(x_deg_arr))
    fig1.add_trace(go.Scatter(x=x_deg_arr, y=y_sin_full, mode='lines', name='Sin 파형', line=dict(color='red')), row=1, col=2)
    fig1.add_trace(go.Scatter(x=[angle_deg], y=[sin_val], mode='markers', name='현재 Y점', marker=dict(color='red', size=10)), row=1, col=2)
    fig1.add_vline(x=angle_deg, line_width=1, line_dash="dash", line_color="gray", row=1, col=2)

    # 레이아웃
    fig1.update_xaxes(range=[-1.5, 1.5], zeroline=True, zerolinecolor='black', row=1, col=1)
    fig1.update_yaxes(range=[-1.5, 1.5], zeroline=True, zerolinecolor='black', scaleanchor="x", scaleratio=1, row=1, col=1)
    fig1.update_xaxes(title_text="각도 (°)", range=[0, 360], dtick=90, zeroline=True, row=1, col=2)
    fig1.update_yaxes(title_text="값", range=[-2, 2], zeroline=True, row=1, col=2)
    fig1.update_layout(height=520, margin=dict(l=20, r=20, t=40, b=20))

    st.plotly_chart(fig1, use_container_width=True)


# ==============================================================================
# [모듈 2] 사인(Sine) 함수 개형
# ==============================================================================
elif menu == "2. 사인(Sine) 함수 개형":
    st.title("2. 사인(Sine) 함수 개형 및 변수 조절")
    st.latex(r"y = A \cdot \sin(B(x - C)) + D")

    col_ctrl, col_graph = st.columns([1, 2.5])

    with col_ctrl:
        st.subheader("🎛️ 사인 함수 파라미터")
        A = st.slider("진폭 / 수직폭 (A)", 0.1, 5.0, 1.0, step=0.1, key="sin_A")
        B = st.slider("주기 계수 (B)", 0.1, 4.0, 1.0, step=0.1, key="sin_B")
        C_deg = st.slider("평행이동 / 위상 (C, °)", -180, 180, 0, step=15, key="sin_C")
        D = st.slider("Y축 이동 (D)", -3.0, 3.0, 0.0, step=0.5, key="sin_D")

        period = 360 / B
        st.markdown("---")
        st.subheader("📊 함수 정보")
        st.write(f"- **현재 수식**: $y = {A:.1f}\\sin({B:.1f}(x - {C_deg}^\circ)) + {D:.1f}$")
        st.write(f"- **주기 (Period)**: **{period:.1f}°** ($360^\circ / {B:.1f}$)")
        st.write(f"- **최댓값**: **{A + D:.1f}**")
        st.write(f"- **최솟값**: **{-A + D:.1f}**")

    with col_graph:
        x_deg = np.linspace(-360, 720, 1080)
        y_user = A * np.sin(B * np.radians(x_deg - C_deg)) + D
        y_base = np.sin(np.radians(x_deg))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_deg, y=y_user, mode='lines', name='변형된 Sin', line=dict(color='red', width=3)))
        fig.add_trace(go.Scatter(x=x_deg, y=y_base, mode='lines', name='기본 Sin (비교용)', opacity=0.4, line=dict(color='gray', dash='dash')))

        fig.update_layout(
            title="사인 함수 개형 변화",
            xaxis_title="각도 (°)", yaxis_title="Y 값",
            xaxis=dict(range=[-360, 720], dtick=180, zeroline=True),
            yaxis=dict(range=[-6, 6], zeroline=True),
            height=550, margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# [모듈 3] 코사인(Cosine) 함수 개형
# ==============================================================================
elif menu == "3. 코사인(Cosine) 함수 개형":
    st.title("3. 코사인(Cosine) 함수 개형 및 변수 조절")
    st.latex(r"y = A \cdot \cos(B(x - C)) + D")

    col_ctrl, col_graph = st.columns([1, 2.5])

    with col_ctrl:
        st.subheader("🎛️ 코사인 함수 파라미터")
        A = st.slider("진폭 / 수직폭 (A)", 0.1, 5.0, 1.0, step=0.1, key="cos_A")
        B = st.slider("주기 계수 (B)", 0.1, 4.0, 1.0, step=0.1, key="cos_B")
        C_deg = st.slider("평행이동 / 위상 (C, °)", -180, 180, 0, step=15, key="cos_C")
        D = st.slider("Y축 이동 (D)", -3.0, 3.0, 0.0, step=0.5, key="cos_D")

        period = 360 / B
        st.markdown("---")
        st.subheader("📊 함수 정보")
        st.write(f"- **현재 수식**: $y = {A:.1f}\\cos({B:.1f}(x - {C_deg}^\circ)) + {D:.1f}$")
        st.write(f"- **주기 (Period)**: **{period:.1f}°** ($360^\circ / {B:.1f}$)")
        st.write(f"- **최댓값**: **{A + D:.1f}**")
        st.write(f"- **최솟값**: **{-A + D:.1f}**")

    with col_graph:
        x_deg = np.linspace(-360, 720, 1080)
        y_user = A * np.cos(B * np.radians(x_deg - C_deg)) + D
        y_base = np.cos(np.radians(x_deg))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_deg, y=y_user, mode='lines', name='변형된 Cos', line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=x_deg, y=y_base, mode='lines', name='기본 Cos (비교용)', opacity=0.4, line=dict(color='gray', dash='dash')))

        fig.update_layout(
            title="코사인 함수 개형 변화",
            xaxis_title="각도 (°)", yaxis_title="Y 값",
            xaxis=dict(range=[-360, 720], dtick=180, zeroline=True),
            yaxis=dict(range=[-6, 6], zeroline=True),
            height=550, margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# [모듈 4] 탄젠트(Tangent) 함수 개형
# ==============================================================================
elif menu == "4. 탄젠트(Tangent) 함수 개형":
    st.title("4. 탄젠트(Tangent) 함수 개형 및 변수 조절")
    st.latex(r"y = A \cdot \tan(B(x - C)) + D")

    col_ctrl, col_graph = st.columns([1, 2.5])

    with col_ctrl:
        st.subheader("🎛️ 탄젠트 함수 파라미터")
        A = st.slider("수직 기울기 / 폭 (A)", 0.1, 5.0, 1.0, step=0.1, key="tan_A")
        B = st.slider("주기 계수 (B)", 0.1, 4.0, 1.0, step=0.1, key="tan_B")
        C_deg = st.slider("평행이동 / 위상 (C, °)", -180, 180, 0, step=15, key="tan_C")
        D = st.slider("Y축 이동 (D)", -3.0, 3.0, 0.0, step=0.5, key="tan_D")

        period = 180 / B
        st.markdown("---")
        st.subheader("📊 함수 정보")
        st.write(f"- **현재 수식**: $y = {A:.1f}\\tan({B:.1f}(x - {C_deg}^\circ)) + {D:.1f}$")
        st.write(f"- **주기 (Period)**: **{period:.1f}°** ($180^\circ / {B:.1f}$)")
        st.write("- **최대/최솟값**: 없음 (무한대)")

    with col_graph:
        x_deg = np.linspace(-360, 720, 2000)
        tan_inner = B * np.radians(x_deg - C_deg)
        
        # 점근선 인근에서 값이 튀는 것을 방지하기 위해 값 제한
        y_user = A * np.tan(tan_inner) + D
        y_user[np.abs(np.tan(tan_inner)) > 10] = np.nan

        y_base = np.tan(np.radians(x_deg))
        y_base[np.abs(y_base) > 10] = np.nan

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_deg, y=y_user, mode='lines', name='변형된 Tan', line=dict(color='green', width=3)))
        fig.add_trace(go.Scatter(x=x_deg, y=y_base, mode='lines', name='기본 Tan (비교용)', opacity=0.4, line=dict(color='gray', dash='dash')))

        fig.update_layout(
            title="탄젠트 함수 개형 변화",
            xaxis_title="각도 (°)", yaxis_title="Y 값",
            xaxis=dict(range=[-360, 720], dtick=180, zeroline=True),
            yaxis=dict(range=[-6, 6], zeroline=True),
            height=550, margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
