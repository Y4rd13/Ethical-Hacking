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
