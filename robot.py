import RPi.GPIO as GPIO
import bluetooth


# Номера пинов для левого мотора
LEFT_RPWM = 17
LEFT_LPWM = 27

# Номера пинов для правого мотора
RIGHT_RPWM = 23
RIGHT_LPWM = 24


# Настройка GPIO
GPIO.setmode(GPIO.BCM)


# Настройка пинов для левого мотора
GPIO.setup(LEFT_RPWM, GPIO.OUT)
GPIO.setup(LEFT_LPWM, GPIO.OUT)

# Настройка пинов для правого мотора
GPIO.setup(RIGHT_RPWM, GPIO.OUT)
GPIO.setup(RIGHT_LPWM, GPIO.OUT)


# Функции для управления моторами
def move_forward():
    GPIO.output(LEFT_RPWM, GPIO.LOW)
    GPIO.output(LEFT_LPWM, GPIO.HIGH)
    GPIO.output(RIGHT_RPWM, GPIO.LOW)
    GPIO.output(RIGHT_LPWM, GPIO.HIGH)


def move_backward():
    GPIO.output(LEFT_RPWM, GPIO.HIGH)
    GPIO.output(LEFT_LPWM, GPIO.LOW)
    GPIO.output(RIGHT_RPWM, GPIO.HIGH)
    GPIO.output(RIGHT_LPWM, GPIO.LOW)


def move_left():
    GPIO.output(LEFT_RPWM, GPIO.HIGH)
    GPIO.output(LEFT_LPWM, GPIO.LOW)
    GPIO.output(RIGHT_RPWM, GPIO.LOW)
    GPIO.output(RIGHT_LPWM, GPIO.HIGH)


def move_right():
    GPIO.output(LEFT_RPWM, GPIO.LOW)
    GPIO.output(LEFT_LPWM, GPIO.HIGH)
    GPIO.output(RIGHT_RPWM, GPIO.HIGH)
    GPIO.output(RIGHT_LPWM, GPIO.LOW)


def stop():
    GPIO.output(LEFT_RPWM, GPIO.LOW)
    GPIO.output(LEFT_LPWM, GPIO.LOW)
    GPIO.output(RIGHT_RPWM, GPIO.LOW)
    GPIO.output(RIGHT_LPWM, GPIO.LOW)


# Функция для выполнения команды
def move(command, last_command):
    if command == last_command:
        stop()
        print('stop')
        return b'0'
    elif command == b'3':
        move_forward()
        print('move_forward')
    elif command == b'4':
        move_backward()
        print('move_backward')
    elif command == b'1':
        move_left()
        print('move_left')
    elif command == b'2':
        move_right()
        print('move_right')
    return command


def main():
    # Создаем объект сервера Bluetooth, Выбираем порт для обмена данными
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_socket.bind(("", port))
    server_socket.listen(1)

    print("Ожидание входящего соединения...")
    client_socket, client_info = server_socket.accept()
    print("Соединение установлено с", client_info)
    
    last_data = b'0'
    while True:
        try:
            # Принимаем данные от клиента
            data = client_socket.recv(1024)

            if not data:
                break
            
            last_data = move(data, last_data)

            # Отправляем ответ обратно клиенту
            client_socket.send("Сообщение получено".encode())
        except Exception as e:
            print("Ошибка:", e)
            break

    # Закрываем соединения
    client_socket.close()
    server_socket.close()
    return 0


if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
