letterboek = {chr(ord('a') + i): 10 + i for i in range(26)}
nummerboek = {value: key for key, value in letterboek.items()}


def letter_to_number(x):
    assert isinstance(x, str), 'Input should be a string.'
    assert len(x) == 1, 'Input should have length 1'
    return letterboek[x] if x in letterboek else int(x)


def number_to_letter(x):
    assert isinstance(x, int), 'Input should be an integer.'
    assert x in range(10+26), 'Input should be under 36'
    return nummerboek[x] if x in nummerboek else str(x)


def letter_str_to_integer_list(str):
    return [letter_to_number(y) for y in str]


def integer_list_to_letter_str(list):
    return ''.join([number_to_letter(y) for y in list])


def decimal_to_base_m(x, m, p=14):
    if isinstance(x, (Zero, One)):
        return x

    n = 10
    if isinstance(x, (int, float)):
        x = BaseN(str(x), n=n)

    sgn = '+' if x.sgn == +1 else '-'
    x_int, x_float = map(lambda y: BaseN(y, n=n), (x.repr_int(), x.repr_float()))
    base = BaseN(str(m), n=n)

    # Integer part
    str_int = ''
    while x_int:
        rest = x_int % base
        str_int += number_to_letter(int(rest.repr_int()))
        x_int //= base
    str_int = str_int[::-1]

    # Float part
    floats = len(str(x_float))
    een = BaseN('1' + '0' * floats, n=n)
    str_float = ''
    for i in range(p):
        x_float *= base
        elem = x_float // een
        str_float += number_to_letter(int(elem.repr_int()))
        x_float %= een

    str_total = sgn + str_int + '.' + str_float
    return BaseN(str_total, n=m)


def base_n_to_decimal(x, p=14):
    if isinstance(x, (Zero, One)):
        return x

    assert isinstance(x, BaseN)
    m = 10
    n = x.n

    sgn = '+' if x.sgn == +1 else '-'
    x_int, x_float = map(lambda y: BaseN(y, n=n), (x.repr_int(), x.repr_float()))
    base = BaseN(str(decimal_to_base_m(x=m, m=n)), n=n)

    # Integer part
    str_int = str(int(x_int.repr_int(), n))

    # Float part
    floats = len(str(x_float))
    een = BaseN('1' + '0' * floats, n=n)
    str_float = ''
    for i in range(p):
        x_float *= base
        elem = x_float // een
        str_float += str(int(elem.repr_int(), n))
        x_float %= een

    str_total = sgn + str_int + '.' + str_float
    return BaseN(str_total, n=m)


def self_other_check(self, other):
    if isinstance(other, (int, float)):
        other = BaseN(other, n=10).change_base(m=self.n)
    return other


class BaseN:
    def __init__(self, x: str, n: int = 10, precision: int = 14):
        assert n in range(2, 10+26+1)  # 10 cijfers + 26 letters en geen base 0 of base 1
        self.n = n
        self.p = precision

        if not x:
            x = '0'

        if not isinstance(x, str):
            x = str(x)

        self.sgn = -1 if x[0] == '-' else +1
        x = x.lstrip('+-0')
        self.str_int, self.str_float = x.rstrip('0').split('.') if '.' in x else (x, '')

        if not self.str_int:
            self.str_int = '0'
            if not self.str_float:
                self.sgn = +1

        self.list_int, self.list_float = map(letter_str_to_integer_list, (self.str_int, self.str_float))

    def get_filled_list(self, n_int, n_float):
        mapping = (list_float, floats), (list_int, ints) = tuple(map(lambda list: (list.copy(), len(list)), (self.list_float, self.list_int)))
        for i, ((listi, leni), maxi) in enumerate(zip(mapping, (n_float, n_int))):
            if i:
                listi.reverse()
            for _ in range(maxi - leni):
                listi.append(0)
            if i:
                listi.reverse()
        return list_int + list_float

    def __eq__(self, other):
        other = self_other_check(self, other)

        if self.sgn != other.sgn:
            return False

        floats = max(len(self.list_float), len(other.list_float))
        ints = max(len(self.list_int), len(other.list_int))
        list1, list2 = self.get_filled_list(ints, floats), other.get_filled_list(ints, floats)
        return list1 == list2

    def __ne__(self, other):
        other = self_other_check(self, other)

        if self.sgn != other.sgn:
            return False

        floats = max(len(self.list_float), len(other.list_float))
        ints = max(len(self.list_int), len(other.list_int))
        list1, list2 = self.get_filled_list(ints, floats), other.get_filled_list(ints, floats)
        return list1 != list2

    def __lt__(self, other):
        other = self_other_check(self, other)

        if self.sgn == -1 and other.sgn == +1:
            return True
        if self.sgn == +1 and other.sgn == -1:
            return False

        floats = max(len(self.list_float), len(other.list_float))
        ints = max(len(self.list_int), len(other.list_int))
        list1, list2 = self.get_filled_list(ints, floats), other.get_filled_list(ints, floats)

        for elem1, elem2 in zip(list1, list2):
            if elem1 > elem2:
                return False
            if elem1 < elem2:
                return True
        return False

    def __gt__(self, other):
        other = self_other_check(self, other)

        if self.sgn == -1 and other.sgn == +1:
            return False
        if self.sgn == +1 and other.sgn == -1:
            return True

        floats = max(len(self.list_float), len(other.list_float))
        ints = max(len(self.list_int), len(other.list_int))
        list1, list2 = self.get_filled_list(ints, floats), other.get_filled_list(ints, floats)

        for elem1, elem2 in zip(list1, list2):
            if elem1 > elem2:
                return True
            if elem1 < elem2:
                return False
        return False

    def __le__(self, other):
        other = self_other_check(self, other)

        if self.sgn == -1 and other.sgn == +1:
            return True
        if self.sgn == +1 and other.sgn == -1:
            return False

        floats = max(len(self.list_float), len(other.list_float))
        ints = max(len(self.list_int), len(other.list_int))
        list1, list2 = self.get_filled_list(ints, floats), other.get_filled_list(ints, floats)

        for elem1, elem2 in zip(list1, list2):
            if elem1 > elem2:
                return False
            if elem1 < elem2:
                return True
        return True

    def __ge__(self, other):
        other = self_other_check(self, other)

        if self.sgn == -1 and other.sgn == +1:
            return False
        if self.sgn == +1 and other.sgn == -1:
            return True

        floats = max(len(self.list_float), len(other.list_float))
        ints = max(len(self.list_int), len(other.list_int))
        list1, list2 = self.get_filled_list(ints, floats), other.get_filled_list(ints, floats)

        for elem1, elem2 in zip(list1, list2):
            if elem1 > elem2:
                return True
            if elem1 < elem2:
                return False
        return True

    def __abs__(self):
        absolute = self.copy()
        absolute.sgn = +1
        return absolute

    def __add__(self, other):
        other = self_other_check(self, other)

        sgn_self, sgn_other = self.sgn, other.sgn
        sgn = sgn_self * sgn_other
        abs_self, abs_other = abs(self), abs(other)
        num1, sgn1, num2, sgn2 = (abs_self, sgn_self, abs_other, sgn_other) if abs_self > abs_other else (abs_other, sgn_other, abs_self, sgn_self)

        rest = 0
        sum_list = []
        floats = max(len(num1.list_float), len(num2.list_float))
        ints = max(len(num1.list_int), len(num2.list_int))
        list1, list2 = num1.get_filled_list(ints, floats), num2.get_filled_list(ints, floats)
        for elem1, elem2 in zip(list1[::-1], list2[::-1]):
            elem = elem1 + sgn*elem2 + rest
            rest = elem // self.n
            elem %= self.n
            sum_list.append(elem)
        sum_list.append(rest)
        sum_str = integer_list_to_letter_str(sum_list[::-1])
        sum_str = sum_str[:-floats] + '.' + sum_str[-floats:] if floats else sum_str
        num3 = BaseN(sum_str, self.n)
        if num3:
            num3.sgn = sgn1
        return num3

    def __radd__(self, other):
        other = self_other_check(self, other)

        return other.__add__(self)

    def __sub__(self, other):
        other = self_other_check(self, other)

        return self + (-other)

    def __rsub__(self, other):
        other = self_other_check(self, other)

        return other.__sub__(self)

    def __mul__(self, other):
        other = self_other_check(self, other)

        floats1 = len(self.list_float)
        floats2 = len(other.list_float)
        floats = floats1 + floats2
        list1 = self.list_int + self.list_float
        list2 = other.list_int + other.list_float
        mul_list = [0 for _ in (*list1, *list2)]
        for i, elem1 in enumerate(list1[::-1]):
            rest = 0
            for j, elem2 in enumerate(list2[::-1]):
                elem = mul_list[i+j]
                elem += elem1 * elem2 + rest
                rest = elem // self.n
                elem %= self.n
                mul_list[i+j] = elem

            mul_list[i+j+1] += rest

        mul_str = integer_list_to_letter_str(mul_list[::-1])
        mul_str = mul_str[:-floats] + '.' + mul_str[-floats:] if floats else mul_str

        if self.sgn * other.sgn == -1:
            mul_str = '-' + mul_str
        return BaseN(mul_str, self.n)

    def __rmul__(self, other):
        other = self_other_check(self, other)

        return other.__mul__(self)

    def __floordiv__(self, other):
        other = self_other_check(self, other)
            
        assert other != Zero(), 'Division by zero'

        sgn1, sgn2 = self.sgn, other.sgn
        num1, num2 = self.copy(), other.copy()
        num1.sgn = num2.sgn = +1

        i = BaseN('0', n=self.n)
        if sgn1*sgn2 == +1:
            while num1 >= num2:
                num1 -= num2
                i += One()
        else:
            while num1 > num2:
                num1 -= num2
                i -= One()
            i -= One()
        return i

    def __rfloordiv__(self, other):
        other = self_other_check(self, other)

        return other.__floordiv__(self)

    def __mod__(self, other):
        other = self_other_check(self, other)
            
        assert other != Zero(), 'Division by zero'

        if self == Zero():
            return self.copy()

        sgn1, sgn2 = self.sgn, other.sgn
        num1, num2 = self.copy(), other.copy()
        num1.sgn = num2.sgn = +1

        if sgn1 * sgn2 == +1:
            while num1 >= num2:
                num1 -= num2
        else:
            while num1 > num2:
                num1 -= num2
            num1 = num2 - num1
        return num1

    def __rmod__(self, other):
        other = self_other_check(self, other)

        return other.__mod__(self)

    def __divmod__(self, other):
        other = self_other_check(self, other)
            
        assert other != Zero(), 'Division by zero'

        sgn1, sgn2 = self.sgn, other.sgn
        num1, num2 = self.copy(), other.copy()
        num1.sgn = num2.sgn = +1

        i = Zero()
        if sgn1 * sgn2 == +1:
            while num1 >= num2:
                num1 -= num2
                i += One()
        else:
            while num1 > num2:
                num1 -= num2
                i -= One()
            num1 = num2 - num1
            i -= One()
        return i, num1

    def __rdivmod__(self, other):
        other = self_other_check(self, other)

        return other.__divmod__(self)

    def __truediv__(self, other):
        other = self_other_check(self, other)
            
        assert other != Zero(), 'Division by zero'

        int1, int2 = len(self.repr_int()), len(other.repr_int())
        float2 = len(other.repr_float())
        float1 = self.p + len(other.repr_float())
        floats = float1 - float2

        list1, list2 = self.get_filled_list(int1, float1), other.get_filled_list(int2, float2)
        str1, str2 = integer_list_to_letter_str(list1), integer_list_to_letter_str(list2)

        quotient_str = ''
        divisor = BaseN(str2, self.n)
        dividend = BaseN('0', self.n)
        for i, elem1 in enumerate(str1):
            dividend = BaseN(str(dividend) + elem1, self.n)
            if dividend < divisor:
                quotient_elem = '0'
            else:
                quotient_elem = dividend // divisor
                dividend -= quotient_elem * divisor
                quotient_elem = quotient_elem.repr_int()
            quotient_str += quotient_elem

        quotient_str = quotient_str[:-floats] + '.' + quotient_str[-floats:] if floats else quotient_str

        if self.sgn * other.sgn == -1:
            quotient_str = '-' + quotient_str
        return BaseN(quotient_str, self.n)

    def __rtruediv__(self, other):
        other = self_other_check(self, other)

        return other.__truediv__(self)

    def __str__(self):
        str_int = self.str_int.lstrip('0')
        str_float = self.str_float.rstrip('0')
        if not str_int:
            str_int = '0'
        dot = '.' if str_float else ''
        sgn = '-' if self.sgn == -1 else ''
        return sgn + str_int + dot + str_float

    def __repr__(self):
        return f"BaseN('{str(self)}', {self.n}, {self.p})"

    def repr_int(self):
        str_int = self.str_int.lstrip('0')
        if not str_int:
            str_int = '0'
        return str_int

    def repr_float(self):
        return self.str_float.rstrip('0')

    def __bool__(self):
        return self != Zero()

    def __int__(self):
        return self.sgn * int(self.repr_int(), self.n)

    def __float__(self):
        x = base_n_to_decimal(self)
        return float(str(x))

    def __round__(self, n=None):
        if n is None:
            n = 0

        if n < 0:
            return

        else:
            str_float = self.str_float[:n]
            if n+1 < len(self.str_float):
                return

    def copy(self):
        return eval(repr(self))

    def change_base(self, m, p=14):
        n = self.n

        sgn = '+' if self.sgn == +1 else '-'
        x_int, x_float = map(lambda y: BaseN(y, n=n), (self.repr_int(), self.repr_float()))
        base = BaseN(str(decimal_to_base_m(x=m, m=n)), n=n)

        # Integer part
        str_int = ''
        while x_int:
            rest = x_int % base
            str_int += number_to_letter(int(rest))
            x_int //= base
        str_int = str_int[::-1]

        # Float part
        floats = len(str(x_float))
        een = BaseN('1' + '0' * floats, n=n)
        str_float = ''
        for i in range(p):
            x_float *= base
            elem = x_float // een
            str_float += number_to_letter(int(elem.repr_int()))
            x_float %= een

        str_total = sgn + str_int + '.' + str_float
        return BaseN(str_total, n=m)

    def __neg__(self):
        num = self.copy()
        num.sgn *= -1
        return num

    def __pos__(self):
        num = self.copy()
        return num


class Zero(BaseN):
    def __init__(self):
        self.n = 10
        self.sgn = +1
        self.str_int, self.str_float = ('0', '')
        self.list_int, self.list_float = [0], []

    def __eq__(self, other):
        other = self_other_check(self, other)
            
        return str(other) == '0'

    def __ne__(self, other):
        other = self_other_check(self, other)
            
        return str(other) != '0'

    def __lt__(self, other):
        other = self_other_check(self, other)
            
        if self == other:
            return False
        return other.sgn == -1

    def __gt__(self, other):
        other = self_other_check(self, other)
            
        if self == other:
            return False
        return other.sgn == +1

    def __le__(self, other):
        other = self_other_check(self, other)
            
        if self == other:
            return True
        return other.sgn == -1

    def __ge__(self, other):
        other = self_other_check(self, other)
            
        if self == other:
            return True
        return other.sgn == +1

    def __abs__(self):
        return self.copy()

    def __add__(self, other):
        other = self_other_check(self, other)
            
        return other.copy()

    def __sub__(self, other):
        other = self_other_check(self, other)
            
        num2 = other.copy()
        num2.sgn *= -1
        return num2

    def __mul__(self, other):
        other = self_other_check(self, other)
            
        return BaseN('0', self.n)

    def __floordiv__(self, other):
        other = self_other_check(self, other)
            
        assert other != Zero(), 'Division by zero'
        return BaseN('0', self.n)

    def __mod__(self, other):
        other = self_other_check(self, other)
            
        assert other != Zero(), 'Division by zero'
        return BaseN('0', self.n)

    def __divmod__(self, other):
        other = self_other_check(self, other)
            
        assert other != Zero(), 'Division by zero'
        return BaseN('0', self.n), BaseN('0', self.n)

    def __truediv__(self, other):
        other = self_other_check(self, other)
            
        assert other != Zero(), 'Division by zero'
        return Zero

    def __str__(self):
        return '0'

    def __repr__(self):
        return 'Zero()'

    def repr_int(self):
        return '0'

    def repr_float(self):
        return ''

    def __bool__(self):
        return False

    def __int__(self):
        return 0

    def __float__(self):
        return 0.0

    def copy(self):
        return Zero()

    def change_base(self, m=None, p=None):
        return self


class One(BaseN):
    def __init__(self):
        self.n = 10
        self.sgn = +1
        self.str_int, self.str_float = ('1', '')
        self.list_int, self.list_float = [1], []

    def __eq__(self, other):
        other = self_other_check(self, other)
            
        return str(other) == '1'

    def __ne__(self, other):
        other = self_other_check(self, other)
            
        return str(other) != '1'

    def __lt__(self, other):
        other = self_other_check(self, other)
            
        if self == other:
            return False
        if other.sgn == -1:
            return True
        return str(other)[0] != '0'

    def __gt__(self, other):
        other = self_other_check(self, other)
            
        if self == other:
            return False
        if other.sgn == -1:
            return False
        return str(other)[0] == '0'

    def __le__(self, other):
        other = self_other_check(self, other)

        if self == other:
            return True
        if other.sgn == -1:
            return False
        return str(other)[0] != '0'

    def __ge__(self, other):
        other = self_other_check(self, other)

        if self == other:
            return True
        if other.sgn == -1:
            return True
        return str(other)[0] == '0'

    def __abs__(self):
        return self.copy()

    def __mul__(self, other):
        other = self_other_check(self, other)

        return other.copy()

    def __str__(self):
        return '1'

    def __repr__(self):
        return 'One()'

    def repr_int(self):
        return '1'

    def repr_float(self):
        return ''

    def __bool__(self):
        return True

    def __int__(self):
        return 1

    def __float__(self):
        return 1.0

    def copy(self):
        return One()

    def change_base(self, m=None, p=None):
        return self
