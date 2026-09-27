"""Assemble labeled review sheets from the native comparison and pose renders."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PREVIEWS = ROOT / 'previews'
PAPER = '#f3efe7'
CARD = '#faf8f2'
INK = '#39322e'
MUTED = '#756d63'
ACCENT = '#80644d'


def font(size, bold=False):
    choices = (
        f'/System/Library/Fonts/Supplemental/Arial{" Bold" if bold else ""}.ttf',
        f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf',
    )
    for name in choices:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default(size=size)


def label(sheet, xy, text, size=28, bold=False, fill=INK):
    ImageDraw.Draw(sheet).text(xy, text, font=font(size, bold), fill=fill)


def image_in(sheet, source, box, crop=False):
    im = Image.open(PREVIEWS / source).convert('RGBA')
    if crop:
        bounds = im.getchannel('A').getbbox()
        if bounds:
            im = ImageOps.expand(im.crop(bounds), border=22, fill=(0, 0, 0, 0))
    x, y, w, h = box
    im = ImageOps.contain(im, (w, h), Image.Resampling.LANCZOS)
    sheet.paste(im, (x + (w-im.width)//2, y + (h-im.height)//2), im)


def card(sheet, box):
    x, y, w, h = box
    ImageDraw.Draw(sheet).rounded_rectangle((x, y, x+w, y+h), radius=24, fill=CARD)


def header(sheet, title, subtitle):
    label(sheet, (54, 36), 'BISCUIT  /  MODEL STUDY', 21, True, ACCENT)
    label(sheet, (50, 76), title, 62, True)
    label(sheet, (54, 158), subtitle, 28, fill=MUTED)


def save(sheet, name):
    sheet.save(PREVIEWS / name, quality=94, subsampling=0)
    print(PREVIEWS / name)


def review():
    sheet = Image.new('RGB', (1800, 1230), PAPER)
    header(sheet, 'A little more Biscuit.',
           'Soft charcoal toe beans · four toes and one central pad on every paw')
    card(sheet, (50, 222, 900, 920))
    label(sheet, (82, 245), 'PAW UP', 23, True, ACCENT)
    image_in(sheet, 'comparison/after-paw-presented.png', (78, 294, 844, 800), crop=True)
    for name, title, y in [('front-sole', 'FRONT PAW', 222), ('hind-sole', 'HIND PAW', 696)]:
        card(sheet, (978, y, 772, 446))
        label(sheet, (1010, y+23), title, 23, True, ACCENT)
        image_in(sheet, f'comparison/after-{name}.png', (1000, y+64, 728, 360))
    label(sheet, (54, 1174), 'Current approved model · warm charcoal #493F3C · matte finish · existing rig and poses',
          24, fill=MUTED)
    save(sheet, 'toe-beans-review.jpg')


def comparison():
    sheet = Image.new('RGB', (1800, 2620), PAPER)
    header(sheet, 'From paw to toe beans.', 'Matched native renders · same pose, camera and lighting in each row')
    label(sheet, (86, 226), 'BEFORE / PREVIOUS MODEL', 25, True, MUTED)
    label(sheet, (978, 226), 'AFTER / APPROVED TOE BEANS', 25, True, ACCENT)
    rows = [('front-sole', 'Front paw'), ('hind-sole', 'Hind paw'),
            ('all-soles', 'All four soles'), ('paw-presented', 'Paw presented')]
    for index, (name, title) in enumerate(rows):
        y = 282 + index*568
        for version, x in [('before', 50), ('after', 944)]:
            card(sheet, (x, y, 806, 544))
            label(sheet, (x+30, y+21), title, 27, True)
            image_in(sheet, f'comparison/{version}-{name}.png', (x+24, y+69, 758, 453))
    label(sheet, (54, 2570), 'Sole details are enlarged for review. The toe bean model is the current approved standard.',
          23, fill=MUTED)
    save(sheet, 'comparison.jpg')


def poses():
    sheet = Image.new('RGB', (1800, 1510), PAPER)
    header(sheet, 'The familiar poses.', 'The same four rig-version-2 presets, now with pads attached to every paw')
    for index, (name, title) in enumerate([('standing', 'Standing'), ('sitting', 'Sitting'),
                                          ('lying', 'Lying down'), ('paw-raised', 'Paw raised')]):
        x, y = 50+(index%2)*894, 222+(index//2)*614
        card(sheet, (x, y, 806, 584))
        label(sheet, (x+30, y+21), title, 29, True)
        image_in(sheet, f'native/{name}.png', (x+32, y+78, 742, 478), crop=True)
    label(sheet, (54, 1462), 'Current approved model · softly sculpted geometry · 20 pads total', 24, fill=MUTED)
    save(sheet, 'pose-overview.jpg')


if __name__ == '__main__':
    review()
    comparison()
    poses()
