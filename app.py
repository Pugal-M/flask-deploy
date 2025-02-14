
from flask import Flask,request,jsonify
import numpy as np
import werkzeug
import werkzeug.utils
import re
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
        for key in keywords:
            if re.search(rf"\b{key}\b", line):
                start = line.find("(")
                end = line.find(")")
                if start != -1 and end != -1:
                    content = line[start + 1:end].split(",")
                    if len(content) > 1:
                        output = content[0].strip()
                        inputs = [inp.strip() for inp in content[1:]]
                        results.append(f"{key}: Output = {output}, Inputs = {', '.join(inputs)}")

    return "\n".join(results) if results else "No matches found"

@app.route('/parse', methods=['POST'])
def parse_file():
    try:
        data = request.get_json()
        verilog_text = data.get("verilog_code", "")

        if not verilog_text:
            return jsonify({"error": "No Verilog code provided"}), 400

        parsed_output = parse_verilog(verilog_text)
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
