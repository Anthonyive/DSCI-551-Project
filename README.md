# DSCI-551-Project

## Notes

1. Python virtual environment has been set up using `pipenv`. You need `pipenv` installed ([learn more](https://pipenv-fork.readthedocs.io/en/latest/)). Then run:

   ```bash
   pipenv install
   ```

   `pipenv` will install all python packages in the virtual environment. In the future, use

   ```bash
   pipenv install <wanted-package>
   ```

   to install a python package and it will keep track of what packages used in our project.

2. To access the Walmart API, you will need `consumer ID` from your account and three files: one private key pair file and two certificates. For more details, see [Walmart Affiliates API Quick Start](https://walmart.io/docs/affiliate/quick-start-guide). Put these three files to the root directory.

   ```bash
   ❯ ls | grep WM
   WM_IO_my_rsa_key_pair
   WM_IO_private_key.pem
   WM_IO_public_key.pem
   ```
