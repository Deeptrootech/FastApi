def paginate(query, skip: int, limit: int):
    total = query.count()
    data = query.offset(skip).limit(limit).all()
    return total, data
