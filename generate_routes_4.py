#Creates a new text file "routes4.txt"
text_file = open("routes4.txt", "w")

#Set some starting variables
first_octect = 1
first = 1

while first_octect <= 224:
    first = str(first_octect)
    first_octect += 1
    second_octect = 1
    while second_octect <= 254:
        second = str(second_octect)
        second_octect += 1
        third_octect = 1
        while third_octect <= 254:
            third = str(third_octect)
            third_octect += 1
            # Juniper
            text_file.write("set routing-options static route "+first+"."+second+"."+third+".0/24 next-hop discard\n")
            # NX-OS
            #text_file.write("ip route "+first+"."+second+"."+third+".0/24 null0\n")

            #IOS
            #text_file.write("ip route "+first+"."+second+"."+third+".0 255.255.255.0 null0\n")

#Close out the file
text_file.close()
