# Инструкция для программиста ЧПУ

## Что готово

Новый сценарий поддерживает тринадцать типов со стандартными сборками:

| Код `--type` | Тип |
| --- | --- |
| `ballmill` | Сферическая фреза |
| `centerdrill` | Центровка |
| `diskmill` | Дисковая фреза |
| `counterbore` | Цековка |
| `countersink` | Зенковка |
| `drill` | Обычное спиральное сверло |
| `endmill` | Обычная концевая фреза |
| `reamer` | Развёртка |
| `tap_blind` | Метчик для глухого отверстия |
| `tap_through` | Метчик для сквозного отверстия |
| `toroidmill` | Тороидальная фреза |
| `chamfermill` | Угловая фасочная фреза |
| `threadmill` | Резьбовая фреза |
| `internalradiusmill` | Фреза внутреннего радиуса |

Токарно-фрезерные оправки и другие типы пока доступны только через прежние
задания. Они не перенесены в CSV.

Новая серия — это папка с четырьмя файлами. Python редактировать не нужно.
Серия содержит по одному варианту длины для каждого диаметра и одинаковое
число зубьев. Для другого числа зубьев или другой длины создайте другую серию.
Диаметры поддерживаются с точностью до 0,01 мм.

Все пути ниже считаются от корня скачанного проекта. В текущей рабочей копии
это `d:/PROJ/CREO_tool_xml_generator`. Команды выполняйте в терминале из этой
папки. После переноса проекта используйте его новый путь.

## 0. Подготовить программу один раз

Нужны установленный uv и Python 3.14. Выполните:

```bash
uv sync --locked
uv run python -m src.tool_updater --help
uv run python -m src.tool_updater types
```

Для безопасной тренировки есть серия `demo_ballmill` с искусственными данными:

```bash
uv run python -m src.tool_updater check --series demo_ballmill
uv run python -m src.tool_updater show --series demo_ballmill
uv run python -m src.tool_updater generate --series demo_ballmill
```

Её результат находится в `generated_xmls/series/demo_ballmill/`.
**Не используйте учебный результат на станке.**

## 1. Найти каталог производителя

Найдите PDF с нужной серией. Проверьте обозначение, материал инструмента,
число зубьев, единицы размеров, материал заготовки и условия режимов.
Сохраните PDF у себя. Публиковать его вместе с проектом не требуется.

Программа не извлекает таблицы из PDF. Копируйте таблицу в редактор таблиц,
затем переносите нужные значения в столбцы шаблона. Проверьте перенос строк,
десятичные разделители и сноски производителя.

## 2. Создать серию

Пример имени папки: `my_tool`. Используйте строчные латинские буквы,
цифры и `_`, первый символ — буква. Максимум 60 символов.

```bash
uv run python -m src.tool_updater init --series my_tool --type ballmill
```

Создаётся папка `catalogs/my_tool/`:

| Файл | Что внести |
| --- | --- |
| `series.toml` | Название серии и число зубьев |
| `geometry.csv` | Таблицу размеров |
| `cutting.csv` | Таблицу режимов |
| `source.txt` | Название PDF, редакцию, страницы, условия режимов |

Повторный `init` не заменяет существующую папку.

## 3. Заполнить описание

В `catalogs/my_tool/series.toml` замените название и число зубьев:

```toml
name = "Производитель — обозначение серии"
type = "ballmill"
teeth = 2
```

В заготовке `teeth = 0`: это преднамеренная блокировка генерации, пока вы
не укажете настоящее число зубьев. Строку `type` не меняйте после `init`:
она определяет таблицу размеров и расчётный класс.

## 4. Перенести таблицу размеров

Заголовок `geometry.csv` зависит от типа. Не меняйте его.

Для `ballmill` и `endmill`:

```text
diameter_mm;flute_length_mm;length_mm;order_no
```

Для `centerdrill` задаются оба диаметра, длина сверления и два угла:

```text
drill_diameter_mm;cutter_diameter_mm;flute_length_mm;length_mm;order_no;point_angle_deg;countersink_angle_deg;drill_length_mm
```

`drill_diameter_mm` — диаметр сверления. Он используется для режимов
резания и должен быть меньше `cutter_diameter_mm`. `cutter_diameter_mm` —
наружный диаметр центровки. `point_angle_deg` и
`countersink_angle_deg` должны быть больше 0 и меньше 180°. Длина
`drill_length_mm` должна быть меньше `flute_length_mm`.

Для `diskmill` задаются параметры диска, хвостовика и встроенной оправки:

```text
diameter_mm;cutter_width_mm;corner_radius_mm;corner_chamfer_mm;corner_chamfer_angle_deg;flute_length_mm;holder_length_mm;holder_min_length_mm;shank_diameter_mm;teeth_num;order_no
```

`diameter_mm` — диаметр диска. `cutter_width_mm` — ширина диска и ключ
поиска режимов резания. `flute_length_mm` — рабочая длина. Для дисковой
фрезы `holder_length_mm` используется как общая длина legacy-инструмента.
`holder_min_length_mm` — минимальный вылет; он не должен быть больше
`holder_length_mm`. `shank_diameter_mm` — диаметр хвостовика. Поля
`corner_radius_mm`, `corner_chamfer_mm` и `corner_chamfer_angle_deg` могут
быть равны нулю. `teeth_num` задаёт число зубьев строки.

В новом CSV-сценарии данные оправки берутся из этой строки, а не из
legacy-файла `holders_for_SGSF.json`. XML и BOM всё равно создаются
существующим классом дисковой фрезы; проверьте названия сборок в CREO.

| Столбец | Значение |
| --- | --- |
| `diameter_mm` | Диаметр режущей части, мм |
| `flute_length_mm` | Длина режущей части, мм |
| `length_mm` | Общая длина инструмента, мм |
| `order_no` | Артикул или комментарий; можно оставить пустым |

Для `drill` добавляется угол при вершине:

```text
diameter_mm;flute_length_mm;length_mm;order_no;point_angle_deg
```

Для `countersink` добавляются диаметр и угол вершины:

```text
diameter_mm;flute_length_mm;length_mm;order_no;point_diameter_mm;point_angle_deg
```

`point_diameter_mm` — диаметр площадки у вершины. Он должен быть меньше
`diameter_mm`. `point_angle_deg` — угол зенковки, меньше 180°.

Для `counterbore` задаются направляющая и длина зажима:

```text
diameter_mm;flute_length_mm;length_mm;order_no;point_diameter_mm;tip_offset_mm;tail_holding_length_mm
```

`point_diameter_mm` — диаметр направляющей, меньше `diameter_mm`.
`tip_offset_mm` — длина направляющей. `tail_holding_length_mm` — часть
общей длины в зажиме; она должна быть меньше `length_mm`.

Для `reamer` задаются вылет и фаска:

```text
diameter_mm;flute_length_mm;length_mm;order_no;length_out_of_holder_mm;corner_chamfer_mm
```

`length_out_of_holder_mm` — вылет развёртки, не больше `length_mm`.
`corner_chamfer_mm` записывается в XML как фаска режущей части.

Для `tap_blind` и `tap_through` используется одна схема:

```text
diameter_mm;flute_length_mm;length_mm;order_no;point_diameter_mm;chamfer_length_mm;thread_pitch_mm
```

`point_diameter_mm` — диаметр отверстия под резьбу, меньше диаметра
метчика. `chamfer_length_mm` — длина заходной фаски. `thread_pitch_mm` —
шаг резьбы: старый расчёт использует его как подачу на оборот. Выберите
`tap_blind` или `tap_through` по виду отверстия: XML ссылается на разные
сборки CREO.

Для `toroidmill` добавляется радиус скругления:

```text
diameter_mm;flute_length_mm;length_mm;order_no;corner_radius_mm
```

`corner_radius_mm` должен быть больше 0 и меньше половины диаметра.

Для `chamfermill` используется отдельная схема размеров:

```text
tip_diameter_mm;shank_diameter_mm;cut_length_mm;length_mm;order_no;angle_deg
```

`tip_diameter_mm` — диаметр кончика, `shank_diameter_mm` — диаметр
хвостовика, `cut_length_mm` — рабочая длина. `angle_deg` — полный угол
фрезы, больше 0 и меньше 180°.

Для `threadmill` добавляется шаг резьбы:

```text
diameter_mm;flute_length_mm;length_mm;order_no;thread_pitch_mm
```

`thread_pitch_mm` записывается в XML как смещение конца резьбовой фрезы.
Расчёт класса использует подачу на зуб: значения `F` и `Fn` из
`cutting.csv` автоматически приводятся к `Fz`.

Для `internalradiusmill` используется отдельная схема:

```text
cutter_diameter_mm;shank_diameter_mm;length_mm;order_no;corner_radius_mm
```

`cutter_diameter_mm` — диаметр режущей части, `shank_diameter_mm` —
диаметр хвостовика. `corner_radius_mm` задаёт радиус и расчётную длину
режущей части. Режимы приводятся к подаче на зуб (`Fz`).

| Дополнительный столбец | Значение |
| --- | --- |
| `point_angle_deg` | Угол при вершине сверла в градусах, больше 0 и меньше 180 |

Одна строка — один типоразмер. Рабочая длина должна быть меньше общей.
В этом сценарии вылет рассчитывается старым методом: рабочая длина плюс
диаметр с округлением. Если он больше общей длины, проверка остановится.
Для `endmill` PDF часто содержит диаметр хвостовика. Обычный старый класс
EndMill в текущем XML не использует это значение. Поэтому такого столбца
нет: не создавайте поле, которое не влияет на результат. Проверьте сборку
и хвостовик в CREO. Для типов со специальным хвостовиком нужен отдельный
сценарий, а не подмена значения в этой таблице.

## 5. Перенести таблицу режимов

Откройте `catalogs/my_ballmill/cutting.csv`. Заголовок:

```text
material;diameter_mm;vc_m_min;feed_kind;feed_value
```

Для `diskmill` добавьте глубину резания по радиусу:

```text
material;diameter_mm;vc_m_min;feed_kind;feed_value;radial_depth_mm
```

`radial_depth_mm` — Ae в миллиметрах. Это значение сохраняется в XML для
дисковой фрезы; остальные типы используют общую схему без этого столбца.

| Столбец | Значение |
| --- | --- |
| `material` | Группа: `iso_P`, `iso_M`, `iso_K`, `iso_N`, `iso_S`, `iso_H` |
| `diameter_mm` | Диаметр из таблицы размеров, мм |
| `vc_m_min` | Скорость резания Vc, м/мин |
| `feed_kind` | `F` — мм/мин; `Fz` — мм/зуб; `Fn` — мм/оборот |
| `feed_value` | Значение подачи именно в выбранных единицах |
| `radial_depth_mm` | Ae, только для `diskmill`, мм |

Одна строка — одна пара «группа материала + диаметр».
Не вставляйте интервалы `80–120`, единицы `мм` или формулы в числовые поля.
Если PDF содержит диапазон, технолог должен выбрать значение и записать
основание выбора в `source.txt`. Нельзя автоматически считать любое значение
диапазона подходящим для ваших условий.

Сейчас для каждого диаметра нужны все шесть групп ISO. Если производитель
не даёт нужные режимы, **не заполняйте пробелы выдуманными числами**:
этот каталог пока нельзя использовать в новом сценарии. Выбор ограниченного
набора материалов потребует отдельного изменения генератора.

### Как сохранить CSV

- Кодировка UTF-8; UTF-8 с BOM также поддерживается.
- Разделитель столбцов — `;`, не запятая и не табуляция.
- Десятичный разделитель — точка или запятая; без разделителей тысяч.
- Сохраняйте именно CSV, а не XLSX под именем CSV.
- Не меняйте английские имена столбцов и регистр кодов материалов.
- Если в комментарии есть `;` или кавычки, сохраняйте файл через редактор
  таблиц: он должен корректно заключить значение в кавычки.

## 6. Найти серию и проверить данные

Никакие строки в Python добавлять не нужно. CLI находит папки автоматически.

```bash
uv run python -m src.tool_updater list
uv run python -m src.tool_updater check --series my_tool
uv run python -m src.tool_updater show --series my_tool
```

`list` показывает описания, а не подтверждённую готовность данных.
`check` проверяет таблицы, расчёты и синтаксис XML, но не пишет файлы.
`show` дополнительно показывает множители и итоговые режимы по диаметрам.
При ошибке исправьте указанный файл и строку, затем повторите `check`.
Числовые значения должны быть конечными и положительными; повторы запрещены.

## 7. Получить XML

```bash
uv run python -m src.tool_updater generate --series my_tool
```

Результат: `generated_xmls/series/my_tool/`, один XML на диаметр.
В конце программа печатает полный путь результата.
По умолчанию существующие XML не заменяются. Для повторной генерации:

```bash
uv run python -m src.tool_updater generate --series my_tool --overwrite
```

Перед записью проверяются все данные и XML. Каждый файл сначала записывается
во временный файл. Сбой замены не обрезает прежний XML. Но общей отмены серии
нет: успешно записанные файлы остаются, если следующий файл записать не удалось.
Для записи без замены файловая система должна поддерживать жёсткие ссылки
(проверено на локальном диске Windows); некоторые сетевые диски и FAT могут
не поддерживать этот способ. При ошибке выберите локальную папку вывода.

## 8. Изменить множители

Редактируйте файл настроек типа, а не Python-классы:

| Тип | Файл |
| --- | --- |
| `ballmill` | `settings/machining.toml` |
| `diskmill` | `settings/diskmill.toml` |
| `counterbore` | `settings/counterbore.toml` |
| `countersink` | `settings/countersink.toml` |
| `drill` | `settings/drill.toml` |
| `endmill` | `settings/endmill.toml` |
| `reamer` | `settings/reamer.toml` |
| `tap_blind`, `tap_through` | `settings/tap.toml` |
| `toroidmill` | `settings/toroidmill.toml` |
| `chamfermill` | `settings/chamfermill.toml` |
| `threadmill` | `settings/threadmill.toml` |
| `internalradiusmill` | `settings/internalradiusmill.toml` |

| Раздел/параметр | Что изменяет |
| --- | --- |
| `[roughing]`, `[finishing]` | Режимы из `cutting.csv`; множителей нет |
| `[axial]` | Коэффициент диаметра для глубины Ap по группам ISO |
| `[radial]` | Коэффициент диаметра для ширины Ae по группам ISO |

Подачи F/Fz/Fn приводятся к единицам, которые ожидает выбранный тип.
Скрытые множители режимов не применяются. Исходные Ap/Ae
из PDF в этом этапе не загружаются: они рассчитываются из диаметра.
Для `counterbore`, `drill`, `countersink` и `reamer` старый расчёт всегда
задаёт `Ae = 0`.
Для `tap_blind` и `tap_through` старый класс также задаёт `Ap = 0`; это
сохранённое legacy-поведение, а не технологическая рекомендация.
Legacy-ограничение оборотов 18000 об/мин сохраняется. Дополнительные
материалы (пластики, латунь) вычисляются из ISO-групп в старом сценарии.
Новая серия использует только заявленные ISO-группы; пустые группы не
добавляются в её XML. `show` показывает только рассчитанные значения.

Для отдельной серии скопируйте файл настроек, измените копию и каждый раз
передавайте один и тот же `--settings` командам `check`, `show`, `generate`.
Без этого флага используется общий файл. Скрытых настроек на уровне серии нет.

## 9. Флаги и справка

| Флаг | Где используется | Назначение |
| --- | --- | --- |
| `--help` | Везде | Справка; например `generate --help` |
| `--series NAME` | `init`, `check`, `show`, `generate` | Имя папки серии |
| `--type TYPE` | `init` | `ballmill`, `centerdrill`, `chamfermill`, `counterbore`, `countersink`, `diskmill`, `drill`, `endmill`, `internalradiusmill`, `reamer`, `tap_blind`, `tap_through`, `threadmill` или `toroidmill` |
| `--settings PATH` | `check`, `show`, `generate` | Другой файл множителей |
| `--output PATH` | `generate` | Итоговая папка, без автоматической подпапки серии |
| `--overwrite` | `generate` | Разрешить замену одноимённых XML |
| `--catalogs PATH` | **Перед командой** | Другая корневая папка серий |

Пути с пробелами заключайте в кавычки. Относительные пути флагов считаются
от текущей папки терминала. Пример для другой библиотеки:

```bash
uv run python -m src.tool_updater --catalogs "D:/Tool library/catalogs" list
```

## 10. Проверить результат в CREO

Успешный `check` подтверждает структуру данных и синтаксис XML, но не
пригодность для обработки. Проверьте импорт, доступность моделей сборок,
диаметр, длины, вылет, единицы, материал инструмента и все режимы.
Проверку должен выполнить специалист до применения результата на станке.
Совместимость с конкретной версией CREO в этой работе не подтверждена.

Старые JSON-каталоги не перенесены автоматически. Прежний запуск
`uv run python -m src.tool_updater.main --list` остаётся доступен,
но это другой сценарий: он использует прежние настройки и Python-задания.
