from flask import request, current_app
from sqlalchemy.orm import Query
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import math



class PaginationConfig:
    """ Конфигурация пагинации """
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100
    MIN_PER_PAGE = 1


class PaginationResult:
    """ Результат пагинации """

    def __init__(
        self,
        items: List[Any],
        total: int,
        page: int,
        per_page: int,
        pages: int
    ):
        self.items = items
        self.total = total
        self.page = page
        self.per_page = per_page
        self.pages = pages
        self.has_next = page < pages
        self.has_prev = page > 1

    def to_dict(self, include_meta: bool = True) -> Dict[str, Any]:
        """ Преобразовать в словарь """
        result = {
            'items': self.items,
            'pagination': {
                'total': self.total,
                'page': self.page,
                'per_page': self.per_page,
                'pages': self.pages,
                'has_next': self.has_next,
                'has_prev': self.has_prev
            }
        }

        if include_meta:
            result['meta'] = {
                'page': self.page,
                'per_page': self.per_page,
                'total_pages': self.pages,
                'total_items': self.total
            }

        return result
    

class PaginationService:
    """ Сервис для работы с пагинацией """

    @staticmethod
    def get_pagination_params() -> Tuple[int, int]:
        """
        Получить параметры пагинации запроса
        
        Returns:
            Tuple[int, int]: (page, per_page)
        """
        try:
            page = request.args.get('page', PaginationConfig.DEFAULT_PAGE, type=int)
            per_page = request.args.get('per_page', PaginationConfig.DEFAULT_PER_PAGE, type=int)

            # Валидация
            page = max(1, page)
            per_page = max(
                PaginationConfig.MIN_PER_PAGE,
                min(per_page, PaginationConfig.MAX_PER_PAGE)
            )

            return page, per_page
        
        except (ValueError, TypeError):
            return PaginationConfig.DEFAULT_PAGE, PaginationConfig.DEFAULT_PER_PAGE
        
    @staticmethod
    def get_filter_params(filter_keys: List[str]) -> Dict[str, Any]:
        """
        Получить параметры фильтрации из запроса

        Args:
            filter_keys: Список ключей для фильтрации
        
        Returns:
            Dict[str, Any]: Параметры фильтрации
        """
        filters = {}
        for key in filter_keys:
            value = request.args.get(key)
            if value is not None and value != '':
                # Преобразование типов
                if value.lower() in ['true', 'false']:
                    filters[key] = value.lower() == 'true'
                elif value.isdigit():
                    filters[key] = int(value)
                else:
                    filters[key] = value
        
        return filters

    @staticmethod
    def get_sort_params(
        default_sort: str = 'created_at',
        default_order: str = 'desc',
        allowed_fields: Optional[List[str]] = None
    ) -> Tuple[str, str]:
        """
        Получить параметры сортировки

        Args:
            default_sort: Поле для сортировки по умолчанию
            default_order: Порядок сортировки по умолчанию
            allowed_fields: Разрешенные поля для сортировки

        Returns:
            Tuple[str, str]: (sort_field, sort_order)
        """
        sort_by = request.args.get('sort_by', default_sort)
        sort_order = request.args.get('sort_order', default_order)

        # Валидация порядка сортировки
        if sort_order.lower() not in ['asc', 'desc']:
            sort_order = default_order

        # Валидация поля сортировки
        if allowed_fields and sort_by not in allowed_fields:
            sort_by = default_sort

        return sort_by, sort_order
    
    @staticmethod
    def paginate_query(
        query: Query,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        error_out: bool = False
    ) -> PaginationResult:
        """
        Выполнить пагинацию запроса

        Args:
            query: SQLAlchemy Query объект
            page: Номер страницы (если None - берется из запроса)
            per_page: Кол-во элементов на странице (если None - берется из запроса)
            error_out: Выбрасывать ошибку при несуществующей странице

        Returns:
            PaginationResult: Результат пагинации
        """
        if page is None or per_page is None:
            page, per_page = PaginationService.get_pagination_params()

        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=error_out
        )

        return PaginationResult(
            items=pagination.items,
            total=pagination.total,
            page=page,
            per_page=per_page,
            pages=pagination.pages
        )
    
    @staticmethod
    def create_response(
        items: List[Any],
        total: int,
        page: int,
        per_page: int,
        pages: int,
        additional_data: Optional[Dict[str, Any]] = None,
        include_pagination_meta: bool = True
    ) -> Dict[str, Any]:
        """
        Создать стандартизированный ответ с пагинацией
        
        Args:
            items: Список элементов
            total: Общее кол-во
            page: Текущая страница
            per_page: Кол-во на странице
            pages: Всего страниц
            additional_data: Дополнительные данные для ответа
            include_pagination_meta: Включать ли метаданные пагинации
        
        Returns:
            Dict[str, Any]: Словарь для ответа JSON
        """
        response = {
            'data': items,
            'pagination': {
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': pages,
                'has_next': page < pages,
                'has_prev': page > 1
            }
        }

        if include_pagination_meta:
            response['meta'] = {
                'page': page,
                'per_page': per_page,
                'total_pages': pages,
                'total_items': total
            }

        if additional_data:
            response.update(additional_data)
        
        return response
    
    @staticmethod
    def paginate_and_response(
        query: Query,
        serializer_func=None,
        additional_data: Optional[Dict[str, Any]] = None,
        **pagination_kwargs
    ) -> Tuple[Dict[str, Any], int]:
        """
        Упрощенный метод для пагинации и создания ответов
        
        Args:
            query: SQLAlchemy Query
            serializer_func: Функция для сериализации элементов
            additional_data: Дополнительные данные
            pagination_kwargs: Аргументы для paginatie_query

        Returns:
            Tuple[Dict[str, Any], int]: (response_data, status_code)
        """
        try:
            pagination_result = PaginationService.paginate_query(query, **pagination_kwargs)

            items = pagination_result.items
            if serializer_func:
                items = [serializer_func(item) for item in items]

            response_data = PaginationService.create_response(
                items=items,
                total=pagination_result.total,
                page=pagination_result.page,
                per_page=pagination_result.per_page,
                pages=pagination_result.pages,
                additional_data=additional_data
            )

            return response_data, 200
        
        except Exception as e:
            current_app.logger.error(f'Ошибка пагинации: {str(e)}')
            return {'error': str(e)}, 500
        

def with_pagination(default_per_page: int = 20):
    """
    Декоратор для автоматической обработки пагинации в роутах

    Args:
        default_per_page: Кол-во элементов по умолчанию
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            page, per_page = PaginationService.get_pagination_params()

            if default_per_page and per_page == PaginationConfig.DEFAULT_PER_PAGE:
                per_page = default_per_page
            
            request.pagination_page = page
            request.pagination_per_page = per_page

            return func(*args, **kwargs)
        return wrapper
    return decorator
