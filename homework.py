M_IN_KM : int = 1000 # метров в километре



class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str, # тип тренировки (название)
                 duration: float, # продолжительность тренировки
                 distance: float, # преодоленная за тренировку дистанция
                 speed: float, # средняя скорость во время тренировки
                 calories: float, #сожженные за тренировку калории
                 ) -> None:
        self.training_type = training_type 
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> None:
        print(f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.2f} ч.; Дистанция: {self.distance:.2f} км; Ср. скорость: {self.speed:.2f} км/ч; Потрачено ккал: {self.calories:.2f}.')

class Training:
    """Базовый класс тренировки."""
    LEN_STEP : float = 0.65 # длина шага по умолчанию

    def __init__(self,
                 action: int, # количество действий (шагов, грибков и тд)
                 duration: float, # продолжительность тренировки
                 weight: float, # вес тренирующегося
                 ) -> None:
        self.action = action 
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км.
        Вычисляет расстояние по формуле:
        количество_шагов * длина_шага / 1000 (метров в км)
        """
        distance: float = self.action * LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.
        Вычисляет среднюю скорость по формуле:
        преодоленная_дистанция_за_тренировку / время_тренировки 
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        В абстрактном классе реализации не имеет.
        """
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий.
        Вычисляет затраченные калории по формуле:
        (18 * средняя_скорость - 20) * вес_спортсмена / 1000 * время_тренировки_в_минутах 
        """
        CALLORY_RUNNING_COEF1 : int = 18 # коэф. для расчета калорий при беге 1
        CALLORY_RUNNING_COEF2 : int = 20 # коэф. для расчета калорий при беге 2
        calories: float = (CALLORY_RUNNING_COEF1 * self.get_mean_speed() - 
            CALLORY_RUNNING_COEF2) * self.weight / M_IN_KM * self.duration
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__ (self,
                 action: int, # количество действий (шагов, грибков и тд)
                 duration: float, # продолжительность тренировки
                 weight: float, # вес тренирующегося
                 height: float # высота тренирующегося
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий.
        Вычисляет затраченные калории по формуле:
        (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес) * время_тренировки_в_минутах 
        """
        CALLORY_WALKING_COEF1 : int = 0.035 # коэф. для расчета калорий при ходьбе 1
        CALLORY_WALKING_COEF2 : int = 2 # коэф. для расчета калорий при ходьбе 2
        CALLORY_WALKING_COEF3 : int = 0.029 # коэф. для расчета калорий при ходьбе 3
        calories: float = (CALLORY_WALKING_COEF1 * self.weight + 
            (self.get_mean_speed() * CALLORY_WALKING_COEF2 / self.height) * 
            CALLORY_WALKING_COEF3 * self.weight) * self.duration
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 0.65 # длина гребка

    def __init__ (self,
                 action: int, # количество действий (шагов, грибков и тд)
                 duration: float, # продолжительность тренировки
                 weight: float, # вес тренирующегося
                 length_pool: float, # длина бассейна в метрах
                 count_pool: float # сколько раз пользователь переплыл бассейн
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.
        Вычисляет среднюю скорость по формуле:
        длина_бассейна * количество_бассейнов / 1000 / время_тренировки 
        (1000 - метров в км)
        """
        speed: float = self.length_pool * self.count_pool / M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий.
        Вычисляет затраченные калории по формуле:
        (средняя_скорость + 1.1) * 2 * вес   
        """
        CALLORY_SWIMING_COEF1 : int = 1.1 # коэф. для расчета калорий при плавании 1
        CALLORY_SWIMING_COEF2 : int = 2 # коэф. для расчета калорий при плавании 2
        calories: float = ((self.get_mean_speed() + CALLORY_SWIMING_COEF1) * 
            CALLORY_SWIMING_COEF2 * self.weight)
        return calories
    


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    pass


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

