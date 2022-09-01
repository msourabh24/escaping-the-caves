cipher_txt = 'omkf pi hdn cmgef icphsck .H krg vphqkc c, fic mco kqgf ioqag eo qfcmckf oq ficpihdn cm .Kg dcgeficu hfcm pi hdn cmklo uuncdgmc oqfc mc kfoq afihqfiokgq c!Fi cpgy cvkc yeg mfio kdck kha cokh kodjuck vn k fofvfo gqpojicmoqli opiyoa of kihsc nccqki oefc ynr2 juhpck. Fi c jhkklgm yok oMxr9V1x ya flofigvffic xvgfck. Fio kokfice'

# Frequency Analysis of only the alphabet without considering the case
frq = {}
alphabet = 'abcdefghijklmnopqrstuvwxyz'
for i in alphabet:
    frq[i] = cipher_txt.lower().count(i)
cipher_len = 0
for i in frq:
    cipher_len = cipher_len + frq[i]
for i in frq:
    frq[i] = frq[i]*100/cipher_len
frq = sorted(frq.items(), key=lambda k:k[1], reverse=True)
for i in frq:
    print("{}: {:.3f}%".format(i[0],i[1]))
