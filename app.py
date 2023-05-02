#from _typeshed import OpenBinaryMode
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

# for colors
import numpy as np #needed for spec2col
from funktionen import spectralTrafo
from funktionen import spectralGuess

app = Flask(__name__)
app.config['SECRET_KEY'] = '4413'

@app.route("/rgbTransfromation", methods=['GET', 'POST'])
def rgbTransromation():
    if request.method == 'POST':
        data = request.get_json()['data']
        r = int(data[1:3], 16)
        g = int(data[3:5], 16)
        b = int(data[5:], 16)
        srgb_in = np.array([r,g,b])
        ill = request.get_json()['ill']
        obs = request.get_json()['obs']
        if ill == 'd50':
            if obs == '2':
                spectralData = list(spectralGuess.srgb2spec(srgb_in, ill = 'd50', obs = '2').clip(0,1))
            elif obs == '10':
                spectralData = list(spectralGuess.srgb2spec(srgb_in, ill = 'd50', obs = '10').clip(0,1))
            else:
                raise "Observer has to be either '2' or '10'"
        elif ill == 'd65':
            if obs == '2':
                spectralData = list(spectralGuess.srgb2spec(srgb_in, ill = 'd65', obs = '2').clip(0,1))
            elif obs == '10':
                spectralData = list(spectralGuess.srgb2spec(srgb_in, ill = 'd65', obs = '10').clip(0,1))
            else:
                raise "Observer has to be either '2' or '10'"
        else:
            "Illumination has to be either d50 or d65"
        # creation of srgb values

        srgb_50_2 = ref2spec(spectralData, obs='2', ill='d50')
        srgb_50_10 = ref2spec(spectralData, obs='10', ill='d50')
        srgb_65_2 = ref2spec(spectralData, obs='2', ill='d65')
        srgb_65_10 = ref2spec(spectralData, obs='10', ill='d65')
      
        data = {'spectrum': spectralData, 
                'srgb_50_2': srgb_50_2,
                'srgb_50_10': srgb_50_10,
                'srgb_65_2': srgb_65_2,
                'srgb_65_10': srgb_65_10}
        return jsonify(data), 200
    else:
        print('not good')
        return jsonify({'some': 'issue'})

@app.route('/spectralTransformation', methods=['GET', 'POST'])
def spectralTransformation():
    # POST request
    if request.method == 'POST':
        data = request.get_json()['data'] # extract data
        ref = np.array(data)

        srgb_50_2 = ref2spec(ref, obs='2', ill='d50')
        srgb_50_10 = ref2spec(ref, obs='10', ill='d50')
        srgb_65_2 = ref2spec(ref, obs='2', ill='d65')
        srgb_65_10 = ref2spec(ref, obs='10', ill='d65')

        srgb = {'srgb_50_2': srgb_50_2,
                'srgb_50_10': srgb_50_10, 
                'srgb_65_2': srgb_65_2,
                'srgb_65_10': srgb_65_10}

        return jsonify(srgb), 200
    # GET request
    else:
        Specturm = {'Spec': list(random_spec())}
        return jsonify(Specturm)  

@app.route('/')
def main_page():

    session['wavelength'] = [i for i in range(340,840,10)]
    session['reflectance'] = list(random_spec())

    # Umrechnung von Reflectance in srgb
    ref = np.array(session.get('reflectance'))
    srgb_50_2 = ref2spec(ref, obs='2', ill='d50')
    srgb_50_10 = ref2spec(ref, obs='10', ill='d50')
    srgb_65_2 = ref2spec(ref, obs='2', ill='d65')
    srgb_65_10 = ref2spec(ref, obs='10', ill='d65')
    
    return render_template('simpleTemplate.html', srgb_50_2 = srgb_50_2, srgb_50_10 = srgb_50_10, 
                    srgb_65_2 = srgb_65_2, srgb_65_10 = srgb_65_10, 
                    labels = session.get('wavelength'), values = session.get('reflectance'),
                    logo_path = "static/images/mein_logo_zugeschnitten.png", background_image_path = "static/images/spectrum.jpg",
                    favicon_path = "static/images/favicon.png")

def random_spec():
    sigma0 = 0.2    # alt nicht benötigt da uniform(0,1,1)
    sigma1 = 0.08   # alt sigma1 = 0.1
    sigma2 = 0.08   # alt sigma2 = 0.1
    alpha = 0.7     # alt alpha = 0 oder halt unten komplett rausstreichen
    s0 = np.random.normal(0.5, sigma0, 1).clip(0,1)
    #s0 = np.random.uniform(0,1,1)
    s1 = s0 + np.random.normal(0, sigma1, 1)
    s1 = s1.clip(0,1)
    normalVerteilung = np.random.normal(0, sigma2, 48)
    dataPoints = list(s0)
    dataPoints.append(s1[0])
    for value in normalVerteilung:
        nextPoint = dataPoints[-1] + alpha*(dataPoints[-1]-dataPoints[-2]) + value
        if nextPoint < 0:
            dataPoints.append(0)
        elif nextPoint > 1:
            dataPoints.append(1)
        else:
            dataPoints.append(nextPoint)
    return np.array(dataPoints)

def ref2spec(ref, obs, ill):
    xyz = spectralTrafo.spec2xyz(ref, obs=obs, ill=ill)
    #srgb = spectralTrafo.xyz2srgb(xyz, ill=ill)
    #srgb = np.clip(srgb*255, 0, 255)
    rgb = spectralTrafo.xyz2rgb(xyz)
    srgb = np.clip(spectralTrafo.gamma_correction(rgb)*255, 0, 255)
    srgb = list(np.rint(srgb))
    #print(xyz, rgb, srgb)
    return srgb