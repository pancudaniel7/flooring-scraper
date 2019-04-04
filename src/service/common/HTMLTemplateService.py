def create_product_details_template(labels: [], values: []):
    html_content: str = '<div>'
    for label, value in zip(labels, values):
        html_content += '<strong>{}: </strong><span>{}</span></br>'.format(label, value)
    html_content += '</div>'
    return html_content
