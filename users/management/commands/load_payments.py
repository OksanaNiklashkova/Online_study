import os
import random
from datetime import date, timedelta

from django.core.management import BaseCommand, call_command

from studies.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):
    help = "заполняет БД объектами модели платеж, создает по 10 объектов с рандомными данными за один запуск"

    def handle(self, *args, **options):
        count = 10

        courses = Course.objects.all()
        lessons = Lesson.objects.all()
        users = User.objects.all()

        payment_methods = [Payment.CASH, Payment.TRANSFER]
        created_count = 0

        for i in range(count):
            try:
                # Случайный пользователь
                user = random.choice(users)

                # Случайная дата (последние 30 дней)
                payment_date = date.today() - timedelta(days=random.randint(0, 30))

                # Случайная сумма (от 1000 до 10000)
                amount = round(random.uniform(1000, 10000), 2)

                # Случайный метод оплаты
                payment_method = random.choice(payment_methods)

                # Создаем платеж
                payment = Payment.objects.create(
                    user=user,
                    payment_date=payment_date,
                    amount=amount,
                    payment_method=payment_method
                )

                # Добавляем случайный курс или урок
                if courses.exists() and random.choice([True, False]):
                    course = random.choice(courses)
                    payment.paid_course.add(course)

                if lessons.exists() and random.choice([True, False]):
                    lesson = random.choice(lessons)
                    payment.paid_lesson.add(lesson)

                created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Создан платеж #{created_count}: {user.username} - {amount} руб.'
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка при создании платежа: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано {created_count} платежей из {count} запланированных'
            )
        )