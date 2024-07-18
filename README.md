# 1. Описание
Disciples Mobile - пошаговая игра в жанре Turn Base RPG, с боями в стиле "Стенка на стенку", прокачкой существ и отстройкой Столицы, созданная на основе известной TBS Disciples 2. Разработка ведется уже 2 года в одиночку. Создавалось с целью лучшего понимания ООП.
## Игровой процесс: 
- выбор стартового героя (герой выбирается один раз за игру); 
- найм существ в Столице за золото:
- продвижение на карте Кампании; 
- участие в боях стенка на стенку; 
- отстройка Столицы;
- улучшение героя и существ;
- победа над главным Боссом.
После победы в бою юниты и герой получают опыт, а игрок - золото. При достижении нужного для повышения количества опыта, юнит переходит на следующую ступень развития. Для этого должно быть отстроено соответствующее здание в Столице за золото. Герои при переходе на новый уровень получают повышенные характеристики и случайный перк (способность). В конце каждого уровня кампании будет поджидать Босс. За победу над Боссом нас будет ждать повышенная награда, а также переход на следующий уровень Кампании. Всего в Кампании 3 уровня на Сложностях 1 и 2. И 4 уровня Кампании на Сложности 3.
![](images/gif/battle_anim/disciples_rec.gif)

# 2. Стек технологий
- python 3
- PyQt5
- SQLAlchemy
- sqlite / postgres
- pyinstaller

# 3. Инструкция по установке
- Способ 1 - exe-file Работает только на Windows. Скачиваем весь архив. Запускаем exe-file из папки 'dist'.
- Способ 2 - скачиваем весь архив. Устанавливаем все зависимости (файл requirements.txt). Запускаем client_main_window.py

# 4. Инструкция по использованию (как играть)
## НОВАЯ ИГРА
- Сначала нужно выбрать или создать игрока
- Для выбора фракции нажать кнопку "Выбор фракции"
- Далее выбрать - продолжить игру или начать новую
- Выбрать героя для старта (4 класса героев: боец, маг, стрелок и жезлоносец)
- В окне Армии можно нанять бойцов для отряда, посмотреть их характеристики, а также расставить своих существ.
- В окне Построек можно посмотреть ветви развития своих существ, все стадии их развития и что требуется для постройки зданий.
## НАЙМ ЮНИТОВ
- Для найма армии нужно зайти в окно "Столица" и нажать на кнопку "Экран армии", либо нажать клавишу "P"
- Чтобы нанять юнита, нужно нажать на пустой слот рядом со слотом совего героя
## ПОСТРОЙКА В СТОЛИЦЕ
- Для входа в окно Построек в главном окне Столицы нажать на кнопку "Построить здание", либо нажать клавишу "S"
- Откроется дерево постройки стрелков. Для выбора других ветвей существ, нужно переходить по кнопкам "Маги", "Бойцы", "Поддержка". 
## КАМПАНИЯ
- Для начала Кампании нужно выйти на Главное окно (MainWindow) и выбрать Сложность от 1 до 3.
- Далее нажать кнопку Кампания. Откроется окно со случайно сгенерированными отрядами врагов, сквозь которых нужно пройти до главного Босса.
- Выбираем отряд, который хотим атаковать, при желании смотрим характеристики бойцов. Вокруг активного вражеского отряда будет красная рамка.
- Для нападения нажимаем кнопку "В бой!"
## ОКНО БИТВЫ
- Юниты ходят в порядке их Инициативы. Юниты с более высокой Инициативой ходят первыми.
- Для выбора цели можно навести курсор как на самого юнита, так и на его иконку. При нажатии ЛКМ активный юнит атакует выбранную цель.
- Кнопка "Автобой" - активное существо само атакует наиболее подходящую цель.
- Кнопка "Защита" - активный юнит пропускает ход и получает 50% бонус к Броне до совего следующего хода.
- Кнопка "Ожидание" - активный юнит переносится в конец по шкале Инициативы. Если ожидающих юнитов несколько, последним будет ходить наиболее инициативный.
