class Book:
    """
    The Book class - just a little class to make the attribute handling easier - which it does, by a lot
    """
    def __init__(self, parent_book: str, page_id, page_slug: str, filename):
        self.parent_book = parent_book
        self.page_id = page_id
        self.page_slug = page_slug
        self.filename = filename

    def __str__(self):
        return f"Book: {self.parent_book}: PageID {self.page_id}, Page slug: {self.page_slug}, Filename: {self.filename} "