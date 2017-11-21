def xor_that(sec1, sec2):
    return hex(int(sec1,16)^int(sec2,16))[2:]

def generate_data(array):
    xor_valueSAB = xor_that(array[0],array[1])
    temp = ""
    if(array[5]==0):
        temp = (xor_valueSAB.zfill(4).upper()
        + xor_that(xor_that(xor_valueSAB,array[2]),array[3])).zfill(4).upper()
    else:
        temp = xor_that(xor_valueSAB, array[4]).zfill(4).upper()

    print(temp)


arr1 = ["0C73","80C1","A2A9", "92F5","9B57",0,"8CB2BCEE"]
arr2 = ["27C2","0879","35F6", "1A4D","27BC",1,"0807"]
arr_test = ["D75C","EE87","C568","FCB3","4674",1]

generate_data(arr1)
