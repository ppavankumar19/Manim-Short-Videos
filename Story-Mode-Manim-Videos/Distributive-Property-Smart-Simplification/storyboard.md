# Storyboard: "The Power of Breaking It Apart"
## Distributive Property & Smart Simplification

**Video Title:** The Power of Breaking It Apart

**Topic:** Distributive Property & Smart Simplification

**Target Class Level:** Classes 6–12

**Estimated Duration:** 2–3 minutes

**Learning Objective:** Students will visually understand that multiplying a whole is equal to multiplying its parts, allowing them to use the distributive property for mental math, algebraic expansion, and smart simplification.

**Historical Hook:** Ancient farmers and land surveyors needed to calculate the total area of divided plots of land without measuring the entire boundary again.

**Core Visual Metaphor / Idea:** The Area Model (a large rectangle splitting into two smaller rectangles, maintaining the exact same total area).

**Formula(s):** $a(b + c) = ab + ac$

**Worked Example:** $4 \times 23 = 4(20 + 3) = 80 + 12 = 92$

**Real-World Application:** Calculating the total cost of bulk orders (e.g., buying 5 identical kits, each containing items of two different prices).

**Student Challenge:** Calculate $6 \times 98$ using smart simplification.

---

## Storyboard Overview

| Scene | Time | Learning Goal | Visual Composition | Animation / Movement | Key On-Screen Text | Math / Formula | Narration Intent | Transition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. History / Hook | 00:00–00:20 | Introduce the problem of calculating total parts. | Large rectangle split into two sections (land plots). | Lines draw out the land. Labels appear on sides. | "How much land total?" | None yet. | Explain the historical need to measure large, divided areas easily. | Rectangle slides to center, text fades. |
| 2. Intuitive Concept | 00:20–00:50 | Visually prove the property without equations. | The divided rectangle duplicating and splitting apart. | Rectangle duplicates. One stays whole; the other splits into two pieces. | "Whole = Sum of Parts" | None yet. | State that measuring the whole boundary is the same as measuring the parts and adding them. | Pieces merge back, preparing for variables. |
| 3. Formula | 00:50–01:20 | Connect the visual area to algebraic notation. | Rectangle with width $a$, lengths $b$ and $c$. Formula below. | Labels fly from diagram to form the equation. Arcs draw to show distribution. | "The Distributive Property" | $a(b + c) = ab + ac$ | Explain how the variable $a$ multiplies into both $b$ and $c$ to find total area. | Diagram shrinks, formula moves to top corner. |
| 4. Worked Example | 01:20–01:50 | Apply the concept to simplify mental arithmetic. | $4 \times 23$ equation paired with a $4 \times 23$ rectangle splitting. | $23$ splits into $20$ and $3$. Equation transforms step-by-step. | "Smart Simplification" | $4(20 + 3)$ = $80 + 12$ = $92$ | Walk through how breaking a hard number into easy parts makes mental math simple. | Elements wipe out, revealing real-world icons. |
| 5. Real-World App | 01:50–02:15 | Show practical utility beyond geometry. | 5 identical shopping bags, each containing a $20 item and a $3 item. | Bags unpack. Groups of 20 and groups of 3 align and multiply. | "Total Cost" | $5(20 + 3)$ | Show how we naturally distribute when calculating bulk purchases in everyday life. | Screen clears. "Your Turn" appears. |
| 6. Student Challenge | 02:15–02:40 | Test understanding with subtraction distribution. | $6 \times 98$. Hint showing 98 near 100. | Equation transforms to show subtraction. Pause timer appears. | "Pause and try it!" | $6(100 - 2)$ = $600 - 10$ | Challenge the student to use the same logic, but with subtraction. | Answer flashes, then shrinks into final recap. |
| 7. Finalization | 02:40–03:00 | Reinforce core visual and formula. | The splitting rectangle from Scene 2 and the core formula from Scene 3. | Rectangle splits and rejoins on a loop. Formula highlights. | "Break it down to make it simple." | $a(b + c) = ab + ac$ | Summarize that distribution is just breaking a big problem into manageable pieces. | Fade to black. |

---

## Detailed Scene Information

### SCENE 1 — HISTORY / WHY WAS THIS CONCEPT NEEDED?

**Time:** 00:00–00:20

**Purpose:** Establish the practical problem: finding the total amount of something that is split into parts.

**Initial Frame:** Blank screen.

**Visual Layout:**
- Center: A large rectangular plot of land on a grid.
- Top: Title text.

**Visual Elements:**
- Grid background (faint)
- A large rectangle with a dashed line splitting it vertically
- Left side colored faint yellow (wheat)
- Right side colored faint green (corn)
- Measurement brackets on the left and bottom edges

**Animation Sequence:**
- 0–5 sec: Grid fades in. The outer boundary of the large rectangle is drawn using `Create()`
- 5–10 sec: A dashed line draws down the middle, splitting the rectangle. Yellow and green fill colors fade in
- 10–15 sec: Measurement brackets pop in along the left edge and the bottom edges of the two sections
- 15–20 sec: Text "How much land total?" fades in above the rectangle

**On-Screen Text:**
"How much land total?"

**Mathematical Elements:** None. Keep it visual.

**Narration Intent:** Explain that ancient land surveyors frequently needed to calculate the area of large fields that were divided into different crops. They needed a reliable rule to know the total area without measuring everything twice.

**Manim Implementation Idea:** Use `Rectangle()`, `DashedLine()`, and `Brace()`. `FadeIn` for colors.

**Camera / Focus:** Static wide shot on the rectangle.

**Transition to Next Scene:** Text fades out. Grid fades out. The rectangle slides slightly up to make room for a duplicate.

---

### SCENE 2 — INTUITIVE CONCEPT

**Time:** 00:20–00:50

**Purpose:** Visually demonstrate that the area of the whole is exactly equal to the sum of the areas of its parts.

**Initial Frame:** The yellow/green rectangle from Scene 1, positioned slightly above center.

**Visual Layout:**
- Top: Original intact rectangle
- Bottom: A duplicate rectangle that will break apart
- Center: Text appearing between them

**Visual Elements:**
- Original rectangle (joined)
- Duplicate rectangle (split into two independent squares/rectangles)
- An equal sign

**Animation Sequence:**
- 0–5 sec: The top rectangle duplicates. The copy slides down to the bottom half of the screen
- 5–15 sec: The bottom rectangle splits along the dashed line. The yellow piece slides left, the green piece slides right
- 15–20 sec: A plus sign appears between the separated pieces. An equal sign appears between the top whole rectangle and the bottom separated pieces
- 20–30 sec: The text "Whole = Sum of Parts" writes out. The bottom pieces slide back together and apart again to emphasize they are exactly the same size

**On-Screen Text:**
"Whole = Sum of Parts"

**Mathematical Elements:** None yet.

**Narration Intent:** Explain that measuring the entire field all at once gives the exact same result as measuring the wheat field, measuring the corn field, and adding them together.

**Manim Implementation Idea:** Use `VGroup` to copy. Use `shift()` to move the left and right pieces along the x-axis. `Write()` for text.

**Camera / Focus:** Focus on the breaking apart and rejoining motion.

**Transition to Next Scene:** The bottom rectangles and text fade out. The top rectangle shifts to the center and grows slightly.

---

### SCENE 3 — FORMULA

**Time:** 00:50–01:20

**Purpose:** Translate the visual intuition into mathematical notation (the Distributive Property).

**Initial Frame:** The joined yellow/green rectangle in the center.

**Visual Layout:**
- Center: Rectangle
- Bottom: Formula
- Labels: Surrounding the rectangle

**Visual Elements:**
- Rectangle
- Red label $a$ (height)
- Blue label $b$ (width of left section)
- Green label $c$ (width of right section)
- Curved arrows for distribution

**Animation Sequence:**
- 0–5 sec: Braces appear on the rectangle. The label $a$ (red) appears on the left. The label $b$ (blue) appears on the bottom left. The label $c$ (green) appears on the bottom right
- 5–10 sec: The brace for the entire bottom edge appears, labeled $(b + c)$
- 10–15 sec: The area of the whole is written below: $a(b + c)$
- 15–20 sec: The area of the individual parts populates inside the rectangles: $ab$ inside the yellow, $ac$ inside the green
- 20–25 sec: The formula completes below: $a(b + c) = ab + ac$
- 25–30 sec: Curved arrows draw from the $a$ to the $b$, and from the $a$ to the $c$ in the formula, highlighting the "distribution"

**On-Screen Text:**
"The Distributive Property"

**Mathematical Elements:**
- $a$ (red)
- $b$ (blue)
- $c$ (green)
- $a(b + c) = ab + ac$

**Narration Intent:** Introduce the variables. Show how the width '$a$' applies to both '$b$' and '$c$'. Explain that the formula simply states mathematically what we just saw visually: the whole equals the sum of the parts.

**Manim Implementation Idea:** Use `MathTex` with `set_color_by_tex` to keep variables color-coded. Use `CurvedArrow` to show the distributive arcs. `TransformFromCopy` to pull the letters from the diagram to build the equation.

**Camera / Focus:** Focus shifts from the diagram to the equation at the bottom.

**Transition to Next Scene:** The title and rectangle shrink and move to the top left corner as a reference. The center clears for the worked example.

---

### SCENE 4 — WORKED EXAMPLE

**Time:** 01:20–01:50

**Purpose:** Demonstrate "smart simplification" using numbers to solve mental math easily.

**Initial Frame:** Small reference diagram top left. Center is blank.

**Visual Layout:**
- Top left: Reference diagram
- Center-left: A new numerical rectangle
- Center-right: Step-by-step equation transformation

**Visual Elements:**
- A new rectangle labeled with numbers
- Text equations transforming

**Animation Sequence:**
- 0–5 sec: The problem $4 \times 23$ appears in the center
- 5–10 sec: A rectangle appears. Height is $4$. Total width is $23$
- 10–15 sec: The rectangle splits. The width $23$ changes to $20$ and $3$
- 15–20 sec: The equation transforms: $4(20 + 3)$. Distributive arrows draw from 4 to 20, and 4 to 3
- 20–25 sec: The equation transforms to $(4 \times 20) + (4 \times 3)$. The numbers $80$ and $12$ appear inside the rectangle pieces
- 25–30 sec: Equation resolves to $80 + 12$, and finally $92$

**On-Screen Text:**
"Smart Simplification"

**Mathematical Elements:**
- $4 \times 23$
- $4(20 + 3)$
- $80 + 12$
- $92$

**Narration Intent:** Walk through the mental math. Why struggle with 4 times 23? Break 23 into 20 and 3. Distribute the 4. Now it's just 80 plus 12, which is easily 92.

**Manim Implementation Idea:** Use `TransformMatchingTex` to show the equation morphing step-by-step. Keep the color coding: 4 is red, 20 is blue, 3 is green.

**Camera / Focus:** Keep attention bouncing between the split rectangle and the transforming equation.

**Transition to Next Scene:** All elements wipe out or fade to black.

---

### SCENE 5 — REAL-WORLD APPLICATION

**Time:** 01:50–02:15

**Purpose:** Show that this isn't just about rectangles; it's about grouping any real-world quantities.

**Initial Frame:** Blank screen.

**Visual Layout:**
- Center: 5 generic shopping bags or boxes
- Below: Price tags
- Bottom: Equation

**Visual Elements:**
- 5 bag icons
- Inside each bag (revealed): A blue square ($20 item) and a green circle ($3 item)

**Animation Sequence:**
- 0–5 sec: 5 bags slide onto the screen. Text appears: "Buying 5 identical kits"
- 5–10 sec: The bags disappear, leaving behind their contents grouped together: (Square + Circle) + (Square + Circle) + ... five times
- 10–15 sec: Equation appears: $5 \times (\$20 + \$3)$
- 15–20 sec: The items rearrange visually on screen. All 5 Squares group together. All 5 Circles group together
- 20–25 sec: Equation transforms to $5(\$20) + 5(\$3)$, matching the visual grouping

**On-Screen Text:**
"Total Cost"

**Mathematical Elements:**
- $5(20 + 3)$
- $5(20) + 5(3)$
- $100 + 15 = 115$

**Narration Intent:** Explain that when buying 5 kits, you can either find the cost of one kit and multiply by 5, or calculate the total cost of all the first items, plus the total cost of all the second items. It's the exact same property.

**Manim Implementation Idea:** Use simple `Square()` and `Circle()` for items to keep the Manim clean and reliable. `VGroup` arrangements to show the reorganization of items.

**Camera / Focus:** Focus on the physical rearrangement of the shapes, proving the math visually.

**Transition to Next Scene:** Shapes scale down to zero. The text "Your Turn" scales up aggressively in the center.

---

### SCENE 6 — STUDENT CHALLENGE

**Time:** 02:15–02:40

**Purpose:** Challenge the student to apply the concept independently, introducing the idea that distribution works with subtraction too.

**Initial Frame:** "Your Turn" in the center.

**Visual Layout:**
- Center: The math problem
- Bottom: A pause timer

**Visual Elements:**
- Large text problem
- A visual hint
- Pause icon

**Animation Sequence:**
- 0–5 sec: "Your Turn" fades out. The problem $6 \times 98$ writes in large text
- 5–10 sec: A hint appears: "Hint: 98 is very close to 100"
- 10–15 sec: $6 \times 98$ transforms into $6(100 - 2)$
- 15–20 sec: "Pause and try it!" appears. A visual 3-second countdown bar shrinks at the bottom of the screen
- 20–25 sec: Arrows distribute the 6. The equation transforms to $600 - 12$
- 25–30 sec: Final answer $588$ appears

**On-Screen Text:**
- "Your Turn"
- "Hint: 98 is very close to 100"
- "Pause and try it!"

**Mathematical Elements:**
- $6 \times 98$
- $6(100 - 2)$
- $600 - 12 = 588$

**Narration Intent:** Challenge the student. Ask them to solve 6 times 98 using smart simplification. Give them the hint to use 100 minus 2. Prompt them to pause. Reveal the solution.

**Manim Implementation Idea:** Use a `Rectangle()` whose width scales down as a loading bar for the pause timer. Use `ReplacementTransform` for the mathematical steps.

**Camera / Focus:** Center screen, large readable text for mobile.

**Transition to Next Scene:** Answer glows, then shrinks and moves to the top, transitioning into the final recap screen.

---

### SCENE 7 — FINALIZATION / RECAP

**Time:** 02:40–03:00

**Purpose:** Provide a lasting visual memory of the core concept and formula.

**Initial Frame:** Clear screen, transitioning from the previous scene.

**Visual Layout:**
- Top: Core takeaway text
- Center: The splitting rectangle from Scene 2
- Bottom: The core formula from Scene 3

**Visual Elements:**
- The yellow and green rectangles
- The formula with colored variables
- Main takeaway text

**Animation Sequence:**
- 0–5 sec: The whole rectangle appears in the center. The formula $a(b + c)$ appears below it
- 5–15 sec: The rectangle continuously slowly splits and rejoins on a loop. As it splits, the formula shifts to $= ab + ac$. As it rejoins, it shifts back to $a(b + c)$
- 15–20 sec: The text "Break it down to make it simple." appears in large bold letters at the top. The animation holds on the split state

**On-Screen Text:**
"Break it down to make it simple."

**Mathematical Elements:**
$a(b + c) = ab + ac$

**Narration Intent:** Summarize the lesson. The distributive property isn't just an algebra rule to memorize; it's a tool to break complex problems into simple, bite-sized pieces. Break it down to make it simple.

**Manim Implementation Idea:** Use an `updater` or a looped animation for the rectangle splitting and merging. Use `MathTex` for the formula.

**Camera / Focus:** Static, balanced composition holding all three key elements (Text, Visual, Formula).

**Transition to Next Scene:** Fade to black.

---

## Next Steps

This storyboard is verified and ready for the **build prompt stage** (Stage 4 in `process.md`). 

To proceed:
1. Confirm the mathematical accuracy and pedagogical goals with the textbook
2. Identify any reference Manim patterns from the local repos (`manim/`, `manimce-public-animations/`, `Manim-Mobjects-and-Animations/`)
3. Create the build prompt for Claude Code, specifying:
   - Topic folder: `Distributive-Property-Smart-Simplification/`
   - Characters/scenario: Ancient land surveyors (hook), then abstract variables
   - Concrete numbers: 4×23, 6×98, 5 kits example
   - Visual style: Reuse chalkboard background, chalk-vector rectangles, VoiceoverScene + edge-tts sync
   - Beat structure: (as per the 7 scenes above)
   - Constraints: "Explain every formula variable," "show the area model visually," "test with subtraction," "provide a real-world anchor"
