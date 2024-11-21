# info.py
class Info:
    def deastole(self, status: bool) -> str:
        return f"Blood status is now {'Deastole' if status else 'Sistole'}"

    def user_info(self, is_old: int, fatigue: int):
        return f'you old: {is_old}, твоя нагрузка: {fatigue}'

    def dead(self, start: bool):
        return 'Вы погибли' if start else 'Вы выжили'