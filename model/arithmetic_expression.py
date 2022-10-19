from model.arithmetic_operation_base import ArithmeticOperation


class ArithmeticExpression:
    PARENTHESES_OPEN = list('([{')
    PARENTHESES_CLOSE = list(')]}')

    __ERROR_WRONG_EXPRESSION = 'Ошибка: Вероятно выражение задано некорректно!'
    #__ERROR_NO_OPERATION_DEFINED = 'Ошибка: Оерация "{}" не определена!'

    def __init__(self, operations_set: set[ArithmeticOperation]):
        if operations_set is None:
            raise ValueError

        self.OPERATION_SIGNS = list(map(lambda op: op.SIGN, operations_set))

        # # словарь { значёк операции : модель операции }
        # self.operations = {op_model.SIGN: op_model for op_model in operations_set}

        # список словарей { значёк операции : модель операции } отсортированный по возрастанию PRIORITY
        # (операции с меньшим приоритетом выполняются раньше операций с большим приоритетом)
        self.operations_by_priority_asc = [{op.SIGN: op for op in operations_set if op.PRIORITY == pr}
                                           for pr in sorted(set([o.PRIORITY for o in operations_set]))]

    def calculate_expression_string(self, expression_str: str) -> tuple[float, str]:
        # stage 1: normalize string
        normalized_repr = self.__normalize_expression_string(expression_str)
        # stage 2: convert to list of floats and special symbols
        expression_lst = ArithmeticExpression.__expression_string_to_list(
            normalized_repr)
        # stage 3: replace all items representing sub-expressions in parentheses by equal lists
        ArithmeticExpression.__convert_to_subexpressions_tree(expression_lst)
        # stage 4: calculate all atomic "sub-expression" lists
        return self.__solve_subexpressions_tree(expression_lst)

    @staticmethod
    def __remove_consequent_duplicates(string: str, character: str):
        character_twice = str(character)*2
        length = -1
        while len(string) != length:
            length = len(string)
            string = string.replace(character_twice, character)
        return string

    def __normalize_expression_string(self, expr_str: str):
        NUM_MINUS_SIGN_ALIAS = 'm'
        expr_str = ''.join(expr_str.strip().split())
        expr_str = expr_str.replace(',', '.')
        expr_str = expr_str[::-1] \
            .replace('-+', NUM_MINUS_SIGN_ALIAS + '+') \
            .replace('--', NUM_MINUS_SIGN_ALIAS + '-')
        expr_str = ArithmeticExpression.__remove_consequent_duplicates(
            expr_str, '+')
        expr_str = ArithmeticExpression.__remove_consequent_duplicates(
            expr_str, '-')

        # после удаления дубликатов можно удалить лишний + после (
        # и заменить - после ( на временный алиас
        for opening_parenthesis in ArithmeticExpression.PARENTHESES_OPEN:
            expr_str = expr_str.replace('-' + opening_parenthesis,
                                        NUM_MINUS_SIGN_ALIAS + opening_parenthesis)
            expr_str = expr_str.replace('+' + opening_parenthesis,
                                        opening_parenthesis)
        expr_str = expr_str[::-1]
        if expr_str[0] == '-':
            expr_str = expr_str.replace('-', NUM_MINUS_SIGN_ALIAS, 1)
        expr_str = expr_str.replace('+-', '-').replace('-+', '-')

        for spec_symb in self.OPERATION_SIGNS \
            + ArithmeticExpression.PARENTHESES_OPEN \
                + ArithmeticExpression.PARENTHESES_CLOSE:
            expr_str = expr_str.replace(spec_symb, ' ' + spec_symb + ' ')

        expr_str = expr_str.replace(NUM_MINUS_SIGN_ALIAS, '-')

        return expr_str

    @staticmethod
    def __expression_string_to_list(normalized_expr_str):
        expr_lst = normalized_expr_str.split()
        # expr_lst = list(map(lambda x: float(x) if x.isdigit() else x, expr_lst)) # bad! подходит для int

        def to_suitable_value(x):
            try:
                return float(x)
            except ValueError:
                return str(x)

        expr_lst = list(map(to_suitable_value, expr_lst))
        return expr_lst

    @staticmethod
    def __get_first_index(src_lst, values_lst):
        last_idx = len(src_lst) - 1
        return next(i if matches else -1 for i, v in enumerate(src_lst) if (matches := v in values_lst) or i == last_idx)

    @staticmethod
    def __get_first_index_backward(src_lst, from_index, values_lst):
        while from_index >= 0:
            if src_lst[from_index] in values_lst:
                return from_index
            from_index -= 1
        return -1

    @staticmethod
    def __convert_to_subexpressions_tree(expr_lst: list):
        """ Извлекаем из списка первое попавшееся элементарное выражение в скобках,
        заменяя все элементы исходного списка, относящиеся к найденному выражению,
        включая скобки, на один единственный элемент содержащий список,
        представляющий найденное элементарное выражение (без скобок).
        Возвращает индекс элемента-списка, представляющего элементарное выражение.
        """
        if len(expr_lst) < 2:
            return

        close_idx = ArithmeticExpression.__get_first_index(
            expr_lst, ArithmeticExpression.PARENTHESES_CLOSE)
        if close_idx == -1:
            return

        # закрывающая скобка в начале выражения -> удаляем и повторяем заново:
        if close_idx == 0:
            expr_lst.pop(0)

            ArithmeticExpression.__convert_to_subexpressions_tree(expr_lst)

        open_idx = ArithmeticExpression.__get_first_index_backward(
            expr_lst, close_idx-1, ArithmeticExpression.PARENTHESES_OPEN)
        # не найдена парная открывающая скобка -> удаляем плохие элементы и повтряем заново:
        if open_idx == -1:
            while open_idx < close_idx:
                expr_lst.pop(0)
                open_idx += 1

            ArithmeticExpression.__convert_to_subexpressions_tree(expr_lst)

        # теперь возможны следующие варианты:
        # 1. подвыражение пусто -> просто удаляем скобки и повторяем поиск
        # 2. подвыражение содержит один элемент -> удаляем скобки и оставляем элемент, только если это число
        # 3. подвыражение сложное -> заменяем на список
        subexpr_items_count = close_idx - open_idx - 1
        # 1.->
        if subexpr_items_count == 0:
            expr_lst.pop(open_idx)
            expr_lst.pop(open_idx)
            # eturn extract_next_subexpression(expr_lst)
        # 2. ->
        elif subexpr_items_count == 1:
            expr_lst.pop(open_idx)
            if not isinstance(expr_lst[open_idx], str):
                expr_lst.pop(open_idx+1)
            else:
                expr_lst.pop(open_idx)
                expr_lst.pop(open_idx)
        # 3. ->
        else:
            subexpr_lst = expr_lst[open_idx+1:close_idx]
            while close_idx > open_idx:
                expr_lst.pop(open_idx)
                close_idx -= 1
            expr_lst[open_idx] = subexpr_lst

        ArithmeticExpression.__convert_to_subexpressions_tree(expr_lst)

    def __perform_sub_operation_over_list(self, atomic_expr_lst: list, index, operation_model: ArithmeticOperation) -> tuple[float, str]:
        operation_model.init(
            atomic_expr_lst[index-1], atomic_expr_lst[index+1])
        res, err = operation_model.calc()
        if err:
            return (None, err)

        atomic_expr_lst[index] = res
        atomic_expr_lst.pop(index-1)
        atomic_expr_lst.pop(index)
        return (res, err)

    def __perform_next_operation(self, atomic_expr_lst: list) -> tuple[float, str]:
        for priority_operations in self.operations_by_priority_asc:
            priority_signs = list(priority_operations.keys())

            for i in range(len(atomic_expr_lst) - 1):
                item = atomic_expr_lst[i]
                if item in priority_signs:
                    operation_model = priority_operations[item]
                    # возвращаем, для propagation сообщения об ошибки по стеку вызовов, если таковая вдруг возникла
                    return self.__perform_sub_operation_over_list(atomic_expr_lst, i, operation_model)

    def __calculate_atomic_expression(self, atomic_expr_lst) -> tuple[float, str]:
        crnt_len = len(atomic_expr_lst)
        if crnt_len > 1:
            if atomic_expr_lst[0] == '-' and (not isinstance(atomic_expr_lst[1], str)):
                atomic_expr_lst[1] = -atomic_expr_lst[1]
                atomic_expr_lst.pop(0)
                return self.__calculate_atomic_expression(atomic_expr_lst)
        elif crnt_len == 1:
            if not isinstance(atomic_expr_lst[0], str):
                return (atomic_expr_lst[0], None)
            else:
                return (0, ArithmeticExpression.__ERROR_WRONG_EXPRESSION)
        else:
            return (0, None)

        res = None
        prior_len = -1
        while (crnt_len := len(atomic_expr_lst)) != prior_len and crnt_len > 1:
            prior_len = crnt_len
            res, err = self.__perform_next_operation(atomic_expr_lst)
            if err:
                return (None, err)

        if crnt_len == 1:  # когда всё ОК!
            if res is None:  # например, изначально подвыражение это одно число в скобках
                return (atomic_expr_lst[0], None)
            else:
                return (res, None)
        else:
            return (res, f'Неизвестная ошибка при вычислении подвыражения "{" ".join(map(str, atomic_expr_lst))}".')

    @ staticmethod
    def __is_atomic(expr_lst: list):
        for item in expr_lst:
            if isinstance(item, list):
                return False
        return True

    def __solve_subexpressions_tree(self, subexpressions_tree) -> tuple[float, str]:
        if ArithmeticExpression.__is_atomic(subexpressions_tree):
            return self.__calculate_atomic_expression(subexpressions_tree)

        size = len(subexpressions_tree)
        i = 0
        while i < size:
            item = subexpressions_tree[i]
            if isinstance(item, list):
                res: float = None
                err: str = None
                if ArithmeticExpression.__is_atomic(item):
                    res, err = self.__calculate_atomic_expression(item)
                else:
                    # если наткнулись на список-подвыражение, но не атомарное, то рекурсивно проходимся и по нему:
                    res, err = self.__solve_subexpressions_tree(item)

                if err:
                    return (None, err)

                # меняем список-подвыражение на значение результата подвыражения:
                subexpressions_tree[i] = res

            i += 1

        return self.__solve_subexpressions_tree(subexpressions_tree)
