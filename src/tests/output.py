class Base:
    pass


class A(Base):
    def __init__(self):
        super().__init__()


class B(Base):
    def __init__(self):
        super().__init__()


class C(A, B):
    def __init__(self):
        super().__init__()
        super(B, self).__init__()
