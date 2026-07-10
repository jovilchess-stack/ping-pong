import curses
import time

def juego(stdscr):
    # --- Configuración de la Terminal ---
    curses.curs_set(0)          # Ocultar el cursor físico
    stdscr.nodelay(1)           # Entrada no bloqueante (no detiene el juego esperando una tecla)
    stdscr.keypad(True)         # Habilitar soporte para flechas del teclado y combinaciones
    
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
    intervalo_pelota = 0.08  # Controla la velocidad de la pelota de forma independiente
    
    while True:
        stdscr.clear()
        tiempo_actual = time.time()
        
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

        # --- Dibujar Bordes Superior e Inferior ---
        for x in range(ANCHO):
            stdscr.addch(0, x, '#')
            stdscr.addch(ALTO - 1, x, '#')
            
        # --- Dibujar Línea Central (Mejora visual) ---
        for y in range(1, ALTO - 1):
            if y % 2 == 0:
                stdscr.addch(y, ANCHO // 2, ':')

        # --- Dibujar Marcador ---
        stdscr.addstr(1, ANCHO // 4 - 5, f"Jugador A: {puntos_a}", curses.A_BOLD)
        stdscr.addstr(1, (ANCHO // 4) * 3 - 7, f"Bot B (IA): {puntos_b}", curses.A_BOLD)

        # --- Dibujar Paleta Izquierda (Jugador A) ---
        for i in range(-2, 3):
            if 0 < paleta_a + i < ALTO - 1:
                stdscr.addch(paleta_a + i, 2, '|')

        # --- Dibujar Paleta Derecha (Bot B) ---
        for i in range(-2, 3):
            if 0 < paleta_b + i < ALTO - 1:
                stdscr.addch(paleta_b + i, ANCHO - 3, '|')

        # --- Dibujar Pelota ---
        if 0 < pelota_y < ALTO - 1 and 0 < pelota_x < ANCHO:
            stdscr.addch(int(pelota_y), int(pelota_x), 'O', curses.A_BOLD)

        stdscr.refresh()
        
        # --- Captura de Controles Ultra-Sensible (Sin retraso) ---
        tecla = stdscr.getch()
        if tecla == ord('q'):
            break
        # Soporte para W/S y Flechas (Arriba/Abajo) para máxima comodidad
        elif tecla in (ord('w'), ord('W'), curses.KEY_UP) and paleta_a > 3:
            paleta_a -= 1
        elif tecla in (ord('s'), ord('S'), curses.KEY_DOWN) and paleta_a < ALTO - 4:
            paleta_a += 1

        # --- Lógica Independiente de la Pelota ---
        # La pelota se mueve solo si ha pasado el tiempo configurado en 'intervalo_pelota'
        if tiempo_actual - ultimo_movimiento_pelota >= intervalo_pelota:
            ultimo_movimiento_pelota = tiempo_actual
            
            # Movimiento de la pelota
            pelota_x += dir_x
            pelota_y += dir_y

            # --- Inteligencia Artificial Dinámica (Bot B) ---
            # El bot calcula su movimiento al mismo ritmo que se desplaza la pelota
            if pelota_x > ANCHO // 3:
                if pelota_y < paleta_b and paleta_b > 3:
                    paleta_b -= 1
                elif pelota_y > paleta_b and paleta_b < ALTO - 4:
                    paleta_b += 1

            # Rebote en techo y suelo
            if pelota_y <= 1 or pelota_y >= ALTO - 2:
                dir_y *= -1

            # Colisión con Paleta Izquierda (Aumenta velocidad progresivamente)
            if pelota_x == 3 and (paleta_a - 2 <= pelota_y <= paleta_a + 2):
                dir_x *= -1
                intervalo_pelota = max(0.03, intervalo_pelota - 0.004)

            # Colisión con Paleta Derecha (Aumenta velocidad progresivamente)
            if pelota_x == ANCHO - 4 and (paleta_b - 2 <= pelota_y <= paleta_b + 2):
                dir_x *= -1
                intervalo_pelota = max(0.03, intervalo_pelota - 0.004)

            # --- Gestión de Puntos y Reinicios Confortables ---
            # Punto para el Bot
            if pelota_x <= 0:
                puntos_b += 1
                pelota_x, pelota_y = ANCHO // 2, ALTO // 2
                dir_x = 1
                intervalo_pelota = 0.08
                stdscr.refresh()
                time.sleep(0.6)  # Pausa corta y cómoda antes de reanudar
                ultimo_movimiento_pelota = time.time()

            # Punto para el Jugador A
            if pelota_x >= ANCHO - 1:
                puntos_a += 1
                pelota_x, pelota_y = ANCHO // 2, ALTO // 2
                dir_x = -1
                intervalo_pelota = 0.08
                stdscr.refresh()
                time.sleep(0.6)
                ultimo_movimiento_pelota = time.time()

        # Frecuencia de actualización de la interfaz (Aprox. 60 FPS)
        time.sleep(0.016)

# Iniciar la aplicación de curses de forma segura
curses.wrapper(juego)
