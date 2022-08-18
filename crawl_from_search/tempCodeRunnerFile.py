html = get_search_html(keyword, 2)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'page.html')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)