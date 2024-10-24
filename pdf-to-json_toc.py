import fitz  # PyMuPDF
import json


def extract_toc_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    toc = doc.get_toc(simple=False)
    doc.close()

    memo = []
    count_ = 1
    for ind, item in enumerate(toc):
        level, title, page_num, dest = item
        # print(title)
        if title[0].isdigit():
            memo.append(title)
        elif title.startswith("Глава"):
            memo.append(str(f"{count_} ") + toc[ind + 1][1])
            count_ += 1
    return memo


def toc_to_json(toc_lines):
    def insert_entry(structure, number, title):
        if number.endswith("."):
            last_dot_index = number.rfind('.')
            number = number[:last_dot_index] + number[last_dot_index + 1:]
            levels = number.split('.')
            levels[-1] = levels[-1] + "."

        else:
            levels = number.split('.')

        current = structure
        for i, level in enumerate(levels):
            current = current.setdefault(".".join(levels[:i+1]), {})

            if i == 0:
                current["title"] = title
                current = current.setdefault("sections", {})

            if i == 1:
                current["title"] = title
                current = current.setdefault("subsections", {})
            elif i == 2:
                current["title"] = title
        # current["title"] = title

    json_structure = {}

    for line in reversed(toc_lines):
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        number = parts[0]

        title = parts[1].strip()
        insert_entry(json_structure, number, title)

    json_structure = dict(sorted(json_structure.items()))
    memo = dict()
    for i in range(1, 14):
        memo[str(i)] = json_structure[str(i)]

    return memo

def main():
    pdf_file_path = "Sample-for-chatbot.pdf"  # Replace with your PDF file path

    output_file = "toc_output.json"

    toc_lines = extract_toc_pdf(pdf_file_path)
    json_data = toc_to_json(toc_lines)

    # Save JSON to a file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    print(f"TOC saved to {output_file}")


if __name__ == "__main__":
    main()
