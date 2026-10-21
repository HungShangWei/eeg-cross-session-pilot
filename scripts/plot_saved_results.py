#!/usr/bin/env python3
"""Render seven fixed saved summaries as four SVG/PNG pairs.

This is a display-only script, not an experiment or statistical estimator.
Input: results/primary_saved_results.csv, selected by exact record_id.
Thresholds: existing results/README.md, "Interpretation beside the numbers",
and docs/PILOT_METHODS_AND_LIMITATIONS.md, "Saved primary result and usefulness".
No research code, trial data, means, intervals, or tests are executed here.
Requires an already installed Pillow; no package installation is performed.
"""
import argparse
import csv
from decimal import Decimal
import hashlib
import io
import json
import math
from pathlib import Path
import platform
from xml.sax.saxutils import escape, quoteattr

from PIL import Image, ImageDraw, ImageFont, __version__ as pillow_version

WIDTH, HEIGHT, SCALE = 1600, 1200, 2
INK, MUTED, GRID, ACCENT = '#172b3a', '#465968', '#dce3e8', '#176579'
CSV_SHA256 = '29e4e3ab5eeeff2f2443b62395fdb7ffe90f2106febb4ed02b49fc7a96f9c341'
RECORD_IDS = ('T_minus_H_J', 'T_guard', 'H_guard', 'T_J', 'H_J', 'T_C', 'H_C')
INTERVAL_IDS = ('T_minus_H_J', 'T_J', 'H_J', 'T_C', 'H_C')
# Directly transcribed prespecified rules; these are not new estimates.
THRESHOLDS = {'non_inferiority_margin': Decimal('0.02'),
              'loss_upper_bound': Decimal('0.20'),
              'coverage_lower_bound': Decimal('0.50'),
              'required_people': Decimal('7')}
FONT_REGULAR = ('/System/Library/Fonts/Supplemental/Arial.ttf',
                '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf', 'Arial.ttf',
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVuSans.ttf')
FONT_BOLD = ('/System/Library/Fonts/Supplemental/Arial Bold.ttf',
             '/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf', 'Arial Bold.ttf',
             '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 'DejaVuSans-Bold.ttf')


def load_font(candidates, size):
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    raise RuntimeError('No supported font found; provide an installed Arial or DejaVu Sans font.')


class Scene:
    """A common numeric drawing scene for SVG and supersampled PNG."""
    def __init__(self, title, source_records):
        self.title = title
        self.source_records = source_records
        self.elements = []
        self.text_boxes = []
        self.font_family = load_font(FONT_REGULAR, 24).getname()[0]

    def text(self, x, y, text, size=24, bold=False, anchor='start', fill=INK, background=False):
        self.elements.append(('text', dict(x=x, y=y, text=text, size=size, bold=bold, anchor=anchor, fill=fill, background=background)))

    def multiline(self, x, y, lines, size=24, bold=False, anchor='start', fill=INK, gap=None, background=False):
        for i, line in enumerate(lines):
            self.text(x, y + i * (gap or size * 1.3), line, size, bold, anchor, fill, background)

    def line(self, x1, y1, x2, y2, fill=INK, width=2, dash=None):
        self.elements.append(('line', dict(x1=x1, y1=y1, x2=x2, y2=y2, fill=fill, width=width, dash=dash)))

    def rect(self, x, y, w, h, fill='white', stroke=INK, width=2):
        self.elements.append(('rect', dict(x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, width=width)))

    def marker(self, x, y, shape='circle', fill=ACCENT):
        self.elements.append(('marker', dict(x=x, y=y, shape=shape, fill=fill)))

    def render(self, destination, stem):
        image = Image.new('RGB', (WIDTH * SCALE, HEIGHT * SCALE), 'white')
        draw = ImageDraw.Draw(image)
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img">',
               '<title>' + escape(self.title) + '</title>',
               '<desc>' + escape('Visualization of saved summaries, not a new analysis. Source: results/primary_saved_results.csv. Exact source values: ' + json.dumps(self.source_records, separators=(',', ':'))) + '</desc>',
               '<rect width="1600" height="1200" fill="white"/>']
        def scaled(values):
            return tuple(float(v) * SCALE for v in values)
        for kind, e in self.elements:
            if kind == 'text':
                font = load_font(FONT_BOLD if e['bold'] else FONT_REGULAR, round(e['size'] * SCALE))
                anchor = {'start': 'ls', 'middle': 'ms', 'end': 'rs'}[e['anchor']]
                xy = scaled((e['x'], e['y']))
                box = draw.textbbox(xy, e['text'], font=font, anchor=anchor)
                box = tuple(v / SCALE for v in box)
                if box[0] < 0 or box[1] < 0 or box[2] > WIDTH or box[3] > HEIGHT:
                    raise ValueError('Text extends outside the figure: ' + e['text'])
                self.text_boxes.append({'text': e['text'], 'bbox': box})
                if e['background']:
                    pad = 6
                    draw.rectangle(scaled((box[0]-pad, box[1]-pad, box[2]+pad, box[3]+pad)), fill='white')
                    svg.append(f'<rect x="{box[0]-pad:.6f}" y="{box[1]-pad:.6f}" width="{box[2]-box[0]+2*pad:.6f}" height="{box[3]-box[1]+2*pad:.6f}" fill="white"/>')
                draw.text(xy, e['text'], font=font, fill=e['fill'], anchor=anchor)
                svg.append(f'<text x="{e["x"]:.6f}" y="{e["y"]:.6f}" font-family={quoteattr(self.font_family + ", Arial, sans-serif")} font-size="{e["size"]}" font-weight="{700 if e["bold"] else 400}" text-anchor="{e["anchor"]}" fill="{e["fill"]}">{escape(e["text"])}</text>')
            elif kind == 'line':
                coords = (e['x1'], e['y1'], e['x2'], e['y2'])
                if e['dash']:
                    dx, dy = e['x2'] - e['x1'], e['y2'] - e['y1']
                    length = math.hypot(dx, dy)
                    pos = 0
                    while pos < length:
                        end = min(pos + e['dash'][0], length)
                        draw.line(scaled((e['x1'] + dx * pos / length, e['y1'] + dy * pos / length,
                                          e['x1'] + dx * end / length, e['y1'] + dy * end / length)),
                                  fill=e['fill'], width=round(e['width'] * SCALE))
                        pos += sum(e['dash'])
                    dash = f' stroke-dasharray="{e["dash"][0]} {e["dash"][1]}"'
                else:
                    draw.line(scaled(coords), fill=e['fill'], width=round(e['width'] * SCALE))
                    dash = ''
                svg.append(f'<line x1="{e["x1"]:.6f}" y1="{e["y1"]:.6f}" x2="{e["x2"]:.6f}" y2="{e["y2"]:.6f}" stroke="{e["fill"]}" stroke-width="{e["width"]}"{dash}/>')
            elif kind == 'rect':
                draw.rectangle(scaled((e['x'], e['y'], e['x'] + e['w'], e['y'] + e['h'])), fill=e['fill'], outline=e['stroke'], width=round(e['width'] * SCALE))
                svg.append(f'<rect x="{e["x"]:.6f}" y="{e["y"]:.6f}" width="{e["w"]:.6f}" height="{e["h"]:.6f}" fill="{e["fill"]}" stroke="{e["stroke"]}" stroke-width="{e["width"]}"/>')
            else:
                x, y, radius = e['x'], e['y'], 9
                if e['shape'] == 'circle':
                    draw.ellipse(scaled((x-radius, y-radius, x+radius, y+radius)), fill=e['fill'], outline=INK, width=2*SCALE)
                    svg.append(f'<circle cx="{x:.6f}" cy="{y:.6f}" r="9" fill="{e["fill"]}" stroke="{INK}" stroke-width="2"/>')
                else:
                    draw.rectangle(scaled((x-radius, y-radius, x+radius, y+radius)), fill='white', outline=INK, width=3*SCALE)
                    svg.append(f'<rect x="{x-radius:.6f}" y="{y-radius:.6f}" width="18" height="18" fill="white" stroke="{INK}" stroke-width="3"/>')
        svg.append('</svg>')
        (destination / (stem + '.svg')).write_text('\n'.join(svg) + '\n', encoding='utf-8')
        image = image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        image.save(destination / (stem + '.png'), format='PNG', optimize=True)


def xmap(value, lower, upper, left, right):
    return left + float((Decimal(str(value)) - Decimal(str(lower))) /
                        (Decimal(str(upper)) - Decimal(str(lower)))) * (right-left)


def rounded(value, digits=4):
    return f'{Decimal(value):.{digits}f}'


def header(scene, number, title, subtitles):
    scene.text(80, 48, f'DREC01  /  SAVED PRIMARY RESULTS  /  FIGURE {number}', 20, True, fill=MUTED)
    scene.text(80, 107, title, 39, True)
    scene.multiline(80, 155, subtitles, 24, fill=MUTED, gap=34)


def footer(scene, label, caption_lines, records, outcome, rows):
    scene.line(80, 780, 1520, 780, GRID, 2)
    scene.text(80, 822, label, 24, True)
    scene.multiline(80, 860, caption_lines, 23, gap=32)
    scene.text(80, 972, 'Primary nominal budget 10 | Fixed prefix 40 | Deferral cost 0.25 | Acceptance probability ≥ 0.75', 22, fill=MUTED)
    scene.text(80, 1007, 'Independent n = 9 people; neural seeds were averaged within each person.', 22, fill=MUTED)
    scene.text(80, 1042, 'Actual labels received/used and the complete event chain remain incompletely verified.', 22, fill=MUTED)
    if outcome == 'C':
        definition = 'C = accepted / all evaluation opportunities; technical-invalid opportunities stay as deferrals.'
    else:
        definition = 'J = (accepted errors + 0.25 × deferrals) / all evaluation opportunities; technical-invalid counts as defer.'
    scene.text(80, 1080, definition, 21, fill=MUTED)
    if outcome == 'counts':
        scene.text(80, 1112, 'C = accepted / all evaluation opportunities, including technical-invalid deferrals.', 21, fill=MUTED)
    else:
        scene.text(80, 1112, 'Visualization of saved summaries, not a new analysis; no mean or interval was recalculated.', 21, fill=MUTED)
    scene.text(80, 1148, 'REVIEWED_WITH_UNRESOLVED_GAPS | publishable_as_pilot_results=false', 19, fill=MUTED)
    scene.text(80, 1180, 'Source: primary_saved_results.csv | record_id: ' + ', '.join(records), 18, fill=MUTED)


def axis(scene, lower, upper, ticks, left=480, right=1480, top=292, bottom=660, label=''):
    for value, text in ticks:
        x = xmap(value, lower, upper, left, right)
        scene.line(x, top, x, bottom, GRID, 1)
        scene.line(x, bottom, x, bottom+8, INK, 2)
        scene.text(x, bottom+38, text, 23, anchor='middle', fill=MUTED)
    scene.line(left, bottom, right, bottom, INK, 2)
    scene.text((left+right)/2, bottom+88, label, 24, anchor='middle')


def point_interval(scene, row, y, lower, upper, shape='circle', left=480, right=1480):
    values = {k: xmap(row[k], lower, upper, left, right) for k in ('estimate', 'interval_lower', 'interval_upper')}
    lo, hi = values['interval_lower'], values['interval_upper']
    scene.line(lo, y, hi, y, INK, 5)
    for x in (lo, hi):
        scene.line(x, y-14, x, y+14, INK, 3)
    scene.marker(values['estimate'], y, shape)
    return {'record_id': row['record_id'], 'source_values': {k: row[k] for k in values},
            'x_pixels': values, 'y_pixel': y, 'axis_range': [str(lower), str(upper)], 'axis_pixel_range': [left, right]}


def records_for(rows, ids):
    return [{k: rows[r][k] for k in ('record_id', 'estimate', 'interval_lower', 'interval_upper', 'interval_type')} for r in ids]


def build_figures(rows, destination):
    rendered = []
    ids = ['T_minus_H_J']
    scene = Scene('Saved proxy-loss difference: T minus H', records_for(rows, ids))
    header(scene, '01', 'Saved proxy-loss difference: T minus H', [
        'Scalar-temperature recalibration (T) minus regularized classification-head update (H)',
        'Point: saved mean difference. Line: ordinary two-sided 95% t interval.'])
    lower, upper, left, right = '-0.008', '0.024', 450, 1480
    axis(scene, lower, upper, [(str(x), str(x)) for x in ('-0.005', '0', '0.005', '0.010', '0.015', '0.020')],
         left=left, right=right, label='Proxy decision loss J difference (T minus H)')
    zero = xmap('0', lower, upper, left, right)
    margin = xmap(THRESHOLDS['non_inferiority_margin'], lower, upper, left, right)
    scene.line(zero, 292, zero, 660, MUTED, 2)
    scene.text(zero, 267, 'Zero difference', 23, anchor='middle')
    scene.line(margin, 292, margin, 660, INK, 3, (10, 7))
    scene.multiline(margin, 235, ['Non-inferiority', 'margin: 0.02'], 23, anchor='middle')
    scene.multiline(80, 428, ['Proxy loss J', 'T minus H'], 27, True)
    points = [point_interval(scene, rows[ids[0]], 432, lower, upper, left=left, right=right)]
    row = rows[ids[0]]
    scene.multiline(850, 518, ['Mean: ' + rounded(row['estimate'], 5),
        '95% t interval: [' + rounded(row['interval_lower'], 5) + ', ' + rounded(row['interval_upper'], 5) + ']'],
        25, anchor='middle', gap=36, background=True)
    footer(scene, 'NON-INFERIORITY COMPONENT ONLY', [
        'Supported at the saved-summary and prespecified-rule level.',
        'Not equivalence, superiority, or practical success.',
        'Negative values indicate lower proxy loss for T only.'], ids, 'J', rows)
    scene.render(destination, '01_saved_loss_difference')
    rendered.append({'stem': '01_saved_loss_difference', 'points': points, 'thresholds': {'zero': '0', 'non_inferiority_margin': '0.02'}, 'scene': scene})

    ids = ['T_guard', 'H_guard']
    scene = Scene('Participants meeting individual usefulness criteria', records_for(rows, ids))
    header(scene, '02', 'Participants meeting individual usefulness criteria', [
        'Saved counts for each method; no count interval was supplied and no error bars are added.'])
    left, right, top, bottom = 200, 1480, 270, 650
    for value in range(10):
        y = bottom - float(Decimal(value) / Decimal('9')) * (bottom-top)
        scene.line(left, y, right, y, GRID, 1)
        scene.text(left-22, y+8, str(value), 23, anchor='end', fill=MUTED)
    scene.line(left, top, left, bottom, INK, 2)
    scene.line(left, bottom, right, bottom, INK, 2)
    scene.text(left, 235, 'Number of participants (0–9)', 24)
    threshold_y = bottom - float(THRESHOLDS['required_people'] / Decimal('9')) * (bottom-top)
    scene.line(left, threshold_y, right, threshold_y, INK, 3, (10, 7))
    scene.text(right, threshold_y-18, 'Required: 7 of 9', 25, True, anchor='end')
    points = []
    for rid, center, color in [('T_guard', 600, ACCENT), ('H_guard', 1120, '#e7ecef')]:
        y = bottom - float(Decimal(rows[rid]['estimate']) / Decimal('9')) * (bottom-top)
        scene.rect(center-100, y, 200, bottom-y, fill=color, width=3)
        if rid == 'H_guard':
            for offset in range(22, int(bottom-y)-10, 28):
                scene.line(center-92, y+offset, center+92, y+offset, MUTED, 2)
        scene.text(center, y-23, rows[rid]['estimate'] + ' of ' + rows[rid]['n_independent'], 31, True, anchor='middle')
        label = ['Scalar-temperature', 'recalibration (T)'] if rid == 'T_guard' else ['Regularized classification-', 'head update (H)']
        scene.multiline(center, 697, label, 25, anchor='middle')
        points.append({'record_id': rid, 'source_value': rows[rid]['estimate'], 'bar_bottom_pixel': bottom,
                       'bar_top_pixel': y, 'count_axis': ['0', '9'], 'axis_pixel_range': [bottom, top], 'count_interval': 'NOT_PROVIDED'})
    footer(scene, 'REQUIRED PARTICIPANT COUNT NOT MET', [
        'Individual criteria: loss J ≤ 0.20 AND coverage C ≥ 0.50.',
        'Both methods fell short of the required count; group interval criteria also failed.',
        'These counts do not identify participants or establish overlap between methods.'], ids, 'counts', rows)
    scene.render(destination, '02_participant_usefulness')
    rendered.append({'stem': '02_participant_usefulness', 'points': points, 'thresholds': {'required_people': '7', 'individual_J_maximum_inclusive': '0.20', 'individual_C_minimum_inclusive': '0.50'}, 'scene': scene})

    for number, stem, metric, ids, upper, ticks in [
        ('03', '03_saved_decision_loss', 'J', ['T_J', 'H_J'], '0.32', [(x, x) for x in ('0', '0.05', '0.10', '0.15', '0.20', '0.25', '0.30')]),
        ('04', '04_saved_coverage', 'C', ['T_C', 'H_C'], '1', [(x, x) for x in ('0', '0.2', '0.4', '0.5', '0.6', '0.8', '1.0')])]:
        loss = metric == 'J'
        title = 'Saved decision loss: group criterion not met' if loss else 'Saved coverage: group criterion not met'
        scene = Scene(title, records_for(rows, ids))
        header(scene, number, title, ['Points: saved means. Lines: ordinary two-sided 95% t intervals.',
            'The prespecified group criterion concerns an interval endpoint, not the mean.'])
        axis(scene, '0', upper, ticks, label='Proxy decision loss J (dimensionless)' if loss else 'Coverage C (accepted share of all evaluation opportunities)')
        threshold = THRESHOLDS['loss_upper_bound' if loss else 'coverage_lower_bound']
        threshold_x = xmap(threshold, '0', upper, 480, 1480)
        scene.line(threshold_x, 292, threshold_x, 660, INK, 3, (10, 7))
        scene.text(threshold_x, 261, 'Boundary: ' + ('0.20' if loss else '0.50'), 24, True, anchor='middle')
        points = []
        for rid, y, shape, label in [(ids[0], 354, 'circle', ['Scalar-temperature', 'recalibration (T)']),
                                     (ids[1], 518, 'square', ['Regularized classification-', 'head update (H)'])]:
            scene.multiline(80, y-5, label, 26)
            points.append(point_interval(scene, rows[rid], y, '0', upper, shape))
            r = rows[rid]
            scene.text(980, y+63, 'Mean ' + rounded(r['estimate']) + '  |  95% t interval [' + rounded(r['interval_lower']) + ', ' + rounded(r['interval_upper']) + ']', 24, anchor='middle', background=True)
        if loss:
            footer(scene, 'REQUIRED: INTERVAL UPPER ENDPOINT STRICTLY BELOW 0.20', [
                'Both methods failed this criterion, although their means are below 0.20.',
                'Interval overlap is not used to infer a new difference test.',
                'J is an artificial decision proxy, not a human or clinical outcome.'], ids, metric, rows)
        else:
            footer(scene, 'REQUIRED: INTERVAL LOWER ENDPOINT STRICTLY ABOVE 0.50', [
                'Both methods failed this criterion, although their means are above 0.50.',
                'Coverage is acceptance share, not classification accuracy or human success.',
                'The original 0–1 scale is retained.'], ids, metric, rows)
        scene.render(destination, stem)
        rendered.append({'stem': stem, 'points': points, 'thresholds': {'bound': str(threshold), 'required_endpoint': 'upper' if loss else 'lower', 'strict_direction': '<' if loss else '>'}, 'scene': scene})
    for item in rendered:
        scene = item.pop('scene')
        item['font_family'] = scene.font_family
        item['text_bounds'] = scene.text_boxes
        item['outputs'] = []
        for extension in ('svg', 'png'):
            p = destination / (item['stem'] + '.' + extension)
            data = p.read_bytes()
            item['outputs'].append({'filename': p.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    return rendered


def main():
    public_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path, default=public_root / 'results/primary_saved_results.csv')
    parser.add_argument('--output-dir', type=Path, default=public_root / 'figures')
    args = parser.parse_args()
    data = args.csv.read_bytes()
    if hashlib.sha256(data).hexdigest() != CSV_SHA256 or len(data) != 7129:
        raise ValueError('Fixed saved CSV identity does not match. No figures generated.')
    all_rows = list(csv.DictReader(io.StringIO(data.decode('utf-8'))))
    rows = {r['record_id']: r for r in all_rows}
    if len(all_rows) != 7 or set(rows) != set(RECORD_IDS):
        raise ValueError('Expected exactly the seven fixed record_id values.')
    for rid, row in rows.items():
        for field, expected in [('n_independent', '9'), ('nominal_budget', '10'), ('target_prefix_trials', '40'),
                                ('deferral_cost', '0.25'), ('acceptance_probability', '0.75')]:
            if row[field] != expected:
                raise ValueError('Unexpected saved context: ' + field)
        if rid in INTERVAL_IDS:
            if row['interval_type'] != 'ordinary two-sided t' or row['confidence_level'] != '0.95':
                raise ValueError('Unexpected interval type.')
        elif row['interval_lower'] != 'NOT_PROVIDED' or row['interval_upper'] != 'NOT_PROVIDED':
            raise ValueError('No participant-count interval is expected.')
    if args.output_dir.is_symlink():
        raise ValueError('Output directory must not be a symbolic link.')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = build_figures(rows, args.output_dir)
    print(json.dumps({'scope': 'display of saved summaries only; no statistical recomputation',
        'source_csv_bytes': len(data), 'source_csv_sha256': CSV_SHA256,
        'python_version': platform.python_version(), 'pillow_version': pillow_version,
        'canvas_pixels': [WIDTH, HEIGHT], 'png_supersampling_scale': SCALE,
        'svg_renderer': 'Python standard library; same numeric scene as Pillow PNG',
        'source_records': records_for(rows, RECORD_IDS), 'figures': result}, indent=2))


if __name__ == '__main__':
    main()
