#Librerias
from machine import Pin
import utime
from tm1637 import TM1637

# Configuración de los pines
Button_Reset = Pin(14, Pin.IN, Pin.PULL_UP)
Button_Des = Pin(13, Pin.IN, Pin.PULL_UP)
Button_Inc = Pin(32, Pin.IN, Pin.PULL_UP)
Button_Camb = Pin(15, Pin.IN, Pin.PULL_UP)
Button_Alarm = Pin(22,Pin.IN, Pin.PULL_UP)
Led_S = Pin(4, Pin.OUT)
LedAM = Pin(21, Pin.OUT)
LedPM = Pin(27, Pin.OUT)
LedAlarma_Inicio = Pin(5, Pin.OUT)
LedAlarma_Final = Pin(23, Pin.OUT)
Buzzer = Pin(12, Pin.OUT)
Bombillo = Pin(33, Pin.OUT)

# Inicialización del módulo TM1637
tm = TM1637(dio=Pin(16), clk=Pin(17))

# Configura el brillo (0-7)
tm.brightness(4)

# Variables
tiempo_transcurrido_ms = 0
tiempo_12h = 0
aux = 0
aux_modo = 0
aux_Alarm = 0
Contador_AlarmInicio=0
Contador_AlarmFinal=0
modo_hora = 0
TiempoAlarma_Inicio=0
TiempoAlarma_Final=0

def obtener_hora_minutos_segundos(tiempo_transcurrido_ms):
    # Calcula las horas, los minutos y los segundos
    horas = (tiempo_transcurrido_ms // 3600000) % 24  # 1 hora = 3600000 ms
    minutos = (tiempo_transcurrido_ms % 3600000) // 60000  # 1 minuto = 60000 ms
    segundos = (tiempo_transcurrido_ms % 60000) // 1000  # 1 segundo = 1000 ms

    return horas, minutos, segundos

# Bucle principal
while True:
    # Verifica si se presionó el botón para resetear
    if not Button_Reset.value():
        utime.sleep_ms(20)  # Espera para evitar lecturas falsas por rebote
        if not Button_Reset.value():
            tiempo_transcurrido_ms = 0
            tiempo_12h = 0
            aux = 0
            aux_modo = 0
            aux_Alarm = 0
            TiempoAlarma_Inicio=0
            TiempoAlarma_Final=0
            tm.show("0000")
            LedAM.value(False)
            LedPM.value(False)
            LedAlarma_Inicio.value(False)
            LedAlarma_Final.value(False)
            while not Button_Reset.value():
                pass  # Espera hasta que se suelte el botón
    
        horas, minutos, segundos = obtener_hora_minutos_segundos(tiempo_transcurrido_ms)    
    

    # Verifica si se presionó el botón para cambiar el modo a AM/PM
    if not Button_Camb.value():
        utime.sleep_ms(20)  # Espera para evitar lecturas falsas por rebote
        if not Button_Camb.value():
            aux_modo += 1 
            if(aux_modo == 4):
                aux_modo = 0
        if(aux_modo == 0):
            LedPM.value(False)
            LedAM.value(False)
        elif(aux_modo == 1):
            if(tiempo_transcurrido_ms >= 13*3600000 and tiempo_transcurrido_ms <= 23*3600000 + 59*60000 + 59000):
                tiempo_12h = tiempo_transcurrido_ms - 12*3600000
                LedPM.value(True)
                LedAM.value(False)
            elif(tiempo_transcurrido_ms >= 1*3600000 and tiempo_transcurrido_ms <= 11*3600000 + 59*60000 + 59000):
                LedAM.value(True)
                LedPM.value(False)
            elif(tiempo_transcurrido_ms >= 12*3600000 and tiempo_transcurrido_ms <= 12*3600000 + 59*60000 + 59000):
                LedAM.value(False)
                LedPM.value(True)
            else:
                tiempo_12h = tiempo_transcurrido_ms + 12*3600000
                LedAM.value(True)
                LedPM.value(False)
                
    # Verifica si se presionó el botón para desplazarse entre los displays
    if(aux_modo == 2):
        LedPM.value(False)
        LedAM.value(False)
        LedAlarma_Final.value(True)
        LedAlarma_Inicio.value(True)
        if not Button_Des.value():
            utime.sleep_ms(20)  # Espera para evitar lecturas falsas por rebote
            if not Button_Des.value():
                if(aux == 4):
                    aux = 0
                else:
                    aux += 1                          
            while not Button_Des.value():
                pass  # Espera hasta que se suelte el botón 
        if not Button_Inc.value():
            utime.sleep_ms(20)  # Espera para evitar lecturas falsas por rebote
            if not Button_Inc.value():
                if(aux == 0):
                    minutos += 1
                elif(aux == 1):
                    minutos += 10
                elif(aux == 2):
                    horas += 1
                else:
                    if(horas >= 20):
                        horas -= 30
                    horas += 10
                tiempo_transcurrido_ms = (horas*3600 + minutos*60)*1000
                tiempo_12h = tiempo_transcurrido_ms
        horas, minutos, segundos = obtener_hora_minutos_segundos(tiempo_transcurrido_ms)
                
    # Verifica si se presionó el botón para cambiar al modo a Alarma
    if(aux_modo==3):
        if not Button_Alarm.value():
            utime.sleep_ms(20)
            if not Button_Alarm.value():
                aux_Alarm += 1
                if (aux_Alarm==3):
                    aux_Alarm=0            
        if(aux_Alarm==1):
            horas, minutos, segundos = obtener_hora_minutos_segundos(TiempoAlarma_Inicio)
            tm.numbers(horas, minutos, segundos)
            LedAlarma_Inicio.value(True)
            LedAlarma_Final.value(False)
            if not Button_Des.value():
                utime.sleep_ms(20)  # Espera para evitar lecturas falsas por rebote
                if not Button_Des.value():
                    if(Contador_AlarmInicio == 4):
                        Contador_AlarmInicio = 0
                    else:
                        Contador_AlarmInicio += 1                          
                while not Button_Des.value():
                    pass  # Espera hasta que se suelte el botón
            if not Button_Inc.value():
                utime.sleep_ms(20)  # Espera para evitar lecturas falsas por rebote
                if not Button_Inc.value():
                    if(Contador_AlarmInicio == 0):
                        minutos += 1
                    elif(Contador_AlarmInicio == 1):
                        minutos += 10
                    elif(Contador_AlarmInicio == 2):
                        horas += 1
                    else:
                        if(horas >= 20):
                            horas -= 30
                        horas += 10
                    TiempoAlarma_Inicio = (horas*3600 + minutos*60)*1000
        elif(aux_Alarm==2):
            horas, minutos, segundos = obtener_hora_minutos_segundos(TiempoAlarma_Final)
            tm.numbers(horas, minutos, segundos)
            LedAlarma_Final.value(True)
            LedAlarma_Inicio.value(False)
            if not Button_Des.value():
                utime.sleep_ms(20)  # Espera para evitar lecturas falsas por rebote
                if not Button_Des.value():
                    if(Contador_AlarmFinal == 4):
                        Contador_AlarmFinal = 0
                    else:
                        Contador_AlarmFinal += 1                          
                while not Button_Des.value():
                    pass  # Espera hasta que se suelte el botón
            if not Button_Inc.value():
                utime.sleep_ms(20)  # Espera para evitar lecturas falsas por rebote
                if not Button_Inc.value():
                    if(Contador_AlarmFinal == 0):
                        minutos += 1
                    elif(Contador_AlarmFinal == 1):
                        minutos += 10
                    elif(Contador_AlarmFinal == 2):
                        horas += 1
                    else:
                        if(horas >= 20):
                            horas -= 30
                        horas += 10
                    TiempoAlarma_Final = (horas*3600 + minutos*60)*1000
        else:
            LedAlarma_Final.value(False)
            LedAlarma_Inicio.value(False)
    # Hace parpadear el LED cada segundo
    Led_S.value(not Led_S.value())  # Invierte el estado del LED
    
    if(tiempo_transcurrido_ms >= 24*3600000):
        tiempo_transcurrido_ms -= 24*3600000
        
    if(tiempo_transcurrido_ms>=TiempoAlarma_Inicio and tiempo_transcurrido_ms<=TiempoAlarma_Final):
        Buzzer.value(True)
        Bombillo.value(True)
    else:
        Buzzer.value(False)
        Bombillo.value(False)
    
    if(aux_modo == 0 and aux_Alarm==0):
        horas, minutos, segundos = obtener_hora_minutos_segundos(tiempo_transcurrido_ms)
    elif(aux_modo == 1):
        horas, minutos, segundos = obtener_hora_minutos_segundos(tiempo_12h)
    elif(aux_Alarm==1 ):
        horas, minutos, segundos = obtener_hora_minutos_segundos(TiempoAlarma_Inicio)
    elif(aux_Alarm==2):
        horas, minutos, segundos = obtener_hora_minutos_segundos(TiempoAlarma_Final)
    
    # Muestra la hora, los minutos y los segundos en el TM1637
    tm.numbers(horas, minutos, segundos)
    print(aux_modo)  #Se muestra por consola los segundos transcurridos
    
    # Actualiza el tiempo transcurrido
    tiempo_transcurrido_ms += 1000  # Aumenta en 1000 ms (1 segundo)
    tiempo_12h += 1000  # Aumenta en 1000 ms (1 segundo)

    # Espera un segundo antes de actualizar la
    utime.sleep(1)