"""
Introduction to Division - Manim Animation
Full self-contained script with explanations and narrated voiceover.
Low-quality render (480p) for quick testing

Voice: en-IN-PrabhatNeural via speech_service.get_speech_service() (see
speech_service.py). Video-first sync: every self.play/self.wait duration
below is unchanged from the original silent cut; only the narration text
and its per-section edge-tts rate were tuned (via tts_tune.py) to fit those
fixed durations, never the other way round.
"""

from manim import *
from manim_voiceover import VoiceoverScene

from speech_service import get_speech_service

# Narration per section, paired with the edge-tts rate tuned (via
# tts_tune.tune_rate) so spoken duration matches that section's existing
# animation length. Keep new rates within a similar band if you edit text.
NARRATION = {
    "title": "Let us discuss division. It just means sharing things fairly!",
    "scenario": (
        "Here are twelve cookies, and here are four friends. How many "
        "cookies does each friend get, if we share them equally?"
    ),
    "grouping": (
        "Let us share them out. One cookie to each friend, again, and "
        "again. Now every group has three cookies."
    ),
    "symbol": (
        "We write this using a symbol. Twelve divided by four equals "
        "three. Twelve is the dividend, the total amount. Four is the "
        "divisor, the number of groups. And three is the quotient, how "
        "many each group gets."
    ),
    "practice": (
        "Now you try. Fifteen divided by five equals what? Count them "
        "out in five equal groups. Three dots in each group. So the "
        "answer is three!"
    ),
    "conclusion": (
        "And that is division. It means sharing fairly, so everyone "
        "gets the same amount. Thanks for learning with me!"
    ),
}

# Tuned edge-tts rate per section (tts_tune.py), so each NARRATION entry
# fits its section's fixed animation duration without changing the rule's
# calm-pace band by too much in any one beat.
BEAT_RATE = {
    "title": "+21%",
    "scenario": "+39%",
    "grouping": "+9%",
    "symbol": "+38%",
    "practice": "+32%",
    "conclusion": "+39%",
}


class IntroductionToDivision(VoiceoverScene):
    """
    A complete introduction to division concept using:
    1. Real-world example (sharing cookies)
    2. Visual grouping
    3. Symbol introduction
    4. Practice problem
    """
    def construct(self):
        # --- SECTION 1: Title Slide ---
        self.set_speech_service(
            get_speech_service(rate=BEAT_RATE["title"]), create_subcaption=True
        )
        title = Text("Introduction to Division", font_size=48, color=BLUE)
        subtitle = Text("Making Sharing Fair!", font_size=32, color=YELLOW)
        subtitle.next_to(title, DOWN)

        with self.voiceover(text=NARRATION["title"]):
            self.play(Write(title))
            self.wait(0.5)
            self.play(FadeIn(subtitle, shift=UP))
            self.wait(1)
            self.play(FadeOut(title), FadeOut(subtitle))
            self.wait(0.3)

        # --- SECTION 2: Real-World Scenario ---
        self.set_speech_service(
            get_speech_service(rate=BEAT_RATE["scenario"]), create_subcaption=True
        )
        # Show 12 cookies
        cookies = VGroup(*[
            Circle(radius=0.3, color=ORANGE, fill_opacity=0.8).shift(
                RIGHT * (i % 4 - 1.5) + UP * (1 - i // 4 * 0.8)
            ) for i in range(12)
        ])
        cookies_text = Text("12 Cookies", font_size=28, color=ORANGE)
        cookies_text.next_to(cookies, DOWN, buff=0.5)

        # Show 4 friends
        friends = VGroup(*[
            Circle(radius=0.4, color=GREEN, fill_opacity=0.5).shift(
                RIGHT * (i - 1.5) * 1.8 + DOWN * 1.5
            ) for i in range(4)
        ])
        friends_text = Text("4 Friends", font_size=28, color=GREEN)
        friends_text.next_to(friends, DOWN, buff=0.3)

        question = Text("How many cookies does each friend get?", font_size=30, color=WHITE)
        question.next_to(friends, DOWN, buff=1.2)

        with self.voiceover(text=NARRATION["scenario"]):
            # Animate scene
            self.play(FadeIn(cookies), Write(cookies_text))
            self.wait(0.5)
            self.play(FadeIn(friends), Write(friends_text))
            self.wait(0.5)
            self.play(Write(question))
            self.wait(1.5)

            # Clear for next section
            self.play(FadeOut(cookies), FadeOut(cookies_text),
                     FadeOut(friends), FadeOut(friends_text),
                     FadeOut(question))
            self.wait(0.3)

        # --- SECTION 3: Visual Grouping ---
        self.set_speech_service(
            get_speech_service(rate=BEAT_RATE["grouping"]), create_subcaption=True
        )
        # Show cookies being divided into 4 groups
        group_title = Text("Dividing into Equal Groups", font_size=36, color=BLUE)
        group_title.to_edge(UP)

        # Create 4 groups with 3 cookies each
        groups = VGroup()
        for g in range(4):
            group = VGroup(*[
                Circle(radius=0.25, color=ORANGE, fill_opacity=0.8).shift(
                    RIGHT * (g - 1.5) * 2.5 + UP * (0.3 - i * 0.35)
                ) for i in range(3)
            ])
            groups.add(group)

        # Add group labels
        labels = VGroup(*[
            Text(f"Group {i+1}", font_size=20, color=YELLOW).next_to(
                groups[i], DOWN, buff=0.2
            ) for i in range(4)
        ])

        # Count per group
        count_text = Text("3 cookies per group", font_size=32, color=YELLOW)
        count_text.next_to(groups, DOWN, buff=1.2)

        with self.voiceover(text=NARRATION["grouping"]):
            self.play(Write(group_title))
            self.wait(0.5)

            # Animate groups appearing
            for group, label in zip(groups, labels):
                self.play(FadeIn(group), Write(label), run_time=0.6)
            self.wait(1)

            self.play(Write(count_text))
            self.wait(1.5)

            # Clear
            self.play(FadeOut(groups), FadeOut(labels),
                     FadeOut(group_title), FadeOut(count_text))
            self.wait(0.3)

        # --- SECTION 4: Division Symbol Introduction ---
        self.set_speech_service(
            get_speech_service(rate=BEAT_RATE["symbol"]), create_subcaption=True
        )
        symbol_title = Text("The Division Symbol", font_size=36, color=BLUE)
        symbol_title.to_edge(UP)

        # Show the equation
        equation = MathTex("12", "\\div", "4", "=", "3", font_size=72)
        equation.shift(UP * 0.5)

        # Explain dividend
        dividend_label = Text("Dividend", font_size=24, color=ORANGE)
        dividend_label.next_to(equation[0], DOWN, buff=0.3)
        dividend_expl = Text("(Total amount)", font_size=18, color=ORANGE)
        dividend_expl.next_to(dividend_label, DOWN)

        divisor_label = Text("Divisor", font_size=24, color=GREEN)
        divisor_label.next_to(equation[2], DOWN, buff=0.3)
        divisor_expl = Text("(Number of groups)", font_size=18, color=GREEN)
        divisor_expl.next_to(divisor_label, DOWN)

        quotient_label = Text("Quotient", font_size=24, color=YELLOW)
        quotient_label.next_to(equation[4], DOWN, buff=0.3)
        quotient_expl = Text("(Amount per group)", font_size=18, color=YELLOW)
        quotient_expl.next_to(quotient_label, DOWN)

        with self.voiceover(text=NARRATION["symbol"]):
            self.play(Write(symbol_title))
            self.wait(1.0)

            # Animate parts with explanations
            self.play(Write(equation[0]))  # 12
            self.wait(0.3)

            self.play(Write(equation[1]), Write(equation[2]))  # ÷ and 4
            self.wait(0.3)

            self.play(Write(equation[3]), Write(equation[4]))  # = and 3
            self.wait(1.0)

            # Add all labels with animation
            self.play(FadeIn(dividend_label), FadeIn(divisor_label),
                     FadeIn(quotient_label), FadeIn(dividend_expl),
                     FadeIn(divisor_expl), FadeIn(quotient_expl))
            self.wait(4)

            # Clear
            self.play(FadeOut(equation), FadeOut(dividend_label),
                     FadeOut(divisor_label), FadeOut(quotient_label),
                     FadeOut(dividend_expl), FadeOut(divisor_expl),
                     FadeOut(quotient_expl), FadeOut(symbol_title))
            self.wait(0.3)

        # --- SECTION 5: Practice Problem ---
        self.set_speech_service(
            get_speech_service(rate=BEAT_RATE["practice"]), create_subcaption=True
        )
        practice_title = Text("Let's Practice!", font_size=40, color=BLUE)
        practice_title.to_edge(UP)

        # Problem: 15 ÷ 5 = ?
        problem = MathTex("15", "\\div", "5", "=", "?", font_size=80)
        problem.shift(UP * 0.5)

        # Show visual representation
        # 15 dots in 5 groups
        dots = VGroup()
        for g in range(5):
            group = VGroup(*[
                Dot(radius=0.08, color=BLUE).shift(
                    RIGHT * (g - 2) * 2 + UP * (0.3 - i * 0.3)
                ) for i in range(3)
            ])
            dots.add(group)

        # Show answer
        answer = MathTex("3", font_size=80, color=YELLOW)
        answer.next_to(problem[4], RIGHT, buff=0.1)

        with self.voiceover(text=NARRATION["practice"]):
            self.play(Write(practice_title))
            self.wait(0.5)

            self.play(Write(problem))
            self.wait(1)

            # Animate dots appearing with counting
            for group in dots:
                self.play(FadeIn(group), run_time=0.4)
            self.wait(0.5)

            self.play(Write(answer))
            self.wait(0.5)

            # Highlight answer
            self.play(answer.animate.set_color(GREEN))
            self.wait(1)

        # --- SECTION 6: Conclusion ---
        self.set_speech_service(
            get_speech_service(rate=BEAT_RATE["conclusion"]), create_subcaption=True
        )
        conclusion = Text("Division = Sharing Fairly!", font_size=44, color=YELLOW)
        conclusion.shift(UP * 0.5)

        thanks = Text("Thanks for Learning!", font_size=36, color=BLUE)
        thanks.next_to(conclusion, DOWN, buff=0.8)

        with self.voiceover(text=NARRATION["conclusion"]):
            self.play(FadeOut(practice_title), FadeOut(problem),
                     FadeOut(dots), FadeOut(answer))
            self.wait(0.3)

            self.play(Write(conclusion))
            self.wait(0.5)

            self.play(Write(thanks))
            self.wait(2)

            # Fade out everything
            self.play(FadeOut(conclusion), FadeOut(thanks))
            self.wait(0.3)


# For low-quality rendering (480p)
# Run with: manim -pql introduction_to_division.py IntroductionToDivision
