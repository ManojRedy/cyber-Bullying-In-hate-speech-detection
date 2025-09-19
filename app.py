from flask import Flask, render_template, request, jsonify
from detoxify import Detoxify
import json
from datetime import datetime

app = Flask(__name__)

# Load the model once when the app starts
model = Detoxify('multilingual')

# Global variable to store analysis history
analysis_history = []

@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze text sent from the form"""
    try:
        # Get text from the form
        text = request.form['text']
        
        if not text.strip():
            return jsonify({'error': 'Please enter some text'})
        
        # Get prediction from the model
        results = model.predict(text)
        
        # Convert results to a more readable format
        analysis = []
        for label, score in results.items():
            analysis.append({
                'label': label,
                'score': float(score),
                'percentage': f"{score*100:.2f}%"
            })
        
        # Check if toxic
        is_toxic = float(results['toxicity']) > 0.75
        
        # Create result object for history
        result_data = {
            'text': text,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'results': analysis,
            'is_toxic': is_toxic,
            'toxicity_score': float(results['toxicity'])
        }
        
        # Add to history (keep last 100 analyses)
        analysis_history.append(result_data)
        if len(analysis_history) > 100:
            analysis_history.pop(0)
        
        return jsonify({
            'success': True,
            **result_data
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})

@app.route('/analyze-batch', methods=['POST'])
def analyze_batch():
    """Analyze multiple texts at once"""
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        
        if not texts:
            return jsonify({'error': 'No texts provided'})
        
        results = []
        for text in texts:
            if text.strip():  # Only analyze non-empty texts
                prediction = model.predict(text)
                results.append({
                    'text': text,
                    'toxicity': float(prediction['toxicity']),
                    'is_toxic': float(prediction['toxicity']) > 0.75
                })
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})

@app.route('/history')
def get_history():
    """Get analysis history"""
    return jsonify({
        'success': True,
        'count': len(analysis_history),
        'history': analysis_history
    })

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear analysis history"""
    global analysis_history
    analysis_history = []
    return jsonify({'success': True, 'message': 'History cleared'})

if __name__ == '__main__':
    app.run(debug=True)