from django.db import models
from django.conf import settings
import os
import requests
import logging

logger = logging.getLogger(__name__)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if hasattr(self.user, "telegram_id") and self.user.telegram_id:
            self.send_telegram_notification()

    def send_telegram_notification(self):
        token = os.getenv("TELEGRAM_TOKEN")

        if not token:
            logger.error("TELEGRAM_TOKEN не установлен в .env или переменных окружения.")
            return

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": self.user.telegram_id,
            "text": "Вам пришёл новый заказ!"
        }

        try:
            response = requests.post(url, data=data)
            if response.status_code != 200:
                logger.error(f"Ошибка Telegram API {response.status_code}: {response.text}")
            else:
                logger.info("Сообщение успешно отправлено в Telegram.")
        except Exception as e:
            logger.exception(f"Ошибка при отправке сообщения в Telegram: {e}")
