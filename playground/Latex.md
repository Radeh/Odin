# SAMPLE LATEX EQUATIONS IN MARKDOWN

This is an example of **inline math**: $E = mc^2$.

Here is a **block equation**:

$$
\nabla \cdot \vec{E} = \frac{\rho}{\varepsilon_0}
$$

And another block equation with **aligned** notation:

$$
\begin{aligned}
f(x) &= b^2 + bx + c, \\
g(x) &= \int_0^x e^{-t^2} \, dt.
\end{aligned}
$$

You can also reference variables within the text, for example:

- Let $x \in \mathbb{R}$ be a real number.
- We define the function $h(x) = x^2 + 1$.

## Additional Example

We might also show a **system of equations**:

$$
\begin{cases}
x + y = 10,\\
x - y = 4.
\end{cases}
$$

**Inline example** within a sentence: Notice that $x + y = 10$ implies $y = 10 - x$.

$$
v = 13 - y
$$

**Tip**: Many static Markdown previews (e.g., GitHub) do _not_ render LaTeX by default. To properly see the math, use a Markdown viewer with math support (VS Code, Typora, Obsidian, or an online renderer like HackMD). If you use a static site generator (like Jekyll, Hugo, or MkDocs), be sure to enable or include a math rendering plugin (MathJax or KaTeX).
