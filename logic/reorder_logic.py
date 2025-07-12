def generate_reorder_suggestions(items, threshold=3):
    """
    Generate reorder suggestions based on item quantities
    """
    reorder_suggestions = []
    
    for item in items:
        if item['quantity'] <= threshold:
            # Simple reorder logic: reorder 10 units when quantity is low
            reorder_suggestions.append({
                'name': item['name'],
                'current_quantity': item['quantity'],
                'reorder_quantity': 10
            })
    
    return reorder_suggestions
