# SCONE Keycloak integration Python module

Scontain prepared a set of functions to integrate Keycloak into Python systems.

Keycloak is an _identity and access manager_ to which applications can outsource user management and access control.
The workflow is:
* User authenticates itself on Keycloak
* Keycloak issues an access token with their details, such as email address and roles (for _RBAC_ systems)
* Recipient system checks if the roles claimed by the user correspond to any of the roles the system accepts
* Recipient system sends the access token to the same server it has been issued to check the veracity of the claims in it
* Keycloak issues a validation token if it has been issued there and if it is within the valid period
* Recipient system can now proceed

## Module: sconekc

Example of how to use the Python module **`sconekc`**. On Python prompt `>>>`.

### Use case: successful

You will have to provide a **realm**, a **client**, a **username**, a **password**:
* `REALM='surgonomics'`
* `CLIENT='pravega-client'`
* `USERNAME1='haneks'`
* `PASSWORD1='Skfo42fdr872'`

Import the module (e.g. consider `sconekc.py` file is in current directory):
* `import sconekc as kc`

Obtain an access token:
* `AT=kc.get_access_token(f'https://keycloak.neardata.eu:30443/realms/{REALM}/protocol/openid-connect/token', f'{CLIENT}', f'{USERNAME1}', f'{PASSWORD1}', cert='cert.pem', key='key.pem')`

The result is a triplet separated by dot '.'. Example (stripped string):
* **eyJhbGciOiJSUzI1NiIsInR5.eyJleHAiOjE3NDkyMTU4OTQsImlhdCI6MTc0OTIxMzQ5NCwianRpIjoiNDNmN.gz33ItRfQgiK6pa-0q-UWkk2tWz7b_g2XRzM-SbZNFAFtqz7hT35RVcjbfmyw8wE1iPZ1h7YQ5DECB_KQ0doYLxKXPCr4K50jBElprc6I47AL_BZToy-k9pzMNbv1YykzXd_j5XbGL2HhRXLtyfzgSRHbp8vkVlh2Oo-lTPH3X3yuoZkFnGa0Qz41iXFKEv**

Inspect the access token:
* `kc.showJWT(AT)`
```
Header:  {'alg': 'RS256',
 'kid': '1kqyGywGSCD50AAM2dhir-DvbfBJQjFOwj40O_7w9Q8',
 'typ': 'JWT'}
Token:   {'acr': '1',
 'allowed-origins': ['http://localhost*', 'https://localhost*'],
 'aud': 'account',
 'azp': 'pravega-client',
 'email': 'haneks@neardata.eu',
 'email_verified': True,
 'exp': 1749216324,
 'family_name': 'Keks',
 'given_name': 'Hansa',
 'iat': 1749213924,
 'iss': 'https://keycloak.neardata.eu:30443/realms/surgonomics',
 'jti': 'c639f1b5-441a-4b9c-8d3e-e4a149de62af',
 'name': 'Hansa Keks',
 'preferred_username': 'haneks',
 'realm_access': {'roles': ['pravega_lungs',
                            'pravega_liver',
                            'default-roles-surgonomics']},
 'resource_access': {'account': {'roles': ['manage-account',
                                           'manage-account-links',
                                           'view-profile']}},
 'scope': 'surg-ongo openid email profile',
 'sid': 'e66ffe54-2d97-42d6-XXYY-d2cdd1b08762',
 'sub': 'd3efadeb-95eb-4d49-YYZZ-7aa51fde137a',
 'typ': 'Bearer'}
Signature:   'F4K47zH0jby5YbywiLYkQVySNsZClaDJiOPtHUc-soq_Fvxv4e1mZX3Psz2piY4HJ1Grvo9QQYpX4651ItqVx7_4CjtIEx4uaKV6VKXX-idw8nbVNaqLQbizTe-QBl8Y-GpU--Ko_mlCXe_az-0KCRfsqSH4VcvDas1I-VDsGnwyMrEv6fQHNX3CJu25A'
Issued at:  2025-06-06 12:45:24 (localtime)
Not before: Undefined (localtime)
Expiration: 2025-06-06 13:25:24 (localtime)
```

The system will proceed if the user has the access to the role **pravega_lungs**:
* `header, jwt, signature, issued, started, validto = kc.sliceJWT(AT)`
* `op='pravega_lungs'; print(f'user can execute the system {op}. submit AT for validation') if op in jwt['realm_access']['roles'] else print(f'user cannot execute the system {op}. abort connection')`
  - **user can execute the system pravega_lungs. submit AT for validation** 

To confirm whether this is the truth, a corresponding validation token has to be issued by the same server:
* `VT=kc.get_validation_token(f'https://keycloak.neardata.eu:30443/realms/{REALM}/protocol/openid-connect/userinfo', AT, cert='../cert.pem', key='../key.pem')`

With the validation token:
* `print(f"{VT['preferred_username']}; {VT['accesstokendatetimeissuing']}; {VT['accesstokendatetimeexpiring']}; Valid for {str(int((VT['validationtokentimestampvalidation']-VT['accesstokentimestampissuing'])/60))} minutes more")`
  - **haneks; Issued at:  2025-06-06 12:45:24 (localtime); Expiration: 2025-06-06 13:25:24 (localtime); Valid for 20 minutes more**

### Use case: unsuccessful

Same **realm** and **client**, but different **username** and **password**:
* `USERNAME2='haneks'`
* `PASSWORD2='Skfo42fdr872'`

Obtain an access token:
* `AT=kc.get_access_token(f'https://keycloak.neardata.eu:30443/realms/{REALM}/protocol/openid-connect/token', f'{CLIENT}', f'{USERNAME2}', f'{PASSWORD2}', cert='cert.pem', key='key.pem')`

Inspect the access token:
* `kc.showJWT(AT)`
```
Header:  {'alg': 'RS256',
 'kid': '1kqyGywGSCD50AAM2dhir-DvbfBJQjFOwj40O_7w9Q8',
 'typ': 'JWT'}
Token:   {'acr': '1',
 'allowed-origins': ['http://localhost*', 'https://localhost*'],
 'aud': 'account',
 'azp': 'pravega-client',
 'email': 'kellsen@neardata.eu',
 'email_verified': True,
 'exp': 1749218926,
 'family_name': 'Varnsen',
 'given_name': 'Kelly',
 'iat': 1749216526,
 'iss': 'https://keycloak.neardata.eu:30443/realms/surgonomics',
 'jti': '261be651-c464-4473-8bb4-341703f1ea28',
 'name': 'Kelly Varnsen',
 'preferred_username': 'kellsen',
 'realm_access': {'roles': ['offline_access',
                            'pravega_liver',
                            'default-roles-surgonomics',
                            'pravega_kidney']},
 'resource_access': {'account': {'roles': ['manage-account',
                                           'manage-account-links',
                                           'view-profile']}},
 'scope': 'surg-ongo openid email profile',
 'sid': '3c7a0f79-c5e1-4502-8b00-8194636e671b',
 'sub': 'd8e973ea-1a5c-46d0-8ff6-6f86eb6776a0',
 'typ': 'Bearer'}
Signature:   'J_671QBa_DOrrhJAA2WCbCkjmgW8SYzI-xmrR7X42tnufDB_6XuA-lKhV5vopPWWgbRxo2L8vrf3cehT6U-DEZvnFFgg0WQWqlvAM5yJZuRZjQu0lvR-jxkrYB_hRneHHVhDjMY-qzY29Oy6ftyV_IIS0ck1GLlfbODGU_K8jRgziwz0fpgdc6n51Cqxv-o0Pc'
Issued at:  2025-06-06 13:28:46 (localtime)
Not before: Undefined (localtime)
Expiration: 2025-06-06 14:08:46 (localtime)
```

The system will proceed if the user has the access to the role **pravega_lungs**:
* `header, jwt, signature, issued, started, validto = kc.sliceJWT(AT)`
* `op='pravega_lungs'; print(f'user can execute the system {op}. submit AT for validation') if op in jwt['realm_access']['roles'] else print(f'user cannot execute the system {op}. abort connection')`
  - **user cannot execute the system pravega_lungs. abort connection** 

User has other roles (**pravega_liver**, **pravega_kidney**) regarding what he or she can do in the operation room. Therefore, the system can abort the connection.
