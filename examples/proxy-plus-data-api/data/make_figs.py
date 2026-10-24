"""生成博客图：数字全部从实测 CSV 和 IPFoxy 标价现算。"""
import csv, statistics as st, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figs")
rows = list(csv.DictReader(open(os.path.join(HERE, "amazon-page-weight-2026-10-24.csv"))))
def med(method):
    v = [int(r["transfer_bytes"]) for r in rows if r["method"].startswith(method) and r["real_page"] == "yes" and r["page_type"] == "product_page"]
    return st.median(v), min(v), max(v), len(v)
HTML = med("html_only"); NOMEDIA = med("headless_chrome_no_images_fonts"); FULL = med("headless_chrome_full")
TIERS = [("1GB", 5.99), ("10GB", 4.99), ("50GB", 3.99), ("100GB", 2.99), ("500GB", 2.39), ("1000GB", 1.99)]
API = 1.388889
THEME = {
  "light": dict(bg="#FFFFFF", text="#101214", muted="#50575D", axis="#8A9096", grid="#E9EBED", accent="#0A9E8E", s2="#3A4046", s3="#B4BABF", warn="#C2410C"),
  "dark": dict(bg="#101214", text="#F2F4F5", muted="#A7AFB5", axis="#8C959C", grid="#262B2F", accent="#0ACAB5", s2="#E3E7EA", s3="#5E676E", warn="#FB923C"),
}
FONT = "Inter, 'PingFang SC', 'Hiragino Sans GB', 'Noto Sans SC', 'Microsoft YaHei', 'Segoe UI', system-ui, sans-serif"
def t(x, y, s, c, size=12.5, anchor="start", weight=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" dominant-baseline="central" style="font-size:{size}px;font-family:{FONT};font-weight:{weight}" fill="{c}">{html.escape(s)}</text>'
def svg(w, h, label, body, c):
    return f'<svg role="img" aria-label="{html.escape(label)}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><rect width="{w}" height="{h}" fill="{c["bg"]}"/>{body}</svg>\n'
L = {
 "zh": dict(
   f1t="同一个 Amazon 商品页，三种抓法各下载多少字节", f1s="中位数，单位 MB（1 MB = 10⁶ 字节）；细线是最小值到最大值。2026-10-24 新加坡宽带直连实测",
   m1="只取 HTML（curl，gzip）", m2="无头 Chrome，屏蔽图片和字体", m3="无头 Chrome，整页加载", api="EveryInfra 商品详情 JSON（不走代理）",
   n=lambda n: f"n={n}",
   f2t="每 1000 个商品页的代理流量费，和数据接口对比", f2s="按 IPFoxy 动态住宅官网每 GB 标价（2026-10-24 读取），假设每页都一次成功",
   tier=lambda g, p: f"{g} 套餐 ${p}/GB", apiline=lambda v: f"EveryInfra 每千次 ${v:.2f}",
   f3t="只取 HTML 时，成功率要多高才比数据接口省钱", f3s="代理流量费 ÷ 成功率 = 接口每千次 $1.39 时的成功率；超过 100% 表示这一档怎么都不省",
   never="做不到", ),
 "en": dict(
   f1t="Bytes per Amazon product page, by fetch method", f1s="Median in MB (1 MB = 10⁶ bytes); thin line = min to max. Measured 2026-10-24 in Singapore, no proxy",
   m1="HTML only (curl, gzip)", m2="Headless Chrome, images and fonts blocked", m3="Headless Chrome, full page load", api="EveryInfra product JSON (no proxy)",
   n=lambda n: f"n={n}",
   f2t="Proxy traffic cost per 1,000 product pages vs. the data API", f2s="IPFoxy rotating residential list price per GB (read 2026-10-24); assumes every page succeeds on the first try",
   tier=lambda g, p: f"{g} plan, ${p}/GB", apiline=lambda v: f"EveryInfra: ${v:.2f} per 1,000 calls",
   f3t="HTML only: success rate needed to beat the data API", f3s="Traffic cost ÷ success rate = $1.39 per 1,000 calls. Above 100% means this plan never wins",
   never="never", ),
 "es": dict(
   f1t="Bytes por página de producto de Amazon, según el método", f1s="Mediana en MB (1 MB = 10⁶ bytes); línea fina: mín. a máx. Medido el 2026-10-24 en Singapur, sin proxy",
   m1="Solo HTML (curl, gzip)", m2="Chrome headless, sin imágenes ni fuentes", m3="Chrome headless, carga completa", api="JSON de producto de EveryInfra (sin proxy)",
   n=lambda n: f"n={n}",
   f2t="Costo de tráfico proxy por 1.000 páginas frente a la API de datos", f2s="Precio de lista por GB del proxy residencial rotativo de IPFoxy (consultado el 2026-10-24); supone éxito al primer intento",
   tier=lambda g, p: f"Plan {g}, ${p}/GB", apiline=lambda v: "EveryInfra: $" + f"{v:.2f}".replace(".", ",") + " por 1.000 llamadas",
   f3t="Solo HTML: tasa de éxito necesaria para costar menos que la API", f3s="Costo de tráfico ÷ tasa de éxito = $1,39 por 1.000 llamadas. Más de 100 % significa que ese plan nunca gana",
   never="nunca", ),
}
def money(v, lang):
    s = f"${v:.2f}"
    return s.replace(".", ",") if lang == "es" else s
def pct(v, lang):
    s = f"{v:.0f}%"
    return s.replace("%", " %") if lang == "es" else s
def mb(v, lang, d=2):
    s = f"{v:.{d}f}"
    return s.replace(".", ",") if lang == "es" else s

def fig1(lang, theme):
    c, l = THEME[theme], L[lang]; W, H = 760, 315; x0, x1 = 300, 600; maxv = 14.0
    sx = lambda v: x0 + (x1 - x0) * v / maxv
    b = [t(24, 26, l["f1t"], c["text"], 17, weight=600), t(24, 50, l["f1s"], c["muted"], 11.5)]
    for v in range(0, 15, 2):
        b.append(f'<path d="M{sx(v):.1f} 78V282" stroke="{c["grid"]}"/>'); b.append(t(sx(v), 296, mb(v, lang, 0), c["axis"], 11.5, "middle"))
    data = [(l["api"], 3569 / 1e6, None, None, None, c["s3"]), (l["m1"],) + tuple(x / 1e6 if i < 3 else x for i, x in enumerate(HTML)) + (c["accent"],),
            (l["m2"],) + tuple(x / 1e6 if i < 3 else x for i, x in enumerate(NOMEDIA)) + (c["s2"],), (l["m3"],) + tuple(x / 1e6 if i < 3 else x for i, x in enumerate(FULL)) + (c["s2"],)]
    for i, (name, m, lo, hi, n, col) in enumerate(data):
        y = 100 + i * 50
        b.append(t(x0 - 12, y, name, c["text"], 12.5, "end"))
        b.append(f'<rect x="{x0}" y="{y-11}" width="{max(sx(m)-x0, 2):.1f}" height="22" fill="{col}" rx="2"/>')
        if lo is not None:
            b.append(f'<path d="M{sx(lo):.1f} {y}H{sx(hi):.1f}" stroke="{c["axis"]}" stroke-width="1.5"/>')
            b.append(f'<path d="M{sx(lo):.1f} {y-6}V{y+6}M{sx(hi):.1f} {y-6}V{y+6}" stroke="{c["axis"]}" stroke-width="1.5"/>')
        label = f"{mb(m, lang, 3 if m < 1 else 2)} MB" + (f" · {l['n'](n)}" if n else "")
        b.append(t(max(sx(m), sx(hi or 0)) + 8, y, label, c["text"], 12.5, weight=600))
    b.append(f'<path d="M{x0} 78V282" stroke="{c["axis"]}"/>')
    return svg(W, H, l["f1t"], "".join(b), c)

def fig2(lang, theme):
    c, l = THEME[theme], L[lang]; W, H = 760, 350; x0, x1 = 300, 545; maxv = 50
    sx = lambda v: x0 + (x1 - x0) * v / maxv
    b = [t(24, 26, l["f2t"], c["text"], 17, weight=600), t(24, 50, l["f2s"], c["muted"], 11.5)]
    for v in range(0, 51, 10):
        b.append(f'<path d="M{sx(v):.1f} 78V318" stroke="{c["grid"]}"/>'); b.append(t(sx(v), 332, money(v, lang).replace(",00", "").replace(".00", ""), c["axis"], 11.5, "middle"))
    methods = [(l["m1"], HTML[0]), (l["m2"], NOMEDIA[0]), (l["m3"], FULL[0])]
    sel = [TIERS[0], TIERS[-1]]
    y = 96
    for name, bytes_ in methods:
        b.append(t(x0 - 12, y + 14, name, c["text"], 12.5, "end"))
        for j, (g, p) in enumerate(sel):
            v = bytes_ * 1000 / 1e9 * p; yy = y + j * 26
            col = c["s2"] if j == 0 else c["accent"]
            b.append(f'<rect x="{x0}" y="{yy}" width="{max(sx(v)-x0,2):.1f}" height="20" fill="{col}" rx="2"/>')
            b.append(t(sx(v) + 8, yy + 10, f"{money(v, lang)} · {l['tier'](g, p if lang != 'es' else str(p).replace('.', ','))}", c["text"], 11.5))
        y += 74
    ax = sx(API)
    b.append(f'<path d="M{ax:.1f} 78V318" stroke="{c["warn"]}" stroke-width="2" stroke-dasharray="5 4"/>')
    b.append(t(ax + 6, 70, l["apiline"](API), c["warn"], 12, weight=600))
    b.append(f'<path d="M{x0} 78V318" stroke="{c["axis"]}"/>')
    return svg(W, H, l["f2t"], "".join(b), c)

def fig3(lang, theme):
    c, l = THEME[theme], L[lang]; W, H = 760, 340; y0, y1 = 280, 90; x0 = 90; bw = 70; gap = 34; maxv = 200
    sy = lambda v: y0 - (y0 - y1) * min(v, maxv) / maxv
    b = [t(24, 26, l["f3t"], c["text"], 17, weight=600), t(24, 50, l["f3s"], c["muted"], 11.5)]
    for v in (0, 50, 100, 150, 200):
        b.append(f'<path d="M{x0-10} {sy(v):.1f}H{x0 + 6*(bw+gap)}" stroke="{c["grid"]}"/>'); b.append(t(x0 - 16, sy(v), pct(v, lang), c["axis"], 11.5, "end"))
    b.append(f'<path d="M{x0-10} {sy(100):.1f}H{x0 + 6*(bw+gap)}" stroke="{c["warn"]}" stroke-width="2" stroke-dasharray="5 4"/>')
    for i, (g, p) in enumerate(TIERS):
        need = HTML[0] * 1000 / 1e9 * p / API * 100; x = x0 + i * (bw + gap)
        col = c["s3"] if need > 100 else c["accent"]
        b.append(f'<rect x="{x}" y="{sy(need):.1f}" width="{bw}" height="{y0 - sy(need):.1f}" fill="{col}" rx="2"/>')
        lab = pct(need, lang) + (f" ({l['never']})" if need > 100 else "")
        b.append(t(x + bw / 2, sy(need) - 12, lab, c["text"], 12, "middle", 600))
        b.append(t(x + bw / 2, y0 + 16, g, c["text"], 12, "middle"))
        b.append(t(x + bw / 2, y0 + 34, f"${p}/GB".replace(".", ",") if lang == "es" else f"${p}/GB", c["muted"], 11.5, "middle"))
    b.append(f'<path d="M{x0-10} {y0}H{x0 + 6*(bw+gap)}" stroke="{c["axis"]}"/>')
    return svg(W, H, l["f3t"], "".join(b), c)

os.makedirs(OUT, exist_ok=True)
for lang in L:
    for theme in THEME:
        for name, fn in (("fig-01-page-bytes", fig1), ("fig-02-cost-per-1000", fig2), ("fig-03-breakeven-success", fig3)):
            open(os.path.join(OUT, f"{name}.{lang}.{theme}.svg"), "w").write(fn(lang, theme))
print("HTML", HTML, "NOMEDIA", NOMEDIA, "FULL", FULL)
