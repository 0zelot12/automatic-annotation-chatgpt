def render_html(document):
    html_output = ""
    for token, ner_tag in zip(document.tokens, document.ner_tags):
        html_output += "<span>" + token + "<span>"
