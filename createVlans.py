
#!/usr/bin/env python
__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

# list of packages that should be imported for this code to work
import cobra.mit.access
import cobra.mit.session
import cobra.mit.request
import cobra.model.fvns
import cobra.mit.naming
from cobra.internal.codec.xmlcodec import toXMLStr
from itertools import chain




def chapeter_parse_range_list(rngs):
    parts = rngs.split(',')
    items = []
    for part in parts:
        part = part.strip()
        if '-' in part:
            item = part.split('-')
            start = item[0]
            end = item[1]
            rng = range(int(start), int(end)+1)
            for i in rng:
                items.append(i)
        else:
            items.append(int(part))
    return list(set(items))


# log into an APIC and create a directory object
ls = cobra.mit.session.LoginSession('http://10.94.238.68', 'admin', 'cisco123')
md = cobra.mit.access.MoDirectory(ls)
md.login()

# the top level object on which operations will be made
# Confirm the dn below is for your top dn
topDn = cobra.mit.naming.Dn.fromString('uni/infra/vlanns-[placeholder]-static')
topParentDn = topDn.getParent()
topMo = md.lookupByDn(topParentDn)

# build the request using cobra syntax

vlanpool = raw_input("Enter Name of VLAN Pool: ")
vlanraw = raw_input("Enter list of VLANs in free form: ")
vlanlist = chapeter_parse_range_list(vlanraw)
print vlanlist

fvnsVlanInstP = cobra.model.fvns.VlanInstP(topMo, ownerKey=u'', name=unicode(vlanpool), descr=u'', ownerTag=u'', allocMode=u'static')

for vlan in vlanlist:
    cobra.model.fvns.EncapBlk(fvnsVlanInstP, to=u'vlan-{}'.format(vlan), from_=u'vlan-{}'.format(vlan), name=u'', descr=u'', allocMode=u'static')


#fvnsEncapBlk = cobra.model.fvns.EncapBlk(fvnsVlanInstP, to=u'vlan-52', from_=u'vlan-52', name=u'', descr=u'', allocMode=u'static')
#fvnsEncapBlk2 = cobra.model.fvns.EncapBlk(fvnsVlanInstP, to=u'vlan-98', from_=u'vlan-98', name=u'', descr=u'', allocMode=u'static')
#fvnsEncapBlk3 = cobra.model.fvns.EncapBlk(fvnsVlanInstP, to=u'vlan-99', from_=u'vlan-99', name=u'', descr=u'', allocMode=u'static')
#fvnsEncapBlk4 = cobra.model.fvns.EncapBlk(fvnsVlanInstP, to=u'vlan-44', from_=u'vlan-44', name=u'', descr=u'', allocMode=u'static')
#fvnsEncapBlk5 = cobra.model.fvns.EncapBlk(fvnsVlanInstP, to=u'vlan-2', from_=u'vlan-2', name=u'', descr=u'', allocMode=u'static')
#fvnsEncapBlk6 = cobra.model.fvns.EncapBlk(fvnsVlanInstP, to=u'vlan-110', from_=u'vlan-100', name=u'', descr=u'', allocMode=u'static')


# commit the generated code to APIC
print toXMLStr(topMo)
c = cobra.mit.request.ConfigRequest()
c.addMo(topMo)
md.commit(c)

