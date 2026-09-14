import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Page Config
st.set_page_config(
    page_title="삼각함수 단계별 학습 앱",
    page_icon="📐",
    layout="wide"
)

# 2. Sidebar Navigation
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
st.sidebar.info("💡 왼쪽 메뉴에서 원하시는 학습 주제를 선택할 수 있습니다.")


# ==============================================================================
# [모듈 1] 단위원과 삼각함수의 개념 (단위원 전용)
# ==============================================================================
if menu == "1. 단위원과 삼각함수의 개념":
    st.title("1. 단위원으로 배우는 삼각함수 개념")
    st.write("""
    반지름의 길이가 1인 **단위원(Unit Circle)** 상에서 각도 $\\theta$에 따른 삼각함수의 정의입니다:
    - **$\cos(\\theta)$ (파란색)**: 동경 끝점의 **X좌표** (X축 선)
    - **$\sin(\\theta)$ (빨간색)**: 동경 끝점의 **Y좌표** (Y축 선)
    - **$\\tan(\\theta)$ (초록색)**: 접선 $X=1$ 과 만나는 **Y 높이**
    """)

    # 각도 입력 및 값 계산
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

    # Plotly 단위원 그래프 생성
    fig1 = go.Figure()

    # 1) 단위원 테두리 (원)
    theta_full = np.linspace(0, 2 * np.pi, 300)
    fig1.add_trace(go.Scatter(
        x=np.cos(theta_full), y=np.sin(theta_full), 
        mode='lines', name='단위원 (r=1)', 
        line=dict(color='lightgray', dash='dot', width=2)
    ))

    # 2) 동경 (원점에서 끝점 P까지의 선)
    fig1.add_trace(go.Scatter(
        x=[0, cos_val], y=[0, sin_val], 
        mode='lines+markers', name='동경 (r=1)', 
        line=dict(color='purple', width=3),
        marker=dict(size=8, color='purple')
    ))

    # 3) Cos (X축 좌표 선)
    fig1.add_trace(go.Scatter(
        x=[0, cos_val], y=[0, 0], 
        mode='lines', name='Cos (X축 길이)', 
        line=dict(color='blue', width=5)
    ))

    # 4) Sin (Y축 좌표 선)
    fig1.add_trace(go.Scatter(
        x=[cos_val, cos_val], y=[0, sin_val], 
        mode='lines', name='Sin (Y축 길이)', 
        line=dict(color='red', width=5)
    ))

    # 5) Tan (x=1 접선 상에서의 높이)
    if not np.isnan(tan_val) and abs(tan_val) <= 3:
        fig1.add_trace(go.Scatter(
            x=[1, 1], y=[0, tan_val], 
            mode='lines', name='Tan (접선 높이)', 
            line=dict(color='green', width=5)
        ))
        # 동경 연장선
        fig1.add_trace(go.Scatter(
            x=[0, 1], y=[0, tan_val], 
            mode='lines', showlegend=False, 
            line=dict(color='green', dash='dot')
        ))

    # 점 P 표기
    fig1.add_trace(go.Scatter(
        x=[cos_val], y=[sin_val],
        mode='text', text=[f"  P({cos_val:.2f}, {sin_val:.2f})"],
        textposition="top right", showlegend=False
    ))

    # X축, Y축 기준선 및 축 레이아웃 설정
    fig1.update_xaxes(
        title_text="<b>X 축</b> (Cos 영역)",
        range=[-1.6, 1.6], 
        zeroline=True, zerolinewidth=2, zerolinecolor='black',
        dtick=0.5, gridcolor='whitesmoke'
    )
    fig1.update_yaxes(
        title_text="<b>Y 축</b> (Sin 영역)",
        range=[-1.6, 1.6], 
        zeroline=True, zerolinewidth=2, zerolinecolor='black',
        scaleanchor="x", scaleratio=1,
        dtick=0.5, gridcolor='whitesmoke'
    )

    fig1.update_layout(
        title="단위원에서의 삼각함수 정의 시각화",
        width=700,
        height=650,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(x=1.02, y=1, xanchor="left", yanchor="top")
    )

    st.plotly_chart(fig1, use_container_width=False)


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

        # X축과 Y축 강조 설정
        fig.update_xaxes(title_text="<b>X 축 (각도 °)</b>", range=[-360, 720], dtick=180, zeroline=True, zerolinewidth=2, zerolinecolor='black')
        fig.update_yaxes(title_text="<b>Y 축 (값)</b>", range=[-6, 6], zeroline=True, zerolinewidth=2, zerolinecolor='black')

        fig.update_layout(
            title="사인 함수 개형 변화",
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

        # X축과 Y축 강조 설정
        fig.update_xaxes(title_text="<b>X 축 (각도 °)</b>", range=[-360, 720], dtick=180, zeroline=True, zerolinewidth=2, zerolinecolor='black')
        fig.update_yaxes(title_text="<b>Y 축 (값)</b>", range=[-6, 6], zeroline=True, zerolinewidth=2, zerolinecolor='black')

        fig.update_layout(
            title="코사인 함수 개형 변화",
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
        
        y_user = A * np.tan(tan_inner) + D
        y_user[np.abs(np.tan(tan_inner)) > 10] = np.nan

        y_base = np.tan(np.radians(x_deg))
        y_base[np.abs(y_base) > 10] = np.nan

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_deg, y=y_user, mode='lines', name='변형된 Tan', line=dict(color='green', width=3)))
        fig.add_trace(go.Scatter(x=x_deg, y=y_base, mode='lines', name='기본 Tan (비교용)', opacity=0.4, line=dict(color='gray', dash='dash')))

        # X축과 Y축 강조 설정
        fig.update_xaxes(title_text="<b>X 축 (각도 °)</b>", range=[-360, 720], dtick=180, zeroline=True, zerolinewidth=2, zerolinecolor='black')
        fig.update_yaxes(title_text="<b>Y 축 (값)</b>", range=[-6, 6], zeroline=True, zerolinewidth=2, zerolinecolor='black')

        fig.update_layout(
            title="탄젠트 함수 개형 변화",
            height=550, margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
