def create_product_template(labels: [], values: [], product_code: str = ''):
    html_content: str = '<div>'
    if product_code != '':
        html_content += '<div><strong>Product code: </strong><span>{}</span></div>'.format(product_code)
    for label, value in zip(labels, values):
        html_content += '<div><strong>{}: </strong><span>{}</span></div>'.format(label, value)
    html_content += '</div>'
    return html_content


def create_second_product_template(values: [], product_code: str = ''):
    html_content: str = '<div>'
    if product_code != '':
        html_content += '<div><strong>Product code: </strong><span>{}</span></div>'.format(product_code)
    for value in values:
        html_content += '<div><span>{}</span></div>'.format(value)
    html_content += '</div>'
    return html_content
