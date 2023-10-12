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

### Install Guest Additions in a VirtualBox VM

    sudo apt-get install virtualbox-guest-additions-iso

    cd /media/kali/VBox_GAs_6.1.16
    sudo ./VBoxLinuxAdditions.run
    reboot

    # also you can use
    sudo apt install build-essential dkms
    # or
    sudo apt install build-essential dkms linux-headers-$(uname -r)

## Linux Command-Line Interface (CLI)

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

### Logical Operators
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


### Linux File Permissions

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
