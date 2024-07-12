import re
import sys
import os

def transpile_noodle_to_js(noodle_code):

    noodle_code = re.sub(r'(\w+): (\w+) = (.+)', r'let \1: \2 = \3;', noodle_code)

    noodle_code = re.sub(r'struct (\w+) {(.+)}', r'class \1 {\n  \2\n}', noodle_code)

    noodle_code = re.sub(r'let (\w+): (\w+) = (.+)', r'var \1: \2 = \3;', noodle_code)

    noodle_code = re.sub(r'func (\w+)\((.+): (\w+)\): (\w+)\n  return (.+)',
                         r'function \1(\2: \3): \4 {\n  if (typeof \2 !== "\3") {\n    throw new Error(`\2 must be of type \3`);\n  }\n  return \5;\n}', noodle_code)

    noodle_code = re.sub(r'for (\w+) in (\w+)\n  (.+)',
                         r'for (let \1 of \2) {\n  \3\n}', noodle_code)

    noodle_code = re.sub(r'if (\w+) then\n  (.+)',
                         r'if (\1) {\n  \2\n}', noodle_code)

    noodle_code = re.sub(r'while (\w+)\n  (.+)',
                         r'while (\1) {\n  \2\n}', noodle_code)

    noodle_code = re.sub(r'switch (\w+)\n  case (\w+):\n    (.+)',
                         r'switch (\1) {\n  case \2:\n    \3\n  break;\n}', noodle_code)

    noodle_code = re.sub(r'class (\w+)\n  (.+)',
                         r'class \1 {\n  \2\n}', noodle_code)

    noodle_code = re.sub(r'(\w+)\[(\d+)\] = (.+)', r'let \1 = new Array(\2).fill(\3);', noodle_code)

    noodle_code = re.sub(r'#(.+)', r'// \1', noodle_code)

    noodle_code = re.sub(r'@(\w+)\nfunc (\w+)\((.*)\)', r'function \2(...args) {\n  return \1(\2, ...args);\n}', noodle_code)

    noodle_code = re.sub(r'document\.(\w+)\((.*)\)', r'document.\1(\2);', noodle_code)

    noodle_code = re.sub(r'try\n  (.+)\ncatch (\w+)\n  (.+)\nfinally\n  (.+)',
                         r'try {\n  \1\n} catch (\2) {\n  \3\n} finally {\n  \4\n}', noodle_code)

    noodle_code = re.sub(r'try\n  (.+)\ncatch (\w+)\n  (.+)',
                         r'try {\n  \1\n} catch (\2) {\n  \3\n}', noodle_code)

    noodle_code = re.sub(r'async func (\w+)\((.*)\)', r'async function \1(\2)', noodle_code)

    noodle_code = re.sub(r'type (\w+) = (.+)', r'type \1 = \2;', noodle_code)

    return noodle_code

def main():
    if len(sys.argv) < 3:
        print("Usage: ./noodle.exe -c <input_file> [: <output_file>]")
        return

    input_file = sys.argv[2]
    output_file = input_file.replace(".noodle", ".js")

    if len(sys.argv) == 5 and sys.argv[3] == ":":
        output_file = sys.argv[4]

    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist.")
        return

    with open(input_file, "r") as f:
        noodle_code = f.read()

    js_code = transpile_noodle_to_js(noodle_code)

    with open(output_file, "w") as f:
        f.write(js_code)

    print(f"Transpiled {input_file} to {output_file}")

if __name__ == "__main__":
    main()