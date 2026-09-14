import streamlit as st
import numpy as np
import plotly.graph_objects as px
import math
import random

st.set_page_config(
    page_title="삼각함수 완벽 학습 도구 (Trigonometry Interactive Explorer)",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for aesthetic polish
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }
    .info-card {
        background-color: #1e293b;
        padding: 1.2rem;
        border-radius: 0.75rem;
        border: 1px solid #334155;
        margin-bottom: 1rem;
    }
    .metric-badge {
        background-color: #0f172a;
        padding: 0.8rem;
        border-radius: 0.5rem;
        border: 1px solid #334155;
        text-align: center;
    }
    .quiz-card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #475569;
    }
</style>
""", unsafe_allow_html=True)


st.sidebar.title("📐 삼각함수 학습 목차")
selected_module = st.sidebar.radio(
    "학습할 모듈을 선택하세요:",
    [
        "1. 단위원과 삼각함수의 개념",
        "2. 사인(Sine) 함수 개형",
        "3. 코사인(Cosine) 함수 개형",
        "4. 탄젠트(Tangent) 함수 개형과 점근선",
        "5. 📝 무한 동적 퀴즈"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: 각 슬라이더를 조작하면서 그래프 및 단위원의 변화를 실시간으로 확인해보세요!")


# ==============================================================================
# MODULE 1: UNIT CIRCLE EXPLORER
# ==============================================================================
if selected_module == "1. 단위원과 삼각함수의 개념":
    st.markdown('<div class="main-header">1. 단위원과 삼각함수의 정의</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">반지름이 1인 단위원(Unit Circle) 위에서의 동경과 삼각함수의 기하학적 의미를 관찰합니다.</div>', unsafe_allow_html=True)

    col_ctrl, col_graph = st.columns([1, 2])

    with col_ctrl:
        st.subheader("⚙️ 각도 설정")
        angle_deg = st.slider("각도 θ (도, Degree)", min_value=0, max_value=360, value=45, step=1)
        angle_rad = np.radians(angle_deg)
        
        # Display angle in terms of pi
        pi_fraction = angle_deg / 180.0
        
        st.markdown(f"""
        <div class="info-card">
            <p><b>각도 표현:</b></p>
            <ul>
                <li>육십진법: <b>{angle_deg}°</b></li>
                <li>호도법: <b>{angle_rad:.3f} rad</b> ({pi_fraction:.2f}π rad)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        cos_val = np.cos(angle_rad)
        sin_val = np.sin(angle_rad)
        tan_val = np.tan(angle_rad) if abs(cos_val) > 1e-5 else None

        st.subheader("📊 삼각비 계산값")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(f'<div class="metric-badge"><span style="color:#3b82f6;font-weight:bold;">cos(θ)</span><br><h3>{cos_val:.3f}</h3></div>', unsafe_allow_html=True)
        with m_col2:
            st.markdown(f'<div class="metric-badge"><span style="color:#ef4444;font-weight:bold;">sin(θ)</span><br><h3>{sin_val:.3f}</h3></div>', unsafe_allow_html=True)
        with m_col3:
            tan_disp = f"{tan_val:.3f}" if tan_val is not None and abs(tan_val) < 100 else "∞"
            st.markdown(f'<div class="metric-badge"><span style="color:#10b981;font-weight:bold;">tan(θ)</span><br><h3>{tan_disp}</h3></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card" style="margin-top:1rem;">
            <h4>💡 핵심 삼각함수 정의</h4>
            <p>• <b>$\cos\\theta$</b>: 동경과 단위원의 교점 $P(x,y)$의 <b>x좌표</b> (밑변)</p>
            <p>• <b>$\sin\\theta$</b>: 동경과 단위원의 교점 $P(x,y)$의 <b>y좌표</b> (높이)</p>
            <p>• <b>$\\tan\\theta$</b>: 동경의 <b>기울기</b> = $\\frac{\sin\\theta}{\cos\\theta}$ = 접선 $x=1$에서의 높이</p>
        </div>
        """, unsafe_allow_html=True)

    with col_graph:
        fig = px.Figure()

        # 1. Circle
        theta = np.linspace(0, 2*np.pi, 300)
        fig.add_trace(px.Scatter(x=np.cos(theta), y=np.sin(theta), mode='lines', name='단위원', line=dict(color='#64748b', width=2)))

        # 2. Axes
        fig.add_shape(type="line", x0=-1.5, y0=0, x1=1.5, y1=0, line=dict(color="#475569", width=1.5))
        fig.add_shape(type="line", x0=0, y0=-1.5, x1=0, y1=1.5, line=dict(color="#475569", width=1.5))

        # 3. Radius / Terminal Arm (Hypotenuse)
        px_val = cos_val
        py_val = sin_val
        fig.add_trace(px.Scatter(x=[0, px_val], y=[0, py_val], mode='lines+markers', name='동경 (Radius)', line=dict(color='#a855f7', width=3), marker=dict(size=8)))

        # 4. Cosine Projection (Blue horizontal line)
        fig.add_trace(px.Scatter(x=[0, px_val], y=[0, 0], mode='lines', name='cos(θ) [X좌표]', line=dict(color='#3b82f6', width=4)))

        # 5. Sine Projection (Red vertical line)
        fig.add_trace(px.Scatter(x=[px_val, px_val], y=[0, py_val], mode='lines', name='sin(θ) [Y좌표]', line=dict(color='#ef4444', width=4)))

        # 6. Tangent Projection (Green line at x = 1)
        if tan_val is not None and abs(tan_val) < 5:
            fig.add_trace(px.Scatter(x=[1, 1], y=[0, tan_val], mode='lines', name='tan(θ) [접선]', line=dict(color='#10b981', width=4)))
            fig.add_trace(px.Scatter(x=[0, 1], y=[0, tan_val], mode='lines', name='동경 연장선', line=dict(color='#10b981', width=1.5, dash='dash')))

        # Tangent line reference x=1
        fig.add_shape(type="line", x0=1, y0=-1.5, x1=1, y1=1.5, line=dict(color="#334155", width=1, dash="dot"))

        fig.update_layout(
            title=f"단위원 시각화 (θ = {angle_deg}°)",
            xaxis=dict(range=[-1.5, 1.5], zeroline=False, scaleanchor="y", scaleratio=1),
            yaxis=dict(range=[-1.5, 1.5], zeroline=False),
            template="plotly_dark",
            height=550,
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )

        st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# HELPER FOR GENERAL GRAPHING
# ==============================================================================
def render_function_module(func_type, title, accent_color, default_amplitude=1.0):
    st.markdown(f'<div class="main-header">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">일반식 $y = A \\cdot \\{func_type}(B(x - C)) + D$ 의 파라미터 변형을 관찰합니다.</div>', unsafe_allow_html=True)

    c_ctrl, c_graph = st.columns([1, 2])

    with c_ctrl:
        st.subheader("⚙️ 파라미터 계수 조정")
        A = st.slider("진폭/확대 (A)", min_value=0.1, max_value=4.0, value=float(default_amplitude), step=0.1, key=f"{func_type}_A")
        B = st.slider("주기 계수 (B)", min_value=0.2, max_value=4.0, value=1.0, step=0.1, key=f"{func_type}_B")
        C = st.slider("위상 이동 / X축 이동 (C, 도)", min_value=-180, max_value=180, value=0, step=15, key=f"{func_type}_C")
        D = st.slider("Y축 평행이동 (D)", min_value=-3.0, max_value=3.0, value=0.0, step=0.5, key=f"{func_type}_D")

        show_base = st.checkbox("기본 파형 $y = \\" + func_type + "(x)$ 점선 비교", value=True, key=f"{func_type}_base")

        # Period calculation
        period = (180.0 / B) if func_type == 'tan' else (360.0 / B)
        
        # Display current formula in LaTeX
        sign_C = "-" if C >= 0 else "+"
        abs_C = abs(C)
        sign_D = "+" if D >= 0 else "-"
        abs_D = abs(D)
        
        st.markdown(f"""
        <div class="info-card">
            <h4>📝 현재 설정된 함수 수식</h4>
            <p style="font-size:1.2rem; text-align:center;">
                $y = {A:.1f} \\cdot \\{func_type}({B:.1f}(x {sign_C} {abs_C}^\circ)) {sign_D} {abs_D:.1f}$
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
            <h4>📐 계산된 주요 매개변수</h4>
            <ul>
                <li><b>주기 (Period):</b> <span style="color:#a855f7;font-weight:bold;">{period:.1f}°</span></li>
                {"<li><b>최댓값 (Max):</b> <span style='color:#10b981;font-weight:bold;'>" + f"{A + D:.1f}" + "</span></li>" if func_type != 'tan' else ""}
                {"<li><b>최솟값 (Min):</b> <span style='color:#ef4444;font-weight:bold;'>" + f"{-A + D:.1f}" + "</span></li>" if func_type != 'tan' else ""}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_graph:
        x_deg = np.linspace(-360, 720, 1000)
        x_rad_shifted = np.radians(x_deg - C)

        fig = px.Figure()

        # Base curve
        if show_base:
            if func_type == 'sin':
                y_base = np.sin(np.radians(x_deg))
            elif func_type == 'cos':
                y_base = np.cos(np.radians(x_deg))
            elif func_type == 'tan':
                y_base = np.tan(np.radians(x_deg))
                y_base[np.abs(y_base) > 8] = np.nan
            fig.add_trace(px.Scatter(x=x_deg, y=y_base, mode='lines', name=f'기본 {func_type}(x)', line=dict(color='#64748b', width=1.5, dash='dash')))

        # Transformed curve
        if func_type == 'sin':
            y_val = A * np.sin(B * x_rad_shifted) + D
            y_range = [-5, 5]
        elif func_type == 'cos':
            y_val = A * np.cos(B * x_rad_shifted) + D
            y_range = [-5, 5]
        elif func_type == 'tan':
            y_val = A * np.tan(B * x_rad_shifted) + D
            # Handle asymptotes by inserting NaN where tangent blows up
            y_val[np.abs(np.tan(B * x_rad_shifted)) > 10] = np.nan
            y_range = [-8, 8]

        fig.add_trace(px.Scatter(x=x_deg, y=y_val, mode='lines', name=f'변형 {func_type}(x)', line=dict(color=accent_color, width=3.5)))

        # Tangent Asymptotes Visualizer
        asymptotes_list = []
        if func_type == 'tan':
            # Asymptotes: B*(x - C) = 90 + 180*k  =>  x = (90 + 180*k)/B + C
            for k in range(-10, 10):
                asym_x = (90.0 + 180.0 * k) / B + C
                if -360 <= asym_x <= 720:
                    asymptotes_list.append(round(asym_x, 1))
                    fig.add_shape(type="line", x0=asym_x, y0=-15, x1=asym_x, y1=15, line=dict(color="#f59e0b", width=1.5, dash="dash"))

        # Axes & Grid layout
        fig.add_shape(type="line", x0=-360, y0=0, x1=720, y1=0, line=dict(color="#475569", width=1.5))
        fig.add_shape(type="line", x0=0, y0=-15, x1=0, y1=15, line=dict(color="#475569", width=1.5))

        # Y = D baseline indicator
        if D != 0:
            fig.add_shape(type="line", x0=-360, y0=D, x1=720, y1=D, line=dict(color="#e2e8f0", width=1, dash="dot"))

        fig.update_layout(
            title=f"{title} 그래프",
            xaxis=dict(range=[-360, 720], title="각도 (x, Degree)", dtick=180),
            yaxis=dict(range=y_range, title="y"),
            template="plotly_dark",
            height=520,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

        if func_type == 'tan' and asymptotes_list:
            st.warning(f"⚡ **화면 내 점근선 위치**: x = {', '.join([str(a) + '°' for a in asymptotes_list])}")


# ==============================================================================
# MODULE 2, 3, 4: SINE, COSINE, TANGENT GRAPHERS
# ==============================================================================
if selected_module == "2. 사인(Sine) 함수 개형":
    render_function_module('sin', "2. 사인(Sine) 함수 개형", "#ef4444", default_amplitude=1.0)

elif selected_module == "3. 코사인(Cosine) 함수 개형":
    render_function_module('cos', "3. 코사인(Cosine) 함수 개형", "#3b82f6", default_amplitude=1.0)

elif selected_module == "4. 탄젠트(Tangent) 함수 개형과 점근선":
    render_function_module('tan', "4. 탄젠트(Tangent) 함수 개형과 점근선", "#10b981", default_amplitude=1.0)


# ==============================================================================
# MODULE 5: INFINITE DYNAMIC QUIZ SYSTEM
# ==============================================================================
elif selected_module == "5. 📝 무한 동적 퀴즈":
    st.markdown('<div class="main-header">5. 📝 무한 동적 삼각함수 퀴즈</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">다양한 난이도의 삼각함수 문제들을 풀며 학습한 개념을 완성해보세요. (무한 문제 생성)</div>', unsafe_allow_html=True)

    difficulty = st.select_slider(
        "난이도를 선택하세요:",
        options=["초급", "중급", "고급"],
        value="초급"
    )

    # Function to generate dynamic math question
    def generate_question(diff):
        if diff == "초급":
            angles = [0, 30, 45, 60, 90, 120, 135, 150, 180, 270, 360]
            deg = random.choice(angles)
            func = random.choice(["sin", "cos", "tan"])
            rad = np.radians(deg)
            
            if func == "sin":
                ans = np.sin(rad)
            elif func == "cos":
                ans = np.cos(rad)
            else:
                if deg in [90, 270]:
                    ans = "undefined"
                else:
                    ans = np.tan(rad)
            
            if ans == "undefined":
                ans_str = "정의되지 않음 (무한대)"
                explanation = f"$\\tan({deg}^\\circ) = \\frac{{\\sin({deg}^\\circ)}}{{\\cos({deg}^\\circ)}}$ 에서 $\\cos({deg}^\\circ) = 0$ 이므로 값이 정의되지 않습니다."
            else:
                ans_str = f"{ans:.3f}"
                explanation = f"단위원 상에서 {deg}° 동경의 좌표를 이용해 $\\{func}({deg}^\\circ) = {ans_str}$ 값을 얻습니다."

            question_text = f"다음 삼각비의 값은 얼마인가요? $\\{func}({deg}^\\circ)$ (소수점 3자리 반올림 또는 '정의되지 않음')"
            options = [ans_str]
            # Generate distractor choices
            while len(options) < 4:
                d_deg = random.choice(angles)
                d_val = np.sin(np.radians(d_deg)) if func == "sin" else np.cos(np.radians(d_deg))
                d_str = f"{d_val:.3f}"
                if d_str not in options:
                    options.append(d_str)
            random.shuffle(options)
            return question_text, options, ans_str, explanation

        elif diff == "중급":
            A = random.choice([2, 3, 4])
            B = random.choice([2, 3, 4])
            func = random.choice(["sin", "cos", "tan"])
            
            period = (180 / B) if func == "tan" else (360 / B)
            question_text = f"함수 $y = {A} \\cdot \\{func}({B}x)$ 의 **주기(Period)**는 몇 도(°)인가요?"
            ans_str = f"{period:.1f}°"
            
            options = [ans_str, f"{period * 2:.1f}°", f"{period / 2:.1f}°", f"{360 * B:.1f}°"]
            options = list(set(options))
            while len(options) < 4:
                options.append(f"{random.randint(30, 360):.1f}°")
            random.shuffle(options)

            base_period = "180^\\circ" if func == "tan" else "360^\\circ"
            explanation = f"삼각함수 $y = A \\cdot \\{func}(Bx)$의 주기는 기본 주기인 $\\frac{{{base_period}}}{{|B|}}$ 로 구합니다. 따라서 $\\frac{{{base_period}}}{{{B}}} = {ans_str}$ 입니다."
            return question_text, options, ans_str, explanation

        else: # 고급
            A = random.choice([2, 3])
            D = random.choice([1, 2])
            func = random.choice(["sin", "cos"])
            
            max_v = A + D
            min_v = -A + D
            q_type = random.choice(["최댓값", "최솟값"])
            
            ans_val = max_v if q_type == "최댓값" else min_v
            ans_str = str(ans_val)
            
            question_text = f"함수 $y = {A} \\cdot \\{func}(2x) + {D}$ 의 **{q_type}**은 무엇인가요?"
            
            options = [ans_str, str(ans_val + 1), str(ans_val - 2), str(A)]
            options = list(set(options))
            while len(options) < 4:
                options.append(str(random.randint(-5, 8)))
            random.shuffle(options)

            explanation = f"$\\{func}(2x)$의 값의 범위는 $-1 \\le \\{func}(2x) \\le 1$ 입니다. 따라서 ${A} \\cdot (-1) + {D} \\le y \\le {A} \\cdot (1) + {D}$ 가 되어 최댓값은 {max_v}, 최솟값은 {min_v} 입니다."
            return question_text, options, ans_str, explanation

    # Initialize quiz state
    if "current_q" not in st.session_state or st.session_state.get("last_diff") != difficulty:
        q_text, opts, ans, expl = generate_question(difficulty)
        st.session_state["current_q"] = q_text
        st.session_state["opts"] = opts
        st.session_state["ans"] = ans
        st.session_state["expl"] = expl
        st.session_state["last_diff"] = difficulty
        st.session_state["submitted"] = False

    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    st.subheader(f"❓ {difficulty} 문제")
    st.write(st.session_state["current_q"])

    user_choice = st.radio("정답을 선택하세요:", st.session_state["opts"], key="user_choice_radio")

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("정답 제출하기", type="primary"):
            st.session_state["submitted"] = True

    with c2:
        if st.button("🔄 다음 새로운 문제 생성"):
            q_text, opts, ans, expl = generate_question(difficulty)
            st.session_state["current_q"] = q_text
            st.session_state["opts"] = opts
            st.session_state["ans"] = ans
            st.session_state["expl"] = expl
            st.session_state["submitted"] = False
            st.rerun()

    if st.session_state.get("submitted", False):
        if user_choice == st.session_state["ans"]:
            st.success("🎉 **정답입니다! 완벽해요!**")
            st.balloons()
        else:
            st.error(f"❌ **아쉽네요! 정답은 {st.session_state['ans']} 입니다.**")
        
        st.info(f"💡 **해설**: {st.session_state['expl']}")

    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("---")
st.markdown("<p style='text-align:center; color:#64748b; font-size:0.8rem;'>Streamlit & Plotly 기반 삼각함수 인터랙티브 수학 교육용 앱</p>", unsafe_allow_html=True)
