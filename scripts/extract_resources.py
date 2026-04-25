"""Extract main content from the 18 prevention/awareness column pages.

Reads Shift_JIS HTML from /tmp/edf_resources/, extracts the body content
between the second <DIV id=contents> and its closing tag, cleans up the HTML,
rewrites image paths, and writes UTF-8 JSON for Astro pages to consume.

Output: src/data/resources.json
"""
import json
import re
from pathlib import Path

SOURCE = Path("C:/Users/yuki/AppData/Local/Temp/edf_resources")
OUT = Path("C:/edforum-site/src/data/resources.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

# Slug -> (title, section)
PAGES = [
    ("column1", "はじめに", "diet", "正常体重でのダイエットの危険性"),
    ("diet1", "日本特有の若年女性痩せすぎ問題", "diet", "正常体重でのダイエットの危険性"),
    ("diet2", "すぐにはやってこない、痩せすぎの悪影響", "diet", "正常体重でのダイエットの危険性"),
    ("diet3", "若年からのカロリー制限の危険性", "diet", "正常体重でのダイエットの危険性"),
    ("diet4", "甘すぎる痩せすぎの基準", "diet", "正常体重でのダイエットの危険性"),
    ("diet5", "外圧頼りの現状", "diet", "正常体重でのダイエットの危険性"),
    ("diet6", "さいごに", "diet", "正常体重でのダイエットの危険性"),
    ("diet7", "文献", "diet", "正常体重でのダイエットの危険性"),
    ("model1", "痩せすぎファッションモデルの問題の背景とBMI", "model", "世界の痩せすぎモデル規制の経緯と日本"),
    ("model2", "痩せすぎファッションモデルの死亡", "model", "世界の痩せすぎモデル規制の経緯と日本"),
    ("model3", "欧米各国の痩せすぎモデル規制", "model", "世界の痩せすぎモデル規制の経緯と日本"),
    ("model4", "日本での現状", "model", "世界の痩せすぎモデル規制の経緯と日本"),
    ("model5", "文献", "model", "世界の痩せすぎモデル規制の経緯と日本"),
    ("media", "メディアからの影響で摂食障害が増えるのか", "media", "メディアからの影響は本当なのか"),
    ("media2", "痩せ礼賛のメディアの影響についての研究", "media", "メディアからの影響は本当なのか"),
    ("media3", "体型への不満と女性の心身の健康", "media", "メディアからの影響は本当なのか"),
    ("media4", "新しいメディアの影響", "media", "メディアからの影響は本当なのか"),
    ("column2", "摂食障害治療", "treatment", "摂食障害治療"),
]


def extract_body(html: str) -> str:
    """Extract the main content area.

    The structure varies across pages:
      - column1.html / column2.html: content is in <DIV id=contents> directly
      - diet*.html / model*.html / media*.html: content is in a SECOND <DIV id=contents>
        wrapped in <DIV align=center>
    We find the <H2> title and grab up to <!-- コンテンツ終わり --> or the next <DIV id=footer>.
    """
    # Find the LAST <H2> that introduces content (there may be navigation H2s before)
    # Strategy: find <DIV align=center>...<DIV id=contents..> if exists, otherwise
    # take the only <DIV id=contents>.

    # Try the wrapper pattern first (diet/model/media pages)
    m = re.search(
        r'<DIV align=center>\s*<DIV id=contents[^>]*>(.+?)</DIV>\s*</DIV>',
        html, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1)

    # Fallback: find the content div that contains H2 + body (column1/column2)
    # The first <DIV id=contents> often contains the head photo + content;
    # find the one that has a real H2 with our content.
    matches = list(re.finditer(
        r'<DIV id=contents[^>]*>(.*?)(?=<!-- メインコンテンツ終わり -->|<DIV id=menu>|<!-- メニュー -->)',
        html, re.DOTALL | re.IGNORECASE))
    if matches:
        # Take the first one that has substantial text (>200 chars after stripping tags)
        for m in matches:
            inner = m.group(1)
            text = re.sub(r'<[^>]+>', '', inner)
            text = re.sub(r'\s+', '', text)
            if len(text) > 100:
                return inner
        return matches[0].group(1)

    return ""


def clean_html(content: str) -> str:
    """Clean up the extracted HTML for use in Astro."""
    # Normalize whitespace within tags
    content = re.sub(r'\n+', '\n', content)

    # Remove navigation arrows (mae.gif/tugi.gif) since we'll add our own
    content = re.sub(
        r'<P[^>]*align=center[^>]*>\s*<A[^>]*href="[^"]+\.html"[^>]*>\s*<IMG[^>]*src="img/mae\.gif"[^>]*>\s*</A>.*?</P>',
        '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(
        r'<A[^>]*href="[^"]+\.html"[^>]*>\s*<IMG[^>]*src="img/(?:mae|tugi)\.gif"[^>]*>\s*</A>',
        '', content, flags=re.DOTALL | re.IGNORECASE)

    # Remove the line.gif decoration
    content = re.sub(
        r'<IMG[^>]*src="img/line\.gif"[^>]*>',
        '', content, flags=re.IGNORECASE)
    content = re.sub(
        r'<IMG[^>]*src="img/home\.png"[^>]*>',
        '', content, flags=re.IGNORECASE)

    # Rewrite image paths to local
    content = re.sub(
        r'src="img/([^"]+)"',
        r'src="/edforum-site/resources/\1"', content, flags=re.IGNORECASE)

    # Remove inline styles that lock dimensions (let CSS handle responsiveness)
    content = re.sub(r'\s+style="[^"]*"', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s+width="[0-9]+"', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s+height="[0-9]+"', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s+align="?[a-z]+"?', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s+border="?[0-9]+"?', '', content, flags=re.IGNORECASE)

    # Remove FONT tags but keep their content
    content = re.sub(r'<FONT[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'</FONT>', '', content, flags=re.IGNORECASE)

    # Lowercase known tags
    for tag in ['DIV', 'P', 'BR', 'IMG', 'STRONG', 'SUP', 'SUB', 'A', 'B', 'H1', 'H2', 'H3', 'TABLE', 'TR', 'TD', 'TH', 'UL', 'OL', 'LI']:
        content = re.sub(rf'<{tag}\b', f'<{tag.lower()}', content)
        content = re.sub(rf'</{tag}>', f'</{tag.lower()}>', content)

    # Internal page links (column1.html etc) should point to /resources/<slug>/
    content = re.sub(
        r'href="(column1|column2|diet[1-7]|model[1-5]|media|media[2-4])\.html"',
        r'href="/edforum-site/resources/\1/"', content)

    # Remove leading 全角 spaces from paragraphs (looks weird in modern layout)
    content = re.sub(r'<p>\s*[　　]+', '<p>', content)

    # Collapse multiple spaces
    content = re.sub(r' {2,}', ' ', content)

    # Strip trailing whitespace per line
    content = '\n'.join(line.rstrip() for line in content.split('\n'))

    return content.strip()


def main():
    pages = []
    for slug, title, section_slug, section_title in PAGES:
        html_path = SOURCE / f"{slug}.html"
        if not html_path.exists():
            print(f"[skip] {slug}: not found")
            continue
        raw = html_path.read_bytes().decode("shift_jis", errors="replace")
        body = extract_body(raw)
        cleaned = clean_html(body)
        pages.append({
            "slug": slug,
            "title": title,
            "section": section_slug,
            "sectionTitle": section_title,
            "html": cleaned,
        })
        print(f"[ok] {slug}: {len(cleaned)} chars")

    OUT.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {len(pages)} pages to {OUT}")


if __name__ == "__main__":
    main()
