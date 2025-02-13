
from flask import Flask,request,jsonify
import numpy as np
import werkzeug
import werkzeug.utils
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

@app.route('/upload',methods=["POST"])
def upload():
    if(request.mathod == "POST"):
        imagefile = request.files['image']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        imagefile.save("./uploadimage/"+filename)
        return jsonify({
            "message" : "Image Uploaded Succesfully"
        })


if __name__== "__main__":
    app.run()
