def pretty_dump_json(obj, indent=4, level=0, max_length=20):
    compact_result = custom_json_dumps_compact(obj)
    if len(compact_result) <= max_length:
        return compact_result
    
    spacing = ' ' * (indent * level)
    next_spacing = ' ' * (indent * (level + 1))
    if isinstance(obj, dict):
        items = []
        for key, value in obj.items():
            item = next_spacing + repr(key) + ': ' + pretty_dump_json(value, indent, level + 1, max_length)
            items.append(item)
        return '{\n' + ',\n'.join(items) + '\n' + spacing + '}'
    elif isinstance(obj, list):
        items = []
        for item in obj:
            items.append(next_spacing + pretty_dump_json(item, indent, level + 1, max_length))
        return '[\n' + ',\n'.join(items) + '\n' + spacing + ']'
    else:
        return repr(obj)

def custom_json_dumps_compact(obj):
    if isinstance(obj, dict):
        items = []
        for key, value in obj.items():
            items.append(repr(key) + ': ' + custom_json_dumps_compact(value))
        return '{' + ', '.join(items) + '}'
    elif isinstance(obj, list):
        items = []
        for item in obj:
            items.append(custom_json_dumps_compact(item))
        return '[' + ', '.join(items) + ']'
    else:
        return repr(obj)

data = {
    "name": "Alice",
    "age": 30,
    "children": [
        {
            "name": "Bob",
            "age": 10
        },
        {
            "name": "Charlie",
            "age": 5
        }
    ]
}

print(pretty_dump_json(data, indent=2, max_length=44))
