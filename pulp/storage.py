import os


def content_unit_path(content_unit_file, filename):
    # This is basically pulp.server.content.storage.get_path, but only needs to return the unit
    # type and unit key digest path components
    unit = content_unit_file.unit
    content_type = unit.content_type
    digest = unit.key_digest
    return os.path.join('units', content_type, digest[0:2], digest[2:], filename)
