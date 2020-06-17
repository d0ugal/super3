class Base:
    pass


class A(Base):
    def __init__(self):
        super().__init__()


class B(Base):
    def __init__(self):
        super(B, self).__init__()


class C(A, B):
    def __init__(self):
        super(C, self).__init__()
        super(B, self).__init__()

    def some_method(self):
        try:
            pass
        except:
            pass
        else:

            def _wrapped():
                return super(C, self).__init__()

    @classmethod
    def a_class_method(cls):
        super(C, cls).something()
