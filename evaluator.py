This core Python script utilizes the native `ast` library to scan for variable definitions, loop structures, and exception blocks, packaging everything into the clean JSON format your project describes.

```python
#!/usr/bin/env python3
import ast
import json
import sys
import argparse
from typing import Dict, Any, List

class CodeQualityAnalyzer(ast.NodeVisitor):
    """
    AST Visitor to identify code smells, unused variables, 
    and algorithmic complexities like nested loops.
    """
    def __init__(self):
        self.report = {
            "complexity_issues": [],
            "anti_patterns": [],
            "unused_elements": []
        }
        # Tracking states
        self.current_loop_depth = 0
        self.defined_variables = set()
        self.used_variables = set()

    def visit_For(self, node: ast.For):
        self.current_loop_depth += 1
        if self.current_loop_depth > 1:
            self.report["complexity_issues"].append({
                "line": node.lineno,
                "type": "Nested Loop Detected",
                "severity": "Warning",
                "message": f"Nested loop identified at depth {self.current_loop_depth}. Risks O(N^2) or worse complexity."
            })
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_While(self, node: ast.While):
        self.current_loop_depth += 1
        if self.current_loop_depth > 1:
            self.report["complexity_issues"].append({
                "line": node.lineno,
                "type": "Nested Loop Detected",
                "severity": "Warning",
                "message": f"Nested loop (while) identified at depth {self.current_loop_depth}."
            })
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_Name(self, node: ast.Name):
        # Track if variable is being assigned to or read from
        if isinstance(node.ctx, ast.Store):
            self.defined_variables.add((node.id, node.lineno))
        elif isinstance(node.ctx, ast.Load):
            self.used_variables.add(node.id)
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        for handler in node.handlers:
            # handler.type is None represents a bare 'except:' block
            if handler.type is None:
                self.report["anti_patterns"].append({
                    "line": handler.lineno,
                    "type": "Bare Except Clause",
                    "severity": "Critical",
                    "message": "Found bare 'except:'. This silences unexpected system exits and exceptions."
                })
        self.generic_visit(node)

    def finalize_unused_variables(self):
        """Cross-references defined vs used variables to uncover dead code."""
        for var_name, line in self.defined_variables:
            # Ignore private/throwaway underscores common in Python
            if var_name not in self.used_variables and not var_name.startswith('_'):
                self.report["unused_elements"].append({
                    "line": line,
                    "variable": var_name,
                    "message": f"Variable '{var_name}' is assigned but never used."
                })

def evaluate_pep8_rules(source_code: str) -> List[Dict[str, Any]]:
    """Evaluates cosmetic and layout configurations matching PEP8 guidelines."""
    pep8_violations = []
    lines = source_code.splitlines()
    
    for index, line in enumerate(lines, start=1):
        # Rule: Max Line Length (PEP8 standard is 79, though 88 is widely accepted now)
        if len(line) > 79:
            pep8_violations.append({
                "line": index,
                "type": "Line Too Long",
                "length": len(line),
                "message": f"Line exceeds typical PEP 8 max-length recommendation ({len(line)}/79 chars)."
            })
    return pep8_violations

def analyze_snippet(source_code: str) -> Dict[str, Any]:
    """Runs combined AST and mechanical code validation rules over source text."""
    metrics = {
        "meta": {"lines_processed": len(source_code.splitlines())},
        "pep8_violations": evaluate_pep8_rules(source_code),
        "structural_analysis": {}
    }
    
    try:
        tree = ast.parse(source_code)
        analyzer = CodeQualityAnalyzer()
        analyzer.visit(tree)
        analyzer.finalize_unused_variables()
        metrics["structural_analysis"] = analyzer.report
        metrics["meta"]["status"] = "Success"
    except SyntaxError as se:
        metrics["meta"]["status"] = "Failed (Syntax Error)"
        metrics["meta"]["error_details"] = str(se)
        metrics["structural_analysis"] = {"error": "Could not parse AST due to code structural syntax failure."}
        
    return metrics

def main():
    parser = argparse.ArgumentParser(description="Code Quality Evaluation Tool Engine")
    parser.add_argument("file", help="Path to the target Python code script file.")
    parser.add_argument("-o", "--output", help="Optional destination path to write JSON file output.")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as source_file:
            content = source_file.read()
    except Exception as e:
        print(f"Error opening or reading file: {e}", file=sys.stderr)
        sys.exit(1)

    evaluation_report = analyze_snippet(content)
    json_output = json.dumps(evaluation_report, indent=4)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out_file:
            out_file.write(json_output)
        print(f"✅ Evaluation complete. JSON analysis written cleanly to: {args.output}")
    else:
        print(json_output)

if __name__ == "__main__":
    main()
