# Telegram Бот для сбора голосового датасета
**Задача:**<br>
Собрать датасет голосового ввода для обучения нейронной сети по распознаванию голоса

**Результаты:**<br>
Разработан Telegram бот разбивающий входной файл на короткие фразы и предоставляющий их пользователю для озвучивания. Все голосовые сообщения сохраняются в папку Data в формате .WAV (Данный формат требовался на выходе для обучения уже готовой нейронной сети). Так же для удобства дальнейшего использования все файлы собраны в таблицу, которая хранит длительность, путь к файлу и расшифровку. После требуется лишь прочитать manifest.csv и собрать из этого Tensorflow.Dataset. Так же реализовано сохранение прогресса пользователя, что позволяет не держать бота всегда включенным, а включать лишь по требованию.

**Внедрение:**<br>
Бот опробован и с его помощью уже успешно собран Датасет из 400 наименований, пополнивший открытый Датасет.
