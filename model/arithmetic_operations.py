# реализации модели "арифметическая операция"

from model.arithmetic_operation_base import ArithmeticOperation

# model API#1: concrete types: Mult, Div, etc


class Multiplication(ArithmeticOperation):
    SIGN = '*'
    NAME = 'произведение'
    PRIORITY = 1

    @classmethod
    def _get_result(cls):
        return (cls.operand_a * cls.operand_b, None)


class Division(ArithmeticOperation):
    SIGN = '/'
    NAME = 'деление'
    PRIORITY = 1
    __ERROR_DIV_BY_ZERO = 'Ошибка: Попытка деления на ноль!'

    @classmethod
    def _get_result(cls):
        if cls.operand_b == 0:
            return (None, Division.__ERROR_DIV_BY_ZERO)
        return (cls.operand_a/cls.operand_b, None)


class Addition(ArithmeticOperation):
    SIGN = '+'
    NAME = 'сложение'
    PRIORITY = 2

    @classmethod
    def _get_result(cls):
        return (cls.operand_a + cls.operand_b, None)


class Substraction(ArithmeticOperation):
    SIGN = '-'
    NAME = 'вычитание'
    PRIORITY = 2

    @classmethod
    def _get_result(cls):
        return (cls.operand_a - cls.operand_b, None)


class Exponentiation(ArithmeticOperation):
    SIGN = '^'
    NAME = 'возведение в степень'
    PRIORITY = 0
    __ERROR_ZERO_POW_ZERO = 'Ошибка: Результат операции неопределён. Попытка возведения нуля в нулевую степень!'
    __ERROR_ZERO_POW_NEG = 'Ошибка: Недопустимая операция возведения нулевого значения в отрицательную степень!'

    @classmethod
    def _get_result(cls):
        if cls.operand_a == 0 and cls.operand_b == 0:
            return (None, cls.__ERROR_ZERO_POW_ZERO)
        elif cls.operand_a == 0 and cls.operand_b < 0:
            return (None, cls.__ERROR_ZERO_POW_NEG)
        return (cls.operand_a ** cls.operand_b, None)


# model API#2: various sets/dicts accessors

# простой набор из имеющихся операций
operations_set: set[ArithmeticOperation] = (
    Exponentiation, Multiplication, Division, Addition, Substraction)

# словарь { значёк операции : модель операции }
operations_by_sign = {op_model.SIGN: op_model for op_model in operations_set}

available_operation_signs = list(map(lambda op: op.SIGN, operations_set))

def is_valid_sign(operation_sign):
    return operation_sign in available_operation_signs

# ============== VVV делегировано AritmneticExpression VVV ================================
# # словарь словарей { приоритет : { значёк операции : модель операции } },
# # в котором пары {значёк:операция} ранжированы по приоритемам
# operations_by_priority = {priority: {op.SIGN: op for op in operations_set if op.PRIORITY == priority}
#                           for priority in set([o.PRIORITY for o in operations_set])}

# # список словарей { значёк операции : модель операции } отсортированный по возрастанию PRIORITY
# # (операции с меньшим приоритетом выполняются раньше операций с большим приоритетом)
# operations_by_priority_asc = [{op.SIGN: op for op in operations_set if op.PRIORITY == pr}
#                               for pr in sorted(set([o.PRIORITY for o in operations_set]))]
# ==========================================================================================

# testing:

# if __name__ == '__main__':
#     Multiplication.init(15, 22.5)
#     res, err = Multiplication.calc()
#     print(f'result = {res}  error = {err}')
#     print(15*22.5)

#     res, err = Division.calc()
#     print(f'result = {res}  error = {err}')

#     Division.init(10, 0)
#     res, err = Division.calc()
#     print(f'result = {res}  error = {err}')

#     Division.init(15, 5)
#     res, err = Division.calc()
#     print(f'result = {res}  error = {err}')
