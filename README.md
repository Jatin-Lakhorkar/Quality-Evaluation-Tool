# Code Quality Evaluation Tool 🚀

A lightweight, high-performance Python CLI tool designed to statically analyze code snippets against PEP 8 style guides, algorithmic complexities, and structural anti-patterns. By leveraging Abstract Syntax Tree (AST) parsing, the tool evaluates code layout without execution, generating structured, CI/CD-ready JSON feedback reports.

## Key Features

*   **AST-Driven Static Analysis:** Parses source code into abstract syntax trees to detect deep structural code smells, unused variables, and inefficient loop architectures.
*   **Multi-Rule Engine:** Evaluates snippets across three main pillars:
    *   *PEP 8 Compliance:* Line length, naming conventions, and structural layouts.
    *   *Algorithmic Complexity:* Identifies nested iterations that lead to $O(N^2)$ or worse performance.
    *   *Anti-Pattern Metrics:* Captures unsafe practices (e.g., bare `except:` blocks) and dead code.
*   **Batch Processing Scale:** Optimized to handle evaluation pipelines across 1,000+ sample files seamlessly.
*   **Structured JSON Output:** Formats reports cleanly for downstream consumption by Github Actions, pre-commit hooks, or custom dashboards.

## Installation

Clone the repository and ensure you have Python 3.8+ installed. No external dependencies are required for the core analyzer engine.

```bash
git clone [https://github.com/yourusername/code-quality-evaluator.git](https://github.com/yourusername/code-quality-evaluator.git)
cd code-quality-evaluator
