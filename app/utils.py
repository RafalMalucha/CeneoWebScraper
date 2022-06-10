def get_item(ancestor, selector, attribute=None, return_list=False):
    try:
        if return_list:
            pros = ancestor.select(selector)
            return [item.get_text().strip() for item in pros]
        if attribute:
            return ancestor.select_one(selector)[attribute]
        return ancestor.select_one(selector).get_text().strip()
    except (AttributeError, TypeError):
        return None
