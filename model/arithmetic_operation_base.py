# базовый класс, определяющий интерфейсные методы init() и calc() модели "арифметическая операция"

# model abstract type to provide model's API: .init(a,b) .calc() SIGN NAME PRIORITY

class ArithmeticOperation:
    SIGN = 'n'
    NAME = 'none'
    PRIORITY = 0
    __ERROR_NOT_INITIALIZED = 'Ошибка: Не инициализированы операнды для операции'

    __is_initialized: bool = False
    operand_a: float
    operand_b: float

    @classmethod
    def init(cls, operand_a, operand_b):
        cls.operand_a = operand_a
        cls.operand_b = operand_b
        cls.__is_initialized = True

    @classmethod
    def calc(cls) -> tuple[float, str]:
        """ Возвращает кортеж (результат операции, описание ошибки)
        И сбрасывает состояние на 'не инициализировано'.
        """
        if not cls.__is_initialized:
            return (None, f'{ArithmeticOperation.__ERROR_NOT_INITIALIZED} {cls.NAME}!')

        cls.__is_initialized = False
        return cls._get_result()

    @classmethod
    def _get_result(cls):
        return (0, None)
