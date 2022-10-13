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

    def get_message(self) -> str:
        message: str = f'Тип тренировки: {self.training_type}; '
        message += f'Длительность: {round(self.duration,3)}; '
        message += f'Дистанция: {round(self.distance,3)} км; '
        message += f'Ср. скорость: {round(self.speed,3)} км/ч; '
        message += f'Потрачено ккал: {round(self.calories,3)}.'
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # длина шага по умолчанию
    M_IN_KM: int = 1000  # метров в километре
    MIN_IN_H: int = 60  # минут в часе

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
        M_IN_KM: int = 1000  # метров в километре
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
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18  # коэф. для расчета калорий 1
    CALORIES_MEAN_SPEED_SHIFT: int = 1.79  # коэф. для расчета калорий 2

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий.
        Вычисляет затраченные калории по формуле:
        (18 * средняя_скорость + 1,79) * вес / 1000 * время_тренировки
        """
        speed: float = self.get_mean_speed()  # средняя скорость
        weight: float = self.weight  # вес
        dur: float = self.duration  # продолжительность тренировки
        calories: float = self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
        calories = calories + self.CALORIES_MEAN_SPEED_SHIFT
        calories = calories * weight / self.M_IN_KM * dur
        return calories  # Из 1й строки формулы полотно-портянка кода
        # ОБОЖАЮ ПЕП8. Все для читаемости кода, ведь так понятне, конечно!

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
    LEN_STEP: float = 0.64  # длина шага
    CALORIES_WEIGHT_MULTIPLIER: int = 0.035  # коэф. для расчета калорий 1
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2  # коэф. для расчета калорий 2
    CALORIES_SPEED_HEIGHT_MULTIPLIER: int = 0.029  # коэф. для расчета калорий3
    KMH_IN_MSEC: int = 0.278  # км/ч в м/с
    CM_IN_M: int = 100  # сантиметров в метре
    S_IN_M: int = 60  # сек в минуте

    def __init__(self,
                 action: int,  # количество действий (шагов, грибков и тд)
                 duration: float,  # продолжительность тренировки В Ч
                 weight: float,  # вес тренирующегося В КГ
                 height: float  # высота тренирующегося В СМ
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий.
        Вычисляет затраченные калории по формуле:
        (0.035 * вес + (скорость * 2 / рост) * 0.029 * вес) * время_тренировки
        """
        weight: float = self.weight  # вес
        height: float = self.height / self.CM_IN_M  # рост
        speed: float = self.get_mean_speed() * self.KMH_IN_MSEC  # скорость
        duration: float = self.duration / self.MIN_IN_H / self.S_IN_M
        calories: float = 0  # калории
        calories = speed * self.CALORIES_MEAN_SPEED_MULTIPLIER / height
        calories *= self.CALORIES_SPEED_HEIGHT_MULTIPLIER * weight
        calories += self.CALORIES_WEIGHT_MULTIPLIER * weight
        calories *= duration
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
    LEN_STEP: float = 1.38  # длина гребка
    CALORIES_MEAN_SPEED_SHIFT: int = 1.1  # слагаемое скорости
    CALORIES_WEIGHT_MULTIPLIER: int = 2  # множитель для расчета калорий

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
        speed: float = 0
        speed = self.length_pool * self.count_pool / self.M_IN_KM
        speed /= self.duration
        return speed

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий.
        Вычисляет затраченные калории по формуле:
        (средняя_скорость + 1.1) * 2 * вес
        """
        CALORIES_MEAN_SPEED_SHIFT: int = 1.1  # слагаемое скорости
        CALORIES_WEIGHT_MULTIPLIER: int = 2  # множитель для расчета калорий
        speed: float = self.get_mean_speed()  # скорость
        weight: float = self.weight  # вес
        duration: float = self.duration
        calories: float = speed + CALORIES_MEAN_SPEED_SHIFT
        calories *= CALORIES_WEIGHT_MULTIPLIER * weight * duration
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
    if workout_type == 'WLK' or workout_type == 'Walking':
        return SportsWalking(data[0], data[1], data[2], data[3])
    elif workout_type == 'RUN' or workout_type == 'Running':
        return Running(data[0], data[1], data[2])
    elif workout_type == 'SWM' or workout_type == 'Swimming':
        return Swimming(data[0], data[1], data[2], data[3], data[4])


def main(training: Training) -> None:
    """Главная функция.
    Выводит информаци"""
    info: InfoMessage = training.show_training_info()
    message: str = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
