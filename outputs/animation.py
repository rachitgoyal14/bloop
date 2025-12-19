from manim import *

class Scene1_Standardformofaquadraticequation(Scene):
    def construct(self):
        eq = MathTex(r"ax^2", r"+", r"bx", r"+", r"c", r"=", r"0")
        eq.move_to(ORIGIN)
        self.play(Write(eq[0]))  # ax^2
        self.wait(1)
        self.play(Write(eq[1]))  # +
        self.wait(1)
        self.play(Write(eq[2]))  # bx
        self.wait(1)
        self.play(Write(eq[3]))  # +
        self.wait(1)
        self.play(Write(eq[4]))  # c
        self.wait(1)
        self.play(Write(eq[5]))  # =
        self.wait(1)
        self.play(Write(eq[6]))  # 0
        self.wait(2)

class Scene2_Graphofaquadraticfunction(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True},
        )
        axes.to_edge(DOWN)

        parabola = axes.plot(lambda x: x**2, x_range=[-2.5, 2.5], color=BLUE)

        vertex = Dot(axes.c2p(0, 0), color=RED)
        axis_of_symmetry = Line(axes.c2p(0, -1), axes.c2p(0, 4), color=GREEN, stroke_width=2, stroke_opacity=0.7)

        vertex_label = MathTex(r"(0,0)").next_to(vertex, DOWN)
        aos_label = Tex("Axis of symmetry").next_to(axis_of_symmetry, RIGHT)

        self.play(Create(axes))
        self.wait(1)
        self.play(Create(parabola))
        self.wait(1)
        self.play(Create(vertex))
        self.play(Write(vertex_label))
        self.wait(1)
        self.play(Create(axis_of_symmetry))
        self.play(Write(aos_label))
        self.wait(3)

class Scene3_Factoringmethod(Scene):
    def construct(self):
        step1 = MathTex(r"x^2 + 5x + 6")
        step2 = MathTex(r"= (x + 2)(x + 3)")

        step1.to_edge(UP)
        step2.next_to(step1, DOWN, buff=1)

        self.play(Write(step1))
        self.wait(2)
        self.play(Transform(step1, step2))
        self.wait(3)

class Scene4_Completingthesquare(Scene):
    def construct(self):
        eq1 = MathTex(r"x^2 + 6x + 5")
        eq2 = MathTex(r"= (x^2 + 6x + 9) - 9 + 5")
        eq3 = MathTex(r"= (x + 3)^2 - 4")

        eq1.to_edge(UP)
        eq2.next_to(eq1, DOWN, buff=1)
        eq3.next_to(eq2, DOWN, buff=1)

        self.play(Write(eq1))
        self.wait(2)
        self.play(Transform(eq1, eq2))
        self.wait(2)
        self.play(Transform(eq1, eq3))
        self.wait(3)

class Scene5_Quadraticformula(Scene):
    def construct(self):
        formula = MathTex(r"x", "=", r"\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
        formula.to_edge(UP)

        substitution = MathTex(r"x", "=", r"\frac{-3 \pm \sqrt{3^2 - 4 \cdot 1 \cdot 2}}{2 \cdot 1}")
        substitution.next_to(formula, DOWN, buff=1)

        self.play(Write(formula))
        self.wait(3)
        self.play(Write(substitution))
        self.wait(3)

class Scene6_Discriminantandnatureofroots(Scene):
    def construct(self):
        # Discriminant formula
        disc = MathTex(r"\Delta", r"=", r"b^2 - 4ac")
        disc.to_edge(UP)

        # Text explanations
        text_pos = Tex(r"When $\Delta > 0$, two distinct real roots")
        text_zero = Tex(r"When $\Delta = 0$, one real root")
        text_neg = Tex(r"When $\Delta < 0$, no real roots")

        text_pos.next_to(disc, DOWN, buff=0.5)
        text_zero.next_to(text_pos, DOWN, buff=0.5)
        text_neg.next_to(text_zero, DOWN, buff=0.5)

        # Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True},
        )
        axes.to_edge(DOWN)

        # Parabolas
        parabola_pos = axes.plot(lambda x: x**2 - 1, x_range=[-2.5, 2.5], color=BLUE)  # Delta > 0
        parabola_zero = axes.plot(lambda x: x**2, x_range=[-2.5, 2.5], color=GREEN)       # Delta = 0
        parabola_neg = axes.plot(lambda x: x**2 + 1, x_range=[-2.5, 2.5], color=RED)      # Delta < 0

        self.play(Write(disc))
        self.wait(1)
        self.play(Write(text_pos))
        self.wait(1)
        self.play(Create(axes), Create(parabola_pos))
        self.wait(2)

        self.play(FadeOut(parabola_pos), FadeOut(axes), FadeOut(text_pos))

        self.play(Write(text_zero))
        self.play(Create(axes), Create(parabola_zero))
        self.wait(2)

        self.play(FadeOut(parabola_zero), FadeOut(axes), FadeOut(text_zero))

        self.play(Write(text_neg))
        self.play(Create(axes), Create(parabola_neg))
        self.wait(3)
