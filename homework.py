M_IN_KM: int = 1000  # метров в километре


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,  # тип тренировки
                 duration: float,  # продолжительность тренировки
                 distance: float,  # преодоленная за тренировку дистанция
                 speed: float,  # средняя скорость во время тренировки
                 calories: float,  # сожженные за тренировку калории
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> None:
        message: str = f'Тип тренировки: {self.training_type}; '
        message += f'Длительность: {self.duration:.3f}; '
        message += f'Дистанция: {self.distance:.3f} км; '
        message += f'Ср. скорость: {self.speed:.3f} км/ч; '
        message += f'Потрачено ккал: {self.calories:.3f}.'
        print(message)


class Training:
    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,  # количество действий (шагов, грибков и тд)
                 duration: float,  # продолжительность тренировки
                 weight: float,  # вес тренирующегося
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км.
        Вычисляет расстояние по формуле:
        количество_шагов * длина_шага / 1000 (метров в км)
        """
        LEN_STEP: float = 0.65  # длина шага по умолчанию
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
        """Вернуть информационное сообщение о выполненной тренировке.
        Возвращаемое сообщение содержит информацию о типе и продолжительности
        теренировки, а такеже о преодоленной дистанции, средней скорости
        и потраченных за тренировку калориях"""
        info: InfoMessage = InfoMessage(
            'Неустановленный тип тренировки',
            self.duration, self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий.
        Вычисляет затраченные калории по формуле:
        (18 * средняя_скорость - 20) * вес / 1000 * время_тренировки
        """
        C_COEF1: int = 18  # коэф. для расчета калорий при беге 1
        C_COEF2: int = 20  # коэф. для расчета калорий при беге 2
        speed: float = self.get_mean_speed()  # средняя скорость
        weight: float = self.weight  # вес
        dur: float = self.duration  # продолжительность тренировки
        calories: float = (C_COEF1 * speed - C_COEF2) * weight / M_IN_KM * dur
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке.
          Возвращаемое сообщение содержит информацию о типе и продолжительности
          теренировки, а такеже о преодоленной дистанции, средней скорости
          и потраченных за тренировку калориях"""
        info: InfoMessage = InfoMessage(
            'Running',
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return info


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,  # количество действий (шагов, грибков и тд)
                 duration: float,  # продолжительность тренировки
                 weight: float,  # вес тренирующегося
                 height: float  # высота тренирующегося
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий.
        Вычисляет затраченные калории по формуле:
        (0.035 * вес + (скорость * 2 / рост) * 0.029 * вес) * время_тренировки
        """
        C_COEF_1: int = 0.035  # коэф. для расчета калорий 1
        C_COEF_2: int = 2  # коэф. для расчета калорий 2
        C_COEF_3: int = 0.029  # коэф. для расчета калорий 3
        wi: float = self.weight
        hi: float = self.height
        sp: float = self.get_mean_speed()
        dur: float = self.duration
        calories: float = 0
        calories = (C_COEF_1 * sp + (sp * C_COEF_2 / hi) * C_COEF_3 * wi) * dur
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке.
        Возвращаемое сообщение содержит информацию о типе и продолжительности
        теренировки, а такеже о преодоленной дистанции, средней скорости
        и потраченных за тренировку калориях"""
        info: InfoMessage = InfoMessage(
            'SportsWalking',
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return info


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 0.65  # длина гребка

    def __init__(self,
                 action: int,  # количество действий (шагов, грибков и тд)
                 duration: float,  # продолжительность тренировки
                 weight: float,  # вес тренирующегося
                 length_pool: float,  # длина бассейна в метрах
                 count_pool: float  # сколько раз пользователь переплыл бассейн
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
        speed: float = 0  # тип отдельно, чтобы влезть в 79 символов PEP8
        speed = self.length_pool * self.count_pool / M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий.
        Вычисляет затраченные калории по формуле:
        (средняя_скорость + 1.1) * 2 * вес
        """
        C_COEF1: int = 1.1  # коэф. для расчета калорий при плавании 1
        C_COEF2: int = 2  # коэф. для расчета калорий при плавании 2
        speed: float = self.get_mean_speed()  # скорость
        weight: float = self.weight  # вес
        calories: float = (speed + C_COEF1) * C_COEF2 * weight
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке.
        Возвращаемое сообщение содержит информацию о типе и продолжительности
        теренировки, а такеже о преодоленной дистанции, средней скорости
        и потраченных за тренировку калориях"""
        info: InfoMessage = InfoMessage(
            'Swimming',
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return info


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков.
    Получает на вход тип тренировки и данные от датчиков.
    Первый аргумент - тип тренировки, WLK - ходьба, RUN - бег, SWM - плавание
    Второй аргумент - данные тренировки
    Для ходьбы:
    - количество шагов,
    - время тренировки в часах,
    - вес пользователя,
    - рост пользователя
    Для бега:
    - количество шагов,
    - время тренировки в часах,
    - вес пользователя
    Для плавания:
    - количество гребков,
    - время в часах,
    - вес пользователя,
    - длина бассейна,
    - сколько раз пользователь переплыл бассейн

    Возвращает созданный объект тренировки соответствующего класса
    """
    if workout_type == 'WLK':
        return SportsWalking(data[0], data[1], data[2], data[3])
    elif workout_type == 'RUN':
        return Running(data[0], data[1], data[2])
    elif workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])


def main(training: Training) -> None:
    """Главная функция.
    Выводит информаци"""
    info: InfoMessage = training.show_training_info()
    info.get_message()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)