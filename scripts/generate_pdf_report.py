import os
from fpdf import FPDF
from pathlib import Path

def generate_pdf():
    # 경로 설정
    artifact_dir = Path(r"C:\Users\정영훈\.gemini\antigravity\brain\3ca89c6c-f77f-4f0e-9934-b69485aaffef")
    md_path = artifact_dir / "walkthrough.md"
    pdf_path = artifact_dir / "walkthrough.pdf"
    
    if not md_path.exists():
        print(f"Error: {md_path} not found.")
        return

    # PDF 설정
    from fpdf.enums import XPos, YPos
    
    pdf = FPDF()
    pdf.add_page()
    
    # 한글 폰트 등록
    pdf.add_font("Malgun", "", r"C:\Windows\Fonts\malgun.ttf")
    pdf.add_font("MalgunBold", "", r"C:\Windows\Fonts\malgunbd.ttf")
    
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip("\n")
        
        # Indentation handling
        indent = 0
        if line.startswith("    "):
            indent = 10
            line = line.strip()
        else:
            line = line.strip()

        if not line:
            pdf.ln(5)
            continue

        pdf.set_x(10 + indent)
        width = 190 - indent # A4 width (210) - margin (10*2) - indent

        if line.startswith("# "):
            pdf.set_font("MalgunBold", size=20)
            pdf.multi_cell(width, 15, line[2:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(5)
        elif line.startswith("## "):
            pdf.set_font("MalgunBold", size=16)
            pdf.multi_cell(width, 12, line[3:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(3)
        elif line.startswith("### "):
            pdf.set_font("MalgunBold", size=13)
            pdf.multi_cell(width, 10, line[4:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)
        elif line.startswith("- "):
            pdf.set_font("Malgun", size=11)
            pdf.multi_cell(width, 8, f"• {line[2:]}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        elif line == "---":
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)
        else:
            pdf.set_font("Malgun", size=11)
            pdf.multi_cell(width, 8, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(str(pdf_path))
    print(f"PDF 생성 완료: {pdf_path}")

if __name__ == "__main__":
    generate_pdf()
