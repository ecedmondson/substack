API_BASE = "/api/"

def make_router_prefix_pattern(subpaths: list):
    return API_BASE + "/".join(subpaths)