import common
from common import Console as Con
from common import ForeColor, BackColor


class view_settings:
    TITLE_FORECOLOR = ForeColor.CYAN
    USER_INPUT_VALUE_FORECOLOR = ForeColor.BRIGHT_GREEN
    USER_INPUT_SIGN_FORECOLOR = ForeColor.BRIGHT_MAGENTA
    END_RESULT_FORECOLOR = ForeColor.BRIGHT_YELLOW
    SUB_RESULT_FORECOLOR = ForeColor.BRIGHT_WHITE


def prepare():
    Con.activate_ansi_esc_seq_in_win_cmd()
    Con.clear()


def show_title():
    common.print_title('Калькулятор', fore_color=view_settings.TITLE_FORECOLOR)


def __print_horizontal_line():
    console_width, _ = Con.get_size()
    print('\u2508'*console_width)


def _get_raw_input(prompt, fore_color: ForeColor):
    value_str = input(prompt + fore_color.value)
    print(common.escape_codes.RESET, end='')
    return value_str


def get_value_raw():
    return _get_raw_input('Введите значение или выражение: ',
                          view_settings.USER_INPUT_VALUE_FORECOLOR)


def get_operation_sign():
    return _get_raw_input('Введите операцию ("=" \u2014 чтобы завершить): ',
                          view_settings.USER_INPUT_SIGN_FORECOLOR)


def show_error(message):
    common.print_error(message)


def show_sub_result(value: float):
    print(Con.format('  Результат:', italic=True),
          Con.format(f'{value:g}', fore_color=view_settings.SUB_RESULT_FORECOLOR))


def show_expression_result(value: float):
    print(Con.format(f'  Значение выражения: {value:g}', italic=True))


def show_end_result(value: float):
    print(view_settings.END_RESULT_FORECOLOR.value, common.escape_codes.BOLD)
    __print_horizontal_line()
    print(f'Результат: {value:g}')
    __print_horizontal_line()
    print(common.escape_codes.RESET)
