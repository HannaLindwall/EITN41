from math import log
from H0 import *
from B1 import *
import base64

def encode_INT(integer):
    # get hexa-representation
    hex_int = format(integer, "x")
    hex_int = pad_hexa(hex_int, len(hex_int))
    # check for padding
    padding = check_padding(hex_int)
    encoded_int = padding + hex_int
    # get nbr of bytes needed to represent the integer
    nbr_bytes = bytes_needed(integer) if padding == "" else bytes_needed(integer) + 1
    # get the lenght and add it before the encoded_int
    encoded_int = get_L(nbr_bytes) + encoded_int

    return "02" + encoded_int

def get_L(nbr_bytes):
    flag = ""
    #bytes needed to represent the integer
    if nbr_bytes > 127:
        #if the integer is represented with more than 127 bytes -> long
        # 8 + # of bytes to represent the lenght
        flag += "8" + format(bytes_needed(nbr_bytes), "x")
    # get the hexa representation of nbr_bytes -> lenght
    L = format(nbr_bytes, "x")
    L = flag + pad_hexa(L, len(L))
    return L

def encode_CERT(nbr_bytes):
    flag = ""
    # the bytes needed for the RSA key
    if nbr_bytes > 127 :
        #if the integer is represented with more than 127 bytes -> long
        # 8 + # of bytes to represent the lenght
        flag += "8" + format(bytes_needed(V), "x")
    L = format(nbr_bytes, "x")
    L = flag + pad_hexa(L, len(L))
    print("cert", L)
    return "30" + L

def check_padding(hex_int):
    check_byte = hex_int[:1]
    padding = "" if int(check_byte, 16) < 8 else "00"
    return padding

def bytes_needed(integer):
    if integer == 0:
        return 1
    return int(log(integer, 256)) + 1

def pad_hexa(hexa_length, length):
    return hexa_length if length % 2 == 0 else "0" + hexa_length

def encode_byte(hexa):
    return hexaToByte(hexa)

def create_RSA_key(p, q, e):
    enc_n = encode_INT(p * q)
    #print(enc_n)
    enc_e = encode_INT(e)
    #print(enc_e)
    phi = (p-1) * (q-1)
    d = mulinv(e, phi)
    enc_d = encode_INT(d)
    #print(enc_d)
    enc_p = encode_INT(p)
    #print(enc_p)
    enc_q = encode_INT(q)
    #print(enc_q)
    exp1 = encode_INT(d % (p-1))
    #print(exp1)
    exp2 = encode_INT(d % (q-1))
    #print(exp2)
    coeff = encode_INT(mulinv(q, p))
    #print(coeff)
    key = "020100" + enc_n + enc_e + enc_d + enc_p + enc_q + exp1 + exp2 + coeff
    cert = "30" + get_L(len(key)//2)
    print(cert)
    print(key)
    RSA_key = cert + key
    #print(RSA_key)
    return base64.b64encode(hexaToByte(RSA_key)).decode("utf-8")


# integer = 161863091426469985001358176493540241719547661391527305133576978132107887717901972545655469921112454527920502763568908799229786534949082469136818503316047702610019730504769581772016806386178260077157969035841180863069299401978140025225333279044855057641079117234814239380100022886557142183337228046784055073741
#integer = 12
integer = 116720652182360431109979778521489477854006953411861232361619542888755896946603852853779646985985297355699948140217125512317873227754506446823326411744016712834988543311290627997501609652214132647038227650669715285123163397877200988577227376243304643185196032682086573923681134752501684597087410553028089195189
#exempel 1
encoded_hexa = encode_INT(integer)
print(encoded_hexa)
#exempel 2
# encoded_byte = encode_byte(encoded_hexa)
# print(encoded_byte)
#exempel 3
# p = 2530368937
# q = 2612592767
# e = 65537

# p = 139721121696950524826588106850589277149201407609721772094240512732263435522747938311240453050931930261483801083660740974606647762343797901776568952627044034430252415109426271529273025919247232149498325412099418785867055970264559033471714066901728022294156913563009971882292507967574638004022912842160046962763
# q = 141482624370070397331659016840167171669762175617573550670131965177212458081250216130985545188965601581445995499595853199665045326236858265192627970970480636850683227427420000655754305398076045013588894161738893242561531526805416653594689480170103763171879023351810966896841177322118521251310975456956247827719
# e = 65537
p = 161659820377723447141827530438498753241658182799832205699712948886237004020923916105117371536892944961485941580268831428570309939627266270844668746409398707644694739210998332574126476603880670020020894682486365727084655607994349177133212406726032729205965483186546293665482064658650475233363695019354811812287
q = 152891096400272376517362879670644842732893606303506658193575202471154195888263155074625015150022008711931757249060502354406554051284576064006513940574577329019388270844265213596679468157969746607773209746484142384544431320878353450419878973041597796079630648912173252448009880094169181976467399978758829469977
e = 65537

# key = create_RSA_key(p, q, e)
# print("key:\n", key)
