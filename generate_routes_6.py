#Creates a new text file "routes6.txt"
text_file = open("routes6.txt", "w")

#Set some starting variables use the decimal equivilant of the hex number
first_nibble = 8192
first = 8192

#Use the hex number for the range
while first_nibble in range (8192,9984):
    first = hex(first_nibble)[2:]
    first_nibble += 1
    second_nibble = 1
    while second_nibble <= 300:
        second = hex(second_nibble)[2:]
        second_nibble += 1
        third_nibble = 1
        while third_nibble <= 300:
            third = hex(third_nibble)[2:]
            third_nibble += 1
            # Juniper
            text_file.write("set routing-options rib inet6.0 static route "+first+":"+second+":"+third+"::/48 next-hop discard\n")
            # Cisco
            #text_file.write("ipv6 route "+first+":"+second+":"+third+"::/48 null0\n")

#Close out the file
text_file.close()
