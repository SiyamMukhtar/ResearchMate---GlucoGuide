from loader import load_pdf

pages = load_pdf("data/type2_diabetes_review.pdf")

print("Total pages:", len(pages))
print("---- Page 1 ke pehle 300 characters ----")
print(pages[0]["text"][:300])