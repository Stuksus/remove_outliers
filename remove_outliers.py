#!/usr/bin/env python
# coding: utf-8

# In[1]:


def removing_outliers(column,frame, count = 0,total_outliers = 0, alpha = 1.5):
        """
        Метод удаления выбросов с помощью межквартильного размаха

        Параметры:
        - column: Имя столбца, где нужно найти выбросы
        - frame: Фрейм, где находится столбец для анализа
        - count: Количество рекурсивных циклов проверки 
        - total_outliers: Общая сумма выбросов, найденных за все циклы проверки
        - alpha: Коэфициент при вычислении интервала

        Возвращет:
        - frame: Обработанный фрейм
        - leng: Количесвто выбросов на цикле
        - total_outliers: Общее количество выбросов
        """
        # Получим квантиль 25%
        q25=np.array(frame[column].describe(percentiles=[.25,.75]).loc['25%'])
        # Получим квантиль 75%
        q75=np.array(frame[column].describe(percentiles=[.25,.75]).loc['75%'])
        # Получим первую границу
        first_part=q25-alpha*(q75-q25)
        # Получим 2 границу
        second_part=q75+alpha*(q75-q25)
        # Инициализируем список для индексов, подготовленных к удалению
        index_del= []
        # Получим все значения, удолитворяющих промежутку
        prep_frame = frame[(frame[column] > first_part) & (frame[column] < second_part)]
        # Подсчет количсва удаленных выбросов
        leng = frame.shape[0] - prep_frame.shape[0]
        # Увеление счетчика циклов
        count += 1
        # Заменим исходную таблицу обработанной
        frame = prep_frame.copy()
        # Удалим не нужную таблицу
        del prep_frame
        # Проверим условия выхода
        if leng > 0 and count <= 5:
            frame,leng,total_outliers = removing_outliers(column,frame, count,total_outliers+leng)
        else:
            print('Количество строк, выбранных для удаления {}: {}. Количество итераций {}'.format(column,total_outliers,count),end = "\n\n")
        return frame,leng,total_outliers

