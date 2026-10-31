# Project Report: Prompt Comparison and Improvement Tool

## 1. Objective
Show that a prompt with context, role, constraints and output format gives better results than a basic prompt.

## 2. Method
The tool builds two prompts for each task, gets two outputs, scores both against the stated constraints
(word limit, bullet count, table/code format, subject line, no filler introduction) and declares a winner.

## 3. Results on selected examples
| # | Task | Basic score | Improved score | Better prompt |
|---|---|---|---|---|
| 1 | Explain photosynthesis | 33 | 100 | Improved |
| 2 | Leave email to manager | 0 | 100 | Improved |
| 3 | Benefits of exercise | 33 | 100 | Improved |
| 4 | Palindrome function | 0 | 100 | Improved |
| 5 | 7-day study plan | 0 | 100 | Improved |

## 4. Observations
- Basic prompts gave long, generic answers and ignored format and length.
- The Role set the tone and level (teacher, business writer, developer).
- Context removed guesswork (e.g. the exact leave dates, the exam topics).
- Constraints controlled length and structure.
- Output format made answers directly usable (table, code block, email with subject).

## 5. Limitations
- The rule-based score checks format and length, not factual correctness.
- Demo outputs are saved samples; live outputs can vary between runs.

## 6. Conclusion
The improved prompt was better in all 5 examples because it gave the model clear instructions.
