from typing import Optional, TypeVar, Callable, Iterable, List, Any

T = TypeVar('T')  # pylint: disable=invalid-name


def first(_list: Iterable[T], predicate: Callable[[T], bool]) -> Optional[T]:
    """
    return the first element of the list if it match the predicate, otherwise it returns None
    """
    result = None
    for elt in _list:
        if predicate(elt):
            result = elt
            break

    return result


def extract_till(_list: Iterable[T], predicate: Callable[[T], bool]) -> List[T]:
    """
    Extrait les éléments d'un itérateur dans une sous liste
    jusqu'à ce que le prédicat soit valide.

    >>> _list = [1, 2, 3, 4, 5, 6]
    >>> extract_till(_list, lambda r: r > 4) # output : [1, 2, 3, 4]

    Si aucun élément de le premier élément de l'itérateur répond au prédicat, alors
    le résultat est une liste vide

    >>> _list = [1, 2, 3, 4, 5, 6]
    >>> extract_till(_list, lambda r: r > 0) # output : []
    """
    result = []
    for record in _list:
        if predicate(record):
            break

        result.append(record)

    return result


def count(elements: List[Any], condition: Optional[Callable] = None):
    'Returns the count of elements in list that satisfies the given condition'
    if condition:
        _count = len(list(filter(condition, elements)))
    else:
        _count = len(elements)
    return _count


def monotone(elements: Iterable[int], monotone_rotation: int = 4096) -> Iterable[int]:
    """
    transform a list of element in monotone counter
    """

    previous_element = None
    count_rotation = 0
    for element in elements:
        if previous_element is not None and element < (previous_element - monotone_rotation / 10):
            count_rotation += 1

        yield element + monotone_rotation * count_rotation
        previous_element = element
