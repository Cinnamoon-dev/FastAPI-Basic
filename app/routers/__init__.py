import math
from sqlalchemy.orm import Query

# item pagination
def paginate(query: Query, page: int = 1, rows_per_page: int = 1):
    itens_count = query.count()
    pages_count = math.ceil(itens_count / rows_per_page)
    prev = None
    next = None

    if page - 1 > 0:
        prev = page - 1
    
    if page + 1 < pages_count :
        next = page + 1

    output = {
        "itens": [],
        "pagination": {
            "pages_count": pages_count,
            "itens_count": itens_count,
            "itens_per_page": rows_per_page,
            "prev": prev,
            "next": next,
            "current": page
        },
        "error": False
    }

    start = page * rows_per_page - rows_per_page
    stop = page * rows_per_page

    itens = query.slice(start, stop)
    return itens, output

# -------------------------------------------------------------------------------------------------- #

# update table line
def instance_update(instance, request_json):
    """
    This function updates every key received from the request in an instance of a table, if the key exists in that table.
    
    Example: The table User has three columns (id, name, email) and the request object has five fields (name, age, bloodType, email, address).
    The updated fields in the instance will be (name, email).

    The parameter instance should be a query from a table. 

    `instance = User.query.get(id)`
    """

    instance_keys = list(instance.to_dict().keys())

    for key in instance_keys:
        if key in request_json:
            setattr(instance, key, request_json.get(key))
    
    if "email" in request_json:
        setattr(instance, 'email', request_json.get("email").lower())
    
    # TODO
    # Hash password
    if "password" in request_json:
        setattr(instance, 'password', request_json.get("password"))