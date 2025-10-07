import requests
import sys

def get_ca_cert(cas, session, secret, cert, key):
    sessioncas = requests.Session()
    if (cert is not None and key is not None) == True:
        sessioncas.cert=(cert, key)
    url=f"https://{cas}:8081/v1/values/session={session},secret={secret}"

    try:
        response = sessioncas.get(url,
            headers={"Content-Type":"application/pem-certificate-chain"},
            verify=False,
        )
        if(response.status_code != 200):
            return response.status_code, f"[ERR]HTTP STATUS CODE:{response.status_code}. Body:{response.json()}"
        pem_secret = response.json()['value']
        if(pem_secret == None or pem_secret == ''):
            return response.status_code, f"[ERR]Invalid secret. Body:{response.json()}"
        if "BEGIN" in pem_secret:
            while pem_secret[len(pem_secret)-1] == '\n':
                pem_secret=pem_secret[0:len(pem_secret)-1]
        return response.status_code, pem_secret
    except (requests.exceptions.ConnectionError, OSError) as errcnx:
        print("[ERR]Exception:", errcnx.strerror)
        print("[ERR]Exception:", errcnx)
        return response.status_code, f"[ERR]Exception: {errcnx.strerror}, {errcnx}"

def main(argv, argc):
    cert=None #'' #'cert.pem'
    key=None #'' #'key.pem'
    retcode=0
    if argc == 4:
        cas     = argv[1]
        session = argv[2]
        secret  = argv[3]
    elif argc == 5:
        cas     = argv[1]
        session = argv[2]
        secret  = argv[3]
        cert    = argv[4]
    elif argc == 6:
        cas     = argv[1]
        session = argv[2]
        secret  = argv[3]
        cert    = argv[4]
        key     = argv[5]
    else:
        print(f"[ERR]invalid number of parameters({argc}): {argv[0]} CAS SESSION SECRET [CERT] [KEY]")
        return 1
    # First execution should succeed if the program runs attested and has access granted to the secret through export: session:
    # Second execution should succeed the secret has export_public: true
    # Otherwise it simply fails and gives the reasons
    status, body = get_ca_cert(cas, session, secret, cert, key)
    if status != 200:
        firsterror=body
        cert=None
        key=None
        status, body = get_ca_cert(cas, session, secret, cert, key)
        if status != 200:
            seconderror=body
            body=f"[ERR]there were 2 errors retrieving the secret {secret} from session {session} at CAS {cas}: 1.st:{firsterror} 2.nd:{firsterror}"
            retcode=status
    return retcode, body

if __name__ == '__main__':
    retcode, body = main(sys.argv, len(sys.argv))
    print(body)
    exit(retcode)
