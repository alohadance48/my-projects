# info.py

class Info:
    def deastole(self, status: bool) -> bool:
        print(f"Info: Blood status is now {'Deastole' if status else 'Sistole'}")
        return status

    def user_info(self, is_old: int,fatigue:int):
        print(f'Info:you old:{is_old}твоя нагрузка:{fatigue}')
        return is_old

    def defects(self, not_full_heart: bool, deabet: bool, olf: bool):
        pass

    def dead(self, start: bool):
        pass

    def pulse(self, status: int):
        pass

    def end(self, end: bool):
        pass