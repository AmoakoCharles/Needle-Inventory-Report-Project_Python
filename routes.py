from flask import Blueprint, render_template, request
import math
from data_loader import load_inventory_data, apply_filters
from exporter import export_to_csv, export_to_excel, export_to_pdf
from config import PER_PAGE

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    data = load_inventory_data()
    factory_filter = request.args.get('factory', '')
    location_filter = request.args.get('location', '')
    needle_filter = request.args.get('needle', '')
    page = int(request.args.get('page', 1))

    filtered_data = apply_filters(data, factory_filter, location_filter, needle_filter)

    total_items = len(filtered_data)
    total_pages = math.ceil(total_items / PER_PAGE)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    paginated_data = filtered_data.iloc[start:end]

    factories = sorted(data['factory'].dropna().unique())
    locations = sorted(data['stock location'].dropna().unique())
    needles = sorted(data['needle id'].dropna().unique())

    return render_template('index.html',
                            tables=paginated_data.to_dict(orient='records'),
                            factories=factories,
                            locations=locations,
                            needles=needles,
                            current_factory=factory_filter,
                            current_location=location_filter,
                            current_needle=needle_filter,
                            page=page,
                            total_pages=total_pages)

@bp.route('/export/csv')
def export_csv():
    data = load_inventory_data()
    factory_filter = request.args.get('factory', '')
    location_filter = request.args.get('location', '')
    needle_filter = request.args.get('needle', '')
    filtered_data = apply_filters(data, factory_filter, location_filter, needle_filter)
    return export_to_csv(filtered_data)

@bp.route('/export/excel')
def export_excel():
    data = load_inventory_data()
    factory_filter = request.args.get('factory', '')
    location_filter = request.args.get('location', '')
    needle_filter = request.args.get('needle', '')
    filtered_data = apply_filters(data, factory_filter, location_filter, needle_filter)
    return export_to_excel(filtered_data)

@bp.route('/export/pdf')
def export_pdf():
    data = load_inventory_data()
    factory_filter = request.args.get('factory', '')
    location_filter = request.args.get('location', '')
    needle_filter = request.args.get('needle', '')
    filtered_data = apply_filters(data, factory_filter, location_filter, needle_filter)
    return export_to_pdf(filtered_data)
