import telebot
import json
from telebot import types

bot = telebot.TeleBot('')

#запятая после старшего разряда
def ffz(number):
    if abs(number) >= 1 and number < 0: number = number * 10 ** ((-1) * (len(str(int(number))) - 1))
    elif abs(number) >= 1 and number >= 0: number = number * 10 ** ((-1) * (len(str(int(number)))))
    return number

#двоичное представление вещественного числа
def fbin(number):
    number = abs(number)
    #c = bin(int(number))[2:]
    #number -= int(number)
    x = ''
    for i in range(16):
        number *= 2
        x += str(int(number))
        number -= int(number)
    return str(int(x) / 10 ** 16) #+ int(c)

#прямой код числа
def direct_code(number):
    if type(number) == int:
        x = '1|' + bin(number)[3:] if number < 0 else '0|' + bin(number)[2:]
    else:
        prom_f = fbin(number)
        x = '1' + prom_f[1:] if number < 0 else prom_f
    return x

#обратный код числа
def reverse_code(number):
    if number < 0:
        number = direct_code(number)
        znak = number[:2]
        number = number[2:].replace("0","2")
        number = number.replace("1","0")
        number = number.replace("2","1")
        return znak + number
    else:
        return direct_code(number)

#дополнительный код числа
def additional_code(number, carry = 1):
    result = number[-1]
    if result == '1' and carry == 1:
        result = '0'
        carry = 1
    elif result == '0' and carry == 1:
        result = '1'
        carry = 0
    if len(number) > 1:
        result = additional_code(number[:-1], carry) + result
    return result

#сложение в прямых кодах
def addition_direct_code(message):
    f_bool = False
    if str(message.text).count('-') in [0, 2]:
        msg = (str(message.text)).split(" ")
        if '.' in msg[0]:
            f_bool = True
        if f_bool == True:
            msga = float(msg[0])
            msgb = float(msg[1])
            a = "-" + fbin(ffz(msga)) if "-" in msg[0] else fbin(ffz(msga))
            b = "-" + fbin(ffz(msgb)) if "-" in msg[0] else fbin(ffz(msgb))
            fsum = ffz(msga + msgb)
        else:
            msga = int(msg[0])
            msgb = int(msg[1])
            a = "-" + bin(msga)[3:] if "-" in msg[0] else bin(msga)[2:]
            b = "-" + bin(msgb)[3:] if "-" in msg[1] else bin(msgb)[2:]
            fsum = msga + msgb
        bot.send_message(message.chat.id, f'A = {msg[0]}(10) = {a}(2)\n'
                                          f'B = {msg[1]}(10) = {b}(2)\n'
                                          f'Aпр = {direct_code(msga)}\n'
                                          f'Bпр = {direct_code(msgb)}\n'
                                          f'*Cпр = {direct_code(fsum)}*\n'
                                          f'C = {msga + msgb}', parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, '🫢 Упс, читай внимательнее тему, числа должны быть одного знака!')

#сложение в обратных кодах
def addition_reverse_code(message):
    f_bool = False
    msg = (str(message.text)).split(" ")
    if '.' in msg[0] or '.' in msg[1]:
        msga = float(msg[0])
        msgb = float(msg[1])
        a = "-" + fbin(ffz(msga)) if "-" in msg[0] else fbin(ffz(msga))
        b = "-" + fbin(ffz(msgb)) if "-" in msg[1] else fbin(ffz(msgb))
        fsum = ffz(msga + msgb)
    else:
        msga = int(msg[0])
        msgb = int(msg[1])
        a = "-" + bin(msga)[3:] if "-" in msg[0] else bin(msga)[2:]
        b = "-" + bin(msgb)[3:] if "-" in msg[1] else bin(msgb)[2:]
        fsum = msga + msgb
    bot.send_message(message.chat.id, f'A = {msg[0]}(10) = {a}(2)\n'
                                      f'B = {msg[1]}(10) = {b}(2)\n'
                                      f'Aобр = {reverse_code(msga)}\n'
                                          f'Bобр = {reverse_code(msgb)}\n'
                                          f'*Cобр = {reverse_code(fsum)}*\n'
                                          f'C = {msga + msgb}', parse_mode='Markdown')

#сложение в дополнительных кодах
def addition_add_code(message):
    f_bool = False
    msg = (str(message.text)).split(" ")
    if '.' in msg[0] or '.' in msg[1]:
        msga = float(msg[0])
        msgb = float(msg[1])
        a = "-" + fbin(ffz(msga)) if "-" in msg[0] else fbin(ffz(msga))
        b = "-" + fbin(ffz(msgb)) if "-" in msg[1] else fbin(ffz(msgb))
        fsum = ffz(msga + msgb)
    else:
        msga = int(msg[0])
        msgb = int(msg[1])
        a = "-" + bin(msga)[3:] if "-" in msg[0] else bin(msga)[2:]
        b = "-" + bin(msgb)[3:] if "-" in msg[1] else bin(msgb)[2:]
        fsum = msga + msgb
    rca = reverse_code(msga)
    rcb = reverse_code(msgb)
    rcf = reverse_code(fsum)
    bot.send_message(message.chat.id, f'A = {msg[0]}(10) = {a}(2)\n'
                                          f'B = {msg[1]}(10) = {b}(2)\n'
                                          f'Aдоп = {rca[:2] + additional_code(rca[2::]) if rca[0] == "1" else direct_code(msga)}\n'
                                          f'Bдоп = {rcb[:2] + additional_code(rcb[2::]) if rcb[0] == "1" else direct_code(msgb)}\n'
                                          f'*Cдоп = {rcf[:2] + additional_code(rcf[2::]) if rcf[0] == "1" else direct_code(fsum)}*\n'
                                          f'C = {msga + msgb}', parse_mode='Markdown')

#старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "👋 Привет, я твой бот-помощник по изучению основ построения ЭВМ!")

#обработка обратных вызовов кнопок
@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    req = call.data.split('_')
    markup = types.InlineKeyboardMarkup()
    #темы
    if 'Кодирование чисел в ЭВМ.' in req:
        markup.add(types.InlineKeyboardButton(text=f'Тема.', callback_data=f'Кодирование чисел в ЭВМ. Тема.'),
                   types.InlineKeyboardButton(text=f'Перевод чисел.', callback_data=f'Перевод чисел.'))
        markup.add(types.InlineKeyboardButton(text=f'<--- Назад', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + '1'
                                                                                + ",\"CountPage\":" + '4' + "}"))
        bot.edit_message_text(f'Выбери из списка:', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    elif 'ФПЧ.' in req:
        markup.add(types.InlineKeyboardButton(text=f'Тема.', callback_data=f'ФПЧ. Тема.'))
        markup.add(types.InlineKeyboardButton(text=f'<--- Назад', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + '1'
                                                                                + ",\"CountPage\":" + '4' + "}"))
        bot.edit_message_text(f'Выбери из списка:', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    elif 'ППЧ.' in req:
        markup.add(types.InlineKeyboardButton(text=f'Тема.', callback_data=f'ППЧ. Тема.'))
        markup.add(types.InlineKeyboardButton(text=f'<--- Назад', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + '1'
                                                                                + ",\"CountPage\":" + '4' + "}"))
        bot.edit_message_text(f'Выбери из списка:', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    elif 'СЧВАК.' in req:
        markup.add(types.InlineKeyboardButton(text=f'Тема.', callback_data=f'СЧВАК. Тема.'))
        markup.add(types.InlineKeyboardButton(text=f'Сложение чисел в прямых кодах.',
                                              callback_data=f'СЧВАК.ПК.'))
        markup.add(types.InlineKeyboardButton(text=f'Сложение чисел в обратных кодах.',
                                              callback_data=f'СЧВАК.ОК.'))
        markup.add(types.InlineKeyboardButton(text=f'Сложение чисел в дополнительных кодах.',
                                              callback_data=f'СЧВАК.ДК.'))
        markup.add(types.InlineKeyboardButton(text=f'<--- Назад', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + '1'
                                                                                + ",\"CountPage\":" + '4' + "}"))
        bot.edit_message_text(f'Выбери из списка:', reply_markup=markup, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)

    #действия
    elif 'Кодирование чисел в ЭВМ. Тема.' in req:
        bot.send_message(call.message.chat.id, f'_Тема: Кодирование чисел в ЭВМ._\n\nОдин из способов выполнения операции '
                                               f'вычитания с помощью сумматора — замена знака вычитаемого на противоположный '
                                               f'и прибавление его к уменьшаемому:\n\nА - В = А + (-В).\n\n'
                                               f'Для машинного представления отрицательных чисел используют прямой, '
                                               f'дополнительный и обратный коды. Рассмотрим на примере чисел, '
                                               f'представленных в форме с фиксированной запятой.'
                                               f'\n\n*Прямой код*\n'
                                               f'Прямой код числа A = -0,a1a2...an — это машинное изображение этого числа в виде '
                                               f'[А]пр = 1,a1a2...an. Из определения следует, что в прямом коде все '
                                               f'цифровые разряды отрицательного числа остаются неизменными, а в '
                                               f'знаковой части записывается единица. Например, если А = -0,101110, то '
                                               f'[А]пр = 1,101110. Положительное число в прямом коде не меняет своего '
                                               f'изображения. _Например_, если А = 0,110101, то [А]пр =0,110101.'
                                               f'\n\n*Обратный код*\n'
                                               f'Обратный код числа A = -0,a1a2...an — такое машинное изображение '
                                               f'этого числа [A]об = -1,b1b2...bn, для которого b1 = 0, если a1 = 1 и b1 = 1, '
                                               f'если a1 = 0. Из определения следует, что обратный код двоичного числа '
                                               f'является инверсным изображением самого числа, в котором все разряды '
                                               f'исходного числа принимают инверсное (обратное) значение, т.е. все нули '
                                               f'заменяются нa единицы, а все единицы — на нули. _Например_, если '
                                               f'А = -0,110101. то [A]об = 1,010001.'
                                               f'\n\n*Дополнительный код*\n'
                                               f'Дополнительный код числа A = -0,a1a2...an — такое машинное изображение '
                                               f'этого числа [A]доп = -1,b1b2...bn, для которого b1 = 0, если a1 = 1 и b1 = 1, '
                                               f'если a1 = 0, за исключением последнего значащего разряда. '
                                               f'_Например_, число A = -0,101110 запишется в дополнительном коде так: '
                                               f'[А]доп = 1,010010. '
                                               f'Сначала инвертируется цифровая часть исходного числа, '
                                               f'в результате получается его обратный код; затем добавляется единица '
                                               f'в младший разряд цифровой части числа и тем самым получаегся дополнительный код.\n\n'
                                               f'Для целых чисел аналогично, _например_,\nA = 101, [А]пр = 0|101\n'
                                               f'B = -1101, [B]пр = 1|1101, [B]обр = 1|0010'
                                               f'\n\n_Если A >= 0, то [А]пр = [А]обр = [А]доп!_'
                                               f'', parse_mode="Markdown")
    elif 'Перевод чисел.' in req:
        bot.send_message(call.message.chat.id, f'🤓 Введи число в десятичной системе счисления. '
                                               f'Вещественные числа вводите меньше единицы через точку!')
    elif 'ППЧ. Тема.' in req:
        bot.send_message(call.message.chat.id, f'_Тема: Погрешность представления чисел._\n\nВиды погрешностей:\n1)*Абсолютная погрешность представления* - '
                                               f'разность между нстннным значением '
                                               f'входной величины А и ее значением, полученным из машинного изображения '
                                               f'Aм,\nт. е. Δ[А] = А - Ам. \n2)*Относительная погрешность представления* -'
                                               f' величина δA = Δ[А]/Ам\n\n'
                                               f'', parse_mode="Markdown")
    elif 'ФПЧ. Тема.' in req:
        bot.send_message(call.message.chat.id, f'_Тема: Форматы представления чисел в ЭВМ._\n\nЧисло 0,028 можно записать так: '
                                               f'28 × 10^(-3), или 0,03 (с округлением), или 2,8 × 10^2 и т. д. '
                                               f'Разнообразие форм в записи одного числа может послужить причиной '
                                               f'затруднений для работы цифрового автомата. \n_Автоматное (машинное) изображение числа_'
                                               f' — представление числа A в разрядной сетке цифрового автомата. '
                                               f'Условно обозначим автоматное изображение числа символом [A]. '
                                               f'Тогда справедливо соотношение: A = [A]Ka, где Кa — коэффициент, величина которого зависит от формы '
                                               f'представления числа в автомате.'
                                               f'\n\nФорматы представления чисел:\n1)*С фиксированной запятой(ФЗ)* - '
                                               f'естественная форма представления числа в цифровом автомате характеризуется тем,'
                                               f' что положение его разрядов в автоматном изображении остается всегда постоянным независимо от величины самого числа.'
                                               f'\n2)*С плавающей запятой(ПЗ)* - экспоненциальная форма представления '
                                               f'вещественных (действительных) чисел, в которой число хранится в виде мантиссы и порядка \n\n'
                                               f'Разновидности формата с ФЗ:\n'
                                               f'1)*Формат с запятой, зафиксированной перед старшим цифровым разрядом*\n'
                                               f'_Например,_ –0.1100110; +0.1100110\n'
                                               f'2)*Формат с запятой, зафиксированной после младшего цифрового разряда*\n'
                                               f'_Например,_ –1100110.0; +1100110.0\n\n'
                                               f'Разновидности формата с ПЗ:\n1)*Со скрытой единицей*\n'
                                               f'Х = -13.5 = -1101.12 = -0.*1*1011 × 10100\n'
                                               f'\n2)*Со смещённым порядком*\n'
                                               f'Х = -13.5 = -1101.12 = -0.11011 × 10100\n'
                                               f'P = 4(10) = 100(2) – истинный порядок числа\n'
                                               f'E = P + смещение – смещённый порядок числа (характеристика числа)\n'
                                               f'для длины разрядной сетки n=8:\n'
                                               f' 0 0 0 0 0 1 0 0 = P\n'
                                               f'+\n'
                                               f' 0 1 1 1 1 1 1 1 = смещение\n'
                                               f'=\n'
                                               f' 1 0 0 0 0 0 1 1 = E\n\n'
                                               f'3)*Со скрытой единицей и смещённым порядком*\n'
                                               f'Скрытая единица позволяет повысить точность представления мантиссы. '
                                               f'Суть метода в том, что в нормализованной мантиссе старшая цифра всегда '
                                               f'равна единице (для представления нуля используется специальная кодовая комбинация). '
                                               f'Следовательно, эта цифра может не записываться, а подразумеваться. '
                                               f'Запись мантиссы начинают с её второй цифры, и это позволяет задействовать '
                                               f'дополнительный значащий бит для более точного представления числа. '
                                               f'Скрытая единица перед выполнением арифметических операций восстанавливается, '
                                               f'а при записи результата — удаляется.\n'
                                               f'Смещённый порядок хранится в разрядах с 1-го по 8-й и может находиться в диапазоне от 0 до 255. '
                                               f'Для получения фактического значения порядка из содержимого этого поля нужно вычесть фиксированное '
                                               f'значение, равное 128. С таким смещением фактические значения порядка могут лежать в диапазоне '
                                               f'от -128 до +127. ', parse_mode="Markdown")
        bot.send_photo(call.message.chat.id, 'https://i.postimg.cc/zL6QBS2D/image.png')
        bot.send_photo(call.message.chat.id, 'https://i.postimg.cc/BLFV1LRT/image.png')
#[url=https://postimg.cc/TypSfH9H][img]https://i.postimg.cc/TypSfH9H/image.png[/img][/url]
#[url=https://postimg.cc/BLFV1LRT][img]https://i.postimg.cc/BLFV1LRT/image.png[/img][/url]
#https://postimg.cc/gallery/Yqf8nBb
#[url=https://postimg.cc/zL6QBS2D][img]https://i.postimg.cc/zL6QBS2D/image.png[/img][/url]
    elif 'СЧВАК. Тема.' in req:
        bot.send_message(call.message.chat.id, f'_Тема: Сложение чисел в алгебраических кодах._\n\n'
                                               f'*Формальные правила двоичной арифметики:*\n'
                                               f'0 + 0 = 0\n'
                                               f'0 + 1 = 1\n'
                                               f'1 + 0 = 1\n'
                                               f'1 + 1 = (1)0, перенос единицы в старший разряд\n\n'
                                               f'0 - 0 = 0\n'
                                               f'1 - 0 = 1\n'
                                               f'1 - 1 = 0\n'
                                               f'0 - 1 = (1)1, заем в старшем разряде\n\n'
                                               f'*Сложение чисел, представленных в форме с фиксированной запятой, '
                                               f'на двоичных сумматорах:*\n'
                                               f'*Двоичный сумматор прямого кода (ДСПК)* — сумматор, в котором отсутствует '
                                               f'цепь, поразрядного переноса между старшим цифровым и знаковым разрядами. '
                                               f'На ДСПК можно складывать только числа, имеющие одинаковые знаки, т. е. '
                                               f'такой сумматор не может выполнять операцию алгебраического сложения.\n'
                                               f'_Например,_ 0.1011 + 0.0100 = 0.111.\n\n'
                                               f'*Двоичный сумматор дополнительного кода (ДСДК)* — сумматор, '
                                               f'оперирующий изображениями чисел в дополнительном коде. Характерная '
                                               f'особенность ДСДК — наличие цепи поразрядного переноса из старшего '
                                               f'разряда цифровой части в знаковый разряд. Если возникает перенос из знакового разряда, '
                                               f'то он отбрасывается.\n'
                                               f'_Сумма дополнительных кодов чисел есть дополнительный код результата!_\n'
                                               f'_Например,_ 1.0101 + 0.0100 = 1.1001 \n--->'
                                               f' Результат = -0.0111.\n'
                                               f'0.0100 + 1.1101 = (1)0.0001 = 0.0001 \n---> Результат = 0.1100.\n\n'
                                               f'*Двоичный сумматор обратного кода (ДСОК)*1 — сумматор, оперирующий'
                                               f' изображениями чисел в обратном коде. Характерная особенность ДСОК '
                                               f'— наличие цепи кругового, или циклического, переноса нз знакового '
                                               f'разряда в младший разряд цифровой части.\n'
                                               f'_Сумма обратных кодов чисел есть обратный код результата._\n'
                                               f'_Например,_ 1.1010 + 1.0111 = (1)1.0001 + 1 = 1.0010 (перенос единицы из знакового разряда)\n--->'
                                               f' Результат = -0.1101.\n'
                                               f'0.0101 + 0.0111 = 0.1100 \n---> Результат = 0.1100.', parse_mode="Markdown")
    elif 'СЧВАК.ПК.' in req:
        bot.send_message(call.message.chat.id, f'🤓 Введи строго в формате "число число"! '
                                               f'_Например,_ -5 -9.', parse_mode='Markdown')
        bot.register_next_step_handler(call.message, addition_direct_code)
    elif 'СЧВАК.ОК.' in req:
        bot.send_message(call.message.chat.id, f'🤓 Введи строго в формате "число число"! '
                                               f'_Например,_ 5 -9.', parse_mode='Markdown')
        bot.register_next_step_handler(call.message, addition_reverse_code)
    elif 'СЧВАК.ДК.' in req:
        bot.send_message(call.message.chat.id, f'🤓 Введи строго в формате "число число"! '
                                               f'_Например,_ 5 -9.', parse_mode='Markdown')
        bot.register_next_step_handler(call.message, addition_add_code)
    elif 'МУДЧ.' in req:
        bot.send_message(call.message.chat.id, f'_Тема: Методы умножения двоичных чисел._\n\n'
                                               f'В обоих случаях(см. картинку) операция умножения состоит из ряда '
                                               f'последовательных операций сложения частных произведений. '
                                               f'Операциями сложения управляют разряды множителя: '
                                               f'если в каком-то разряде множителя находится единица, '
                                               f'то к сумме частных произведений добавляется множимое с '
                                               f'соответствующим сдвигом; если в разряде множителя — нуль, '
                                               f'то множимое не прибавляется.', parse_mode='Markdown')
        bot.send_photo(call.message.chat.id, 'https://postimg.cc/ykCHgXcD')
    elif ' ' in req:
        bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAENGi9nMQLcDTjwqY2iAy7JqTgctZUdmwAC6B0AAtGuuUt6cjteLOK5ODYE')
        bot.send_message(call.message.chat.id, '🥺 Здесь пока только котик...')
    #страницы
    elif 'pagination' in req[0]:
        json_string = json.loads(req[0])
        count = json_string['CountPage']
        page = json_string['NumberPage']
        #markup = types.InlineKeyboardMarkup()
        if page == 1:
            markup.add(types.InlineKeyboardButton(text=f'Форматы представления чисел в ЭВМ.', callback_data=f'ФПЧ.'))
            markup.add(types.InlineKeyboardButton(text=f'Погрешность представления чисел.', callback_data=f'ППЧ.'))
            markup.add(
                types.InlineKeyboardButton(text=f'Кодирование чисел в ЭВМ.', callback_data=f'Кодирование чисел в ЭВМ.'))
            markup.add(types.InlineKeyboardButton(text=f'Сложение чисел в алгебраических кодах.', callback_data=f'СЧВАК.'))
            markup.add(types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       types.InlineKeyboardButton(text=f'Вперёд --->',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page + 1) + ",\"CountPage\":" + str(count) + "}"))

        elif page == 2:
            markup.add(types.InlineKeyboardButton(text=f'Методы умножения двоичных чисел .', callback_data=f'МУДЧ.'))
            markup.add(types.InlineKeyboardButton(text=f'Умножение двоичных чисел в прямых кодах.', callback_data=f' '))
            markup.add(types.InlineKeyboardButton(text=f'Умножение двоичных чисел в обратных кодах.', callback_data=f' '))
            markup.add(types.InlineKeyboardButton(text=f'Умножение двоичных чисел в дополнительных кодах.', callback_data=f' '))
            markup.add(types.InlineKeyboardButton(text=f'<--- Назад',callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page - 1) + ",\"CountPage\":" + str(count) + "}"),
                       types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       types.InlineKeyboardButton(text=f'Вперёд --->',callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page + 1) + ",\"CountPage\":" + str(count) + "}"))
        elif page == count:
            markup.add(types.InlineKeyboardButton(text=f'Деление двоичных чисел.', callback_data=f' '),
                       types.InlineKeyboardButton(text=f'', callback_data=f' '),
                       types.InlineKeyboardButton(text=f'', callback_data=f' '))
            markup.add(types.InlineKeyboardButton(text=f'<--- Назад',callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page - 1) + ",\"CountPage\":" + str(count) + "}"),
                       types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       types.InlineKeyboardButton(text=f'Вперёд --->',callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page + 1) + ",\"CountPage\":" + str(count) + "}"))
        try:
            bot.edit_message_text(f'Выбери тему из списка:', reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            print("ERROR")

#о боте
@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.from_user.id, f'_Подробнее о разделе:_\n'
                                           f'*Электронно-вычислительная машина (ЭВМ)* — это комплекс '
                                           f'технических, аппаратных и программных средств, предназначенных для '
                                           f'автоматической обработки информации, вычислений, автоматического управления.\n\n'
                                           f'Основным преобразователем цифровой информации являемся арифметико-логическое устройство.\n'
                                           f'*Арифметико-логическое устройство (АЛУ)* — функциональная часть '
                                           f'ЭВМ, которая выполняет логические и арифметические действия, нсобходимые '
                                           f'для переработки информации, хранящейся в памяти. Оно характеризуется'
                                           f' временем выполнения элементарных операций; средним быстродействием'
                                           f' т. е. количеством арифметических или логических действий (операций), '
                                           f'выполняемых в единицу времени (секунду); набором элементарных действий, '
                                           f'которые оно выполняет. Важной характеристикой АЛУ является также '
                                           f'система счисления, в которой осуществляются все действия.\n\n'
                                           f'Основная цель этого бота — знакомство с понятиями информатики, изложение методов'
                                           f' и средств представления информации в компьютерах и информационных '
                                           f'системах, методов реализации арифметических и логических операций в '
                                           f'цифровых автоматах, а также основ анализа и синтеза логических схем ЭВМ '
                                           f'и информационных систем.\n\n'
                                           f'🤓 По оставшимся вопросам и c пожеланиями можно обратиться: @aevaan', parse_mode='Markdown')

#арифметические основы
@bot.message_handler(commands=['arithmetic_topics'])
def list(message):
    count, page = 3, 1
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=f'Форматы представления чисел в ЭВМ.', callback_data=f'ФПЧ.'))
    markup.add(types.InlineKeyboardButton(text=f'Погрешность представления чисел.', callback_data=f'ППЧ.'))
    markup.add(types.InlineKeyboardButton(text=f'Кодирование чисел в ЭВМ.', callback_data=f'Кодирование чисел в ЭВМ.'))
    markup.add(types.InlineKeyboardButton(text=f'Сложение чисел в алгебраических кодах.', callback_data=f'СЧВАК.'))
    markup.add(types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
               types.InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" +
                                                                          str(page + 1) + ",\"CountPage\":" + str(count) + "}"))
    bot.send_message(message.from_user.id, f'Выбери тему из списка:', reply_markup=markup)

#логические основы
@bot.message_handler(commands=['logical_topics'])
def listl(message):
    '''
    count, page = 4, 1
    markup1 = types.InlineKeyboardMarkup()
    markup1.add(types.InlineKeyboardButton(text=f'Форматы представления чисел в ЭВМ.', callback_data=f'ФПЧ.'))
    markup1.add(types.InlineKeyboardButton(text=f'Погрешность представления чисел.', callback_data=f'ППЧ.'))
    markup1.add(types.InlineKeyboardButton(text=f'Кодирование чисел в ЭВМ.', callback_data=f'Кодирование чисел в ЭВМ.'))
    markup1.add(types.InlineKeyboardButton(text=f'Сложение чисел в алгебраических кодах.', callback_data=f'СЧВАК.'))
    markup1.add(types.InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
               types.InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" +
                                                                          str(page + 1) + ",\"CountPage\":" + str(count) + "}"))'''
    bot.send_message(message.from_user.id, f'😶‍🌫 В разработке!')

#прямой, обратный, дополнительный
@bot.message_handler(content_types=['text'])
def translate(message):
    t = message.text
    try:
        if ('.' in t) and (t.count('.') == 1):
            number = ffz(float(t))
        else: number = int(t)
        if type(number) == int and number > 0: dv = bin(number)[2:]
        elif type(number) == int and number < 0: dv = '-' + bin(number)[3:]
        else:
            if number < 0:
                dv = "-" + fbin(number)[0:]
            else: dv = fbin(number)
            print(dv)
        rc = str(reverse_code(number))
        bot.send_message(message.chat.id, f'Десятичная СС: *{number}*\n'
                                          f'Двоичная СС: *{dv}*\n'
                                          f'Прямой код: *{direct_code(number)}*\n'
                                          f'Обратный код: *{reverse_code(number)}*\n'
                                          f'Дополнительный код: *{rc[:2] + additional_code(rc[2::]) if rc[0] == "1" else direct_code(number)}*\n', parse_mode="Markdown")
    except ValueError:
        bot.send_message(message.chat.id, "😵‍💫 Я пока не понимаю! Попробуйте снова.")

if __name__ == '__main__':
    bot.polling(none_stop=True)