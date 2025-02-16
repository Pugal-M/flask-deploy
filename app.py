
from flask import Flask,request,jsonify
import numpy as np
import werkzeug
import werkzeug.utils
import re
import string 
app = Flask (__name__)

@app.route('/api', methods = ['GET'])
 
def returnascii():
    x1 = float(request.args.get('queryx1'))
    x2 = float(request.args.get('queryx2'))
    y1 = float(request.args.get('queryy1'))
    y2 = float(request.args.get('queryy2'))
    z1 = float(request.args.get('queryz1'))
    z2 = float(request.args.get('queryz2'))
    z3 = float(request.args.get('queryz3'))
    z4 = float(request.args.get('queryz4'))
    coeff_matrix = [
    [1, x1, y1, x1 * y1],
    [1, x2, y1, x2 * y1],
    [1, x1, y2, x1 * y2],
    [1, x2, y2, x2 * y2]
    ]
    d = {}
    rhs = [z1, z2, z3, z4]
    coeff_matrix = np.array(coeff_matrix)
    rhs = np.array(rhs)
    determinant = np.linalg.det(coeff_matrix)
    if determinant == 0:
        return jsonify({"error": "Coefficient matrix is singular and cannot be solved."})

    coefficients = np.linalg.solve(coeff_matrix, rhs)
    A, B, C, D = coefficients
    
    d['A'] = f"A = {A:.6f}"
    d['B'] = f"B = {B:.6f}"
    d['C'] = f"C = {C:.6f}"
    d['D'] = f"D = {D:.6f}"
    return d
app = Flask(__name__)

def parse_verilog(file_content: str) -> str:
    keywords = ["and", "or", "not", "nand", "nor", "xor", "xnor", "buf"]
    results = []

    for line in file_content.splitlines():
        line = line.strip()  # Remove spaces
        for key in keywords:
            if re.match(rf"^{key}\s+\w+\s*\(", line):  # Match gate with instance name
                start = line.find("(")
                end = line.find(")")
                if start != -1 and end != -1:
                    content = line[start + 1:end].split(",")
                    if len(content) > 1:
                        output = content[0].strip()
                        inputs = [inp.strip() for inp in content[1:]]
                        results.append(f"{key}: Output = {output}, Inputs = {', '.join(inputs)}")

    return "\n".join(results) if results else "No gates found"


import re
import string

def generate_netlist(verilog_code: str) -> str:
    # List of logic gates
    keywords = ["and", "or", "not", "nand", "nor", "xor", "xnor", "buf"]
    
    results = []
    header_lines = []
    logical_lines = []
    buffer = ""

    # Extract module definition, input, output, wire declarations
    for line in verilog_code.splitlines():
        line = line.strip()

        if re.match(r"^(module|input|output|wire|reg)\b", line):
            header_lines.append(line)

        if ";" in line:
            parts = line.split(";")
            for part in parts[:-1]:
                logical_lines.append(buffer + part.strip())
                buffer = ""
            buffer = parts[-1].strip()
        else:
            buffer += " " + line + " "
    
    if buffer:
        logical_lines.append(buffer.strip())

    # Fanout tracking
    fanout_counter = {}
    for line in logical_lines:
        for key in keywords:
            matches = re.finditer(rf"\b{key}\b", line, re.IGNORECASE)
            for match in matches:
                start = line.find("(", match.end())
                end = line.find(")", start)
                if start != -1 and end != -1:
                    content = [c.strip() for c in line[start + 1:end].split(",") if c.strip()]
                    if content:
                        output_port, input_ports = content[0], content[1:]
                        for input_port in input_ports:
                            fanout_counter[input_port] = fanout_counter.get(input_port, 0) + 1

    # Generate the netlist output
    instance_counter = 1
    for line in logical_lines:
        for key in keywords:
            matches = re.finditer(rf"\b{key}\b", line, re.IGNORECASE)
            for match in matches:
                start = line.find("(", match.end())
                end = line.find(")", start)
                if start != -1 and end != -1:
                    content = [c.strip() for c in line[start + 1:end].split(",") if c.strip()]
                    if content:
                        output_port, input_ports = content[0], content[1:]
                        fanout = fanout_counter.get(output_port, 1)

                        # Construct gate instance
                        gate_type = key.upper()
                        input_count = len(input_ports)
                        gate_instantiation = f"C12T28SOI_LR_{gate_type}{input_count}X{fanout}_P0 U{instance_counter} ( "

                        input_labels = list(string.ascii_uppercase)
                        for i, input_port in enumerate(input_ports):
                            gate_instantiation += f".{input_labels[i]}({input_port}), "
                        gate_instantiation += f".Z({output_port}) );"

                        results.append(gate_instantiation)
                        instance_counter += 1

    # Construct final module output
    output = "\n".join(header_lines) + "\n\n" + "\n".join(results) + "\n\nendmodule"
    return output


@app.route('/parse', methods=['POST'])
def parse_file():
    try:
        data = request.get_json()
        if not data or "verilog_code" not in data:
            return jsonify({"error": "Invalid JSON format or missing 'verilog_code'"}), 400  

        verilog_text = data["verilog_code"].strip()
        if not verilog_text:
            return jsonify({"error": "Verilog code is empty"}), 400  

        parsed_output = generate_netlist(verilog_text)
        return jsonify({"parsed_result": parsed_output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/upload',methods=["POST"])

# image upload 
def upload():
    if request.method == "POST":
        imagefile = request.files['image']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        imagefile.save("./uploadimage/"+filename)
        return jsonify({
            "message" : "Image Uploaded Succesfully"
        })


if __name__== "__main__":
    app.run()
