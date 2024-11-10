

def addition(n1, n2, code):
  try:
    sign1, num1 = n1.split('|')
    sign2, num2 = n2.split('|')
  except:
    sign1, num1 = n1.split('.')
    sign2, num2 = n2.split('.')

  # Определяем, какое число короче
  shorter_num = num2 if len(num1) > len(num2) else num1
  longer_num = num1 if len(num1) > len(num2) else num2

  # Добавляем к короткому числу
  if code == "d":
    shorter_num = shorter_num.zfill(len(longer_num))
  else:
    shorter_num = (len(longer_num) - len(shorter_num)) * "1" + shorter_num
  print(shorter_num)

  # Складываем числа по битам
  result = []
  carry = 0
  for i in range(len(longer_num) - 1, -1, -1):
    bit1 = int(longer_num[i])
    bit2 = int(shorter_num[i])
    sum_bit = bit1 + bit2 + carry
    result.append(str(sum_bit % 2)) # Остаток от деления на 2 - это бит
    carry = sum_bit // 2       # Целая часть от деления - это перенос

  # Добавляем знак и первые два символа
  result = "".join(result[::-1])
  result = sign2 + "|" + result[0:2] + result[2:]
  return result
