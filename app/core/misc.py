import re
def get_email_domain(email):
    return re.search(r"@([\w.]+)", email).group(1)
