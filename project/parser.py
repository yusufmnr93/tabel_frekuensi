def parse_years(value: str):
    """
    Ubah data YearsOfExperience ke angka (nilai tengah jika range).
    """
    if not isinstance(value, str):
        return None
    s = value.strip().lower()
    try:
        if "-" in s:  # misalnya "2-5"
            a, b = s.split("-")
            return (float(a) + float(b)) / 2
        elif "+" in s:  # misalnya "10+"
            return float(s.replace("+", ""))
        else:  # angka tunggal
            return float(s)
    except:
        return None
