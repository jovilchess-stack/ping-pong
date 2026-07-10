import curses
import time

def juego(stdscr):
    # --- Configuración de la Terminal ---
    curses.curs_set(0)          # Ocultar el cursor físico
    stdscr.nodelay(1)           # Entrada no bloqueante
    stdscr.keypad(True)         # Soporte para capturar caracteres del teclado
    
    # --- Dimensiones Fijas ---
    ALTO, ANCHO = 20, 60
    PUNTOS_VICTORIA = 5
    
    # --- Variables de Estado ---
    paleta_a = ALTO // 2
    paleta_b = ALTO // 2
    pelota_x, pelota_y = ANCHO // 2, ALTO // 2
    dir_x, dir_y = 1, 1
    puntos_a = 0
    puntos_b = 0
    
    # --- Control de Tiempos (Sistema de Reloj) ---
    ultimo_movimiento_pelota = time.time()
    intervalo_pelota = 0.08  # Controla la velocidad de la pelota
    
    while True:
        stdscr.clear()
        tiempo_actual = time.time()
        
        # --- Verificar Condición de Victoria ---
        if puntos_a >= PUNTOS_VICTORIA or puntos_b >= PUNTOS_VICTORIA:
            ganador = "JUGADOR A" if puntos_a >= PUNTOS_VICTORIA else "JUGADOR B"
            stdscr.addstr(ALTO // 2 - 1, ANCHO // 2 - 10, "¡FIN DEL JUEGO!", curses.A_BOLD)
            stdscr.addstr(ALTO // 2, ANCHO // 2 - len(ganador) // 2 - 4, f"Ganador: {ganador}")
            stdscr.addstr(ALTO // 2 + 2, ANCHO // 2 - 14, "Presiona 'q' para salir...")
            stdscr.nodelay(0)
            while True:
                if stdscr.getch() == ord('q'):
                    return

        # --- Dibujar Bordes Superior e Inferior ---
        for x in range(ANCHO):
            stdscr.addch(0, x, '#')
            stdscr.addch(ALTO - 1, x, '#')
            
        # --- Dibujar Línea Central ---
        for y in range(1, ALTO - 1):
            if y % 2 == 0:
                stdscr.addch(y, ANCHO // 2, ':')

        # --- Dibujar Marcador ---
        stdscr.addstr(1, ANCHO // 4 - 5, f"Jugador A: {puntos_a}", curses.A_BOLD)
        stdscr.addstr(1, (ANCHO // 4) * 3 - 6, f"Jugador B: {puntos_b}", curses.A_BOLD)

        # --- Dibujar Paleta Izquierda (Jugador A) ---
        for i in range(-2, 3):
            if 0 < paleta_a + i < ALTO - 1:
                stdscr.addch(paleta_a + i, 2, '|')

        # --- Dibujar Paleta Derecha (Jugador B) ---
        for i in range(-2, 3):
            if 0 < paleta_b + i < ALTO - 1:
                stdscr.addch(paleta_b + i, ANCHO - 3, '|')

        # --- Dibujar Pelota ---
        if 0 < pelota_y < ALTO - 1 and 0 < pelota_x < ANCHO:
            stdscr.addch(int(pelota_y), int(pelota_x), 'O', curses.A_BOLD)

        stdscr.refresh()
        
        # --- Captura de Controles para Ambos Jugadores ---
        tecla = stdscr.getch()
        if tecla == ord('q'):
            break
            
        # Controles Jugador A (W / S) - Minúsculas y Mayúsculas
        if tecla in (ord('w'), ord('W')) and paleta_a > 3:
            paleta_a -= 1
        elif tecla in (ord('s'), ord('S')) and paleta_a < ALTO - 4:
            paleta_a += 1
            
        # Controles Jugador B (I / K) - Minúsculas y Mayúsculas
        elif tecla in (ord('i'), ord('I')) and paleta_b > 3:
            paleta_b -= 1
        elif tecla in (ord('k'), ord('K')) and paleta_b < ALTO - 4:
            paleta_b += 1

        # --- Lógica Independiente de la Pelota ---
        if tiempo_actual - ultimo_movimiento_pelota >= intervalo_pelota:
            ultimo_movimiento_pelota = tiempo_actual
            
            # Movimiento de la pelota
            pelota_x += dir_x
            pelota_y += dir_y

            # Rebote en techo y suelo
            if pelota_y <= 1 or pelota_y >= ALTO - 2:
                dir_y *= -1

            # Colisión con Paleta Izquierda (Jugador A)
            if pelota_x == 3 and (paleta_a - 2 <= pelota_y <= paleta_a + 2):
                dir_x *= -1
                intervalo_pelota = max(0.03, intervalo_pelota - 0.004)

            # Colisión con Paleta Derecha (Jugador B)
            if pelota_x == ANCHO - 4 and (paleta_b - 2 <= pelota_y <= paleta_b + 2):
                dir_x *= -1
                intervalo_pelota = max(0.03, intervalo_pelota - 0.004)

            # --- Sistema de Puntuación ---
            # Punto para Jugador B
            if pelota_x <= 0:
                puntos_b += 1
                pelota_x, pelota_y = ANCHO // 2, ALTO // 2
                dir_x = 1
                intervalo_pelota = 0.08
                stdscr.refresh()
                time.sleep(0.6)
                ultimo_movimiento_pelota = time.time()

            # Punto para Jugador A
            if pelota_x >= ANCHO - 1:
                puntos_a += 1
                pelota_x, pelota_y = ANCHO // 2, ALTO // 2
                dir_x = -1
                intervalo_pelota = 0.08
                stdscr.refresh()
                time.sleep(0.6)
                ultimo_movimiento_pelota = time.time()

        # Pequeña pausa para estabilizar los FPS
        time.sleep(0.016)

curses.wrapper(juego)
