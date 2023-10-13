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
    - [📹 WebRTC](#-webrtc)

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

_Note: Netherlands have great privacy policy, so you can use them. Same with Germany._

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


### 📹 WebRTC

El ajuste `media.peerconnection.enabled` en `about:config` de **Firefox** está relacionado con **WebRTC** (Web Real-Time Communication). WebRTC es una tecnología que permite la comunicación en tiempo real directamente en el navegador sin necesidad de plugins o aplicaciones externas. Es ampliamente utilizado para aplicaciones de videoconferencia, chats en vivo, transferencia de archivos y otras aplicaciones interactivas en tiempo real.

El ajuste `media.peerconnection.enabled` tiene los siguientes efectos:

1. **Cuando está habilitado (valor `true`)**:
    - WebRTC está activo y funcionando en Firefox.
    - Las aplicaciones web pueden establecer conexiones P2P (peer-to-peer) para la transmisión de datos, video y audio.
    - Un posible riesgo asociado con tener esto habilitado es que sitios web maliciosos pueden usar WebRTC para detectar tu dirección IP local y pública, incluso si estás detrás de un VPN. Este riesgo es a menudo referido como una "fuga WebRTC".

2. **Cuando está deshabilitado (valor `false`)**:
    - WebRTC está desactivado en Firefox.
    - Las aplicaciones web no pueden usar WebRTC para establecer conexiones P2P.
    - El riesgo de "fuga WebRTC" se mitiga, ya que WebRTC está desactivado y no puede ser utilizado para detectar las direcciones IP.

Si valoras tu privacidad y quieres asegurarte de que tu dirección IP no sea detectada por sitios web a través de WebRTC, puedes considerar desactivar este ajuste. Sin embargo, ten en cuenta que desactivar WebRTC puede afectar la funcionalidad de aplicaciones y sitios web que dependen de él.