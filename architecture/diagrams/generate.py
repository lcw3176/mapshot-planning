"""맵샷 아키텍처 그림: 같은 좌표 스펙으로 draw.io(.drawio)와 미리보기용 SVG 를 만든다.

아이콘: simple-icons(브랜드, CC0) / @mdi/svg(일반 아이콘, Apache-2.0). 아이콘은 data URI 로 박아서
.drawio 파일 하나만 있으면 draw.io 에서 바로 열고 고칠 수 있다.

쓰는 아이콘은 icons/ 에 `si-이름.svg`, `mdi-이름.svg` 로 둔다. 처음엔 /tmp/icons 에 npm 패키지를 풀어
썼는데, /tmp 가 지워지면 다시 그릴 수 없어서 쓰는 것만 레포에 넣었다. 새 아이콘이 필요하면
simple-icons / @mdi/svg 에서 같은 이름 규칙으로 icons/ 에 추가한다.

실행: python3 generate.py <출력폴더>  →  .drawio 와 미리보기 .svg 생성. PNG 는 SVG 를 배율 2 로 캡처.
"""
import base64
import html
import json
import re
import sys
from pathlib import Path

ICONS = Path(__file__).resolve().parent / 'icons'

FONT = "Helvetica, 'Noto Sans CJK KR', 'Apple SD Gothic Neo', sans-serif"


def icon_svg(name, color):
    src, key = name.split(':')
    path = ICONS / f'{src}-{key}.svg'
    svg = path.read_text(encoding='utf-8')
    paths = re.findall(r'<path[^>]*d="([^"]+)"', svg)
    body = ''.join(f'<path d="{d}"/>' for d in paths)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#{color}">{body}</svg>'


def data_uri(svg):
    return 'data:image/svg+xml,' + base64.b64encode(svg.encode()).decode()


class Diagram:
    def __init__(self, name, w, h, title):
        self.name, self.w, self.h, self.title = name, w, h, title
        self.items = []

    def group(self, x, y, w, h, label, fill, stroke, icon=None, dashed=False, rounded=12):
        self.items.append(dict(t='group', x=x, y=y, w=w, h=h, label=label, fill=fill, stroke=stroke,
                               icon=icon, dashed=dashed, r=rounded))

    def box(self, x, y, w, h, title, lines, fill='ffffff', stroke='b0b7bd', icon=None):
        self.items.append(dict(t='box', x=x, y=y, w=w, h=h, title=title, lines=lines, fill=fill,
                               stroke=stroke, icon=icon))

    def icon(self, cx, y, icon, label, size=40):
        self.items.append(dict(t='icon', cx=cx, y=y, icon=icon, label=label, s=size))

    def edge(self, pts, label=None, dashed=False, label_at=0.5, label_dy=-8, color='4a5560', width=1.5):
        self.items.append(dict(t='edge', pts=pts, label=label, dashed=dashed, la=label_at, ldy=label_dy,
                               color=color, sw=width))

    def legend(self, x, y, entries):
        self.items.append(dict(t='legend', x=x, y=y, entries=entries))

    # ---------------- SVG ----------------
    def svg(self):
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
               f'viewBox="0 0 {self.w} {self.h}" font-family="{FONT}">',
               '<defs>' + ''.join(
                   f'<marker id="arr{c}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                   f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#{c}"/></marker>'
                   for c in {it.get('color', '4a5560') for it in self.items if it['t'] == 'edge'} | {'4a5560'}) + '</defs>',
               f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>',
               f'<text x="28" y="38" font-size="20" font-weight="700" fill="#1f2a33">{html.escape(self.title)}</text>']
        for it in self.items:
            if it['t'] == 'group':
                dash = ' stroke-dasharray="6 4"' if it['dashed'] else ''
                out.append(f'<rect x="{it["x"]}" y="{it["y"]}" width="{it["w"]}" height="{it["h"]}" rx="{it["r"]}" '
                           f'fill="#{it["fill"]}" stroke="#{it["stroke"]}" stroke-width="1.5"{dash}/>')
                tx = it['x'] + 14
                if it['icon']:
                    out.append(self._svg_icon(it['icon'], it['x'] + 12, it['y'] + 9, 20))
                    tx += 26
                out.append(f'<text x="{tx}" y="{it["y"] + 24}" font-size="14" font-weight="700" fill="#2b3640">'
                           f'{html.escape(it["label"])}</text>')
            elif it['t'] == 'box':
                out.append(f'<rect x="{it["x"]}" y="{it["y"]}" width="{it["w"]}" height="{it["h"]}" rx="8" '
                           f'fill="#{it["fill"]}" stroke="#{it["stroke"]}" stroke-width="1.2"/>')
                tx = it['x'] + 12
                if it['icon']:
                    out.append(self._svg_icon(it['icon'], it['x'] + 10, it['y'] + 9, 18))
                    tx += 24
                out.append(f'<text x="{tx}" y="{it["y"] + 23}" font-size="13" font-weight="700" fill="#1f2a33">'
                           f'{html.escape(it["title"])}</text>')
                for i, line in enumerate(it['lines']):
                    out.append(f'<text x="{it["x"] + 12}" y="{it["y"] + 44 + i * 18}" font-size="12" fill="#3b4650">'
                               f'{html.escape(line)}</text>')
            elif it['t'] == 'icon':
                s = it['s']
                out.append(self._svg_icon(it['icon'], it['cx'] - s / 2, it['y'], s))
                for i, line in enumerate(it['label'].split('\n')):
                    weight = '700' if i == 0 else '400'
                    color = '#1f2a33' if i == 0 else '#5a6670'
                    out.append(f'<text x="{it["cx"]}" y="{it["y"] + s + 17 + i * 16}" font-size="12" '
                               f'font-weight="{weight}" fill="{color}" text-anchor="middle">{html.escape(line)}</text>')
            elif it['t'] == 'edge':
                d = 'M' + ' L'.join(f'{x},{y}' for x, y in it['pts'])
                dash = ' stroke-dasharray="6 4"' if it['dashed'] else ''
                c = it['color']
                out.append(f'<path d="{d}" fill="none" stroke="#{c}" stroke-width="{it["sw"]}"{dash} '
                           f'stroke-linejoin="round" marker-end="url(#arr{c})"/>')
                if it['label']:
                    lx, ly = self._label_pos(it)
                    w = self._text_w(it['label']) + 10
                    out.append(f'<rect x="{lx - w / 2}" y="{ly - 12}" width="{w}" height="17" rx="3" fill="#ffffff"/>')
                    out.append(f'<text x="{lx}" y="{ly + 1}" font-size="11.5" fill="#{c if c != "4a5560" else "3b4650"}" '
                               f'font-weight="{700 if c != "4a5560" else 400}" text-anchor="middle">'
                               f'{html.escape(it["label"])}</text>')
            elif it['t'] == 'legend':
                yy = it['y']
                for color, text in it['entries']:
                    out.append(f'<line x1="{it["x"]}" y1="{yy}" x2="{it["x"] + 34}" y2="{yy}" stroke="#{color}" '
                               f'stroke-width="2.5" marker-end="url(#arr{color})"/>')
                    out.append(f'<text x="{it["x"] + 44}" y="{yy + 4}" font-size="12" fill="#2b3640">{html.escape(text)}</text>')
                    yy += 22
        out.append('</svg>')
        return '\n'.join(out)

    @staticmethod
    def _text_w(text):
        return sum(11.5 if ord(ch) > 0x2E80 else 6.6 for ch in text)

    @staticmethod
    def _label_pos(it):
        pts = it['pts']
        segs = list(zip(pts, pts[1:]))
        total = sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in segs)
        target = total * it['la']
        for a, b in segs:
            L = abs(b[0] - a[0]) + abs(b[1] - a[1])
            if target <= L:
                t = target / L if L else 0
                return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t + it['ldy']
            target -= L
        return pts[-1]

    @staticmethod
    def _svg_icon(icon, x, y, s):
        name, color = icon
        inner = icon_svg(name, color)
        inner = inner.replace('<svg xmlns="http://www.w3.org/2000/svg"',
                              f'<svg x="{x}" y="{y}" width="{s}" height="{s}"')
        return inner

    # ---------------- draw.io ----------------
    def drawio(self):
        cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
        n = [1]

        def nid():
            n[0] += 1
            return f'c{n[0]}'

        def esc(s):
            return html.escape(s, quote=True)

        def icon_cell(icon, x, y, s, label='', label_style=''):
            name, color = icon
            style = (f'shape=image;html=1;verticalAlign=top;verticalLabelPosition=bottom;labelBackgroundColor=none;'
                     f'imageAspect=0;aspect=fixed;image={data_uri(icon_svg(name, color))};fontSize=12;'
                     f'fontFamily=Helvetica;{label_style}')
            cells.append(f'<mxCell id="{nid()}" value="{esc(label)}" style="{style}" vertex="1" parent="1">'
                         f'<mxGeometry x="{x}" y="{y}" width="{s}" height="{s}" as="geometry"/></mxCell>')

        cells.append(f'<mxCell id="{nid()}" value="{esc(self.title)}" style="text;html=1;fontSize=20;fontStyle=1;'
                     f'fontFamily=Helvetica;align=left;verticalAlign=middle;" vertex="1" parent="1">'
                     f'<mxGeometry x="24" y="18" width="700" height="30" as="geometry"/></mxCell>')
        for it in self.items:
            if it['t'] == 'group':
                dash = 'dashed=1;dashPattern=6 4;' if it['dashed'] else ''
                pad = 40 if it['icon'] else 14
                style = (f'rounded=1;arcSize={it["r"] / min(it["w"], it["h"]) * 200:.1f};whiteSpace=wrap;html=1;'
                         f'fillColor=#{it["fill"]};strokeColor=#{it["stroke"]};strokeWidth=1.5;{dash}'
                         f'verticalAlign=top;align=left;spacingLeft={pad};spacingTop=4;fontSize=14;fontStyle=1;'
                         f'fontFamily=Helvetica;container=0;')
                cells.append(f'<mxCell id="{nid()}" value="{esc(it["label"])}" style="{style}" vertex="1" parent="1">'
                             f'<mxGeometry x="{it["x"]}" y="{it["y"]}" width="{it["w"]}" height="{it["h"]}" as="geometry"/></mxCell>')
                if it['icon']:
                    icon_cell(it['icon'], it['x'] + 12, it['y'] + 9, 20)
            elif it['t'] == 'box':
                body = '<br>'.join(esc(l) for l in it['lines'])
                pad = 34 if it['icon'] else 12
                value = (f'<div style="padding-left:{pad - 12}px"><b>{esc(it["title"])}</b></div>'
                         f'<div style="font-size:12px;color:#3b4650;margin-top:6px;line-height:1.5">{body}</div>')
                style = (f'rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#{it["fill"]};strokeColor=#{it["stroke"]};'
                         f'verticalAlign=top;align=left;spacingLeft=12;spacingTop=6;fontSize=13;fontFamily=Helvetica;')
                cells.append(f'<mxCell id="{nid()}" value="{esc(value)}" style="{style}" vertex="1" parent="1">'
                             f'<mxGeometry x="{it["x"]}" y="{it["y"]}" width="{it["w"]}" height="{it["h"]}" as="geometry"/></mxCell>')
                if it['icon']:
                    icon_cell(it['icon'], it['x'] + 10, it['y'] + 9, 18)
            elif it['t'] == 'icon':
                lines = it['label'].split('\n')
                label = f'<b>{esc(lines[0])}</b>' + ''.join(f'<br><font color="#5a6670">{esc(l)}</font>' for l in lines[1:])
                s = it['s']
                icon_cell(it['icon'], it['cx'] - s / 2, it['y'], s, label)
            elif it['t'] == 'edge':
                pts = it['pts']
                dash = 'dashed=1;' if it['dashed'] else ''
                style = (f'edgeStyle=none;html=1;rounded=0;endArrow=block;endFill=1;strokeColor=#{it["color"]};'
                         f'strokeWidth={it["sw"]};'
                         f'{dash}fontSize=11;fontFamily=Helvetica;labelBackgroundColor=#ffffff;')
                mids = ''.join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts[1:-1])
                arr = f'<Array as="points">{mids}</Array>' if mids else ''
                eid = nid()
                cells.append(f'<mxCell id="{eid}" value="" style="{style}" edge="1" parent="1">'
                             f'<mxGeometry relative="1" as="geometry">'
                             f'<mxPoint x="{pts[0][0]}" y="{pts[0][1]}" as="sourcePoint"/>'
                             f'<mxPoint x="{pts[-1][0]}" y="{pts[-1][1]}" as="targetPoint"/>{arr}'
                             f'</mxGeometry></mxCell>')
                if it['label']:
                    lx, ly = self._label_pos(it)
                    w = self._text_w(it['label']) + 14
                    bold = 'fontStyle=1;' if it['color'] != '4a5560' else ''
                    fc = it['color'] if it['color'] != '4a5560' else '3b4650'
                    cells.append(f'<mxCell id="{nid()}" value="{esc(it["label"])}" style="text;html=1;fontSize=11;'
                                 f'fontFamily=Helvetica;align=center;verticalAlign=middle;labelBackgroundColor=#ffffff;'
                                 f'{bold}fontColor=#{fc};" vertex="1" parent="1">'
                                 f'<mxGeometry x="{lx - w / 2}" y="{ly - 12}" width="{w}" height="18" as="geometry"/></mxCell>')
        for it in self.items:
            if it['t'] != 'legend':
                continue
            yy = it['y']
            for color, text in it['entries']:
                cells.append(f'<mxCell id="{nid()}" value="" style="endArrow=block;endFill=1;html=1;strokeColor=#{color};'
                             f'strokeWidth=2.5;" edge="1" parent="1"><mxGeometry relative="1" as="geometry">'
                             f'<mxPoint x="{it["x"]}" y="{yy}" as="sourcePoint"/><mxPoint x="{it["x"] + 34}" y="{yy}" '
                             f'as="targetPoint"/></mxGeometry></mxCell>')
                cells.append(f'<mxCell id="{nid()}" value="{esc(text)}" style="text;html=1;fontSize=12;fontFamily=Helvetica;'
                             f'align=left;verticalAlign=middle;" vertex="1" parent="1">'
                             f'<mxGeometry x="{it["x"] + 42}" y="{yy - 10}" width="320" height="20" as="geometry"/></mxCell>')
                yy += 22
        model = (f'<mxGraphModel dx="{self.w}" dy="{self.h}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
                 f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.w}" pageHeight="{self.h}" math="0" shadow="0">'
                 f'<root>{"".join(cells)}</root></mxGraphModel>')
        return (f'<mxfile host="app.diagrams.net"><diagram id="{self.name}" name="{esc(self.title)}">'
                f'{model}</diagram></mxfile>')


def front():
    d = Diagram('mapshot-front', 1240, 690, 'Mapshot-Front 구성 (2026-11)')
    d.icon(80, 352, ('mdi:account-group', '5a6670'), '사용자\n브라우저', 48)
    d.edge([(112, 376), (178, 376)], 'HTTPS')

    d.group(180, 70, 640, 600, 'Cloudflare Pages  (kmapshot.com)', 'fffaf4', 'F38020', ('si:cloudflarepages', 'F38020'), dashed=True)
    d.group(205, 112, 590, 368, 'Vue 3 SPA  (Vuetify 3, Pinia, Vue Router)', 'f1faf5', '4FC08D', ('si:vuedotjs', '4FC08D'))
    for cx, ic, lab in [(270, 'mdi:map-outline', '지도'), (380, 'mdi:newspaper-variant-outline', '도시뉴스'),
                        (490, 'mdi:bell-outline', '공지사항'), (600, 'mdi:file-document-outline', '사용법, FAQ'),
                        (715, 'mdi:email-outline', '문의')]:
        d.icon(cx, 152, (ic, '1867C0'), lab, 34)
    d.box(220, 228, 290, 96, '지도 화면 (MapView)', ['장소 검색, 지도 클릭으로 캡처 범위 지정',
                                                    '템플릿 제작 → 새 탭으로 템플릿 페이지',
                                                    '도시소식 레이어 (국토부 보도자료)'], icon=('mdi:map-outline', '1867C0'))
    d.box(220, 344, 560, 116, '상태 (Pinia 스토어)', ['map.js  지도·캡처 설정, localStorage 에 저장',
                                                    'pressMap.js  도시소식 데이터, 마커 묶음, 목록 필터',
                                                    'news.js, notice.js  도시뉴스·공지 조회 (axios)',
                                                    '빌드 환경변수: VUE_APP_API_URL, 점검 배너'], icon=('si:pinia', 'E5B700'))

    d.group(205, 500, 590, 150, '브라우저에서 바로 부르는 외부 스크립트', 'f6f7f8', 'a7b0b7')
    for cx, ic, lab in [(275, ('si:kakao', 'E6B800'), '카카오맵 SDK\n지도, 장소 검색\n주소 변환'),
                        (390, ('si:googleadsense', '4285F4'), '애드센스\n광고 3자리'),
                        (500, ('si:googleanalytics', 'E37400'), 'GA4, GTM\n방문 분석'),
                        (610, ('si:sentry', '362D59'), 'Sentry\n에러 수집'),
                        (722, ('mdi:email-fast-outline', '5a6670'), 'EmailJS\n문의 메일 발송')]:
        d.icon(cx, 540, ic, lab, 38)

    d.box(900, 150, 300, 132, '템플릿 페이지 (새 탭)', ['API 가 내려주는 HTML (Thymeleaf)',
                                                     '/map/naver | kakao | google | layer',
                                                     '지도 SDK 로 범위를 동적 렌더링'], icon=('mdi:window-open-variant', '1867C0'))
    d.box(900, 342, 300, 150, 'Mapshot-API', ['/news/recent, /news/{id}  도시뉴스',
                                              '/news/map  도시소식 지도',
                                              '/notice, /post  공지·게시글',
                                              '자세한 구성은 API 그림'], fill='f3f9ef', stroke='6DB33F', icon=('si:springboot', '6DB33F'))
    d.edge([(510, 276), (860, 276), (860, 216), (898, 216)], 'window.open', label_at=0.35)
    d.edge([(780, 402), (898, 402)], 'REST (axios)')
    d.edge([(1050, 342), (1050, 284)], '페이지 제공', dashed=True, label_dy=4)
    return d


def api():
    GREEN = '2E9E5B'
    d = Diagram('mapshot-api', 1300, 920, 'Mapshot-API 구성 (2026-11)')
    d.icon(110, 140, ('si:vuedotjs', '4FC08D'), 'Mapshot-Front\nkmapshot.com', 44)
    d.icon(110, 360, ('mdi:web', '1867C0'), '템플릿 페이지\n(사용자 브라우저)', 44)

    d.group(270, 70, 640, 650, '서버  (Docker Compose)', 'f4f9fe', '2496ED', ('si:docker', '2496ED'), dashed=True)
    d.group(310, 112, 575, 590, 'Spring Boot 3.2  (Java 17)', 'f3f9ef', '6DB33F', ('si:springboot', '6DB33F'))
    d.box(325, 152, 545, 74, 'REST 컨트롤러', ['NewsController  /news/recent, /news/{id}   PressMapController  /news/map',
                                              'Notice, Post Controller'])
    # /map/** 요청은 컨트롤러 전에 RateLimitInterceptor 를 먼저 지난다 (Mapshot-API:infra/rateLimit)
    d.box(325, 244, 170, 96, 'RateLimit', ['/map/** 에만 적용', 'bucket4j 전역 버킷 1개', '초과 시 거절'],
          fill='fdf0f2', stroke='E0607E')
    d.box(515, 244, 355, 96, 'MapTemplatesController', ['/map/{naver|kakao|google|layer}',
                                                       'Thymeleaf 템플릿 렌더',
                                                       '템플릿 JS 에 Lambda 주소(layerUrl) 포함'])
    d.edge([(495, 292), (513, 292)], color=GREEN, width=2)
    d.box(325, 358, 375, 110, 'application', ['NewsCollectService  도시뉴스 수집·요약',
                                              'PressCollectService  보도자료 수집·지역 추출',
                                              'PressMapService, RegionDictionary(시군구 281)',
                                              'Notice, Post Service'])
    d.box(715, 358, 155, 110, '스케줄러', ['도시뉴스  매일 11:00', '도시소식  매시 정각'],
          icon=('mdi:clock-outline', '5a6670'))
    d.box(325, 486, 545, 76, 'infra', ['GeminiClient(모델 페일오버), NaverNewsClient, MolitPressClient(Jsoup)',
                                      'PdfTextExtractor(PDFBox), SlackClient, LoggingFilter, CORS'])
    d.icon(597, 600, ('si:h2database', '09476B'), 'H2 파일 DB\ndomain(JPA), schema.sql', 44)
    d.edge([(597, 564), (597, 596)])

    d.group(950, 70, 320, 450, '서버가 부르는 외부', 'f6f7f8', 'a7b0b7')
    for cx, y, ic, lab in [(1035, 120, ('si:googlegemini', '8E75B2'), 'Gemini\n요약, 지역 추출'),
                           (1185, 120, ('si:naver', '03C75A'), '네이버 뉴스\n검색 API'),
                           (1035, 260, ('mdi:rss', 'E86A10'), '국토교통부\n보도자료 RSS, 상세, PDF'),
                           (1185, 260, ('mdi:slack', '4A154B'), 'Slack\n에러 알림'),
                           (1035, 400, ('si:sentry', '362D59'), 'Sentry\n에러 수집')]:
        d.icon(cx, y, ic, lab, 40)
    d.edge([(870, 500), (948, 500)], 'HTTPS', label_at=0.3)

    # Lambda 는 API 가 내려준 템플릿의 JS 가 부른다. 주소는 API 템플릿에 박혀 있고, 실제 요청은 브라우저에서 나간다.
    d.group(950, 545, 320, 125, 'AWS (ap-northeast-2)', 'fff8ee', 'FF9900')
    d.icon(1110, 592, ('mdi:aws', 'FF9900'), 'AWS Lambda\n도시계획 레이어 이미지', 36)
    d.edge([(870, 320), (928, 320), (928, 610), (1088, 610)], '③ 레이어 (템플릿 JS)', color=GREEN, width=2,
           dashed=True, label_at=0.83)

    d.edge([(134, 162), (300, 162), (300, 189), (323, 189)], 'REST', label_at=0.3)
    d.edge([(134, 382), (290, 382), (290, 292), (323, 292)], '② GET /map/*', color=GREEN, width=2, label_at=0.25)

    d.group(270, 760, 640, 140, '템플릿 페이지가 브라우저에서 직접 부르는 것', 'f6f7f8', 'a7b0b7')
    for cx, ic, lab in [(380, ('si:naver', '03C75A'), '네이버 지도 JS'), (520, ('si:kakao', 'E6B800'), '카카오맵 JS'),
                        (660, ('si:googlemaps', '4285F4'), '구글 지도 JS'),
                        (800, ('si:sentry', '362D59'), 'Sentry')]:
        d.icon(cx, 800, ic, lab, 36)
    d.edge([(110, 466), (110, 835), (268, 835)], '③ 지도 JS', color=GREEN, width=2, label_at=0.45)

    d.icon(1110, 690, ('si:githubactions', '2088FF'), 'GitHub Actions\n수동 실행, SSH 배포', 44)
    d.edge([(1086, 712), (912, 712)], 'docker-compose up')
    return d


def flow():
    GRAY, BLUE, GREEN, PURPLE, ORANGE = '7a8691', '1E6FD9', '2E9E5B', '8E5BB5', 'E07A1F'
    d = Diagram('mapshot-flow', 1500, 900, '맵샷 전체 요청 흐름 (2026-11)')
    d.legend(1000, 130, [(GRAY, '페이지 로드: 정적 파일'), (BLUE, '데이터 조회: 프론트 → API (REST)'),
                         (GREEN, '템플릿 제작: ① 새 탭 → ② RateLimit → HTML → ③ 지도 JS·Lambda 레이어'),
                         (PURPLE, '브라우저가 외부를 직접 호출 (SDK, 광고)'), (ORANGE, '서버 배치 수집')])

    d.group(30, 110, 440, 560, '사용자 브라우저', 'f7f9fb', '9aa5ae', ('mdi:account-group', '5a6670'))
    d.box(110, 155, 340, 150, 'kmapshot.com 탭  (Vue SPA)', ['지도, 도시뉴스, 공지사항 화면',
                                                           '도시소식 레이어 (pressMap 스토어)',
                                                           '지도 클릭으로 캡처 범위 지정',
                                                           '템플릿 제작 버튼'], icon=('si:vuedotjs', '4FC08D'))
    d.box(110, 440, 340, 150, '템플릿 탭  (/map/* 페이지)', ['API 가 내려준 HTML',
                                                          '지도 SDK 로 범위를 동적 렌더링',
                                                          '도시계획 레이어 이미지 겹치기',
                                                          '이 화면을 캡처해 템플릿으로 사용'], icon=('mdi:window-open-variant', '1867C0'))

    d.group(30, 700, 440, 160, '브라우저가 직접 부르는 외부', 'f6f7f8', 'a7b0b7')
    for cx, ic, lab in [(90, ('si:kakao', 'E6B800'), '카카오맵 SDK'), (190, ('si:naver', '03C75A'), '네이버 지도 JS'),
                        (290, ('si:googlemaps', '4285F4'), '구글 지도 JS'),
                        (400, ('si:googleadsense', '4285F4'), '애드센스, GA4\nSentry')]:
        d.icon(cx, 750, ic, lab, 34)

    d.box(560, 155, 330, 90, 'Cloudflare Pages', ['정적 파일 (HTML, JS, CSS)'], fill='fffaf4', stroke='F38020',
          icon=('si:cloudflarepages', 'F38020'))
    d.group(560, 300, 330, 560, 'Mapshot-API  (Spring Boot)', 'f3f9ef', '6DB33F', ('si:springboot', '6DB33F'))
    d.box(580, 345, 290, 95, 'REST API', ['/news/map  도시소식', '/news/recent, /news/{id}  도시뉴스',
                                           '/notice, /post  공지·게시글'])
    # /map/** 요청은 컨트롤러 전에 RateLimitInterceptor 를 먼저 지난다
    d.box(580, 458, 290, 40, 'RateLimit  /map/**  (bucket4j)', [], fill='fdf0f2', stroke='E0607E')
    d.box(580, 516, 290, 80, '템플릿 페이지  /map/*', ['Thymeleaf 로 좌표·옵션을 넣은 HTML',
                                                    '템플릿 JS 에 Lambda 주소 포함'])
    d.edge([(725, 498), (725, 514)], color=GREEN, width=2)
    d.box(580, 614, 290, 95, '스케줄러', ['도시뉴스  매일 11:00', '도시소식  매시 정각',
                                         '(RSS → 상세 → PDF 본문 → 지역 추출)'], icon=('mdi:clock-outline', '5a6670'))
    d.icon(725, 750, ('si:h2database', '09476B'), 'H2 파일 DB\nREST 조회, 수집 결과 저장', 40)
    d.edge([(725, 709), (725, 746)], '저장', label_dy=4)

    d.group(980, 300, 490, 560, 'API 쪽에서 부르는 외부', 'f6f7f8', 'a7b0b7')
    # Lambda 는 API 템플릿에 박힌 주소를 템플릿 JS 가 부른다(요청 자체는 브라우저에서 나감). 서버 배치와 구분해 초록 점선.
    for cx, y, ic, lab in [(1105, 340, ('mdi:aws', 'FF9900'), 'AWS Lambda\n도시계획 레이어 이미지'),
                           (1345, 340, ('mdi:rss', 'E86A10'), '국토교통부\n보도자료 RSS, 상세, PDF'),
                           (1105, 470, ('si:naver', '03C75A'), '네이버 뉴스\n검색 API'),
                           (1345, 470, ('si:googlegemini', '8E75B2'), 'Gemini\n요약, 지역 추출'),
                           (1105, 600, ('mdi:slack', '4A154B'), 'Slack\n에러 알림'),
                           (1345, 600, ('si:sentry', '362D59'), 'Sentry\n에러 수집')]:
        d.icon(cx, y, ic, lab, 40)

    d.edge([(450, 200), (558, 200)], '페이지 로드', color=GRAY, width=2)
    d.edge([(450, 280), (515, 280), (515, 392), (578, 392)], 'REST 조회', color=BLUE, width=2, label_at=0.15)
    d.edge([(280, 305), (280, 438)], '① window.open', color=GREEN, width=2)
    d.edge([(450, 478), (578, 478)], '② /map/* 요청', color=GREEN, width=2)
    d.edge([(220, 590), (220, 698)], '③ 지도 JS', color=GREEN, width=2)
    d.edge([(870, 556), (930, 556), (930, 360), (1083, 360)], '③ 레이어 (템플릿 JS)', color=GREEN, width=2,
           dashed=True, label_at=0.8)
    d.edge([(110, 230), (60, 230), (60, 698)], 'SDK, 광고', color=PURPLE, width=2, label_at=0.6)
    d.edge([(870, 662), (978, 662)], '매시 정각', color=ORANGE, width=2)
    return d


if __name__ == '__main__':
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for d in (flow(), front(), api()):
        (out / f'{d.name}.drawio').write_text(d.drawio(), encoding='utf-8')
        (out / f'{d.name}.svg').write_text(d.svg(), encoding='utf-8')
    print('ok')
