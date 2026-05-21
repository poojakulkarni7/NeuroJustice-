import fitz

# ================= LOAD PDF =================
def extract_pdf_lines():
    text = ""
    pdfs = ["ipc.pdf", "bci.pdf"]

    for file in pdfs:
        try:
            doc = fitz.open(file)
            for page in doc:
                text += page.get_text("text") + "\n"
        except:
            pass

    return [l.strip() for l in text.split("\n") if len(l.strip()) > 5]

# ================= SMART MATCH ONLY (NO RULES) =================
def get_risks(user_input):
    lines = extract_pdf_lines()

    if not lines:
        return ["PDF not loaded"], []

    user_words = set(user_input.lower().split())

    matched_sections = []
    matched_risks = []

    for line in lines:
        low = line.lower()
        line_words = set(low.split())

        # 🔥 similarity score (NO HARD RULES)
        overlap = len(user_words.intersection(line_words))

        if overlap >= 2:   
            matched_sections.append(line)

            if any(x in low for x in ["imprison", "fine", "punishment", "liable"]):
                matched_risks.append(line)

    # fallback safety
    if not matched_sections:
        matched_sections = ["Relevant IPC/BCI sections will be determined based on facts"]

    if not matched_risks:
        matched_risks = ["Legal consequences depend on case severity"]

    return matched_risks[:5], matched_sections[:5]