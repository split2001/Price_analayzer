import os
import json
from os import getcwd
import csv



class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path='.'):
        for filename in os.listdir(file_path):  # либо с помощью getcwd() получаем текущую директорию
            if filename.startswith('price'): # проверка на наличие слова price названии файла
                # print('filename found', filename)
                path = os.path.join(file_path, filename)
                with open (path ,'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=',')  # указываем параметр delimiter(разделитель)
                    headers = next(reader)  # метод next извлекает первую строку из csv файла
                    product_col, price_col, weight_col = self._search_product_price_weight(headers)  # получаем индексы нужных столбцов
                    # print('заголовки столбцов', headers)

                    if product_col is not None and price_col is not None and weight_col is not None:
                        for row in reader:
                            name = row[product_col].strip() # привязываем данные из строки к индексу столбца
                            price = float(row[price_col].strip())
                            weight = float(row[weight_col].strip())
                            price_per_kg = price / weight

                            self.data.append({
                                'Наименование': name,
                                'Цена': price,
                                'Вес': weight,
                                'Файл': filename,
                                'Цена за кг': price_per_kg
                            })


        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''

    def _search_product_price_weight(self, headers):
        """
                 Возвращает номера столбцов
               """

        # возможные варианты заголовков
        product_column = ['товар', 'название', 'наименование', 'продукт']
        price_column = ['розница', 'цена']
        weight_column = ['вес', 'масса', 'фасовка']

        product_col  = None
        price_col = None
        weight_col  = None


        for index, header in enumerate(headers):
            if  header.lower() in product_column:
                product_col = index
            elif  header.lower() in price_column:
                price_col = index
            elif header.lower() in weight_column:
                weight_col = index
        return product_col, price_col,  weight_col



    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>№</th>
                    <th>Наименование</th>
                    <th>Цена</th>
                    <th>Вес</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for number, item in enumerate(sorted(self.data, key=lambda x: x['Цена за кг'])):
            result += '<tr>'
            result += f'<td>{number + 1}</td>'
            result += f'<td>{item["Наименование"]}</td>'
            result += f'<td>{item["Цена"]}</td>'
            result += f'<td>{item["Вес"]}</td>'
            result += f'<td>{item["Файл"]}</td>'
            result += f'<td>{item["Цена за кг"]}</td>'
            result += '</tr>'

        result += '''
                    </table>
                </body>
                </html>
                '''

        with open (fname, 'w', encoding='utf-8') as file:
            file.write(result)


    def find_text(self, text):
        results = [product for product in self.data if text.lower() in product['Наименование'].lower()]
        sorted_results = sorted(results, key=lambda x: x['Цена за кг'])

        for i, product in enumerate(sorted_results, 1):
            print(
                f"{i} | {product['Наименование']} | {product['Цена']} | {product['Вес']} | {product['Файл']} | {product['Цена за кг']}")

'''
    Логика работы программы
'''

if __name__ == "__main__":
    pm = PriceMachine()
    pm.load_prices()
    pm.export_to_html()


    while True:
        text = input("Введите текст для поиска (или 'exit' для выхода): ")
        if text.lower() == 'exit':
            print('Программа завершена.')
            pm.export_to_html()
            break

        pm.find_text(text)



