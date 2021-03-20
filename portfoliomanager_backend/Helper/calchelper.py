
PLUS = "+"
MINUS = "-"
POW = "*"
DIV = "/"


def calc_decimals(op1, op2, operation=PLUS, prec=2):
    operations = {
        PLUS: lambda a, b: a + b,
        MINUS: lambda a, b: a - b,
        POW: lambda a, b: a * b,
        DIV: lambda a, b: a / b
    }

    return round(operations[operation](op1, op2), prec)


def calc_diff_perc(op1, op2, as_perc=False, prec=4):
    result = (op1 - op2)
    result = result / op2
    if as_perc:
        return round((result * 100), prec)
    return round(result, prec)


def test():
    print(str(calc_decimals(1.3, 2.15, "+")))
    print(str(calc_decimals(1.3, 2.15, "-")))
    print(str(calc_decimals(1.3, 2.15, "*")))
    print(str(calc_decimals(1.3, 2.15, "/")))
    print(str(calc_diff_perc(839.81, 814.29)))


if __name__ == "__main__":
    test()
