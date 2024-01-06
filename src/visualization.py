def convert_to_html(tokens_with_tags: list[str]) -> str:
    content = ""
    for token in tokens_with_tags:
        if token.startswith("<actor>"):
            token = token.replace("<actor>", "")
            content += f"<span class='actor'>{token}</span> "
        elif token.startswith("<activity>"):
            token = token.replace("<activity>", "")
            content += f"<span class='activity'>{token}</span> "
        elif token.startswith("<activity_data>"):
            token = token.replace("<activity_data>", "")
            content += f"<span class='activity-data'>{token}</span> "
        else:
            content += f"{token} "
    return content
