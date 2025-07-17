import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components

# JSON 파일 불러오기
with open("lotto_100.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

st.set_page_config(page_title="AI 로또 분석 - LOTTO 6/45", layout="wide")

st.title("🎲 AI 로또 분석 - LOTTO 6/45")
## st.caption("최근 100개 회차 기준 | 동행복권 API 기반")

# 회차 기준 내림차순 정렬
df = df.sort_values(by="round", ascending=False)

# 컬럼 한글명 매핑 (보기 편하게)
df.rename(columns={
    "round": "회차",
    "first_prize": "1등 당첨금",
    "first_total_prize": "1등 총 당첨금",
    "first_winner_count": "1등 당첨자 수",
    "sales": "총 판매금액"
}, inplace=True)

### 로또번호 생성기 테스트
import streamlit as st
import random

st.subheader("🎲 랜덤 로또 번호 생성기")

# 상태 초기화
if "lotto_numbers" not in st.session_state:
    st.session_state.lotto_numbers = []

def generate_lotto():
    main = sorted(random.sample(range(1, 46), 6))
    bonus = random.choice([n for n in range(1, 46) if n not in main])
    st.session_state.lotto_numbers = main + [bonus]

# 버튼
st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
clicked = st.button("💡 로또 번호 뽑기", type="primary")
st.markdown("</div>", unsafe_allow_html=True)

if clicked:
    generate_lotto()

# 출력 블럭
if st.session_state.lotto_numbers:
    main = st.session_state.lotto_numbers[:6]
    bonus = st.session_state.lotto_numbers[6]

    def ball_html(num, color):
        return f"<div class='ball' style='background:{color};'>{num}</div>"

    html_balls = "".join([ball_html(n, "#f1c40f") for n in main])
    html_bonus = ball_html(bonus, "#e74c3c")

    responsive_html = f"""
    <style>
        .ball {{
            display: inline-flex;
            justify-content: center;
            align-items: center;
            margin: 6px;
            width: 60px;
            height: 60px;
            border-radius: 30px;
            background: #ccc;
            color: #000;
            font-weight: bold;
            font-size: 22px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        }}
        .lotto-container {{
            display: flex;
            flex-wrap: nowrap;
            justify-content: center;
            align-items: center;
            overflow-x: auto;
            padding: 0 10px;
        }}
        .plus {{
            font-size: 28px;
            margin: 0 12px;
            color: #e74c3c;
            font-weight: bold;
        }}
        /* 태블릿 이하 */
        @media (max-width: 768px) {{
            .ball {{
                width: 48px;
                height: 48px;
                border-radius: 24px;
                font-size: 18px;
                margin: 4px;
            }}
            .plus {{
                font-size: 24px;
                margin: 0 8px;
            }}
        }}
        /* 모바일 세로 */
        @media (max-width: 480px) {{
            .ball {{
                width: 38px;
                height: 38px;
                border-radius: 19px;
                font-size: 16px;
                margin: 3px;
            }}
            .plus {{
                font-size: 20px;
                margin: 0 6px;
            }}
        }}
    </style>

    <div class="lotto-container">
        {html_balls}
        <span class="plus">+</span>
        {html_bonus}
    </div>
    """

    components.html(responsive_html, height=140)
###

## 역대 최다 1등 당첨자 수
st.subheader("🏆 역대 최다 1등 당첨자 수")

# 가장 많은 1등 당첨자 수 가진 회차 데이터 추출
max_row = df.loc[df["1등 당첨자 수"].idxmax()]
max_winners = int(max_row["1등 당첨자 수"])
max_round = int(max_row["회차"])
total_prize = int(max_row["1등 총 당첨금"])
per_person_prize = int(max_row["1등 당첨금"])

# 전광판 숫자 + 단위 '명' 작게 표시
st.markdown(
    f"""
    <h1 style='text-align:center; font-size:96px; margin-bottom:0px;'>
        {max_winners}<span style='font-size:36px;'>명</span>
    </h1>
    """,
    unsafe_allow_html=True
)

# 부가 정보 (중앙 정렬, 작게)
st.markdown(
    f"""
    <div style='text-align:center; font-size:18px; margin-top:5px; line-height:1.6;'>
        {max_round}회차<br>
        1등 총 당첨금: {total_prize:,}원<br>
        1인당 당첨금: {per_person_prize:,}원
    </div>
    """,
    unsafe_allow_html=True
)
###

### 최다 출현 번호
st.subheader("🔢 가장 많이 출현한 번호")

from collections import Counter
import ast

# 문자열 → 리스트 변환 처리
if "numbers" in df.columns and isinstance(df["numbers"].iloc[0], str):
    df["numbers"] = df["numbers"].apply(ast.literal_eval)

if "numbers" in df.columns and isinstance(df["numbers"].iloc[0], list):
    all_numbers = sum(df["numbers"], [])
    counter = Counter(all_numbers)
    most_common_num, count = counter.most_common(1)[0]

    # 숫자 전광판 스타일로, '번' 작게 붙이기
    st.markdown(
        f"""
        <h1 style='text-align:center; font-size:96px; margin-bottom:0px;'>
            {most_common_num}<span style='font-size:36px;'>번</span>
        </h1>
        """,
        unsafe_allow_html=True
    )

    # 설명 텍스트
    st.markdown(
        f"""
        <div style='text-align:center; font-size:18px; margin-top:5px; line-height:1.6;'>
            총 출현 횟수: {count}회<br>
            분석 대상 회차: 최근 {len(df)}회차
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("numbers 데이터가 없거나 올바른 형식이 아닙니다.")
###

st.subheader("📈 1등 당첨금 추이 (회차 기준)")
st.line_chart(df.set_index("회차")[["1등 당첨금"]])

st.subheader("🏆 1등 당첨자 수")
st.bar_chart(df.set_index("회차")[["1등 당첨자 수"]])

st.subheader("💰 총 판매금액")
st.line_chart(df.set_index("회차")[["총 판매금액"]])

st.subheader("🔢 당첨번호 분포 (출현 빈도순)")

# 문자열로 저장된 경우 리스트로 변환
import ast
if isinstance(df["numbers"].iloc[0], str):
    df["numbers"] = df["numbers"].apply(ast.literal_eval)

from collections import Counter
all_numbers = sum(df["numbers"], [])  # 리스트 평탄화
counter = Counter(all_numbers)

freq_df = pd.DataFrame(counter.items(), columns=["번호", "출현 빈도"]).sort_values(by="출현 빈도", ascending=False)
st.bar_chart(freq_df.set_index("번호"))

st.subheader("📋 당첨 히스토리 보기")
st.dataframe(df, use_container_width=True)

