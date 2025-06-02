import socket

def ping_port(host, port):
    # Cria um objeto socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Tenta se conectar ao host na porta específica
        s.connect((host, port))
        s.shutdown(socket.SHUT_RDWR)  # Fecha a conexão
        return True
    except (socket.timeout, ConnectionRefusedError):
        # Se houver um timeout ou conexão recusada, assume que a porta não está acessível
        return False
    finally:
        s.close()

# Exemplo de uso
host = '10.100.0.1'  # Altere para o host que deseja pingar
port = 389  # Porta que deseja pingar

if ping_port(host, port):
    print(f"A porta {port} em {host} está acessível.")
else:
    print(f"A porta {port} em {host} não está acessível.")
