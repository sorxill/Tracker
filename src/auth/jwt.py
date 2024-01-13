from datetime import datetime, timedelta

import jwt

EXPIRE_M = 15
ALG = "RS256"
PRIVATE = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDa2j0DYI3aaLmR
OJ4oVgPYpWi3QJ9VP2FFXpNQ2aQrxBZnXV5zxoBXZAxSghXCh0t4RXbl4NBc+ZBf
o06u8nzZ9PdmHLryi+1TxwKuL29w8iEezhEk3OnUp7ZO8Ogq66KxDx8rEqu78b8+
eIj9gk2t+EQafV9gBMK8Hf7SYqzOFEkU2o5hrob9Kx4YALhQACEjv3UPIYZWJFrY
c5f/47YropLPjYcU7PoxaoJUuKBbFFWz3hOQe21d9sncuKXnOpCTJN+yH5hZz5hg
G1pR4Kz6WNO0iVMurQ+K1w8p6hLtIdfSmhzzCL0ewNSIsNUjQ61W4ldqY6BW0Rdi
r6SOIIMDAgMBAAECggEAFTA14gLSGQg0lxu9LDiPrMTu63cFNhKpzzaF2rkHjPky
FhXTFDBusodMLhzMEIZaxy0qgr0OT0IWOTwtXQC7F7sAzNERRHRJqOfGmaicCHpY
vIvE2yXMObt3ChOG1sjzemL1aI0pNUwFcP3ofWrFLIexyELFHh234NCioCnPgzAD
oEQvGynAO5IdayxhHyaTpAFm9qK5K3WDFpCPWR9j3zUuU19n/X6vMTqwsh4M6h74
vurP3meJEKex0x7ipuWcZLTDrR1AJLGzoz6sxWHDL8fKpPrGcqt6gL9kZ8QJSU9L
H1aPhpk/MyrTNe9AY6R7xzHjHgW034NfN+2K1wSOUQKBgQDbZM0EmNEmVdM7HE7r
fOe62k6wF/8eOEsVASEJ1mNT53qsUbzn0HNvRmrSpwYh43+lg+L+ov+h5JH5b5VR
TNjAb8g/wBaUK3gmqtz/tpDVvmMO5Nu3yIzrFy9wsTN31qB1TOQ6eRwFB66E5ZjE
MCenK8L9/WHpA2IlcAbaacEN6wKBgQD/XlFtPtgoJ8C/jBAzFQi2japDxguJt9Me
N69Gjznl+WQoJ1KGIq1mnAEunfjl1Bm3fqJohHHZv878xls4SdbjNZeYpchpK85V
JQgglfbvGPr01UT4gFBE4aTo3VH6nXEbkTjbC8mLfYLIUugKYJ2Zz2MzLkZPTZ0S
ft+1/IjhSQKBgQCV3sESj9XoCx71tTvQMA4YnYK9VlcnbKsVmSTZlINb0LgDOP8D
mGkSrZbRedl9kuwiw/pvmidojzyMmYX1+LnkkzfHHNAPvbYhK/02DZ/Y82q1xO63
GB/zhG4a3GHdTldkafdKXmseoIW+MR1vf7nGv+U/HjUhOPd1vZZg43dGqwKBgChr
QE4fRU1NxXdL7wB20tM6JvnlLcxVeSfuPmLXpp1c1Np6JtiuQm3cQV+kh1GxOYTO
mVwbon2Jm3Rs3OFS5p09zUnO66Kh2V2mp9uogNYlSQtZejou7QWKBXUKGsClDNMF
ME+TVQosCng0jx+dXTSMG7JtH5nLuhHEXRpL50ppAoGACKOYhm24bzjRhwHikQOB
tY2Nbikk/vVp1SW9LRUopYd+VJFIVynwdDuhItJIDWxrVNqdNk0p7k3JFMfBNdFC
RhYw4c/sXz5Vr8mJdWb0BDtKDd+H1vCKXmGuN0859wZMkd0PzpGm4G7QmFZerYvo
IiWCadGyCso9IwTcZj/rejA=
-----END PRIVATE KEY-----"""

PUBLIC = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2to9A2CN2mi5kTieKFYD
2KVot0CfVT9hRV6TUNmkK8QWZ11ec8aAV2QMUoIVwodLeEV25eDQXPmQX6NOrvJ8
2fT3Zhy68ovtU8cCri9vcPIhHs4RJNzp1Ke2TvDoKuuisQ8fKxKru/G/PniI/YJN
rfhEGn1fYATCvB3+0mKszhRJFNqOYa6G/SseGAC4UAAhI791DyGGViRa2HOX/+O2
K6KSz42HFOz6MWqCVLigWxRVs94TkHttXfbJ3Lil5zqQkyTfsh+YWc+YYBtaUeCs
+ljTtIlTLq0PitcPKeoS7SHX0poc8wi9HsDUiLDVI0OtVuJXamOgVtEXYq+kjiCD
AwIDAQAB
-----END PUBLIC KEY-----
"""


class JWT:
    @staticmethod
    def encode_jwt(
        payload: dict,
        private_key: str = PRIVATE,
        algorithm: str = ALG,
        expire_minutes: int = EXPIRE_M,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
        return encoded

    @staticmethod
    def decode_jwt(
        token: str | bytes,
        public_key: str = PUBLIC,
        algorithm: str = ALG,
    ) -> dict:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded
