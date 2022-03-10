"""
Bài toán:
  Các lớp con có những behavior khác nhau
  cho cùng 1 method được kế thừa từ lớp cha.
  - Nếu dùng kế thừa thì lớp con phải override mọi lúc khi tạo lớp con mới.
  - Nếu tách method đó ra làm interface, lớp con implement interface đó:
    method mà hầu hết trường hợp đều giống nhau => lặp code + sau này sửa đổi
    trên toàn bộ các lớp con thì khó khăn.

Cách giải theo strategy pattern:
  - Tạo 1 interface cho từng loại hành động. => gọi là 1 behavior interface.
  - Mỗi cách behave khác nhau của loại hành động đó
    sẽ là 1 implementation của interface đó. => gọi là 1 behavior strategy.
  - Lớp cha chứa biến có kiểu interface loại hành động, có hàm để set giá trị biến này.

Ví dụ:
  * Bài toán:
    - Lớp Duck cha có implement sẵn phương thức swim và quack, phương thức display thì virtual.
    - Các lớp con implement phương thức display của riêng mình, khi nào swim và quack khác với cha thì override.
    - Khi thêm lớp con mới (ví dụ Duck gỗ, Duck đồ chơi)
      cần phải biết là lớp cha có implement sẵn phương thức swim và quack
      để override theo đúng trường hợp của Duck gỗ (không quack được).
    => Vấn đề: khi implement 1 lớp Duck con mới thì cần phải dò code hoặc đọc tài liệu để
       biết được các method nào được implement sẵn ở Duck cha cần lưu ý để override.
  * Cách giải theo strategy pattern:
    - Tạo interface SwimBehavior, QuackBehavior.
    - Tạo SwimNormally, SwimNoWay,... implement SwimBehavior.
    - Tạo Quack, Squeak, MuteQuack,... implement QuackBehavior.
    - Lớp Duck cha chứa biến swim_behavior kiểu SwimBehavior và biến quack_behavior kiểu QuackBehavior.
    - Lớp con muốn swim kiểu nào thì gọi hàm set_swim_behavior truyền vào implementation đó của SwimBehavior.
    - Lớp con có kiểu swim mới hơn nữa thì tạo 1 implementation mới của SwimBehavior
      rồi set_swim_behavior là implementation mới đó.
      => Khi tạo mới lớp con có kiểu behavior khác, không cần chỉnh sửa code ở lớp cha hay lớp anh/em khác.

"""

import abc
from typing import Optional


class Duck:

    def __init__(self):
        self._quack_behavior: Optional[QuackBehavior] = None
        self._swim_behavior: Optional[SwimBehavior] = None

    def set_quack_behavior(self, quack_behavior):
        self._quack_behavior = quack_behavior

    def set_swim_behavior(self, swim_behavior):
        self._swim_behavior = swim_behavior

    def quack(self):
        self._quack_behavior.quack()

    def swim(self):
        self._swim_behavior.swim()


class QuackBehavior(abc.ABC):

    @abc.abstractmethod
    def quack(self):
        pass


class SwimBehavior(abc.ABC):

    @abc.abstractmethod
    def swim(self):
        pass


# <editor-fold desc="Các implementation (các strategy) của quack behavior">
class Quack(QuackBehavior):

    def quack(self):
        print('quack like a duck')


class Squeak(QuackBehavior):

    def quack(self):
        print('squeak squeak')


class MuteQuack(QuackBehavior):

    def quack(self):
        print('cant quack')


# </editor-fold>


# <editor-fold desc="Các implementation (các strategy) của swim behavior">
class SwimNormally(SwimBehavior):

    def swim(self):
        print('swim normally')


class SwimNoWay(SwimBehavior):

    def swim(self):
        print('cant swim')


# </editor-fold>


class DuckGhe(Duck):

    def __init__(self):
        super().__init__()
        self._quack_behavior = Quack()
        self._swim_behavior = SwimNormally()


class DuckDoChoi(Duck):

    def __init__(self):
        super().__init__()
        self._quack_behavior = Squeak()
        self._swim_behavior = SwimNormally()


class DuckGo(Duck):

    def __init__(self):
        super().__init__()
        self._quack_behavior = MuteQuack()
        self._swim_behavior = SwimNoWay()


if __name__ == '__main__':
    duck_go = DuckGo()
    duck_go.swim()
    duck_go.quack()
