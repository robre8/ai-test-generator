import os
from groq import Groq

def generate_tests_from_code(code: str) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""You are a senior Python test engineer. Your task is to generate pytest unit tests for the following Python code.

CRITICAL INSTRUCTIONS FOR TESTS THAT WILL ALL PASS:
1. Return ONLY valid Python test code - NO markdown, NO code blocks (```), NO explanatory text
2. ALL tests MUST PASS - this is critical, no exceptions allowed unless explicitly caught
3. The code does NOT handle errors, so AVOID testing with invalid inputs that cause exceptions (division by zero, None values, etc)
4. Import from `user_code` module (not from `code`)
5. Test normal, valid use cases that work correctly
6. If a function/method could fail with certain inputs but doesn't handle it, DON'T test those inputs
7. Only test with inputs that the code can handle without raising exceptions
8. Start with imports, followed by test functions - NO introductory explanations

Python Code to Test:
{code}

REMEMBER: Generate tests that will ALL PASS. Avoid edge cases that cause unhandled exceptions.
Generate ONLY the test code (Python syntax only, import from user_code):"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    tests = response.choices[0].message.content.strip()
    
    # Clean up markdown code blocks and non-code lines
    lines = tests.split("\n")
    cleaned_lines = []
    in_code_block = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip markdown markers
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        
        # Skip completely empty lines or lines with only whitespace
        if not stripped:
            cleaned_lines.append("")
            continue
        
        # Skip lines that are clearly explanatory text (not Python code)
        # These typically start with capital letters and contain certain keywords
        if stripped and not any(stripped.startswith(prefix) for prefix in [
            "import", "from", "def ", "class ", "@", "assert", "if ", "for ", 
            "while ", "try", "except", "finally", "with ", "return", "#", "'", '"',
            ".", "[", "(", "+", "-", "*", "/", "="
        ]):
            # This line doesn't look like Python code
            # Only include it if it's a comment (convert if needed)
            if stripped[0] not in ["#"]:
                # Skip it if it looks like English text
                if stripped[0].isupper() and "." in stripped and len(stripped) > 20:
                    continue
        
        cleaned_lines.append(line)
    
    tests = "\n".join(cleaned_lines).strip()
    
    # Remove any trailing non-code text after the last def/assert block
    # Find the last occurrence of 'def ' or 'assert'
    parts = tests.rsplit("assert", 1)
    if len(parts) > 1:
        # Check if there's explanatory text after the last assert
        after_last = parts[1]
        lines_after = after_last.split("\n")
        # Keep only lines that are still part of the test function
        valid_lines = []
        for line in lines_after:
            s = line.strip()
            if s and not s[0].isupper():  # Keep short or code lines
                valid_lines.append(line)
            elif not s:  # Keep empty lines
                valid_lines.append(line)
        tests = parts[0] + "assert" + "\n".join(valid_lines)
    
    tests = tests.strip()
    
    # Replace any remaining references to 'from code' with 'from user_code'
    tests = tests.replace("from code import", "from user_code import")
    tests = tests.replace("import code", "import user_code")
    
    return tests
