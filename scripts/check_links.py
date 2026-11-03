#!/usr/bin/env python3
"""檢查網站本地連結與錨點。只用 Python 標準函式庫，不需額外安裝套件。

原因：這個網站沒有建置流程，因此需要一個能一鍵發現 404 路徑的簡單檢查。
"""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            self.ids.add(element_id)
        if tag == "a" and attributes.get("name"):
            self.ids.add(attributes["name"])
        # 同時檢查頁面導覽、圖片、JS、CSS 與 favicon，避免只檢查超連結。
        attribute = "src" if tag in {"img", "script", "iframe"} else "href" if tag in {"a", "link"} else None
        if attribute and attributes.get(attribute):
            self.links.append((self.getpos()[0], attributes[attribute]))


def main():
    files = sorted(ROOT.rglob("*.html"))
    pages = {}
    for source in files:
        parser = PageParser()
        parser.feed(source.read_text(encoding="utf-8"))
        pages[source.resolve()] = parser

    problems = []

    for source, page in pages.items():
        for lineno, link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme in {"https", "http", "mailto", "tel", "data"} or parsed.netloc:
                continue

            name = source.relative_to(ROOT).as_posix()
            if parsed.scheme:
                problems.append(f"{name}:{lineno} 不支援的連結協定：{link}")
                continue

            # 原因：以 / 開頭的路徑在 GitHub Pages 專案子路徑會指錯位置。
            if parsed.path.startswith("/"):
                problems.append(f"{name}:{lineno} 請改成相對路徑：{link}")
                continue

            path = unquote(parsed.path)
            target = (source.parent / path).resolve() if path else source
            if not target.is_relative_to(ROOT):
                problems.append(f"{name}:{lineno} 連結超出網站資料夾：{link}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                problems.append(f"{name}:{lineno} 找不到檔案：{link}")
                continue

            # 原因：存在的 HTML 檔仍可能連到不存在的 #區塊。
            fragment = unquote(parsed.fragment)
            if fragment and target.suffix.lower() == ".html":
                target_page = pages.get(target)
                if target_page and fragment not in target_page.ids:
                    problems.append(f"{name}:{lineno} 找不到頁面錨點：{link}")

    if problems:
        print("網站連結檢查發現問題：")
        for problem in problems:
            print(" -", problem)
        return 1

    print(f"檢查通過：{len(files)} 個 HTML 頁面的本地連結與錨點均有效。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
