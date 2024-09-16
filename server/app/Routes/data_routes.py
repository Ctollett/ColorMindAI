import logging
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.Models.site_data import SiteData
from app.Middleware.auth import token_required
from datetime import datetime
from app.Controllers.Scraper.scraper import scrape_website
from flask_cors import cross_origin
from app.extensions import mongo
from bson.objectid import ObjectId

main_bp = Blueprint('main', __name__)

@main_bp.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    if url:
        results = scrape_website(url)
        logging.info("Scraping results: %s", results)
        
        if results:
            # Make sure you are accessing the correct keys and the data structure matches what is expected
            response_data = {
                'color_palette': results['processed_colors'].get('color_palette', []),
                'contrast_ratio': results['processed_colors'].get('contrast', 0),
                'harmony_score': results['processed_colors'].get('harmony', 0),
                'best_trait': results['processed_colors'].get('best_trait', 'No dominant trait'),
                'analysis': results.get('analysis', 'No analysis available')
            }
            logging.info("Response data prepared: %s", response_data)
            return jsonify(response_data), 200
        else:
            return jsonify({'error': 'Failed to process the website data'}), 500
    return jsonify({'error': 'No URL provided'}), 400




@main_bp.route('/save', methods=['POST'])
@token_required
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def save(current_user):
    site_data = request.json
    site_data['user_id'] = str(current_user.id)
    
    # Extract fonts from the request data
    fonts = site_data.get('fonts', {})
    heading_fonts = fonts.get('heading_fonts', [])
    subheading_fonts = fonts.get('subheading_fonts', [])
    paragraph_fonts = fonts.get('paragraph_fonts', [])
    
    site_data['data'] = {
        'fonts': {
            'heading_fonts': heading_fonts,
            'subheading_fonts': subheading_fonts,
            'paragraph_fonts': paragraph_fonts
        },
        'colors': site_data.get('colors', []),
        'technologies': site_data.get('technologies', []),
        'analysis': site_data.get('analysis', ''),
        'layout_details': site_data.get('layout_details', {}),
        'screenshot_url': site_data.get('screenshot_url', '')
    }

    try:
        mongo.db.site_data.insert_one(site_data)
        return jsonify({'message': 'Data saved successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/delete/<site_data_id>', methods=['DELETE'])
@token_required
def delete(current_user, site_data_id):

    site_data = SiteData.get(site_data_id)
    if not site_data:
        return jsonify({'error': 'Site data not found'}), 404
    
 
    if site_data['user_id'] != current_user.id:
        return jsonify({'error': 'Unauthorized to delete this data'}), 403


    try:
        SiteData.delete(site_data_id)
        return jsonify({'message': 'Data deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to delete data: ' + str(e)}), 500

@main_bp.route('/site-details/<site_id>', methods=['GET', 'OPTIONS'])
@token_required
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def get_site_details(current_user, site_id):
    logging.info(f"Received request for {request.method} {request.url}")
    try:
        site_data = mongo.db.site_data.find_one({"_id": ObjectId(site_id)})
        logging.info(f"Fetched site data: {site_data}")
        
        if not site_data:
            logging.error("No site found with that ID")
            return jsonify({'error': 'Site not found'}), 404
        
        if site_data['user_id'] != str(current_user.id):
            return jsonify({'error': 'Unauthorized access'}), 403
        
        # Convert MongoDB BSON to JSON
        site_data['_id'] = str(site_data['_id'])
        return jsonify(site_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

