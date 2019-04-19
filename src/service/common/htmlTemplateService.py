from src.service.common.collectorService import get_soup_by_content, tags_text


def create_product_template(labels: [], values: []):
    html_content: str = '<div>'
    for label, value in zip(labels, values):
        html_content += '<div><strong>{}: </strong><span>{}</span></div>'.format(label, value)
    html_content += '</div>'
    return html_content


def create_second_product_template(values: []):
    html_content: str = '<div>'
    for value in values:
        html_content += '<div><span>{}</span></div>'.format(value)
    html_content += '</div>'
    return html_content


def extract_product_details_from_html(content_html: str, labels_selector: str, values_selector: str):
    soup = get_soup_by_content(content_html)
    labels = tags_text(labels_selector, soup)
    values = tags_text(values_selector, soup)
    return [labels, values]