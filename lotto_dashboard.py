import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components

# JSON 파일 불러오기
with open("lotto_100.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

st.set_page_config(page_title="로또 분석 - LOTTO 6/45🎲", layout="wide")

st.title("로또 분석 - LOTTO 6/45🎲")
## st.caption("최근 100개 회차 기준 | 동행복권 API 기반")

GA_TRACKING_ID = "G-HV98N97M8G"  # 본인의 실제 ID로 교체

components.html(f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_TRACKING_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_TRACKING_ID}');
</script>
""", height=0)

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

### 최신회차 
# 최신 회차 기준 데이터
latest = df.loc[df["회차"].idxmax()]
latest_round = int(latest["회차"])
numbers = latest["numbers"]
bonus = latest["bonus"]
first_prize = int(latest["1등 당첨금"])
first_total = int(latest["1등 총 당첨금"])
winner_count = int(latest["1등 당첨자 수"])

def to_eok(value):
    return f"{value / 100_000_000:.1f}억"
    
taxed_prize = int(first_prize * 0.78)

st.subheader(f"🎯 {latest_round}회 당첨 결과")

st.markdown(
    f"""
    - 🎲 **번호**: {', '.join(map(str, numbers))} + 보너스 {bonus}  
    - 💰 **1인당 당첨금**: {to_eok(first_prize)}
    - 💸 **실수령액 (세후)**: {to_eok(taxed_prize)}
    - 👥 **당첨자 수**: {winner_count}명 / 총 당첨금: {to_eok(first_total)}
    """
)
###

### 최신회차 1등 판매점

# JSON 데이터 불러오기
with open("lotto_store_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 회차 리스트 추출 및 선택
rounds = sorted(set(item["round"] for item in data), reverse=True)
selected_round = st.selectbox("회차 선택", rounds)

# 선택된 회차에 해당하는 판매점 출력
st.write(f"### {selected_round}회차 1등 배출 판매점")

filtered = [item for item in data if item["round"] == selected_round]
for item in filtered:
    # 구매 방식에 따라 아이콘 선택
    if "수동" in item["method"]:
        icon = "✍️"
    elif "반자동" in item["method"]:
        icon = "⚙️"
    else:
        icon = "🎯"  # 자동

    st.markdown(f"""
- 🏪 **{item['store']}** ({icon} {item['method']})  
📍 {item['address']}
""")

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

