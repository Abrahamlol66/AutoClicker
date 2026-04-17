# AutoClicker Pro Ultra

Un autoclicker avanzado desarrollado en Python con soporte para múltiples modos de click y atajos de teclado personalizables.

## Características

- **Modo Autoclick:** Realiza clicks repetitivos a una velocidad configurable (CPS).
- **Modo Click Mantenido:** Mantiene el botón del mouse presionado de forma automática hasta que se desactive.
- **Botón Personalizable:** Puedes elegir entre el botón izquierdo o derecho del mouse.
- **Atajos de Teclado:** Configura tus propias teclas para activar o desactivar cada función sin necesidad de abrir la ventana.
- **Interfaz Intuitiva:** Interfaz gráfica sencilla con registro de actividad en tiempo real.

## Descarga y Ejecución

Puedes encontrar el ejecutable en la carpeta `dist/autoclicker.exe`. 

- **Ejecutable Independiente:** El archivo `.exe` es **one-file**, lo que significa que contiene todas las librerías necesarias. Puedes moverlo a cualquier carpeta o enviarlo a otra persona y funcionará sin necesidad de instalar Python o las librerías mencionadas.
- **Permisos de Administrador:** El programa solicitará permisos de administrador al abrirse para poder interactuar correctamente con otras ventanas y juegos.

## Requisitos (Solo para desarrolladores)

Para ejecutar este programa, necesitas tener Python instalado y las siguientes librerías:

```bash
pip install pynput
```

## Instrucciones de Uso

1. **Configuración de Velocidad:** Ingresa el número de clicks por segundo (CPS) deseado (Máximo 100).
2. **Selección de Botón:** Elige si deseas simular el click izquierdo o derecho.
3. **Configuración de Atajos:** 
   - Haz click en el botón del atajo actual (por defecto F6 para Autoclick y F7 para Click Mantenido).
   - Presiona la nueva tecla que deseas asignar.
4. **Activación:**
   - Usa los botones **INICIAR AUTOCLICK** o **MANTENER CLICK** en la interfaz.
   - O utiliza las teclas de acceso rápido configuradas.

## Notas de Seguridad

- El límite de 100 CPS está implementado para prevenir bloqueos accidentales del sistema.
- El programa detecta automáticamente si una función ya está activa antes de iniciar otra para evitar conflictos.
