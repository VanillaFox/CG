# Bezier surface #

Генерация и рендер поверхности Безье с диффузным и бликовым освещением. Реализован с помощью ```C++``` и ```OpenGL```, математика была сделана посредством библиотеки ```glm```.

### Уравнение поверхности Безье ###

[Поверхность Безье](https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%B2%D0%B5%D1%80%D1%85%D0%BD%D0%BE%D1%81%D1%82%D1%8C_%D0%91%D0%B5%D0%B7%D1%8C%D0%B5) порядка $(n, m)$ задается $(n+1)\cdot(m+1)$ контрольными точками $P_{i,j}$.

$p(u, v) = \sum_{i=0}^{n} \sum_{j=0}^{m} B^{n}_{i}(u) B^{m}_{j}(v)P_{i,j}$, где 

$u, v \in (0, 1)$, а $B$ - многочлен Бернштейна:

$B^{n}_{i}(u) = \binom{n}{i} u^{i} (1-u)^{n-i} = \frac{n!}{i!(n-i)!} u^{i} (1-u)^{n-i}$

Генерация поверхности происходит на основе контрольных точек, указанных в figures/coords.txt.

## Аргументы при запуске ## 
```
./cw <flags>
```

## Флаги ##

+ ```-wframe``` - включение каркасной отрисовки;
+ ```-step n``` - установка значения отступа между точками поверхности  $[0 < n < 0.5]$;
+ ```-n n``` - установка порядка n поверхности Безье;
+ ```-m n``` - установка порядка m поверхности Безье.

## Пример ##
```
./cw  -step 0.05 -wframe
```

![alt text](pictures/bicubic.gif)


## Зависимости ##
Перед запуском программы необходимо установить библиотеки ```glfw-x11``` и ```glew```:

### Arch Linux ###

```
sudo pacman -S glfw-x11 glew
```

Также [скачать](https://glm.g-truc.net/0.9.9/index.html) ```glm```, после чего необходимо ее расположить в папку проекта.