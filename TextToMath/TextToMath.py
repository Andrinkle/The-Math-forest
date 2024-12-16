import spacy

class NumberConverter:
    numbers = {
        "ноль": 0, "нуль": 0, "нулю": 0, "один": 1, "одна": 1, "два": 2, "две": 2, "три": 3, "четыре": 4, "пять": 5,
        "шесть": 6, "семь": 7, "восемь": 8, "девять": 9, "десять": 10,
        "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13, "четырнадцать": 14, "пятнадцать": 15,
        "шестнадцать": 16, "семнадцать": 17, "восемнадцать": 18, "девятнадцать": 19, "двадцать": 20,
        "тридцать": 30, "сорок": 40, "пятьдесят": 50, "шестьдесят": 60,
        "семьдесят": 70, "восемьдесят": 80, "девяносто": 90, "сто": 100,
        "двести": 200, "триста": 300, "четыреста": 400, "пятьсот": 500,
        "шестьсот": 600, "семьсот": 700, "восемьсот": 800, "девятьсот": 900,
        "тысяча": 1000, "тысяч": 1000, "миллион": 1000000, "миллиона": 1000000
    }

    @classmethod
    def words_to_number(cls, tokens):
        total = 0
        current = 0
        last_value = 0
        for token in tokens:
            value = cls.numbers.get(token.lemma_, None)
            if value is not None:
                if value >= 1000:
                    current = (current if current else 1) * value
                    total += current
                    current = 0
                elif value >= 100:
                    current += value
                elif value < 100:
                    if last_value >= 100 and value <= 9:
                        current += value
                    else:
                        current += value
                last_value = value
        total += current
        return str(total)

class MathE:
    @staticmethod
    def format_exponent(e_expression):
        if isinstance(e_expression, int):  # Если входное выражение - это просто степень
            return f'exp({e_expression})'
        elif e_expression == 'e':  # Если входное выражение - просто e
            return 'exp(1)'
        else:  # Обрабатываем случай e ** k
            return f'exp({e_expression})'

class TextToMath:
    math_operators = {
        "сложить": "+", "плюс": "+", "прибавить": "+", "вычесть": "-", "минус": "-",
        "умножить": "*", "разделить": "/", "делить": "/", "равный": "=", "далее": "|",
        "больше": ">", "меньше": "<", "больше или равно": ">=", "меньше или равно": "<="
    }
    math_functions = {
        "синус": "sin", "косинус": "cos", "тангенс": "tg", "котангенс": "ctg"
    }

    def __init__(self, nlp_model):
        self.nlp = nlp_model

    def convert_text_to_expression(self, text):
        # Проверка на формат "Система {A} далее {B}"
        if text.startswith("Система") and "далее" in text:
            parts = text.replace("Система", "").split("далее")
            expression_a = self._convert_individual_expression(parts[0].strip())
            expression_b = self._convert_individual_expression(parts[1].strip())
            return f"{expression_a} | {expression_b}"
        
        # Обычная обработка
        return self._convert_individual_expression(text)

    def _convert_individual_expression(self, text):
        doc = self.nlp(text)
        result = ""
        i = 0

        while i < len(doc):
            token = doc[i]
            
            # Обработка чисел
            if token.lemma_ in NumberConverter.numbers:
                number_tokens = [token]
                j = i + 1
                while j < len(doc) and doc[j].lemma_ in NumberConverter.numbers:
                    number_tokens.append(doc[j])
                    j += 1
                number_str = NumberConverter.words_to_number(number_tokens)
                
                if j < len(doc) and doc[j].lemma_ in ["икс", "игрек"]:
                    variable = "x" if doc[j].lemma_ == "икс" else "y"
                    result += f"{number_str}*{variable}"
                    i = j  
                else:
                    result += number_str
                i = j - 1
            
            # Обработка операторов
            elif token.lemma_ in self.math_operators:
                if token.lemma_ in ["больше", "меньше"] and i + 2 < len(doc) and doc[i + 1].lemma_ == "или" and doc[i + 2].lemma_ == "равно":
                    result += self.math_operators[token.lemma_ + " или равно"]
                    i += 2  
                elif token.lemma_ == "умножить" and i + 1 < len(doc) and doc[i + 1].text == "на":
                    result += "*"
                    i += 1  
                elif token.lemma_ == "разделить" and i + 1 < len(doc) and doc[i + 1].text == "на":
                    result += "/"
                    i += 1  
                else:
                    result += self.math_operators[token.lemma_]

            # Обработка математических функций
            elif token.lemma_ in self.math_functions:
                function = self.math_functions[token.lemma_]
                if i + 1 < len(doc) and (doc[i + 1].lemma_ in NumberConverter.numbers or doc[i + 1].lemma_ in ["икс", "игрек"]):
                    if doc[i + 1].lemma_ in NumberConverter.numbers:
                        number_tokens = [doc[i + 1]]
                        j = i + 2
                        while j < len(doc) and doc[j].lemma_ in NumberConverter.numbers:
                            number_tokens.append(doc[j])
                            j += 1
                        argument = NumberConverter.words_to_number(number_tokens)
                        result += f"{function}({argument})"
                        i = j - 1
                    else:
                        variable = "x" if doc[i + 1].lemma_ == "икс" else "y"
                        result += f"{function}({variable})"
                        i += 1
                else:
                    result += function

            # Обработка переменных и специальных символов
            elif token.lemma_ == "пи":
                result += "pi"
            elif token.lemma_ in ["е", "число Эйлера"]:
                if i + 2 < len(doc) and doc[i + 1].lemma_ == "в" and doc[i + 2].lemma_ == "степень":
                    exponent_tokens = []
                    j = i + 3
                    while j < len(doc) and doc[j].lemma_ in NumberConverter.numbers:
                        exponent_tokens.append(doc[j])
                        j += 1
                    exponent = NumberConverter.words_to_number(exponent_tokens)
                    result += MathE.format_exponent(exponent)
                    i = j - 1
                else:
                    result += MathE.format_exponent('e')
            elif token.lemma_ == "в" and i + 1 < len(doc) and doc[i + 1].lemma_ == "степень":
                i += 2
                exponent_tokens = []
                while i < len(doc) and doc[i].lemma_ in NumberConverter.numbers:
                    exponent_tokens.append(doc[i])
                    i += 1
                exponent = NumberConverter.words_to_number(exponent_tokens)
                result += f"**{exponent}"
                i -= 1
            elif token.lemma_ == "икс" and not result.endswith("x"):
                result += "x"
            elif token.lemma_ == "игрек" and not result.endswith("y"):
                result += "y"
            elif token.lemma_ == "открыть" and i + 1 < len(doc) and doc[i + 1].lemma_ == "скобка":
                result += "("
                i += 1
            elif token.lemma_ == "закрыть" and i + 1 < len(doc) and doc[i + 1].lemma_ == "скобка":
                result += ")"
                i += 1

            i += 1

        return result

# Инициализируем spacy и конвертер
nlp = spacy.load("ru_core_news_sm")
converter = TextToMath(nlp)

# Пример использования
# text = "Косинус открыть скобку пи умножить икс закрыть скобку плюс два в степени пятьсот восемьдесят два далее е в степени два делить на пять"
text = "икс в степени пи"
result = converter.convert_text_to_expression(text)
print("Result:", result)

