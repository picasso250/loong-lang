def pretty_dict(obj):
    s = ["{"]
    for k,v in obj.items():
        if k.startswith("__"):
            s.append(f"  {k}: ...,")
        else:
            vs = f"  {k}: "+pretty_var(v)+","
            s.append(vs)
    s.append("}")
    return "\n".join(s)
def pretty_var(obj) -> str:
    if isinstance(obj, dict):
        return pretty_dict(obj)
    else:
        return str(obj)