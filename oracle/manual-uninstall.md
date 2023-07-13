# Oracle RDBMS Manual Uninstall

## Windows

- Uninstall all Oracle components using the Oracle Universal Installer (OUI).
- Run regedit.exe and delete the HKEY_LOCAL_MACHINE/SOFTWARE/Oracle key. This contains registry entires for all Oracle products.
- If you are running 64-bit Windows, you should also delete the HKEY_LOCAL_MACHINE/SOFTWARE/Wow6432Node/Oracle key if it exists.
- Delete any references to Oracle services left behind in the following part of the registry (HKEY_LOCAL_MACHINE/SYSTEM/CurrentControlSet/Services/Ora\*). It should be pretty obvious which ones relate to Oracle.
- Reboot your machine.
- Delete the "C:\Oracle" directory, or whatever directory is your ORACLE_BASE.
- Delete the "C:\Program Files\Oracle" directory.
- If you are running 64-bit Wiindows, you should also delete the "C:\Program Files (x86)\Oracle" directory.
- Remove any Oracle-related subdirectories from the "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\" directory.
- Empty the contents of your "C:\temp" directory.
- Empty your recycle bin.

At this point your machine will be as clean of Oracle components as it can be without a complete OS reinstall.

Remember, manually editing your registry can be very destructive and force an OS reinstall so only do it as a last resort.

If some DLLs can't be deleted, try renaming them, the after a reboot delete them.

## Unix

Uninstalling all products from UNIX is a lot more consistent. If you do need to resort to a manual uninstall you should do something like:

- Uninstall all Oracle components using the Oracle Universal Installer (OUI).
- Stop any outstanding processes using the appropriate utilities.

```
# oemctl stop oms user/password
# agentctl stop
# lsnrctl stop
```

Alternatively you can kill them using the kill -9 pid command as the root user.

- Delete the files and directories below the $ORACLE_HOME.

```
# cd $ORACLE_HOME
# rm -Rf *
```

- With the exception of the product directory, delete directories below the $ORACLE_BASE.

```
# cd $ORACLE_BASE
# rm -Rf admin doc jre o*
```

- Delete the /etc/oratab file. If using 9iAS delete the /etc/emtab file also.

```
# rm /etc/oratab /etc/emtab
```
