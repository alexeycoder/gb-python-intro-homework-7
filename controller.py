from pyexpat import model
import common
from model import arithmetic_operations
from model.arithmetic_expression import ArithmeticExpression
import view


operations_by_sign = arithmetic_operations.operations_by_sign
operations_set = arithmetic_operations.operations_set
arithmetic_expression = ArithmeticExpression(operations_set)

END_SIGN = '='


def _is_valid_value(input_str) -> tuple[bool, float]:
    input_str = common.make_decimal_separator_invariant(input_str)
    try:
        value_float = float(input_str)
        return (True, value_float)
    except ValueError:
        return (False, None)


def _is_valid_expression(input_str) -> tuple[bool, float, str]:
    try:
        result_value_float, err = \
            arithmetic_expression.calculate_expression_string(input_str)
        if err:
            return (False, None, err)
        return (True, result_value_float, None)
    except (ValueError, TypeError):
        return (False, None, None)


def request_value() -> float:
    while True:
        input_str = view.get_value_raw()

        # check if valid single value:
        is_valid, value = _is_valid_value(input_str)
        if is_valid:
            return value

        # otherwise, check if valid expression:
        is_valid, value, err_msg = _is_valid_expression(input_str)
        if is_valid:
            view.show_expression_result(value)
            return value

        if err_msg:
            view.show_error(err_msg)
        else:
            view.show_error('Некорректный ввод!')
        view.show_error('Пожалуйста повторите ввод.')


def request_operation() -> arithmetic_operations.ArithmeticOperation:
    while True:
        operation_sign = view.get_operation_sign()

        if operation_sign == END_SIGN:
            return None

        operation_model = None
        if arithmetic_operations.is_valid_sign(operation_sign):
            operation_model = operations_by_sign[operation_sign]

        if operation_model is None:
            view.show_error('Некорректный ввод: Такая операция не определена!'
                            'Пожалуйста попробуйте ещё раз.')
        else:
            return operation_model


def run_lifecycle():
    view.prepare()
    view.show_title()

    result = request_value()

    while True:
        operation_model = request_operation()
        if operation_model is None:
            break

        operand = request_value()

        operation_model.init(result, operand)
        result_preview, err = operation_model.calc()
        if err:
            view.show_error(err)
            break

        result = result_preview
        view.show_sub_result(result)

    view.show_end_result(result)


def _perform_tests():
    test_expr_str = '-(16.4) + -18/2 - 6.5 / (8+14.2) - ((-11-1)+(+22-2)) + 55.5'
    # -(16.4) + (-18/2) - 6.5 / (8.5+1.5) - (-(-11-1)+(+22-2)) + 55.5
    ae = ArithmeticExpression(operations_set)
    result, err = ae.calculate_expression_string(test_expr_str)
    print('result =', result, ' error =', err)

    test_expr_2_str = 'abc'
    res2, err = ae.calculate_expression_string(test_expr_2_str)
    print('result =', res2, ' error =', err)

