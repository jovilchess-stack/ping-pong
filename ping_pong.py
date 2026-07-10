import curses
import time

def juego(stdscr):
    # Configurar terminal
    curses.curs_set(0)
    stdscr.nodelay(1)
    
    # Dimensiones fijas del juego
    ALTO, ANCHO = 20, 60
    PUNTOS_VICTORIA = 5
    
    # Variables de estado
    paleta_a = ALTO // 2
    paleta_b = ALTO // 2
    pelota_x, pelota_y = ANCHO // 2, ALTO // 2
    dir_x, dir_y = 1, 1
    
    puntos_a = 0
    puntos_b = 0
    
    # Control de velocidad (menor número = más rápido)
    velocidad_base = 0.07
    velocidad_actual = velocidad_base

    while True:
        stdscr.clear()
        
        # --- Verificar Condición de Victoria ---
        if puntos_a >= PUNTOS_VICTORIA or puntos_b >= PUNTOS_VICTORIA:
            ganador = "JUGADOR A" if puntos_a >= PUNTOS_VICTORIA else "COMPUTADORA (B)"
            stdscr.addstr(ALTO // 2 - 1, ANCHO // 2 - 10, "¡FIN DEL JUEGO!", curses.A_BOLD)
            stdscr.addstr(ALTO // 2, ANCHO // 2 - len(ganador) // 2 - 4, f"Ganador: {ganador}")
            stdscr.addstr(ALTO // 2 + 2, ANCHO // 2 - 14, "Presiona 'q' para salir...")
            stdscr.nodelay(0)
            while True:
                if stdscr.getch() == ord('q'):
                    return
        
        # --- Dibujar Bordes ---
        for x in range(ANCHO):
            stdscr.addch(0, x, '#')
            stdscr.addch(ALTO - 1, x, '#')
        
        # --- Dibujar Marcador ---
        stdscr.addstr(1, ANCHO // 4 - 5, f"Jugador A: {puntos_a}")
        stdscr.addstr(1, (ANCHO // 4) * 3 - 7, f"Bot B (IA): {puntos_b}")

        # --- Dibujar Paletas ---
        # Izquierda (Jugador A)
        for i in range(-2, 3):
            if 0 < paleta_a + i < ALTO - 1:
                stdscr.addch(paleta_a + i, 2, '|')

        # Derecha (Bot B)
        for i in range(-2, 3):
            if 0 < paleta_b + i < ALTO - 1:
                stdscr.addch(paleta_b + i, ANCHO - 3, '|')

        # --- Dibujar Pelota ---
        if 0 < pelota_y < ALTO - 1 and 0 < pelota_x < ANCHO:
            stdscr.addch(pelota_y, pelota_x, 'O')

        stdscr.refresh()
        time.sleep(velocidad_actual)

        # --- Controles del Jugador A ---
        tecla = stdscr.getch()
        if tecla == ord('q'):
            break
        elif tecla == ord('w') and paleta_a > 3:
            paleta_a -= 1
        elif tecla == ord('s') and paleta_a < ALTO - 4:
            paleta_a += 1

        # --- Inteligencia Artificial (Bot B) ---
        # El bot sigue el eje Y de la pelota con un leve retraso para que sea ganable
        if pelota_x > ANCHO // 3:  # Solo reacciona si la pelota pasa un tercio del mapa
            if pelota_y < paleta_b and paleta_b > 3:
                paleta_b -= 1
            elif pelota_y > paleta_b and paleta_b < ALTO - 4:
                paleta_b += 1

        # --- Física y Movimiento ---
        pelota_x += dir_x
        pelota_y += dir_y

        # Rebote techo/suelo
        if pelota_y <= 1 or pelota_y >= ALTO - 2:
            dir_y *= -1

        # Colisión Paleta Izquierda (Aumenta velocidad al golpear)
        if pelota_x == 3 and (paleta_a - 2 <= pelota_y <= paleta_a + 2):
            dir_x *= -1
            velocidad_actual = max(0.02, velocidad_actual - 0.005)
        
        # Colisión Paleta Derecha (Aumenta velocidad al golpear)
        if pelota_x == ANCHO - 4 and (paleta_b - 2 <= pelota_y <= paleta_b + 2):
            dir_x *= -1
            velocidad_actual = max(0.02, velocidad_actual - 0.005)

        # --- Sistema de Puntuación y Reinicio ---
        # Punto para B
        if pelota_x <= 0:
            puntos_b += 1
            pelota_x, pelota_y = ANCHO // 2, ALTO // 2
            dir_x = 1  # Saca el jugador A
            velocidad_actual = velocidad_base  # Reiniciar velocidad
            time.sleep(1)

        # Punto para A
        if pelota_x >= ANCHO - 1:
            puntos_a += 1
            pelota_x, pelota_y = ANCHO // 2, ALTO // 2
            dir_x = -1  # Saca el bot
            velocidad_actual = velocidad_base  # Reiniciar velocidad
            time.sleep(1)

# Arrancar juego
curses.wrapper(juego)
