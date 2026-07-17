from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 50
    page_size_query_params = "page_size"
    max_page_size = 75