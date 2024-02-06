# Virtual Machines on MacOS

Creating a Virtual Machine (or VM) with a guest OS can be accomplished by a number of tools. Just remember that you `virtualise` if the `host` and `guest` have the same architecture and `emulate` if they differ. The latter might cause a performance penalty.

[Virtual Box](https://www.virtualbox.org) is targeting x86 and AMD64/Intel64. For Apple Silicon (ARM64) you'll have the option of using a test-build: https://www.virtualbox.org/wiki/Testbuilds.

[Parallels](https://www.parallels.com) offers you a commercial virtualisation subscription if you need support.

[Qemu](https://www.qemu.org) might offer a better alternative, but it requires a build from source or using a package manager (https://wiki.qemu.org/Hosts/Mac). E.g.

```shell
brew install qemu
```

This solution is of course command line driven, but [UTM](https://github.com/utmapp/UTM) has a GUI on top of it. And with the [UTM Gallery](https://mac.getutm.app/gallery/) a quick start is guaranteed.

## Linux Guests

Grab an ISO from your favourite distribution :
* [Ubuntu](https://ubuntu.com/download/desktop)
* [Alpine](https://alpinelinux.org/downloads/)
* [Debian](https://www.debian.org/distrib/)
* [Linux Mint](https://www.linuxmint.com)
* [Fedora](https://fedoraproject.org)
* [OpenSuse](https://get.opensuse.org)

Some sites might offer VM images (e.g. `.qcow2`) for download as well.

## MacOS Guests

For a Mac-in-Mac experience an IPSW (iPhone Software) file is needed. Some download sites are listed [here](https://osxdaily.com/2021/01/28/download-macos-ipsw-files-apple-silicon-m1-mac) like [this one](https://ipsw.me) or go [beta](https://ipswbeta.dev).

## Windows Guests

You can grab the latest ISO from here https://www.microsoft.com/software-download/windows11, but be aware that you'll need to `emulate` this on Apple Silicon machines. [Windows Insider](https://www.microsoft.com/windowsinsider) offers an ARM64 build, but you'll need to sign up.

## Converting Virtual Boxes

Virtual Boxes come in different shapes and sizes like `.vmdk`, `.ova` or `.vdi`. If you like adds, then checkout this[page](https://computingforgeeks.com/convert-virtualbox-disk-image-vdi-to-qcow2-format) or [here](https://www.xmodulo.com/convert-ova-to-qcow2-linux.html) which has all the conversion options laid out.

An example:
```shell
qemu-img convert -f vdi -O qcow2 ubuntu.vdi ubuntu.qcow2 
```

## VM's as Code

One can create and provision a virtual machine fully automatic either on your `on-prem` hardware or somewhere in the `cloud`. This is known as *Infrastructure as Code*. The links here are put up for reference purpose only and not meant as a quick start into this area (with maybe **Vagrant** being the exception).

* [Vagrant](https://developer.hashicorp.com/vagrant)
* For [Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/infrastructure-automation) lots of options to choose from.
* [VMware Aria Suite](https://www.vmware.com/products/aria-suite-vcloud-suite.html)
* [OpenShift](https://www.redhat.com/en/blog/virtual-machines-as-code-with-openshift-gitops-and-openshift-virtualization)