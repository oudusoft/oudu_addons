import base64

def _uses_datas(attachment):
    return "datas" in attachment._fields

def image_bytes(value):
    if not value:
        return b""
    if hasattr(value, "content"):
        return bytes(value.content)
    return base64.b64decode(value)

def attachment_content(attachment):
    if _uses_datas(attachment):
        return image_bytes(attachment.datas)
    return image_bytes(attachment.raw)

def attachment_storage_values(attachment, content):
    content = bytes(content)
    if _uses_datas(attachment):
        return {"datas": base64.b64encode(content)}
    return {"raw": content}

def attachment_image_value(attachment):
    if _uses_datas(attachment):
        return attachment.datas
    return attachment.raw
