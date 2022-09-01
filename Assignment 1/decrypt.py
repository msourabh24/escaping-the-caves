alphabet =    'abcdefghijklmnopqrstuvwxyz'
decrypt_map = 'g emftoahpswrbicnyv lu qd '
print("Encrypted: {}".format(alphabet))
print("Decrypted: {}".format(decrypt_map))

cipher_txt = 'omkf pi hdn cmgef icphsck .H krg vphqkc c, fic mco kqgf ioqag eo qfcmckf oq ficpihdn cm .Kg dcgeficu hfcm pi hdn cmklo uuncdgmc oqfc mc kfoq afihqfiokgq c!Fi cpgy cvkc yeg mfio kdck kha cokh kodjuck vn k fofvfo gqpojicmoqli opiyoa of kihsc nccqki oefc ynr2 juhpck. Fi c jhkklgm yok oMxr9V1x ya flofigvffic xvgfck. Fio kokfice'
shifted_txt = 'omkf pi hdn cmgef icphsck .H krg vphqkc c, fic mco kqgf ioqag eo qfcmckf oq ficpihdn cm .Kg dcgeficu hfcm pi hdn cmklo uuncdgmc oqfc mc kfoq afihqfiokgq c!Fi cpgy cvkc yeg mfio kdck kha cokh kodjuck vn k fofvfo gqpojicmoqli opiyoa of kihsc nccqki oefc ynr2 juhpck. Fi c jhkklgm yok oMxr9V1x ya flofigvffic xvgfck. Fio kokfice'
plain_text = ''
print("\nThe original cipher text: \n{}".format(cipher_txt))

# Decrypting the substitution cipher for alphabet
for c in shifted_txt:
    if ord(c)>=ord('a') and ord(c)<=ord('z'):
        plain_text += decrypt_map[ord(c) - ord('a')]
    elif ord(c)>=ord('A') and ord(c)<=ord('Z'):
        plain_text += decrypt_map[ord(c) - ord('A')].upper()
    else:
        plain_text += c
print("\nDecrypted text: \n{}".format(plain_text))

plain_text = ''
# Decrypting the substitution cipher for alphabet
for c in shifted_txt:
    if ord(c)>=ord('a') and ord(c)<=ord('z'):
        plain_text += decrypt_map[ord(c) - ord('a')]
    elif ord(c)>=ord('A') and ord(c)<=ord('Z'):
        plain_text += decrypt_map[ord(c) - ord('A')].upper()
# Decrypting the Caesar cipher for digits by shifting the digit back by 6 places
    elif ord(c)>=ord('0') and ord(c)<=ord('9'):
        plain_text += str((int(c) - 6) % 10)
    else:
        plain_text += c
print("\nDecrypted text after changing digits: \n{}".format(plain_text))

# Shifting the text by 13 places, we get:
plain_text = 'This is the first chamber of the caves. As you can see, there is nothing of interest in the chamber. Some of the later chambers will be more interesting than this one! The code used for this message is a simple substitution cipher in which digits have been shifted by 6 places. The password is iRqy3U5qdgt without the quotes.'

print("\nText after shifting: \n{}".format(plain_text))


password = 'iRqy3U5qdgt'
print("\nPassword: {}".format(password))
