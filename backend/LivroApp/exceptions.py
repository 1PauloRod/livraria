class BookError(Exception):
    """Exceção base para erros relacionados a livros."""
    pass

class BookNotFoundError(BookError):
    pass
        
        
class BookUnavailableError(BookError):
    pass


class BookAlreadyReturnedError(BookError):
    pass

