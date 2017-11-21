#!/usr/bin/env python
import ipaddress
from pcapfile import savefile
import string

abu_ip = "159.237.13.37"
mix_ip = "94.147.150.188"
mix_file = "cia.log.1337.pcap"
partners = 2

def analyze_mix(m_ip, a_ip, nbr_partners, mix_file):

    testcap = open(mix_file, 'rb')
    capfile = savefile.load_savefile(testcap, layers=2, verbose=True)
    to_ip = []
    from_ip = []
    for pkt in capfile.packets:
        from_ip.append(pkt.packet.payload.src.decode('UTF8'))
        to_ip.append(pkt.packet.payload.dst.decode('UTF8'))
    testcap.close()
    disjoint_sets, other_sets = get_all_sets(from_ip, to_ip, m_ip, a_ip, partners)
    receivers = get_receivers(disjoint_sets, other_sets, abu_ip)
    print(receivers)

def get_all_sets(f_ip, t_ip, mix_ip, an_ip, p):
    disjoint_sets, other_sets, i = [], [], 0
    while i is not None:
        #hitta block med abu's ip
        i = f_ip.index(an_ip, i) #man skickar in i för att skjuta på sökningen
        #hitta meddelnade batchen efter abu's ip
        start = i = f_ip.index(mix_ip,i)
        #hittar nästa mix_ip
        try: end = t_ip.index(mix_ip,i)
        #den har nått slutet
        except: end = None
        #den kör resten ut för att end=None
        receiver_batch = t_ip[start:end]
        i = end
        if(len(disjoint_sets) < p):
            check = True
            if(len(disjoint_sets)==0):
                disjoint_sets.append(set(receiver_batch))
            else :
                for element in disjoint_sets:
                    if(not(element.isdisjoint(receiver_batch))):
                        check = False
                #add to either disjoint set or to the sets which aren't disjoint
                #add_to_this_set becomes a reference to either one of them
                add_to_this_set = disjoint_sets if check else other_sets
                add_to_this_set.append(set(receiver_batch))
        else:
            other_sets.append(set(receiver_batch))
    return disjoint_sets, other_sets

def get_receivers(disjoint_R, all_R, abu):
    for element in all_R:
        index = []
        for j in range(0,len(disjoint_R)):
            if(not(element.isdisjoint(disjoint_R[j]))):
                index.append(j)
        if(len(index)==1):
            disjoint_R[index[0]] = disjoint_R[index[0]] & element
    return disjoint_R


analyze_mix(mix_ip, abu_ip, partners,mix_file)
