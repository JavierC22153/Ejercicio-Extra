import random

MENSAJE = "Criptografia UVG 2026"

# PARTE A

def cifrar_xor(mensaje, semilla):
    random.seed(semilla)
    cifrado = []
    for caracter in mensaje:
        keystream = random.randint(0, 255)
        byte_cifrado = ord(caracter) ^ keystream
        cifrado.append(byte_cifrado)
    return cifrado

def descifrar_xor(cifrado, semilla):
    random.seed(semilla)
    mensaje = ""
    for byte in cifrado:
        keystream = random.randint(0, 255)
        caracter = chr(byte ^ keystream)
        mensaje += caracter
    return mensaje


print("PARTE A — Cifrado de flujo con XOR")
print("-------------------------------------")
SEMILLA = 42
print(f"Mensaje original  : {MENSAJE}")

cifrado = cifrar_xor(MENSAJE, SEMILLA)
print(f"Mensaje cifrado   : {' '.join(f'{b:02x}' for b in cifrado)}")

descifrado = descifrar_xor(cifrado, SEMILLA)
print(f"Mensaje recuperado: {descifrado}")

# PARTE B — Cifrado por bloques 

SBOX = {
    'A':'Q', 'B':'W', 'C':'E', 'D':'R', 'E':'T', 'F':'Y', 'G':'U',
    'H':'I', 'I':'O', 'J':'P', 'K':'A', 'L':'S', 'M':'D', 'N':'F',
    'O':'G', 'P':'H', 'Q':'J', 'R':'K', 'S':'L', 'T':'Z', 'U':'X',
    'V':'C', 'W':'V', 'X':'B', 'Y':'N', 'Z':'M', ' ':'_',
    '0':'1', '1':'2', '2':'3', '3':'4', '4':'5', '5':'6',
    '6':'7', '7':'8', '8':'9', '9':'0', '_':' '
}
SBOX_INV = {v: k for k, v in SBOX.items()}

TRANSPONER     = [3, 0, 5, 2, 7, 4, 1, 6]
TRANSPONER_INV = [1, 6, 3, 0, 5, 2, 7, 4]

CLAVE = "UVGCLAVE"

def sustituir(bloque):
    return ''.join(SBOX.get(c, c) for c in bloque)

def transponer(bloque):
    return ''.join(bloque[i] for i in TRANSPONER)

def aplicar_xor(bloque, clave):
    return bytes(ord(c) ^ ord(clave[i % len(clave)]) for i, c in enumerate(bloque))

def sustituir_inv(bloque):
    return ''.join(SBOX_INV.get(c, c) for c in bloque)

def transponer_inv(bloque):
    resultado = [''] * 8
    for i, pos in enumerate(TRANSPONER):
        resultado[pos] = bloque[i]
    return ''.join(resultado)

def cifrar_bloques(mensaje, clave):
    mensaje = mensaje.upper()
    while len(mensaje) % 8 != 0:
        mensaje += ' '
    cifrado = b""
    for i in range(0, len(mensaje), 8):
        bloque = mensaje[i:i+8]
        p1 = sustituir(bloque)
        p2 = transponer(p1)
        p3 = aplicar_xor(p2, clave)
        print(f"  Bloque {i//8+1}: '{bloque}' → sust '{p1}' → trans '{p2}' → XOR '{p3.hex()}'")
        cifrado += p3
    return cifrado

def descifrar_bloques(cifrado, clave):
    descifrado = ""
    for i in range(0, len(cifrado), 8):
        bloque_bytes = cifrado[i:i+8]
        p1 = ''.join(chr(b ^ ord(clave[j % len(clave)])) for j, b in enumerate(bloque_bytes))
        p2 = transponer_inv(p1)
        p3 = sustituir_inv(p2)
        descifrado += p3
    return descifrado.rstrip(' ')


print("\nPARTE B — Cifrado por bloques")
print("-------------------------------------")
print(f"Mensaje original  : {MENSAJE}")
print(f"Clave             : {CLAVE}")

print("\nTransformaciones por bloque:")
cifrado_b = cifrar_bloques(MENSAJE, CLAVE)

print(f"\nMensaje cifrado   : {cifrado_b.hex()}")

descifrado_b = descifrar_bloques(cifrado_b, CLAVE)
print(f"Mensaje recuperado: {descifrado_b}")