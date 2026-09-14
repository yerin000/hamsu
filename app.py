import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Page Config
st.set_page_config(
    page_title="삼각함수 개념 & 개형 완벽 학습 앱",
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
        "4. 탄젠트(Tangent) 함수 개형",
        "5. 📝 학습 점검 퀴즈"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 왼쪽 메뉴에서 원하는 모듈을 클릭하세요.")


# ==============================================================================
# [모듈 1] 단위원과 삼각함수의 개념
# ==============================================================================
if menu == "1. 단위원과 삼각함수의 개념":
    st.title("1. 단위원으로 배우는 삼각함수의 정의")
    
    # 개념 설명글
    st.markdown("""
    ### 📖 개념 설명
    반지름의 길이가 **1인 원**을 **단위원(Unit Circle)**이라고 합니다. 
    단위원 위를 움직이는 점 $P(x, y)$와 $X$축 양의 방향과 이루는 각도를 $\\theta$라고 할 때, 삼각함수는 다음과 같이 정의됩니다.
    
    1. **$\cos(\\theta)$ (파란색)**: 동경 끝점 $P$의 **$X$좌표**입니다. ($X$축 상의 길이)
    2. **$\sin(\\theta)$ (빨간색)**: 동경 끝점 $P$의 **$Y$좌표**입니다. ($Y$축 상의 길이)
    3. **$\\tan(\\theta)$ (초록색)**: $X=1$에서의 접선과 동경의 연장선이 만나는 **높이**입니다. 즉, $\\tan(\\theta) = \\frac{\\sin\\theta}{\\cos\\theta}$ (기울기)를 의미합니다.
    """)
    st.markdown("---")

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

    fig1 = go.Figure()

    # 단위원 테두리
    theta_full = np.linspace(0, 2 * np.pi, 300)
    fig1.add_trace(go.Scatter(
        x=np.cos(theta_full), y=np.sin(theta_full), 
        mode='lines', name='단위원 (r=1)', 
        line=dict(color='lightgray', dash='dot', width=2)
    ))

    # 동경
    fig1.add_trace(go.Scatter(
        x=[0, cos_val], y=[0, sin_val], 
        mode='lines+markers', name='동경 (r=1)', 
        line=dict(color='purple', width=3),
        marker=dict(size=8, color='purple')
    ))

    # Cos (X축)
    fig1.add_trace(go.Scatter(
        x=[0, cos_val], y=[0, 0], 
        mode='lines', name='Cos (X축 길이)', 
        line=dict(color='blue', width=5)
    ))

    # Sin (Y축)
    fig1.add_trace(go.Scatter(
        x=[cos_val, cos_val], y=[0, sin_val], 
        mode='lines', name='Sin (Y축 길이)', 
        line=dict(color='red', width=5)
    ))

    # Tan (접선)
    if not np.isnan(tan_val) and abs(tan_val) <= 3:
        fig1.add_trace(go.Scatter(
            x=[1, 1], y=[0, tan_val], 
            mode='lines', name='Tan (접선 높이)', 
            line=dict(color='green', width=5)
        ))
        fig1.add_trace(go.Scatter(
            x=[0, 1], y=[0, tan_val], 
            mode='lines', showlegend=False, 
            line=dict(color='green', dash='dot')
        ))

    # 점 P 좌표 표기
    fig1.add_trace(go.Scatter(
        x=[cos_val], y=[sin_val],
        mode='text', text=[f"  P({cos_val:.2f}, {sin_val:.2f})"],
        textposition="top right", showlegend=False
    ))

    fig1.update_xaxes(
        title_text="<b>X 축</b> (Cos)", range=[-1.6, 1.6], 
        zeroline=True, zerolinewidth=2, zerolinecolor='black',
        dtick=0.5, gridcolor='whitesmoke'
    )
    fig1.update_yaxes(
        title_text="<b>Y 축</b> (Sin)", range=[-1.6, 1.6], 
        zeroline=True, zerolinewidth=2, zerolinecolor='black',
        scaleanchor="x", scaleratio=1, dtick=0.5, gridcolor='whitesmoke'
    )

    fig1.update_layout(
        title="단위원 삼각함수 정의 시각화", width=700, height=600,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(x=1.02, y=1, xanchor="left", yanchor="top")
    )

    st.plotly_chart(fig1, use_container_width=False)


# ==============================================================================
# [모듈 2] 사인(Sine) 함수 개형
# ==============================================================================
elif menu == "2. 사인(Sine) 함수 개형":
    st.title("2. 사인(Sine) 함수 개형 및 성질")
    
    st.markdown("""
    ### 📖 사인 함수 개념 및 공식
    사인 함수 기본형 $y = \sin(x)$는 **원점 대칭(기함수)**이며 주기적인 파형을 가집니다.
    변형된 수식 $y = A \cdot \sin(B(x - C)) + D$에서의 역할은 다음과 같습니다.
    
    - **$A$ (진폭/수직 폭)**: 최댓값과 최솟값의 폭을 결정합니다. ($\text{최댓값} = A + D$, $\text{최솟값} = -A + D$)
    - **$B$ (주기 계수)**: 주기를 결정합니다. **주기** = $\\frac{360^\circ}{B}$
    - **$C$ (평행이동/위상)**: $X$축 방향 평행이동 ($C^\circ$만큼 오른쪽 이동)
    - **$D$ (Y축 이동)**: $Y$축 방향 평행이동
    """)
    st.latex(r"y = A \cdot \sin(B(x - C)) + D")
    st.markdown("---")

    col_ctrl, col_graph = st.columns([1, 2.5])

    with col_ctrl:
        st.subheader("🎛️ 파라미터 조절")
        A = st.slider("진폭 / 수직폭 (A)", 0.1, 5.0, 1.0, step=0.1, key="sin_A")
        B = st.slider("주기 계수 (B)", 0.1, 4.0, 1.0, step=0.1, key="sin_B")
        C_deg = st.slider("평행이동 (C, °)", -180, 180, 0, step=15, key="sin_C")
        D = st.slider("Y축 이동 (D)", -3.0, 3.0, 0.0, step=0.5, key="sin_D")

        period = 360 / B
        st.markdown("---")
        st.subheader("📊 주요 정보")
        st.write(f"- **현재 수식**: $y = {A:.1f}\\sin({B:.1f}(x - {C_deg}^\circ)) + {D:.1f}$")
        st.write(f"- **주기 (Period)**: **{period:.1f}°** ($360^\circ / {B:.1f}$)")
        st.write(f"- **최댓값**: **{A + D:.1f}** / **최솟값**: **{-A + D:.1f}**")

    with col_graph:
        x_deg = np.linspace(-360, 720, 1080)
        y_user = A * np.sin(B * np.radians(x_deg - C_deg)) + D
        y_base = np.sin(np.radians(x_deg))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_deg, y=y_user, mode='lines', name='변형된 Sin', line=dict(color='red', width=3)))
        fig.add_trace(go.Scatter(x=x_deg, y=y_base, mode='lines', name='기본 Sin (비교용)', opacity=0.4, line=dict(color='gray', dash='dash')))

        fig.update_xaxes(title_text="<b>X 축 (각도 °)</b>", range=[-360, 720], dtick=180, zeroline=True, zerolinewidth=2, zerolinecolor='black')
        fig.update_yaxes(title_text="<b>Y 축 (값)</b>", range=[-6, 6], zeroline=True, zerolinewidth=2, zerolinecolor='black')

        fig.update_layout(title="사인 함수 개형 변화", height=550, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# [모듈 3] 코사인(Cosine) 함수 개형
# ==============================================================================
elif menu == "3. 코사인(Cosine) 함수 개형":
    st.title("3. 코사인(Cosine) 함수 개형 및 성질")
    
    st.markdown("""
    ### 📖 코사인 함수 개념 및 공식
    코사인 함수 기본형 $y = \cos(x)$는 **Y축 대칭(우함수)**이며, 사인 함수를 $X$축 방향으로 $-90^\circ$ 평행이동한 것과 같습니다.
    
    - **$A$ (진폭/수직 폭)**: 최댓값과 최솟값의 폭을 결정합니다. ($\text{최댓값} = A + D$, $\text{최솟값} = -A + D$)
    - **$B$ (주기 계수)**: 주기를 결정합니다. **주기** = $\\frac{360^\circ}{B}$
    - **$C$ (평행이동/위상)**: $X$축 방향 평행이동
    - **$D$ (Y축 이동)**: $Y$축 방향 평행이동
    """)
    st.latex(r"y = A \cdot \cos(B(x - C)) + D")
    st.markdown("---")

    col_ctrl, col_graph = st.columns([1, 2.5])

    with col_ctrl:
        st.subheader("🎛️ 파라미터 조절")
        A = st.slider("진폭 / 수직폭 (A)", 0.1, 5.0, 1.0, step=0.1, key="cos_A")
        B = st.slider("주기 계수 (B)", 0.1, 4.0, 1.0, step=0.1, key="cos_B")
        C_deg = st.slider("평행이동 (C, °)", -180, 180, 0, step=15, key="cos_C")
        D = st.slider("Y축 이동 (D)", -3.0, 3.0, 0.0, step=0.5, key="cos_D")

        period = 360 / B
        st.markdown("---")
        st.subheader("📊 주요 정보")
        st.write(f"- **현재 수식**: $y = {A:.1f}\\cos({B:.1f}(x - {C_deg}^\circ)) + {D:.1f}$")
        st.write(f"- **주기 (Period)**: **{period:.1f}°** ($360^\circ / {B:.1f}$)")
        st.write(f"- **최댓값**: **{A + D:.1f}** / **최솟값**: **{-A + D:.1f}**")

    with col_graph:
        x_deg = np.linspace(-360, 720, 1080)
        y_user = A * np.cos(B * np.radians(x_deg - C_deg)) + D
        y_base = np.cos(np.radians(x_deg))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_deg, y=y_user, mode='lines', name='변형된 Cos', line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=x_deg, y=y_base, mode='lines', name='기본 Cos (비교용)', opacity=0.4, line=dict(color='gray', dash='dash')))

        fig.update_xaxes(title_text="<b>X 축 (각도 °)</b>", range=[-360, 720], dtick=180, zeroline=True, zerolinewidth=2, zerolinecolor='black')
        fig.update_yaxes(title_text="<b>Y 축 (값)</b>", range=[-6, 6], zeroline=True, zerolinewidth=2, zerolinecolor='black')

        fig.update_layout(title="코사인 함수 개형 변화", height=550, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# [모듈 4] 탄젠트(Tangent) 함수 개형 (점근선 수식 포함)
# ==============================================================================
elif menu == "4. 탄젠트(Tangent) 함수 개형":
    st.title("4. 탄젠트(Tangent) 함수 개형 및 점근선")
    
    st.markdown("""
    ### 📖 탄젠트 함수 성질 및 점근선 공식
    탄젠트 함수 $y = \tan(x)$는 **원점 대칭(기함수)**이며, **기본 주기는 $180^\circ$**입니다.
    
    1. **점근선 (Asymptote)**: $\cos(\\theta) = 0$이 되는 지점에서 탄젠트 값이 존재하지 않아 곡선이 도달하지 못하는 직선이 생깁니다.
    2. **변형 시 주기**: $y = A\cdot\tan(B(x-C))+D$의 주기는 **$\\frac{180^\circ}{B}$** 입니다.
    3. **점근선 방정식**: $B(x - C) = 90^\circ + 180^\circ \cdot n$ (단, $n$은 정수)
       $$\Rightarrow x = \frac{90^\circ + 180^\circ \cdot n}{B} + C$$
    """)
    st.latex(r"y = A \cdot \tan(B(x - C)) + D")
    st.markdown("---")

    col_ctrl, col_graph = st.columns([1, 2.5])

    with col_ctrl:
        st.subheader("🎛️ 파라미터 조절")
        A = st.slider("수직 기울기 / 폭 (A)", 0.1, 5.0, 1.0, step=0.1, key="tan_A")
        B = st.slider("주기 계수 (B)", 0.1, 4.0, 1.0, step=0.1, key="tan_B")
        C_deg = st.slider("평행이동 (C, °)", -180, 180, 0, step=15, key="tan_C")
        D = st.slider("Y축 이동 (D)", -3.0, 3.0, 0.0, step=0.5, key="tan_D")

        period = 180 / B
        st.markdown("---")
        st.subheader("📊 주요 정보 & 점근선")
        st.write(f"- **현재 수식**: $y = {A:.1f}\\tan({B:.1f}(x - {C_deg}^\circ)) + {D:.1f}$")
        st.write(f"- **주기 (Period)**: **{period:.1f}°** ($180^\circ / {B:.1f}$)")
        st.write("- **최대/최솟값**: 없음 (무한대)")

    with col_graph:
        x_deg = np.linspace(-360, 720, 3000)
        tan_inner = B * np.radians(x_deg - C_deg)
        
        y_user = A * np.tan(tan_inner) + D
        y_user[np.abs(np.tan(tan_inner)) > 10] = np.nan

        y_base = np.tan(np.radians(x_deg))
        y_base[np.abs(y_base) > 10] = np.nan

        fig = go.Figure()

        # 점근선 (Asymptotes) 계산 및 주황색 수직 점선으로 추가
        # n에 따른 점근선 위치: x = (90 + 180*n)/B + C
        asymptotes = []
        for n in range(-10, 15):
            asymptote_x = (90 + 180 * n) / B + C_deg
            if -360 <= asymptote_x <= 720:
                asymptotes.append(asymptote_x)
                fig.add_vline(
                    x=asymptote_x, 
                    line_width=1.5, 
                    line_dash="dash", 
                    line_color="orange"
                )

        # 탄젠트 곡선 추가
        fig.add_trace(go.Scatter(x=x_deg, y=y_user, mode='lines', name='변형된 Tan', line=dict(color='green', width=3)))
        fig.add_trace(go.Scatter(x=x_deg, y=y_base, mode='lines', name='기본 Tan (비교용)', opacity=0.3, line=dict(color='gray', dash='dash')))

        # 범례용 가짜 트레이스 (점근선 설명 표시)
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', name='점근선 (Asymptote)', line=dict(color='orange', dash='dash', width=1.5)))

        fig.update_xaxes(title_text="<b>X 축 (각도 °)</b>", range=[-360, 720], dtick=180, zeroline=True, zerolinewidth=2, zerolinecolor='black')
        fig.update_yaxes(title_text="<b>Y 축 (값)</b>", range=[-6, 6], zeroline=True, zerolinewidth=2, zerolinecolor='black')

        fig.update_layout(title="탄젠트 함수 개형 및 점근선 시각화", height=550, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

        # 점근선 좌표 안내
        if asymptotes:
            asym_str = ", ".join([f"{x:.1f}°" for x in asymptotes[:5]])
            st.info(f"📍 **현재 화면 영역 내 주요 점근선 위치**: {asym_str} ...")


# ==============================================================================
# [모듈 5] 📝 학습 점검 퀴즈 & 실시간 피드백
# ==============================================================================
elif menu == "5. 📝 학습 점검 퀴즈":
    st.title("5. 삼각함수 개념 학습 점검 퀴즈")
    st.write("학습한 내용을 바탕으로 문제를 풀어보세요! 정답을 제출하면 **즉시 상세한 피드백**이 제공됩니다.")
    st.markdown("---")

    # Q1
    st.subheader("Q1. 단위원에서 각도 θ에 대응하는 동경 끝점 P(x, y)의 X좌표가 의미하는 삼각함수는 무엇인가요?")
    q1_ans = st.radio("선택하세요:", ["사인 (sin θ)", "코사인 (cos θ)", "탄젠트 (tan θ)", "코탄젠트 (cot θ)"], key="q1")
    
    if st.button("Q1 정답 확인", key="btn1"):
        if q1_ans == "코사인 (cos θ)":
            st.success("🎉 **정답입니다!**\n\n**해설**: 단위원(r=1)에서 점 P의 X좌표는 $\cos\\theta$, Y좌표는 $\sin\\theta$입니다.")
        else:
            st.error("❌ **틀렸습니다.**")
            st.info("💡 **피드백**: $X$좌표는 **코사인($\cos\\theta$)**입니다! 반대로 $Y$좌표가 사인($\sin\\theta$)입니다.")

    st.markdown("---")

    # Q2
    st.subheader("Q2. 함수 $y = 3\sin(2x)$의 주기(Period)는 몇 도(°)인가요?")
    q2_ans = st.radio("선택하세요:", ["90°", "180°", "360°", "720°"], key="q2")
    
    if st.button("Q2 정답 확인", key="btn2"):
        if q2_ans == "180°":
            st.success("🎉 **정답입니다!**\n\n**해설**: 사인 함수의 기본 주기는 $360^\circ$입니다. 계수 $B=2$이므로 주기는 $\\frac{360^\circ}{2} = 180^\circ$가 됩니다.")
        else:
            st.error("❌ **틀렸습니다.**")
            st.info("💡 **피드백**: 주기는 $\\frac{\text{기본주기}(360^\circ)}{B}$ 공식으로 계산합니다. $B=2$이므로 $360 / 2 = 180^\circ$입니다.")

    st.markdown("---")

    # Q3
    st.subheader("Q3. 탄젠트 함수 $y = \tan(x)$의 점근선이 존재하는 이유로 가장 적절한 것은?")
    q3_ans = st.radio("선택하세요:", [
        "진폭이 너무 커져서", 
        "tan θ = sin θ / cos θ 에서 cos θ = 0 이 되어 분모가 0이 되기 때문에", 
        "Y축 평행이동 때문에", 
        "X축 대칭 이동 때문에"
    ], key="q3")
    
    if st.button("Q3 정답 확인", key="btn3"):
        if q3_ans == "tan θ = sin θ / cos θ 에서 cos θ = 0 이 되어 분모가 0이 되기 때문에":
            st.success("🎉 **정답입니다!**\n\n**해설**: $\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}$에서 $\\cos\\theta = 0$이 되는 $90^\circ, 270^\circ \dots$ 등의 지점에서는 값이 정의되지 않아 점근선이 발생합니다.")
        else:
            st.error("❌ **틀렸습니다.**")
            st.info("💡 **피드백**: 분모인 **$\cos\\theta$가 0이 되는 지점**에서는 수학적으로 나눗셈이 정의되지 않기 때문에 점근선이 생깁니다.")
