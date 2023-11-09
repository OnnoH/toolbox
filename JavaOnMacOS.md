# Java on MacOS

Download the required JDK or GraalVM from https://jdk.java.net or https://www.graalvm.org/downloads/ respectively. For older JDKs go down to the archive https://jdk.java.net/archive/.

```shell
cd ~/Downloads
tar xf graalvm-jdk-21_macos-aarch64_bin.tar.gz
sudo mv graalvm-jdk-17.0.9+11.1 /Library/Java/JavaVirtualMachines/
java --version
```

If the version isn't allowed to open (\*.jdk was blocked from use because it is not from an identified developer), just go to System Settings -> Privacy & Security -> General -> click 'Allow Anyway' on the **Security** section. Just confirm **Open** next run. _(MacOS Ventura 13.3)_

If a message is shown that the JDK is damaged, remove it from quarantine:

```shell
sudo xattr -r -d com.apple.quarantine /Library/Java/JavaVirtualMachines/graalvm-jdk-17.0.9+11.1
```

List versions:

```shell
/usr/libexec/java_home -V
```

Change version:

```shell
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
```

Verify version:

```shell
java --version
```

or JDK <= 8 : `java -version`

Remove version:

```shell
sudo rm -rf /Library/Java/JavaVirtualMachines/graalvm-jdk-17.0.9+11.1
```
