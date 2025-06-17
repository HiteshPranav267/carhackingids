def hex_to_int(x):
    try:
        return int(str(x), 16)
    except:
        return 0  # fallback for bad data
