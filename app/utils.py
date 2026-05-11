import PyPDF2


# -------------------------
# EXTRACT TEXT FROM RESUME
# -------------------------
def extract_resume_text(pdf_file):

    reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


# -------------------------
# AI MATCH SCORE
# -------------------------
def match_score(resume_text, job_description):

    resume_words = set(
        resume_text.lower().split()
    )

    job_words = set(
        job_description.lower().split()
    )

    matched = resume_words.intersection(
        job_words
    )

    if len(job_words) == 0:
        return 0

    score = (
        len(matched) / len(job_words)
    ) * 100

    return round(score, 2)