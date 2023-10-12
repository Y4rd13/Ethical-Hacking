## Quick Tweaks to start using Kali Linux

### Tweak your Kali VM

```
...
[ifupdown]
managed="true"
```

    cd /etc/NetworkManager

### Kali Repositories sources list

    ```
    sudo nano /etc/apt/sources.list
    ```

### Update, Install DKMS (Dynamic Kernel Module Support)

`dkms linux-headers-$(uname -r)` instalará el soporte para módulos dinámicos del kernel y los encabezados del kernel para la versión actual del kernel que estás usando. Esto es esencial si planeas instalar o compilar módulos del kernel personalizados. Por ejemplo, al instalar ciertos drivers o programas que requieren módulos del kernel específicos.

```
sudo apt update && sudo apt upgrade -y
sudo apt-get update && sudo apt-get install -y dkms linux-headers-$(uname -r)
sudo apt update && sudo apt upgrade -y
reboot
```
