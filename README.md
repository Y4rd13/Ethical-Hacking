# 🛡️ Ethical Hacking Course


## 📖 Table of Contents
<details>

- [🛡️ Ethical Hacking Course](#️-ethical-hacking-course)
  - [📖 Table of Contents](#-table-of-contents)
  - [🚀 Quick Tweaks to start using Kali Linux](#-quick-tweaks-to-start-using-kali-linux)
    - [🛠️ Tweak your Kali VM](#️-tweak-your-kali-vm)
    - [📜 Kali Repositories sources list](#-kali-repositories-sources-list)
    - [⚙️ Update, Install DKMS (Dynamic Kernel Module Support)](#️-update-install-dkms-dynamic-kernel-module-support)
    - [💿 Install Guest Additions in a VirtualBox VM](#-install-guest-additions-in-a-virtualbox-vm)
  - [🖥️ Linux Command-Line Interface (CLI)](#️-linux-command-line-interface-cli)
    - [🔗 Logical Operators](#-logical-operators)
    - [🔒 Linux File Permissions](#-linux-file-permissions)
  - [🌐 TOR](#-tor)
    - [⬇️ Install TOR](#️-install-tor)
    - [👤 Create a new user](#-create-a-new-user)
  - [🔗 Proxychains](#-proxychains)
    - [🌐 Tor Proxychains](#-tor-proxychains)
    - [🦊 Firefox Proxychains](#-firefox-proxychains)
    - [⚙️ Import custom proxy to proxychains](#️-import-custom-proxy-to-proxychains)
  - [🛡️ VPN](#️-vpn)
    - [🌐 OpenVPN](#-openvpn)
    - [🌐 NordVPN](#-nordvpn)
    - [🌐 NordVPN + OpenVPN](#-nordvpn--openvpn)
    - [📹 WebRTC](#-webrtc)
      - [1. Ajuste `media.peerconnection.enabled`](#1-ajuste-mediapeerconnectionenabled)
      - [2. Efectos de habilitar/deshabilitar WebRTC](#2-efectos-de-habilitardeshabilitar-webrtc)
      - [3. ¿Qué sucede si desactivo WebRTC?](#3-qué-sucede-si-desactivo-webrtc)
      - [4. ¿Debería desactivar WebRTC?](#4-debería-desactivar-webrtc)
  - [🔧 MAC Changer](#-mac-changer)
    - [Por qué no cambiar la dirección MAC puede ser una vulnerabilidad:](#por-qué-no-cambiar-la-dirección-mac-puede-ser-una-vulnerabilidad)
    - [¿Por qué la dirección MAC no deja la red local?](#por-qué-la-dirección-mac-no-deja-la-red-local)
    - [¿Por qué no es beneficioso cambiar la dirección MAC en una máquina virtual?](#por-qué-no-es-beneficioso-cambiar-la-dirección-mac-en-una-máquina-virtual)
    - [¿Cuándo podría ser beneficioso cambiar la dirección MAC?](#cuándo-podría-ser-beneficioso-cambiar-la-dirección-mac)
    - [Vendor](#vendor)
    - [En Virtual Machines](#en-virtual-machines)
    - [En Máquinas Físicas:](#en-máquinas-físicas)
  - [🔍 Nmap](#-nmap)
    - [🌐 Escaneo Básico](#-escaneo-básico)
    - [🔍 Escaneo Detallado con Versiones de Servicios](#-escaneo-detallado-con-versiones-de-servicios)
    - [🧠 Escaneo Avanzado con Nmap](#-escaneo-avanzado-con-nmap)
    - [🛡️ Escaneo de Detección de OS](#️-escaneo-de-detección-de-os)
    - [📡 nslookup: Resolución de Nombres a IPs](#-nslookup-resolución-de-nombres-a-ips)
    - [📖 Aprender Más](#-aprender-más)

</details>


## 🚀 Quick Tweaks to start using Kali Linux

### 🛠️ Tweak your Kali VM

  `sudo nano /etc/NetworkManager/NetworkManager.conf`

    ...
    [ifupdown]
    managed="true"


### 📜 Kali Repositories sources list

    
    sudo nano /etc/apt/sources.list
    

### ⚙️ Update, Install DKMS (Dynamic Kernel Module Support)

`dkms linux-headers-$(uname -r)` instalará el soporte para módulos dinámicos del kernel y los encabezados del kernel para la versión actual del kernel que estás usando. Esto es esencial si planeas instalar o compilar módulos del kernel personalizados. Por ejemplo, al instalar ciertos drivers o programas que requieren módulos del kernel específicos.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt-get update && sudo apt-get install -y dkms linux-headers-$(uname -r)
sudo apt update && sudo apt upgrade -y
reboot
```

### 💿 Install Guest Additions in a VirtualBox VM

    sudo apt-get install virtualbox-guest-additions-iso

    cd /media/kali/VBox_GAs_6.1.16
    sudo ./VBoxLinuxAdditions.run
    reboot

    # also you can use
    sudo apt install build-essential dkms
    # or
    sudo apt install build-essential dkms linux-headers-$(uname -r)

## 🖥️ Linux Command-Line Interface (CLI)

| Command | Description                                        | Explanation                                              | Usage                                   |
| ------- | -------------------------------------------------- | -------------------------------------------------------- | --------------------------------------- |
| `ls`    | List files                                         | Lists the contents of a directory                        | `ls /home/user`                         |
| `cd`    | Change directory                                   | Changes the current directory to the specified one       | `cd /home/user/Documents`               |
| `pwd`   | Print working directory                            | Displays the current directory path                      | `pwd`                                   |
| `mkdir` | Make directory                                     | Creates a new directory                                  | `mkdir new_directory`                   |
| `rm`    | Remove file                                        | Deletes a file or directory                              | `rm file.txt` or `rm -r directory_name` |
| `cp`    | Copy file                                          | Copies files or directories                              | `cp source.txt destination.txt`         |
| `mv`    | Move file                                          | Moves or renames files or directories                    | `mv old_name.txt new_name.txt`          |
| `cat`   | Concatenate files and print on the standard output | Displays the contents of a file                          | `cat file.txt`                          |
| `less`  | Opposite to `more`                                 | Views file content with scrolling capability             | `less file.txt`                         |
| `grep`  | Global regular expression print                    | Searches for a pattern within files                      | `grep "pattern" file.txt`               |
| `echo`  | Display a line of text                             | Prints the specified text                                | `echo "Hello, World!"`                  |
| `touch` | Change file timestamps                             | Creates an empty file or updates the timestamp of a file | `touch new_file.txt`                    |
| `chown` | Change file owner and group                        | Changes the owner and/or group of a file                 | `chown user:group file.txt`             |
| `chmod` | Change file mode bits                              | Modifies file permissions                                | `chmod 755 file.txt`                    |
| `man`   | Display a command's manual page                    | Shows the manual page of a command                       | `man ls`                                |
| `help`  | Display help for a built-in command                | Provides help for shell built-in commands                | `help cd`                               |

- `|` (Pipe): Takes the output of one command as input to another : `ls -l \| grep "txt"`

### 🔗 Logical Operators
| Operador | Descripción                                                                                   | Ejemplo                  |
| -------- | --------------------------------------------------------------------------------------------- | ------------------------ |
| `&&`     | Ejecuta el segundo comando si el primero tiene éxito                                          | `command1 && command2`   |
| `||`     | Ejecuta el segundo comando si el primero falla                                                | `command1 || command2`   |
| `!`      | Invierte el resultado (éxito/fallo) del comando                                               | `! command`              |
| `;`      | Ejecuta el segundo comando después del primero, sin importar si el primero tiene éxito o no  | `command1 ; command2`    |
| `&`      | Ejecuta el comando en segundo plano                                                           | `command &`              |
| `|`      | Toma la salida de un comando como entrada de otro                                             | `command1 \| command2`   |
| `>`      | Redirige la salida estándar a un archivo                                                      | `command > file`         |
| `>>`     | Redirige la salida estándar a un archivo, agregando el resultado al final del archivo         | `command >> file`        |
| `<`      | Redirige la entrada estándar desde un archivo                                                 | `command < file`         |
| `<<`     | Redirige la entrada estándar desde un documento de texto                                      | `command << EOF`         |


### 🔒 Linux File Permissions

| Valor Numérico | Permiso (Letras) | Descripción                                                          |
| -------------- | ---------------- | -------------------------------------------------------------------- |
| `4`            | `r`              | Leer (Read): El archivo puede ser leído.                             |
| `2`            | `w`              | Escribir (Write): Se pueden realizar cambios en el archivo.          |
| `1`            | `x`              | Ejecutar (Execute): El archivo puede ser ejecutado como un programa. |
| `0`            | `-`              | Ninguno (None): No se puede realizar ninguna acción en el archivo.   |

| Combinaciones/Modificadores | Descripción                              | Ejemplo de Uso                            |
| --------------------------- | ---------------------------------------- | ---------------------------------------- |
| `chmod 755`                 | Propietario: rwx, Grupo: r-x, Otros: r-x | `chmod 755 file.txt`                     |
| `chmod 644`                 | Propietario: rw-, Grupo: r--, Otros: r-- | `chmod 644 file.txt`                     |
| `chmod 700`                 | Propietario: rwx, Grupo: ---, Otros: --- | `chmod 700 file.txt`                     |
| `chmod 777`                 | Propietario: rwx, Grupo: rwx, Otros: rwx | `chmod 777 file.txt`                     |
| `chmod +x`                  | Añade permiso de ejecución a todos       | `chmod +x script.sh`                     |
| `chmod u+x`                 | Añade permiso de ejecución al propietario| `chmod u+x script.sh`                    |
| `chmod g-w`                 | Quita permiso de escritura al grupo      | `chmod g-w file.txt`                     |
| `chmod o-r`                 | Quita permiso de lectura a otros         | `chmod o-r file.txt`                     |


## 🌐 TOR

### ⬇️ Install TOR

    sudo apt install tor -y

### 👤 Create a new user

You don't want to compromise your system by running Tor as root. So, create a new user for Tor.

    sudo adduser {{test_user}}


## 🔗 Proxychains

Ability to route your traffic through a proxy server or a chain of proxy servers for anonymity purposes.

Always use SOCKS5 proxy, since it supports the UDP protocol and DNS lookups.

If you want to route your traffic using Tor, it is recommended to use `dynamic_chain` mode, due it's instability.


     sudo nano /etc/proxychains4.conf

    dynamic_chain
    ...
    [ProxyList]
    # add proxy here ...
    # meanwile
    # defaults set to "tor"
    socks4  127.0.0.1 9050
    socks5  127.0.0.1 9050


### 🌐 Tor Proxychains
    
    service tor start
    service tor status

    # Or
    sudo systemctl start tor
    sudo systemctl status tor

    # to stop
    sudo systemctl stop tor
    
### 🦊 Firefox Proxychains

Now you can use proxychains to route your traffic through Tor.

    proxychains firefox www.duckduckgo.com

Check your DNS leaks at [DNS Leak Test](https://www.dnsleaktest.com/)

### ⚙️ Import custom proxy to proxychains

_💡Note: Netherlands have great privacy policy, so you can use them. Same with Germany._

For example, go to (and copy a proxy):

  - [GithubRepo: ProxyList](https://github.com/jetkai/proxy-list) : An automatic updated list of free SOCKS4, SOCKS5, HTTP & HTTPS proxies in JSON, TXT, CSV, XML & YAML format. Proxies are online at the time of testing & updated every hour. Geolocation & detection status is also available.
    - [online-proxies/json/proxies-advanced.json](https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/json/proxies-advanced.json)

  - [ProxyList-Socks5](https://www.proxy-list.download/SOCKS5)

  - [FreeProxyUpdate-Socks5](https://freeproxyupdate.com/socks5-proxy)

  - [ProxyScrape](https://proxyscrape.com/free-proxy-list) 

  - [SocksProxyList](https://www.socks-proxy.net/)


  `sudo nano /etc/proxychains4.conf` , then:

    
    [ProxyList]
    # add proxy here ...
    # meanwile
    # defaults set to "tor"
    socks4  127.0.0.1 9050
    socks5  127.0.0.1 9050
    socks5  45.77.136.54 56747
    socks5  194.163.188.30 16871
    socks5  195.248.242.15 1237
    socks5  1.12.55.136 2080
    ... # add more here
    

## 🛡️ VPN

### 🌐 OpenVPN

    sudo apt install openvpn -y
    sudo openvpn --config {{file.ovpn}}


### 🌐 NordVPN

[NordVPN Linux installation](https://support.nordvpn.com/Connectivity/Linux/1325531132/Installing-and-using-NordVPN-on-Debian-Ubuntu-Raspberry-Pi-Elementary-OS-and-Linux-Mint.htm)

    nordvpn login
    nordvpn connect {country/group}

### 🌐 NordVPN + OpenVPN

[Connect to NordVPN with OpenVPN using Linux Terminal](https://support.nordvpn.com/Connectivity/Linux/1047409422/Connect-to-NordVPN-using-Linux-Terminal.htm)

1. Disable [IPV6](https://support.nordvpn.com/Connectivity/Linux/1047409212/How-to-disable-IPv6-on-Linux.htm)

    ```sh
    sudo nano /etc/sysctl.conf

    # Add the following at the bottom of the file:
    net.ipv6.conf.all.disable_ipv6 = 1
    net.ipv6.conf.default.disable_ipv6 = 1
    net.ipv6.conf.lo.disable_ipv6 = 1
    net.ipv6.conf.tun0.disable_ipv6 = 1

    # Save and Reboot your device.
    # To re-enable IPv6, remove the above lines from /etc/sysctl.conf and reboot your device.
    ```

2. Only after disabling IPV6, install the OpenVPN client by entering:

    ```sh
    sudo apt-get install openvpn
    ```
  
3. Download the OpenVPN configuration files with the command:

    ```sh
    sudo wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
    ```

4. ... Follow next steps in the **official guide:** [Connect to NordVPN with OpenVPN using Linux Terminal](https://support.nordvpn.com/Connectivity/Linux/1047409422/Connect-to-NordVPN-using-Linux-Terminal.htm).

### 📹 WebRTC

**Check your WebRTC leaks at [BrowserLeaks](https://browserleaks.com/webrtc)**

#### 1. Ajuste `media.peerconnection.enabled`

Ve a **Firefox** y escribe `about:config` en la barra de direcciones. Luego, busca `media.peerconnection.enabled` y deshabilítalo. Finalmente, **reinicia Firefox**.

El ajuste `media.peerconnection.enabled` en `about:config` de **Firefox** está relacionado con **WebRTC** (Web Real-Time Communication). WebRTC es una tecnología que permite la comunicación en tiempo real directamente en el navegador sin necesidad de plugins o aplicaciones externas. Es ampliamente utilizado para aplicaciones de videoconferencia, chats en vivo, transferencia de archivos y otras aplicaciones interactivas en tiempo real.


#### 2. Efectos de habilitar/deshabilitar WebRTC

El ajuste `media.peerconnection.enabled` tiene los siguientes efectos:

1. **Cuando está habilitado (valor `true`)**:
    - WebRTC está activo y funcionando en Firefox.
    - Las aplicaciones web pueden establecer conexiones P2P (peer-to-peer) para la transmisión de datos, video y audio.
    - Un posible riesgo asociado con tener esto habilitado es que sitios web maliciosos pueden usar WebRTC para detectar tu dirección IP local y pública, incluso si estás detrás de un VPN. Este riesgo es a menudo referido como una "fuga WebRTC" (**WebRTC Leak**).

2. **Cuando está deshabilitado (valor `false`)**:
    - WebRTC está desactivado en Firefox.
    - Las aplicaciones web no pueden usar WebRTC para establecer conexiones P2P.
    - El riesgo de "fuga WebRTC" (**WebRTC Leak**) se mitiga, ya que WebRTC está desactivado y no puede ser utilizado para detectar las direcciones IP.

#### 3. ¿Qué sucede si desactivo WebRTC?
Si `media.peerconnection.enabled` está configurado en `false`, algunas de las funcionalidades o acciones que no podrías realizar o que se verían afectadas incluyen:

- **Videoconferencias:** Muchos servicios de videoconferencia en línea dependen de WebRTC para funcionar directamente en el navegador. Si desactivas WebRTC, podrías experimentar problemas o no poder unirte a llamadas en plataformas como Jitsi, Google Meet, entre otros.

- **Chats en vivo con audio o video:** Las plataformas de chat que ofrecen opciones de llamadas de voz o video en tiempo real, como Discord Web o Facebook Messenger, podrían no funcionar correctamente.

- **Transferencia de archivos P2P:** Algunos sitios web y aplicaciones utilizan WebRTC para permitir la transferencia de archivos directamente entre usuarios sin pasar por un servidor central. Si desactivas WebRTC, estas transferencias podrían no ser posibles.

- **Juegos en línea con funciones de chat de voz:** Algunos juegos en línea que se juegan directamente en el navegador y que ofrecen chat de voz en tiempo real podrían no funcionar correctamente.

- **Aplicaciones de streaming en vivo:** Plataformas que permiten el streaming en vivo desde el navegador podrían depender de WebRTC para capturar y transmitir audio y video.

- **Aplicaciones de realidad aumentada o virtual:** Algunas aplicaciones web de AR o VR que requieren transmisión en tiempo real de datos podrían no funcionar sin WebRTC.

- **Detección automática de dispositivos:** WebRTC puede ayudar a las aplicaciones web a detectar y acceder a cámaras y micrófonos disponibles en tu dispositivo. Si lo desactivas, algunas aplicaciones podrían no ser capaces de acceder a estos dispositivos correctamente.

#### 4. ¿Debería desactivar WebRTC?
Si valoras tu privacidad y quieres asegurarte de que tu dirección IP no sea detectada por sitios web a través de WebRTC, puedes considerar desactivar este ajuste. Sin embargo, ten en cuenta que desactivar WebRTC puede afectar la funcionalidad de aplicaciones y sitios web que dependen de él.

En resumen, desactivar WebRTC puede mejorar la privacidad y seguridad, pero también puede limitar o afectar la funcionalidad de muchos servicios y aplicaciones web modernas que dependen de esta tecnología para la comunicación en tiempo real. Es importante sopesar los pros y contras antes de decidir desactivarlo.

---

## 🔧 MAC Changer

La dirección MAC (Media Access Control) es un identificador único asignado a interfaces de red para comunicaciones en el segmento de red física. Sirve como una dirección de hardware para tu dispositivo en una red local.


### Por qué no cambiar la dirección MAC puede ser una vulnerabilidad:

1. **Rastreo y Monitoreo** (Tracking & Monitoring): 📍
   - Muchas redes públicas (como las de cafeterías o aeropuertos) pueden rastrear tu dispositivo en función de su dirección MAC. Esto significa que cada vez que te conectas a estas redes, saben que eres tú. Con el tiempo, esto puede ser utilizado para construir un perfil de tus hábitos, ubicaciones y horarios.

2. **Suplantación** (Spoofing & Impersonation): 🎭
   - Si un atacante conoce la dirección MAC de un dispositivo confiable en una red, potencialmente puede suplantar esa dirección MAC y obtener acceso no autorizado a la red.

3. **Acceso a Datos Históricos** (Historical Data Access): 📜
   - En ciertos escenarios, los registros de red podrían mantenerse basados en direcciones MAC. Si tu dirección MAC nunca cambia, puede ser más fácil para alguien (con acceso a estos registros) acceder a todos los datos históricos y actividad asociada con tu dispositivo.

4. **Anonimato Reducido**: 🕵️‍♂️
   - En combinación con otras técnicas de rastreo, una dirección MAC consistente puede reducir aún más el anonimato de un usuario en el ámbito digital.

Por estas razones, cambiar periódicamente tu dirección MAC puede mejorar tu privacidad y seguridad, dificultando que entidades maliciosas rastreen, monitoreen o suplanten tu dispositivo.

### ¿Por qué la dirección MAC no deja la red local?

La dirección MAC es una dirección física utilizada para la comunicación dentro de una red local (LAN). A diferencia de las direcciones IP, que pueden ser utilizadas para rastrear paquetes a medida que viajan por Internet, las direcciones MAC operan en la Capa 2 (Capa de Enlace de Datos) del modelo OSI y no son utilizadas ni requeridas cuando los paquetes salen de la red local. Una vez que un paquete se prepara para ser enviado fuera de la LAN, la dirección MAC del dispositivo original se reemplaza por la dirección MAC del router o gateway. De esta manera, la dirección MAC original nunca deja la LAN y, por lo tanto, no puede ser utilizada para rastrear el tráfico a medida que viaja a través de Internet.

### ¿Por qué no es beneficioso cambiar la dirección MAC en una máquina virtual?

No es util cambiar la dirección MAC en una VM suele, puesto que suele ser más problemático que beneficioso debido a:

1. **Aislamiento de Red**: 🏠
   - La dirección MAC de la VM no es visible externamente debido al adaptador virtual que se comunica con el host físico.
   
2. **Configuración Adicional**: ⚙️
   - Requiere ajustes complicados en el software de virtualización y posiblemente en el host.

3. **Conflictos de Direcciones**: ❌
   - Riesgo de duplicar una dirección MAC existente en la red.

4. **Uso Principal de VMs**: 🎯
   - Las VMs generalmente se usan en entornos aislados, reduciendo la necesidad de cambiar la MAC.

5. **Licencias de Software**: 📜
   - Algunos softwares pueden dejar de funcionar si cambia su MAC asociada.

### ¿Cuándo podría ser beneficioso cambiar la dirección MAC?

En dispositivos físicos directamente expuestos a redes públicas, como un USB booteable, cambiar la dirección MAC puede mejorar la privacidad y la seguridad al hacer más difícil el rastreo y monitoreo del dispositivo.

### Vendor

Un "vendor" en el contexto de una dirección MAC se refiere al fabricante de la tarjeta de interfaz de red (NIC) u otro dispositivo de red. La dirección MAC es un identificador único de 48 bits asignado a interfaces de red para comunicaciones en la red física.

La dirección MAC se divide en dos partes:
1. **Identificador Único Organizacional (OUI)**: Los primeros 24 bits de la dirección MAC representan el OUI, que es asignado por la IEEE al fabricante. Esta parte identifica al fabricante del dispositivo de red.
2. **Identificador del Dispositivo**: Los 24 bits restantes son asignados por el fabricante y sirven como identificador único para el dispositivo de red en sí.

Examinando la parte OUI de una dirección MAC, se puede determinar el fabricante del dispositivo de red. Hay bases de datos y herramientas en línea que ayudan a identificar el fabricante asociado con una dirección MAC particular mediante la comprobación del OUI.

**Por ejemplo:**

Supongamos que tienes una dirección MAC como `6C:88:14:AB:CD:EF`. 

1. **Identificador Único Organizacional (OUI)**: La parte `6C:88:14` es el OUI, que corresponde al fabricante. Por ejemplo, este OUI podría corresponder a la empresa Apple Inc.
2. **Identificador del Dispositivo**: La parte `AB:CD:EF` es el identificador único del dispositivo asignado por Apple.

Usando bases de datos en línea o herramientas, puedes buscar el OUI `6C:88:14` para encontrar que corresponde a Apple Inc. Esto indica que este dispositivo de red fue fabricado por Apple.

### En Virtual Machines

En máquinas virtuales, cambiar la dirección MAC puede interrumpir la conexión. Sin embargo, en máquinas físicas o sistemas arrancados desde USB, este problema generalmente no ocurre.

_Note: en el caso de VirtualBox, la direccion MAC puede ser cambiada en la configuracion de VM, randomizando los bits, pero no el Vendor manufacturer._

1. **Capa Adicional de Abstracción**: Las máquinas virtuales (VM) funcionan sobre un hipervisor o software de virtualización, que actúa como una capa intermedia entre el sistema operativo de la VM y el hardware físico del host. Esta capa de abstracción maneja las conexiones de red y presenta una "tarjeta de red virtual" a la VM.

2. **Gestión de Redes por el Hipervisor**: Cuando configuras una VM, el hipervisor crea una interfaz de red virtual para esa VM. A menudo, esta interfaz se asigna con una dirección MAC específica. Si cambias la dirección MAC dentro de la VM sin informar al hipervisor, puede causar conflictos o desconexiones ya que el hipervisor podría no reconocer la nueva dirección MAC como válida para esa VM específica.

3. **Políticas de Seguridad**: Algunos hipervisores o sistemas de gestión de VM tienen políticas de seguridad que previenen o alertan sobre cambios en las direcciones MAC para prevenir suplantaciones o ataques en la red virtualizada.

### En Máquinas Físicas:

1. **Acceso Directo al Hardware**: A diferencia de las VM, las máquinas físicas interactúan directamente con el hardware, incluida la tarjeta de red. Cambiar la dirección MAC en este escenario se realiza directamente en la tarjeta de red, sin capas intermedias de abstracción.

2. **Sin Políticas de Hipervisor**: Ya que no hay un hipervisor involucrado, no hay políticas adicionales o reglas de gestión de red que puedan interferir o desconectar la conexión cuando cambias la dirección MAC.

3. **Persistencia**: En máquinas físicas o sistemas arrancados desde USB, la dirección MAC original de la tarjeta de red sigue siendo la misma tras reiniciar el dispositivo, a menos que se realice un cambio permanente. Esto no siempre es el caso en VMs, donde el hipervisor podría revertir a la dirección MAC original asignada a la VM tras un reinicio.


## 🔍 Nmap

Nmap (Network Mapper) es una herramienta para exploración de red y auditoría de seguridad. Permite descubrir dispositivos que se están ejecutando en una red y encontrar puertos abiertos junto con varios atributos de la red. Nmap es ampliamente utilizado en el mundo del hacking ético para descubrir puntos vulnerables en la red.

### 🌐 Escaneo Básico

Para escanear una dirección IP o un dominio:
  
      nmap {{target_ip_or_domain}}

🎯 Escaneo de Puertos Específicos:

      nmap -p {{port}} {{target_ip_or_domain}}
      nmap -p 22,80,443 {{target_ip_or_domain}}

### 🔍 Escaneo Detallado con Versiones de Servicios

Para obtener información detallada sobre los servicios que se están ejecutando en los puertos abiertos:

      nmap -sV {{target_ip_or_domain}}

### 🧠 Escaneo Avanzado con Nmap

Para llevar a cabo un escaneo detallado y avanzado en una dirección IP o dominio, se puede utilizar el siguiente comando:

      nmap -v -A {{target_ip_or_domain}}
  
- `-v`: Incrementa el nivel de verbosidad, permitiendo ver más detalles sobre lo que Nmap está haciendo durante el escaneo.
- `-A`: Realiza una detección avanzada, incluyendo la detección de sistema operativo, versión de servicios, detección de scripts y traceroute.

Para guardar la salida del escaneo en un archivo (Grepable Format):

      nmap -oG {{target_ip_or_domain}} > {{output_file}} (/home/SCAN)

Luego para obtener la información del archivo:

      cat {{input_file}} | grep {{grep_value}} | awk -F "{{delimiter}}" '{print $column_number}' > {{output_file}}
      cat /home/SCAN | grep Up | awk -F " " '{print $2}' > SCAN2

- `awk`: Es una herramienta de procesamiento de texto que permite extraer información de archivos de texto. En este caso, se utiliza para extraer la dirección IP de la salida del escaneo. Donde `-F` es el delimitador y `$2` es el número de columna.

Luego puedes usar el archivo de salida para realizar un escaneo de puertos en las direcciones IP que se encontraron:

      nmap -iL {{input_file}} -vv

      Por ejemplo:
      nmap -iL SCAN2 -vv

- `iL`: Permite leer las direcciones IP de un archivo de entrada.

### 🛡️ Escaneo de Detección de OS

Para detectar el sistema operativo de la máquina objetivo:

      nmap -O {{target_ip_or_domain}}

### 📡 nslookup: Resolución de Nombres a IPs

Antes de realizar un escaneo con Nmap, es posible que desees resolver un nombre de dominio a una dirección IP o viceversa. `nslookup` es una herramienta que permite hacer justamente eso.

Para resolver un nombre de dominio a una dirección IP:

      nslookup {{target_ip_or_domain}}

`nslookup` es útil para verificar que estás escaneando el objetivo correcto o para obtener información adicional sobre un dominio o dirección IP antes de realizar un escaneo más invasivo con Nmap.

### 📖 Aprender Más
Nmap es una herramienta poderosa con muchas características y opciones. Para aprender más sobre cómo usar Nmap, consulta la página man o la [documentacion de Nmap](https://nmap.org/docs.html).

      man nmap
