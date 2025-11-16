# 📘 **Personal Assistant CLI**

**Personal Assistant CLI** — це консольний помічник, який дозволяє:
- зберігати контакти (телефони, email, адреси, дні народження)
- вести нотатки з тегами
- шукати та переглядати записи
- користуватися автодоповненням команд
- зручно працювати з кольоровими підказками в терміналі

Додаток працює локально та зберігає ваші дані в  
**`~/.assistant/addressbook.pkl`**, незалежно від того, на якій ви операційній системі.

---

## 🚀 Встановлення

### 1. Встановлення через PyPI (рекомендовано)

```

pip install personal-assistant

```

### 2. Запуск програми

Після встановлення з’являється команда:

```

assistant

```

Це запустить інтерфейс Personal Assistant CLI.

---

## 📂 Де зберігаються дані?

Контакти та нотатки зберігаються **не в пакеті**, а у вашому домашньому каталозі:

- Linux / macOS: `/home/USER/.assistant/addressbook.pkl`
- Windows: `C:\Users\USER\.assistant\addressbook.pkl`

Файл створюється автоматично.

---

## 📜 Основні можливості

### 👥 **Робота з контактами**
```
       Дія        |         Команда
--------------------------------------------------------
Додати контакт    | `add John 380991234567`
Змінити телефон   | `change John 380991234567 0671234567`
Видалити контакт  | `delete John`
Показати телефон  | `phone John`
Показати email    | `email John`
Показати день народження  | `birthday John`
Показати повну інформацію | `contact John`
Вивести всі контакти      | `all`
```

## ✉ Email
```
     Дія       |            Команда
--------------------------------------------------------
Додати email   | `add-email John example@gmail.com`
Змінити email  | `change-email John old@gmail.com new@gmail.com`
Видалити email | `delete-email John example@gmail.com`
```

## 🎂 Дні народження
```
               Дія                |     Команда
--------------------------------------------------------
Додати день народження            | `add-birthday John 2000-01-31`
Показати день народження          | `birthday John`
Дні народження у найближчі 7 днів | `birthdays`
У найближчі 35 днів               | `birthdays 35`
```

## 🏠 Адреси
```
      Дія     |     Команда
--------------------------------------------------------
Додати адресу | `add-address John Kyiv, Lesi Ukrainky 12`
```

## 📝 Нотатки
```
          Дія         |     Команда
--------------------------------------------------------
Додати нотатку      | `add-note`
Видалити нотатку    | `delete-note`
Змінити нотатку     | `change-note`
Знайти за назвою    | `find-note-by-title`
Знайти за тегом     | `find-note-by-tag`
Вивести всі нотатки | `all-notes`
```

## 🤖 Загальні команди
```
        Дія       |     Команда
--------------------------------------------------------
Привітання        | `hello`
Завершення роботи | `exit` або `close`
Довідка           | `help`
```

## 🧩 Автодоповнення команд

Додаток підтримує:

- підказки під час набору
- пошук найближчої команди (`Did you mean..?`)
- кольоровий інтерфейс (через `colorama`)

---
## ❓ FAQ / Поширені питання

- Де зберігаються мої контакти?
```
~/.assistant/addressbook.pkl (Linux/macOS) 
або 
C:\Users\USER\.assistant\addressbook.pkl (Windows).
```
- Чому я бачу старі дані після видалення пакета?
```
Дані залишаються у файлі addressbook.pkl. Щоб почати з чистого листа — видали цей файл.
```
- Чи можна переносити дані на інший комп’ютер?
```
Так, скопіюй файл addressbook.pkl на нову машину в аналогічне розташування.
```
- Як додати нову команду чи змінити поведінку бота?

```
Для цього потрібно редагувати код у папці src/personal_assistant
та перевстановити пакет локально (pip install -e .).
```
## ⌨️ Короткі приклади використання

#### Додати контакт
`assistant> add John 380991234567`

#### Додати email
`assistant> add-email John john@gmail.com`

#### Перевірити день народження
`assistant> birthday John`

#### Подивитись всі контакти
`assistant> all`

## 💠 Системні вимоги
- Python ≥ 3.9
- Пакети: colorama, prettytable, prompt_toolkit, wcwidth
- Працює на Linux, macOS та Windows

## 📦 Структура проєкту (для розробників)

```
personal-assistant/
│
├── src/personal_assistant/
│   ├── addressbook.py
│   ├── colorize.py
│   ├── command_use.py
│   ├── commands.py
│   ├── errors.py
│   ├── fields.py
│   ├── input_parser.py
│   ├── notes.py
│   ├── pickle_data.py
│   ├── record.py
│   ├── utils.py
│   └── **init**.py
│
├── main.py
├── pyproject.toml
├── setup.cfg
├── requirements.txt
└── README.md
```

## 🛠 Розробка та локальне встановлення

### Клонування

```
git clone [https://github.com/](https://github.com/)<your_repo>/personal_assistant
cd personal_assistant
```

### Локальна установка у режимі розробки

```
pip install -e .
```

### Запуск локальної версії

```
assistant
```

---

## 📤 Публікація на PyPI

### Створити дистрибутив

```
python -m build
```

### Завантажити

```
twine upload dist/*
```

---

## 📝 Ліцензія та внесок
Проект ліцензований під **MIT License**.
Внесок: через pull request або issue на GitHub

---

## ❤️ Автори

Команда **Pythonauts**  
Ваш персональний CLI-асистент для роботи з контактами та нотатками.

## 📫 Контакт / Підтримка
- GitHub: https://github.com/yulikafsd/personal_assistant
- Email: ju.zagorovsky@gmail.com

```