python generate_template.py template template/data.json
python map_maker.py template dummyweb
python testimonials.py template dummyweb
python listing_pages_generator.py template dummyweb/listing mls_data.geojson
python listing_list_page.py template dummyweb/listings mls_data.geojson
python generic_page.py template dummyweb