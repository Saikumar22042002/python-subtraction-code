import logging
from flask import Flask, jsonify, request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint to confirm service is running."""
    return jsonify({"status": "healthy"}), 200


@app.route('/subtract', methods=['GET'])
def subtract():
    """Subtracts parameter 'b' from 'a'."""
    a_val = request.args.get('a')
    b_val = request.args.get('b')

    if a_val is None or b_val is None:
        logger.warning("Missing one or more required parameters: 'a', 'b'.")
        return jsonify({"error": "Missing required query parameters: 'a' and 'b'"}), 400

    try:
        a_float = float(a_val)
        b_float = float(b_val)
        result = a_float - b_float
        logger.info(f"Subtraction successful: {a_float} - {b_float} = {result}")
        return jsonify({"a": a_float, "b": b_float, "result": result}), 200
    except (ValueError, TypeError):
        logger.error(f"Invalid input provided: a='{a_val}', b='{b_val}'")
        return jsonify({"error": "Invalid input. 'a' and 'b' must be numbers."}), 400


@app.route('/', methods=['GET'])
def index():
    """Index route providing basic service information."""
    return jsonify({"message": "Subtraction API. Use /subtract?a=<num>&b=<num>"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
