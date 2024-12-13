class Info:
    def deastole(self, status: bool) -> str:
        return f"Blood status is now {'Deastole' if status else 'Sistole'}"

    def user_info(self, is_old: int, fatigue: int):
        return f'Age: {is_old}, Fatigue: {fatigue}'

    def dead(self, start: bool):
        return 'You died' if start else 'You survived'