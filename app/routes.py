from flask import Flask, redirect, render_template, url_for, request, flash, Response
from markupsafe import Markup
from datetime import datetime
from flask import current_app as app
from .api import *  # Assuming this imports your logic for interacting with the API
import csv
from io import StringIO

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # POST request
    if request.method == 'POST':
        sel = request.form['sel']
        query = request.form['search']
        # "Find All Drugs" selected
        if sel == 'getDrugs':
            return redirect(url_for('drugs', query=query))
        # "Approximate Match" selected
        elif sel == 'getApproximateMatch':
            return redirect(url_for('approx_match', query=query))
        # "Image" selected
        elif sel == 'image':
            return redirect(url_for('img_srv', query=query))
        # No function was selected
        else:
            flash(Markup('<strong>Please select a function.</strong> Not sure which to use? Click <a href="/help" class="alert-link">here</a> to view the help page.'))
            return render_template('search.html')
    # GET request
    else:
        return render_template('search.html')

@app.route('/drugs/<query>')
def drugs(query):
    try:
        res = rxnorm(query, 'getDrugs')
        return render_template('drugs.html', meds=res)
    except:
        return render_template('error.html')

@app.route('/approx-match/<query>')
def approx_match(query):
    try:    
        res = rxnorm(query, 'getApproximateMatch')
        return render_template('approx-match.html', meds=res, search_term=query)
    except:
        return render_template('error.html')
    
@app.route('/image/<query>')
def img_srv(query):
    try:
        img = {}
        img['keyword'] = query
        r = requests.post('https://image-srv.herokuapp.com/image', data=img)
        res = r.json()
        return render_template('image.html', url=res['image'])
    except:
        return render_template('error.html')

@app.route('/download')
def download():
    search_term = request.args.get('term')
    # Assuming `meds` is the result of your search function,
    # you need to get that data for the search_term.
    meds = get_meds(search_term)  # Replace this with your logic to fetch results for `search_term`

    # Create CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['RxNorm Name', 'RxCUI', 'Prescribable', 'Source', 'Score'])

    for med in meds:
        writer.writerow([med['RxNorm Name'], med['RxCUI'], med['PRESCRIBABLE'], med['Source'], med['score']])

    # Set CSV response headers
    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={search_term}_results.csv'}
    )

@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
