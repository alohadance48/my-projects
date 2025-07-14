class Info:
    def deastole(self, status: bool) -> bool:
        print(f"Info: Blood status is now {'Deastole' if status else 'Sistole'}")
        return status

    def user_info(self, is_old: int, fatigue: int):
        print(f'Info: Age: {is_old}, Fatigue: {fatigue}')

    def dead(self, is_dead: bool):
        print('Вы погибли' if is_dead else 'Вы выжили')