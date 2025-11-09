# CC3501-FloppyBird
# Flappy Bird - Tarea 2 Gráfica

Implementación simplificada del juego Flappy Bird usando Python, Pyglet y OpenGL.
Desarrollado como Tarea 2 del curso de Computación Gráfica

## Descripción

Juego donde controlas un pájarito que debe esquivar tuberías mientras vuela. El juego aumenta su dificultad progresivamente con la velocidad de las tuberías.

## Requisitos

- Python 3.8+
- Pyglet
- NumPy
- OpenGL
- PIL (Pillow)

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/tarea2-grafica.git
cd Tarea2Grafica/Tarea2
```

### 2. Instalar dependencias
```bash
pip install pyglet numpy pillow PyOpenGL
```

### 3. Ejecutar el juego
```bash
python template.py
```

## Controles

- **ESPACIO**: Iniciar juego / Impulsar al pájaro hacia arriba / Reiniciar después de Game Over

## Características

- Física de gravedad 
- Fondo en movimiento continuo
- Música de fondo 
- Tuberías con alturas aleatorias
- Dificultad progresiva (las tuberías aceleran)
- Detección de colisiones
- Sistema de reciclaje de tuberías

## Cómo Se Juega

1. **Pantalla de inicio**: Presiona ESPACIO para comenzar
2. **Durante el juego**: 
   - Presiona ESPACIO para hacer que el pájaro suba
   - Evita chocar con las tuberías
   - Evita tocar el suelo o el techo
3. **Game Over**: Presiona ESPACIO para reiniciar

## Mecánicas del Juego

### Colisiones
El juego detecta tres tipos de colisiones:
1. Pájaro contra tubería superior
2. Pájaro contra tubería inferior  
3. Pájaro contra límites (suelo/techo)

### Sistema de Tuberías
- **Cantidad**: 5 tuberías activas
- **Reciclaje**: Cuando una tubería sale de pantalla, se reposiciona a la derecha con altura aleatoria

## Decisiones de Diseño

1. **Scene Graph**: Uso de grafo de escena para organizar objetos jerárquicamente
2. **Reciclaje de objetos**: Las tuberías se reciclan en lugar de crearse o destruirse
4. **Shaders**: Implementación con GLSL 330 para renderizado eficiente
5. **Easter egg**: Música sorpresa al iniciar el juego

## Tecnologías Utilizadas

- **Pyglet**: Framework para gráficos y ventanas
- **OpenGL**: Renderizado 3D/2D
- **NumPy**: Operaciones matemáticas y matrices
- **PIL/Pillow**: Manejo de texturas
- **GLSL**: Shaders de vértices y fragmentos

