# The Lagrange interpolation polynomial #

Построение графика [интерполяционного многочлена Лагранжа](https://ru.wikipedia.org/wiki/%D0%98%D0%BD%D1%82%D0%B5%D1%80%D0%BF%D0%BE%D0%BB%D1%8F%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B9_%D0%BC%D0%BD%D0%BE%D0%B3%D0%BE%D1%87%D0%BB%D0%B5%D0%BD_%D0%9B%D0%B0%D0%B3%D1%80%D0%B0%D0%BD%D0%B6%D0%B0) по 5 точкам реализовано с помощью `python` и библиотек `numpy` и `matplotlib`.

### Интерполяционный многочлен Лагранжа ###

Пусть задана <img src="https://render.githubusercontent.com/render/math?math=n+1"> пара чисел <img src="https://render.githubusercontent.com/render/math?math=(x_0, y_0), (x_1, y_1), ... , (x_n, y_n)">, где все <img src="https://render.githubusercontent.com/render/math?math=x_j"> различны.

<img src="https://render.githubusercontent.com/render/math?math=L(x)\displaystyle\sum_{i=0}^{n} y_il_i(x)">, где

базисные полиномы <img src="https://render.githubusercontent.com/render/math?math=l_i"> определяются по формуле:

<img src="https://render.githubusercontent.com/render/math?math=l_i(x) =\displaystyle\prod_{j=0, j \neq i}^n \frac{x-x_j}{x_i-x_j}">

## Зависимости ##
Необходимо поставить библиотеки `numpy` и `matplotlib`:
### Arch Linux ###
```
sudo pacman -S python-numpy python-matplotlib
```
## Пример ##
```
python main.py
```

![alt text](pictures/graph.png)