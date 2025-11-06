"""
Test samples for complexity analyzer validation.
Each function is annotated with its expected McCabe complexity.
"""


# Expected complexity: 1 (no branches)
def simple_function():
    """Simple function with no branches."""
    return 42


# Expected complexity: 2 (1 if statement)
def single_if(x):
    """Single if statement."""
    if x > 0:
        return x
    return 0


# Expected complexity: 3 (2 if statements)
def two_ifs(x, y):
    """Two independent if statements."""
    if x > 0:
        x = x * 2
    if y > 0:
        y = y * 2
    return x + y


# Expected complexity: 4 (if-elif-else chain = 3 decision points)
def if_elif_else(x):
    """If-elif-else chain."""
    if x > 10:
        return "large"
    elif x > 5:
        return "medium"
    elif x > 0:
        return "small"
    else:
        return "zero or negative"


# Expected complexity: 3 (1 for loop + 1 if inside)
def loop_with_if(items):
    """For loop with conditional."""
    count = 0
    for item in items:
        if item > 0:
            count += 1
    return count


# Expected complexity: 4 (1 while + 1 if + 1 elif)
def while_with_conditionals(x):
    """While loop with conditionals."""
    result = 0
    while x > 0:
        if x % 2 == 0:
            result += x
        elif x % 3 == 0:
            result += x * 2
        x -= 1
    return result


# Expected complexity: 5 (and adds 1, or adds 1)
def boolean_operators(a, b, c):
    """Function with boolean operators."""
    if a > 0 and b > 0:
        return True
    if c < 0 or b < 0:
        return False
    return None


# Expected complexity: 6 (nested ifs: outer + inner1 + inner2 + inner3 + inner4)
def nested_conditions(x, y):
    """Nested conditional statements."""
    if x > 0:
        if y > 0:
            if x > y:
                return "x bigger"
            else:
                return "y bigger or equal"
        else:
            return "y negative"
    return "x not positive"


# Expected complexity: 4 (try-except adds 2: except handler adds 1 each)
def exception_handling(x):
    """Function with exception handling."""
    try:
        result = 10 / x
    except ZeroDivisionError:
        return 0
    except ValueError:
        return -1
    return result


# Expected complexity: 3 (list comprehension with if)
def list_comprehension_example(items):
    """List comprehension with conditional."""
    positive = [x for x in items if x > 0]
    if len(positive) > 5:
        return positive[:5]
    return positive


# Expected complexity: 5 (multiple generators with ifs)
def complex_comprehension(matrix):
    """Complex comprehension with multiple conditions."""
    result = [
        x * y
        for row in matrix
        for x in row if x > 0
        for y in row if y > 0
    ]
    return result


# Expected complexity: 3 (with statement + if)
def with_statement_example(filename):
    """Function using with statement."""
    with open(filename, 'r') as f:
        content = f.read()
        if len(content) > 0:
            return content.strip()
    return ""


# Expected complexity: 2 (assert counts as decision point)
def function_with_assert(x):
    """Function with assert statement."""
    assert x > 0, "x must be positive"
    return x * 2


# Expected complexity: 30+ (very complex function - should be flagged)
def very_complex_function(data, config, options):
    """
    Intentionally complex function to test high complexity detection.
    This should be flagged as complex or very_complex.
    """
    results = []
    errors = []
    
    if not data:
        return None
    
    if config is None:
        config = {}
    
    for item in data:
        if item is None:
            continue
            
        if 'type' not in item:
            errors.append("Missing type")
            continue
        
        if item['type'] == 'A':
            if 'value' in item:
                if item['value'] > 100:
                    results.append(item['value'] * 2)
                elif item['value'] > 50:
                    results.append(item['value'] * 1.5)
                elif item['value'] > 10:
                    results.append(item['value'])
                else:
                    errors.append("Value too small")
            else:
                errors.append("Missing value")
                
        elif item['type'] == 'B':
            if options and 'mode' in options:
                if options['mode'] == 'fast':
                    results.append(item.get('value', 0))
                elif options['mode'] == 'safe':
                    if item.get('validated', False):
                        results.append(item['value'])
                    else:
                        errors.append("Not validated")
                else:
                    errors.append("Unknown mode")
            else:
                results.append(item.get('value', 0))
                
        elif item['type'] == 'C':
            try:
                value = int(item['value'])
                if value > 0 and value < 1000:
                    results.append(value)
                else:
                    errors.append("Value out of range")
            except (ValueError, KeyError):
                errors.append("Invalid value")
        
        else:
            errors.append(f"Unknown type: {item['type']}")
    
    if len(errors) > 0 and len(results) == 0:
        return None
    elif len(errors) > len(results):
        return None
    else:
        return results


# Expected complexity: 8+ (moderate complexity)
def moderate_complexity_example(items, threshold, mode):
    """
    Moderately complex function - should be in moderate range.
    """
    count = 0
    total = 0
    
    if not items:
        return 0
    
    for item in items:
        if mode == 'strict':
            if item > threshold and item < threshold * 2:
                count += 1
                total += item
        elif mode == 'relaxed':
            if item > threshold / 2:
                count += 1
                total += item
        else:
            count += 1
            total += item
    
    if count > 0:
        return total / count
    return 0
