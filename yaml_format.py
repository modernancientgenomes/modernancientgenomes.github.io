import sys

def transform_lines(input_lines):
    output_lines = []
    family_name = ""

    for line in input_lines:
        if 'family:' in line:
            family_name = line.split(':')[1].strip()
        elif 'given:' in line:
            given_name = line.split(':')[1].strip()
            output_lines.append(f"- {given_name} {family_name}")
        else:
            # If the line doesn't contain 'family' or 'given', leave it as is
            output_lines.append(line.strip())

    return '\n'.join(output_lines)

# Example usage
if __name__ == "__main__":
    input_lines = sys.stdin.readlines()
    transformed_text = transform_lines(input_lines)
    print(transformed_text)
