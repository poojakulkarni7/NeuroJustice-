import json
import random
from report_generator import build_report
from pdf_processor import get_risks

# ================= LOAD DATA =================
def load_dataset():
    with open("legal_ethics_dataset.json", "r", encoding="utf-8") as f:
        return json.load(f)
dataset = load_dataset()

def detect_category(user_input):
    text = user_input.lower()
    scores = {}

    for cat, data in dataset.items():
        if cat == "default":
            continue
        score = 0

        for kw in data["keywords"]:
            if kw.lower() in text:
                score += 1

        scores[cat] = score

    # best match select
    best_cat = max(scores, key=scores.get)

    # if nothing matched
    if scores[best_cat] == 0:
        return "default"

    return best_cat

def is_legal_or_ethical(user_input):

    text = user_input.lower()

    legal_words = [
        "law", "legal", "court", "judge", "case", "lawyer",
        "fraud", "murder", "theft", "crime", "ipc",
        "confidential", "ethics", "ethical", "client",
        "evidence", "justice", "bank", "hack"
    ]

    for word in legal_words:
        if word in text:
            return True

    return False

# ================= SMART PROS / CONS =================
def pick_unique(items, user_input, count=3):
    if not items:
        return []

    text = user_input.lower()
    scored = []

    for item in items:
        item_low = item.lower()
        score = 0

        # word match
        for w in text.split():
            if w in item_low:
                score += 2

        # legal boost
        boost_words = ["court", "fraud", "murder", "confidential", "lie", "hack", "bank", "case"]
        for w in boost_words:
            if w in text and w in item_low:
                score += 3
        scored.append((score, item))
    scored.sort(reverse=True)

    top = [x[1] for x in scored if x[0] > 0]

    if not top:
        top = items

    return random.sample(top, min(count, len(top)))

# ================= MAIN FUNCTION =================
def analyze_situation(user_input):
    if not is_legal_or_ethical(user_input):
     return "Invalid Situation", "⚠ This is not a legal or ethical problem."

    cat = detect_category(user_input)
    data = dataset[cat]

    pros = pick_unique(data.get("pros", []), user_input, 3)
    cons = pick_unique(data.get("cons", []), user_input, 3)

    risks, sections = get_risks(user_input)

    report = build_report(
        user_input,
        data["issue_name"],
        pros,
        cons,
        risks,
        sections
    )
    
    return data["issue_name"], report