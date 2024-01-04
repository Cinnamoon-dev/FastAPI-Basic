import math
from sqlalchemy.orm import Query

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