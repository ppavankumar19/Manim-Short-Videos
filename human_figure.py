"""A poseable human figure for lesson scenes.

Built from scene-unit "capsules" (rect + two end caps) rather than strokes,
so limb thickness scales with the figure instead of drifting with manim's
point-based stroke width. Every pose produces the *same* submobject
structure in the same order, which is what lets `Transform(man, man2)`
morph one pose into another instead of cross-fading.

Anatomy is laid out on a 1.7-unit-tall man (so one scene unit reads as one
metre in the heights-and-distances lesson): head is ~1/7.5 of height,
shoulders ~2 head-widths, leg ~48% of height.

Angles: 0 rad points straight down; positive rotates toward +x, so for a
figure `facing=RIGHT`, positive swings the limb forward. `look` tilts the
head about the neck (positive = looking up).
"""
from __future__ import annotations

import numpy as np
from manim import (
    VGroup, Circle, Rectangle, Polygon, Ellipse, Sector,
    ORIGIN, UP, DOWN, LEFT, RIGHT, PI,
)

SKIN = "#E9B489"
SHIRT = "#4F8EF7"
SHIRT_DARK = "#3466C4"
PANTS = "#2A3550"
HAIR = "#241812"
SHOE = "#12161F"


def _rot(vec, angle: float) -> np.ndarray:
    c, s = np.cos(angle), np.sin(angle)
    return np.array([c * vec[0] - s * vec[1], s * vec[0] + c * vec[1], 0.0])


def capsule(p1, p2, width: float, color: str, opacity: float = 1.0) -> VGroup:
    """A rounded bar between two points, sized in scene units."""
    p1 = np.asarray(p1, dtype=float)
    p2 = np.asarray(p2, dtype=float)
    v = p2 - p1
    length = max(float(np.linalg.norm(v)), 1e-3)
    mid = (p1 + p2) / 2
    rect = Rectangle(width=length, height=width, fill_color=color,
                     fill_opacity=opacity, stroke_width=0)
    rect.move_to(mid).rotate(float(np.arctan2(v[1], v[0])), about_point=mid)
    cap1 = Circle(radius=width / 2, fill_color=color, fill_opacity=opacity,
                  stroke_width=0).move_to(p1)
    cap2 = Circle(radius=width / 2, fill_color=color, fill_opacity=opacity,
                  stroke_width=0).move_to(p2)
    return VGroup(rect, cap1, cap2)


# Pose = joint angles in radians. Defaults are a relaxed standing pose.
STANDING = {
    "r_shoulder": 0.16, "r_elbow": 0.18,
    "l_shoulder": -0.14, "l_elbow": 0.10,
    "r_hip": 0.06, "r_knee": -0.02,
    "l_hip": -0.07, "l_knee": 0.03,
    "look": 0.0,
}

POINTING_UP = {
    **STANDING,
    "r_shoulder": 2.35, "r_elbow": -0.28,
    "l_shoulder": -0.20, "l_elbow": 0.18,
    "look": 0.42,
}

LOOKING_UP = {**STANDING, "look": 0.42}

WALK_A = {
    **STANDING,
    "r_hip": 0.42, "r_knee": -0.10,
    "l_hip": -0.38, "l_knee": 0.45,
    "r_shoulder": -0.40, "l_shoulder": 0.44,
}

WALK_B = {
    **STANDING,
    "r_hip": -0.38, "r_knee": 0.45,
    "l_hip": 0.42, "l_knee": -0.10,
    "r_shoulder": 0.44, "l_shoulder": -0.40,
}


class Man(VGroup):
    """A standing man, feet at `base`, built to `height` scene units."""

    def __init__(self, base=ORIGIN, height: float = 1.7, facing=RIGHT,
                 pose: dict | None = None, shirt: str = SHIRT,
                 pants: str = PANTS, skin: str = SKIN, shadow: bool = True,
                 **kwargs):
        super().__init__(**kwargs)
        p = {**STANDING, **(pose or {})}
        h = height
        self.height_units = h

        # --- skeleton landmarks (feet at origin, rebuilt per pose) --------
        hip_y, sho_y, neck_y = 0.50 * h, 0.805 * h, 0.838 * h
        hip_dx, sho_dx = 0.045 * h, 0.088 * h
        thigh, shin = 0.235 * h, 0.245 * h
        upper_arm, forearm = 0.175 * h, 0.165 * h
        head_r = 0.075 * h
        head_c = np.array([0.0, 0.918 * h, 0.0])

        arm_w, leg_w = 0.052 * h, 0.072 * h

        def leg(side_dx, hip_a, knee_a, color):
            hip = np.array([side_dx, hip_y, 0.0])
            knee = hip + thigh * _rot(DOWN, hip_a)
            ankle = knee + shin * _rot(DOWN, hip_a + knee_a)
            foot = Ellipse(width=0.145 * h, height=0.055 * h, fill_color=SHOE,
                           fill_opacity=1, stroke_width=0)
            foot.move_to(ankle + np.array([0.035 * h, -0.016 * h, 0.0]))
            return VGroup(capsule(hip, knee, leg_w, color),
                          capsule(knee, ankle, leg_w * 0.88, color), foot)

        def arm(side_dx, sho_a, elb_a, color):
            sho = np.array([side_dx, sho_y, 0.0])
            elbow = sho + upper_arm * _rot(DOWN, sho_a)
            wrist = elbow + forearm * _rot(DOWN, sho_a + elb_a)
            hand = Circle(radius=0.036 * h, fill_color=skin, fill_opacity=1,
                          stroke_width=0).move_to(wrist)
            return VGroup(capsule(sho, elbow, arm_w, color),
                          capsule(elbow, wrist, arm_w * 0.9, skin), hand)

        # torso: shoulders taper to waist and back out at the hips
        torso = Polygon(
            np.array([-sho_dx - 0.012 * h, sho_y + 0.03 * h, 0.0]),
            np.array([sho_dx + 0.012 * h, sho_y + 0.03 * h, 0.0]),
            np.array([sho_dx * 0.72, 0.63 * h, 0.0]),
            np.array([hip_dx + 0.022 * h, hip_y - 0.01 * h, 0.0]),
            np.array([-hip_dx - 0.022 * h, hip_y - 0.01 * h, 0.0]),
            np.array([-sho_dx * 0.72, 0.63 * h, 0.0]),
            fill_color=shirt, fill_opacity=1, stroke_width=0,
        ).round_corners(radius=0.028 * h)

        neck = capsule(np.array([0.0, sho_y - 0.005 * h, 0.0]),
                       np.array([0.0, neck_y + 0.02 * h, 0.0]), 0.055 * h, skin)

        # head group rotates about the neck for the "looking up" tilt
        skull = Circle(radius=head_r, fill_color=skin, fill_opacity=1,
                       stroke_width=0).move_to(head_c)
        # Sector is a pie slice about `arc_center`, so the flat edge sits on
        # the brow line and the curve caps the skull — drawn *after* the
        # skull or it disappears underneath it.
        hair = Sector(radius=head_r * 1.05, angle=PI * 1.16,
                      start_angle=-PI * 0.08, arc_center=head_c,
                      fill_color=HAIR, fill_opacity=1, stroke_width=0)
        nose = Polygon(
            head_c + np.array([head_r * 0.80, 0.010 * h, 0.0]),
            head_c + np.array([head_r * 1.22, -0.006 * h, 0.0]),
            head_c + np.array([head_r * 0.80, -0.022 * h, 0.0]),
            fill_color=skin, fill_opacity=1, stroke_width=0,
        )
        eye = Circle(radius=0.0090 * h, fill_color="#1B1B1B", fill_opacity=1,
                     stroke_width=0).move_to(
            head_c + np.array([head_r * 0.42, head_r * 0.10, 0.0]))
        head = VGroup(skull, nose, hair, eye)
        head.rotate(p["look"], about_point=np.array([0.0, neck_y, 0.0]))

        far_col = SHIRT_DARK if shirt == SHIRT else shirt
        parts = VGroup(
            leg(-hip_dx, p["l_hip"], p["l_knee"], pants),          # far leg
            arm(-sho_dx, p["l_shoulder"], p["l_elbow"], far_col),  # far arm
            torso, neck, head,
            leg(hip_dx, p["r_hip"], p["r_knee"], pants),           # near leg
            arm(sho_dx, p["r_shoulder"], p["r_elbow"], shirt),     # near arm
        )

        if facing[0] < 0:
            parts.flip(UP)

        ground_shadow = Ellipse(width=0.34 * h, height=0.055 * h,
                                fill_color="#000000", fill_opacity=0.28,
                                stroke_width=0).move_to(np.array([0.0, 0.012 * h, 0.0]))
        if shadow:
            self.add(ground_shadow)
        self.add(parts)
        self.shift(np.asarray(base, dtype=float))

        self.eye_level = 0.90 * h  # where the line of sight starts

    def eye_point(self) -> np.ndarray:
        """World-space point of the eye, for drawing the line of sight."""
        return self.get_bottom() + np.array([0.0, self.eye_level, 0.0])
