# Building Lithops Docker images
_**READ THIS README BEFORE EXECUTING ANYTHING**_

You don't need to rebuild anything if it is not necessary. Just retrieve the images:
- **Vanilla Lithops**: `docker pull registry.scontain.com/amiguel/neardatapublic/lithops:vanilla`
- **SCONE Lithops**: `docker pull registry.scontain.com/amiguel/neardatapublic/lithops:latest`

## Versions
- Linux <span style="color:red">Alpine 3.17</span>
- SCONE <span style="color:red">5.8.0</span>
- Python <span style="color:red">3.10</span>
- Lithops <span style="color:red">3.0.1</span>

## Multiple phases with multiple stages

There are 3 phases, with 4 Dockerfile artifacts that are necessary, wherein multiple stages are executed:

1. **Base image**
   * <u>Dockerfile.lithops.python3.10.1.base</u>
     * Python 3.10 installation with Lithops essential modules
     * Patches applied and demo Lithops programs copied
   ****

2. **Enriched image**
   * <u>Dockerfile.lithops.python3.10.2.scratch</u>
     * Other Linux programs and other Python modules are installed
     * Image size is reduced by using "_**`FROM scratch`**_"
   ****

3. **Signed image**
   * <u>Dockerfile.lithops.python3.10.3.sign</u>
     * Python interpreter `python3.10` is signed to use SCONE libraries instead of traditional GLIBC
     * You have to provide a file [./files/identity.pem](./files/identity.pem "not available in the repository"). Check how to create one [here](https://sconedocs.github.io/ee_sconify_image/#identity)
     * Image size is reduced by using "_**`FROM scratch`**_"
   ****

4. **Lithops final injection**
   * <u>Dockerfile.lithops.github</u>
     * Used by the `lithops` desktop program, a Python program with the functionality to inject a Lithops installation inside a Docker image
     * It uses the Dockerfile above to perform the final step


### Execute the phases
Currently, the build settings are directly in the shell scripts and Dockerfile

You will have to change every mention to **yourdockerrepo** to your Docker login or path to private repository. Docker allows to push image to their public repository inside your login. As follows:
* `build_python310-lithops.1.base.sh` has _MADE_IMAGE=_**yourdockerrepo**_/lithops:alpine_python310-lithops301.1.base_
* `build_python310-lithops.2.scratch.sh` has _BASE_IMAGE=_**yourdockerrepo**_/lithops:alpine_python310-lithops301.1.base_ and _MADE_IMAGE=_**yourdockerrepo**_/lithops:alpine_python310-lithops301.2.scratch_
* `build_python310-lithops.3.final.sh` has  _BASE_IMAGE=_**yourdockerrepo**_/lithops:alpine_python310-lithops301.2.scratch_, _MADE_IMAGE=_**yourdockerrepo**_/lithops:alpine_python310-scone-lithops301_ and _VNLA_IMAGE=_**yourdockerrepo**_/lithops:alpine_python310-vanilla-lithops301_
* `Dockerfile.lithops.github` has _FROM_ **yourdockerrepo**_/lithops:alpine_python310-lithops301.2.scratch_

### First phase
Creation of the base image. It takes a really long time
* Execute: `./build_python310-lithops.1.base.sh 2>&1 |tee .build_python310-lithops.1.base.out >/dev/null`

### Second phase
Enrichment of the base image with other programs and Python modules
* Here is where you can go back and rebuild the image used in your programs, instead of going far back to the 1st stage. Just edit the corresponding Dockerfile
* Execute: `./build_python310-lithops.2.scratch.sh 2>&1 |tee .build_python310-lithops.2.scratch.out >/dev/null`

### Third phase
Preparation of the final images. Both Vanilla Lithops and SCONE Lithops are produced

Also, here is where the necessary images are pushed onto the repository
* Execute: `./build_python310-lithops.3.final.sh 2>&1 |tee .build_python310-lithops.3.final.out >/dev/null`
