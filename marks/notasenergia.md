## Elementos importantes en la función de energía de Yump

### Decisión de extremos inferior y superior

Cualquier valor de la energía debe estar contenido en un par de valores que representen algo valioso en términos del cumplimiento del programa de Yump.
En este caso se decidió que el valor de la energía mínimo sería 20 y el máximo 120.

Al mínimo se puede llegar simplemente ignorando la plataforma de forma sistemática. Al máximo solo se puede llegar con un cumplimiento perfecto del programa. Al 100, sin embargo, se puede llegar por diversos caminos, lo cual es importante para no caer en el error de que para llegar al 100 solo hay un posible camino.

### Qué elementos influyen negativa o positivamente

**Cumplir el programa en fecha otorga bonus**: 3 puntos por mission ejecutada en fecha.

**Cumplir el programa fuera de fecha otorga bonus**: 3 puntos por mision ejecutada fuera de fecha.

Ambos criterios tienen un máximo de bonificación en todo caso de 30 puntos.

**No cumplir los programas otorga penalización**: -3 puntos por misión sin ejecutar (atendiendo al calendario)

Este criterior tiene un máximo de penalización en todo caso de -30 puntos.

**Introducir elementos personales otorga bonus**: 2 puntos por elemento personal usado.

Este criterio tiene un máximo de bonificación de 10 puntos.

**Repetir dinámicas otorgra bonus**: una cantidad de puntos calculada en función del número de repeticiones ejecutadas en los últimos días.

Este criterio tiene un máximo de bonificación de 20 puntos.

### Cuándo se calcula el valor actualizado de la energía

En el caso de Yump, se valoró que ese cálculo se hiciera en el momento de realizar login en la plataforma. Ese cálculo permitiría tener el valor antiguo y el nuevo y poder presentar un cambio en la barra de energía del usuario.
Si fueran a enviarse notificaciones al usuario en otro momento, el cálculo debería hacerse también durante el logout.

### Cómo influye la evolución del programa en el tiempo

En Yump no era lo mismo el primer día que la segunda semana que el final del programa. Se querían reflejar aspectos como lo fácil que podría ser arrancar con fuerza o sentir mayor dificultad en algún momento del programa.
Para ello se creó una función normalizadora que empleaba una simple función escalar. 
Esta función escalar representaba un valor porcentual para cada día del calendario del programa.
Si queríamos mostrar progreso fácil al comienzo, incluso más del teórico, esa función escalar tenía un valor superior a 100. En momentos del programa en donde consideraba Yump que había que hacer un esfuerzo adicional, esa función escalar tendría un valor más cercano a 80.

Esta función escalar rara vez podría otorgar mayor valor que el teórico de 120 pero es posible que pudiera hacer descender el nivel de energía por debajo de 20 en algún momento.

Esta función escalar no está personalizada por persona pero podría hacerse y podría considerarse un nivel de dificultad personalizado.

