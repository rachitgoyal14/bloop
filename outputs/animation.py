from manim import *

class Scene1_Definitionofaquadraticequation(Scene):
    def construct(self):
        eq = MathTex(r"ax^2", r"+", r"bx", r"+", r"c", r"=", r"0")
        eq.set(font_size=72)
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
            y_range=[-1, 9, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": True},
        )
        axes_labels = axes.get_axis_labels(x_label=Tex("x"), y_label=Tex("y"))

        # Quadratic function y = x^2 - 2x + 1 (vertex at (1,0))
        parabola = axes.plot(lambda x: x**2 - 2*x + 1, x_range=[-0.5, 2.5], color=BLUE)

        vertex = Dot(axes.coords_to_point(1, 0), color=RED)
        vertex_label = Tex("Vertex (1,0)").next_to(vertex, UP)

        axis_of_symmetry = axes.get_vertical_line(axes.coords_to_point(1, 0), color=YELLOW)

        self.play(Create(axes), Write(axes_labels))
        self.wait(1)
        self.play(Create(parabola))
        self.wait(1)
        self.play(Create(vertex), Write(vertex_label))
        self.wait(1)
        self.play(Create(axis_of_symmetry))
        self.wait(2)

class Scene3_Standardformandvertexform(Scene):
    def construct(self):
        # Standard form
        standard = MathTex(r"y", "=", r"ax^2", r"+", r"bx", r"+", r"c")
        standard.to_edge(UP)

        # Vertex form
        vertex = MathTex(r"y", "=", r"a", r"\left(x - h\right)^2", r"+", r"k")
        vertex.to_edge(DOWN)

        self.play(Write(standard))
        self.wait(2)
        self.play(Transform(standard, vertex))
        self.wait(2)
        self.play(FadeOut(standard))

class Scene4_Factoringmethod(Scene):
    def construct(self):
        expr = MathTex(r"x^2", r"+", r"5x", r"+", r"6")
        expr.set(font_size=72)
        factored = MathTex(r"(x + 2)", r"(x + 3)")
        factored.next_to(expr, DOWN, buff=1)

        self.play(Write(expr))
        self.wait(2)
        self.play(Transform(expr, factored))
        self.wait(2)

class Scene5_Completingthesquare(Scene):
    def construct(self):
        step1 = MathTex(r"x^2 + 6x + 5 = 0")
        step2 = MathTex(r"x^2 + 6x = -5")
        step3 = MathTex(r"x^2 + 6x + 9 = -5 + 9")
        step4 = MathTex(r"(x + 3)^2 = 4")

        step1.to_edge(UP)
        step2.next_to(step1, DOWN, buff=0.5)
        step3.next_to(step2, DOWN, buff=0.5)
        step4.next_to(step3, DOWN, buff=0.5)

        self.play(Write(step1))
        self.wait(2)
        self.play(Write(step2))
        self.wait(2)
        self.play(Write(step3))
        self.wait(2)
        self.play(Write(step4))
        self.wait(2)

class Scene6_Quadraticformuladerivation(Scene):
    def construct(self):
        eq1 = MathTex(r"ax^2 + bx + c = 0")
        eq2 = MathTex(r"ax^2 + bx = -c")
        eq3 = MathTex(r"x^2 + \frac{b}{a}x = -\frac{c}{a}")
        eq4 = MathTex(r"x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2 = -\frac{c}{a} + \left(\frac{b}{2a}\right)^2")
        eq5 = MathTex(r"\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}")
        eq6 = MathTex(r"x + \frac{b}{2a} = \pm \frac{\sqrt{b^2 - 4ac}}{2a}")
        eq7 = MathTex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")

        eqs = [eq1, eq2, eq3, eq4, eq5, eq6, eq7]
        for i, eq in enumerate(eqs):
            eq.to_edge(UP)
            if i > 0:
                eq.next_to(eqs[i-1], DOWN, buff=0.5)

        for eq in eqs:
            self.play(Write(eq))
            self.wait(2)

class Scene7_Usingthequadraticformula(Scene):
    def construct(self):
        formula = MathTex(r"x", "=", r"\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
        formula.to_edge(UP)

        substitution = MathTex(r"x", "=", r"\frac{-3 \pm \sqrt{3^2 - 4 \cdot 1 \cdot (-4)}}{2 \cdot 1}")
        substitution.next_to(formula, DOWN, buff=1)

        simplification = MathTex(r"x", "=", r"\frac{-3 \pm \sqrt{9 + 16}}{2}")
        simplification.next_to(substitution, DOWN, buff=0.5)

        roots = MathTex(r"x", "=", r"\frac{-3 \pm 5}{2}")
        roots.next_to(simplification, DOWN, buff=0.5)

        root1 = MathTex(r"x", "=", r"1")
        root1.next_to(roots, DOWN, buff=0.5).to_edge(LEFT)

        root2 = MathTex(r"x", "=", r"-4")
        root2.next_to(roots, DOWN, buff=0.5).to_edge(RIGHT)

        self.play(Write(formula))
        self.wait(2)
        self.play(Write(substitution))
        self.wait(2)
        self.play(Write(simplification))
        self.wait(2)
        self.play(Write(roots))
        self.wait(2)
        self.play(Write(root1), Write(root2))
        self.wait(2)

class Scene8_Discriminantandnatureofroots(Scene):
    def construct(self):
        disc = MathTex(r"\Delta", r"=", r"b^2 - 4ac")
        disc.to_edge(UP)

        text1 = Tex(r"If $\Delta > 0$, two distinct real roots")
        text2 = Tex(r"If $\Delta = 0$, one real root")
        text3 = Tex(r"If $\Delta < 0$, two complex roots")

        text1.next_to(disc, DOWN, buff=0.5)
        text2.next_to(text1, DOWN, buff=0.3)
        text3.next_to(text2, DOWN, buff=0.3)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-4, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": True},
        )
        axes_labels = axes.get_axis_labels(x_label=Tex("x"), y_label=Tex("y"))

        # Three parabolas for different discriminants
        parabola_pos = axes.plot(lambda x: x**2 - 2*x + 1, x_range=[-1, 3], color=GREEN)  # Delta=0
        parabola_two = axes.plot(lambda x: x**2 - 3*x + 2, x_range=[0, 3], color=BLUE)  # Delta>0
        parabola_complex = axes.plot(lambda x: x**2 + 2*x + 5, x_range=[-4, 0], color=RED)  # Delta<0

        self.play(Write(disc))
        self.wait(2)
        self.play(Write(text1))
        self.wait(1)
        self.play(Write(text2))
        self.wait(1)
        self.play(Write(text3))
        self.wait(2)

        self.play(Create(axes), Write(axes_labels))
        self.wait(1)
        self.play(Create(parabola_two))
        self.wait(1)
        self.play(Create(parabola_pos))
        self.wait(1)
        self.play(Create(parabola_complex))
        self.wait(2)
