import os
import math
from PIL import Image

class VisualInspector:
    """
    Engine 3: Visual & Accessibility Inspector
    Extracts dominant color palettes from graphics, calculates WCAG 2.1 AA/AAA
    relative luminance contrast ratios, and evaluates text inside images.
    """

    DEFAULT_APPROVED_PALETTES = [
        {"name": "Deep Navy", "hex": "#0F172A", "rgb": (15, 23, 42)},
        {"name": "Electric Blue", "hex": "#2563EB", "rgb": (37, 99, 235)},
        {"name": "Sky Cyan", "hex": "#0EA5E9", "rgb": (14, 165, 233)},
        {"name": "Slate Dark", "hex": "#1E293B", "rgb": (30, 41, 59)},
        {"name": "Off-White", "hex": "#F8FAFC", "rgb": (248, 250, 252)},
        {"name": "Pure White", "hex": "#FFFFFF", "rgb": (255, 255, 255)},
        {"name": "Emerald Green", "hex": "#10B981", "rgb": (16, 185, 129)},
        {"name": "Amber Warning", "hex": "#F59E0B", "rgb": (245, 158, 11)}
    ]

    def __init__(self, brand_assets=None):
        self.approved_palette = []
        if brand_assets:
            for a in brand_assets:
                if a.asset_type == 'PALETTE' and a.asset_value.startswith('#'):
                    h = a.asset_value.lstrip('#')
                    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                    self.approved_palette.append({"name": a.name, "hex": a.asset_value.upper(), "rgb": rgb})
        
        if not self.approved_palette:
            self.approved_palette = self.DEFAULT_APPROVED_PALETTES

    @staticmethod
    def hex_to_rgb(hex_str):
        h = hex_str.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hex(rgb):
        return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

    @staticmethod
    def calculate_relative_luminance(rgb):
        """Calculates WCAG relative luminance according to sRGB formula."""
        def channel_lum(val):
            c = val / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        r, g, b = rgb[0], rgb[1], rgb[2]
        return 0.2126 * channel_lum(r) + 0.7152 * channel_lum(g) + 0.0722 * channel_lum(b)

    @classmethod
    def calculate_contrast_ratio(cls, rgb1, rgb2):
        """Calculates WCAG 2.1 contrast ratio: (L1 + 0.05) / (L2 + 0.05). Accepts RGB tuples or hex strings."""
        if isinstance(rgb1, str):
            rgb1 = cls.hex_to_rgb(rgb1)
        if isinstance(rgb2, str):
            rgb2 = cls.hex_to_rgb(rgb2)
        lum1 = cls.calculate_relative_luminance(rgb1)
        lum2 = cls.calculate_relative_luminance(rgb2)
        l_max = max(lum1, lum2)
        l_min = min(lum1, lum2)
        return round((l_max + 0.05) / (l_min + 0.05), 2)

    def extract_dominant_colors(self, image_path, num_colors=5):
        """Extracts dominant colors from an image using Pillow quantization."""
        try:
            img = Image.open(image_path).convert('RGB')
            # Resize for fast processing
            img = img.resize((150, 150))
            # Quantize to reduce to top colors
            quantized = img.quantize(colors=num_colors)
            palette = quantized.getpalette()[:num_colors * 3]
            colors = []
            for i in range(num_colors):
                rgb = (palette[i*3], palette[i*3+1], palette[i*3+2])
                colors.append({
                    'hex': self.rgb_to_hex(rgb),
                    'rgb': rgb
                })
            return colors
        except Exception as e:
            return []

    def evaluate_image(self, image_path):
        """
        Evaluates an image for palette conformity, contrast, and OCR text.
        Performs pairwise contrast checks across ALL dominant color pairs,
        flagging any combination with ratio < 4.5:1.
        """
        flags = []
        dominant_colors = self.extract_dominant_colors(image_path)
        
        # 1. Palette Conformity Check
        unapproved_colors = []
        for dom in dominant_colors:
            # Check Euclidean color distance to closest approved palette
            min_dist = float('inf')
            closest_token = None
            for app in self.approved_palette:
                dist = math.sqrt(
                    (dom['rgb'][0] - app['rgb'][0])**2 +
                    (dom['rgb'][1] - app['rgb'][1])**2 +
                    (dom['rgb'][2] - app['rgb'][2])**2
                )
                if dist < min_dist:
                    min_dist = dist
                    closest_token = app
            
            # If color is more than threshold distance away from any approved color
            if min_dist > 55:  # Tolerance threshold
                unapproved_colors.append((dom['hex'], closest_token['hex']))
        
        if unapproved_colors:
            for unapp_hex, rec_hex in unapproved_colors[:3]:
                flags.append({
                    'flag_type': 'VISUAL',
                    'snippet': f"Color Token {unapp_hex}",
                    'severity': 'WARNING',
                    'explanation': f"Off-Brand Visual Color: Hex code {unapp_hex} is not in the approved brand palette.",
                    'suggested_fix': f"Replace with approved brand token {rec_hex}",
                    'rule_code': 'BG-VIS-01',
                    'citation': 'Brand Design System § 1.3 (Approved Color Tokens)'
                })

        # 2. Pairwise Contrast Analysis — check ALL pairs of dominant colors
        if len(dominant_colors) >= 2:
            seen_pairs = set()
            for i in range(len(dominant_colors)):
                for j in range(i + 1, len(dominant_colors)):
                    c1 = dominant_colors[i]
                    c2 = dominant_colors[j]
                    pair_key = tuple(sorted([c1['hex'], c2['hex']]))
                    if pair_key in seen_pairs:
                        continue
                    seen_pairs.add(pair_key)

                    ratio = self.calculate_contrast_ratio(c1['rgb'], c2['rgb'])
                    if ratio < 4.5:
                        flags.append({
                            'flag_type': 'ACCESSIBILITY',
                            'snippet': f"Contrast Ratio {ratio}:1 ({c1['hex']} vs {c2['hex']})",
                            'severity': 'CRITICAL',
                            'explanation': (
                                f"WCAG 2.1 Contrast Violation: Color pair {c1['hex']} and {c2['hex']} "
                                f"has a contrast ratio of {ratio}:1, below the mandatory 4.5:1 AA threshold."
                            ),
                            'suggested_fix': (
                                "Adjust one or both colors to achieve at least 4.5:1 contrast ratio. "
                                f"Consider darkening {c1['hex']} or lightening {c2['hex']}."
                            ),
                            'rule_code': 'BG-ACC-01',
                            'citation': 'WCAG 2.1 Level AA / ADA Title III Accessibility Requirement'
                        })

        # 3. Text OCR inside graphic
        extracted_text = ""
        try:
            import pytesseract
            img = Image.open(image_path)
            extracted_text = pytesseract.image_to_string(img).strip()
        except Exception:
            # Graceful fallback if tesseract binary is not installed in local OS path
            extracted_text = ""

        deductions = sum(25 if f['severity'] == 'CRITICAL' else 10 for f in flags)
        score = max(20, 100 - deductions)

        return {
            'score': score,
            'flags': flags,
            'dominant_colors': dominant_colors,
            'extracted_text': extracted_text
        }

    def generate_accessibility_report(self, image_path):
        """
        Generates a high-level accessibility report for the image.
        Returns a dict with keys: wcag_level, dominant_issue, fixes.
        """
        result = self.evaluate_image(image_path)
        flags = result['flags']
        score = result['score']
        dominant_colors = result.get('dominant_colors', [])

        # Determine WCAG compliance level
        critical_acc_flags = [f for f in flags if f['flag_type'] == 'ACCESSIBILITY' and f['severity'] == 'CRITICAL']
        if not critical_acc_flags:
            wcag_level = "AA_PASS"
        elif score >= 60:
            wcag_level = "AA_PARTIAL"
        else:
            wcag_level = "AA_FAIL"

        # Dominant issue
        if critical_acc_flags:
            dominant_issue = critical_acc_flags[0]['explanation']
        elif flags:
            dominant_issue = flags[0]['explanation']
        else:
            dominant_issue = "No accessibility issues detected. Image appears WCAG 2.1 AA compliant."

        # Actionable fixes
        fixes = []
        if critical_acc_flags:
            fixes.append(
                f"Resolve {len(critical_acc_flags)} contrast violation(s): "
                "Ensure all color pairs have at least 4.5:1 contrast ratio for normal text."
            )
        visual_flags = [f for f in flags if f['flag_type'] == 'VISUAL']
        if visual_flags:
            fixes.append(
                f"Replace {len(visual_flags)} off-brand color(s) with approved palette tokens "
                "to maintain visual consistency and accessibility."
            )
        if not fixes:
            fixes.append("No immediate fixes required. Continue monitoring with each new asset version.")
        fixes.append(
            "Use the WebAIM Contrast Checker (webaim.org/resources/contrastchecker) to verify "
            "text-on-background combinations before final export."
        )

        return {
            "wcag_level": wcag_level,
            "dominant_issue": dominant_issue,
            "fixes": fixes,
            "score": score,
            "critical_contrast_violations": len(critical_acc_flags),
            "dominant_colors": [c['hex'] for c in dominant_colors]
        }
