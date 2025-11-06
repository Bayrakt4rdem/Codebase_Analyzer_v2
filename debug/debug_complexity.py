"""Debug script to understand complexity calculation."""

import ast

code = """
def nested_conditions(x, y):
    if x > 0:              # +1 (decision point 1)
        if y > 0:          # +1 (decision point 2)
            if x > y:      # +1 (decision point 3)
                return "x bigger"
            else:          # else doesn't add to complexity in McCabe
                return "y bigger or equal"
        else:              # else doesn't add to complexity
            return "y negative"
    return "x not positive"
"""

tree = ast.parse(code)
func = tree.body[0]

print("AST nodes in nested_conditions:")
print("="*60)

def show_nodes(node, level=0):
    indent = "  " * level
    if isinstance(node, (ast.If, ast.While, ast.For)):
        print(f"{indent}{node.__class__.__name__} at line {node.lineno}")
    elif isinstance(node, ast.BoolOp):
        print(f"{indent}{node.__class__.__name__}: {node.op.__class__.__name__}")
    
    for child in ast.iter_child_nodes(node):
        if not isinstance(child, (ast.FunctionDef, ast.ClassDef)):
            show_nodes(child, level + 1)

show_nodes(func)

print("\n" + "="*60)
print("Expected complexity: 1 (base) + 3 (if statements) = 4")
print("Note: 'else' branches don't add to McCabe complexity")
print("The 6 in the expected might be counting else branches,")
print("which is non-standard. McCabe complexity is typically")
print("edges - nodes + 2, which for this function is 4.")
