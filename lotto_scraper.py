# lotto_scraper.py
import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

def fetch_round_data(round_number):
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={round_number}"
    try:
        res = requests.get(url)
        data = res.json()

        if data.get("returnValue") != "success":
            print(f"[!] Invalid data for round {round_number}")
            return None

        nums = [data[f"drwtNo{i}"] for i in range(1, 7)]
        bonus = data["bnusNo"]
        first_prize = data["firstWinamnt"]
        first_winner_count = data["firstPrzwnerCo"]
        sales = data["totSellamnt"]

        return {
            "round": round_number,
            "numbers": nums,
            "bonus": bonus,
            "first_total_prize": first_prize * first_winner_count,
            "first_winner_count": first_winner_count,
            "first_prize": first_prize,
            "auto": None,  # Not provided by API
            "manual": None,  # Not provided by API
            "semi_auto": None,  # Not provided by API
            "sales": sales
        }

    except Exception as e:
        print(f"[!] Error on round {round_number}: {e}")
        return None


def fetch_recent_lotto_data(latest_round, count=100):
    results = []
    for i in tqdm(range(latest_round, latest_round - count, -1)):
        data = fetch_round_data(i)
        if data:
            results.append(data)
    return results


if __name__ == "__main__":
    latest_round = 1180  # 예시: 최신 회차를 수동 지정 (또는 API로 가져오게 구성 가능)
    data = fetch_recent_lotto_data(latest_round)
    with open("lotto_100.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ lotto_100.json 저장 완료")