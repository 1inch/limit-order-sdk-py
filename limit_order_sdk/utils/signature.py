def signature_to_r_vs(signature: str) -> tuple[bytes, bytes]:
    r = int(signature[:66], 16)
    s = int(signature[66:130], 16)
    v = int(signature[130:], 16)

    if v == 0 or v == 27:
        vs = (0 << 255) | s
    elif v == 1 or v == 28:
        vs = (1 << 255) | s
    else:
        raise ValueError('Invalid signature')

    return r.to_bytes(32), vs.to_bytes(32)