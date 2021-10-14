import os
from concurrent.futures import ProcessPoolExecutor


from tqdm import tqdm
import pandas as pd
import numpy as np


class check_nan_decorator(object):
    def __init__(self, target):
        self.target = target
        try:
            functools.update_wrapper(self, target)
        except:
            pass

    def __call__(self, content):
        if pd.isna(content):
            return content
        
        return self.target(content)
    
    
class ParallelPreprocessing:
    def __init__(self, data: pd.DataFrame, max_workers: int=8, make_copy=False) -> None:
        self.data = data.copy() if make_copy else data
        self.max_workers = max_workers
        
    def run_series_function(self, col_name:str, func, inplace=False, paralleling=True):
        """
        Args:
            col_name: название колонки, над которыми будет происходить операции
            func: функция, принимающая значение колонок и выполняющая с ними различные операции
            
        Returns:
            Список кортежей, первый элемент это индекс элемента(начинается всего с 0 и идет с шагом 1),
            а второе - преобразованные заданной функцией элементы
        """
    
        results = []
        
        if paralleling:
            results = self._solve_paralleling(col_name, func)
        else:
            decorated_func = check_nan_decorator(func)
            
            results = self.data[col_name].map(func)
            
        results = np.array(results)
        
        if not inplace:
            return results
        
        new_values = results
        self.data[col_name] = new_values
        
    
    def _solve_paralleling(self, col_name, func):
        result = []
        
        new_func = check_nan_decorator(func)
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            result = executor.map(new_func, self.data[col_name].to_list())
        
        return list(result)
    
    def change_data(self, data):
        self.data = data
        
    def get_data(self, data):
        return self.data
    
    @staticmethod
    def run_on_list_function(l, func):
        p = ParallelPreprocessing(
            df.DataFrame(l, columns='content'),
            max_workers=4,
            make_copy=False,
        )
        
        res = p.run_series_function('content', func)
        
        return res