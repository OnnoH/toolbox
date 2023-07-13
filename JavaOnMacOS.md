# Java on MacOS

Download the required JDK from https://jdk.java.net or https://jdk.java.net/archive/

```shell
cd ~/Downloads
tar xf openjdk-13.0.1_osx-x64_bin.tar.gz
sudo mv jdk-13.0.1.jdk /Library/Java/JavaVirtualMachines/
java --version
```

If the version isn't allowed to open (\*.jdk was blocked from use because it is not from an identified developer), just go to System Settings -> Privacy & Security -> General -> click 'Allow Anyway' on the **Security** section. Just confirm **Open** next run. _(MacOS Ventura 13.3)_

List versions:

```shell
/usr/libexec/java_home -V
```

Change version:

```shell
export JAVA_HOME=$(/usr/libexec/java_home -v 1.8)
```

Verify version:

```shell
java --version
```

or JDK <= 8 : `java -version`

Remove version:

```shell
sudo rm -rf /Library/Java/JavaVirtualMachines/jdk-9.0.4.jdk
```
